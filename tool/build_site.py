#!/usr/bin/env python3
"""Bangun situs statis SEO dari bank konten -> docs/ (GitHub Pages)."""
import html
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
PAGES = DOCS / "p"
BANK = ROOT / "content" / "bank.json"
REELS = ROOT / "tool" / "content" / "reels.json"
BASE = "https://sunarno85.github.io/paycheck-playbook"
FB = "https://www.facebook.com/paycheckplaybookus"
SITE_TITLE = "Paycheck Playbook — Practical US Money Tips"
DESC = "Short, practical money habits for US paychecks: budgeting, savings, credit, debt and retirement. For educational purposes only. Not financial advice."
E = html.escape


def shell(title, description, body, url, image=f"{BASE}/icon.png"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(description)}">
<link rel="canonical" href="{E(url)}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Paycheck Playbook">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(description)}">
<meta property="og:url" content="{E(url)}">
<meta property="og:image" content="{E(image)}">
<meta name="twitter:card" content="summary_large_image">
<style>
body{{margin:0 auto;max-width:720px;padding:24px 18px 60px;background:#071F2B;color:#E9F7F4;font:16px/1.65 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
a{{color:#8FE3D0}} h1{{font-size:26px;line-height:1.25;margin:0 0 10px}} h2{{font-size:20px;margin:32px 0 8px}}
.meta{{color:#A9C9C5;font-size:13px;margin-bottom:24px}}
.card{{background:#0F3D3E;border:1px solid #25615f;border-radius:14px;padding:16px 18px;margin:14px 0}}
.post{{white-space:pre-wrap}} nav a{{margin-right:14px;font-size:14px}}
footer{{margin-top:40px;color:#A9C9C5;font-size:13px;border-top:1px solid #25615f;padding-top:16px}}
</style>
<script type="application/ld+json">
{json.dumps({"@context":"https://schema.org","@type":"Organization","name":"Paycheck Playbook","url":BASE,"sameAs":[FB]}, ensure_ascii=False)}
</script>
</head>
<body>
<nav><a href="{BASE}/">Home</a><a href="{FB}">Facebook</a><a href="{BASE}/reels.html">Reels</a></nav>
{body}
<footer>© {datetime.now(timezone.utc).year} Paycheck Playbook · For educational purposes only. Not financial advice.</footer>
</body>
</html>
"""


def slug(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "post"


def post_page(post):
    title = f"{post['title']} — Paycheck Playbook"
    desc = (post["message"].split("\n")[0])[:155]
    url = f"{BASE}/p/{post['id']}-{slug(post['title'])}.html"
    body = (f"<article><h1>{E(post['title'])}</h1>"
            f"<div class='meta'>Paycheck Playbook · US money tips</div>"
            f"<div class='card post'>{E(post['message'])}</div>"
            f"<p><a href='{FB}'>Follow @paycheckplaybookus on Facebook →</a></p></article>")
    return url, shell(title, desc, body, url)


def main():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    reels = json.loads(REELS.read_text(encoding="utf-8"))
    PAGES.mkdir(parents=True, exist_ok=True)
    (DOCS / "icon.png").write_bytes(
        (ROOT / "tool" / "panel" / "icon.png").read_bytes())

    urls = []
    for post in bank:
        url, page = post_page(post)
        (PAGES / url.rsplit("/", 1)[-1]).write_text(page, encoding="utf-8")
        urls.append(url)

    # Hub
    items = []
    for post in bank[:60]:
        url, _ = post_page(post)
        items.append(f"<div class='card'><a href='{E(url)}'>{E(post['title'])}</a></div>")
    body = ("<h1>Paycheck Playbook</h1>"
            "<p>Practical money habits for US paychecks — budgeting, savings, "
            "credit, debt, and retirement. Short posts you can actually use.</p>"
            f"<p><a href='{FB}'><b>Follow on Facebook →</b></a></p>"
            "<h2>Latest posts</h2>" + "".join(items))
    (DOCS / "index.html").write_text(
        shell(SITE_TITLE, DESC, body, f"{BASE}/"), encoding="utf-8")

    # Reel index
    rlines = []
    for reel in reels.values():
        rlines.append(f"<div class='card'><b>{E(reel['title'])}</b><p>{E((reel.get('caption') or '').split(chr(10))[0])}</p></div>")
    (DOCS / "reels.html").write_text(
        shell("Reels — Paycheck Playbook", DESC,
              "<h1>Reels</h1>" + "".join(rlines) + f"<p><a href='{FB}'>Watch on Facebook →</a></p>",
              f"{BASE}/reels.html"), encoding="utf-8")

    sitemap = ["<?xml version='1.0' encoding='UTF-8'?>",
               "<urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'>"]
    for url in [f"{BASE}/", f"{BASE}/reels.html"] + urls:
        sitemap.append(f"<url><loc>{E(url)}</loc></url>")
    sitemap.append("</urlset>")
    (DOCS / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (DOCS / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"docs/: {len(urls)} artikel + index + reels + sitemap")


if __name__ == "__main__":
    main()
