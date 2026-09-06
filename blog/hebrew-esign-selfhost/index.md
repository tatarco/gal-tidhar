<!-- Run the Hebrew e-signature yourself · Gal Tidhar — https://gal.tidhar.org.il/blog/hebrew-esign-selfhost/ -->

# Run the Hebrew e-signature yourself

_Documenso · AGPL · Hebrew · RTL · API_

**2026-08-27**  ·  ~10 min read  ·  by Gal Tidhar

The companion to [the build story](/blog/hebrew-esign/). This one is the manual: **the licence question answered first**, then every feature that is actually on the branch, the two API surfaces, the HTML-to-PDF path, the recipient upload slots, and how to deploy it. The fork is [github.com/tatarco/documenso](https://github.com/tatarco/documenso), branch `he-locale`.

## First: is this legal to run?

Short answer: **yes, and the reason matters.** Documenso is licensed AGPL-3.0 - one licence file at the repository root, no separately-licensed enterprise directory. My fork is public and stays AGPL, which is exactly what the licence asks of anyone who modifies it and runs it as a network service.

Documenso publishes its own guidance on when the Community Edition is enough, and it is worth reading before you start, because the trap is not obvious:

| What you are doing | Licence you need |
|---|---|
| Running it internally, unmodified | Community (AGPL) |
| Running it with modifications you publish under AGPL | Community (AGPL) |
| Running it with **private** modifications | Enterprise |
| A SaaS product built on modified Documenso code | Enterprise |
| A SaaS product using the Documenso API only | Community (AGPL) |
| White-label with proprietary changes | Enterprise |

So: **fork publicly and you are fine. Fork privately and change things, and you are the case the Enterprise licence exists for.** The AGPL's network clause is the whole point - if your users interact with your modified version over a network, they are entitled to your source. Keeping my fork public was not generosity, it was the licence working as designed.

One runtime consequence worth knowing: exactly one feature is hard-gated behind a licence key in the code - the **CSC (Cloud Signature Consortium) signing transport**. Everything below runs without a key. The local signing transport, which is what most self-hosters use, is not gated.

## What the engine does

Everything in this section is on the `he-locale` branch today, not planned.

### Hebrew and RTL

- Hebrew catalog for the signer-facing UI (the admin UI still falls back to English).
- `?lang=he` pins the signer language per link, regardless of browser settings.
- `dir="rtl"` on the document root when the locale is Hebrew, with same-row fields sorting right-to-left.
- RTL-aware alignment for values inserted into the PDF, so a Hebrew value does not hang off the wrong edge of its box.
- A Hebrew font inside the sealing renderer, so typed Hebrew seals as glyphs rather than empty squares. This is the fix that made the whole thing possible.

### Form mode - `?view=form`

- **Read-first wizard:** step one is the full document, read-only, with no interactive boxes on the PDF at all. Step two is the form.
- **Side-by-side on desktop** - form on the document's start side (right in RTL), read-only preview beside it, independent column scrolling. On mobile the form stands alone with a view-document toggle.
- **Live field placeholders in the preview** - what you type appears on the page as you type it.
- **Grouped sections and repeating groups** - add and remove instances (the dependants table), with the remove button clearing that instance's fields.
- Checkbox fallback control when a field carries no options, compact checkbox overlay fit, and inline field-commit errors instead of silent failures.
- Next-field navigation that targets the form and reveals collapsed groups.

### Documents out

- The recipient can download the **filled but still pending** PDF, not only the sealed one.
- The completion page shows an inline preview of the sealed document on desktop, with live status on the Download button.
- The sealed PDF ships with its audit certificate.

### Recipient upload slots

The newest feature on the branch, and the one I would look at first if you are building anything beyond signatures: a recipient can be given **upload slots** - places to attach supporting documents as part of signing. It is a full vertical slice, not a UI stub:

- Schema and database migration for the slots.
- Server-only CRUD, plus tRPC routes for create / find / delete.
- Slots accepted per recipient at envelope-create time.
- Signer-side slots inside form mode, with completion gating so a required attachment blocks completion.
- **The uploads are packaged into the sealed PDF**, and the attachment is recorded in the audit trail.

Honest note on maturity: this landed most recently, the last commit on it is a typecheck fix, and it has had far less real-world use than form mode. Treat it as working-but-young.

### HTML to PDF

The engine renders PDFs from HTML through Playwright-driven Chromium - `packages/lib/server-only/htmltopdf/` - and uses it for the signing certificate and the audit-log PDF. If you want those, you need the Chromium image variant: `docker/Dockerfile.chromium`, which layers `@playwright/browser-chromium` on top of the base image. The plain image is smaller and skips them.

## The APIs

Two surfaces, both live on the same instance.

### v1 - stable REST

A ts-rest contract mounted under `/api/v1`. The full route list:

`GET /api/v1/documents
POST /api/v1/documents
GET /api/v1/documents/:id
DELETE /api/v1/documents/:id
GET /api/v1/documents/:id/download
POST /api/v1/documents/:id/fields
PATCH /api/v1/documents/:id/fields/:fieldId
POST /api/v1/documents/:id/recipients
PATCH /api/v1/documents/:id/recipients/:recipientId
POST /api/v1/documents/:id/send
POST /api/v1/documents/:id/resend
GET /api/v1/templates
GET /api/v1/templates/:id
POST /api/v1/templates/:templateId/create-document
POST /api/v1/templates/:templateId/generate-document

GET /api/v1/openapi.json ← the machine-readable spec
GET /api/v1/me ← test your credentials
`
 Method-by-route varies; take `/api/v1/openapi.json` from your own instance as the source of truth rather than this list. There are also Zapier endpoints (`/api/v1/zapier/list-documents`, `subscribe`, `unsubscribe`) if you want the no-code path.

**This is the API that made the 173-field mapping possible.** The field-creation endpoint takes coordinates, so a script can emit an entire form's field map in one run - which is the whole trick behind [the Tofes 101 build](/blog/hebrew-esign/).

### v2 - the newer surface

A tRPC-derived OpenAPI surface served at `/api/v2` (and `/api/v2-beta`), with CORS and its own rate-limit middleware, and its spec at `/api/v2/openapi.json`. It covers considerably more of the product than v1 - envelopes, documents, fields, recipients, templates, folders, teams, organisations, webhooks, API tokens, embedding. If you are starting fresh, start here; v1 is the one with the stable contract and the wider blast radius of existing integrations.

**One gap to know about:** the upload-slot routes are tRPC-only right now. They are reachable from the app, not from the v1 REST contract. If you need slots over plain HTTP, that is the piece to add.

## Deploying it

The repository ships a production Docker Compose at `docker/production/compose.yml`: Postgres 15 with a healthcheck, plus the app. Two things you must change from the stock file.

**1. Point the image at your own build.** The stock compose pulls `documenso/documenso:latest` - upstream, without any of this. The branch's CI builds a GHCR image from the branch and also exports the image as a tar artifact, specifically so you can deploy without a registry. Use one of those, or build `docker/Dockerfile` yourself.

**2. Mount the Hebrew font.** The sealing renderer resolves `noto-sans.ttf` from more than one location depending on the code path - `packages/assets/fonts/` and `apps/remix/public/fonts/` among them. Bind-mount a Noto font with Hebrew coverage over each of them. Miss one and you get squares from whichever path you missed, which is a genuinely confusing bug to hit in production.

Then the environment. Copy `.env.example` and fill in at minimum:

`NEXTAUTH_SECRET
NEXT_PRIVATE_ENCRYPTION_KEY
NEXT_PRIVATE_ENCRYPTION_SECONDARY_KEY
NEXT_PUBLIC_WEBAPP_URL # your real external URL
NEXT_PRIVATE_DATABASE_URL
NEXT_PRIVATE_SMTP_TRANSPORT # + host/port/user/pass
NEXT_PRIVATE_SMTP_FROM_NAME
NEXT_PRIVATE_SMTP_FROM_ADDRESS
NEXT_PRIVATE_SIGNING_TRANSPORT=local
NEXT_PRIVATE_SIGNING_LOCAL_FILE_PATH # or _CONTENTS
NEXT_PRIVATE_SIGNING_PASSPHRASE
`
 The signing transport is the one people get stuck on. `local` means the instance seals with a certificate you supply as a P12 file (path or base64 contents). It costs nothing and it is not licence-gated. Upload transport defaults to `database`, which is the simplest thing that works; S3-compatible storage is configured through the `NEXT_PRIVATE_UPLOAD_*` variables if you outgrow it.

Mine runs as Docker on a small VPS behind a Cloudflare tunnel, with GitHub Actions building the image. Nothing about that is required - it is one boring shape that works.

## If you want to contribute back

The Hebrew and RTL work is being prepared as pull requests to upstream Documenso, where an open issue asks for exactly this plumbing - and the same changes unlock Arabic and Persian, because RTL is one problem, not three.

Worth knowing before you open a PR there: Documenso has a **Contributor License Agreement**. Contributing grants Documenso Inc. a perpetual, worldwide, non-exclusive, royalty-free, sublicensable licence over your contribution. That is common for open-core companies and it is not a reason not to contribute, but it is a thing you agree to, so read `CLA.md` rather than clicking past it.

### Start here

Try the live demo first - it mints you your own private Tofes 101, nobody shares a link, and I am not a party to your document. It is rate-limited and it is a demo, so please do not enter real personal data. Then clone the branch and read `docker/production/compose.yml`.

[Live demo: mint your own 101](https://sign.zazet-solutions.hr/try101) · [The fork (branch he-locale)](https://github.com/tatarco/documenso) · [The build story](/blog/hebrew-esign/) · [ZaZet Solutions](https://zazet-solutions.hr)
