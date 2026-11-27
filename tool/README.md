# Content Factory

Mesin untuk membuat dan (opsional) mempublish Reels "Paycheck Playbook".

> ⚠️ Di perangkat dengan storage < 1,2 GB, jalankan lewat **GitHub Actions** — lihat `../CLOUD.md`. Kode tool-nya tetap sama.

## Alur kerja

```
reels.json → edge-tts (voice-over) → Pexels (stok video) → ffmpeg (render 9:16 + teks) → MP4 + paket unggahan → Graph API (opsional)
```

## Setup sekali

```bash
cd ~/fb-us-money/tool
bash setup.sh
cp config.env.example config.env
# isi config.env, lihat GET_TOKEN.md untuk token
chmod 600 config.env
```

## Pemakaian

```bash
python factory.py check           # cek python, ffmpeg, font, token
python factory.py build R1        # buat voice-over + video + paket hari itu
python factory.py build all       # buat 12 Reels sekaligus
python factory.py pack R1         # hanya tulis paket teks (tanpa render)
python factory.py publish R1      # DRY RUN, tidak posting
python factory.py publish R1 --yes  # posting via Graph API
```

Hasil ada di `~/fb-us-money/output/`:
- `R1.mp4` ... `R12.mp4`
- `R1_paket.md` ... (caption, timeline, instruksi upload)

## Yang masih perlu kamu lakukan

1. Buat Page Facebook (checklist di `../05_CHECKLIST_SETUP.md`).
2. Dapatkan Page token (`GET_TOKEN.md`) kalau mau publish otomatis.
3. Ambil kunci Pexels gratis supaya stok videonya nyata (tanpa itu tool pakai background solid).
4. Kirim screenshot Insights ke saya tiap 3 hari untuk analisis.

## Keamanan

- Token ONLY disimpan di `config.env` di perangkatmu.
- `DRY_RUN=1` secara default agar tidak ada posting tidak sengaja.
- Jangan pernah membagikan isi `config.env`.
