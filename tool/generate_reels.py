#!/usr/bin/env python3
"""Tambah skrip Reel R13-R20 ke tool/content/reels.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FILE = ROOT / "content" / "reels.json"

NEW = [
    {
        "id": "R13", "title": "True hourly wage",
        "vo": "Your salary isn't what you think it is. Take your weekly pay, then subtract the costs of working — commute, lunches, daycare, uniforms. Divide what's left by every hour you actually give to work, including the commute. That's your real hourly wage. A fifteen dollar job with an hour commute and paid parking might really be eleven. Before you take a raise or a second job, know the number. For educational purposes only. Not financial advice.",
        "overlays": ["Paycheck ≠ hourly wage", "Subtract commute + costs", "Divide by real hours"],
        "stock_queries": ["commuter train", "office desk", "calculator"],
        "caption": "Know your real hourly wage before you say yes to overtime. Save this.\n\nFor educational purposes only. Not financial advice.\n\n#Paycheck #PersonalFinance #MoneyTips #USMoney",
    },
    {
        "id": "R14", "title": "Credit freeze",
        "vo": "A credit freeze is free and it stops someone from opening accounts in your name. Do it with all three bureaus — Equifax, Experian, and TransUnion. You'll get a PIN for each one, so save them somewhere safe. It doesn't lower your score, and it doesn't stop accounts you already have. When you need new credit, unfreeze it temporarily. Ten minutes today can prevent months of cleanup. For educational purposes only. Not financial advice.",
        "overlays": ["Free + reversible", "Do all 3 bureaus", "Save your PINs"],
        "stock_queries": ["phone security screen", "envelope with mail", "computer desk"],
        "caption": "Have you frozen your credit? Save this for later.\n\nFor educational purposes only. Not financial advice.\n\n#CreditScore #IdentityTheft #PersonalFinance #USMoney",
    },
    {
        "id": "R15", "title": "Tax refund plan",
        "vo": "A tax refund feels like a bonus, but it's your own money coming back. Before it lands, decide the split. First, cover anything you put off — a car repair, a medical bill. Second, add to your starter savings. Third, attack the highest interest debt. Whatever's left can be a small treat. Decide now, because money sitting in checking has a way of disappearing. For educational purposes only. Not financial advice.",
        "overlays": ["Refund = your money", "1. Delayed bills", "2. Savings", "3. High-interest debt"],
        "stock_queries": ["tax documents", "bank app transfer", "calculator"],
        "caption": "What's your refund plan? Save this before the deposit lands.\n\nFor educational purposes only. Not financial advice.\n\n#Taxes #SavingMoney #PersonalFinance #USMoney",
    },
    {
        "id": "R16", "title": "Medical bill check",
        "vo": "Got a medical bill that makes no sense? Ask for an itemized statement. Compare it with the explanation of benefits from your insurer. Then call the billing office and ask two questions: can this be adjusted, and do you have a financial assistance policy? Many hospitals do. Never ignore it — unpaid medical bills can end up in collections. For educational purposes only. Not financial advice.",
        "overlays": ["Ask for itemized bill", "Compare to EOB", "Ask about assistance"],
        "stock_queries": ["medical paperwork", "hospital corridor", "phone call"],
        "caption": "Save this before you pay a bill you don't understand.\n\nFor educational purposes only. Not financial advice.\n\n#MedicalBills #PersonalFinance #MoneyTips #USMoney",
    },
    {
        "id": "R17", "title": "Rent increase",
        "vo": "Your lease is up and the landlord wants more. Before you panic, check three things: comparable rents in your zip code, whether you've been a reliable tenant, and if new tenants are getting a move-in special. Then ask politely for a smaller increase or a longer lease. Get the answer in writing. Worst case, you finally know your options. For educational purposes only. Not financial advice.",
        "overlays": ["Check comparables", "Ask politely", "Get it in writing"],
        "stock_queries": ["apartment building", "lease paperwork", "apartment keys"],
        "caption": "Would you negotiate rent? Save this before your renewal.\n\nFor educational purposes only. Not financial advice.\n\n#Renting #Housing #PersonalFinance #USMoney",
    },
    {
        "id": "R18", "title": "Insurance quotes",
        "vo": "Shopping insurance once a year can free up real cash. Get quotes for auto and renters from at least three companies. Ask about bundling and loyalty discounts — but don't assume they're automatic. Raise your deductible only if you actually have that amount saved. Cheaper isn't better if you can't cover the claim yourself. For educational purposes only. Not financial advice.",
        "overlays": ["3 quotes minimum", "Ask about discounts", "Deductible must be saved"],
        "stock_queries": ["car keys", "insurance documents", "laptop comparison"],
        "caption": "When did you last shop your insurance? Save this.\n\nFor educational purposes only. Not financial advice.\n\n#Insurance #SavingMoney #PersonalFinance #USMoney",
    },
    {
        "id": "R19", "title": "Payday checklist",
        "vo": "Payday checklist in thirty seconds. One: pay yourself first. Two: fund your sinking buckets. Three: pay the statement balance in full. Four: check for new subscriptions. Five: write down one money win. That's the whole system. Do it in the same order every time and it stops being a chore. For educational purposes only. Not financial advice.",
        "overlays": ["1. Pay yourself", "2. Sinking funds", "3. Pay in full", "4. Subscriptions", "5. One win"],
        "stock_queries": ["paycheck paper", "bank app on phone", "notebook and pen"],
        "caption": "Which step do you always skip? Save this for payday.\n\nFor educational purposes only. Not financial advice.\n\n#Payday #Budgeting #PersonalFinance #USMoney",
    },
    {
        "id": "R20", "title": "Weekly money date",
        "vo": "Pick one day a week for twenty minutes. Open your accounts, check what came in and what went out, look at next week's bills, and write down one thing that went well. That's it. No perfect spreadsheet required. The goal isn't to obsess — it's to stop being surprised. For educational purposes only. Not financial advice.",
        "overlays": ["20 minutes, once a week", "In / out / upcoming", "One win"],
        "stock_queries": ["desk with notebook", "calendar on phone", "coffee and laptop"],
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
    print(f"reels.json sekarang {len(data)} skrip ({added} ditambahkan)")


if __name__ == "__main__":
    main()
