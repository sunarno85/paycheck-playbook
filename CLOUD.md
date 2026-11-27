# Menjalankan tool lewat cloud (karena storage HP penuh)

HP saat ini punya ~300 MB kosong, sementara `python + ffmpeg` butuh ~797 MB. Jadi production dijalankan di GitHub Actions (gratis), lalu MP4-nya didownload ke HP.

## 1. Siapkan repository

1. Buat repository GitHub baru (misal `paycheck-playbook`).
2. Upload seluruh folder `fb-us-money` ke repository itu (bisa lewat web drag-and-drop).
3. Pastikan file `.github/workflows/build-reels.yml` ikut ter-upload (folder `.github` tersembunyi — aktifkan "show hidden files" saat drag).

## 2. Isi Secrets

Di repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Nama | Isi |
|---|---|
| `PEXELS_API_KEY` | Kunci gratis dari https://www.pexels.com/api/ |
| `PAGE_ID` | ID Page Facebook (dari `GET_TOKEN.md`) |
| `PAGE_ACCESS_TOKEN` | Page access token (dari `GET_TOKEN.md`) |

Kalau belum mau publish otomatis, `PAGE_ID` dan token boleh dikosongkan dulu.

## 3. Jalankan

**Actions → Build Paycheck Playbook Reels → Run workflow**
- `reel`: `R1` untuk coba, atau `all` untuk 12 video.
- `publish`: **centang hanya kalau token sudah valid dan kamu siap tayang**.

Setelah selesai, klik artifact `reels-all` → download → extract di HP.

## 4. Upload manual (kalau publish tidak dicentang)

Buka Meta Business Suite → Create → Reel → pilih MP4 dari hasil download → paste caption dari `R*_paket.md` → jadwalkan 07:30 ET.

## Kenapa tidak dipasang di HP?

`pkg install python ffmpeg` menarik 95 paket (~797 MB) karena `libplacebo` → `python` → `glslang` → `llvm/clang`. Storage tidak mencukupi, jadi saya tidak memaksa install yang bisa merusak sistem Termux. Tool-nya tetap sama; hanya lokasi eksekusinya yang pindah ke cloud.

Kalau kamu tidak punya GitHub, saya bisa buatkan versi **Google Colab** (tinggal jalankan sel di browser, hasilnya di-download).
