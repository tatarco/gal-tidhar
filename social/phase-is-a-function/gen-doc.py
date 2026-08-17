#!/usr/bin/env python3
"""Build the ZaZet choices doc body for the "a phase is a function" post (series 1/6)."""
import base64, html, pathlib

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/phase-is-a-function.txt"

DESIGNS = [
    ("1", "the claim", "Bold-claim shape - the format he picked five times running. The whole idea in one sentence, with 'a function' in yellow."),
    ("2", "the signature card", "The actual phase block as an artifact. Concrete, copyable, stops a developer's scroll in under a second."),
    ("3", "the exchange", "Same work, two contracts: scope creep on one side, done-and-paid on the other. Teaches the whole point in one look."),
    ("4", "the mapping", "Five rows of code-term = deal-term. This is the series thesis rendered literally."),
    ("5", "the four jobs", "PM, QA, spec, payroll - the four people who held this for you as an employee. The emotional hook, not the mechanism."),
    ("6", "the payoff quote", "A phase boundary is not a Gantt line, it is where the risk changes hands."),
]

post = POST.read_text(encoding="utf-8").strip()
chars = len(post)

SKILL_URL = "https://github.com/tatarco/agent-skills/tree/main/skills/typed-phase"

comment = f"""התבנית המלאה, ובנוסף סקיל שמקבל אפיון או שרשור הודעות מלקוח ומפרק אותו לשלבים מוקלדים:
{SKILL_URL}

התקנה: npx skills add tatarco/agent-skills

השדות: נכנס / יוצא / תשלום / גמור כש / מי מאשר / לא כלול.
מה שהוא לא עושה - הוא לא מתמחר. זה פוסט אחר."""


def img(num, lang):
    p = HERE / f"hero-{num}-{lang}.png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{num}-{lang.upper()}</b></p>'
            f'<img src="data:image/png;base64,{b64}" alt="hero {num} {lang}">')


opts = ""
for num, name, why in DESIGNS:
    for lang in ("en", "he"):
        code = f"{num}-{lang.upper()}"
        rec = ' <span class="rec">RECOMMENDED</span>' if code == "1-HE" else ""
        alt = ' <span class="rec">RUNNER-UP</span>' if code == "2-HE" else ""
        opts += (f'<div class="opt" data-value="{code}">'
                 f'<div class="opt-head"><span class="dot"></span>'
                 f'<b>{code}</b> &middot; {html.escape(name)}{rec}{alt}</div>'
                 f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; freelance series, post 1 of 6</p>
  <h1>A phase is a function. Post, heroes and three open calls.</h1>
  <p class="lede">Post 1 of a six-part series on the business skills a salaried developer
  suddenly has to own. Pick a hero, answer the three questions at the bottom, and I will build
  the companion page. Your picks save in this page.</p>
</div>

<section class="step">
  <h2>The series</h2>
  <p class="sub">The through-line: you do not learn these skills the human way, you encode them.
  Every post is the same move on a different gap - find it, ingest the people who are good at it,
  turn it into a pipeline with memory. One post per day.</p>
  <div class="tbl-wrap"><table>
    <tr><th>#</th><th>Post</th><th>What it teaches</th></tr>
    <tr><td class="num">1</td><td><b>A phase is a function</b></td>
      <td>Scope in/out, definition of done, acceptance test, payment milestone. The four jobs an employer used to do for you.</td></tr>
    <tr><td class="num">2</td><td>Putting a number on it</td>
      <td>Floor / value / alternative. The day you stop dividing by hours.</td></tr>
    <tr><td class="num">3</td><td>The board</td>
      <td>Nine advisors who disagree with each other, and why the disagreement is the output.</td></tr>
    <tr><td class="num">4</td><td>Ingestion</td>
      <td>How a body of work becomes an advisor that actually pushes back instead of agreeing.</td></tr>
    <tr><td class="num">5</td><td>Distribution</td>
      <td>This post was written by the system that writes my posts. Hero generation and the draft-to-final feedback loop.</td></tr>
    <tr><td class="num">6</td><td>The state file</td>
      <td>An employee's skill resets every job. A freelancer's has to compound.</td></tr>
  </table></div>
  <div class="note-box">Post 1 ends on a one-line tease for post 2, so day-one readers come back
  on day two. Every post after this one stands alone for a cold reader.</div>
</section>

<section class="step">
  <h2>The post</h2>
  <p class="sub">{chars:,} characters, well under LinkedIn's 3,000 cap. Hebrew, plain hyphens,
  link in the first comment.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
</section>

<section class="step">
  <h2>The skill - shipped</h2>
  <p class="sub">The post promises a template in the first comment, so there is now a real one.
  <code>typed-phase</code> is live and public in your existing skills repo.</p>
  <div class="note-box ok"><b>Live:</b> <code>{SKILL_URL}</code><br>
  Installs with <code>npx skills add tatarco/agent-skills</code>.</div>
  <p>It takes a spec, a client thread or a rough verbal scope and slices it into phases typed with
  your six fields, in your order: <code>in / out / payment / done when / signed off by /
  not included</code>. Every rule in it came out of your post:</p>
  <ul>
    <li>The five mappings exactly as you wrote them, including <b>PR</b> as the payment milestone
      and the test being approved <b>by the client</b>, not "by both sides".</li>
    <li><b>The auto-approval clause is its own field, not a footnote.</b> A named approver, a
      deadline, and what happens when the deadline passes. This was the best thing in your
      rewrite - the usual way a phase stalls is silence, not rejection, and almost nobody writes
      the default.</li>
    <li><b>The MVP-slicing paragraph became four rules:</b> each phase usable on its own, smallest
      possible acceptance surface, close one before opening the next, stay visible so you never
      disappear for a year.</li>
    <li><b>It refuses to invent a field.</b> Anything the input cannot fill comes back as
      <code>??? - who is the named approver, and by when?</code> rather than a plausible guess.
      An unresolved list is the deliverable, not a failure.</li>
    <li><b>It will not price anything.</b> No rates, no anchors, no floors - none of your pricing
      logic left the private skills. That is post 2, and keeping it out is what makes this one
      safe to ship.</li>
  </ul>
  <p>Blank template in English and Hebrew is in <code>TEMPLATE.md</code> next to it.</p>
  <div class="copybar"><button class="copybtn" data-copy="comment-text">Copy first comment</button></div>
  <pre id="comment-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(comment)}</pre>
</section>

<section class="step">
  <h2>Hero image - pick one</h2>
  <p class="sub">Six designs, each in English and Hebrew. Click the one you want. The full local
  path is printed above every image so you can paste it straight into LinkedIn's file picker.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>Three calls I did not want to make for you</h2>

  <p class="q">1. How does ZaZet get the traffic?</p>
  <p class="sub">This is the only one still genuinely open, and shipping the skill changed its
  shape. The first comment now has a real payload - a GitHub repo - so ZaZet is no longer
  competing to be the link, it needs a role. You wanted the series feeding zazet-solutions.hr, and
  the docs portal is gated so cold LinkedIn traffic cannot land there.</p>
  <div id="linktarget" data-persist-choice class="opts small">
    <div class="opt" data-value="zazet-article"><div class="opt-head"><span class="dot"></span>
      <b>Public article on zazet-solutions.hr, linked first, repo second</b>
      <span class="rec">RECOMMENDED</span></div>
      <p class="why">The article is the readable version of the post with the full template in it;
      the repo is for people who want to install it. ZaZet gets the landing, GitHub gets the
      committed readers, and the repo README links back. Six posts amortise the one build.</p></div>
    <div class="opt" data-value="repo-only"><div class="opt-head"><span class="dot"></span>
      <b>Repo only, ZaZet linked from the README</b></div>
      <p class="why">Zero build. ZaZet gets a trickle of referral traffic instead of the landing,
      which is not really what you asked for.</p></div>
    <div class="opt" data-value="gal-blog"><div class="opt-head"><span class="dot"></span>
      <b>gal.tidhar.org.il blog with a ZaZet call-to-action</b></div>
      <p class="why">The blog machinery and deploy already exist, so it is the fastest. But it
      feeds your personal site, not the business one.</p></div>
  </div>

  <p class="q">2. [settled by your rewrite] The first year story</p>
  <p class="sub">You answered this yourself: two and a half months on a one-week fixed price, the
  three "מדהים!" messages, loving the client less as it went on, no leg to stand on. That is
  blunter than anything I would have written for you and it is the strongest part of the post.
  Left exactly as you wrote it.</p>
  <div style="display:none">
  <p class="q">2b. The first year story - how blunt?</p>
  <p class="sub">The post currently says that in my first freelance year I did not know when a
  phase ended, took a fixed-price project, worked double the hours I quoted, and did not feel
  entitled to complain because I had never written down what "done" meant. No client is
  identifiable. The ledger says the embarrassing version is the one that lands.</p>
  <div id="confession" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it as written</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is the only unfakeable part of the post. A model does not write "I did not
      feel entitled to complain" about itself.</p></div>
    <div class="opt" data-value="softer"><div class="opt-head"><span class="dot"></span>
      <b>Soften it</b></div>
      <p class="why">Keep the mechanism, drop the doubled hours and the not-allowed-to-complain
      line. Reads more composed, lands less.</p></div>
    <div class="opt" data-value="blunter"><div class="opt-head"><span class="dot"></span>
      <b>Go blunter</b></div>
      <p class="why">Name the money it cost. Higher risk, and the ledger says blunt is your register,
      not mine to choose.</p></div>
  </div>

  </div>

  <p class="q">3. [settled] The skill is shipped</p>
  <p class="sub">The private pricing skills stay private. <code>typed-phase</code> is the half with
  no confidential content in it, and it is now public - so the post's opening line is backed by
  something the reader can install, instead of being a tease.</p>
</section>

<section class="step">
  <h2>Two things you should know before this goes out</h2>
  <ul>
    <li><b>The reach risk is now smaller than it was.</b> The draft I gave you had no measured
      number and no installable artifact, which put it in the same shape as your 300-700 posts -
      describing your setup rather than handing the reader something. Your rewrite added a
      measurement ("a week turned into two and a half months") and the skill added the artifact.
      Both of the levers that carried cache-economics to 25,185 are now present in some form.</li>
    <li><b>The example is invented.</b> The customer-import phase, the 50k rows, the 30% and
      "Dana" are all constructed, as you asked. Nothing in the post comes from a real deal record.</li>
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
