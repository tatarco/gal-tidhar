#!/usr/bin/env python3
"""Build the ZaZet choices doc for the Facebook post (personal profile, English)."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
POST = (HERE / "post-fb.txt").read_text(encoding="utf-8").strip()
WRAP_SRC = HERE.parent / "ferry-vision" / "out-choices.html"
WRAP_BODY = HERE.parent / "ferry-vision" / "choices-body.html"

HEROES = [
    ("hero-fb", "A", "the combination, with a headline", "RECOMMENDED",
     "Both screenshots on the site's own cream, with the question a driver actually asks across the top. "
     "A friend scrolling past reads the headline, sees a real port camera at night and a card full of real "
     "departure times, and understands the whole thing without reading a word of the post. It is also the only "
     "one of the three that works as a thumbnail."),
    ("hero-fb-b", "B", "the two screenshots, no headline", "",
     "Pure product. No claim, no copy, just the thing itself - the live camera with 'a queue is starting' and "
     "the departures card. More honest-looking and less like an ad; weaker for anyone who scrolls without "
     "reading the post."),
    ("hero-fb-c", "C", "13 boats against 8 printed", "",
     "The one surprising fact, blown up: the timetable prints 8 for that stretch and 13 actually left. This is "
     "the most shareable of the three and the most likely to start an argument in the comments with someone who "
     "lives there - which on Facebook is the point. It hides the live camera entirely."),
]


def img(stem, code):
    p = HERE / f"{stem}.png"
    prev = HERE / f".preview-{code}.jpg"
    if not prev.exists():
        subprocess.run(["sips", "-Z", "1100", "-s", "format", "jpeg", "-s", "formatOptions", "74",
                        str(p), "--out", str(prev)], check=True, capture_output=True)
    b64 = base64.b64encode(prev.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{code}</b></p>'
            f'<img src="data:image/jpeg;base64,{b64}" alt="hero {code}">')


opts = ""
for stem, code, name, tag, why in HEROES:
    t = f' <span class="rec">{tag}</span>' if tag else ""
    opts += (f'<div class="opt" data-value="{code}">'
             f'<div class="opt-head"><span class="dot"></span><b>{code}</b> &middot; {html.escape(name)}{t}</div>'
             f'<p class="why">{html.escape(why)}</p>{img(stem, code)}</div>')

FIRST = """croatianferries.com

Line 332 Valbiska (Krk) - Merag (Cres), and every other line in the country:
https://croatianferries.com/en/line/332/"""


def pre(id_, text):
    return f'<pre id="{id_}" class="term" style="white-space:pre-wrap">{html.escape(text)}</pre>'


BODY = f"""
<div class="title">
  <p class="eyebrow">Facebook &middot; personal profile &middot; croatianferries.com</p>
  <h1>When do I need to be at the ferry, and is it even running tonight?</h1>
  <p class="lede">Not a LinkedIn post. This one is for your own wall, in English, written the way you would
  actually tell a friend: the same conversation in the car every time you drive back from Lo&#353;inj, and the page
  that finally answers it. <b>Zero technical content</b> - no cameras-as-sensors, no detection, no method. The only
  numbers in it are the ones a driver cares about: be there by 20:06, 13 boats today against 8 printed.
  {len(POST):,} characters.</p>
</div>

<section class="step">
  <h2>The post - ready to paste</h2>
  <div class="copybar"><button class="copybtn" data-copy="post">Copy post</button></div>
  {pre("post", POST)}
</section>

<section class="step">
  <h2>01 &middot; Hero image - pick one</h2>
  <p class="sub">Facebook is not LinkedIn: the feed is friends, family and people who actually drive this route, and
  a photo of the real thing beats a designed claim card every time. All three are built from your own two
  screenshots. The full local path above each image pastes straight into the file picker.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>02 &middot; Where does the link go?</h2>
  <p class="q">On LinkedIn the link always goes in the first comment because a link in the body costs reach. Facebook
  behaves differently, and on a personal profile the trade is different again.</p>
  <div id="link" data-persist-choice class="opts small">
    <div class="opt" data-value="body-plain"><div class="opt-head"><span class="dot"></span>
      <b>In the body, as plain text, with the image attached</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">As drafted: "croatianferries.com" on its own line, no https, and the hero attached as a photo.
      Facebook shows your image rather than generating its own preview card, the URL stays tappable, and friends can
      copy it. This is the version that looks like a person sharing something, not a page running an ad.</p></div>
    <div class="opt" data-value="preview"><div class="opt-head"><span class="dot"></span>
      <b>Full https:// URL, let Facebook build the preview card</b></div>
      <p class="why">You lose control of the image - Facebook picks the og:image - but the whole card becomes
      clickable, which gets more clicks from people on phones. Worth it only if the site's own preview image is
      better than these three, and it is not.</p></div>
    <div class="opt" data-value="comment"><div class="opt-head"><span class="dot"></span>
      <b>First comment, LinkedIn style</b></div>
      <p class="why">Safest for reach if you think your profile gets throttled for outbound links. Costs you every
      friend who reads the post and never opens the comments, which on a personal wall is most of them.</p></div>
  </div>
</section>

<section class="step">
  <h2>03 &middot; The opening line</h2>
  <p class="q">You asked for a super excited tone. Drafted as: <i>"Ok I am far too excited about this, but I finally
  fixed the thing that has been annoying me for years."</i></p>
  <div id="open" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Excited and slightly self-deprecating at once, which is the register that survives on a
      personal wall. It also promises a fix rather than a product, so nobody scrolls past thinking it is an
      advert.</p></div>
    <div class="opt" data-value="story"><div class="opt-head"><span class="dot"></span>
      <b>Open on the car instead</b></div>
      <p class="why">"Every time we drive back from Lo&#353;inj it is the same conversation in the car." Starts on the
      shared experience rather than on you, which travels further among locals and slower among friends.</p></div>
    <div class="opt" data-value="rewrite"><div class="opt-head"><span class="dot"></span>
      <b>Write it yourself</b></div>
      <p class="why">It is your wall and your voice. If you have the line, mine goes.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; The ask at the end</h2>
  <p class="q">Drafted as: <i>"tell me what is missing or wrong. I fix whatever people complain about, usually the
  same day."</i> That sentence is what turned 52 Facebook group posts into 11 real issues.</p>
  <div id="ask" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is true, it invites the one kind of comment that is actually useful, and comments are what
      make Facebook show the post to more people.</p></div>
    <div class="opt" data-value="queue"><div class="opt-head"><span class="dot"></span>
      <b>Ask for the harder thing</b></div>
      <p class="why">"If you are sitting in that queue, press the I'm here button on the page." That is the one
      piece of data nobody but a person standing there can give you - but it is a bigger ask from a friend
      scrolling.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>End on the link</b></div>
      <p class="why">Cleanest, least needy, fewest comments.</p></div>
  </div>
</section>

<section class="step">
  <h2>05 &middot; Does this also go to the island groups?</h2>
  <p class="q">You already have 52 Croatian, German and English island groups mapped from episode 1. This post is
  written for a personal wall; the same text in a group reads differently.</p>
  <div id="groups" data-persist-choice class="opts small">
    <div class="opt" data-value="wall-only"><div class="opt-head"><span class="dot"></span>
      <b>Personal wall only, for now</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The groups had their launch round and the follow-up post is already parked for your review. A
      second wave this soon reads as spam to the same moderators who are already sitting on six of your posts.</p></div>
    <div class="opt" data-value="krk"><div class="opt-head"><span class="dot"></span>
      <b>Wall, plus the Krk / Cres / Lo&#353;inj groups only</b></div>
      <p class="why">This post is specifically about line 332, so the three islands it actually serves are a fair
      audience. Needs the "I" rewritten out of a couple of sentences.</p></div>
    <div class="opt" data-value="all"><div class="opt-head"><span class="dot"></span>
      <b>Roll it into the parked follow-up campaign</b></div>
      <p class="why">Use this as the body of the second wave to all 52 instead of writing a new one.</p></div>
  </div>
</section>

<section class="step">
  <h2>The first comment, if you pick that in decision 02</h2>
  <div class="copybar"><button class="copybtn" data-copy="first">Copy first comment</button></div>
  {pre("first", FIRST)}
</section>

<section class="step">
  <h2>Honest notes</h2>
  <ul>
    <li><b>Every number in the post is from your own two screenshots,</b> taken at 20:04 on 10 September: next boat
      20:30, be there by 20:06, 13 departures since 05:04, about one every 67 minutes, 8 printed for that stretch,
      last boat out 18:57 against its printed 19:00. Nothing was rounded or improved.</li>
    <li><b>The camera frame is a night shot of an empty road</b> while the label says "a queue is starting". That is
      what the site was actually saying at 20:04, and it is the weakest thing in hero A and B. If it bothers you, C
      avoids it entirely - or say the word and I will rebuild A around this afternoon's frame, where there is a real
      queue of cars up the hill, and change the times to match.</li>
    <li><b>Nothing technical is in the post,</b> as asked. No mention of how the queue is read, no detection, no
      method, no beta caveat. The site itself still carries the BETA tag on the queue line, which is visible in the
      hero, and that is the honest place for it.</li>
    <li><b>The €51.50 / 6 adults / 2 children panel was cropped out of the hero</b> - it is your own saved crossing
      and it named your family's size on a public post.</li>
    <li><b>The post says "free, no ads, no cookies, nothing to install",</b> which is true today. It does not say
      free forever.</li>
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
doc = doc.replace("<title>Ferry vision - LinkedIn post", "<title>Ferry - Facebook post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
