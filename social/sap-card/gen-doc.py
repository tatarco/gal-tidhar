#!/usr/bin/env python3
"""Build the ZaZet choices doc body for the SAP-business-card origin post."""
import base64
import html
import pathlib
import subprocess

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/sap-card.txt"

DESIGNS = [
    ("1", "the claim", "Bold-claim shape - the one he picked five times running. Whole story in a "
     "sentence, with the card as a small artifact underneath."),
    ("2", "the card, full bleed", "The photo IS the hook. A worn 2013 SAP card in a hand, one line "
     "of caption. This is the closest thing here to the Wiz-logo post that did 133k."),
    ("3", "the exchange", "What he told me / what I actually did, with the punchline underneath: "
     "I took exactly half the advice."),
    ("4", "the quote", "Husain's sentence at full size, attributed, with the card under it."),
    ("5", "the timeline", "2013 cart, 2013 card, then the studying, a decade of code, and 2026 - "
     "someone asks you to sell again. The thirteen-year arc in one look."),
    ("6", "the two rules", "What a mall cart teaches about selling software: open with a "
     "question, demo on their hand. The useful half, no story."),
]

BLOG = "https://gal.tidhar.org.il/blog/sap-card/"

post = POST.read_text(encoding="utf-8").strip()
chars = len(post)

comment = f"""הסיפור המלא, כולל כלל שלישי מהעגלה שלא נכנס לפוסט ומה שהייתי אומר לעצמי ב-2013:
{BLOG}"""


def img(num, lang):
    """Embed a downscaled JPEG preview; the doc has a 5 MB ceiling, the PNGs do not fit."""
    p = HERE / f"hero-{num}-{lang}.png"
    prev = HERE / f".preview-{num}-{lang}.jpg"
    if not prev.exists():
        subprocess.run(["sips", "-Z", "1000", "-s", "format", "jpeg", "-s", "formatOptions", "72",
                        str(p), "--out", str(prev)], check=True, capture_output=True)
    b64 = base64.b64encode(prev.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{num}-{lang.upper()}</b></p>'
            f'<img src="data:image/jpeg;base64,{b64}" alt="hero {num} {lang}">')


opts = ""
for num, name, why in DESIGNS:
    for lang in ("en", "he"):
        code = f"{num}-{lang.upper()}"
        tag = ""
        if code == "2-HE":
            tag = ' <span class="rec">RECOMMENDED</span>'
        elif code == "1-HE":
            tag = ' <span class="rec">RUNNER-UP</span>'
        opts += (f'<div class="opt" data-value="{code}">'
                 f'<div class="opt-head"><span class="dot"></span>'
                 f'<b>{code}</b> &middot; {html.escape(name)}{tag}</div>'
                 f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; origin story</p>
  <h1>The SAP business card. Post, heroes, and three calls that are yours.</h1>
  <p class="lede">Pulled from your WhatsApp thread with the founder. The card photo is the hero, redacted.
  Pick an image, answer the three questions at the bottom, and I will finish the blog post and
  push it. Your picks save in this page.</p>
</div>

<section class="step">
  <h2>The post</h2>
  <p class="sub">{chars:,} characters, well under LinkedIn's 3,000 cap. Hebrew, plain hyphens,
  link in the first comment.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
  <div class="copybar"><button class="copybtn" data-copy="comment-text">Copy first comment</button></div>
  <pre id="comment-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(comment)}</pre>
</section>

<section class="step">
  <h2>Hero image - pick one</h2>
  <p class="sub">Six designs, each in English and Hebrew. Click the one you want. The full local
  path is printed above every image so you can paste it straight into LinkedIn's file picker.</p>
  <p class="sub"><b>The recommendation breaks the usual advice on purpose.</b> The ledger says the
  bold-claim shape wins, but your single biggest post ever (133k) was an image that WAS the thing
  it was about - the Wiz logo. Here the thing it is about is a physical object with an SAP logo on
  it, photographed years ago, worn at the edges. No graphic I can draw beats that.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>What I removed, and what I changed after verification</h2>
  <ul>
    <li><b>Husain's surname, mobile, fax and email are blurred on every image.</b> He handed you
      that card in a mall, not to LinkedIn in 2026. First name plus "manager at SAP" keeps the
      entire punchline. The company office address on the card is published and left readable.</li>
    <li><b>The year is now 2013, on your correction.</b> My first draft said 2012, inferred from
      the Brazil videos in the same thread - which are a different job. Everything downstream moved
      with it: the Dubai line is now "seven years before anyone signed anything", and the arc is
      thirteen years, not fourteen.</li>
    <li><b>"12 hours a day" is gone.</b> A verification pass caught that I had invented it - your
      message says full-time, not a number of hours. It now says full time, everywhere.</li>
    <li><b>Husain's quote is marked as a reconstruction.</b> The Hebrew now says
      "אמר לי משהו בסגנון" and the blog says outright that the wording is yours and the content is
      his. What you actually wrote in the thread was a paraphrase, and presenting a paraphrase inside
      quotation marks thirteen years later is the one thing in this post that could be called
      out.</li>
    <li><b>The founder and his company stay anonymous.</b> "מייסד של חברה שעדיין בסטלת׳" - no name,
      no product name, no URL to the site it built. It is in stealth and you said you would post
      about it anonymously.</li>
  </ul>
</section>

<section class="step">
  <h2>Three calls I did not want to make for you</h2>

  <p class="q">1. How much of the founder story goes in?</p>
  <p class="sub">Right now the post carries it in three beats: he is trying to recruit you for GTM,
  you caught yourself describing the cart mid-call, and then he pointed the harness at you and
  one-shot a whole site about you - headline "איך חוסיין מ-SAP הפך את גל טדהר למתכנת", surname
  misspelled. That last beat is the funniest thing in the post and it doubles as your own second
  rule: he demoed on your hand, not his.</p>
  <div id="founder" data-persist-choice class="opts small">
    <div class="opt" data-value="all-three"><div class="opt-head"><span class="dot"></span>
      <b>All three beats, company anonymous</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">As drafted. It gives the origin story a reason to exist today, and the
      one-shot site is the proof for the rule you just taught. He gets a flattering anonymous
      mention, which is what you told him you would do.</p></div>
    <div class="opt" data-value="recruit-only"><div class="opt-head"><span class="dot"></span>
      <b>Only the recruiting beat, drop the one-shot site</b></div>
      <p class="why">Keeps the "someone asked me to sell again" frame, loses the demo punchline.
      Choose this if you would rather not put any weight behind a product you have not used yet -
      even anonymously.</p></div>
    <div class="opt" data-value="none"><div class="opt-head"><span class="dot"></span>
      <b>Pure origin story, no founder at all</b></div>
      <p class="why">The version I drafted first. Cleaner, and it has no answer to "why are you
      telling me this today".</p></div>
  </div>

  <p class="q">2. The closing line to Husain</p>
  <p class="sub">The post currently ends: "חוסיין, אם אתה במקרה פה - איחרתי בעשור, אבל הגעתי."
  It is the funniest line in the draft and it is also the one that could read as a stunt.</p>
  <div id="closer" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It closes the loop the hook opened, and it invites exactly the comment
      thread you want ("did you ever find him?").</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it, end on the cart paragraph</b></div>
      <p class="why">Drier, more composed, and one fewer thing that can be read as bait.</p></div>
    <div class="opt" data-value="find-him"><div class="opt-head"><span class="dot"></span>
      <b>Keep it and actually try to find him</b></div>
      <p class="why">Ask the feed to help. Highest upside by a distance if it works, and it turns
      a story post into an ongoing one. Also the version most likely to be called a stunt, and it
      puts a real person on the spot without asking him first.</p></div>
  </div>

  <p class="q">3. Where does the first comment point?</p>
  <p class="sub">The companion post is written and staged at <code>{BLOG}</code>. It is on your
  personal site with a ZaZet call-to-action at the bottom, same as the rest of your field notes.
  You raised on the last post that you want the series feeding zazet-solutions.hr instead.</p>
  <div id="linktarget" data-persist-choice class="opts small">
    <div class="opt" data-value="gal-blog"><div class="opt-head"><span class="dot"></span>
      <b>gal.tidhar.org.il, as written</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">This one is a personal story, not a ZaZet capability piece. It belongs on the
      personal site, and the ZaZet link at the bottom does the handoff. Zero extra build.</p></div>
    <div class="opt" data-value="zazet"><div class="opt-head"><span class="dot"></span>
      <b>Move it to a public page on zazet-solutions.hr</b></div>
      <p class="why">Feeds the business site, but a founder origin story on a company site reads
      as an About page, and it needs the public blog build you have not done yet.</p></div>
    <div class="opt" data-value="none"><div class="opt-head"><span class="dot"></span>
      <b>No link at all</b></div>
      <p class="why">Pure story post, nothing to click. Cleanest read, and it wastes the traffic.</p></div>
  </div>
</section>

<section class="step">
  <h2>One thing you should know before this goes out</h2>
  <ul>
    <li><b>This post has no measured number and no installable artifact.</b> Your top posts either
      taught a mechanism with a checkable number (cache economics, 25,185) or carried a famous
      logo (Wiz, 133k). This one has SAP in line 1 and a real photograph, which buys the
      scroll-stop, and the two cart rules are the useful half - but it is a story, and the ledger
      cannot tell you a story post will travel. Worth posting because it is true and it is
      yours, not because the numbers predict it.</li>
    <li><b>The blog post is written and staged but not pushed.</b> It goes live the moment you
      pick a hero, so the first-comment link is never dead.</li>
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

(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote choices-body.html", len(BODY), "bytes")
