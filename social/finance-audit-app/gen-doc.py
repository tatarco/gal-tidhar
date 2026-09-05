#!/usr/bin/env python3
"""Build the ZaZet choices doc for the finance-audit-app repost (media fix)."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/finance-audit-app.txt"
WRAP_SRC = HERE.parent / "finance-audit-beta" / "out-choices.html"
WRAP_BODY = HERE.parent / "finance-audit-beta" / "choices-body.html"

DESIGNS = [
    ("8", "the combination (1+2)", "Your call: the claim as headline, the three half-blind "
     "sources as the proof underneath, your own punch line - throw it all together and the real "
     "crap floats up - closing the block. The hook and the mechanism in one frame."),
    ("2", "the claim", "Bold-claim shape - four straight picks on your last four posts. The claim "
     "is the post's promise in one breath: a free app that finds where your parents' money leaks "
     "quietly. The brew-style one-line install and the testers ask sit underneath."),
    ("7", "the real product", "The actual app, rendered clean from source at exact LinkedIn ratio - "
     "not a cropped screenshot. The Wiz principle: the image IS the thing the post is about. "
     "Hebrew only, because the product is Hebrew."),
    ("1", "the one big number", "3 sources, each one half-blind alone. The mechanism insight from "
     "your own post body - mail knows why, the card knows how much, the bank never sees the "
     "revolving debt."),
    ("3", "the exchange", "Each source alone: half the story / all three together: the leaks "
     "surface. The same insight as design 1, compressed to two cells."),
    ("4", "the breakdown grid", "What each source cannot see, row by row, ending with double "
     "insurance and the forgotten sub. Most screenshot-able, also the densest."),
    ("5", "the payoff quote", "Your own closing line - let's help everyone's parents - at full "
     "size. The warmest frame, and the least informative for a cold reader."),
    ("6", "the pipeline", "One line, a few clicks, a report. Sells the brew-style installer, "
     "which is the newest engineering beat in the post."),
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
    langs = ("he",) if num == "7" else ("en", "he")
    for lang in langs:
        code = f"{num}-{lang.upper()}"
        tag = ""
        if code == "8-HE":
            tag = ' <span class="rec">YOUR PICK - 1+2 COMBINED</span>'
        elif code == "7-HE":
            tag = ' <span class="rec">RUNNER-UP</span>'
        opts += (f'<div class="opt" data-value="{code}">'
                 f'<div class="opt-head"><span class="dot"></span>'
                 f'<b>{code}</b> &middot; {html.escape(name)}{tag}</div>'
                 f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')

shots = "".join(
    f'<p class="pathline"><code>/Users/galtidhar/Desktop/Screenshot 2026-08-24 at 11.23.{s} '
    f'blurred.png</code></p>' for s in ("04", "14", "23", "27", "37"))

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; repost, media fix</p>
  <h1>Same post, better pictures. Pick the hero, the text does not move.</h1>
  <p class="lede">The testers post went up with raw app screenshots and 11 impressions - cheap to
  delete. The text below is exactly what you published, character for character. What changes is
  the media: one strong standalone hero on the post, the app walkthrough shots demoted to the
  first comment, where your post already promises them.</p>
</div>

<section class="step">
  <h2>The post - unchanged</h2>
  <p class="sub">{chars:,} characters, your published text verbatim. Copy, delete the old post,
  repost with the hero you pick below.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
</section>

<section class="step">
  <h2>Hero image - pick one</h2>
  <p class="sub">Six built designs in English and Hebrew, plus the real product shot. Click one;
  your pick saves in this page. The full local path above each image pastes straight into
  LinkedIn's file picker.</p>
  <p class="sub"><b>8-HE is your call, combined from 1+2:</b> the claim buys the one-second stop,
  the three half-blind sources reward the second look. The old media failed because five UI
  screenshots ask the feed to study them, and the feed never studies. <b>7-HE stays the
  runner-up:</b> the product itself, rendered clean at 1200&times;630 - your instinct with the
  Desktop screenshot was right, the crop was the only problem.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>The first comment - the walkthrough images</h2>
  <p class="q">Your post promises "מצרף תמונות נוספות בתגובות". What goes there?</p>
  <div id="comment-imgs" data-persist-choice class="opts small">
    <div class="opt" data-value="blurred-five"><div class="opt-head"><span class="dot"></span>
      <b>The five blurred step screenshots</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Already scrubbed of your name, the bank credential ID, the bank name, the
      Gmail line and the machine path. In a comment they are for the curious, not the scroll -
      exactly where dense UI shots belong. Paths:</p>{shots}</div>
    <div class="opt" data-value="product-only"><div class="opt-head"><span class="dot"></span>
      <b>Just the clean product render (7-HE)</b></div>
      <p class="why">One image in the comment instead of five. Cleaner, shows less of the actual
      flow the testers will walk through.</p></div>
    <div class="opt" data-value="none"><div class="opt-head"><span class="dot"></span>
      <b>Nothing - drop the promise</b></div>
      <p class="why">Only if you also edit the post line that promises them, which breaks the
      keep-the-text-verbatim baseline.</p></div>
  </div>
</section>

<section class="step">
  <h2>What I did not touch, and one honest note</h2>
  <ul>
    <li><b>The text is byte-for-byte what you published.</b> No AI-tells pass, no restructure -
      you wrote it, it stays. If you want a pass on it, say so and it becomes a separate step.</li>
    <li><b>Privacy in the media:</b> the five step screenshots are the blurred versions; the 7-HE
      product render was produced from source with an empty profile, so no real name, bank or
      path appears in any frame.</li>
    <li><b>Delete-and-repost cost:</b> the post sits at 11 impressions, so nothing real is lost.
      Repost in the morning Israel time rather than right now if you can - first-hour velocity
      is what the feed measures.</li>
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

# wrap: reuse the finance-audit-beta shell (head + mast / footer) around the new body
shell = WRAP_SRC.read_text(encoding="utf-8")
old_body = WRAP_BODY.read_text(encoding="utf-8")
i = shell.find(old_body.strip()[:80])
j = shell.find(old_body.strip()[-60:]) + 60
assert i > 0 and j > i, "wrapper markers not found"
doc = shell[:i] + BODY + shell[j:]
doc = doc.replace("<title>Finance audit beta - LinkedIn post",
                  "<title>Finance audit app - repost media")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
