#!/data/data/com.termux/files/usr/bin/bash
# Publish 12 Reels dari folder hasil build (mis. artifact GitHub Actions) ke Page.
# Pakai alur rupload yang terverifikasi: start -> raw upload -> finish.
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VIDEO_DIR="${1:?Pemakaian: publish_from_dir.sh /path/ke/folder-output}"
CFG="$ROOT/tool/config.env"
LOG="$ROOT/tool/publish_from_dir.log"

PAGE=$(grep -m1 '^PAGE_ID=' "$CFG" | cut -d= -f2-)
TOK=$(grep -m1 '^PAGE_ACCESS_TOKEN=' "$CFG" | cut -d= -f2-)
[ -n "$PAGE" ] && [ -n "$TOK" ] || { echo "ERROR: config.env kosong"; exit 1; }
[ -d "$VIDEO_DIR" ] || { echo "ERROR: folder tidak ada: $VIDEO_DIR"; exit 1; }

fail=0
for n in $(seq 1 12); do
  reel="R$n"
  video="$VIDEO_DIR/$reel.mp4"
  paket="$VIDEO_DIR/${reel}_paket.md"
  if [ ! -s "$video" ] || [ ! -s "$paket" ]; then
    echo "[$(date)] $reel ERROR: file tidak lengkap" >> "$LOG"
    fail=$((fail + 1))
    continue
  fi

  caption=$(awk '
    /^## Caption siap paste/ {insec=1; next}
    insec && /^```/ {if (fence==0) {fence=1; next} else exit}
    insec && fence==1 {print}
  ' "$paket")
  if [ -z "$caption" ]; then
    echo "[$(date)] $reel ERROR: caption kosong" >> "$LOG"
    fail=$((fail + 1))
    continue
  fi

  start=$(curl -sS -X POST "https://graph.facebook.com/$PAGE/video_reels" \
    -d "upload_phase=start" -d "access_token=$TOK")
  vid=$(START_JSON="$start" python -c 'import os,json; print(json.loads(os.environ["START_JSON"]).get("video_id",""))' 2>/dev/null)
  url=$(START_JSON="$start" python -c 'import os,json; print(json.loads(os.environ["START_JSON"]).get("upload_url",""))' 2>/dev/null)
  if [ -z "$vid" ] || [ -z "$url" ]; then
    echo "[$(date)] $reel ERROR start: ${start:0:200}" >> "$LOG"
    fail=$((fail + 1))
    continue
  fi

  size=$(stat -c %s "$video")
  upload=$(curl -sS -X POST \
    -H "Authorization: OAuth $TOK" \
    -H "Offset: 0" \
    -H "X-Entity-Length: $size" \
    -H "Content-Type: application/octet-stream" \
    --data-binary "@$video" "$url")
  if ! printf '%s' "$upload" | grep -q '"success"[[:space:]]*:[[:space:]]*true'; then
    echo "[$(date)] $reel ERROR upload: ${upload:0:200}" >> "$LOG"
    fail=$((fail + 1))
    continue
  fi

  finish=$(curl -sS -X POST "https://graph.facebook.com/$PAGE/video_reels" \
    --data-urlencode "access_token=$TOK" \
    --data-urlencode "upload_phase=finish" \
    --data-urlencode "video_id=$vid" \
    --data-urlencode "video_state=PUBLISHED" \
    --data-urlencode "description=$caption")
  post=$(FINISH_JSON="$finish" python -c 'import os,json; d=json.loads(os.environ["FINISH_JSON"]); print(d.get("post_id","")); assert "error" not in d' 2>/dev/null)
  if [ -z "$post" ]; then
    echo "[$(date)] $reel ERROR finish: ${finish:0:250}" >> "$LOG"
    fail=$((fail + 1))
    continue
  fi
  echo "[$(date)] $reel OK video=$vid post=$post" >> "$LOG"
  echo "$reel OK post=$post"
  sleep 3
done

echo "Selesai. Gagal: $fail. Log: $LOG"
[ "$fail" -eq 0 ]
