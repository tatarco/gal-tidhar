#!/usr/bin/env python3
"""Build the ZaZet choices doc body for the callrec post."""
import base64, html, pathlib

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/callrec.txt"
BLOG = "https://gal.tidhar.org.il/blog/callrec/"
REPO = "https://github.com/tatarco/callrec"

DESIGNS = [
    ("2c", "icon-forward (NEW)", "The row is the message: one short line, the platform icons flowing into Claude, a red REC dot on top."),
    ("2b", "the claim, with icons (NEW)", "Design 2 exactly as you liked it, plus the REC dot and the icon flow underneath."),
    ("1", "the one big number", "0 per month, 0 bytes leaving. Platforms + straight-into-Claude in the sub-line."),
    ("2", "the claim", "Every call, any platform, transcribed locally, handed to Claude. His proven shape - four picks running."),
    ("3", "the exchange", "Mic only = a monologue. Mic + BlackHole = a conversation. Teaches the whole constraint in one look."),
    ("4", "the architecture", "The three pieces and what each one does."),
    ("5", "the breakdown", "The three things that are not documented anywhere obvious."),
    ("6", "the payoff quote", "My memory of a call is a summary written by the guy who wanted the deal to go well."),
]

post = POST.read_text(encoding="utf-8").strip()


def img(num, lang):
    p = HERE / f"hero-{num}-{lang}.png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{num}-{lang.upper()}</b></p>'
            f'<img src="data:image/png;base64,{b64}" alt="hero {num} {lang}">')


opts = ""
for num, name, why in DESIGNS:
    rec = ' <span class="rec">RECOMMENDED</span>' if num == "2c" else ""
    for lang in ("en", "he"):
        code = f"{num}-{lang.upper()}"
        opts += (f'<div class="opt" data-value="{code}">'
                 f'<div class="opt-head"><span class="dot"></span>'
                 f'<b>{code}</b> &middot; {html.escape(name)}{rec if lang == "he" else ""}</div>'
                 f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; callrec</p>
  <h1>Post, heroes and the two open calls.</h1>
  <p class="lede">Pick a hero, answer the two questions at the bottom, and I will finish the blog
  post and the og image. Your picks save in the page.</p>
</div>

<section class="step">
  <h2>The post</h2>
  <p class="sub">2,832 characters, under LinkedIn's 3,000 cap. Hebrew, plain hyphens, link in the
  first comment.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
  <div class="copybar"><button class="copybtn" data-copy="comment-text">Copy first comment</button></div>
  <pre id="comment-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >הקוד, ההסבר המלא והמלכודות:
{BLOG}

הריפו: {REPO}</pre>
</section>

<section class="step">
  <h2>Hero image - pick one</h2>
  <p class="sub">Eight designs, each in English and Hebrew. The top two are the new icon versions. Click the one you want. The full path is
  printed above every image so you can paste it straight into LinkedIn's file picker.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>Two calls I did not want to make for you</h2>

  <p class="q">1. The client anecdote - keep it?</p>
  <p class="sub">The post says a prospect told me each of his customers has a different stack, and
  that by the time I wrote it down it had turned into the thing I wanted to build. No name, no
  company, no numbers. It is the most human beat in the post and it is also a live deal.</p>
  <div id="anecdote" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Nothing identifies him. Without it the post is a tool demo.</p></div>
    <div class="opt" data-value="generic"><div class="opt-head"><span class="dot"></span>
      <b>Make it generic</b></div>
      <p class="why">"A client said something and I wrote down my own version of it." Safer, flatter.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it</b></div>
      <p class="why">Post ends on the mechanism and the Claude Code skill.</p></div>
  </div>

  <p class="q">2. Name the skill?</p>
  <p class="sub">The post currently names <code>/dealroom-record</code>, which is my own private
  deal pipeline. Naming it invites "what is dealroom" questions in the comments - good for reach,
  and it points at how you actually work.</p>
  <div id="skillname" data-persist-choice class="opts small">
    <div class="opt" data-value="name"><div class="opt-head"><span class="dot"></span>
      <b>Name it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is the most interesting part and it is the thing people will ask about.</p></div>
    <div class="opt" data-value="unnamed"><div class="opt-head"><span class="dot"></span>
      <b>Describe it without the name</b></div>
      <p class="why">"A skill in Claude Code that files the transcript." Keeps the deal machinery private.</p></div>
  </div>
</section>

<section class="step">
  <h2>What I cut, and why</h2>
  <ul>
    <li>The client's name, his company, his industry and anything about his numbers. The post says
      "a prospect" and nothing else.</li>
    <li>The whisper benchmark (six seconds of audio in about two on an M4) - true, measured here,
      but it stalled the run toward the Claude Code payoff. It is in the blog post.</li>
    <li>The install command list. The post teaches the constraint; the blog post has the steps.</li>
  </ul>
  <div class="note-box"><b>Live now:</b> the repo is public at <code>{REPO}</code> and the blog
  post goes up at <code>{BLOG}</code> once you have picked a hero.</div>
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
.opts.small .opt{{cursor:pointer}}
.q{{font-weight:700;font-size:17px;margin-top:26px}}
</style>
<script src="/copy.js"></script>
<script src="/persist.js"></script>
"""

(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote choices-body.html", len(BODY), "bytes")
