#!/data/data/com.termux/files/usr/bin/bash
# Hubungkan adb di Termux ke perangkat sendiri lewat Wireless Debugging.
# Pemakaian: bash adb_connect.sh <port-pairing> <kode-6-digit> <port-utama>
set -euo pipefail

if [ $# -ne 3 ]; then
  echo "Pemakaian: bash adb_connect.sh <port-pairing> <kode> <port-utama>"
  exit 1
fi

PAIR_PORT="$1"
CODE="$2"
MAIN_PORT="$3"
HOST=$(ifconfig wlan0 2>/dev/null | awk '/inet /{print $2; exit}')
[ -n "$HOST" ] || HOST=127.0.0.1

adb start-server >/dev/null 2>&1 || true
echo "Pairing $HOST:$PAIR_PORT ..."
printf '%s\n' "$CODE" | adb pair "$HOST:$PAIR_PORT"
echo "Connect $HOST:$MAIN_PORT ..."
adb connect "$HOST:$MAIN_PORT"

sleep 2
if adb devices | grep -E '[:.][0-9]+[[:space:]]+device$' >/dev/null; then
  echo "ADB TERHUBUNG."
  adb devices
else
  echo "Gagal terhubung. Cek port di menu Wireless debugging."
  adb devices
  exit 1
fi
