#!/usr/bin/env python3
"""Tarik Insights mingguan dari Graph API -> 04_TRACKER.csv + draf balasan komentar."""
import csv
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "tool" / "config.env"
cfg = {}
if CFG.exists():
    for line in CFG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
PAGE = os.environ.get("PAGE_ID") or cfg.get("PAGE_ID", "")
TOKEN = os.environ.get("PAGE_ACCESS_TOKEN") or cfg.get("PAGE_ACCESS_TOKEN", "")
if not PAGE or not TOKEN:
    raise SystemExit("ERROR: PAGE_ID / PAGE_ACCESS_TOKEN tidak ada")


def api(path, **params):
    params["access_token"] = TOKEN
    url = f"https://graph.facebook.com/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


def total_metric(name):
    try:
        d = api(f"{PAGE}/insights", metric=name, period="day")
        values = d.get("data", [{}])[0].get("values", [])[-7:]
        total = 0
        for item in values:
            val = item.get("value", 0)
            if isinstance(val, (int, float)):
                total += val
            elif isinstance(val, dict):
                total += sum(v for v in val.values() if isinstance(v, (int, float)))
        return int(total)
    except Exception:
        return 0


views = total_metric("page_video_views")
engaged = total_metric("page_post_engagements")
reactions = total_metric("page_actions_post_reactions_total")

try:
    page = api(PAGE, fields="followers_count,fan_count")
except Exception:
    page = {}
followers = page.get("followers_count") or page.get("fan_count") or ""

try:
    videos = api(f"{PAGE}/videos", fields="id,description,status", limit=50).get("data", [])
except Exception:
    videos = []

video_views = 0
for video in videos:
    try:
        d = api(f"{video['id']}/video_insights", metric="total_video_views")
        for item in d.get("data", [{}])[0].get("values", []):
            val = item.get("value", 0)
            if isinstance(val, (int, float)):
                video_views += int(val)
    except Exception:
        pass

wib = timezone(timedelta(hours=7))
today = datetime.now(wib).strftime("%Y-%m-%d")
tracker = ROOT / "04_TRACKER.csv"
with tracker.open(newline="", encoding="utf-8") as fh:
    rows = list(csv.reader(fh))
if not rows:
    rows = [["Tanggal", "Kode", "Format", "Judul", "Jam ET", "Views",
             "Retensi 3 detik %", "Watch time menit", "Likes", "Komentar",
             "Shares", "Saves", "Followers baru", "Link clicks",
             "Est penghasilan USD", "Catatan insight"]]
header = rows[0]
row = [""] * len(header)
row[0] = today
row[1] = "ALL"
row[2] = "Weekly"
row[3] = "Ringkasan otomatis Graph API"
row[4] = "-"
row[5] = video_views or views
row[12] = followers
row[15] = (f"auto: page_video_views={views}, page_video_views_reel={video_views}, "
           f"post_engagements={engaged}, reactions={reactions}. "
           "Retensi/watch time perlu screenshot Insights manual.")
rows = [r for r in rows[1:] if not r or r[0] != today] + [row]
with tracker.open("w", newline="", encoding="utf-8") as fh:
    csv.writer(fh).writerows([header] + rows)

# Draf balasan komentar terbaru
lines = [f"# Draf balasan komentar — {today}", "",
         "Balas dengan kalimat lengkap, bukan cuma emoji.", ""]
try:
    posts = api(f"{PAGE}/posts", fields="id,message,created_time", limit=10).get("data", [])
except Exception:
    posts = []
count = 0
for post in posts:
    try:
        comments = api(post["id"] + "/comments",
                       fields="id,message,from,created_time", limit=20).get("data", [])
    except Exception:
        comments = []
    if not comments:
        continue
    snippet = (post.get("message") or "").split("\n")[0][:70]
    lines += [f"## Post: {snippet}", ""]
    for c in comments:
        who = (c.get("from") or {}).get("name", "?")
        lines += [f"- **{who}:** {(c.get('message') or '').strip()}",
                  f"  Balas: thanks for sharing this! ...", ""]
        count += 1
if count == 0:
    lines.append("Belum ada komentar baru minggu ini.")
(ROOT / "tool" / "replies_pending.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

print(f"OK {today}: views={row[5]}, engagements={engaged}, reactions={reactions}, "
      f"followers={followers or 'n/a'}, komentar={count}")
