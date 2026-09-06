<!-- The debt with no end date · Gal Tidhar — https://gal.tidhar.org.il/blog/money-audit/ -->

# The debt with no end date

Cancelling my father's junk app subscriptions took an evening. Then I connected both my parents' banks and cards through open banking and found something far more expensive and far quieter: a credit card that has been **revolving at 17.69% since 2006**. If not another shekel was ever added to it, a **ILS 232** purchase back then is a **ILS 6,028** debt today. Nobody bought anything. It just sat there, doubling every 4.3 years, with no schedule and no date it ends.

## Why a statement cannot show you this

Nine institutions. Eighty-three accounts once you count every card, loan, savings plan and pension. Two people. A year is roughly **2,400 transactions**, arriving as one PDF per month per account.

A charge is never suspicious on its own statement. It is suspicious next to everything else - because it repeats weekly, or because it sits on a card carrying 17% while cash does nothing in a different bank. The statement is built to show you one account at a time, which is exactly the view that hides all four of these.

`python3 openbank.py pull # aggregator API -> local snapshot.db
python3 openbank.py sql "SELECT ..." # ask across all of it at once`

 A loan ends. This does not.
 Everyone knows what a loan is: an amount, a schedule, a rate, and a date on which it is gone. Revolving credit is sold in the same aisle and is a different object entirely. It starts when one month's card bill is not paid in full. From then on there is **no schedule and no end date**. The balance is simply carried, interest is applied to it, and the arrangement continues for as long as the minimum payment keeps arriving.

At 17.69%, the balance doubles every **4.3 years**. Compounded across twenty years that is a factor of about **26**:

| Year | Balance, if nothing is ever added |
|---|---|
| 2006 | ILS 232 |
| 2010 | ILS 448 |
| 2014 | ILS 866 |
| 2018 | ILS 1,673 |
| 2022 | ILS 3,232 |
| 2026 | **ILS 6,028** |

The real card was not static, of course - things were bought and payments were made. The point of the table is the shape: whatever went on that card in 2006 was small, and the number sitting there now is not.

## Five reasons nobody ever sees it

This is the part worth internalising, because every one of these is structural rather than accidental.

1. **The interest is not a line on the statement.** It is already inside the balance you are asked to pay. No row anywhere says "this month the debt cost you ILS 900". Twenty years, and that number has never once been written in front of the two people paying it.
2. **It is not a charge, so it cannot be searched for.** Every instinct - and every budgeting app - looks at transactions. This lives in the fields of the account itself, a place nobody opens.
3. **The minimum payment looks like responsible behaviour.** It is paid on time, every month, and it is precisely the mechanism keeping the balance alive.
4. **There is no end date to notice passing.** A loan that never finished would be alarming. This never had a finish line to miss.
5. **It is the most profitable debt a card issuer holds.** Nobody is going to call and point it out. Nothing about that is illegal.

Together with a second card at 13%, that is roughly **ILS 70,000 at 13-18%**, costing about **ILS 1,000 a month** in interest alone.

## And a bank away, the money that could kill it

**ILS 40,000** idle in a joint checking account earning nothing, while ILS 70,000 revolves at 13-18% somewhere else. The two are at different institutions, so neither app knows the other exists, and no advisor has ever seen both at once.

The fix is embarrassing: move money from one pocket to the other. It is worth around **ILS 700 a month** and requires no discipline, no budgeting, and no giving anything up. It simply requires a view that spans two banks, which is the one thing the banking system does not sell you.

## The same query also found: PayPal billing agreements

About **ILS 11,000 over twelve months**: dropshipping, supplements, small overseas suppliers. Not impulse purchases - **live billing agreements**, authorised once, years ago, when an order was placed.

This is the mechanism worth understanding, because it defeats every piece of standard advice:

- It is **not** in the Google Play or App Store subscription list, which is where everyone is told to look.
- The merchant does not have to email you before charging. Many do not.
- It lives in one place only: PayPal, under _Settings → Payments → Automatic payments_. Almost nobody has opened that page.
- On the card statement it shows up as "PAYPAL", with the actual merchant name buried or absent.

Three of the agreements still active pointed at Chinese suppliers for orders placed years ago and long forgotten.

## And three health policies - with a correction

Three private policies from three insurers on top of the public fund, about ILS 1,500 a month. My first read was "you cannot claim the same event three times, so two of these are waste". That is **only half right**, and the half that is wrong matters:

- **Reimbursement cover (שיפוי)** - surgery, medication, treatment abroad - pays back an expense you actually incurred, against receipts. Hold three of those and one event still gets reimbursed once. That overlap is real waste.
- **Compensation cover (פיצוי)** - long-term care (סיעודי), critical illness - pays a fixed agreed sum with no receipts. Those **do** pay in parallel, from every insurer holding one. Cancelling a second סיעודי policy because it "duplicates" throws away money you would genuinely have received.

So the correct action is not "cancel the duplicates". It is: sort the three policies into שיפוי and פיצוי clauses first, and only then decide. I had this wrong before someone who knows the market pushed back, and the correction is worth more than the original finding.

## Nobody here broke a law

That is the part that got under my skin. There is no villain to shout at. One month in 2006 where a card bill was not paid in full, one bank that does not talk to another, a card issuer reporting exactly what regulation requires, three insurance agents each doing their job. And at the end of it, two people who count every shekel at the supermarket are paying roughly **ILS 3,000 a month for nothing**, without a single illegal act anywhere in the chain.

The scam apps were the easy part. They are theft and they are obvious once you look. This is worse, because it is all working as designed.

## Two traps if you run this yourself

Both produce confidently wrong numbers, and both are worth knowing before you tell a pensioner anything about their money.

### 1. A revolving card reports as many snapshots of itself

An Israeli card issuer reports a rolling credit product as **one row per monthly cycle**: same account number, a different contract start date each month. Thirteen months on file look exactly like thirteen separate loans. Sum them and you multiply the debt by the number of cycles on record - a 10x error, in my case, on the single most frightening number in the whole audit.

`-- WRONG
SELECT SUM(balance) FROM accounts WHERE account_type='loan';

-- RIGHT: latest snapshot per distinct account number
WITH latest AS (
 SELECT account_number, MAX(reference_date) rd FROM accounts
 WHERE account_type='loan' GROUP BY 1)
SELECT a.person, a.account_number, a.balance FROM accounts a
JOIN latest l ON l.account_number = a.account_number
 AND l.rd = a.reference_date;`
 2. The same person has two spellings
 One bank holds her name in Hebrew, another in Latin characters. Filter a total by the owner string the bank gives you and entire cards vanish from it silently. Resolve every owner string to a person first, then filter on the person.

And one rule that is not technical: **the transaction data cannot tell a fraud from a supplier.** Two merchants I had flagged as scams turned out to be legitimate - one is my father's actual e-cigarette supplier, with real order confirmations sitting in his mailbox. Check the mailbox before you accuse anyone of anything.

## What it costs, honestly

Israeli open banking (חוק שירות מידע פיננסי, live since 2023) opens bank APIs only to a licensed information-service provider. There is no consumer tier, so for anyone else's accounts you are **renting a licence**, not paying for a wrapper. The EU/UK PSD2 equivalent works the same way.

| Line item | Cost |
|---|---|
| Open-banking aggregator (Israel: Financy / Open-Finance.ai, Starter tier) | ILS 49/month, cancellable |
| Model time for the audit - about 2,000 assistant turns in one day | ~USD 1,700 at API list prices |
| What I actually paid for that model time | a USD 200/month subscription |

I am printing the API number because "look what AI did for free" is a lie. Paid per token, this day costs more than a financial advisor charges for an hour. It was worth it because it did not stop after an hour, and because an advisor would not have opened PayPal's automatic-payments page either.

## Findings change nothing. Actions do.

After the report, with them present and approving item by item: every junk subscription cancelled with its end date recorded, **40+ refund requests filed** and confirmed in writing, cancellation emails sent to the services with no cancel button, and one Hebrew page with a tick-box list of what is left - the items that need their password, their phone, or a visit to the bank.

Recoverable without giving up a single thing they enjoy: **ILS 3,000-4,500 a month.** A trip abroad every year, funded entirely by things that were taking money for nothing.

## Three things you can check tonight, with no tools at all

1. **How much interest did they pay last month?** Not the balance. The cost.
2. **PayPal → Settings → Payments → Automatic payments.** Everything listed there can charge them tomorrow, with no email first.
3. **Is any card set to revolving or minimum payment?** That is the switch that turns a bill into a permanent debt.

Most people cannot answer any of the three about their own accounts, let alone their parents'.

### The skill

The whole pipeline is packaged as an installable agent skill - the aggregator pull, the per-person ownership resolver, the query playbook, both traps written down so they cost you nothing, and the rule about checking the mailbox before accusing a merchant.

[money-audit on GitHub ↗](https://github.com/tatarco/agent-skills/tree/main/skills/money-audit) · [Part one: the subscriptions ←](/blog/subscription-audit/) · [All field notes](/) · [LinkedIn ↗](https://www.linkedin.com/in/galtidhar/)
