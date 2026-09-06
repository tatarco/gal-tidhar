#!/usr/bin/env python3
"""Build the ZaZet choices doc for the ferry-analytics post (episode 2)."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
DR = pathlib.Path.home() / ".claude/skills/linkedin/drafts"
POST_HE = (DR / "ferry-analytics.txt").read_text(encoding="utf-8").strip()
POST_EN = (DR / "ferry-analytics-en.txt").read_text(encoding="utf-8").strip()
WRAP_SRC = HERE.parent / "ferry-outreach" / "out-choices.html"
WRAP_BODY = HERE.parent / "ferry-outreach" / "choices-body.html"

DESIGNS = [
    ("5", "the sawn-off title", "RECOMMENDED. The real port title as Google actually printed it, cut dead at 60 "
     "characters, with the fixed one underneath saying kamera uzivo. This is the Wiz principle: the image IS the "
     "artifact, not a description of it, and it is the one thing line 1 has not already spent. A cold reader sees a "
     "sentence chopped mid-word and has to know whose site that is."),
    ("1", "position 5", "STRONG CONTENDER. One measured number, which is the shape of your 25,185 post. The cost: "
     "line 1 of the post already says position 5 at Merag, so the hero repeats the hook instead of adding to it."),
    ("3", "aimed at / actually ranks", "The two columns side by side: 49, 57, 67 against 5, 8, 6, 9. It teaches the "
     "whole post in one look and it is the most useful frame for a technical reader. Needs two seconds of reading."),
    ("2", "the claim", "The bold-claim shape, your most-picked design across the ledger. Carries the post for a cold "
     "reader, but states the conclusion instead of showing the evidence."),
    ("4", "the ranking table", "All six queries with their positions, the four nobody aimed at on top. The most "
     "credible of the six and the most boring - it is a table, and tables read as reports."),
    ("6", "99 / 16 / 83", "Why only 16 ports claim a camera. The discipline frame. Good idea, weakest scroll-stop."),
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


TAGS = {"5-HE": "RECOMMENDED", "1-HE": "CONTENDER", "5-EN": "IF ENGLISH POST", "1-EN": "IF ENGLISH POST"}
opts = ""
for num, name, why in DESIGNS:
    for lang in ("he", "en"):
        opts += option(num, name, why, lang, TAGS.get(f"{num}-{lang.upper()}", ""))

FIRST_HE = """כל השאילתות והמיקומים, הכותרות לפני ואחרי, ושתי ההמלצות שמחקתי באותו יום שנכתבו:
https://gal.tidhar.org.il/blog/ferry-analytics/

עמוד נמל עם מצלמה חיה: https://croatianferries.com/en/port/merag/
פרק 1, 52 קבוצות פייסבוק בתור באג טראקר: https://gal.tidhar.org.il/blog/ferry-outreach/"""

FIRST_EN = """Every query and position, the titles before and after, and the two recommendations I retracted the same day I wrote them:
https://gal.tidhar.org.il/blog/ferry-analytics/

A port page with a live camera: https://croatianferries.com/en/port/merag/
Episode 1, 52 Facebook groups as a bug tracker: https://gal.tidhar.org.il/blog/ferry-outreach/"""


def pre(id_, text, rtl):
    style = 'direction:rtl;text-align:right;' if rtl else ''
    return (f'<pre id="{id_}" class="term" style="{style}white-space:pre-wrap">{html.escape(text)}</pre>')


BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; croatianferries.com &middot; series post 2</p>
  <h1>Position 5 for a port camera nobody aimed at. Pick the language, the hero, and four lines.</h1>
  <p class="lede">Episode 2, ferry only. The spine is one mechanism taken all the way down: <b>Google told me which
  of my pages work, and they are not the ones I would have chosen</b> - the live port cameras and the pages named
  for one specific pair of ports. Every number is recomputed from today's Search Console snapshot, not from the
  handoff. The GA4 story from the same session is out entirely, because it happened on zazet-solutions and cannot
  carry an episode about the ferry site. Line 1 carries the episode frame, as you asked on post 1, and episode 1 is
  named in the second paragraph and again in the first comment.</p>
</div>

<section class="step">
  <h2>01 &middot; Which language goes on LinkedIn?</h2>
  <p class="q">Same call as episodes 0 and 1.</p>
  <div id="lang" data-persist-choice class="opts small">
    <div class="opt" data-value="he"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Every outlier you have was Hebrew, and this is a builder story with checkable numbers, which is
      what your network engages with. The queries stay in Latin either way - they are what people actually type.</p></div>
    <div class="opt" data-value="en"><div class="opt-head"><span class="dot"></span>
      <b>English</b></div>
      <p class="why">{len(POST_EN):,} characters, under the cap. Reaches Croatian and German readers if reshared, at
      the cost of the reach the ledger measures.</p></div>
    <div class="opt" data-value="both"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew now, English a week later</b></div>
      <p class="why">Two entities, two posts. Worked once before.</p></div>
  </div>
</section>

<section class="step">
  <h2>The post, Hebrew</h2>
  <p class="sub">{len(POST_HE):,} characters (cap 3,000). אמ!לק opener with the episode frame and the camera number in
  line 1, episode 1 named in paragraph 2, the embarrassing baseline, the head terms that are nowhere, the eight
  phrases that rank, the cameras, the truncated titles, and the 16-of-99 discipline.</p>
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
  the Wiz logo itself, not a description of it. Your 25,185 post had no famous name and ran on one measured number.
  Those are the two shapes that have worked, and here they are 5-HE and 1-HE. On episode 1 you took the artifact
  shape over the claim shape for the first time.</p>
  <p class="sub"><b>Which one here.</b> 5-HE, on the same tiebreaker as last time: line 1 already spends "position 5
  at Merag", so the number hero repeats the hook while the sawn-off title adds the thing the text has not reached
  yet. A cold reader seeing a real page title chopped mid-word wants to know whose site that is.</p>
  <p class="sub"><b>The honest risk.</b> 5-HE is a defect in your own product at poster size on your own feed. On the
  launch post you deleted that kind of line yourself. The argument that this is different: it is fixed, the post is
  about finding it, and it is not a launch - but if it reads as a reason not to trust the site, take 1-HE, which is
  not a consolation prize.</p>
  <p class="sub">Click one; your pick saves in this page. The full local path above each image pastes straight into
  LinkedIn's file picker. Match the hero language to decision 01.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>03 &middot; The truncated-titles section</h2>
  <p class="q">278 of 396 of your own pages were broken in search results for two months. It is the strongest
  material in the post and it is also a bug in your own product, which the ledger says you cut.</p>
  <div id="titles" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep as drafted</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The croatian-ferries rule was about a <i>launch</i> post, where an unfixed bug is a reason not to
      click. This is fixed, shipped and tested, and finding it is the payoff of the whole post. Without it the post
      is only "the long tail ranks", which everyone already knows.</p></div>
    <div class="opt" data-value="one-line"><div class="opt-head"><span class="dot"></span>
      <b>Demote to one line</b></div>
      <p class="why">"On the way I found that 278 of 396 port titles were cut off in Google, and fixed it." Keeps the
      number, loses the 87-character example that makes it concrete.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it, blog only</b></div>
      <p class="why">Post ends on the cameras. Cleanest, and about 500 characters shorter, but the post loses its
      second half and its only real defect.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; The one click</h2>
  <p class="q">"One click. 172 impressions. A full month." Fourth consecutive post with a drafted-in embarrassing
  number, and the first three all survived your edit untouched.</p>
  <div id="baseline" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is what makes the rest readable as investigation rather than a success story, and it is the
      one thing in the post a model would not write about itself.</p></div>
    <div class="opt" data-value="soften"><div class="opt-head"><span class="dot"></span>
      <b>Keep the numbers, drop "embarrassing"</b></div>
      <p class="why">Report them flat and let the reader judge.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut the baseline</b></div>
      <p class="why">Go straight to the rankings. Stronger looking, weaker post, and someone will ask.</p></div>
  </div>
</section>

<section class="step">
  <h2>05 &middot; The takeaway line near the end</h2>
  <p class="q">"I stopped trying to rank for Croatia ferries and started building around what already works." On
  episode 1 you rewrote every generalisation back into first person - this one already is first person, but it is
  still the closest thing in the post to advice.</p>
  <div id="takeaway" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep as drafted</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It says what you did, not what the reader should do, and it names the two concrete things: a
      page per named pair, a camera on every port that has one.</p></div>
    <div class="opt" data-value="rewrite"><div class="opt-head"><span class="dot"></span>
      <b>Write it yourself</b></div>
      <p class="why">Your version of this line was the best line in episode 1. If you have one, mine goes.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it</b></div>
      <p class="why">End on the 16-of-99 discipline and the three-to-four weeks. Less tidy, more honest.</p></div>
  </div>
</section>

<section class="step">
  <h2>06 &middot; Episode 3</h2>
  <p class="q">Episode 1 promised the queue camera as the next one, and this post is about cameras in search rather
  than counting cars in the queue. Worth deciding what episode 3 is before someone asks.</p>
  <div id="next" data-persist-choice class="opts small">
    <div class="opt" data-value="queue"><div class="opt-head"><span class="dot"></span>
      <b>The queue camera, computer vision</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Still the strongest unshipped story and the one episode 1 already promised. This post makes the
      case for it: the cameras are the only thing you have that nobody else does, and Google has already noticed.</p></div>
    <div class="opt" data-value="verification"><div class="opt-head"><span class="dot"></span>
      <b>The verification oracle, where the site loses 7 times</b></div>
      <p class="why">Checking yourself against a competitor and publishing the losses.</p></div>
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
    <li><b>Every query and position is read from the snapshot,</b> not from the handoff:
      <code>~/.claude/skills/analytics/ledger/snapshots/2026-09-06.json</code>, GSC 2026-08-07 to 2026-09-03.
      1 click, 172 impressions, CTR 0.58%, average position 20.7. hak merag 5 (2 impressions), hak kamera porozina 8,
      hak kamera brestova 9, gazenica brbinj trajekt 7, domince korcula 8, fähre sumartin makarska fahrplan 9,
      fähre zadar dugi otok fahrplan 11. Head terms: fähre kroatien 49, fähre split supetar 57, dubrovnik to split
      ferry schedule 67.</li>
    <li><b>The title numbers are from the commit, and the tests pass:</b> ferry-watch <code>273a48b</code>, 278 of 396
      over-length down to 6, 16 of 99 ports carry a camera and are resolved against the camera map at build time,
      146 site tests green, deployed to Cloudflare Pages.</li>
    <li><b>Every position here is a tiny sample.</b> hak merag is 2 impressions; most of the rest are 1. The post
      says which pages rank, never how much traffic they bring, because 172 impressions cannot support the second
      claim. This is also why the "position 57" retraction is in the blog: it is the same mistake, made by me,
      three paragraphs earlier in the same run.</li>
    <li><b>No traffic win is claimed anywhere,</b> in the post or the blog. SEO takes three to four weeks; the post
      says so out loud and promises nothing.</li>
    <li><b>The GA4 near-miss is not in this post.</b> It is a zazet-solutions story and an episode about the maritime
      portal cannot carry it. It is also a post about model behaviour, which the ledger flags as the risky genre. It
      keeps until you want a standalone post about it.</li>
    <li><b>The two retractions are in the blog, not the post</b> - the n=1 position and the Cloudflare 301 that the
      redirect file never showed. They are the most useful material for a technical reader and they slow the post
      down.</li>
    <li><b>Still open and named in the blog:</b> 98 of 172 impressions come from Croatia while the /de/ tree is what
      ranks, and www serves a full duplicate at 200 with a canonical mitigating it.</li>
    <li><b>Blog is live at</b> gal.tidhar.org.il/blog/ferry-analytics/ once pushed, with the full query table, both
      retractions, the title before and after, and what is still open. og.png is 5-EN until you pick.</li>
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
doc = doc.replace("<title>Ferry outreach - LinkedIn post", "<title>Ferry analytics - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
