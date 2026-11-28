#!/usr/bin/env python3
"""Balas komentar baru di Page dengan template aman (tanpa nasihat finansial)."""
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = ROOT / "tool" / "config.env"
STATE = ROOT / "content" / "replied_comments.json"
LIMIT = 10

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

TEMPLATES = {
    "question": [
        "Great question — I'm planning a post on exactly this. Hit Follow so you don't miss it.",
        "Good question! I'll break it down in an upcoming post. Save the page to catch it.",
        "Thanks for asking — this deserves a proper post, and one is on the way.",
    ],
    "thanks": [
        "You're welcome — glad it was useful!",
        "Appreciate that. More practical posts coming soon.",
        "Happy it helped. See you on the next one!",
    ],
    "saved": [
        "That's the idea — save it and come back when payday rolls around.",
        "Nice. Small habits repeated beat big plans once.",
        "Exactly why I post these — easy to revisit when you need it.",
    ],
    "default": [
        "Appreciate you reading and commenting — more US money tips coming soon.",
        "Thanks for joining the conversation. Follow along for the next one.",
        "Thanks for sharing your take. More practical posts on the way.",
    ],
}


def api(path, **params):
    params["access_token"] = TOKEN
    url = f"https://graph.facebook.com/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.load(resp)


def post_comment(comment_id, message):
    data = urllib.parse.urlencode(
        {"message": message, "access_token": TOKEN}).encode("utf-8")
    req = urllib.request.Request(
        f"https://graph.facebook.com/{comment_id}/comments",
        data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def pick(message, ident):
    low = message.lower()
    if "?" in message or any(w in low for w in ("how ", "what ", "why ", "should i")):
        key = "question"
    elif any(w in low for w in ("thank", "appreciate", "helpful")):
        key = "thanks"
    elif any(w in low for w in ("save", "saved", "sharing")):
        key = "saved"
    else:
        key = "default"
    options = TEMPLATES[key]
    return options[int(ident[-3:].replace("_", "0") or "0", 36) % len(options)]


def main():
    replied = set()
    if STATE.exists():
        replied = set(json.loads(STATE.read_text(encoding="utf-8")).get("ids", []))
    cutoff = datetime.now(timezone.utc) - timedelta(days=14)
    try:
        posts = api(f"{PAGE}/posts", fields="id", limit=20).get("data", [])
    except Exception as exc:
        print("Gagal ambil post:", str(exc)[:160])
        return
    done = 0
    for post in posts:
        if done >= LIMIT:
            break
        try:
            comments = api(post["id"] + "/comments",
                           fields="id,message,from,created_time", limit=50).get("data", [])
        except Exception:
            continue
        for c in comments:
            if done >= LIMIT:
                break
            cid = c.get("id", "")
            msg = (c.get("message") or "").strip()
            who = (c.get("from") or {}).get("id", "")
            created = c.get("created_time", "")
            if not cid or cid in replied or not msg or who == PAGE:
                continue
            try:
                when = datetime.fromisoformat(created.replace("Z", "+00:00"))
                if when < cutoff:
                    continue
            except ValueError:
                pass
            reply = pick(msg, cid)
            try:
                result = post_comment(cid, reply)
                if result.get("id"):
                    replied.add(cid)
                    done += 1
                    print("balas", cid[-12:], "->", reply[:60])
            except Exception as exc:
                print("gagal balas", cid[-12:], str(exc)[:120])
    STATE.write_text(json.dumps({"ids": sorted(replied)}, indent=2) + "\n", encoding="utf-8")
    print(f"selesai: {done} balasan baru, {len(replied)} total terbalas")


if __name__ == "__main__":
    main()
