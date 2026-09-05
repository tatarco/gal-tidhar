#!/usr/bin/env python3
"""Build the ZaZet choices doc for the ferry-outreach post."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
DR = pathlib.Path.home() / ".claude/skills/linkedin/drafts"
POST_HE = (DR / "ferry-outreach.txt").read_text(encoding="utf-8").strip()
POST_EN = (DR / "ferry-outreach-en.txt").read_text(encoding="utf-8").strip()
WRAP_SRC = HERE.parent / "croatian-ferries" / "out-choices.html"
WRAP_BODY = HERE.parent / "croatian-ferries" / "choices-body.html"

DESIGNS = [
    ("5", "the hate comment", "RECOMMENDED. 'Do you need an app to cross the road too?' huge in yellow, with the "
     "payoff underneath: the rudest comment was also the most useful one. This is the shape that carried your 133k "
     "post - there the image WAS the subject (the Wiz logo itself), here it IS the artifact (the actual comment). It "
     "is also the only hero of the six that opens a loop on its own: a cold reader has to know who said that and what "
     "you did about it. And it does not duplicate the post, because line 1 already spends the numbers."),
    ("1", "the one big number", "STRONG CONTENDER. 31 minutes, from a stranger correcting my Croatian to the fix "
     "live. This is the cache-economics shape (25,185 impressions with no famous logo, on a measured number). The "
     "cost: line 1 of the post now carries 52 groups and 11 issues, so the number hero says a second number instead "
     "of adding something new, and '31 minutes' needs its subtitle before it means anything."),
    ("2", "the claim", "The bold-claim shape, your most-picked design across the ledger. Carries the whole post in "
     "one line for a cold reader, but it states the conclusion rather than showing the evidence."),
    ("4", "comment to issue", "The five real comments and what each became, with the minutes. The most credible "
     "frame and the most useful, but it is a table, and tables read as reports."),
    ("3", "the exchange", "The real Croatian comment about 'vozni red' next to what shipped 31 minutes later. Your "
     "pick on phase-is-a-function. Teaches the whole mechanism without the post, but needs a second of reading."),
    ("6", "the pipeline", "Sweep -> triage -> reply, with the honest numbers underneath. The frame a technical "
     "reader likes most, and the one that needs the post to land."),
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

FIRST_HE = """התהליך המלא, המספרים, כל התגובות שהפכו לאישיוז, והבאג שדיווח לי על האנגייג'מנט של מישהו אחר בתור שלי:
https://gal.tidhar.org.il/blog/ferry-outreach/

האתר: https://croatianferries.com
איך נקראו 23 קבצי ה-PDF: https://gal.tidhar.org.il/blog/croatian-ferries/"""

FIRST_EN = """The full process, the numbers, every comment that became an issue, and the bug that reported a stranger's engagement as mine:
https://gal.tidhar.org.il/blog/ferry-outreach/

The site: https://croatianferries.com
How the 23 PDFs were read: https://gal.tidhar.org.il/blog/croatian-ferries/"""


def pre(id_, text, rtl):
    style = 'direction:rtl;text-align:right;' if rtl else ''
    return (f'<pre id="{id_}" class="term" style="{style}white-space:pre-wrap">{html.escape(text)}</pre>')


BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; croatianferries.com &middot; series post 1</p>
  <h1>52 Facebook groups, 153 comments, and 11 issues opened by strangers. Pick the language, the hero, and four lines.</h1>
  <p class="lede">You asked for the outreach post: lots of numbers, the scripts, comments as issues to fix, and some
  hate comments. All four are in. The spine is one mechanism taken all the way down - <b>the comments are the bug
  tracker</b> - and the numbers are the honest version, including the 15 posts that cannot be measured at all. Every
  quote in the post is real and lifted verbatim from <code>seen.json</code>; every minutes figure is the real gap
  between the GitHub issue opening and closing. The measurement bug is deliberately NOT in the post (it is a bug in
  your own tooling on a post about your own product, which the ledger says you cut) - it is the long section in the
  blog instead.</p>
</div>

<section class="step">
  <h2>01 &middot; Which language goes on LinkedIn?</h2>
  <p class="q">Same call as the launch post. Your reach is Israeli tech and every outlier was Hebrew, but the
  Croatian comments are the texture and they stay in Croatian either way.</p>
  <div id="lang" data-persist-choice class="opts small">
    <div class="opt" data-value="he"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The audience that actually sees your posts, and this is a builder-and-distribution story, which
      is exactly what your network engages with. The Croatian quotes stay untranslated-then-translated inline, which
      is part of the texture.</p></div>
    <div class="opt" data-value="en"><div class="opt-head"><span class="dot"></span>
      <b>English</b></div>
      <p class="why">Trimmed to 2,990 characters to fit LinkedIn's cap - one hate quote and the Filip bullet are out.
      Reaches Croatian readers if reshared, at the cost of the reach the ledger shows.</p></div>
    <div class="opt" data-value="both"><div class="opt-head"><span class="dot"></span>
      <b>Hebrew now, English a week later</b></div>
      <p class="why">Two posts, two entities. Worked once before.</p></div>
  </div>
</section>

<section class="step">
  <h2>The post, Hebrew</h2>
  <p class="sub">{len(POST_HE):,} characters (cap 3,000). אמ!לק opener with the number in line 1, the honest numbers
  block, five real comments with the minutes, the hate block, the paragraph where you delete your own rebuttal, and
  the small-beats-big payoff.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-he">Copy Hebrew post</button></div>
  {pre("post-he", POST_HE, True)}
</section>

<section class="step">
  <h2>The post, English</h2>
  <p class="sub">{len(POST_EN):,} characters, trimmed to clear the cap.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-en">Copy English post</button></div>
  {pre("post-en", POST_EN, False)}
</section>

<section class="step">
  <h2>02 &middot; Hero image - pick one</h2>
  <p class="sub">You shortlisted <b>5-HE</b> (the hate comment) and <b>1-HE</b> (the 31 minutes), so those two are
  first. Both map onto a shape that has already worked for you, which is why it is a real question and not an obvious
  one.</p>
  <p class="sub"><b>What your own numbers say.</b> Your 133,171-impression post carried a single image that WAS its
  subject - the Wiz logo, the actual thing being discussed, not a description of it. Your 25,185 post had no famous
  name at all and ran on one measured number a reader could check against their own account. So the feed has rewarded
  you twice, for two different images: <i>the artifact</i>, and <i>the number</i>. That is exactly 5-HE versus 1-HE.</p>
  <p class="sub"><b>Which one here.</b> I would take 5-HE, on one tiebreaker: line 1 of the post now opens with the
  episode frame and both numbers, so the number hero repeats the hook while the quote hero adds the one thing the
  text has not spent yet. A cold reader seeing "do you need an app to cross the road too?" has to find out who said
  it. A cold reader seeing "31 minutes" has to read the subtitle before it means anything. The Wiz post did not
  explain the logo either - it showed it.</p>
  <p class="sub"><b>The honest risk.</b> 5-HE puts a stranger insulting your work at the top of your own feed, at
  poster size, with no context until someone reads on. If that is not a trade you want, 1-HE is not a consolation
  prize - it is the shape of your number-two post of all time.</p>
  <p class="sub">Click one; your pick saves in this page. The full local path above each image pastes straight into
  LinkedIn's file picker. Match the hero language to decision 01.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>03 &middot; The hate-comment block</h2>
  <p class="q">Four real quotes, verbatim, including one calling the site pointless. This is the part you asked for
  and it is also the part that puts insults about your work on your own feed.</p>
  <div id="hate" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep all four</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Quoting someone dismissing your work, and then agreeing he was useful, is the least fakeable
      thing in the post. Nobody launching a product does this.</p></div>
    <div class="opt" data-value="two"><div class="opt-head"><span class="dot"></span>
      <b>Keep two</b></div>
      <p class="why">The road one and the app one. Shorter, same point, less pile-on.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut the block</b></div>
      <p class="why">Go straight from the fixes to the small-groups payoff. Loses the best paragraph in the post
      (the deleted rebuttal), which depends on it.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; The paragraph where you delete your own rebuttal</h2>
  <p class="q">"I sat and wrote him a long reasoned reply about what he had missed and how bad the site he was
  recommending is, and I deleted all of it." This is the undefended line - you losing your temper at a stranger and
  then not sending it.</p>
  <div id="rebuttal" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep as drafted</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Fourth consecutive post where the drafted embarrassing line is the one you keep.</p></div>
    <div class="opt" data-value="hotter"><div class="opt-head"><span class="dot"></span>
      <b>Write it hotter yourself</b></div>
      <p class="why">If the real feeling was angrier than this, write that paragraph in raw. It always beats mine.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it</b></div>
      <p class="why">Straight from the quotes to "he told you where the bar is". Cleaner and flatter.</p></div>
  </div>
</section>

<section class="step">
  <h2>05 &middot; The series frame</h2>
  <p class="q">Last line currently says "post 1 in a series on turning a small site into the best maritime portal in
  Croatia". Committing publicly to a series is a commitment to ship the next ones.</p>
  <div id="series" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep the series line</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">The freelance series worked with the same device. Proposed run: 2. the queue camera (computer
      vision on the HAK cameras, the thing this actually started from) &middot; 3. the verification oracle, where the
      site is checked against a competitor and loses 7 times &middot; 4. the 64-line state register and why operators
      are hand-kept &middot; 5. four languages and what the German and Italian reviewers changed.</p></div>
    <div class="opt" data-value="tease"><div class="opt-head"><span class="dot"></span>
      <b>Name post 2 specifically</b></div>
      <p class="why">e.g. "the next one is about counting cars in the queue from a traffic camera". A concrete tease
      beats an abstract series promise, but it locks the order.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>No series line</b></div>
      <p class="why">Post stands alone, no commitment.</p></div>
  </div>
</section>

<section class="step">
  <h2>06 &middot; The 6 groups holding your post for admin approval</h2>
  <p class="q">Your open question from the handoff. It affects the post only if you want a different last word on
  it, but it is a real operational call and it is the next batch's strategy.</p>
  <div id="moderators" data-persist-choice class="opts small">
    <div class="opt" data-value="write-off"><div class="opt-head"><span class="dot"></span>
      <b>Write them off, post the 10 planned groups instead</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">A cold DM to a volunteer moderator is low-yield, and the data says those big groups underperform
      the small ones even when they do approve. The 10 groups sitting at <code>planned</code> in outreach.json cost
      you nothing and target the shape that actually works.</p></div>
    <div class="opt" data-value="chase"><div class="opt-head"><span class="dot"></span>
      <b>Chase all 6</b></div>
      <p class="why">One polite DM each, in Croatian, offering the site as a free resource. Costs an hour. If two
      approve you get a big-group data point you currently do not have.</p></div>
    <div class="opt" data-value="chase-two"><div class="opt-head"><span class="dot"></span>
      <b>Chase the two biggest only</b></div>
      <p class="why">Cheapest test of whether the moderation wall is worth pushing on at all.</p></div>
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
    <li><b>Every number recomputed from the repo today,</b> not from the handoff. <code>ops/fb/metrics.json</code>:
      52 posts, 37 anchored reads totalling 1,211 likes / 153 comments / 39 shares, 8 of those 37 at zero likes,
      6 <code>pending admin approval</code>, 4 <code>unreadable</code>, 5 stale unanchored entries. The post says
      "15 I cannot measure" (6 + 9), which is the defensible grouping - the handoff's "42 measured / 13 at zero"
      predates the anchor fix and I did not reuse it.</li>
    <li><b>Every comment is verbatim from <code>seen.json</code></b> and every fix is a real closed issue:
      #11 plovidbeni red (31 min), #14 the 6.9 validity (34 min), #13 Stinica - Mišnjak (58 min), #3 the Prizna
      camera, #12 operator coverage. The minutes are createdAt to closedAt from the GitHub API.</li>
    <li><b>The hate quotes are real and unedited,</b> from Andrej, Krešimir, Martina and Darko. First names only in
      the post for the helpful ones; the critical ones are quoted without any name at all, so nobody gets pointed at
      on your feed.</li>
    <li><b>The measurement bug is in the blog, not the post.</b> Ledger rule from croatian-ferries: a bug in your own
      thing on a post about your own thing reads as a reason not to trust it. The blog carries the full five-guard
      table and the "never write an unanchored reading" rule, which is the strongest technical material in the
      session.</li>
    <li><b>Privacy pass:</b> no full names of critics, no group member counts that identify a specific group as the
      one that ignored you, no personal circumstances anywhere. The helpful commenters are first-name-only and are
      being credited, publicly, for a public comment.</li>
    <li><b>The LinkedIn skill bundle you remembered from /ideas</b> is idea-backlog #230, and I identified the repo:
      <code>sergebulaev/linkedin-skills</code>, 11 skills - post writer with 20 hook formulas, comment drafter, reply
      handler, post audit, humanizer, hook extractor, content planner, engagement monitor, profile optimizer,
      employee advocacy, repurposer. <b>It has nothing on hero design.</b> Its only visual guidance is a paid
      illustration API (Pixfaro) that composites your handle and brand colour onto a generated image, plus one idea
      worth noting: a "quote-card of your hook", which is precisely what 5-HE is. The hook-formula library and the
      humanizer are worth mining into /linkedin separately; neither helps this decision. Your own two outliers are
      much stronger evidence than that repo, which is what decision 02 is argued from.</li>
    <li><b>Known weakness:</b> no famous company in line 1. The checkable things are 52 groups and 11 of 25 issues.
      Facebook is the only recognizable name available and it is not a scroll-stop on its own.</li>
    <li><b>Blog is live at</b> gal.tidhar.org.il/blog/ferry-outreach/ once pushed, with the machinery table, the full
      comment-to-issue table, the competitor map, and the measurement bug. og.png is 2-EN until you pick.</li>
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
doc = doc.replace("<title>Croatian ferries - LinkedIn post", "<title>Ferry outreach - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
