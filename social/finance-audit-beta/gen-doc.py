#!/usr/bin/env python3
"""Build the ZaZet choices doc body for the finance-audit beta post."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/finance-audit-beta.txt"

DESIGNS = [
    ("2", "the claim", "Bold-claim shape - his default pick, and here the claim IS the ask: "
     "if you have Claude Code and Gmail, you can audit your parents' money. Names a recognizable "
     "tool in the frame and states the beta call underneath."),
    ("1", "the one big number", "4 of 6. The measured-number shape that carried cache-economics to "
     "25k with no famous logo. Intriguing, but it sells the checklist rather than the beta."),
    ("3", "the exchange", "A website that collects bank data needs a licence / software on your own "
     "machine does not. The regulation-chose-the-architecture idea in two cells. He picked the "
     "exchange shape last time."),
    ("4", "the breakdown grid", "All six traps with their tells. The most useful frame for a "
     "cold reader and the one most likely to be screenshotted, at the cost of being dense."),
    ("5", "the payoff quote", "“Money arriving is not income.” The single most dangerous trap, "
     "at full size, with the 3x consequence underneath."),
    ("6", "the architecture", "Local bank / your mail / your agent, and nothing leaves the machine. "
     "Answers the trust objection visually, which is the objection that will fill the comments."),
]

post = POST.read_text(encoding="utf-8").strip()
chars = len(post)

FIRST_COMMENT = ("הפירוט המלא, שש המלכודות, ומה בדיוק עובד ומה לא:\n"
                 "https://gal.tidhar.org.il/blog/finance-audit-beta/\n\n"
                 "הספריות שהעבודה הקשה נשענת עליהן, שתיהן MIT וישראליות:\n"
                 "israeli-bank-scrapers - https://github.com/eshaham/israeli-bank-scrapers\n"
                 "Caspion - https://github.com/brafdlog/caspion\n\n"
                 "מי שרוצה להיכנס לביתא, תכתבו לי בפרטי ותגידו לאיזה בנק תכוונו את זה. "
                 "זאת השאלה הפתוחה היחידה שבאמת מעניינת אותי כרגע.")


def img(num, lang):
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
        elif code == "4-HE":
            tag = ' <span class="rec">RUNNER-UP</span>'
        opts += (f'<div class="opt" data-value="{code}">'
                 f'<div class="opt-head"><span class="dot"></span>'
                 f'<b>{code}</b> &middot; {html.escape(name)}{tag}</div>'
                 f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; beta recruitment</p>
  <h1>The finance audit, as software. Post, heroes, and three calls that are yours.</h1>
  <p class="lede">The follow-up the comments on the 16,000 post asked for: not another finding,
  a tool they can run themselves. Copy the post, pick a hero, and answer the three questions at
  the bottom. Your picks save in this page.</p>
</div>

<section class="step">
  <h2>The post</h2>
  <p class="sub">{chars:,} characters, under LinkedIn's 3,000 cap with about 80 to spare.
  Hebrew, plain hyphens, link in the first comment.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
</section>

<section class="step">
  <h2>The first comment</h2>
  <p class="sub">Goes up immediately after posting. Carries the blog link, the credit to both
  libraries with their repos, and the one question you want in every DM.</p>
  <div class="copybar"><button class="copybtn" data-copy="first-comment">Copy first comment</button></div>
  <pre id="first-comment" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(FIRST_COMMENT)}</pre>
</section>

<section class="step">
  <h2>Hero image - pick one</h2>
  <p class="sub">Six designs, each in English and Hebrew. Click the one you want. The full local
  path is printed above every image so you can paste it straight into LinkedIn's file picker.</p>
  <p class="sub"><b>Why 2-HE.</b> This post has a job other than being read - it has to make 5 to 10
  people write to you. The claim shape is the only one of the six that puts the offer in the frame
  itself, and it names Claude Code, which is the recognizable name your line 1 is buying. 4-HE is
  the runner-up because the traps grid is the most screenshot-able thing here, but it sells the
  idea rather than the ask.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>Three calls I did not want to make for you</h2>

  <p class="q">1. How do people get in - DM, or a public repo?</p>
  <p class="sub">The repo is local, MIT, and has no git remote. The post as drafted routes
  everyone through your DMs.</p>
  <div id="route" data-persist-choice class="opts small">
    <div class="opt" data-value="dm"><div class="opt-head"><span class="dot"></span>
      <b>DMs only, repo stays private</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">You asked for 5-10 people, not a launch. A DM gate gives you exactly that
      number, lets you refuse anyone who should not be pointing this at a parent's account, and
      means the first install problems arrive with a person attached to them. It also keeps the
      Leumi-only status from being discovered by a stranger at 2am.</p></div>
    <div class="opt" data-value="push-public"><div class="opt-head"><span class="dot"></span>
      <b>Push the repo public now, link it in the first comment</b></div>
      <p class="why">More reach, more stars, more credibility for the credit you are giving the
      two libraries. Also uncontrolled: 14 untested banks in public, and a README that has to
      carry every warning the DM conversation would have carried.</p></div>
    <div class="opt" data-value="waitlist"><div class="opt-head"><span class="dot"></span>
      <b>A form instead of DMs</b></div>
      <p class="why">Scales better and reads more like a product launch, which is the thing you
      said this is explicitly not. Only worth it if you expect far more than 10.</p></div>
  </div>

  <p class="q">2. The password paragraph - keep it this blunt?</p>
  <p class="sub">The draft says out loud that this teaches people to type a bank password into
  something that is not the bank, and calls it the exact pattern fraud departments fight, before
  answering it.</p>
  <div id="candour" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it, in full</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Every technical reader is going to think it within four seconds of reading
      the hook. Saying it first is the only version where you control the framing, and it is the
      paragraph most likely to earn a serious comment thread rather than a suspicious one.</p></div>
    <div class="opt" data-value="soften"><div class="opt-head"><span class="dot"></span>
      <b>Keep the four guarantees, drop the fraud-department line</b></div>
      <p class="why">Same information, less alarming. Loses the part that proves you are not
      selling anything.</p></div>
  </div>

  <p class="q">3. The "it feels invasive" paragraph</p>
  <p class="sub">The unpunctuated one about what it is like to sit and read your parents' account.
  I drafted it in deliberately, because the ledger says you add exactly this paragraph yourself
  when it is missing. It is my words, not yours - rewrite it in your own before posting.</p>
  <div id="raw" data-persist-choice class="opts small">
    <div class="opt" data-value="rewrite"><div class="opt-head"><span class="dot"></span>
      <b>You rewrite it in your own words</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is the only paragraph in the post that cannot be faked, and it is the
      one a model should not be writing for you.</p></div>
    <div class="opt" data-value="asis"><div class="opt-head"><span class="dot"></span>
      <b>Leave it as drafted</b></div>
      <p class="why">It is close enough to your register to survive. Slightly too composed.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it</b></div>
      <p class="why">Makes it a cleaner engineering post and a colder one. It also buys back
      about 300 characters if you want them elsewhere.</p></div>
  </div>
</section>

<section class="step">
  <h2>What I left out, and what you should check</h2>
  <ul>
    <li><b>No screenshots of the running app, on purpose.</b> Every frame would carry real
      balances and real merchant names, and the localhost URL carries a live session token that
      rotates each launch. If you want an app carousel later it has to be shot against synthetic
      data, not scrubbed after the fact.</li>
    <li><b>No bank other than Leumi is claimed anywhere</b> - not in the post, not in the hero,
      not in the blog post. The other 14 are described as wired and untested, which is what they
      are. This is the claim most likely to be tested by a commenter.</li>
    <li><b>No family member's finances appear.</b> The four audits are referenced by relationship
      only - my parents, my sister, my wife's family - with no amounts attached to any of them.
      The one number in the post, the 3x deficit error, is mine, not theirs.</li>
    <li><b>It is never called open banking.</b> It is a scraper with consent, and the post says so.</li>
    <li><b>Confirm before this goes out:</b> that you have rotated the Leumi password that was
      shared during testing. Nothing public should be written until that is done.</li>
  </ul>
</section>

<section class="step">
  <h2>One honest weakness</h2>
  <ul>
    <li><b>This post asks for something.</b> Every one of your outliers gave the reader something
      to use with no strings - a number to check on their own account, a habit, a skill to install.
      This one ends in a request, and requests travel worse than gifts. The counterweight is the
      traps checklist: six items, four of which pass an arithmetic review, useful whether or not
      anyone ever installs the tool. If the post underperforms, that is the reason, and the fix
      next time is to ship the checklist as a skill first and the beta ask second.</li>
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
