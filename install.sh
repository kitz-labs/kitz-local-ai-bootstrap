#!/usr/bin/env bash
set -euo pipefail

if [[ "$(uname -s)" != "Darwin" ]]; then
  printf 'KITZ Local AI requires macOS.\n' >&2
  exit 1
fi

if [[ "$(uname -m)" != "arm64" ]]; then
  printf 'KITZ Local AI requires Apple Silicon (arm64).\n' >&2
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  printf 'curl is required but was not found.\n' >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

if ! command -v brew >/dev/null 2>&1; then
  printf 'Homebrew is missing; installing it now.\n'
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  if [[ -x /opt/homebrew/bin/brew ]]; then
    eval "$(/opt/homebrew/bin/brew shellenv)"
  fi
fi

if ! command -v git >/dev/null 2>&1; then
  printf 'Git is missing; installing it now.\n'
  brew install git
fi

if ! command -v git >/dev/null 2>&1; then
  printf 'Git installation failed or git is still unavailable.\n' >&2
  exit 1
fi

if [[ -f "$HOME/.zshrc" ]] && grep -q 'localai-neustart' "$HOME/.zshrc"; then
  printf 'Existing localai-neustart detected and will be preserved.\n'
fi

install_root="${KITZ_INSTALL_ROOT:-$HOME/KITZLABS-AI/agent-core}"
script_dir=""
if [[ -n "${BASH_SOURCE[0]:-}" && -f "${BASH_SOURCE[0]}" ]]; then
  script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
fi

if [[ -n "$script_dir" && -f "$script_dir/pyproject.toml" ]]; then
  source_repo="$script_dir"
else
  repo_url="${KITZ_REPO_URL:-}"
  repo_ref="${KITZ_REPO_REF:-}"
  if [[ -z "$repo_url" ]]; then
    printf 'KITZ_REPO_URL must be set when install.sh is executed through a pipe.\n' >&2
    exit 1
  fi

  mkdir -p "$(dirname "$install_root")"
  if [[ -d "$install_root/.git" ]]; then
    if [[ -n "$repo_ref" ]]; then
      git -C "$install_root" fetch --depth 1 origin "$repo_ref"
      git -C "$install_root" checkout --detach FETCH_HEAD
    else
      git -C "$install_root" fetch --prune
      git -C "$install_root" pull --ff-only
    fi
  else
    if [[ -n "$repo_ref" ]]; then
      git clone --branch "$repo_ref" --depth 1 "$repo_url" "$install_root"
    else
      git clone "$repo_url" "$install_root"
    fi
  fi
  source_repo="$install_root"
fi

if [[ "$source_repo" != "$install_root" ]]; then
  mkdir -p "$(dirname "$install_root")"
  if [[ ! -e "$install_root" ]]; then
    git clone "$source_repo" "$install_root"
  elif [[ -d "$install_root/.git" ]]; then
    git -C "$install_root" fetch --prune || true
  fi
  source_repo="$install_root"
fi

cd "$source_repo"
uv tool install --force "$source_repo"
uv run --no-dev kitz-installer install "$@"
