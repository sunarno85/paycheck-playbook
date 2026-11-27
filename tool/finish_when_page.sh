#!/data/data/com.termux/files/usr/bin/bash
# Tunggu sampai Page "Paycheck Playbook" muncul, lalu lanjutkan semuanya otomatis.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOKEN_FILE="$HOME/facebook_token"
[ -s "$TOKEN_FILE" ] || { echo "ERROR: $TOKEN_FILE kosong"; exit 1; }
TOKEN=$(tr -d '\r\n' < "$TOKEN_FILE")
LOG="$ROOT/tool/finish_when_page.log"

for i in $(seq 1 90); do
  JSON=$(curl -sS -G https://graph.facebook.com/me/accounts \
    --data-urlencode "access_token=$TOKEN" \
    --data-urlencode 'fields=id,name,access_token') || JSON="{}"
  MATCH=$(printf '%s' "$JSON" | python -c '
import sys, json
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)
for p in d.get("data", []):
    if "paycheck playbook" in p.get("name", "").lower():
        print(p["id"], p.get("access_token", ""))
        break
' 2>/dev/null || true)

  if [ -n "$MATCH" ]; then
    read -r PAGE_ID PAGE_TOKEN <<<"$MATCH"
    echo "[$(date)] Page ditemukan: $PAGE_ID" >> "$LOG"
    python - "$PAGE_ID" "$PAGE_TOKEN" <<'PY'
import sys, pathlib
p = pathlib.Path.home() / "fb-us-money/tool/config.env"
lines = p.read_text().splitlines() if p.exists() else []
updates = {"PAGE_ID": sys.argv[1], "PAGE_ACCESS_TOKEN": sys.argv[2]}
out, seen = [], set()
for line in lines:
    key = line.split("=", 1)[0]
    if key in updates:
        out.append(f"{key}={updates[key]}")
        seen.add(key)
    else:
        out.append(line)
for key, value in updates.items():
    if key not in seen:
        out.append(f"{key}={value}")
p.write_text("\n".join(out) + "\n")
PY
    chmod 600 "$ROOT/tool/config.env"
    echo "[$(date)] config.env terisi" >> "$LOG"
    bash "$ROOT/tool/set_secrets.sh" >> "$LOG" 2>&1 || true
    bash "$ROOT/tool/publish_all.sh" >> "$LOG" 2>&1 || true
    echo "SELESAI — lihat $LOG"
    exit 0
  fi
  echo "[$(date)] cek $i: Page belum ada" >> "$LOG"
  sleep 10
done

echo "Page tidak muncul dalam 15 menit. Lihat $LOG"
exit 1
