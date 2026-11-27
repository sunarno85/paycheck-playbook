# Cara supaya saya bisa buat repo + upload otomatis

Login di aplikasi GitHub tidak bisa dipanggil dari shell. Cara paling aman: buat **Personal Access Token (PAT)**, simpan di file lokal, lalu saya yang jalankan `tool/github_push.sh`.

## 1. Buat token (1 menit)

Buka browser (atau aplikasi GitHub → browser): **https://github.com/settings/tokens**

- Klik **Generate new token → Generate new token (classic)**
- Note: `fb-paycheck`
- Expiration: **90 days**
- Centang:
  - ✅ `repo` (semua sub-scope)
  - ✅ `workflow` (wajib untuk upload file `.github/workflows/`)
- Klik **Generate token**, lalu salin tokennya.

## 2. Simpan token di HP (jangan kirim ke saya)

Buka Termux, jalankan:

```bash
cat > ~/.github_token <<'EOF'
TOKEN_YANG_TADI_KAMU_SALIN
EOF
chmod 600 ~/.github_token
```

Atau pakai file manager: buat file bernama `.github_token` di `/data/data/com.termux/files/home/` lalu isi dengan token tersebut.

## 3. Bilang "sudah"

Begitu file itu ada, saya yang:
1. Membaca username GitHub-mu lewat API.
2. Membuat repo `paycheck-playbook`.
3. Meng-upload semua file (termasuk workflow Actions).
4. Memberi tahu URL repo-nya.

Token tidak pernah saya tampilkan atau kirim ke mana-mana — saya hanya memanggil file itu dari script.

## Catatan

- Tanpa scope `workflow`, upload file workflow akan gagal.
- Token bisa dicabut kapan saja di halaman Settings → Tokens.
- Alternatif kalau tidak mau buat token: ikutin `PANDUAN_5_MENIT.md` bagian B (upload manual lewat web).
