#!/usr/bin/env python3
"""Build the ZaZet choices doc for the agent-handoff post."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/agent-handoff.txt"
WRAP_SRC = HERE.parent / "finance-audit-beta" / "out-choices.html"
WRAP_BODY = HERE.parent / "finance-audit-beta" / "choices-body.html"

DESIGNS = [
    ("2", "the claim", "RECOMMENDED. The bold-claim shape, your winner on five picks: I gave my agent "
     "a real browser - when it hits a password, it hands the browser to my phone. The tagline "
     "(agent fills the cart, I press Pay) and the NanoClaw credit sit underneath."),
    ("3", "the exchange", "STRONG CONTENDER - your last two picks were this shape. Every browser "
     "agent until now: hits the login, gets stuck (or worse, you give it your password) / Handoff: "
     "sends its browser to my phone, I log in, it continues. The story IS a contrast, which is "
     "when you have picked the exchange before."),
    ("1", "the one big number", "925 seconds - the browser waited for me and the session survived. "
     "The measured number as the scroll-stop, mechanism in four lines underneath."),
    ("4", "the breakdown grid", "What gets handed to the human: password, 2FA, CAPTCHA, the Pay "
     "button - each with its one-liner. Most screenshot-able, densest."),
    ("5", "the price", "5 dollars a month, 10 browser-hours included - Cloudflare Browser Run named, "
     "with the four-way comparison (Browserbase 20, Steel 29, Anchor 50) underneath. "
     "The price is the claim."),
    ("6", "the pipeline", "Agent / the wall / my phone - three cells, flow reading in the post's "
     "direction. The architecture at a glance, least emotional."),
]

post = POST.read_text(encoding="utf-8").strip()
chars = len(post)


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
        elif code == "3-HE":
            tag = ' <span class="rec">YOUR LAST TWO PICKS WERE THIS SHAPE</span>'
        opts += (f'<div class="opt" data-value="{code}">'
                 f'<div class="opt-head"><span class="dot"></span>'
                 f'<b>{code}</b> &middot; {html.escape(name)}{tag}</div>'
                 f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; the agent-browser handoff</p>
  <h1>The agent fills the cart, you press Pay. Pick the hero, settle two calls.</h1>
  <p class="lede">Drafted from last night's build: your agent - NanoClaw, named in the post as you asked - gets a real Chrome in the cloud, and when
  it hits a password, 2FA or the Pay button it hands the browser to your phone, waits, and carries
  on with the login intact. Reframed on your steers: the spine is the MOBILE story (on a PC this is
  easy - remote agent + you on a phone is the hard part), Cloudflare and the 5 dollars/month are
  named in the post with the four-way price comparison, and the free-tier war story moved to the
  blog. Blog is written and ready to push; link goes in the first comment.</p>
</div>

<section class="step">
  <h2>The post</h2>
  <p class="sub">{chars:,} characters (cap 3,000). Hebrew, אמ!לק opener, אמזון in line 1, NanoClaw named in paragraph 2,
  Cloudflare + 5 dollars/month named, closes on the first-comment offer.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
</section>

<section class="step">
  <h2>01 &middot; Hero image - pick one</h2>
  <p class="sub">Six designs, English and Hebrew. Click one; your pick saves in this page. The full
  local path above each image pastes straight into LinkedIn's file picker.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>02 &middot; The toilet paper - keep or dignify?</h2>
  <p class="q">Line 1 says you sent your agent to buy toilet paper. It is the real task from the real
  test, and it is exactly the slightly-embarrassing human detail that works for you.</p>
  <div id="toilet-paper" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Nobody invents toilet paper for a LinkedIn post, which is why it reads as true.
      The closing line (we proved it works, and there is toilet paper at home) depends on it.</p></div>
    <div class="opt" data-value="generic"><div class="opt-head"><span class="dot"></span>
      <b>Make it a generic purchase</b></div>
      <p class="why">Swap for something neutral. Safer, flatter, and the closing line loses its
      punch - it would need a rewrite.</p></div>
  </div>
</section>

<section class="step">
  <h2>03 &middot; The close - offer only, or add a question?</h2>
  <p class="q">The draft ends on the first-comment offer, per your callrec edit (hand the reader
  the thing, no clever question). Two of your last three posts kept a short question anyway.</p>
  <div id="closing" data-persist-choice class="opts small">
    <div class="opt" data-value="offer-only"><div class="opt-head"><span class="dot"></span>
      <b>Offer only (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The architecture, the traps and the numbers - in the first comment. Clean.</p></div>
    <div class="opt" data-value="add-question"><div class="opt-head"><span class="dot"></span>
      <b>Add a short question before the offer</b></div>
      <p class="why">e.g. מה הייתם נותנים לאייג'נט לעשות לבד, ואיפה הייתם עוצרים אותו? One line,
      plain, comment bait for a post whose subject is exactly that boundary.</p></div>
  </div>
</section>

<section class="step">
  <h2>The first comment - ready to paste</h2>
  <div class="copybar"><button class="copybtn" data-copy="first-comment">Copy first comment</button></div>
  <pre id="first-comment" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >הסיפור המלא - הארכיטקטורה, מודל האבטחה, והארבע תקלות שכל אחת מהן נראתה כמו משהו אחר:
https://gal.tidhar.org.il/blog/agent-handoff/</pre>
</section>

<section class="step">
  <h2>What I removed, and two honest notes</h2>
  <ul>
    <li><b>Privacy pass:</b> the post and blog name no family members and no other agents - the
      wider household system stays out entirely. No host addresses, tokens or account IDs anywhere,
      including the page metadata. The one profanity-adjacent moment (you, at the phone, with the
      panel over the login) survives as "עמדתי עם הטלפון וקיללתי" - your register, softened one notch
      for the feed; roughen it back if you want.</li>
    <li><b>The security caveat is in the blog, not the post:</b> the phone-approval flow genuinely
      weakens the boundary it replaced (a tap replaces an offline file edit, and the agent proposes
      the host). In the post it would cost 300 characters against a reader who has no boundary yet;
      in the blog it is stated plainly.</li>
    <li><b>Not claimed anywhere:</b> production-hardened, bot-evasion, or general security. Every
      number is from the actual test: 925 seconds, 10 min/day free tier, 5 dollars/month.</li>
    <li><b>Blog is written but not pushed.</b> On your hero pick I set og.png to its EN twin,
      commit and push - the first-comment link goes live then.</li>
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
                  "<title>Agent handoff - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
