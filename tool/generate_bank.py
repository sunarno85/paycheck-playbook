#!/usr/bin/env python3
"""Tambah konten bank dari topik yang sudah saya susun (tanpa perlu LLM external)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "content" / "bank.json"

# (judul, hook, poin, CTA, hashtag)
TOPICS = [
    ("True hourly wage", "Your hourly wage isn't what your paycheck says.", [
        "Take weekly pay.", "Subtract commute costs, lunches and required gear.",
        "Divide by hours actually worked including commute.",
        "That number is what your time really pays."],
     "Save this before you take a second job. 👇", "#Paycheck #MoneyTips #PersonalFinance #USMoney"),
    ("Emergency fund size", "How big should an emergency fund be?", [
        "Start with $500.", "Then aim for one month of essentials.",
        "Two to six months depends on job stability and dependents.",
        "Progress beats a perfect target."],
     "Save this. 👇 What stage are you at?", "#EmergencyFund #SavingMoney #PersonalFinance #USMoney"),
    ("Statement closing date", "Your card has two dates. Know both.", [
        "Statement date = when your balance is reported.",
        "Due date = when payment must arrive.",
        "Paying before the statement can lower reported utilization.",
        "Autopay the statement balance to avoid interest."],
     "Save this. 👇 Do you know your closing date?", "#CreditScore #CreditCard #PersonalFinance #USMoney"),
    ("Minimum payment trap", "Paying the minimum keeps you in debt longer than you think.", [
        "Minimums are designed to stretch the balance.",
        "Interest keeps compounding on what's left.",
        "Even a small extra payment shortens the timeline.",
        "Check your payoff date on the statement."],
     "Save this. 👇 Want a payoff example?", "#Debt #CreditCard #MoneyTips #USMoney"),
    ("HSA vs FSA", "Two accounts, different rules.", [
        "HSA pairs with high-deductible plans and carries over.",
        "FSA is use-it-or-lose-it, depending on your plan.",
        "Contribution limits change yearly.",
        "Check your plan documents before choosing."],
     "Save this reminder. 👇", "#Healthcare #Benefits #PersonalFinance #USMoney"),
    ("Roth vs traditional", "Two ways to save for retirement, taxed differently.", [
        "Traditional: possible tax deduction now, taxable later.",
        "Roth: no deduction now, qualified withdrawals tax-free.",
        "Your income and employer plan decide what's available.",
        "Read the plan summary before you pick."],
     "Save this. 👇 Which do you have?", "#401k #Retirement #PersonalFinance #USMoney"),
    ("Tax refund plan", "A refund isn't a bonus — it's your money coming back.", [
        "Cover anything you delayed.", "Add to your buffer.",
        "Pay down the highest-interest balance.",
        "Decide the split before the deposit lands."],
     "Save this. 👇 What would you do with yours?", "#Taxes #SavingMoney #PersonalFinance #USMoney"),
    ("Check your W-2", "Before you file, check three lines.", [
        "Wages match your pay stubs.", "Tax withheld looks right.",
        "Retirement contributions match your elections.",
        "Fix errors with your employer, not the IRS first."],
     "Save this. 👇", "#Taxes #Paycheck #PersonalFinance #USMoney"),
    ("Budget app or notebook", "The best budget tool is the one you'll open twice a week.", [
        "Apps automate tracking but need setup.",
        "A notebook forces attention but takes discipline.",
        "A simple spreadsheet sits in the middle.",
        "Try one for 30 days, then decide."],
     "Save this. 👇 Which do you use?", "#Budgeting #MoneyTips #PersonalFinance #USMoney"),
    ("Grocery list method", "A list is a spending limit in disguise.", [
        "Plan meals before you shop.", "Write the list by aisle.",
        "Eat before you go — hungry carts cost more.",
        "Allow one 'want' item so it doesn't blow up."],
     "Save this. 👇", "#Groceries #Budgeting #SavingMoney #USMoney"),
    ("Meal prep math", "Cooking at home isn't automatically cheaper.", [
        "Compare cost per serving, not sticker price.",
        "Batch the ingredients you already buy.",
        "Freeze portions before they turn into takeout.",
        "Track one week to see the real difference."],
     "Save this. 👇", "#MealPrep #Budgeting #PersonalFinance #USMoney"),
    ("Gas price habit", "You don't need to chase the cheapest station.", [
        "Compare the price per gallon on your usual route.",
        "Check tire pressure — it affects mileage.",
        "Combine errands into one loop.",
        "Small habits add up over a month."],
     "Save this. 👇", "#SavingMoney #Budgeting #USMoney"),
    ("Used car checklist", "Before you buy used, bring a checklist.", [
        "Vehicle history report.", "Maintenance records.",
        "Independent mechanic inspection.",
        "Total out-the-door price, not the monthly payment."],
     "Save this. 👇", "#CarBuying #PersonalFinance #MoneyTips #USMoney"),
    ("Lease or buy", "The monthly payment doesn't tell the whole story.", [
        "Leases have mileage limits and fees.",
        "Buying builds equity but costs more upfront.",
        "Calculate total cost over the same time period.",
        "Read the fine print either way."],
     "Save this. 👇", "#CarBuying #PersonalFinance #USMoney"),
    ("Rent negotiation", "You can ask before you sign.", [
        "Research comparable rents nearby.",
        "Ask about move-in specials or longer lease discounts.",
        "Get any promise in writing.",
        "Be polite — worst case is no."],
     "Save this. 👇", "#Renting #Housing #MoneyTips #USMoney"),
    ("Roommate money talk", "Talk about money before you move in.", [
        "Who pays which bill and when.",
        "How shared items are split.",
        "What happens if someone moves out.",
        "Write it down, even between friends."],
     "Save this. 👇", "#Roommates #Housing #PersonalFinance #USMoney"),
    ("Split bills fairly", "Not every bill should be split 50/50.", [
        "Split by income share if it's wildly different.",
        "Assign household items by who uses them.",
        "Use one shared ledger so nobody guesses.",
        "Review monthly, not yearly."],
     "Save this. 👇", # placeholder replaced below
     "#Roommates #Budgeting #PersonalFinance #USMoney"),
    ("Car loan payoff", "Extra payments only help if they go to principal.", [
        "Check whether your lender applies extras to principal.",
        "Ask for a payoff quote.",
        "Compare interest saved versus cash needed elsewhere.",
        "Keep making the regular payment until it's gone."],
     "Save this. 👇", "#DebtPayoff #CarLoan #PersonalFinance #USMoney"),
    ("Call your servicer", "A five-minute call can prevent a big mistake.", [
        "Confirm your balance and interest rate.",
        "Ask how extra payments are applied.",
        "Request the payoff amount in writing.",
        "Save the date and name of who you spoke with."],
     "Save this. 👇", "#StudentLoans #Debt #PersonalFinance #USMoney"),
    ("Holiday spending cap", "Decide the number before December starts.", [
        "List everyone you're buying for.",
        "Set a per-person amount.",
        "Add shipping and wrapping to the total.",
        "When the cap is hit, you're done."],
     "Save this. 👇", "#HolidayBudget #SavingMoney #PersonalFinance #USMoney"),
    ("Gift budget", "Thoughtful doesn't have to mean expensive.", [
        "Set one total, then divide it.",
        "Homemade counts.",
        "Skip the 'just because' add-ons at checkout.",
        "Track as you go, not in January."],
     "Save this. 👇", "#Gifts #Budgeting #SavingMoney #USMoney"),
    ("Giving in the budget", "Giving works better when it's planned.", [
        "Choose a monthly amount first.",
        "Keep it separate from savings.",
        "Review once a year.",
        "No guilt, no guessing at checkout."],
     "Save this. 👇", "#Giving #Budgeting #PersonalFinance #USMoney"),
    ("Savings APY", "Where you keep savings matters.", [
        "APY is what you actually earn after compounding.",
        "Compare similar accounts, not just the big number.",
        "Check minimum balance and withdrawal rules.",
        "Rates move — review twice a year."],
     "Save this. 👇", "#SavingMoney #Banking #PersonalFinance #USMoney"),
    ("CD basics", "A CD trades access for a fixed rate.", [
        "You agree to leave money for a set term.",
        "Early withdrawal usually costs a penalty.",
        "Laddering means several terms at once.",
        "Compare rates and penalties before locking."],
     "Save this. 👇", "#Savings #Banking #PersonalFinance #USMoney"),
    ("Index fund basics", "An index fund buys a whole basket at once.", [
        "It tracks a list instead of picking winners.",
        "Fees still matter over time.",
        "Read the expense ratio and holdings.",
        "Time in the market usually beats timing it."],
     "Save this. 👇", "#Investing #PersonalFinance #USMoney",),
    ("Dollar-cost averaging", "Investing the same amount on a schedule removes timing pressure.", [
        "You buy more shares when prices are lower.",
        "You buy fewer when prices are higher.",
        "It's a rule, not a prediction.",
        "Check whether your plan offers automatic contributions."],
     "Save this. 👇", "#Investing #Retirement #PersonalFinance #USMoney"),
    ("Risk tolerance", "The right investment mix is the one you can hold.", [
        "Ask what a 20% drop would make you do.",
        "If you'd sell, the mix is too aggressive.",
        "Time horizon changes the answer.",
        "Revisit after big life changes."],
     "Save this. 👇", "#Investing #PersonalFinance #USMoney"),
    ("Retirement math", "A quick retirement check you can do tonight.", [
        "Estimate yearly spending in retirement.",
        "Subtract expected guaranteed income.",
        "Multiply the gap by 25 as a rough target.",
        "That's a starting point, not a promise."],
     "Save this. 👇", "#Retirement #PersonalFinance #USMoney"),
    ("Social Security statement", "Check your earnings record once a year.", [
        "Make sure reported wages match your work history.",
        "Look at the estimated benefit at different ages.",
        "Fix errors early, not at claim time.",
        "Create the online account if you don't have one."],
     "Save this. 👇", "#Retirement #PersonalFinance #USMoney"),
    ("Credit freeze", "A credit freeze is free and reversible.", [
        "Freeze with each of the three bureaus.",
        "Keep your PINs somewhere safe.",
        "It stops new accounts, not existing ones.",
        "Unfreeze temporarily when you need new credit."],
     "Save this. 👇", "#IdentityTheft #CreditScore #PersonalFinance #USMoney"),
    ("Fraud alert", "A fraud alert is lighter than a freeze.", [
        "One bureau alert usually notifies the others.",
        "It asks lenders to verify your identity.",
        "It lasts for a set time unless renewed.",
        "A freeze is stronger if you're not applying for credit."],
     "Save this. 👇", "#IdentityTheft #Credit #PersonalFinance #USMoney"),
    ("Debt collector letter", "You have rights when a collector calls.", [
        "Ask for the amount and original creditor in writing.",
        "Don't confirm personal details immediately.",
        "Keep every letter and envelope.",
        "Dispute in writing within the allowed window."],
     "Save this. 👇", "#Debt #ConsumerRights #PersonalFinance #USMoney"),
    ("Medical bill", "A hospital bill is often negotiable.", [
        "Request an itemized statement.",
        "Compare it to the insurance explanation.",
        "Ask about financial assistance policies.",
        "Call the billing office before it goes to collections."],
     "Save this. 👇", "#MedicalBills #PersonalFinance #USMoney"),
    ("Deductible fund", "A deductible is a bill you can plan for.", [
        "Look up your plan's deductible.",
        "Divide it by 12.",
        "Set that aside monthly.",
        "Care becomes less scary when the cash is ready."],
     "Save this. 👇", "#Insurance #SavingMoney #PersonalFinance #USMoney"),
    ("Home repair fund", "Homes don't wait for a convenient month.", [
        "Start with the big systems: roof, HVAC, water heater.",
        "Set a monthly amount even if it's small.",
        "Get two quotes before major work.",
        "Keep records for resale."],
     "Save this. 👇", "#Homeownership #SavingMoney #PersonalFinance #USMoney"),
    ("Pet emergency fund", "Pet care is a budget line, not a surprise.", [
        "Price a routine visit in your area.",
        "Add a cushion for urgent care.",
        "Keep it in savings, not credit.",
        "Review yearly as they age."],
     "Save this. 👇", "#Pets #SavingMoney #PersonalFinance #USMoney"),
    ("Moving budget", "Moving costs more than the truck.", [
        "List deposits, fees, supplies and time off.",
        "Get quotes from two companies.",
        "Declutter before you pack — less to move.",
        "Add a 10% cushion."],
     "Save this. 👇", "#Moving #Budgeting #PersonalFinance #USMoney"),
    ("Raise follow-up", "After a raise, don't let it disappear.", [
        "Update your withholding if needed.",
        "Split the increase: savings, debt, lifestyle.",
        "Decide the split before the first paycheck.",
        "Keep the old budget as your baseline."],
     "Save this. 👇", "#Raise #Paycheck #PersonalFinance #USMoney"),
]


def main():
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    existing = {p["id"] for p in bank}
    n = 1 + max((int(p["id"][1:]) for p in bank
                 if p["id"].startswith("B") and p["id"][1:].isdigit()), default=0)
    added = 0
    for title, hook, points, cta, tags in TOPICS:
        pid = f"B{n:02d}"
        n += 1
        if pid in existing:
            continue
        bullets = "\n".join(f"• {p}" for p in points)
        message = f"{hook}\n\n{bullets}\n\n{cta}\n\nFor educational purposes only. Not financial advice.\n\n{tags}"
        bank.append({"id": pid, "title": title, "message": message,
                     "used": False, "scheduled_at": None, "post_id": None})
        added += 1
    BANK.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"bank sekarang {len(bank)} konten ({added} ditambahkan)")


if __name__ == "__main__":
    main()
