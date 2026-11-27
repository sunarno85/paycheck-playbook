# Panduan 5 Menit — tinggal ikuti, semua teks sudah disiapkan

## A. Buat Page Facebook (3 menit)

1. Buka **https://www.facebook.com/pages/create/**
2. Nama Page: `Paycheck Playbook`
3. Kategori: **Digital Creator** (kalau ada, tambahkan **Finance** sebagai kedua)
   - ❌ Jangan pilih Bank / Investment Service / Financial Advisor
4. Username: coba `@paycheckplaybookus` (kalau terpakai: `@thepaycheckplaybook`)
5. Foto profil: `assets/logo.svg`
6. Cover: `assets/cover.svg`
7. Bio — paste ini:

```
Simple money moves for real life 💵 Budgeting, credit & savings tips for US households. Educational only — not financial advice. 👇 Grab the free budget template.
```

8. Tombol aksi: **Learn More** → untuk sementara arahkan ke `https://www.facebook.com/` (nanti diganti link affiliate)
9. Page Settings → General → **Page verification** → aktifkan kalau tersedia
10. Selesai. Screenshot menu **Monetization** dan kirim ke saya.

## B. Buat repo GitHub (3 menit)

1. Buka **https://github.com/new**
2. Repository name: `paycheck-playbook`
3. Pilih **Public** → klik **Create repository**
4. Di halaman repo: **Add file → Upload files**
5. Drag **semua isi** folder `fb-us-money` ke halaman itu — termasuk folder `.github`, `assets`, `tool`
   - Jangan drag folder `fb-us-money`-nya, tapi isinya
   - Folder `.github` tersembunyi: Aktifkan "Tampilkan file tersembunyi" di file manager HP
6. Klik **Commit changes**

## C. Isi 3 Secrets (2 menit)

Repo → **Settings → Secrets and variables → Actions → New repository secret**

| Name | Secret | Dari mana |
|---|---|---|
| `PEXELS_API_KEY` | kunci API gratis | https://www.pexels.com/api/ → "Get API Key" |
| `PAGE_ID` | angka ID Page | `tool/GET_TOKEN.md` langkah 4 |
| `PAGE_ACCESS_TOKEN` | token Page | `tool/GET_TOKEN.md` langkah 4 |

Tanpa Pexels key tool tetap jalan (pakai background warna). Tanpa token, tool tetap bisa bikin video tapi tidak publish.

## D. Jalankan (1 menit)

1. Tab **Actions** → klik **Build Paycheck Playbook Reels**
2. Klik **Run workflow**
3. Isi:
   - `reel`: `R1`
   - `publish`: **NONAKTIF** (kosongkan centang) untuk uji coba
4. Tunggu ~3–5 menit → klik artifact `reels-R1` → download → extract
5. Lihat hasil `R1.mp4` dan `R1_paket.md`

## E. Kalau R1 sudah bagus

Jalankan lagi dengan:
- `reel`: `all`
- `publish`: **centang** (hanya kalau token sudah benar)

12 Reels akan otomatis dipublish ke Page.

## F. Kirim ke saya

- Screenshot **Monetization** Page
- Screenshot **Insights** (3 hari sekali)
- Pesan error kalau workflow gagal (token di-sensor dulu)

Saya yang analisis angkanya dan perbaiki strategi konten berikutnya.
