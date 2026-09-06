<!-- A free Hebrew e-signature, proven on Israel's worst form · Gal Tidhar — https://gal.tidhar.org.il/blog/hebrew-esign/ -->

# A free Hebrew e-signature, proven on Israel's worst form

_E-signature · Hebrew · RTL · Self-hosted_

**2026-08-27**  ·  ~8 min read  ·  by Gal Tidhar

I needed e-signatures for my business, went down the usual list, and ended up forking an open-source one because **none of them could seal a Hebrew character**. This is the build: real RTL, a Hebrew font inside the PDF sealing engine, a form-style signing mode that replaces clicking boxes onto a PDF, and **Tofes 101** - 173 fields - mapped without placing a single one by hand. Software cost: zero. There is a live demo at the end that mints you your own private copy.

## The boring beginning

ZaZet needs signed documents. Proposals, engagement letters, the occasional form. The options, in the order I actually tried them:

- **DocuSign.** Works, costs money per envelope, and the documents live on someone else's server.
- **FillFaster.** A client's project. Not mine to use for my own business.
- **DocuSeal.** Self-hostable and good, but the API I needed sits behind the paid tier.
- **Documenso.** Open source (AGPL), self-hostable, a real product. This was the one.

So I stood it up, uploaded a Hebrew document, signed it, and opened the sealed PDF:

`□□□□ □□□□`
 Empty boxes. The sealing renderer - the part that burns the signer's values permanently into the PDF - carried no Hebrew font at all. Everything upstream was fine: the value was correct in the database, correct in the browser, correct in the preview. It became squares at the last step, which is the step that produces the legal artifact.

And the font was only the visible symptom. The whole signer experience was left-to-right English. I was not going to send that to an Israeli client and ask them to figure it out.

## The fork

The work lives in [tatarco/documenso](https://github.com/tatarco/documenso), branch `he-locale`, forked from v2.17.0. AGPL, so the fork is public - which is the licence working exactly as intended rather than a favour I am doing anyone. Twenty-four commits ahead of `main`, in three groups.

### 1. Hebrew, properly

A full Hebrew catalog for the signer UI, a `?lang=he` override so a link can force the language regardless of browser settings, and `dir="rtl"` plumbed through the signing surfaces. Then the parts nobody thinks about until they are wrong: text alignment _inside the sealed PDF values_ has to be RTL-aware too, or a Hebrew name lands hanging off the left edge of its box.

### 2. The font, in the right place

The fix for the squares is unglamorous: bind-mount a Noto Hebrew font over the three paths the sealing renderer looks in, and make the renderer choose it for Hebrew text. That is it. It is the kind of bug that takes twenty minutes to fix and four hours to find, because every layer above it looked correct.

### 3. Form mode

This is the part I would keep even if Hebrew were never a problem. Every e-signature tool works the same way: you drag boxes onto a PDF, and the signer clicks the boxes. It is a metaphor built for a desktop mouse and a paper mental model, and on a phone it is miserable.

`?view=form` gives the signer a labeled vertical form instead - real field labels, in Hebrew - with the document as a **live preview beside it**: the value appears on the PDF as you type. Around it: a read-the-document-first step, collapsible sections so a two-page form is not a wall, repeating groups (an "add a child" row for the dependants table, with plus and minus), and required-field gating with Hebrew messages.

## 173 fields, and none of them placed by hand

Tofes 101 is the annual Israeli employee tax form. Every employee fills one, every year, and nobody enjoys it. As a test case it is close to worst-case: **173 fields** - 90 text, 79 checkboxes, one dropdown, one email, one date, one signature - packed into a dense two-page government layout.

Placing those by dragging boxes is a long, dull job and a permanent maintenance liability. Asking a model for coordinates is worse: language models are genuinely bad at "put this box at these exact coordinates", and they are bad in a way that looks fine until you render it.

So I inverted the roles:

- **Deterministic code measures.** A Python script reads the PDF's own text layer - the printed labels and the checkbox glyphs are real text objects with real coordinates - and anchors each field to the label it belongs to. Nothing is guessed; every position is derived from something already on the page.
- **The agent looks.** The script renders the page with every field box drawn on top, as an image. The agent reviews the image and says which boxes are wrong and in which direction. It never emits a coordinate; it emits a correction.
- **The loop closes into an artifact.** The script emits the API payload that creates the document with all 173 fields. Re-runnable, diffable, and re-derivable if the form ever changes.

Measured position error in the final seal: **0.14%**.

The general rule that came out of it, and the reason I think this matters beyond one form: **do not ask a model to measure, and do not ask code to judge.** Code is exact and blind; the model is approximate and sighted. Give each one the job it is actually good at and the loop converges fast.

## What it stops being

The non-obvious result of form mode plus a real field map is that the PDF stops being the document. The fields are named data with types; the PDF is an output format. Once that is true, the same form can render as a mobile form, be pre-filled from another system, and produce JSON on submission instead of a scan that a person retypes into payroll by hand.

The version of Tofes 101 most Israelis fill today is printed, marked with a mouse in a PDF reader or a pen, photographed, emailed as a crooked JPEG, and typed back in at the other end. Every step of that exists because the PDF was treated as the thing itself.

## Deployment, and what it costs

| Item | Value |
|---|---|
| Software cost | Zero. Documenso is AGPL; the fork is public. |
| Hosting | Docker on a small Hetzner VPS I already had, behind a Cloudflare tunnel |
| Builds | GitHub Actions builds the image |
| Per-envelope fee | None. No page limits, no seat count. |
| Where documents live | My server. They never leave it. |

**One honest limit, stated plainly:** this is an advanced electronic signature with an audit trail and a sealed PDF. It is not a certified/qualified signature issued under Israel's Electronic Signature Law, and I am not claiming legal equivalence for it. For ordinary business documents that is fine and it is what most people using DocuSign are getting too. For anything where a statute names a certified signature, it is not the tool.

## Going back upstream

The Hebrew and RTL work is being prepared as pull requests back to Documenso. There is an open issue asking for exactly this plumbing, and the same changes that make Hebrew work unlock Arabic and Persian - the RTL problem is one problem, not three. Keeping the fix in a private fork would have been the faster path and the worse one.

## Two things worth knowing before you copy this

- **When a value is correct everywhere except the final artifact, start at the artifact.** The Hebrew was right in the database, right in the API response, right in the browser and right in the preview. It only became squares in the sealing renderer - the one layer that produces the thing you actually keep.
- **Write the mapper before you place the second field.** Hand-placing is seductive because the first few are quick. 173 of them is a lost day and a result nobody can regenerate when the form changes.

### Try it - you get your own private copy

The demo mints a fresh, private Tofes 101 for every visitor: nobody shares a link, and I am not a party to your document. Fill it as a Hebrew form, sign it, download the sealed PDF with its audit certificate. It is rate-limited and it is a demo - **please do not enter real personal data.**

[Live demo: mint your own 101](https://sign.zazet-solutions.hr/try101) · [Run it yourself: features, APIs, deploy](/blog/hebrew-esign-selfhost/) · [The fork (branch he-locale)](https://github.com/tatarco/documenso) · [ZaZet Solutions](https://zazet-solutions.hr) · [More about me](/)
