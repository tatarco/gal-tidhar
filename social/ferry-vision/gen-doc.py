#!/usr/bin/env python3
"""Build the ZaZet choices doc for the ferry-vision post (episode 3: the queue light)."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
DR = pathlib.Path.home() / ".claude/skills/linkedin/drafts"
POST_HE = (DR / "ferry-vision.txt").read_text(encoding="utf-8").strip()
POST_EN = (DR / "ferry-vision-en.txt").read_text(encoding="utf-8").strip()
WRAP_SRC = HERE.parent / "ferry-analytics" / "out-choices.html"
WRAP_BODY = HERE.parent / "ferry-analytics" / "choices-body.html"

DESIGNS = [
    ("1", "the frame with the zones drawn on it", "RECOMMENDED, and the one you asked for. The real 17:16 frame "
     "from camera 488 - a queue of cars up the hill and the red polygon at the bend with a lorry in it - with the "
     "487 frame inset showing green and yellow, and the three colours defined underneath. This is the Wiz "
     "principle: the image IS the thing the post is about, not a description of it. It is also the only hero here "
     "that a non-technical reader understands in one second, and the only one that shows the product."),
    ("2", "the claim", "STRONG CONTENDER, and your most-picked shape across the ledger. States the moat in five "
     "words - it is not the model, it is the picture of the empty road - which is the line the whole post hangs "
     "on. Cost: it states the conclusion instead of showing the evidence, and line 1 already spends it."),
    ("4", "the two humps", "THE ONE FOR A TECHNICAL READER. The real distribution, 576 readings over three days, "
     "with the threshold marked in the valley. It proves the claim that nobody chose the threshold by hand, which "
     "is the most falsifiable thing in the post. It also needs three seconds of reading and a chart literacy that "
     "half your feed does not have."),
    ("6", "50 minutes", "The one-big-number shape, which is your 25,185 post. Red at 17:17, one boat at 17:33, "
     "green at 18:07. It carries the most surprising fact in the post and it does not repeat the hook."),
    ("5", "what the camera saw at Merag", "The credibility table: 13 printed departures against 16 seen, the edge "
     "density numbers, 311,537 frames. The most defensible of the six and the most boring - it is a table, and "
     "tables read as reports."),
    ("3", "stopped measuring / measure instead", "The exchange shape. How many cars are waiting, against is this "
     "patch still road. It teaches the whole design decision in one look, which is the actual spine of the post."),
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


TAGS = {"1-HE": "RECOMMENDED", "2-HE": "CONTENDER", "1-EN": "IF ENGLISH POST"}
opts = ""
for num, name, why in DESIGNS:
    for lang in ("he", "en"):
        opts += option(num, name, why, lang, TAGS.get(f"{num}-{lang.upper()}", ""))

FIRST_HE = """כל השיטה, המספרים, שתי הטעויות ומה שעדיין לא עובד:
https://gal.tidhar.org.il/blog/ferry-vision/

הרמזור החי, מרג: https://croatianferries.com/en/port/merag/
פרק 1, 52 קבוצות פייסבוק בתור באג טראקר: https://gal.tidhar.org.il/blog/ferry-outreach/
פרק 2, שבוע ראשון בחיפוש: https://gal.tidhar.org.il/blog/ferry-analytics/"""

FIRST_EN = """The whole method, the numbers, the two mistakes and what still does not work:
https://gal.tidhar.org.il/blog/ferry-vision/

The live light, Merag: https://croatianferries.com/en/port/merag/
Episode 1, 52 Facebook groups as a bug tracker: https://gal.tidhar.org.il/blog/ferry-outreach/
Episode 2, week one in search: https://gal.tidhar.org.il/blog/ferry-analytics/"""


def pre(id_, text, rtl):
    style = 'direction:rtl;text-align:right;' if rtl else ''
    return (f'<pre id="{id_}" class="term" style="{style}white-space:pre-wrap">{html.escape(text)}</pre>')


BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; croatianferries.com &middot; series post 3</p>
  <h1>I stopped counting cars. I ask whether that patch of road is still road.</h1>
  <p class="lede">Episode 3, the one episode 1 promised: <b>the queue camera</b>. The spine is the method, taken all
  the way down - a per-hour reference of the empty road built from a nine-day per-pixel median, brightness levelled,
  the fraction of pixels that moved, two humps and a threshold in the valley. Then green/yellow/red, the 18 and 14
  minutes to full measured from the archive rather than predicted, the ship on the ramp read by edge density (which
  found three sailings the timetable does not print), and the moment yesterday when one boat took a queue that had
  reached the bend. The moat claim is the close, and it is deliberately unflattering: none of the code is clever,
  the asset is 311,537 frames that only started accruing on 29 August.</p>
</div>

<section class="step">
  <h2>01 &middot; Which language goes on LinkedIn?</h2>
  <p class="q">Same call as episodes 1 and 2.</p>
  <div id="lang" data-persist-choice class="opts small">
    <div class="opt" data-value="he"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">{len(POST_HE):,} characters, cap 3,000. Every outlier you have was Hebrew, and this is the most
      technical post in the series, which is what your network engages with.</p></div>
    <div class="opt" data-value="en"><div class="opt-head"><span class="dot"></span>
      <b>English</b></div>
      <p class="why">{len(POST_EN):,} characters. This is the one post in the series with genuine international
      reach - it is a computer-vision method, not a Croatian ferry story - at the cost of the reach the ledger
      actually measures.</p></div>
    <div class="opt" data-value="both"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew now, English a week later</b></div>
      <p class="why">Two entities, two posts. Worked once before, and this is the strongest candidate in the series
      for it.</p></div>
  </div>
</section>

<section class="step">
  <h2>The post, Hebrew</h2>
  <p class="sub">{len(POST_HE):,} characters. אמ!לק with the episode frame and the moat claim in line 1, the local's
  sentence, the not-road rule, the method, the two humps, the three squares and where the method dies, time to full,
  the ship by edge density, the 50 minutes, no counts, the YOLO-World weeks, and the moat.</p>
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
  <p class="sub"><b>What your own numbers say.</b> Your 133,171 post carried a single image that WAS its subject -
  the Wiz logo itself. Your 25,185 post had no famous name and ran on one measured number. On episode 1 you took the
  artifact shape over the claim shape for the first time.</p>
  <p class="sub"><b>Which one here.</b> 1-HE, which is also what you asked for: the real frame with the zones drawn
  on it. It is the artifact shape at its strongest - the picture is literally what the post is about, a cold reader
  understands it in one second with no chart literacy, and the three colours are defined right under it so the
  image carries the whole idea on its own if nobody reads a word.</p>
  <p class="sub"><b>The honest note on it.</b> Green and yellow are on camera 487 and red is on 488, so the hero is a
  composite of two frames from the same minute, not one photograph. The inset says which camera it is; if you would
  rather ship a single unedited frame, 1 minus the inset is a one-line change - say so.</p>
  <p class="sub">Click one; your pick saves in this page. The full local path above each image pastes straight into
  LinkedIn's file picker. Match the hero language to decision 01.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>03 &middot; The YOLO-World paragraph</h2>
  <p class="q">"I spent weeks on a beautiful physical explanation of why the camera cannot see that far. It sees
  fine. YOLO-World returned 2 cars on a frame with fifteen." The ledger says never build a post around a model
  getting something wrong - but here the model is a tool I chose, the mistake is mine, and the takeaway is usable by
  anyone with a detector.</p>
  <div id="yolo" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep as drafted</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is the human paragraph in a very technical post, it is genuinely embarrassing (weeks of
      confident physics over a wrong model), and the gift is concrete: when the detector disagrees with your eyes,
      swap the model before you theorise about optics. The spine of the paragraph is what the reader gets, not what
      the model did.</p></div>
    <div class="opt" data-value="shorter"><div class="opt-head"><span class="dot"></span>
      <b>Keep the lesson, drop the model names</b></div>
      <p class="why">Loses "YOLO-World" and "yolov8" and the 2-against-15. Safer against reading as an AI-fuckup
      story, and much less checkable.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it, blog only</b></div>
      <p class="why">About 300 characters shorter and the post is then all method, no mistake. Also the post's only
      real self-criticism.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; How much of the method stays in the post?</h2>
  <p class="q">The median reference, the brightness levelling, the 22 grey levels and the two humps are four
  paragraphs. It is the most teachable material you have had in the series, and it is also the deepest the series
  has gone into implementation.</p>
  <div id="method" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep all four</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The Wiz post taught HDR and PQ and 4,000 nits and did 133k. Depth is the engine here, not the
      brake, and "a car does not survive a median" is the single most repeatable sentence in the post.</p></div>
    <div class="opt" data-value="drop-hist"><div class="opt-head"><span class="dot"></span>
      <b>Drop the two-humps paragraph</b></div>
      <p class="why">Saves ~200 characters and the histogram hero then has nothing in the text to land on. Keeps
      the reference trick, which is the part people will remember.</p></div>
    <div class="opt" data-value="short"><div class="opt-head"><span class="dot"></span>
      <b>Two sentences, and let the blog carry it</b></div>
      <p class="why">"A reference of the empty road at that hour, and I count what no longer matches." Faster to the
      payoff, and the post stops being the thing a technical reader saves.</p></div>
  </div>
</section>

<section class="step">
  <h2>05 &middot; The moat close</h2>
  <p class="q">"A detector is a five-minute pip install. What you cannot download is what this road looks like empty
  at 06:00. 311,537 frames since 29 August. It is not clever, it just accumulates." This is the thing you named as
  the point of the post.</p>
  <div id="moat" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep as drafted</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is first person, it undersells itself ("it is not clever"), and it never tells the reader
      what they should do - which is the pattern you rewrote back into my draft on episode 1.</p></div>
    <div class="opt" data-value="harder"><div class="opt-head"><span class="dot"></span>
      <b>Say the word moat out loud</b></div>
      <p class="why">"This is my moat" as a sentence. More quotable, and closer to the LinkedIn-guru register you
      normally strip out.</p></div>
    <div class="opt" data-value="rewrite"><div class="opt-head"><span class="dot"></span>
      <b>Write it yourself</b></div>
      <p class="why">Your version of this kind of line was the best line in episode 1. If you have one, mine
      goes.</p></div>
  </div>
</section>

<section class="step">
  <h2>06 &middot; The close</h2>
  <p class="q">Drafted as an offer plus the first-comment pointer - "the code, the numbers and the frames in the
  first comment, and you can go and watch the light live". Fifth consecutive close-with-an-offer.</p>
  <div id="close" data-persist-choice class="opts small">
    <div class="opt" data-value="offer"><div class="opt-head"><span class="dot"></span>
      <b>As drafted</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Hands the reader the thing, which is what you replaced my clever closer with on callrec and
      what you did again on episode 1.</p></div>
    <div class="opt" data-value="question"><div class="opt-head"><span class="dot"></span>
      <b>Add one short question</b></div>
      <p class="why">"What would you have measured instead?" Invites the one comment thread that would actually help
      me - people who have solved outdoor background subtraction.</p></div>
    <div class="opt" data-value="ask"><div class="opt-head"><span class="dot"></span>
      <b>Ask for the thing you actually need</b></div>
      <p class="why">"If you are standing in that queue, press the button on the page." Labels are the real
      bottleneck and nobody but a person in the queue can give them.</p></div>
  </div>
</section>

<section class="step">
  <h2>07 &middot; Episode 4</h2>
  <p class="q">Worth deciding before someone asks in the comments.</p>
  <div id="next" data-persist-choice class="opts small">
    <div class="opt" data-value="valbiska"><div class="opt-head"><span class="dot"></span>
      <b>Valbiska: the lot that will not be read</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The honest sequel. Ten lanes, a contiguous run that starts anywhere and wraps, far lanes 6-10 px
      apart, a number that reads zero through half a busy Sunday, built and deliberately not shipped. A post about
      the thing that did not work, with the physics that killed it.</p></div>
    <div class="opt" data-value="labels"><div class="opt-head"><span class="dot"></span>
      <b>The only people who can label this data are standing in the queue</b></div>
      <p class="why">The feedback loop: three buttons, reports re-measured against their own frame at 04:40, one
      change a day at 05:30 because two cannot be told apart.</p></div>
    <div class="opt" data-value="silent"><div class="opt-head"><span class="dot"></span>
      <b>No promise, decide later</b></div>
      <p class="why">The series line stays generic.</p></div>
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
    <li><b>Every number was recomputed this run, not taken from memory.</b> 311,537 frames is a live ListObjectsV2
      count over the five camera prefixes in R2 (merag/488 68,440 &middot; merag/37 68,424 &middot; merag/487 68,423
      &middot; valbiska/67 53,127 &middot; valbiska/66 53,123). 13 day-prefixes at Merag from 2026-08-29, 10 at
      Valbiska from 2026-09-01. 4,193 frames on one camera on 10 Sept is a frame every ~20 s, which is what the post
      says.</li>
    <li><b>The two humps in hero 4 are real,</b> not drawn. 576 readings of the yellow zone, 6 Sept to 8 Sept,
      every five minutes, daylight only, computed with the shipping <code>notroad.Zone</code> code against the
      shipping references. 163 of them in the 0-5% bin, a trough of 6 in the 20-25% bin, and a second mass peaking
      at 50-55%. The threshold in the port config is 0.20.</li>
    <li><b>The 50-minute story is read off <code>data/spine/stage_log.jsonl</code> and
      <code>berth_log.jsonl</code>,</b> both committed: red at 15:17:56Z, yellow again at 15:27, the departure
      logged at 15:33:11Z, green at 16:07:56Z. The post uses local time (17:17 / 17:33 / 18:07), which is what the
      camera's own overlay shows.</li>
    <li><b>18 and 14 minutes come from the port config,</b> measured over 16 daytime cycles across nine days,
      30 Aug - 6 Sept. The post gives the medians without the ranges (4-34 and 2-24); the blog gives both. If you
      want the ranges in the post it is one clause, but it weakens the sentence.</li>
    <li><b>16 departures against 13 printed is the 8 September figure</b> from the berth log. 9 September was 20.
      The post uses 8 Sept because that is the day that was replayed against the timetable end to end.</li>
    <li><b>The hero frame is the real 15:16:26Z frame,</b> the minute the light was holding red, with the polygons
      drawn from <code>config/ports/merag.json</code> at the exact coordinates the code reads. The detector finds
      2 boxes inside the red polygon on that frame. The inset is the 487 frame from the same minute.</li>
    <li><b>Dennis is named only as "a local from Krk who sends me feedback".</b> His name, the fact that he has a
      contact who handles boarding at Valbiska, and everything else from that thread stays out of the post and out
      of the blog.</li>
    <li><b>Nothing here claims accuracy.</b> There is no precision/recall number anywhere, because there is no
      labelled set - which is the actual state of the project and is said out loud in the blog. The queue reading on
      the site is marked beta.</li>
    <li><b>What is in the blog and deliberately not in the post:</b> the Valbiska lane failure, the validation-set
      mistake (five frames sorted by busyness), the "do not report while replays are running" lesson, the ~19-minute
      lag between the text and the picture, and the feedback loop. Two of those are limitations in my own
      instrumentation, which the ledger says you cut from posts - so they are blog-only by default.</li>
    <li><b>Blog is live at</b> gal.tidhar.org.il/blog/ferry-vision/ once pushed, with the full method, both
      mistakes, the numbers and a "what I would not do again" list. Card added to the root index. og.png is 1-EN
      until you pick.</li>
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
doc = doc.replace("<title>Ferry analytics - LinkedIn post", "<title>Ferry vision - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
