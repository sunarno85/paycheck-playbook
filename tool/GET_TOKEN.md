# Cara dapat Page Access Token (untuk publish otomatis)

Ini **cara resmi Meta Graph API** — tidak perlu password Facebook dan tidak perlu login lewat tool saya. Token disimpan lokal di `config.env` di perangkatmu.

## 1. Buat Meta App

1. Buka https://developers.facebook.com/apps/
2. **Create App** → pilih tipe **Business** → nama: `Paycheck Playbook Bot` → Create.
3. Di App Dashboard → **Settings → Basic**, catat **App ID** dan **App Secret** (rahasia).

## 2. Dapatkan User Token dengan izin Page

1. Buka https://developers.facebook.com/tools/explorer/
2. Pilih app yang tadi dibuat di dropdown **Meta App**.
3. Klik **Generate Access Token**.
4. Di daftar permission, centang:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
5. Klik **Generate Token**, lalu copy token user tersebut.

## 3. Tukar ke long-lived token (opsional tapi disarankan)

Di Termux:

```bash
curl -s "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=USER_TOKEN"
```

Catat nilai `access_token` yang baru (berlaku ±60 hari).

## 4. Ambil Page Access Token

```bash
curl -s "https://graph.facebook.com/me/accounts?fields=id,name,access_token&access_token=LONG_LIVED_TOKEN"
```

Dari hasilnya, pilih entri dengan nama **Paycheck Playbook**:

```json
{
  "data": [
    { "id": "123456789", "name": "Paycheck Playbook", "access_token": "EAA..." }
  ]
}
```

- `id` → masukkan ke `PAGE_ID`
- `access_token` → masukkan ke `PAGE_ACCESS_TOKEN`

## 5. Isi config

```bash
cd ~/fb-us-money/tool
cp config.env.example config.env
nano config.env
chmod 600 config.env
```

## 6. Uji

```bash
python factory.py check
python factory.py build R1
python factory.py publish R1        # dry-run, aman
python factory.py publish R1 --yes  # benar-benar posting
```

## Catatan penting

- App dalam mode **Development** cukup untuk Page milikmu sendiri — tidak perlu App Review.
- Jika `publish` gagal dengan error permission, ulangi langkah 2 dan pastikan user token masih berlaku.
- Tool punya fallback: kalau endpoint Reels gagal, ia mencoba endpoint `/videos`.
- **Jangan kirim token ke saya.** Kalau ada error, kirim hanya pesan error-nya (token saya minta kamu sensor).
