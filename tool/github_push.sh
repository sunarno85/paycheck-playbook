#!/data/data/com.termux/files/usr/bin/bash
# Membuat repo GitHub dan meng-upload seluruh folder fb-us-money lewat REST API.
# Token dibaca dari ~/.github_token (JANGAN dikirim ke siapa pun).
set -euo pipefail

TOKEN_FILE="$HOME/.github_token"
if [ ! -s "$TOKEN_FILE" ]; then
  echo "ERROR: $TOKEN_FILE belum ada atau kosong."
  echo "Buat PAT di https://github.com/settings/tokens lalu simpan ke file itu."
  exit 1
fi
TOKEN=$(tr -d '\r\n' < "$TOKEN_FILE")
API="https://api.github.com"
HDR=(-H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28")

USER_JSON=$(curl -sS "${HDR[@]}" "$API/user")
OWNER=$(printf '%s' "$USER_JSON" | sed -n 's/.*"login": "\([^"]*\)".*/\1/p' | head -n 1)
if [ -z "$OWNER" ]; then
  echo "ERROR: gagal membaca user. Respons: $(printf '%s' "$USER_JSON" | head -c 300)"
  exit 1
fi

REPO="paycheck-playbook"
echo "Owner: $OWNER | Repo: $REPO"

CREATE=$(curl -sS "${HDR[@]}" -X POST "$API/user/repos" \
  -d '{"name":"paycheck-playbook","private":false,"description":"Paycheck Playbook - US personal finance Facebook automation"}')
if printf '%s' "$CREATE" | grep -q '"full_name"'; then
  echo "Repo berhasil dibuat."
elif printf '%s' "$CREATE" | grep -qi 'already exists'; then
  echo "Repo sudah ada — lanjut update file."
else
  echo "ERROR saat buat repo: $(printf '%s' "$CREATE" | head -c 400)"
  exit 1
fi

ROOT="$HOME/fb-us-money"
COUNT=0
FAILED=0
while IFS= read -r f; do
  REL="${f#$ROOT/}"
  B64=$(base64 -w0 "$f")
  PAYLOAD=$(printf '{"message":"add %s","content":"%s","branch":"main"}' "$REL" "$B64")
  RESULT=$(curl -sS "${HDR[@]}" -X PUT "$API/repos/$OWNER/$REPO/contents/$REL" -d "$PAYLOAD")

  if ! printf '%s' "$RESULT" | grep -q '"content"'; then
    SHA=$(curl -sS "${HDR[@]}" "$API/repos/$OWNER/$REPO/contents/$REL" | sed -n 's/.*"sha": "\([^"]*\)".*/\1/p' | head -n 1)
    if [ -n "$SHA" ]; then
      PAYLOAD=$(printf '{"message":"update %s","content":"%s","sha":"%s","branch":"main"}' "$REL" "$B64" "$SHA")
      RESULT=$(curl -sS "${HDR[@]}" -X PUT "$API/repos/$OWNER/$REPO/contents/$REL" -d "$PAYLOAD")
    fi
  fi

  if printf '%s' "$RESULT" | grep -q '"content"'; then
    COUNT=$((COUNT + 1))
    echo "  OK  $REL"
  else
    FAILED=$((FAILED + 1))
    echo "  GAGAL $REL -> $(printf '%s' "$RESULT" | head -c 160)"
  fi
done < <(find "$ROOT" -type f ! -path '*/output/*' ! -path '*/assets/_tmp/*' | sort)

echo ""
echo "Selesai: $COUNT file berhasil, $FAILED gagal."
echo "Repo: https://github.com/$OWNER/$REPO"
echo "Workflow: https://github.com/$OWNER/$REPO/actions"
