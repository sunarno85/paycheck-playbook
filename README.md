# Facebook US Money Page — Operational Kit

Folder ini dibuat untuk kelola Page Facebook baru dengan target audiens **Amerika Serikat**.

Baca urut:

0. **`PANDUAN_5_MENIT.md`** — mulai dari sini; semua teks & klik sudah disiapkan.
1. `00_STRATEGI.md` — keputusan niche, audiens, roadmap uang, aturan aman.
2. `05_CHECKLIST_SETUP.md` — yang harus kamu lakukan sekali di awal (buat Page, setting, tools).
3. `CLOUD.md` — cara menjalankan tool lewat GitHub Actions (storage HP penuh).
4. `01_KALENDER_30_HARI.md` — jadwal 30 hari siap pakai.
5. `02_SKRIP_REELS.md` — 12 skrip voice-over lengkap (hook, VO, teks layar, stok video, caption).
6. `03_TEMPLATE_POST.md` — bio, pinned post, caption carousel, balasan DM, pitch sponsor.
7. `04_TRACKER.csv` — isi harian dengan angka dari Insights; saya yang analisis.

## Tool otomatis (`tool/`)

`tool/factory.py` membuat voice-over, mengambil stok video, merender Reels 9:16 dengan teks, menulis paket unggahan, dan bisa mempublish lewat Meta Graph API.

```bash
cd ~/fb-us-money/tool
bash setup.sh
python factory.py check
python factory.py build R1
python factory.py publish R1        # dry-run
python factory.py publish R1 --yes  # posting
```

Baca `tool/README.md` dan `tool/GET_TOKEN.md` untuk token Page & kunci Pexels. `DRY_RUN=1` default agar tidak posting tidak sengaja.

## Aset visual

`assets/logo.svg`, `assets/cover.svg`, `assets/slide_50_30_20.svg` — bisa dibuka di Canva/browser lalu diekspor ke PNG.

## Pembagian kerja

- **Saya:** strategi, skrip, caption, copy affiliate/sponsor, kode tool, analisis data yang kamu kirim.
- **Tool:** voice-over AI, stok video, render video + teks, paket unggahan, publish via API resmi.
- **Kamu:** buat Page, isi `config.env` (token & API key), jalankan tool, kirim screenshot Insights tiap 3 hari.

⚠️ Jangan pernah kirim password **atau token** Facebook/email ke saya. Token tersimpan lokal di `config.env` perangkatmu.

## Status saat ini

Repo GitHub sudah dibuat: **https://github.com/sunarno85/paycheck-playbook** (23 file ter-upload, `config.env` sengaja tidak ikut).

File workflow `.github/workflows/build-reels.yml` belum bisa dikirim karena PAT hanya punya scope `repo`. GitHub mensyaratkan scope `workflow` untuk file di folder tersebut. Setelah scope `workflow` dicentang di https://github.com/settings/tokens, jalankan:

```bash
bash ~/fb-us-money/tool/finish_setup.sh
```

Skrip itu mengirim workflow, lalu menjalankan uji build `R1` dengan `publish=false`. Hasilnya di tab **Actions** repo.

Status lanjutan: uji `R1` **sukses** (bug mapping audio ffmpeg sudah diperbaiki), lalu build **`all` sukses** menghasilkan 12 MP4 + 12 paket caption di `output/`. File tidak masuk git (sesuai `.gitignore`).

Setelah `tool/config.env` diisi `PAGE_ID`, `PAGE_ACCESS_TOKEN`, dan opsional `PEXELS_API_KEY`, jalankan:

```bash
bash ~/fb-us-money/tool/set_secrets.sh
```

Lalu publish lewat **Actions → Run workflow → reel: all → centang publish**.
