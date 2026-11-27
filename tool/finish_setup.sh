#!/data/data/com.termux/files/usr/bin/bash
# Selesaikan setup setelah PAT memiliki scope: repo + workflow.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOKEN_FILE="$HOME/token_github"
[ -s "$TOKEN_FILE" ] || TOKEN_FILE="$HOME/.github_token"
TOKEN=$(tr -d '\r\n' < "$TOKEN_FILE")

SCOPES=$(curl -sS -D - -o /dev/null -H "Authorization: Bearer $TOKEN" \
  https://api.github.com/user | tr -d '\r' | sed -n 's/^x-oauth-scopes: *//Ip' | tr -d ' ')
case ",$SCOPES," in
  *,workflow,*) ;;
  *)
    echo "Token masih belum punya scope 'workflow'."
    echo "Buka https://github.com/settings/tokens → token fb-paycheck → centang 'workflow' → Save."
    echo "Scope saat ini: $SCOPES"
    exit 1
    ;;
esac

OWNER=$(curl -sS -H "Authorization: Bearer $TOKEN" https://api.github.com/user \
  | sed -n 's/.*"login": "\([^"]*\)".*/\1/p' | head -n 1)
REPO="paycheck-playbook"
API="https://api.github.com/repos/$OWNER/$REPO"

cd "$ROOT"
git add .github/workflows/build-reels.yml
git commit -m 'Add GitHub Actions workflow' >/dev/null 2>&1 || true
GIT_TERMINAL_PROMPT=0 git push origin main

# Jalankan uji coba R1 tanpa publish.
curl -sS -o /dev/null -w 'dispatch: %{http_code}\n' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Accept: application/vnd.github+json' \
  -X POST "$API/actions/workflows/build-reels.yml/dispatches" \
  -d '{"ref":"main","inputs":{"reel":"R1","publish":"false"}}'

echo "Cek progres: https://github.com/$OWNER/$REPO/actions"
echo "Workflow URL: $API/actions/workflows/build-reels.yml"
