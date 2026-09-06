<!-- My 83-year-old father was paying 16,000 shekels a year for nothing · Gal Tidhar — https://gal.tidhar.org.il/blog/subscription-audit/ -->

# My 83-year-old father was paying 16,000 shekels a year for nothing

It started as a favour. His Windows machine was **"annoying"** - three monitors shuffled around, the Start button not opening, icons too small. I sat down to fix it. Six hours later I had cancelled fifteen subscriptions, filed a refund claim for ILS 3,658, and understood that the broken Start button and the missing money were **the same problem**.

## The Start button was a symptom

The first scan of the machine returned something I did not expect: **four security products running at once.** Norton Security Ultra, Avast Premium Security, Avast Cleanup Premium, Avast Driver Updater. Plus a separate paid McAfee subscription that had never been installed.

Windows Defender was switched off entirely, signature age 65535 days. So the machine was _less_ protected than a stock install.

And the Start button crash had a specific cause:

`Faulting application: StartMenuExperienceHost.exe
Faulting module: Windows.UI.Xaml.dll
Exception type: BEX64`
 `BEX64` is a DEP/buffer-overflow fault. The overwhelmingly common cause is third-party code injecting into the shell process - which is exactly what two real-time scanners do when they both hook the same Xaml host. The hosts file had also been rewritten by the security software, and the event log showed `Name resolution policy table has been corrupted`.

## Then I opened his Google Play account

Five active **weekly** subscriptions:

| App | Developer | Price | Per year |
|---|---|---|---|
| Wallet - Digital Card Wallet | YILDIZCO (Turkey) | ILS 75.00/wk | 3,900 |
| QR Code Reader | DELTA TECHNOLOGIES | ILS 54.90/wk | 2,855 |
| Photo Recovery | Technoline Apps | ILS 54.90/wk | 2,855 |
| File Recovery | brain | ILS 46.00/wk | 2,392 |
| Wallet - Digital Card Wallet _(again)_ | YILDIZCO (Turkey) | ILS 31.00/wk | 1,612 |

ILS 261.80 a week. **ILS 13,614 a year**, for an app that reads barcodes and two that claim to recover deleted photos.

The detail that mattered most was not the total. It was that **the same wallet app appears twice**, at two different prices, running concurrently - and one of them reported "0 of 1 devices used", meaning it was never even installed. Nobody subscribes twice to one app at two prices on purpose. That single fact is what makes "he understood what he was agreeing to" impossible to argue.

The package identifier of the QR reader is `com.thetrojanapps.qrcode.reader.scanner`. The developer named themselves "the trojan apps".

Receipt volume went from 1 in October 2025 to 29 in July 2026. That escalation curve is the signature of ad funnels inside one junk app selling the next one - not of a person repeatedly choosing to subscribe.

## A third of his phone bill was kitchen appliances

His mobile bill was ILS 464.44 a month. Only **ILS 126.87** of that was telephone service. The remaining **ILS 337.57** was instalments on household appliances, sold to him over the phone and folded into the bill on 36-month plans:

| Item | He pays | Typical retail | Markup |
|---|---|---|---|
| Dyson V15s Detect | ILS 6,084 | ~2,100-2,300 | ~165-190% |
| Ninja Foodi MAX PRO | ILS 2,538 | ~1,000-1,340 | ~90-150% |
| Ninja CI100 processor | ILS 1,404 | ~330-500 | ~180-325% |
| Knife set with stand | ILS 1,404 | ~150-400 | very high |
| Cortex Air Styler | ILS 723 | ~295-350 | ~105-145% |

ILS 12,152 of appliances at roughly **three times retail**, with about ILS 6,000 still outstanding. The invoice never prints a cash price, so there is nothing on the page to compare against. The markup is structurally invisible.

## How the audit actually runs

Three components. None of them clever.

### 1. Read access to the mailbox, without hijacking your own

The Gmail CLI I already use takes a token path from the environment, so a second mailbox is just a second token file:

`GMAIL_TOKEN=token_dad.json python3 gmail_cli.py auth`
 One browser consent, by someone who has the password. Every later command carries the same variable. My own inbox stays the default and is never touched.

### 2. Rank senders, do not read mail

The sweep runs a dozen billing-shaped queries - receipt, invoice, renewal, the payment processors, the app stores, and the same words in Hebrew - then **ranks senders by frequency**. You do not read anyone's email. A payee that bills monthly for a year floats to the top on its own.

`=== RECURRING PAYEE CANDIDATES (by frequency) ===
 42 Google Play 
 12 noreply.il@gotoglobal.com
 8 Microsoft 
 5 Zoom Communications 
 1 McAfee `
 3. The amounts are in the PDFs, not the emails
 Almost every real invoice arrives as an attachment. Harvest them, extract the text, pull out amounts, dates and card digits. That is how the appliance instalments surfaced - they exist nowhere in the email body, only on page 6 of an eight-page PDF.

Then a browser agent signs into each account and cancels, one at a time, verifying the account page after every single one.

## The refund argument that works

Refund windows govern _changed minds_. They do not govern _a product that was never delivered_. That distinction is the whole game.

McAfee's payment history told the story better than I could:

| Year | Charge |
|---|---|
| 2018 | USD 31.99 _(intro)_ |
| 2019 | USD 99.99 |
| 2021 | USD 119.99 |
| 2022-2026 | USD 129.99 × 5 |

USD 901.92 across eight years - with **0 devices protected** the entire time. I was two days past their 60-day refund window and said so. The refund was approved anyway, in about eight minutes, because the argument was not "he changed his mind", it was "this protected nothing, ever".

> Look for: "0 devices protected", "0 of 1 devices used", two concurrent subscriptions to one product, a price that started as a promo and multiplied, or charge frequency rising with no change in use.

## Two things I would not do differently, and one I would

**I told every support agent who I actually was.** "I manage this account for my father" - not a claim to be him. It cost nothing; the McAfee agent said "Hello Gal" and processed the refund. A false identity claim is the thread that unravels a chargeback six months later.

**I ran a verification pass before sharing any of it.** An independent check re-derived every figure from the raw invoices and found two real errors in my summary - a tariff table that did not reconcile, and a causal claim about a backup payment card that the evidence did not support. Both were fixed before anyone read it. Arithmetic mistakes in a financial document destroy the credibility of the true findings sitting next to them.

**What I would do differently:** get the card statements first. They are not in email - I checked 36 months across every Israeli bank and card issuer, and the statements simply are not there. Four different cards were in play. The mailbox only shows you what bothered to send a receipt.

## If you want to check your own parent's account

Two minutes, no tooling:

1. Open `play.google.com/store/account/subscriptions` on their account.
2. Look for anything billed **weekly**. A weekly price on a utility app is never legitimate.
3. Open their phone bill and compare the total against the line items for actual phone service.
4. Count the antivirus products. If it is more than one, that is the cause of whatever else is wrong with the machine.

### The skill

The whole thing is packaged as a reusable agent skill - the mailbox sweep, the PDF parser, the account URLs, the browser patterns that stop it wasting an hour, and the refund arguments. It works on any mailbox, not just an Israeli one.

[← All field notes](/) · [LinkedIn ↗](https://www.linkedin.com/in/galtidhar/)
