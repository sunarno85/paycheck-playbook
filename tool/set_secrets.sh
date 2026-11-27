#!/data/data/com.termux/files/usr/bin/bash
# Isi GitHub Actions Secrets dari tool/config.env lokal.
# Nilai kosong dilewati. Token GitHub dibaca dari ~/token_github.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOKEN_FILE="$HOME/token_github"
[ -s "$TOKEN_FILE" ] || TOKEN_FILE="$HOME/.github_token"
export GH_TOKEN=$(tr -d '\r\n' < "$TOKEN_FILE")
export REPO="sunarno85/paycheck-playbook"

set -a
# shellcheck disable=SC1091
source "$ROOT/tool/config.env"
set +a

for KEY in PEXELS_API_KEY PAGE_ID PAGE_ACCESS_TOKEN; do
  VALUE="${!KEY:-}"
  if [ -n "$VALUE" ]; then
    gh secret set "$KEY" --repo "$REPO" --body "$VALUE"
    echo "secret $KEY: ter-set"
  else
    echo "secret $KEY: kosong, dilewati"
  fi
done

echo "Cek: https://github.com/$REPO/settings/secrets/actions"
