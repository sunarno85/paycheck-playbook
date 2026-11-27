#!/usr/bin/env python3
"""
Paycheck Playbook content factory.

Commands:
  python factory.py check
  python factory.py build R1
  python factory.py build all
  python factory.py pack R1
  python factory.py publish R1 --yes

build  = voice-over + stok video + render MP4 + paket unggahan
publish= unggah via Meta Graph API (butuh PAGE_ID + PAGE_ACCESS_TOKEN di config.env)
"""

import json
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CFG_FILE = HERE / "config.env"
CONTENT = HERE / "content" / "reels.json"
TMP = ROOT / "assets" / "_tmp"

DEFAULTS = {
    "PAGE_ID": "",
    "PAGE_ACCESS_TOKEN": "",
    "PEXELS_API_KEY": "",
    "PIXABAY_API_KEY": "",
    "VOICE": "en-US-AndrewNeural",
    "FONT": "/system/fonts/Roboto-Bold.ttf",
    "OUT_DIR": str(ROOT / "output"),
    "DRY_RUN": "1",
}


def log(msg):
    print(f"[factory] {msg}", flush=True)


def load_config():
    cfg = dict(DEFAULTS)
    if CFG_FILE.exists():
        for line in CFG_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            cfg[key.strip()] = val.strip().strip('"').strip("'")
    for key in list(cfg):
        if key in __import__("os").environ:
            cfg[key] = __import__("os").environ[key]
    cfg["OUT"] = Path(cfg["OUT_DIR"])
    cfg["OUT"].mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    return cfg


def run(cmd, capture=True):
    return subprocess.run(
        cmd,
        text=True,
        capture_output=capture,
    )


def need(cmd, fatal=False):
    found = shutil.which(cmd)
    if not found and fatal:
        log(f"ERROR: '{cmd}' belum terinstall. Jalankan tool/setup.sh dulu.")
        sys.exit(1)
    return found


def esc(s):
    """Escape path untuk filter_complex ffmpeg."""
    return s.replace("\\", "\\\\").replace(":", "\\:")


def find_font(cfg):
    candidates = [cfg.get("FONT", ""), "/system/fonts/Roboto-Bold.ttf",
                  "/system/fonts/Roboto-Regular.ttf", "/system/fonts/NotoSans-Bold.ttf"]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


def duration(audio):
    probe = need("ffprobe")
    if not probe:
        return 35.0
    r = run([probe, "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(audio)])
    try:
        return float(r.stdout.strip())
    except (ValueError, AttributeError):
        return 35.0


def tts(cfg, reel, path):
    if path.exists() and path.stat().st_size > 5000:
        log(f"voice-over sudah ada: {path.name}")
        return True
    exe = need("edge-tts")
    if exe:
        r = run([exe, "--voice", cfg["VOICE"], "--text", reel["vo"],
                 "--write-media", str(path)])
        if r.returncode == 0 and path.exists():
            log(f"voice-over dibuat (Edge TTS {cfg['VOICE']})")
            return True
        log(f"edge-tts gagal: {r.stderr[:200] if r.stderr else 'unknown'}")
    g = need("gtts-cli")
    if g:
        r = run([g, reel["vo"], "--lang", "en-us", "--output", str(path)])
        if r.returncode == 0 and path.exists():
            log("voice-over dibuat (gTTS)")
            return True
    log("WARNING: engine TTS tidak ada — pakai audio diam. Install: pip install edge-tts")
    run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
         "-t", "35", "-c:a", "libmp3lame", str(path)])
    return False


def fetch_clips(cfg, reel, outdir):
    need("ffmpeg", fatal=True)
    paths = []
    for i, query in enumerate(reel["stock_queries"][:3]):
        dest = outdir / f"{reel['id']}_clip_{i}.mp4"
        if dest.exists() and dest.stat().st_size > 10000:
            paths.append(dest)
            continue
        ok = False
        link = None
        pkey = cfg.get("PEXELS_API_KEY", "")
        bkey = cfg.get("PIXABAY_API_KEY", "")
        try:
            if pkey:
                url = "https://api.pexels.com/videos/search?" + urllib.parse.urlencode(
                    {"query": query, "per_page": 5, "orientation": "portrait"})
                req = urllib.request.Request(
                    url, headers={"Authorization": pkey, "User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.load(resp)
                for video in data.get("videos", []):
                    for f in video.get("video_files", []):
                        if f.get("file_type") == "mp4" and (f.get("height") or 0) >= 900:
                            link = f.get("link")
                            break
                    if link:
                        break
            elif bkey:
                # Pixabay menolak User-Agent bawaan Python (403), jadi pakai UA browser.
                # Kalau query spesifik kosong, cari kata kunci umum yang pasti ada.
                for q in (query, "money", "finance"):
                    url = "https://pixabay.com/api/videos/?" + urllib.parse.urlencode(
                        {"key": bkey, "q": q, "per_page": 5, "safesearch": "true"})
                    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        data = json.load(resp)
                    for hit in data.get("hits", []):
                        vids = hit.get("videos", {})
                        link = (vids.get("medium") or vids.get("small") or {}).get("url")
                        if link:
                            break
                    if link:
                        break
            if link:
                req2 = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req2, timeout=90) as resp, open(dest, "wb") as fh:
                    shutil.copyfileobj(resp, fh)
                ok = dest.stat().st_size > 10000
        except Exception as exc:
            log(f"stok '{query}' gagal: {exc}")
        if not ok:
            log(f"fallback warna solid untuk '{query}' (isi PEXELS_API_KEY/PIXABAY_API_KEY untuk stok asli)")
            run(["ffmpeg", "-y", "-f", "lavfi",
                 "-i", "color=c=0x0F3D3E:s=1080x1920:d=12",
                 "-c:v", "libx264", "-pix_fmt", "yuv420p", str(dest)])
        paths.append(dest)
    return paths


def build_filter(cfg, reel, clips, dur, with_overlays=True):
    seg = dur / len(clips)
    parts = []
    for i, _ in enumerate(clips):
        parts.append(
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920,setsar=1,fps=30,trim=duration={seg:.3f},"
            f"setpts=PTS-STARTPTS[v{i}]"
        )
    parts.append("".join(f"[v{i}]" for i in range(len(clips))) +
                 f"concat=n={len(clips)}:v=1:a=0[base]")
    overlays = reel.get("overlays", []) if with_overlays else []
    if not overlays:
        return ";".join(parts), "base"
    font = find_font(cfg)
    if not font:
        log("WARNING: font tidak ditemukan — overlay dinonaktifkan")
        return ";".join(parts), "base"
    first_end = min(3.0, dur * 0.12)
    step = (dur - first_end) / max(1, len(overlays) - 1)
    for i, text in enumerate(overlays):
        start = 0.0 if i == 0 else first_end + step * (i - 1)
        end = first_end if i == 0 else min(dur, first_end + step * i)
        tf = TMP / f"{reel['id']}_ov_{i}.txt"
        tf.write_text(text, encoding="utf-8")
        prev = "base" if i == 0 else f"ov{i - 1}"
        parts.append(
            f"[{prev}]drawtext=fontfile={esc(font)}:textfile={esc(str(tf))}:"
            f"fontcolor=white:fontsize=62:box=1:boxcolor=black@0.35:boxborderw=16:"
            f"x=(w-text_w)/2:y=h*0.70:enable='between(t,{start:.2f},{end:.2f})'[ov{i}]"
        )
    return ";".join(parts), f"ov{len(overlays) - 1}"


def render(cfg, reel, audio, clips, out):
    need("ffmpeg", fatal=True)
    dur = duration(audio)
    graph, last = build_filter(cfg, reel, clips, dur, True)
    cmd = ["ffmpeg", "-y"]
    for clip in clips:
        cmd += ["-i", str(clip)]
    cmd += ["-i", str(audio), "-filter_complex", graph,
            "-map", f"[{last}]", "-map", f"{len(clips)}:a", "-shortest",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart", str(out)]
    r = run(cmd)
    if r.returncode != 0:
        log("render dengan overlay gagal — coba tanpa teks")
        if r.stderr:
            log(r.stderr[-500:])
        graph, last = build_filter(cfg, reel, clips, dur, False)
        cmd = ["ffmpeg", "-y"]
        for clip in clips:
            cmd += ["-i", str(clip)]
        cmd += ["-i", str(audio), "-filter_complex", graph,
                "-map", f"[{last}]", "-map", f"{len(clips)}:a", "-shortest",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "24",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", str(out)]
        r = run(cmd)
    if r.returncode != 0:
        log(f"ERROR render {reel['id']}: {r.stderr[-600:] if r.stderr else 'unknown'}")
        return False
    log(f"video siap: {out}")
    return True


def write_pack(cfg, reel, video):
    pack = cfg["OUT"] / f"{reel['id']}_paket.md"
    dur = duration(TMP / f"{reel['id']}_vo.mp3") if (TMP / f"{reel['id']}_vo.mp3").exists() else 35
    lines = [
        f"# Paket unggahan {reel['id']} — {reel['title']}",
        "",
        f"- Video: `{video}`",
        f"- Durasi: ±{dur:.0f} detik",
        "- Jam: 07:30 ET (19:30 WIB saat EST)",
        "- Audiens: Public",
        "",
        "## Voice-over",
        "",
        reel["vo"],
        "",
        "## Teks di layar",
        "",
    ]
    for i, text in enumerate(reel["overlays"]):
        lines.append(f"{i + 1}. {text}")
    lines += ["", "## Caption siap paste", "", "```", reel["caption"], "```", "",
              "## Setelah tayang", "",
              "- Balas 5 komentar pertama dengan kalimat lengkap.",
              "- Isi 1 baris `04_TRACKER.csv` dari Insights besok pagi.",
              "- Kirim screenshot ke saya untuk adjustment.", ""]
    pack.write_text("\n".join(lines), encoding="utf-8")
    log(f"paket: {pack}")
    return pack


def api_post(url, fields):
    cmd = ["curl", "-sS", "-X", "POST", url]
    for key, val in fields.items():
        cmd += ["--data-urlencode", f"{key}={val}"]
    r = run(cmd)
    try:
        return json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        return {"raw": r.stdout, "error": r.stderr}


def publish(cfg, reel, video, yes=False):
    if cfg.get("DRY_RUN", "1") == "1" and not yes:
        log("DRY_RUN aktif — tidak memposting. Tambahkan --yes untuk publish.")
        return True
    page, token = cfg.get("PAGE_ID", ""), cfg.get("PAGE_ACCESS_TOKEN", "")
    if not page or not token:
        log("ERROR: PAGE_ID / PAGE_ACCESS_TOKEN kosong. Lihat tool/GET_TOKEN.md")
        return False
    base = f"https://graph.facebook.com/{page}/video_reels"
    start = api_post(base, {"upload_phase": "start", "access_token": token})
    vid, upload_url = start.get("video_id"), start.get("upload_url")
    if vid and upload_url:
        # rupload.facebook.com memakai upload resumable: raw body + header Offset/X-Entity-Length.
        upload_url = str(upload_url).replace("\\/", "/")
        size = Path(video).stat().st_size
        r = run(["curl", "-sS", "-X", "POST",
                 "-H", f"Authorization: OAuth {token}",
                 "-H", "Offset: 0",
                 "-H", f"X-Entity-Length: {size}",
                 "-H", "Content-Type: application/octet-stream",
                 "--data-binary", f"@{video}", upload_url])
        try:
            up = json.loads(r.stdout or "{}")
        except json.JSONDecodeError:
            up = {}
        if r.returncode != 0 or not up.get("success"):
            log(f"upload gagal: {(r.stdout or r.stderr or '')[:300]}")
            return False
        result = api_post(base, {
            "upload_phase": "finish",
            "video_id": vid,
            "video_state": "PUBLISHED",
            "description": reel["caption"],
            "access_token": token,
        })
    else:
        log("Reels API tidak tersedia — fallback ke endpoint /videos")
        r = run(["curl", "-sS", "-X", "POST",
                 "-F", f"source=@{video}",
                 "-F", f"description={reel['caption']}",
                 "-F", f"access_token={token}",
                 f"https://graph.facebook.com/{page}/videos"])
        try:
            result = json.loads(r.stdout or "{}")
        except json.JSONDecodeError:
            result = {"raw": r.stdout}
    log(f"hasil publish: {json.dumps(result, ensure_ascii=False)[:500]}")
    return any(k in result for k in ("id", "video_id", "post_id")) and "error" not in result


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd = args[0]
    cfg = load_config()
    content = json.loads(CONTENT.read_text(encoding="utf-8"))

    if cmd == "check":
        log(f"ffmpeg: {need('ffmpeg') or 'MISSING'}")
        log(f"edge-tts: {need('edge-tts') or 'MISSING'}")
        log(f"font: {find_font(cfg) or 'MISSING'}")
        log(f"Pexels API key: {'ada' if cfg['PEXELS_API_KEY'] else 'kosong'}")
        log(f"Pixabay API key: {'ada' if cfg['PIXABAY_API_KEY'] else 'kosong (fallback warna)'}")
        log(f"Page token: {'ada' if cfg['PAGE_ACCESS_TOKEN'] else 'kosong'}")
        log(f"Output: {cfg['OUT']}")
        return

    if cmd in ("build", "pack", "publish"):
        ids = [a for a in args[1:] if not a.startswith("--")]
        if not ids or ids == ["all"]:
            ids = list(content.keys())
        failed = False
        for rid in ids:
            reel = content.get(rid)
            if not reel:
                log(f"ERROR: {rid} tidak ditemukan")
                failed = True
                continue
            if cmd == "pack":
                write_pack(cfg, reel, cfg["OUT"] / f"{rid}.mp4")
                continue
            video = cfg["OUT"] / f"{rid}.mp4"
            if cmd == "publish":
                if not video.exists():
                    log(f"ERROR: {video} belum ada. Jalankan build dulu.")
                    failed = True
                    continue
                if not publish(cfg, reel, video, yes="--yes" in args):
                    failed = True
                continue
            audio = TMP / f"{rid}_vo.mp3"
            tts(cfg, reel, audio)
            clips = fetch_clips(cfg, reel, TMP)
            if not render(cfg, reel, audio, clips, video):
                failed = True
                continue
            write_pack(cfg, reel, video)
        if failed:
            sys.exit(1)
        return

    log(f"perintah tidak dikenal: {cmd}")


if __name__ == "__main__":
    main()
