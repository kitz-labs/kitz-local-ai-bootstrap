#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
cd "$ROOT"

REPO_NAME="${KITZ_REPO_NAME:-kitz-local-ai-bootstrap}"
TAG="${KITZ_RELEASE_TAG:-v1.0.0}"
RELEASE_FILE="$ROOT/RELEASE_INSTALL_COMMAND.txt"

if [[ -n "$(git status --porcelain)" ]]; then
  printf 'Refusing to publish: working tree is dirty. Commit or stash changes first.\n' >&2
  exit 1
fi

# Publishing is allowed only from a fully passing local build.
python3 -m pytest -q
bash -n install.sh

# Reject obvious plaintext production credential formats in tracked files.
if git grep -nE '(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})' -- . \
  ':(exclude)tests/**' >/dev/null 2>&1; then
  printf 'Refusing to publish: a tracked file appears to contain a plaintext credential.\n' >&2
  exit 1
fi

OWNER="$(gh api user --jq .login)"
if [[ -z "$OWNER" || ! "$OWNER" =~ ^[A-Za-z0-9-]+$ ]]; then
  printf 'Could not determine a valid authenticated GitHub owner.\n' >&2
  exit 1
fi

REPO="$OWNER/$REPO_NAME"
EXPECTED_HTTPS="https://github.com/$REPO.git"
EXPECTED_SSH="git@github.com:$REPO.git"

if gh repo view "$REPO" >/dev/null 2>&1; then
  origin="$(git remote get-url origin 2>/dev/null || true)"
  if [[ "$origin" != "$EXPECTED_HTTPS" && "$origin" != "$EXPECTED_SSH" ]]; then
    printf 'Refusing to publish: %s already exists but this checkout is not connected to it.\n' "$REPO" >&2
    exit 1
  fi
  git push origin HEAD
else
  existing_origin="$(git remote get-url origin 2>/dev/null || true)"
  if [[ -n "$existing_origin" && "$existing_origin" != "$EXPECTED_HTTPS" && "$existing_origin" != "$EXPECTED_SSH" ]]; then
    printf 'Refusing to create repository: current origin points to unrelated repository %s.\n' "$existing_origin" >&2
    exit 1
  fi
  gh repo create "$REPO" --public --source . --remote origin --push
fi

if git rev-parse "$TAG" >/dev/null 2>&1; then
  tag_commit="$(git rev-parse "$TAG^{commit}")"
  head_commit="$(git rev-parse HEAD)"
  if [[ "$tag_commit" != "$head_commit" ]]; then
    printf 'Refusing to move existing tag %s from %s to %s.\n' "$TAG" "$tag_commit" "$head_commit" >&2
    exit 1
  fi
else
  git tag -a "$TAG" -m "KITZ Local AI $TAG"
fi

git push origin "$TAG"

RAW_URL="https://raw.githubusercontent.com/$OWNER/$REPO_NAME/$TAG/install.sh"
tmp_installer="$(mktemp)"
trap 'rm -f "$tmp_installer"' EXIT
curl -fsSL "$RAW_URL" -o "$tmp_installer"

local_hash="$(shasum -a 256 install.sh | awk '{print $1}')"
remote_hash="$(shasum -a 256 "$tmp_installer" | awk '{print $1}')"
if [[ "$local_hash" != "$remote_hash" ]]; then
  printf 'Published installer hash mismatch. Local=%s Remote=%s\n' "$local_hash" "$remote_hash" >&2
  exit 1
fi

COMMAND="KITZ_REPO_URL=https://github.com/$OWNER/$REPO_NAME.git KITZ_REPO_REF=$TAG bash -c \"\$(curl -fsSL $RAW_URL)\""
printf '%s\n' "$COMMAND" > "$RELEASE_FILE"
printf 'Verified KITZ Local AI release %s.\n' "$TAG"
printf '%s\n' "$COMMAND"
