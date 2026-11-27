#!/data/data/com.termux/files/usr/bin/bash
# Setup dependensi untuk content factory di Termux
set -e

FREE=$(df -m "$PREFIX" 2>/dev/null | tail -n 1 | awk '{print $4}')
if [ -n "$FREE" ] && [ "$FREE" -lt 1200 ]; then
  echo "Storage hanya ${FREE} MB. Butuh ~1200 MB untuk python + ffmpeg."
  echo "Jangan paksa install — pakai cloud runner: baca ../CLOUD.md"
  exit 1
fi

echo "==> Update paket Termux"
pkg update -y

echo "==> Install python, ffmpeg, curl"
pkg install -y python ffmpeg curl

echo "==> Install edge-tts (voice-over gratis)"
python -m pip install --upgrade pip setuptools wheel || true
python -m pip install edge-tts

echo "==> Cek hasil"
cd "$(dirname "$0")"
python factory.py check

echo ""
echo "Selesai. Langkah berikutnya:"
echo "1. cp config.env.example config.env"
echo "2. Isi PEXELS_API_KEY (opsional) dan PAGE_ID + PAGE_ACCESS_TOKEN (untuk publish)"
echo "3. Baca GET_TOKEN.md untuk cara dapat token Page"
echo "4. python factory.py build R1"
