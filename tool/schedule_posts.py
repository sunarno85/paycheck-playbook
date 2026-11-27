#!/usr/bin/env python3
"""Publish welcome post + schedule 7 text posts untuk Paycheck Playbook."""
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Nov–Mar = EST (UTC-5). Sesuai catatan di 01_KALENDER_30_HARI.md.
ET = timezone(timedelta(hours=-5), "EST")

ROOT = Path(__file__).resolve().parent.parent
cfg = {}
for line in (ROOT / "tool" / "config.env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1)
        cfg[k.strip()] = v.strip().strip('"').strip("'")
PAGE, TOKEN = cfg["PAGE_ID"], cfg["PAGE_ACCESS_TOKEN"]

WELCOME = """👋 Welcome to Paycheck Playbook.

I'm here for one thing: making money feel less confusing if you're a working person in the US.

Every week you'll get:
💵 simple budget systems
💳 credit score tips that actually move the needle
🏦 ways to stop paying fees you don't owe
📌 checklists you can save and use on payday

Everything here is education, not financial advice. I'm not a licensed advisor. Do your own research.

👇 Comment "HELLO" and tell me your biggest money struggle — I read every reply."""

POSTS = [
    """7 money habits that quietly changed my life:

1. Pay yourself first on payday — even if it's $10.
2. Automate the transfer so you never have to decide.
3. Track every subscription once a month.
4. Wait 24 hours before any non-essential purchase.
5. Pay more than the minimum when you can.
6. Check your credit report once a year.
7. Keep a small starter buffer before you invest.

Save this for payday. Which one is already a habit for you?

For educational purposes only. Not financial advice.

#PersonalFinance #Budgeting #MoneyTips #USMoney #Paycheck""",

    """Your credit score cares about your balance before the statement closes.

That's called utilization: balance ÷ limit. Lower reported balances usually help your score.

Two simple checks:
• Ask your card when the statement closes.
• Pay the statement balance in full by the due date.

Save this before your next statement. 👇

For educational purposes only. Not financial advice.

#CreditScore #CreditUtilization #PersonalFinance #USMoney""",

    """You probably pay for 4 apps you forgot about.

2-minute audit tonight:
1. Open your card statement.
2. Circle every recurring charge.
3. Cancel anything you haven't used in 30 days.

That's found money — no extra income needed.

Comment "AUDIT" if you found at least one. 👇

For educational purposes only. Not financial advice.

#PersonalFinance #Budgeting #SavingMoney #USMoney""",

    """Got a bank fee you didn't expect? Try one calm sentence.

"Hi, I noticed a fee on my account. I've been a customer for a while and this is unusual for me. Could you waive it as a courtesy?"

One request, polite tone, done. Worst case: they say no.

Save this before your next fee hits.

For educational purposes only. Not financial advice.

#Banking #MoneyTips #PersonalFinance #USMoney""",

    """The 26-week savings challenge is simple:

Week 1: save $1
Week 2: save $2
...
Week 26: save $26

Total: $351.

Or flip it: $50 a week for 26 weeks = $1,300.

Pick the version that fits your paycheck — consistency beats size.

Save this. 👇

For educational purposes only. Not financial advice.

#SavingsChallenge #SavingMoney #PersonalFinance #USMoney""",

    """Payday checklist (save this):

☐ Pay yourself first
☐ Split needs / wants / future
☐ Pay the statement balance in full
☐ Move one small amount to savings
☐ Check for new subscriptions
☐ Write down one money win

Which one do you always skip? Tell me below.

For educational purposes only. Not financial advice.

#Payday #Budgeting #MoneyTips #USMoney""",

    """What's your biggest money stress right now?

A) Rent / housing
B) Credit card debt
C) Not knowing where the money goes
D) Building an emergency fund

Drop your letter below — I read every reply and I'll build the next posts around your answers.

For educational purposes only. Not financial advice.

#PersonalFinance #MoneyTips #USMoney #Paycheck""",
]


def api_post(path, params):
    data = urllib.parse.urlencode(params).encode("utf-8")
    req = urllib.request.Request(
        f"https://graph.facebook.com/{path}", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def describe(res):
    if isinstance(res, dict) and res.get("id"):
        return f"id={res['id']}"
    return str(res)[:200]


if "--schedule-only" not in sys.argv:
    try:
        res = api_post(f"{PAGE}/feed", {"message": WELCOME, "access_token": TOKEN})
        print("welcome:", describe(res))
    except urllib.error.HTTPError as exc:
        print("welcome ERROR:", exc.read().decode("utf-8", "replace")[:250])

now = datetime.now(ET)
for i, message in enumerate(POSTS, start=1):
    when = (now + timedelta(days=i)).replace(hour=12, minute=15, second=0, microsecond=0)
    try:
        res = api_post(f"{PAGE}/feed", {
            "message": message,
            "published": "false",
            "scheduled_publish_time": int(when.timestamp()),
            "access_token": TOKEN,
        })
        print(f"hari+{i} {when:%Y-%m-%d %H:%M %Z}:", describe(res))
    except urllib.error.HTTPError as exc:
        print(f"hari+{i} ERROR:", exc.read().decode("utf-8", "replace")[:250])
