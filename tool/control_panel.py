#!/usr/bin/env python3
"""Paycheck Playbook Control Panel — dashboard lokal (Python stdlib saja)."""
import csv
import json
import mimetypes
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PANEL = Path(__file__).resolve().parent / "panel"
BANK = ROOT / "content" / "bank.json"
TRACKER = ROOT / "04_TRACKER.csv"
HOST, PORT = "127.0.0.1", 8765

cfg = {}
CFG_FILE = ROOT / "tool" / "config.env"
if CFG_FILE.exists():
    for line in CFG_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            cfg[k.strip()] = v.strip().strip('"').strip("'")
PAGE = os.environ.get("PAGE_ID") or cfg.get("PAGE_ID", "")
TOKEN = os.environ.get("PAGE_ACCESS_TOKEN") or cfg.get("PAGE_ACCESS_TOKEN", "")
USER_TOKEN_FILE = Path.home() / "facebook_token"

_token_cache = {"at": 0, "data": {}}


def api_get(path, **params):
    params["access_token"] = TOKEN
    url = f"https://graph.facebook.com/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=25) as resp:
        return json.load(resp)


def api_post(path, **fields):
    fields["access_token"] = TOKEN
    data = urllib.parse.urlencode(fields).encode("utf-8")
    req = urllib.request.Request(
        f"https://graph.facebook.com/{path}", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.load(resp)


def nth_sunday(year, month, n):
    d = datetime(year, month, 1)
    first = d.weekday()
    offset = (6 - first) % 7
    return (d + timedelta(days=offset + 7 * (n - 1))).date()


def et_offset(day):
    start = nth_sunday(day.year, 3, 2)
    end = nth_sunday(day.year, 11, 1)
    return -4 if start <= day < end else -5


def token_info():
    if time.time() - _token_cache["at"] < 300:
        return _token_cache["data"]
    info = {"available": False}
    try:
        if USER_TOKEN_FILE.exists():
            ut = USER_TOKEN_FILE.read_text().strip()
            url = "https://graph.facebook.com/debug_token?" + urllib.parse.urlencode(
                {"input_token": ut, "access_token": ut})
            with urllib.request.urlopen(url, timeout=20) as resp:
                d = json.load(resp).get("data", {})
            exp = d.get("expires_at", 0)
            info = {
                "available": True,
                "app": d.get("application", ""),
                "scopes": sorted(d.get("scopes", [])),
                "expires": (datetime.fromtimestamp(exp, timezone.utc).strftime("%Y-%m-%d")
                            if exp else "tidak kedaluwarsa"),
                "valid": d.get("is_valid", False),
            }
    except Exception:
        pass
    _token_cache.update(at=time.time(), data=info)
    return info


def load_bank():
    return json.loads(BANK.read_text(encoding="utf-8"))


def save_bank(bank):
    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_status():
    out = {"server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "page": {},
           "counts": {}, "token": token_info(), "bank": {}, "scheduled": [], "tracker": {}}
    try:
        p = api_get(PAGE, fields="id,name,username,category,about,followers_count")
        out["page"] = {k: p.get(k, "") for k in
                       ("id", "name", "username", "category", "about", "followers_count")}
    except Exception as exc:
        out["page"] = {"error": str(exc)[:150]}
    for key, path, params in (
        ("videos", f"{PAGE}/videos", {"limit": 100}),
        ("scheduled", f"{PAGE}/scheduled_posts", {"limit": 100}),
    ):
        try:
            out["counts"][key] = len(api_get(path, **params).get("data", []))
        except Exception:
            out["counts"][key] = 0
    try:
        out["scheduled"] = [
            {"id": x.get("id", ""),
             "time": datetime.fromtimestamp(
                 x.get("scheduled_publish_time", 0),
                 timezone(timedelta(hours=et_offset(
                     datetime.fromtimestamp(x.get("scheduled_publish_time", 0), timezone.utc).date())))
                 ).strftime("%Y-%m-%d %H:%M ET") if x.get("scheduled_publish_time") else "-",
             "preview": (x.get("message") or "").split("\n")[0][:80]}
            for x in api_get(f"{PAGE}/scheduled_posts",
                             fields="id,message,scheduled_publish_time", limit=100).get("data", [])
        ]
    except Exception:
        out["scheduled"] = []
    bank = load_bank()
    out["bank"] = {
        "total": len(bank),
        "used": sum(1 for p in bank if p.get("used")),
        "next": [p["title"] for p in bank if not p.get("used")][:7],
    }
    if TRACKER.exists():
        with TRACKER.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.reader(fh))
        if len(rows) > 1:
            out["tracker"] = {"last_date": rows[-1][0] if rows[-1] else "",
                              "views": rows[-1][5] if len(rows[-1]) > 5 else "",
                              "note": rows[-1][15] if len(rows[-1]) > 15 else ""}
    return out


def next_available_dates(count):
    """Tanggal ET kosong setelah jadwal terakhir, agar tidak menimpa jadwal lama."""
    dates = set()
    try:
        for item in api_get(f"{PAGE}/scheduled_posts",
                            fields="scheduled_publish_time", limit=100).get("data", []):
            ts = item.get("scheduled_publish_time")
            if ts:
                d = datetime.fromtimestamp(ts, timezone.utc).date()
                dates.add(datetime.fromtimestamp(
                    ts, timezone(timedelta(hours=et_offset(d)))).date())
    except Exception:
        pass
    if dates:
        start = max(dates) + timedelta(days=1)
    else:
        start = datetime.now(timezone.utc).date() + timedelta(days=1)
    return [start + timedelta(days=i) for i in range(count)]


def preview_batch():
    bank = load_bank()
    pending = [p for p in bank if not p.get("used")][:7]
    days = next_available_dates(len(pending))
    return {"message": f"{len(pending)} konten siap dijadwalkan",
            "results": [{"id": p["id"], "title": p["title"],
                         "time": d.strftime("%Y-%m-%d") + " 12:15 ET"}
                        for p, d in zip(pending, days)]}


def schedule_next_batch():
    bank = load_bank()
    pending = [p for p in bank if not p.get("used")][:7]
    if not pending:
        return {"ok": False, "message": "Bank konten habis."}
    days = next_available_dates(len(pending))
    results = []
    for post, day in zip(pending, days):
        when = datetime(day.year, day.month, day.day, 12, 15,
                        tzinfo=timezone(timedelta(hours=et_offset(day))))
        try:
            res = api_post(f"{PAGE}/feed", message=post["message"],
                           published="false",
                           scheduled_publish_time=int(when.timestamp()))
            if res.get("id"):
                post["used"] = True
                post["scheduled_at"] = when.isoformat()
                post["post_id"] = res["id"]
                results.append({"id": post["id"], "status": "OK",
                                "time": when.strftime("%Y-%m-%d %H:%M ET")})
            else:
                results.append({"id": post["id"], "status": "GAGAL", "detail": str(res)[:120]})
        except Exception as exc:
            results.append({"id": post["id"], "status": "GAGAL", "detail": str(exc)[:120]})
        time.sleep(1)
    save_bank(bank)
    ok = sum(1 for r in results if r["status"] == "OK")
    return {"ok": ok == len(results), "message": f"{ok}/{len(results)} post terjadwal.",
            "results": results}


def run_script(cmd, cwd=ROOT):
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180)
        return {"ok": r.returncode == 0, "output": (r.stdout + r.stderr).strip()[-3000:]}
    except Exception as exc:
        return {"ok": False, "output": str(exc)}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path):
        if not path.exists():
            self.send_error(404)
            return
        body = path.read_bytes()
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        route = urllib.parse.urlparse(self.path).path
        if route == "/":
            return self.send_file(PANEL / "index.html")
        if route == "/manifest.json":
            return self.send_file(PANEL / "manifest.json")
        if route == "/icon.png":
            return self.send_file(PANEL / "icon.png")
        if route == "/api/status":
            try:
                return self.send_json(get_status())
            except Exception as exc:
                return self.send_json({"error": str(exc)[:200]}, 500)
        if route == "/api/replies":
            p = ROOT / "tool" / "replies_pending.md"
            return self.send_json({"text": p.read_text(encoding="utf-8") if p.exists() else ""})
        self.send_error(404)

    def do_POST(self):
        route = urllib.parse.urlparse(self.path).path
        if route == "/api/schedule":
            length = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            try:
                payload = json.loads(raw or b"{}")
            except json.JSONDecodeError:
                payload = {}
            if payload.get("preview"):
                return self.send_json(preview_batch())
            return self.send_json(schedule_next_batch())
        if route == "/api/insights":
            return self.send_json(run_script([sys.executable, "tool/weekly_insights.py"]))
        if route == "/api/secrets":
            return self.send_json(run_script(["bash", "tool/set_secrets.sh"]))
        self.send_error(404)


if __name__ == "__main__":
    if not PAGE or not TOKEN:
        raise SystemExit("ERROR: isi PAGE_ID/PAGE_ACCESS_TOKEN di tool/config.env")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"Control Panel: http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
