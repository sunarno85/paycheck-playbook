#!/usr/bin/env python3
"""Tambah skrip Reel R21-R28 untuk jadwal 2x seminggu."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILE = ROOT / "content" / "reels.json"

NEW = [
    {
        "id": "R21", "title": "Overdraft fee opt-out",
        "vo": "Your bank may be charging you for using your own money. At many banks, you can opt out of overdraft coverage for everyday purchases. Then a card payment with no balance is simply declined — no fee. Keep alerts on and link a backup account for real bills. Call the number on your card and ask how to opt out. For educational purposes only. Not financial advice.",
        "overlays": ["Ask to opt out", "Declined ≠ fee", "Keep alerts on"],
        "stock_queries": ["bank card", "phone banking app", "bank counter"],
        "caption": "Did you know you can often opt out? Save this before your next fee.\n\nFor educational purposes only. Not financial advice.\n\n#Banking #MoneyTips #PersonalFinance #USMoney",
    },
    {
        "id": "R22", "title": "Split your deposit",
        "vo": "You can split your direct deposit without doing anything on payday. Ask your payroll portal for a split: a fixed amount goes straight to savings, the rest to checking. If the amount changes, use percentages instead. It's the closest thing to paying yourself first on autopilot. For educational purposes only. Not financial advice.",
        "overlays": ["Payroll → split deposit", "Savings first", "Rest to checking"],
        "stock_queries": ["paycheck paper", "bank app on phone", "savings jar"],
        "caption": "Set it once, then forget it. Save this for your next paycheck.\n\nFor educational purposes only. Not financial advice.\n\n#Paycheck #SavingMoney #PersonalFinance #USMoney",
    },
    {
        "id": "R23", "title": "Subscription audit",
        "vo": "Open your last card statement and circle every recurring charge. Ask three questions: did I use it, would I miss it, and is there a cheaper plan? Then cancel just one. Do this every thirty days, not once a year. One small cancellation each month is twelve fewer charges next year. For educational purposes only. Not financial advice.",
        "overlays": ["Circle recurring charges", "Cancel just one", "Repeat in 30 days"],
        "stock_queries": ["credit card statement", "phone subscriptions", "laptop screen"],
        "caption": "Comment AUDIT if you found one. Save this.\n\nFor educational purposes only. Not financial advice.\n\n#Subscriptions #SavingMoney #PersonalFinance #USMoney",
    },
    {
        "id": "R24", "title": "Statement vs due date",
        "vo": "Your card has two dates people mix up. The statement closing date is when your balance gets reported to the bureaus. The due date is when your payment must arrive. Paying before the closing date can lower reported utilization. Autopay the statement balance so you never pay interest. Check both dates tonight. For educational purposes only. Not financial advice.",
        "overlays": ["Closing = reported", "Due = pay by", "Autopay statement balance"],
        "stock_queries": ["credit card", "paper statement", "calendar"],
        "caption": "Do you know both dates? Save this.\n\nFor educational purposes only. Not financial advice.\n\n#CreditScore #CreditCard #PersonalFinance #USMoney",
    },
    {
        "id": "R25", "title": "Starter emergency fund",
        "vo": "Don't aim for six months of expenses on day one. Start with five hundred dollars. It absorbs a flat tire, a small copay, a late deposit. Keep it in a separate savings account so you don't spend it accidentally. Once that's done, target one month of essentials. Progress beats a perfect number. For educational purposes only. Not financial advice.",
        "overlays": ["Step 1: $500", "Separate account", "Then 1 month"],
        "stock_queries": ["savings account", "car keys", "piggy bank"],
        "caption": "What stage are you at? Save this.\n\nFor educational purposes only. Not financial advice.\n\n#EmergencyFund #SavingMoney #PersonalFinance #USMoney",
    },
    {
        "id": "R26", "title": "Ask for a better rate",
        "vo": "One polite phone call can lower a bill. Try this: I've been a customer for a while and I'd like to stay. Could you check if there's a lower rate or a retention offer available? Ask once, be specific, and get the new price in writing. Worst case, they say no. Best case, you keep the cash. For educational purposes only. Not financial advice.",
        "overlays": ["Call retention", "One specific request", "Get it in writing"],
        "stock_queries": ["phone call", "internet router", "billing paperwork"],
        "caption": "Save this before your next bill.\n\nFor educational purposes only. Not financial advice.\n\n#Bills #SavingMoney #PersonalFinance #USMoney",
    },
    {
        "id": "R27", "title": "Payday loan APR",
        "vo": "A small fee can hide a very large interest rate. If a two-week loan charges fifteen dollars on a hundred, that's roughly four hundred percent a year. Before you sign, ask for the APR in writing and check the rollover fee. If the fee repeats twice, you've paid far more than you borrowed. A credit union small loan may cost less. For educational purposes only. Not financial advice.",
        "overlays": ["$15 on $100 ≈ 400% APR", "Ask for APR in writing", "Watch rollover fees"],
        "stock_queries": ["cash money", "paperwork on desk", "calculator"],
        "caption": "Read the APR, not just the fee. Save this.\n\nFor educational purposes only. Not financial advice.\n\n#Debt #MoneyTips #PersonalFinance #USMoney",
    },
    {
        "id": "R28", "title": "Weekly money date",
        "vo": "Pick one day a week, twenty minutes, same time. Check what came in, what went out, and next week's bills. Then write down one thing that went well. That's the whole system. The goal isn't to obsess over numbers — it's to stop being surprised by them. For educational purposes only. Not financial advice.",
        "overlays": ["20 minutes, once a week", "In / out / upcoming", "One win"],
        "stock_queries": ["notebook and pen", "calendar on phone", "desk with laptop"],
        "caption": "Which day is your money date? Save this.\n\nFor educational purposes only. Not financial advice.\n\n#MoneyDate #Budgeting #PersonalFinance #USMoney",
    },
]


def main():
    data = json.loads(FILE.read_text(encoding="utf-8"))
    added = 0
    for reel in NEW:
        if reel["id"] not in data:
            data[reel["id"]] = reel
            added += 1
    FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"reels.json: {len(data)} skrip ({added} ditambahkan)")


if __name__ == "__main__":
    main()
