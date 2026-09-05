#!/usr/bin/env python3
"""Build the ZaZet choices doc body for the pricing post (series 2/6)."""
import base64, html, pathlib

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/pricing-the-phase.txt"
SKILL_URL = "https://github.com/tatarco/agent-skills/tree/main/skills/typed-phase"

DESIGNS = [
    ("3", "estimate vs reality", "A week quoted, two and a half months spent, and none of the difference was hours. Carries the number from line 1 and is the shape you picked last time."),
    ("1", "the claim", "Hours are a bad denominator because typing is the only thing that got cheaper. The bold-claim shape."),
    ("4", "what it actually cost", "Two weeks waiting, four requests already done, one file seen too late. The receipts behind the number."),
    ("2", "the three anchors", "Floor, value, alternative - and the rule that the floor only holds a veto."),
    ("5", "the risk classes", "fixed / metered / gated / not-a-build. What the skill now emits."),
    ("6", "the payoff quote", "A fixed price is a price on certainty, and you are the one selling it."),
]

post = POST.read_text(encoding="utf-8").strip()
chars = len(post)

comment = f"""הסקיל, עכשיו גם עם סיווג סיכון לכל שלב:
{SKILL_URL}

התקנה: npx skills add tatarco/agent-skills

לכל שלב הוא מוציא סיווג: fixed אם אפשר להתחייב, metered אם זה תלוי במערכת שלא ראית, gated אם מחכים לגורם שלישי, ו-not-a-build אם אי אפשר להגדיר אותו בכלל - ואז הוא מפצל אותו לשלב גילוי קצר ולשלב האמיתי שאחריו.

הוא עדיין לא מתמחר. זה נשאר אצלי."""


def img(num, lang):
    p = HERE / f"hero-{num}-{lang}.png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{num}-{lang.upper()}</b></p>'
            f'<img src="data:image/png;base64,{b64}" alt="hero {num} {lang}">')


opts = ""
for num, name, why in DESIGNS:
    for lang in ("en", "he"):
        code = f"{num}-{lang.upper()}"
        rec = ' <span class="rec">RECOMMENDED</span>' if code == "3-HE" else ""
        opts += (f'<div class="opt" data-value="{code}">'
                 f'<div class="opt-head"><span class="dot"></span>'
                 f'<b>{code}</b> &middot; {html.escape(name)}{rec}</div>'
                 f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; freelance series, post 2</p>
  <h1>Pricing the phase. Post, heroes and two calls.</h1>
  <p class="lede">Ready to post in the morning. Hook, direction and hero recommendation are all
  decided - you only need to confirm or overrule. Your picks save in this page.</p>
</div>

<section class="step">
  <h2>First: how post 1 actually did</h2>
  <p class="sub">Read at five days, which is close enough to your one-week rule to be real.</p>
  <div class="tbl-wrap"><table>
    <tr><th>Metric</th><th class="num">Post 1</th><th>For comparison</th></tr>
    <tr><td>Impressions</td><td class="num">~900</td><td>cache-economics did 25,185; your typical text posts run 150-1,400</td></tr>
    <tr><td>Reactions</td><td class="num">19</td><td>up from 17 at 15h</td></tr>
    <tr><td>Comments</td><td class="num">2</td><td>plus your own first comment</td></tr>
  </table></div>
  <div class="note-box err"><b>Straight answer:</b> it landed in the bottom half of your range.
  Not a flop, but nowhere near the posts that carried you. The 108,654 figure in the LinkedIn
  sidebar is your 7-day profile total across all posts, not this one - do not read it as this
  post's reach.</div>
  <p>Two things I would not blame it on. It was not the writing, which was the strongest draft
  you have shipped through this skill. And it was not the artifact, which is the part that made
  the comments good.</p>
  <p>What I would look at instead:</p>
  <ul>
    <li><b>The subject is narrower than it looks.</b> "How to structure a fixed-price phase" is
      useful to freelancers. Your outliers were useful to anyone with a Claude account. That is a
      much bigger room.</li>
    <li><b>"1 of 6" may be working against you.</b> A numbered series tells a cold reader they
      have already missed something. Every one of your outliers stood completely alone.</li>
  </ul>
</section>

<section class="step">
  <h2>The two comments, and what they bought</h2>
  <p class="sub">Both are still the only two. Nothing new arrived since day one.</p>
  <p><b>Omri Pitaru</b> (AI Enablement at Overwolf) went straight at the field you added and I had
  not thought of:</p>
  <pre class="term" style="direction:rtl;text-align:right;white-space:pre-wrap">מה שהורג פרויקט במחיר קבוע זה בדרך כלל לא סקופ קריפ, זה אישור שלא מגיע. אתה מסיים, שולח, ומחכה שבועיים לאדם אחד שנסע לחופש.</pre>
  <p>He also pushed the metaphor further than the post did: an acceptance criterion is a test whose
  job is <b>social, not technical</b> - it moves "is this good enough" out of taste and into
  something checkable. And he closed with <b>מחכה לפוסט על המספר</b>.</p>
  <p><b>Yehonatan Alfasi</b> came at it from the opposite side: scope growing is good, it is more
  work coming in. The failure is only that it went unpriced.</p>
  <div class="note-box">Both comments are standing in this post's territory. Neither was
  "this happened to me too" - the mechanism landed, not the confession. That is why post 2 goes
  straight at the number with almost no setup.</div>
</section>

<section class="step">
  <h2>The decision I made, and why</h2>
  <p><b>Hook:</b> the number, not the comment. Line 1 is now
  <i>"תמחרתי פרויקט בשבוע עבודה. הוא לקח חודשיים וחצי. וההפרש בין השניים לא היה שעות."</i>
  Your best-performing post without a famous name in it won on a checkable number plus a payoff
  that corrected your own claim, and this is the same shape. Omri's line still opens the middle of
  the post, where it does the pivot work, but it is not carrying the scroll-stop.</p>
  <p><b>Direction:</b> exactly what you promised - putting a number on a <i>phase</i>, not on a
  project - through three anchors, and then the non-obvious part: phases are allowed different
  commercial shapes on purpose, because a discovery gate is sold against a downside rather than
  against effort.</p>
  <p><b>The close answers Omri.</b> The <code>מי מאשר</code> field with a deadline and a default
  turns out to be a pricing mechanism, not a courtesy. A fixed price is a price on certainty, so
  if nothing closes the phase when the client goes quiet, you sold certainty you do not control.
  That lands his comment back into the post that follows it, which is the best possible use of it.</p>
  <p><b>It reads standalone.</b> A cold reader who never saw post 1 loses nothing. I dropped the
  "2 of 6" line and the next-day tease from the draft for that reason - see the question below.</p>
</section>

<section class="step">
  <h2>The post</h2>
  <p class="sub">{chars:,} characters. Hebrew, plain hyphens, link in the first comment.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
  <div class="copybar"><button class="copybtn" data-copy="comment-text">Copy first comment</button></div>
  <pre id="comment-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(comment)}</pre>
</section>

<section class="step">
  <h2>The skill grew, and that is the payload</h2>
  <div class="note-box ok"><b>Live:</b> <code>{SKILL_URL}</code></div>
  <p><code>typed-phase</code> now emits a risk class per phase - <code>fixed</code>,
  <code>metered</code>, <code>gated</code>, <code>best-effort</code>, <code>not-a-build</code> -
  because the class, not your confidence, decides what you can commit to. When a phase is
  <code>not-a-build</code> it splits it into a short discovery gate whose deliverable is the
  missing information, plus the real phase behind it.</p>
  <p>It still emits no prices. Your anchors, rates and floors never left the private skills - the
  post teaches the three anchors as craft, which they are, without a single number of yours in it.</p>
  <p>Growing the same skill rather than shipping a second one is deliberate: it rewards everyone
  who installed it on day one and it makes the series read as a toolkit rather than six essays.</p>
</section>

<section class="step">
  <h2>Two calls</h2>

  <p class="q">1. Keep the series framing, or let each post stand alone?</p>
  <p class="sub">The draft currently has no "2 of 6" and no next-day tease. Post 1 promised
  "מחר" and then five days passed with four other posts in between, so the promise is already
  broken - the question is whether to repair it or drop it.</p>
  <div id="series" data-persist-choice class="opts small">
    <div class="opt" data-value="standalone"><div class="opt-head"><span class="dot"></span>
      <b>Drop the numbering, keep writing them</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Every outlier you have ever had stood alone. Numbering tells a cold reader
      they are late, and it puts you on a schedule you have already missed once. The through-line
      survives without the counter.</p></div>
    <div class="opt" data-value="renumber"><div class="opt-head"><span class="dot"></span>
      <b>Keep "2 of 6" and re-commit to the cadence</b></div>
      <p class="why">Series create return readers, and Omri explicitly said he is waiting for this
      one. Costs you a daily obligation.</p></div>
    <div class="opt" data-value="acknowledge"><div class="opt-head"><span class="dot"></span>
      <b>Keep it, but open by naming the gap</b></div>
      <p class="why">"אמרתי מחר, עברו חמישה ימים" as a one-liner. Honest, very much your register,
      but it spends the first line on housekeeping instead of the number.</p></div>
  </div>

  <p class="q">2. Hero</p>
  <p class="sub">Six designs, EN and HE. Recommendation is <b>3-HE</b> - it is the contrast shape
  you chose last time and it puts the week-versus-ten-weeks number in the image, which is the
  lever the post is built on. Note the cells are inverted from post 1 on purpose: the estimate is
  the calm one and the reality is red.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
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
