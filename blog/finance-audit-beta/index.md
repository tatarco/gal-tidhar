<!-- The audit, as software you run yourself · Gal Tidhar — https://gal.tidhar.org.il/blog/finance-audit-beta/ -->

# The audit, as software you run yourself

I have now run this audit four times by hand - my parents, my sister, my wife's family. Every one of them found real money, and **two of them shipped wrong numbers to the family before I caught them myself**. Those two corrections are the reason there is now a tool instead of a habit. It runs entirely on your machine, it is built on other people's excellent open-source work, and the part that actually matters is not the code.

## Credit where it belongs

The hard, unglamorous problem - logging into an Israeli bank and getting a year of transactions out of it - was solved a decade ago by people who are not me:

- **[israeli-bank-scrapers](https://github.com/eshaham/israeli-bank-scrapers)** by Eshed Shaham. MIT, public since 2017, and the reason this project is a weekend of wiring rather than a year of reverse engineering.
- **[Caspion](https://github.com/brafdlog/caspion)** by Brafdlog. MIT, built on top of the scrapers, and the prior art that shows this shape of tool has existed openly in Israel for years.
- **Puppeteer** for the browser, and **Node 22's built-in `node:sqlite`** so nothing compiles at install time.

What I added is a wrapper, a UI an adult child can drive on a parent's behalf, a Gmail pass, and a checklist. The checklist is the valuable half.

## Why it is software you install, and not a website

Israel sits outside PSD2, so no global aggregator - Plaid, Tink, TrueLayer, GoCardless, Enable Banking - covers Israeli banks. The licensed Israeli aggregators are all paid, and none of them has a free tier with API access. There is no back door here: the only free path to your own bank data is a browser doing what you would do by hand.

The regulation matters more than the pricing. Israel's Financial Information Service Law puts financial-data aggregation under the **Israel Securities Authority** - not the Capital Market Authority, a distinction that cost me a research cycle. The law has **no "for consideration" qualifier and no "by way of business" qualifier**. Being free does not exempt you. There is no nonprofit carve-out and no de-minimis threshold. A website where strangers type their bank credentials would need a licence.

Software that a person installs and runs on their own machine, with their own credentials, where I never receive a byte, is a different legal object: I am distributing software, not collecting data. Both libraries above have been public and Israeli-made for years on that same basis.

## Say the uncomfortable part out loud

This tool asks someone to type a bank password into something that is not the bank. That is the exact pattern every fraud department spends its budget fighting, and pretending otherwise would be worse than the risk. So, plainly:

- Everything runs on your machine. Nothing is sent anywhere. I do not receive a byte and there is no server to receive it.
- The password is **never written to disk** - not encrypted, simply never stored. It goes from the field to the browser and is gone when the process exits.
- Access is **read-only**. There is no code path that moves money.
- The Chrome window is **visible**. You watch the login happen, exactly as you would if you did it yourself.
- It is **not** open banking, and I will not call it that. It is a scraper with your consent and your credentials, on your hardware.

## The six ways to be confidently wrong

This is the actual product. It is a checklist distilled from four real audits, including the two that shipped wrong numbers, and it is what gets pushed into the model's context before it looks at a single shekel. **Four of these six are interpretation errors, not arithmetic** - which means a careful review of the maths passes every one of them.

1. **Inflow is not income.** A savings drawdown, a loan landing, and a cash advance on a credit card all look identical to money arriving. One audit reported a deficit **three times too small** because of this, and note the direction: the error _hid_ the problem rather than exaggerating it.
2. **Co-occurrence is not concurrency.** Two insurers billing in the same months can be a clean handover, not a duplicate policy. This one was caught publicly, by the person whose money it was.
3. **A data feed that starts late looks exactly like a new expense.** One audit claimed a charge "jumped 18x" when the card's history simply began nine days earlier than the comparison window.
4. **Partial boundary months.** Salary lands once a month and spending happens daily, so half a month at the edge of the window reads as a deficit in a perfectly healthy household.
5. **One person, two spellings.** One bank holds a name in Hebrew, another in Latin characters. Filter by the owner string and whole cards vanish from the total, silently.
6. **A revolving card reports one row per monthly cycle.** Thirteen months on file look like thirteen loans. Sum them and you multiply the debt by the number of cycles - a 10x error on the most frightening number in the report.

Items 1 through 4 are the interpretation half. No amount of double-checking the sums catches any of them, because the sums are right and the meaning is wrong.

## Four engineering notes, from real bugs

### 1. A bank that refuses in silence

With a fresh browser profile on every run, the bank sees a brand-new device and **silently declines to submit the form**. No error, no OTP challenge, no failed-login message - nothing at all. A persistent profile is not a convenience here, it is the difference between working and not.

### 2. A race that settles on the first rejection

A `Promise.race` over four selectors reported a failure for a login that had **already succeeded in six seconds**, because a race settles on the first rejection just as happily as on the first resolution. One of those four had also inherited Puppeteer's 30-second default while its three siblings had 60, so on a slow login it lost a race it was never given time to win. Patched at runtime rather than by editing `node_modules`, so `npm update` cannot quietly drop the fix.

### 3. A 448KB Chrome that exits 0

The browser download produced a **448KB** Chrome instead of roughly **340MB**, left a plausible-looking executable in place, and **exited zero**. The `.app` had no `Frameworks` directory, so it died mid-scrape with an unreadable `dlopen` error. The zip was fine; the library's own extractor was failing silently where the system `unzip` succeeded.

### 4. Your global config is not neutral when you shell out to an agent

The analysis runs through `claude -p` with `--output-format stream-json`, so you watch each query and each conclusion arrive instead of staring at a spinner. It also runs `--safe-mode`, and that flag is not paranoia. Without it the subprocess **inherits the operator's own `CLAUDE.md`, hooks and output styles**. On my machine that meant a "be terse, one-sentence answers" instruction and a "you are a lazy senior developer" hook were being injected into the agent writing a household financial report.

## What actually works today

Being precise about this is the whole point of a beta.

| Piece | Status |
|---|---|
| Bank Leumi: 1 account, 152 transactions, 12 months | verified end to end |
| Local SQLite, idempotent resync (content-hashed keys) | verified - re-running a period upserts, never duplicates |
| Gmail harvest: 260 message headers, no OAuth, no cloud project | verified, and the most fragile code in the repo |
| Streamed analysis through `claude -p` | verified |
| The other 14 institutions | **wired, ids validate, never run against a live account** |

I would rather say that plainly than imply coverage I have not earned. Finding out which of the fourteen break, and where a non-technical operator gets stuck, is the entire purpose of the cohort.

## What a beta tester needs

- macOS or Linux, and Node 22 or newer.
- A Claude Code subscription - the analysis runs through your account, not mine.
- **The account owner sitting next to you** to type the code from the SMS. This is built for an adult child helping a parent, not for a parent alone.
- A willingness to tell me exactly where it broke, including the parts that are embarrassing for me.

Five to ten people. Not public yet, deliberately - a tool that touches a pensioner's bank account should meet a handful of careful users before it meets everyone.

### Want in?

Message me on LinkedIn and tell me which bank you would point it at. That is the single most useful thing you can put in the first message, because bank coverage is the open question.

[Message me on LinkedIn ↗](https://www.linkedin.com/in/galtidhar/) · [The audit this came from ←](/blog/money-audit/) · [Where it started ←](/blog/subscription-audit/) · [All field notes](/)
