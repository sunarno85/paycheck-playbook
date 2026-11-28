#!/data/data/com.termux/files/usr/bin/bash
# Jalankan Control Panel di 127.0.0.1:8765.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if curl -s -o /dev/null http://127.0.0.1:8765/; then
  echo "Control Panel sudah berjalan: http://127.0.0.1:8765"
  exit 0
fi

if command -v termux-wake-lock >/dev/null 2>&1; then
  termux-wake-lock || true
fi

nohup python "$ROOT/tool/control_panel.py" > "$ROOT/tool/control_panel.log" 2>&1 &
echo $! > "$ROOT/tool/control_panel.pid"
echo "Control Panel aktif: http://127.0.0.1:8765"
