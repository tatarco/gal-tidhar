#!/usr/bin/env python3
"""Build the ZaZet choices doc for the croatian-ferries post."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
DR = pathlib.Path.home() / ".claude/skills/linkedin/drafts"
POST_HE = (DR / "croatian-ferries.txt").read_text(encoding="utf-8").strip()
POST_EN = (DR / "croatian-ferries-en.txt").read_text(encoding="utf-8").strip()
WRAP_SRC = HERE.parent / "whatsapp-presence" / "out-choices.html"
WRAP_BODY = HERE.parent / "whatsapp-presence" / "choices-body.html"

DESIGNS = [
    ("1", "the one big number", "RECOMMENDED. בעוד 23 דקות, huge, with the line under it. The hero you asked "
     "for: 'your next ferry {time}'. Closest to what carried cache-economics to 25k with no logo - a number a "
     "reader instantly understands - and it is literally what the product shows."),
    ("3", "the exchange", "STRONG CONTENDER. The real PDF footnotes (14:30* 16:00** / * Sails 20.06. & 27.06.) "
     "next to 'your next ferry in 23 min'. Shows the actual before/after, which is the shape that won on "
     "Claude-Code-Hebrew. Teaches the frustration in one second without reading the post."),
    ("2", "the claim", "The bold-claim shape, your most-picked: נמאס לי לפענח PDF / אז בניתי את התשובה. "
     "Line 1 of the post as an image."),
    ("5", "the payoff quote", "כל לוח זמנים של מעבורת בקרואטיה הוא PDF. The shared-frustration line, huge. "
     "The most quotable frame, but it sells the problem rather than the answer."),
    ("4", "what the port page answers", "The five questions and their answers, ending with 'can my "
     "mother-in-law read it'. A list, and lists read as reports - but it is the clearest product tour."),
    ("6", "the pipeline", "PDF → judgment → answer. The actual mechanism, and the frame a technical reader "
     "will like most, but it needs the post to land."),
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


TAGS = {"1-HE": "RECOMMENDED", "3-HE": "CONTENDER", "1-EN": "IF ENGLISH POST", "3-EN": "IF ENGLISH POST"}
opts = ""
for num, name, why in DESIGNS:
    for lang in ("he", "en"):
        opts += option(num, name, why, lang, TAGS.get(f"{num}-{lang.upper()}", ""))

FIRST_HE = """האתר: https://croatianferries.com

הסיפור המלא, איך קוראים 23 קבצי PDF פעם אחת, הבאג של 40 הדקות, ומה עוד חסר:
https://gal.tidhar.org.il/blog/croatian-ferries/

דוגמה לעמוד נמל (ולביסקה, קרק): https://croatianferries.com/en/port/valbiska/"""

FIRST_EN = """The site: https://croatianferries.com

The full story, how 23 PDFs get read once, the 40-minute bug, and what is still missing:
https://gal.tidhar.org.il/blog/croatian-ferries/

A port page, to see it: https://croatianferries.com/en/port/valbiska/"""


def pre(id_, text, rtl):
    style = 'direction:rtl;text-align:right;' if rtl else ''
    return (f'<pre id="{id_}" class="term" style="{style}white-space:pre-wrap">{html.escape(text)}</pre>')


BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; croatianferries.com</p>
  <h1>I was done decrypting PDFs to find my next ferry. Pick the language, the hero, and three lines.</h1>
  <p class="lede">The hook you asked for: enough decrypting PDF timetables, a frustration every Croat with a
  car and every German or Italian tourist shares, and the hero is the product's own line, "your next ferry
  in 23 min". The spine is one mechanism: reading a timetable is judgment, copying 600 times out of it is not,
  so one small file per line records the judgment and code copies the times from the PDF's own text. The
  40-minute bug is demoted to one practical line. The queue camera, the thing you actually started from,
  is named honestly as still on its way. It closes on the embarrassing number: 20 visits, most of them you.</p>
</div>

<section class="step">
  <h2>01 &middot; Which language goes on LinkedIn?</h2>
  <p class="q">Your reach is Israeli tech and every outlier was Hebrew. But the people this site is FOR read
  Croatian, German, Italian and English, and this is the first post that is a product for them rather than
  a story for your network.</p>
  <div id="lang" data-persist-choice class="opts small">
    <div class="opt" data-value="he"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The audience that actually sees your posts. The story (PDF hell, the judgment/copy split,
      the 20 visits) is a builder story, and that is what your network engages with. The site link in the
      first comment still works for anyone.</p></div>
    <div class="opt" data-value="en"><div class="opt-head"><span class="dot"></span>
      <b>English</b></div>
      <p class="why">Reaches Croatian and tourist readers if it gets reshared, at the cost of the reach the
      ledger shows. Same post, translated, below.</p></div>
    <div class="opt" data-value="both"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew now, English a week later</b></div>
      <p class="why">Two posts, two entities. The English one can ride whatever the Hebrew one does.</p></div>
  </div>
</section>

<section class="step">
  <h2>The post, Hebrew</h2>
  <p class="sub">{len(POST_HE):,} characters (cap 3,000). אמ!לק opener, PDF and Jadrolinija in the first two
  lines, the lived moment in the car, the mechanism once, the 40-minute bug in one line, the honest close.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-he">Copy Hebrew post</button></div>
  {pre("post-he", POST_HE, True)}
</section>

<section class="step">
  <h2>The post, English</h2>
  <p class="sub">{len(POST_EN):,} characters. Same post, same order.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-en">Copy English post</button></div>
  {pre("post-en", POST_EN, False)}
</section>

<section class="step">
  <h2>02 &middot; Hero image - pick one</h2>
  <p class="sub">Six designs, Hebrew and English. Click one; your pick saves in this page. The full local
  path above each image pastes straight into LinkedIn's file picker. Match the hero language to decision 01.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>03 &middot; The "20 visits, most of them me" line</h2>
  <p class="q">Last paragraph. It is the true number from the analytics report this week (20 visits, 60 page
  views, 71 of them from the US which is mostly you and crawlers). It is the slightly embarrassing line that
  proves a person wrote it.</p>
  <div id="visits" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Nobody launching a product writes this. That is the point.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it, end on the ask</b></div>
      <p class="why">Cleaner launch post. Loses the only undefended line in it.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; Name Claude Code?</h2>
  <p class="q">The draft never says how it was built. The ledger says a recognizable name in line 1 is the
  cheapest scroll-stop, and the site itself came together between 29 Aug and 2 Sep (the camera work goes
  back to June). PDF is already the named thing in line 1.</p>
  <div id="claude" data-persist-choice class="opts small">
    <div class="opt" data-value="no"><div class="opt-head"><span class="dot"></span>
      <b>Leave it out</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">This post is about the ferry, not the tool. Adding the tool makes it a "look what AI
      built" post, which is the genre you said reads as slop.</p></div>
    <div class="opt" data-value="one-line"><div class="opt-head"><span class="dot"></span>
      <b>One line before the close</b></div>
      <p class="why">e.g. האתר עצמו נבנה בחמישה ימים עם Claude Code. המצלמות לקחו מיוני. True, and it buys
      the name without making it the story.</p></div>
  </div>
</section>

<section class="step">
  <h2>05 &middot; The line you take</h2>
  <p class="q">The draft says "the ferry" without naming which one you sit in the queue for. The hero uses
  Valbiska → Merag because that is the line the project's cameras watch. If you actually take a different
  one, say which and I swap it into the post and the hero.</p>
  <div id="line" data-persist-choice class="opts small">
    <div class="opt" data-value="valbiska-merag"><div class="opt-head"><span class="dot"></span>
      <b>Valbiska → Merag is right</b> <span class="rec">ASSUMED</span></div>
      <p class="why">Krk to Cres, the one the project started on in June.</p></div>
    <div class="opt" data-value="other"><div class="opt-head"><span class="dot"></span>
      <b>A different line</b></div>
      <p class="why">Write it in the comments here or in chat.</p></div>
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
    <li><b>Every number is from the repo this run:</b> 23 car-ferry lines (23 spec files, 23 operator PDFs),
      52 departure ports, 1,076 sailings and 105 seasons (docs/LAUNCH.md, matching the spine), four languages
      with German and Italian reviewed by native speakers (commit 2026-08-31). The 20 visits are from
      <code>scripts/analytics_report.py</code> run today: 20 visits, 60 page views, last 7 days.</li>
    <li><b>The footnotes on the hero are real,</b> copied from the 332 and neighbouring specs: "* Sails 20.06.
      &amp; 27.06. ** 20.06. &amp; 27.06. departs at 18:00." The 14:30 / 16:00 / 18:30 times are illustrative,
      not a real row, so the image never claims a specific departure exists.</li>
    <li><b>The 40-minute bug is real</b> (LAUNCH.md §4, line 434 Zadar - Brbinj, fixed with
      tests/spine/test_duration.py). It is a parser bug, not an AI story, and it is one line in the post.</li>
    <li><b>The queue camera is honestly "still on its way":</b> nothing is capturing yet, every port page says
      coming soon, and the verdict block self-heals when capture starts. Said plainly in the post.</li>
    <li><b>The blog is live at</b> gal.tidhar.org.il/blog/croatian-ferries/ with the spec excerpt, the validator,
      the hash-watched PDFs, the duration bug and what is deliberately not on the site. og.png is 2-EN until you
      pick; then I set it to your pick's EN twin and push.</li>
    <li><b>Privacy pass:</b> nothing personal in any surface. No home location is stated; the line is named
      only as the one the cameras watch. The "mother-in-law" on hero 4 is a joke about languages, no
      circumstances.</li>
    <li><b>Known weakness:</b> line 1 has no famous company. PDF is the recognizable thing, and 23 minutes is
      the checkable number. Jadrolinija means nothing to an Israeli reader, so it sits in line 2 as texture.</li>
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
doc = doc.replace("<title>WhatsApp went silent - LinkedIn post", "<title>Croatian ferries - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
