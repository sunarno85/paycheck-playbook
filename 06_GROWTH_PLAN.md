# Rencana Pertumbuhan — Paycheck Playbook

Tujuan: **mudah ditemukan** dan **ramai secara organik**. Tidak ada beli follower, engagement pod, atau konten orang lain.

## 1. Yang sudah berjalan sendiri

| Sinyal | Otomasi | Efek |
|---|---|---|
| Konsistensi | 1 post teks/hari pukul 12:15 ET (jam makan siang AS) | Algoritma menyukai Page yang rutin |
| Format video | 2 Reel/minggu (Senin & Kamis 09:00 UTC) | Reel punya jangkauan organik terbesar |
| Balasan cepat | `auto-reply.yml` tiap 6 jam, template aman, maks. 10/run | Komentar dibalas → sinyal interaksi naik |
| Discoverability Google | `publish-site.yml` → 135 artikel di GitHub Pages + sitemap | Page & konten muncul di pencarian, bukan hanya di Facebook |
| Pengukuran | `weekly-insights.yml` tiap Senin 08:00 UTC | Lihat format mana yang menang, lalu sesuaikan |

Situs: **https://sunarno85.github.io/paycheck-playbook/**

## 2. Yang perlu diketuk sekali di UI Facebook

Buka Page → **Edit Page Info** / **Settings** (tidak bisa lewat Graph API karena token belum punya `pages_manage_metadata`).

- **Username:** `@paycheckplaybookus` (sudah aktif).
- **Bio / About** — salin:
  ```text
  Practical money habits for US paychecks. Budgeting, savings, credit, debt, and retirement — explained simply. For educational purposes only. Not financial advice.
  ```
- **Website:** `https://sunarno85.github.io/paycheck-playbook/`
- **Pin post:** welcome post (sudah diterbitkan) → titik tiga → **Pin to top of page**.
- **Page verification:** Settings → **Page Verification** → ikuti panduan Meta.
- **Hubungkan Instagram:** Settings → **Instagram** →Connect account (butuh akun IG yang kamu kelola).
- **Undang audiens awal:** Page → titik tiga → **Invite friends** (pilih yang relevan, jangan spam).
- **Matikan Wireless Debugging** di HP setelah semua selesai.

Kalau kamu mau, kirim saja screenshot halaman **Edit Page Info** — saya beri teks siap tempel untuk tiap kolom.

## 3. Cara membaca hasil (2 minggu ke depan)

Buka `04_TRACKER.csv` tiap Senin. Yang diperhatikan:

1. **Reel Views** naik tiap minggu → format/video sudah cocok.
2. **Retensi 3 detik %** rendah (<30%) → hook di 2 detik pertama perlu lebih tajam (saya bisa ganti hook tanpa mengubah isi).
3. **Shares & Saves** lebih penting daripada likes → konten "save this" memang dibuat untuk itu.
4. **Link clicks** dari situs → tanda SEO mulai bekerja.

Kirim screenshot **Insights → Reels → Retention** kalau mau saya sesuaikan panjang dan hook Reel.

## 4. Yang tidak dilakukan

- Membeli follower / likes / views.
- Mengikuti engagement pod atau grup saling comment.
- Mengambil video atau caption orang lain tanpa izin (stok Pixabay sudah berlisensi).
- Memberi nasihat investasi/spesifik per orang — semua konten memakai disclaimer.
