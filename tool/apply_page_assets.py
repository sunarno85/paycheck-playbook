#!/usr/bin/env python3
"""Pasang foto profil, cover, bio dan website Page lewat Graph API."""
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = os.environ.get("PAGE_ID", "")
TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
if not PAGE or not TOKEN:
    raise SystemExit("ERROR: PAGE_ID / PAGE_ACCESS_TOKEN kosong")

BIO = ("Simple money moves for real life 💵 Budgeting, credit & savings tips for "
       "US households. Educational only — not financial advice.")
WEBSITE = f"https://www.facebook.com/{PAGE}"


def post(path, fields, upload=None):
    cmd = ["curl", "-sS", "-X", "POST"]
    for k, v in fields.items():
        cmd += ["-F", f"{k}={v}"]
    if upload:
        cmd += ["-F", f"source=@{upload}"]
    cmd.append(f"https://graph.facebook.com/{path}")
    return subprocess.run(cmd, capture_output=True, text=True, timeout=60)


steps = [
    ("foto profil", f"{PAGE}/picture", {"access_token": TOKEN}, ROOT / "assets" / "logo.png"),
    ("foto cover", f"{PAGE}/photos", {"access_token": TOKEN, "type": "cover"}, ROOT / "assets" / "cover.png"),
    ("bio & website", PAGE, {"access_token": TOKEN, "bio": BIO, "website": WEBSITE}, None),
]

failed = 0
for label, path, fields, upload in steps:
    if upload and not upload.exists():
        print(f"{label}: ERROR file tidak ada {upload}")
        failed += 1
        continue
    res = post(path, fields, upload)
    out = res.stdout.strip()
    ok = '"error"' not in out and bool(out)
    print(f"{label}: {'OK' if ok else 'GAGAL'} {out[:300]}")
    if not ok:
        failed += 1

raise SystemExit(1 if failed else 0)
