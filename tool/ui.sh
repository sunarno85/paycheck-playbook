#!/data/data/com.termux/files/usr/bin/bash
# Helper UI automation lewat adb (cocok dipanggil dari sesi non-interaktif).
set -euo pipefail
TMP=${TMPDIR:-/data/data/com.termux/files/usr/tmp}
XML="$TMP/fb_ui.xml"

dump() {
  adb shell uiautomator dump /sdcard/window.xml >/dev/null 2>&1
  adb pull /sdcard/window.xml "$XML" >/dev/null 2>&1
}

bounds_center() {
  local line="$1"
  local b x1 y1 x2 y2
  b=$(printf '%s' "$line" | sed -n 's/.*bounds="\[\([0-9]\+\),\([0-9]\+\)\]\[\([0-9]\+\),\([0-9]\+\)\]".*/\1 \2 \3 \4/p')
  [ -n "$b" ] || return 1
  read -r x1 y1 x2 y2 <<<"$b"
  echo $(( (x1 + x2) / 2 )) $(( (y1 + y2) / 2 ))
}

case "${1:-help}" in
  texts)
    dump
    grep -o 'text="[^"]*"' "$XML" | sed 's/text="//;s/"$//' | grep -v '^$' | sort -u
    ;;
  tree)
    dump
    tr '>' '>\n' < "$XML" | grep -E 'text="[^"]+"' | sed 's/^ *//'
    ;;
  tap-text)
    dump
    NEEDLE="$2"
    LINE=$(grep -F "text=\"$NEEDLE\"" "$XML" | head -n 1 || true)
    if [ -z "$LINE" ]; then
      LINE=$(grep -iF "$NEEDLE" "$XML" | head -n 1 || true)
    fi
    [ -n "$LINE" ] || { echo "teks tidak ditemukan: $NEEDLE"; exit 1; }
    read -r X Y < <(bounds_center "$LINE")
    echo "tap ($X,$Y) untuk '$NEEDLE'"
    adb shell input tap "$X" "$Y"
    ;;
  tap-id)
    dump
    LINE=$(grep -F "resource-id=\"$2\"" "$XML" | head -n 1 || true)
    [ -n "$LINE" ] || { echo "id tidak ditemukan: $2"; exit 1; }
    read -r X Y < <(bounds_center "$LINE")
    echo "tap ($X,$Y) untuk id $2"
    adb shell input tap "$X" "$Y"
    ;;
  type)
    ESC=$(printf '%s' "$2" | sed 's/ /%s/g; s/&/\\&/g')
    adb shell input text "$ESC"
    ;;
  key)
    adb shell input keyevent "$2"
    ;;
  open)
    adb shell am start -a android.intent.action.VIEW -d "$2" >/dev/null
    ;;
  shot)
    adb shell screencap -p /sdcard/fb_shot.png >/dev/null
    adb pull /sdcard/fb_shot.png "$TMP/fb_shot.png" >/dev/null
    echo "$TMP/fb_shot.png"
    ;;
  wait-text)
    for i in $(seq 1 "${3:-30}"); do
      dump
      if grep -qiF "$2" "$XML"; then echo "muncul: $2"; exit 0; fi
      sleep 1
    done
    echo "tidak muncul: $2"; exit 1
    ;;
  *)
    echo "Pakai: ui.sh texts | tree | tap-text <teks> | tap-id <id> | type <teks> | key <kode> | open <url> | shot | wait-text <teks> [detik]"
    ;;
esac
