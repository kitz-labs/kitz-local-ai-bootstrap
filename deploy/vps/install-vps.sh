#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  printf 'install-vps.sh must run as root via sudo.\n' >&2
  exit 1
fi

prepare_age=0
bundle=""
secrets_file=""
allowed_chat_ids=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --prepare-age)
      prepare_age=1
      shift
      ;;
    --bundle)
      bundle="${2:-}"
      shift 2
      ;;
    --secrets)
      secrets_file="${2:-}"
      shift 2
      ;;
    --allowed-chat-ids)
      allowed_chat_ids="${2:-}"
      shift 2
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      exit 2
      ;;
  esac
done

install_base_packages() {
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y ca-certificates curl python3 python3-venv age
  if ! command -v sops >/dev/null 2>&1; then
    if ! apt-get install -y sops; then
      arch="$(dpkg --print-architecture)"
      case "$arch" in
        amd64) sops_arch="amd64" ;;
        arm64) sops_arch="arm64" ;;
        *) printf 'Unsupported VPS architecture for SOPS: %s\n' "$arch" >&2; exit 1 ;;
      esac
      curl -fsSL \
        "https://github.com/getsops/sops/releases/download/v3.9.4/sops-v3.9.4.linux.${sops_arch}" \
        -o /usr/local/bin/sops
      chmod 0755 /usr/local/bin/sops
    fi
  fi
}

ensure_service_account() {
  if ! id kitz-control >/dev/null 2>&1; then
    useradd --system --create-home --home-dir /var/lib/kitz-control \
      --shell /usr/sbin/nologin kitz-control
  fi
  install -d -o kitz-control -g kitz-control -m 0750 /var/lib/kitz-control
  install -d -o root -g kitz-control -m 0750 /etc/kitz-control
  install -d -o root -g kitz-control -m 0750 /etc/kitz-control/age
  install -d -o root -g root -m 0755 /opt/kitz-control
  install -d -o root -g root -m 0755 /usr/local/libexec
}

prepare_age_identity() {
  install_base_packages
  ensure_service_account
  key_file=/etc/kitz-control/age/keys.txt
  if [[ ! -s "$key_file" ]]; then
    age-keygen -o "$key_file" >/dev/null
    chown root:kitz-control "$key_file"
    chmod 0640 "$key_file"
  fi
  age-keygen -y "$key_file"
}

if [[ "$prepare_age" -eq 1 ]]; then
  prepare_age_identity
  exit 0
fi

if [[ -z "$bundle" || -z "$secrets_file" ]]; then
  printf '%s\n' '--bundle and --secrets are required for final installation.' >&2
  exit 2
fi
if [[ ! -f "$bundle" || ! -f "$secrets_file" ]]; then
  printf 'Bundle or encrypted secrets file is missing.\n' >&2
  exit 2
fi

install_base_packages
ensure_service_account

if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sh
fi

tailscale_ip="$(tailscale ip -4 | head -n 1 | tr -d '[:space:]')"
if [[ -z "$tailscale_ip" ]]; then
  printf 'Tailscale is installed but not connected. Run tailscale up, then rerun the installer.\n' >&2
  exit 1
fi

app_root=/opt/kitz-control/app
rm -rf "$app_root.new"
install -d -o root -g root -m 0755 "$app_root.new"
tar -xzf "$bundle" -C "$app_root.new"
rm -rf "$app_root"
mv "$app_root.new" "$app_root"

python3 -m venv /opt/kitz-control/venv
/opt/kitz-control/venv/bin/pip install --disable-pip-version-check --upgrade pip
/opt/kitz-control/venv/bin/pip install --disable-pip-version-check --no-deps "$app_root"
/opt/kitz-control/venv/bin/pip install --disable-pip-version-check \
  'pydantic>=2.10' 'fastapi>=0.115' 'httpx>=0.28' 'uvicorn>=0.30' \
  'python-telegram-bot>=22.0,<23'

install -m 0640 -o root -g kitz-control "$secrets_file" /etc/kitz-control/secrets.enc.yaml
key_file=/etc/kitz-control/age/keys.txt
if [[ ! -s "$key_file" ]]; then
  printf 'VPS age identity is missing; run --prepare-age first.\n' >&2
  exit 1
fi

cat > /etc/kitz-control/runtime.env <<EOF
KITZ_CONTROL_ROOT=/var/lib/kitz-control
KITZ_CONTROL_BIND=${tailscale_ip}
KITZ_CONTROL_PORT=8765
KITZ_SECRETS_FILE=/etc/kitz-control/secrets.enc.yaml
KITZ_TELEGRAM_ALLOWED_CHAT_IDS=${allowed_chat_ids}
SOPS_AGE_KEY_FILE=/etc/kitz-control/age/keys.txt
EOF
chown root:kitz-control /etc/kitz-control/runtime.env
chmod 0640 /etc/kitz-control/runtime.env

cat > /usr/local/libexec/kitz-control-start <<'WRAPPER'
#!/usr/bin/env bash
set -euo pipefail
set -a
source /etc/kitz-control/runtime.env
set +a
node_tokens_json="$(sops --decrypt --extract '["node_tokens_json"]' "$KITZ_SECRETS_FILE")"
export KITZ_NODE_TOKENS_JSON="$node_tokens_json"
exec /opt/kitz-control/venv/bin/kitz-control-api
WRAPPER
chmod 0755 /usr/local/libexec/kitz-control-start

cat > /usr/local/libexec/kitz-telegram-start <<'WRAPPER'
#!/usr/bin/env bash
set -euo pipefail
set -a
source /etc/kitz-control/runtime.env
set +a
telegram_token="$(sops --decrypt --extract '["telegram_token"]' "$KITZ_SECRETS_FILE")"
if [[ -z "$telegram_token" ]]; then
  printf 'Telegram is not configured; no token present.\n'
  exit 0
fi
export KITZ_TELEGRAM_TOKEN="$telegram_token"
exec /opt/kitz-control/venv/bin/kitz-telegram-bot
WRAPPER
chmod 0755 /usr/local/libexec/kitz-telegram-start

install -m 0644 "$app_root/deploy/vps/kitz-control.service" /etc/systemd/system/kitz-control.service
install -m 0644 "$app_root/deploy/vps/kitz-telegram.service" /etc/systemd/system/kitz-telegram.service

systemctl daemon-reload
systemctl enable --now kitz-control.service

telegram_token="$(SOPS_AGE_KEY_FILE="$key_file" sops --decrypt --extract '["telegram_token"]' /etc/kitz-control/secrets.enc.yaml)"
if [[ -n "$telegram_token" && -n "$allowed_chat_ids" ]]; then
  systemctl enable --now kitz-telegram.service
else
  systemctl disable --now kitz-telegram.service >/dev/null 2>&1 || true
fi

printf 'KITZ Control Node installed on Tailscale address %s:8765\n' "$tailscale_ip"
