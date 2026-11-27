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
