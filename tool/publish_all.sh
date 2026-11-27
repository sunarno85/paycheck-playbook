#!/data/data/com.termux/files/usr/bin/bash
# Publish ke-12 Reels lewat GitHub Actions setelah Secrets terisi.
set -euo pipefail
TOKEN_FILE="$HOME/token_github"
[ -s "$TOKEN_FILE" ] || TOKEN_FILE="$HOME/.github_token"
TOKEN=$(tr -d '\r\n' < "$TOKEN_FILE")
REPO="sunarno85/paycheck-playbook"

CODE=$(curl -sS -o /dev/null -w '%{http_code}' \
  -H "Authorization: Bearer $TOKEN" -H 'Accept: application/vnd.github+json' \
  -X POST "https://api.github.com/repos/$REPO/actions/workflows/build-reels.yml/dispatches" \
  -d '{"ref":"main","inputs":{"reel":"all","publish":"true"}}')

echo "dispatch: $CODE"
echo "Progress: https://github.com/$REPO/actions"
[ "$CODE" = "204" ] || exit 1
