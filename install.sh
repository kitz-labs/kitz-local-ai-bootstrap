#!/usr/bin/env bash
set -euo pipefail

printf '\n==============================================\n'
printf ' KITZ Local AI v1.0.2 Bootstrap\n'
printf '==============================================\n\n'

fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

[[ "$(uname -s)" == "Darwin" ]] || fail 'KITZ Local AI requires macOS.'
[[ "$(uname -m)" == "arm64" ]] || fail 'KITZ Local AI requires Apple Silicon (arm64).'
command -v curl >/dev/null 2>&1 || fail 'curl is required but was not found.'

repo_url="${KITZ_REPO_URL:-https://github.com/kitz-labs/kitz-local-ai-bootstrap.git}"
repo_ref="${KITZ_REPO_REF:-v1.0.2}"
raw_base="${KITZ_RAW_BASE:-https://raw.githubusercontent.com/kitz-labs/kitz-local-ai-bootstrap/${repo_ref}}"
install_root="${KITZ_INSTALL_ROOT:-$HOME/KITZLABS-AI/agent-core}"
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/kitz-bootstrap.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT

if ! command -v uv >/dev/null 2>&1; then
  info '[bootstrap] Installing uv...'
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi
command -v uv >/dev/null 2>&1 || fail 'uv installation failed.'

if ! command -v brew >/dev/null 2>&1; then
  info '[bootstrap] Installing Homebrew...'
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  [[ -x /opt/homebrew/bin/brew ]] && eval "$(/opt/homebrew/bin/brew shellenv)"
fi
command -v brew >/dev/null 2>&1 || fail 'Homebrew installation failed.'

if ! command -v git >/dev/null 2>&1; then
  info '[bootstrap] Installing Git...'
  brew install git
fi
command -v git >/dev/null 2>&1 || fail 'Git installation failed.'

if [[ -f "$HOME/.zshrc" ]] && grep -q 'localai-neustart' "$HOME/.zshrc"; then
  info '[bootstrap] Existing localai-neustart detected and will be preserved.'
fi

mkdir -p "$(dirname "$install_root")"
if [[ -e "$install_root" && ! -d "$install_root/.git" ]]; then
  backup="${install_root}.pre-kitz-$(date +%Y%m%d-%H%M%S)"
  info "[bootstrap] Existing non-Git install root detected; backing up to: $backup"
  mv "$install_root" "$backup"
fi

if [[ -d "$install_root/.git" ]]; then
  info "[bootstrap] Updating source to ${repo_ref}..."
  git -C "$install_root" fetch --depth 1 origin "$repo_ref"
  git -C "$install_root" checkout --detach FETCH_HEAD
else
  info "[bootstrap] Cloning ${repo_ref}..."
  git clone --branch "$repo_ref" --depth 1 "$repo_url" "$install_root"
fi

expected_sha() {
  case "$1" in
    kitz_cli) echo '31959c29bbe2df367a49b30683d08e014ae4c132847cf2ce66a3e09532889d98' ;;
    kitz_control) echo 'aa8b0076f7142a2dd316a860c182f07a4bea734df3ccbb39f1930337dfee8f04' ;;
    kitz_core) echo '245a8e848d6dd6683e2833550e7fb194803456deb14c463b6eb85c0884867ecb' ;;
    kitz_installer) echo '81dcf11d0bbb2bccc38bb44797e059093fd99be7f6ea1896c79d263bdc540717' ;;
    kitz_knowledge) echo '249342f7454fc841f4f1f65143c29886f074b1d778eaaa2fca23e6a2ea6d0619' ;;
    kitz_media) echo '2ba2f43e50c143b2bbb115162fcc36c98b85a8bde9e27239f441e5655cd5db36' ;;
    kitz_ops) echo 'db1a39a48dd3952f765022d30d65ed76360440d08700edc3f9631b5772e4726e' ;;
    kitz_tools) echo 'b959dc002b0421d4342b5922a663da0a92061c849cbe9e2e061c62bc866403b0' ;;
    *) fail "Unknown runtime package: $1" ;;
  esac
}
packages=(kitz_cli kitz_control kitz_core kitz_installer kitz_knowledge kitz_media kitz_ops kitz_tools)

decode_b64() {
  local input="$1" output="$2"
  if base64 -D < "$input" > "$output" 2>/dev/null; then
    return 0
  fi
  base64 --decode < "$input" > "$output" 2>/dev/null || fail "Could not decode $input"
}

fetch_package_b64() {
  local pkg="$1" out="$2"
  case "$pkg" in
    kitz_knowledge)
      : > "$out"
      for n in 00 01 02 03; do
        curl -fsSL "${raw_base}/release-chunks/kitz_knowledge.part${n}" >> "$out" || fail "Download failed: kitz_knowledge.part${n}"
      done
      ;;
    kitz_tools)
      : > "$out"
      for n in 00 01 02; do
        curl -fsSL "${raw_base}/release-chunks/kitz_tools.part${n}" >> "$out" || fail "Download failed: kitz_tools.part${n}"
      done
      ;;
    *)
      curl -fsSL "${raw_base}/release-packages/${pkg}.b64" -o "$out" || fail "Download failed: ${pkg}.b64"
      ;;
  esac
}

info '[bootstrap] Downloading and verifying KITZ runtime packages...'
rm -rf "$install_root/src"
mkdir -p "$install_root/src"

idx=0
for pkg in "${packages[@]}"; do
  idx=$((idx + 1))
  b64="$tmpdir/${pkg}.b64"
  tgz="$tmpdir/${pkg}.tar.gz"
  fetch_package_b64 "$pkg" "$b64"
  decode_b64 "$b64" "$tgz"
  actual="$(shasum -a 256 "$tgz" | awk '{print $1}')"
  expected="$(expected_sha "$pkg")"
  [[ "$actual" == "$expected" ]] || fail "SHA-256 mismatch for $pkg (expected $expected, got $actual)"
  tar -xzf "$tgz" -C "$install_root"
  [[ -d "$install_root/src/$pkg" ]] || fail "Package extraction failed: $pkg"
  info "[$idx/8] $pkg verified"
done

[[ -f "$install_root/src/kitz_installer/main.py" ]] || fail 'KITZ installer entrypoint is missing after extraction.'

cd "$install_root"
info '[bootstrap] Installing KITZ command suite...'
uv tool install --force "$install_root"

info '[bootstrap] Installing Browser Use in an isolated environment...'
if uv tool install --force 'browser-use[core]==0.13.8'; then
  info '[bootstrap] Browser Use isolated environment ready.'
else
  info '[bootstrap] WARNING: Browser Use optional environment could not be installed; Playwright remains available.'
fi

info '[bootstrap] Starting system installer...'
uv run --no-dev kitz-installer install "$@"

printf '\n==============================================\n'
printf ' KITZ Local AI bootstrap completed\n'
printf ' Run: kitz-status\n'
printf '==============================================\n'
