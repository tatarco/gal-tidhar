#!/usr/bin/env python3
"""Build the ZaZet choices doc for the hebrew-esign post."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/hebrew-esign.txt"
WRAP_SRC = HERE.parent / "finance-audit-beta" / "out-choices.html"
WRAP_BODY = HERE.parent / "finance-audit-beta" / "choices-body.html"

DESIGNS = [
    ("8", "the claim + the real fix", "RECOMMENDED, and what you asked for: the bold claim on top, "
     "and underneath the actual before/after - four empty boxes, arrow, ישראל ישראלי in yellow. "
     "Claim buys the scroll-stop, the artifact proves it. Same move as the Claude-Code-Hebrew hero "
     "that printed the real bug next to the fix."),
    ("2", "the claim", "The bold-claim shape: I built a free e-signature that speaks "
     "Hebrew - and ran it on Tofes 101. The fork, the zero cost and 'the documents never leave my "
     "server' sit underneath. Your most-picked shape."),
    ("5", "the squares", "STRONG CONTENDER, and the Wiz principle: the image IS the thing the post "
     "is about. Four empty boxes, huge, in yellow - what my signed Hebrew PDF actually looked like. "
     "Nobody scrolls past four squares without reading why."),
    ("3", "the exchange", "Every e-sign tool: drag a box onto the PDF, put it roughly there, hope / "
     "Form mode: a labeled Hebrew form with the document live beside it. Your last two picks before "
     "the streak broke were this shape."),
    ("1", "the one big number", "173 fields on Israel's most hated form, and I placed zero of them "
     "by hand. The measured number as the scroll-stop, the code-measures/agent-looks loop in four "
     "lines underneath."),
    ("4", "what I tried", "DocuSign / FillFaster / DocuSeal / Documenso, each with the one line that "
     "stopped it. The procurement sequence as a grid - the shape you rewrite my drafts INTO. "
     "Note: this frame names FillFaster (see decision 02)."),
    ("6", "the loop", "The code measures / the agent looks / 0.14% off. The mapping method at a "
     "glance, and the most reusable idea in the post for a technical reader."),
]
EXTRA = ("7", "the product itself", "The real demo, rendered clean: the Hebrew form mode with the "
         "live PDF preview beside it. No claim, no copy - just the thing working in Hebrew. This is "
         "what you picked on finance-audit-app as the runner-up (hero-7, the product).")

post = POST.read_text(encoding="utf-8").strip()
chars = len(post)


def img(num, lang):
    p = HERE / f"hero-{num}-{lang}.png"
    if not p.exists():
        return ""
    prev = HERE / f".preview-{num}-{lang}.jpg"
    if not prev.exists():
        subprocess.run(["sips", "-Z", "1000", "-s", "format", "jpeg", "-s", "formatOptions", "72",
                        str(p), "--out", str(prev)], check=True, capture_output=True)
    b64 = base64.b64encode(prev.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{num}-{lang.upper()}</b></p>'
            f'<img src="data:image/jpeg;base64,{b64}" alt="hero {num} {lang}">')


def option(num, name, why, lang, tag=""):
    code = f"{num}-{lang.upper()}"
    im = img(num, lang)
    if not im:
        return ""
    t = f' <span class="rec">{tag}</span>' if tag else ""
    return (f'<div class="opt" data-value="{code}">'
            f'<div class="opt-head"><span class="dot"></span>'
            f'<b>{code}</b> &middot; {html.escape(name)}{t}</div>'
            f'<p class="why">{html.escape(why)}</p>{im}</div>')


TAGS = {"8-HE": "RECOMMENDED", "2-HE": "THE PLAIN CLAIM", "5-HE": "THE WIZ PRINCIPLE", "7-HE": "THE PRODUCT ITSELF"}
opts = ""
for num, name, why in DESIGNS:
    for lang in ("en", "he"):
        opts += option(num, name, why, lang, TAGS.get(f"{num}-{lang.upper()}", ""))
for lang in ("en", "he"):
    opts += option(EXTRA[0], EXTRA[1], EXTRA[2], lang, TAGS.get(f"7-{lang.upper()}", ""))

FIRST_COMMENT = """הדמו החי - כל אחד שלוחץ מקבל עותק 101 פרטי משלו, אף אחד לא חולק לינק עם אף אחד, ואני לא צד במסמך שלכם:
https://sign.zazet-solutions.hr/try101
(זה דמו, מוגבל בקצב - אל תכניסו נתונים אמיתיים)

רוצים להרים את זה אצלכם? כתבתי מדריך מלא - מה מותר לכם לעשות מבחינת הרישיון (פורק פומבי = חוקי, שינויים פרטיים = צריך רישיון מסחרי), כל הפיצ׳רים של המנוע, שתי ה-API-ים עם רשימת הראוטים המלאה, HTML ל-PDF, שדות העלאת קבצים, והדפלוי:
https://gal.tidhar.org.il/blog/hebrew-esign-selfhost/

הסיפור המלא של הבנייה - תיקון הגופן, מצב הטופס, ואיך מיפיתי 173 שדות בלי לגעת בקואורדינטה אחת:
https://gal.tidhar.org.il/blog/hebrew-esign/

הפורק עצמו, קוד פתוח, ענף he-locale:
https://github.com/tatarco/documenso"""

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; the Hebrew e-signature</p>
  <h1>A free Hebrew e-signature, proven on Tofes 101. Pick the hero, settle three calls.</h1>
  <p class="lede">Hebrew post for the Israeli side. Line 1 names DocuSign and טופס 101 - a paid
  incumbent plus the one form every Israeli employee resents, which is the strongest scroll-stop
  pair available here. The spine is one mechanism taken all the way down: how 173 fields got placed
  without a single hand-placed coordinate (code measures, the agent looks). The gift at the end is
  the live demo that mints the reader their own private 101 - your own cart rule, demo on their
  hand. Blog post is written and ready to push; links go in the first comment.</p>
</div>

<section class="step">
  <h2>The post</h2>
  <p class="sub">{chars:,} characters (cap 3,000). Hebrew, אמ!לק opener, DocuSign + טופס 101 in line 1,
  the procurement sequence drafted in as you always rewrite it, and it closes on the offer.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
</section>

<section class="step">
  <h2>01 &middot; Hero image - pick one</h2>
  <p class="sub">Eight designs, English and Hebrew. Click one; your pick saves in this page. The full
  local path above each image pastes straight into LinkedIn's file picker.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>02 &middot; FillFaster - name it or not?</h2>
  <p class="q">The post says "FillFaster זה פרויקט של לקוח שלי, לא שלי להשתמש בו". It is true, it is
  the honest reason you skipped it, and it is the kind of detail nobody invents. It also tells the
  feed that you built a product for a named client, and it puts a competitor's name in your post.</p>
  <div id="fillfaster" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep the name</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">FillFaster is public; saying you cannot use a client's product for your own
      business reads as integrity, not as a leak. It is also the beat that makes the sequence feel
      lived rather than researched.</p></div>
    <div class="opt" data-value="anonymize"><div class="opt-head"><span class="dot"></span>
      <b>"A product I built for a client"</b></div>
      <p class="why">Same beat, no name. Costs a little concreteness, removes any question about
      whether the client wanted to be identified.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut the line entirely</b></div>
      <p class="why">Three options in the sequence instead of four. Cleanest, flattest.</p></div>
  </div>
</section>

<section class="step">
  <h2>03 &middot; The demo link - first comment, or in the body?</h2>
  <p class="q">The rule here is first comment, because LinkedIn suppresses reach on posts with an
  external link in the body. But this post's whole payoff is a thing the reader can click and use,
  and a pointer to a comment adds a step between the promise and the payoff.</p>
  <div id="demo-link" data-persist-choice class="opts small">
    <div class="opt" data-value="first-comment"><div class="opt-head"><span class="dot"></span>
      <b>First comment (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Keeps the reach. The last line already promises exactly what is waiting there,
      so the loop is opened in the body and closed one tap away.</p></div>
    <div class="opt" data-value="in-body"><div class="opt-head"><span class="dot"></span>
      <b>Put the demo URL in the body</b></div>
      <p class="why">Zero friction to the payoff, at a known reach cost. Worth considering only if
      you care more about people actually trying it than about impressions on this one.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; The close - offer only, or add a question?</h2>
  <p class="q">Drafted as offer-only, per your callrec edit. A question is cheap here because the
  post has an obvious one.</p>
  <div id="closing" data-persist-choice class="opts small">
    <div class="opt" data-value="offer-only"><div class="opt-head"><span class="dot"></span>
      <b>Offer only (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Hand them the demo and stop.</p></div>
    <div class="opt" data-value="add-question"><div class="opt-head"><span class="dot"></span>
      <b>Add one short question</b></div>
      <p class="why">e.g. איזה טופס אתם עדיין מדפיסים, ממלאים ביד ומצלמים? One line, plain, and the
      answers would be a genuinely useful list for you.</p></div>
  </div>
</section>

<section class="step">
  <h2>The first comment - ready to paste</h2>
  <div class="copybar"><button class="copybtn" data-copy="first-comment">Copy first comment</button></div>
  <pre id="first-comment" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(FIRST_COMMENT)}</pre>
</section>

<section class="step">
  <h2>What I removed, and the honest notes</h2>
  <ul>
    <li><b>Privacy pass:</b> no people, no clients and no documents are named anywhere except
      FillFaster (decision 02). No envelope ids, tokens, host addresses or account details in the
      post, the heroes, the blog or the page metadata.</li>
    <li><b>The legal claim is in the blog, not the post.</b> Stated plainly there: this is an
      advanced electronic signature with an audit trail and a sealed PDF, <b>not</b> a certified
      signature under Israel's Electronic Signature Law, and no legal equivalence is claimed. It is
      out of the post only for length - if you would rather carry it, it is one sentence.</li>
    <li><b>The file-upload feature is not mentioned at all.</b> It is still in development; the
      handoff said mention it only as "in progress", and in a post whose credibility rests on
      everything else being real and clickable, an in-progress feature is a liability.</li>
    <li><b>Cut from the post, kept in the blog:</b> the AGPL / public-fork reasoning, the
      bind-mounted font paths, the Hetzner + Cloudflare tunnel + GitHub Actions detail, the full
      field breakdown (90 text / 79 checkboxes / dropdown / email / date / signature), and the
      "what I would not do again" list.</li>
    <li><b>CONFIRM THIS ONE BEFORE POSTING - the procurement sequence.</b> DocuSign costs per
      envelope &rarr; FillFaster is a client's &rarr; DocuSeal's API is behind the paid tier &rarr;
      Documenso, and then the squares. A verification pass flagged that this order and these reasons
      come from my notes on you, <b>not</b> from the build handoff - nothing else in the post is
      unsourced, and this is. It also appears in the blog, the site card and hero 4-* as a grid, so
      a correction has to travel to all four. If the order or a reason is wrong, tell me and I will
      fix everywhere.</li>
    <li><b>Also verified this run:</b> the fork is public and AGPL with branch <code>he-locale</code>
      live (last commit 26 Aug), base tag v2.17.0 exists, and the branch is <b>24 commits</b> ahead
      of main - the handoff said ~18, so the blog now says 24. The demo URL returns 200 on a real
      request (it answers 501 to a HEAD probe, which is a Next.js route-handler quirk, not a
      fault).</li>
    <li><b>Cut on verification:</b> three "what I would not do again" items in the blog were my
      inference rather than anything you told me - the debugging order, "the first twenty fields",
      and the build-order claim about form mode. Replaced with two lessons that follow from facts in
      the handoff. Nothing invented survives in the blog.</li>
    <li><b>Before posting:</b> the demo is rate-limited at 20 mints/hour. A post that works exhausts
      that in a minute. Worth raising the limit first.</li>
    <li><b>Two blog posts now, both written and unpushed.</b> The build story
      (<code>/blog/hebrew-esign/</code>) and a full self-host manual
      (<code>/blog/hebrew-esign-selfhost/</code>) - the licence answer, every feature on the branch,
      the v1 route list and the v2 surface, the Playwright HTML-to-PDF path, the recipient upload
      slots, and the two things you must change in the stock compose file. Both are in the first
      comment.</li>
    <li><b>The licence answer, verified against Documenso's own docs:</b> AGPL-3.0, one licence at
      the repo root, no separately-licensed enterprise directory. Their policy table says a public
      AGPL fork is Community Edition and fine - <b>private</b> modifications are what the Enterprise
      licence is for. Exactly one thing is gated by a licence key in code: the CSC signing
      transport. Your local signing transport is not gated. Also flagged in the manual: contributing
      upstream means signing their CLA, which grants Documenso Inc. a perpetual sublicensable
      licence over the contribution.</li>
    <li><b>Old note:</b> On your hero pick I set og.png to its EN twin, commit
      and push - the first-comment link goes live then.</li>
  </ul>
</section>

<style>
.copybar{{display:flex;justify-content:flex-end;margin:0 0 8px}}
.copybtn{{background:#012169;color:#fff;border:0;padding:8px 18px;font:inherit;font-size:14px;
  cursor:pointer;border-radius:2px}}
.opts{{display:flex;flex-direction:column;gap:22px;margin-top:18px}}
.opt{{border:1px solid rgba(10,22,40,.18);padding:16px;cursor:pointer;background:#fff}}
.opt.chosen{{border-color:#012169;border-width:2px;box-shadow:0 0 0 3px rgba(1,33,105,.10)}}
.opt-head{{display:flex;align-items:center;gap:10px;font-size:15px}}
.dot{{width:13px;height:13px;border-radius:50%;border:2px solid #012169;display:inline-block;flex:none}}
.opt.chosen .dot{{background:#012169;box-shadow:inset 0 0 0 2px #fff}}
.opt.chosen .opt-head::after{{content:"CHOSEN";margin-inline-start:auto;font-size:11px;
  letter-spacing:.12em;color:#012169;font-weight:700}}
.rec{{font-size:11px;letter-spacing:.1em;color:#012169;border:1px solid #012169;padding:2px 7px}}
.why{{color:#4a5e78;font-size:14px;margin:6px 0 12px}}
.pathline{{margin:0 0 6px}}
.pathline code{{font-size:12px;word-break:break-all}}
.opt img{{width:100%;display:block;border:1px solid rgba(10,22,40,.12)}}
.q{{font-weight:700;font-size:17px;margin-top:26px}}
</style>
<script src="/copy.js"></script>
<script src="/persist.js"></script>
"""

shell = WRAP_SRC.read_text(encoding="utf-8")
old_body = WRAP_BODY.read_text(encoding="utf-8")
i = shell.find(old_body.strip()[:80])
j = shell.find(old_body.strip()[-60:]) + 60
assert i > 0 and j > i, "wrapper markers not found"
doc = shell[:i] + BODY + shell[j:]
doc = doc.replace("<title>Finance audit beta - LinkedIn post",
                  "<title>Hebrew e-signature - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
