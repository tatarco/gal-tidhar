#!/usr/bin/env python3
"""Build the ZaZet choices doc for the dont-punt post."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
DR = pathlib.Path.home() / ".claude/skills/linkedin/drafts"
POST_HE = (DR / "dont-punt.txt").read_text(encoding="utf-8").strip()
POST_EN = (DR / "dont-punt-en.txt").read_text(encoding="utf-8").strip()
WRAP_SRC = HERE.parent / "croatian-ferries" / "out-choices.html"
WRAP_BODY = HERE.parent / "croatian-ferries" / "choices-body.html"

DESIGNS = [
    ("2", "the claim", "RECOMMENDED. 'The model wasn't stuck. It decided the boring part was mine. Two words fixed it: "
     "don't punt.' The bold-claim shape, your most-picked five times running, and it carries the whole idea in one look."),
    ("3", "the exchange", "STRONG CONTENDER. The real 20:34 message (numbered clicks, 'reply continue'), your 'don't punt', "
     "and the 20:35 reply 'Taking over and driving it through myself'. Shows the actual artifact, the shape that won on "
     "Claude-Code-Hebrew. The transcript is the proof."),
    ("1", "the two words", "don't punt, huge, yellow. Closest to the Wiz-logo move: the image IS the thing the post is about."),
    ("5", "the payoff quote", "'Every answer that ends with reply continue is a punt.' The most quotable, and the practical "
     "tell the reader takes away."),
    ("4", "the three grades", "list / option / judgment. The most teachable frame and the non-obvious payoff, but it is a "
     "list, and lists read as reports."),
    ("6", "the mechanism", "mood vs. name of a move vs. why it lands. For the reader who wants the why. Needs the post."),
]

def img(num, lang):
    p = HERE / f"hero-{num}-{lang}.png"
    prev = HERE / f".preview-{num}-{lang}.jpg"
    if not prev.exists():
        subprocess.run(["sips", "-Z", "1000", "-s", "format", "jpeg", "-s", "formatOptions", "72",
                        str(p), "--out", str(prev)], check=True, capture_output=True)
    b64 = base64.b64encode(prev.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{num}-{lang.upper()}</b></p>'
            f'<img src="data:image/jpeg;base64,{b64}" alt="hero {num} {lang}">')


def option(num, name, why, lang, tag=""):
    code = f"{num}-{lang.upper()}"
    t = f' <span class="rec">{tag}</span>' if tag else ""
    return (f'<div class="opt" data-value="{code}">'
            f'<div class="opt-head"><span class="dot"></span>'
            f'<b>{code}</b> &middot; {html.escape(name)}{t}</div>'
            f'<p class="why">{html.escape(why)}</p>{img(num, lang)}</div>')


TAGS = {"2-HE": "RECOMMENDED", "3-HE": "CONTENDER", "2-EN": "IF ENGLISH POST", "3-EN": "IF ENGLISH POST"}
opts = ""
for num, name, why in DESIGNS:
    for lang in ("he", "en"):
        opts += option(num, name, why, lang, TAGS.get(f"{num}-{lang.upper()}", ""))

FIRST_HE = """כל חמשת הפאנטים מאותו ערב, מילה במילה, מה כתבתי אחרי כל אחד ומה המודל עשה בתשובה, ולמה "don't punt" עובד כש"תעשה את זה בעצמך" לא:
https://gal.tidhar.org.il/blog/dont-punt/"""

FIRST_EN = """All five punts from that evening, word for word, what I wrote after each and what the model did next, and why "don't punt" works when "just do it" does not:
https://gal.tidhar.org.il/blog/dont-punt/"""


def pre(id_, text, rtl):
    style = 'direction:rtl;text-align:right;' if rtl else ''
    return (f'<pre id="{id_}" class="term" style="{style}white-space:pre-wrap">{html.escape(text)}</pre>')


BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; don't punt</p>
  <h1>don't punt. Pick the language, the hero, and three lines.</h1>
  <p class="lede">The origin, from your own session log: last night, 18:34 to 20:51, wiring Bing, Clarity and GA4 into both
  sites. Five times the model ended with a numbered list of clicks and "reply continue and I'll take over". Five times you
  wrote don't punt and the next reply was "taking over" plus a tool call, no argument. The spine is one mechanism: a punt is
  a decision, not a failure, so "just do it" (a mood) gets a shorter list while "don't punt" (the name of a move the model
  already carries a rule against, stopping short) gets the ball back. The non-obvious payoff is the fifth punt, the one that
  came dressed as professional judgment ("you don't actually need GA4"). The angry paragraph is drafted in, undefended.</p>
</div>

<section class="step">
  <h2>01 &middot; Which language goes on LinkedIn?</h2>
  <p class="q">Every outlier was Hebrew, and Claude Code is a name the Israeli-tech feed stops for. But this one is a
  prompting tip that travels, and the English draft is under the cap.</p>
  <div id="lang" data-persist-choice class="opts small">
    <div class="opt" data-value="he"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The audience that actually sees your posts. Claude Code in line 1, the two words stay in English.</p></div>
    <div class="opt" data-value="en"><div class="opt-head"><span class="dot"></span>
      <b>English</b></div>
      <p class="why">2,957 characters, 43 under the cap. Same post, same order.</p></div>
    <div class="opt" data-value="both"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew now, English a week later</b></div>
      <p class="why">Two posts, two entities.</p></div>
  </div>
</section>

<section class="step">
  <h2>The post, Hebrew</h2>
  <p class="sub">{len(POST_HE):,} characters (cap 3,000). אמ!לק opener with Claude Code and the two words in line 1, the
  evening, the angry paragraph, the football definition, the mechanism once, the continue tell, the fifth punt as the
  embarrassing close, first-comment pointer.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-he">Copy Hebrew post</button></div>
  {pre("post-he", POST_HE, True)}
</section>

<section class="step">
  <h2>The post, English</h2>
  <p class="sub">{len(POST_EN):,} characters.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-en">Copy English post</button></div>
  {pre("post-en", POST_EN, False)}
</section>

<section class="step">
  <h2>02 &middot; Hero image - pick one</h2>
  <p class="sub">Six designs, Hebrew and English. Click one; your pick saves in this page. The full local path above
  each image pastes straight into LinkedIn's file picker. Match the hero language to decision 01.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>03 &middot; The "are you stupid" paragraph</h2>
  <p class="q">Paragraph five. Written from your actual messages (are you stupid, don't fuck with me, do itttttt). The
  post keeps "are you stupid" and drops the curse; the blog keeps both.</p>
  <div id="angry" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep as drafted</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is the paragraph a model would never write about itself. Three posts running the drafted raw
      paragraph survived untouched.</p></div>
    <div class="opt" data-value="curse"><div class="opt-head"><span class="dot"></span>
      <b>Keep, and put the curse back in</b></div>
      <p class="why">"don't fuck with me" verbatim, as on the fleeceware post.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it</b></div>
      <p class="why">Cleaner. Loses the only undefended line in the post.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; The "just do it doesn't work" claim</h2>
  <p class="q">The mechanism paragraph says "do it yourself" is a mood the model answers with a shorter list. Evidence in
  the log: punt three, where you wrote "do itttttt dont punt" together, so I cannot separate the two. It is your
  experience or it is not.</p>
  <div id="mood" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>True, keep it</b> <span class="rec">ASSUMED</span></div>
      <p class="why">The contrast is what makes "name the move" land.</p></div>
    <div class="opt" data-value="soften"><div class="opt-head"><span class="dot"></span>
      <b>Soften to "in my experience"</b></div>
      <p class="why">Same paragraph, one hedge.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut the contrast, keep "name of a move"</b></div>
      <p class="why">Shorter mechanism, no claim about what does not work.</p></div>
  </div>
</section>

<section class="step">
  <h2>05 &middot; The "stopping short" line</h2>
  <p class="q">The post says Claude Code's own instructions tell the model not to hand back work it can finish and name
  that failure "stopping short". That is what I see in the instructions I run with; Anthropic has not published it. It is
  the strongest line in the why, and the one someone could ask you to source.</p>
  <div id="ss" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is true, and it is the difference between a prompt trick and a pointer.</p></div>
    <div class="opt" data-value="soften"><div class="opt-head"><span class="dot"></span>
      <b>Drop the name, keep the claim</b></div>
      <p class="why">"the model is already trained against exactly this", without "stopping short".</p></div>
  </div>
</section>

<section class="step">
  <h2>The first comment - ready to paste</h2>
  <div class="copybar"><button class="copybtn" data-copy="first-he">Copy Hebrew first comment</button></div>
  {pre("first-he", FIRST_HE, True)}
  <div class="copybar" style="margin-top:18px"><button class="copybtn" data-copy="first-en">Copy English first comment</button></div>
  {pre("first-en", FIRST_EN, False)}
</section>

<section class="step">
  <h2>Honest notes, and what I checked</h2>
  <ul>
    <li><b>Every quote is from the session log</b> (zazet-solutions session of 2026-09-03, 18:34 to 20:51 UTC, five user
      messages containing "don't punt"). The 20:34 / 20:35 timestamps on hero 3 are real. "Taking over and driving it
      through myself" is the verbatim first reply after the first don't punt. The blog has all five, with what came
      before and after.</li>
    <li><b>Grep found no "punt" anywhere in your CLAUDE.md, skills or memory.</b> It is purely something you say in the
      moment. The blog says so and argues that is the right place for it.</li>
    <li><b>The hero and post keep "don't punt" in English</b> in the Hebrew version, isolated so bidi cannot reorder
      it. Everything else in the Hebrew frames is Hebrew; timestamps and product names are Latin.</li>
    <li><b>Privacy pass:</b> nothing personal. The sites are yours, the analytics IDs are not shown, no third party
      is named. Your own messages are quoted; the curse is in the blog, not the post, pending decision 03.</li>
    <li><b>Blog is live at</b> gal.tidhar.org.il/blog/dont-punt/ once pushed. og.png is 2-EN until you pick; then I set
      it to your pick's EN twin.</li>
    <li><b>Known weakness:</b> this is a post about the model's behaviour, which the ledger says you distrust as a
      genre. The spine is what the reader gets (two words and why they work), not the failure, and the failure is a
      choice rather than an error. If it still reads as an AI-slop story to you, say so and I reframe around the
      three grades.</li>
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
doc = doc.replace("<title>Croatian ferries - LinkedIn post", "<title>don't punt - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
