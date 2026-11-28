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

- Repo: **https://github.com/sunarno85/paycheck-playbook** (`config.env` sengaja tidak ikut).
- Page: **Paycheck Playbook** / `@paycheckplaybookus` — aktif.
- **12 Reels sudah tayang** memakai footage stok asli (Pixabay), caption + hashtag lengkap. Versi lama ber-background solid sudah dihapus.
- Token Page, `PAGE_ID`, dan API key tersimpan lokal di `tool/config.env` (`600`) dan GitHub Secrets.
- Workflow build + publish sudah aktif di tab **Actions**.

### Perintah penting

```bash
bash ~/fb-us-money/tool/set_secrets.sh                       # sinkronkan config.env -> GitHub Secrets
bash ~/fb-us-money/tool/publish_all.sh                       # build + publish semua Reels
bash ~/fb-us-money/tool/publish_from_dir.sh /path/ke/output   # publish dari artifact tanpa rebuild
```

### Control Panel (dashboard HP)

```bash
bash ~/fb-us-money/tool/start_panel.sh
```

Buka **http://127.0.0.1:8765** di browser HP, lalu pilih **Add to Home Screen** supaya tampil seperti aplikasi. Panel menampilkan status Page, token/izin, jadwal, Insights, dan draf balasan komentar. Tombol **Pratinjau** menunjukkan tanggal sebelum menjadwalkan 7 konten berikutnya dari `content/bank.json`.

Postingan dikirim oleh Facebook lewat `scheduled_publish_time` — HP tidak perlu menyala terus.

### Berjalan otomatis (tanpa campur tangan)

- `weekly-insights.yml` — Senin 08:00 UTC: tarik Insights, isi `04_TRACKER.csv`, buat draf balasan.
- `auto-schedule.yml` — Senin 08:30 UTC: jadwalkan 7 konten berikutnya dari `content/bank.json`.
- `weekly-reel.yml` — Senin & Kamis 09:00 UTC: build + publish 1 Reel baru dari `tool/content/reels.json` (stok Pixabay, voice-over, tanpa fallback warna).
- `auto-reply.yml` — tiap 6 jam: balas komentar baru dengan template aman (maks. 10 per run).
- `publish-site.yml` — regenerate situs SEO di `docs/` (GitHub Pages): **https://sunarno85.github.io/paycheck-playbook/**
- Bank berisi **135 konten teks** (± 19 minggu) dan **15 skrip Reel** baru (R13–R28). Facebook yang mengirim post pada jamnya — HP tidak perlu menyala.

Baca **`06_GROWTH_PLAN.md`** untuk rencana discoverability + langkah UI yang tersisa.

### Yang masih butuh kamu (tidak bisa lewat API)

- Token dengan `pages_manage_metadata` — hanya untuk foto profil, cover, bio, dan website (opsional).
- Verifikasi Page, hubungkan Instagram, dan pin welcome post (UI Facebook).
- Matikan **Wireless Debugging** di HP.
- Screenshot menu **Monetization** / Insights detail bila ingin analisis retensi lebih dalam.
