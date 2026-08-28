#!/usr/bin/env python3
"""Build the ZaZet choices doc for the whatsapp-presence post."""
import base64, html, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/whatsapp-presence.txt"
WRAP_SRC = HERE.parent / "finance-audit-beta" / "out-choices.html"
WRAP_BODY = HERE.parent / "finance-audit-beta" / "choices-body.html"

DESIGNS = [
    ("2", "the claim", "RECOMMENDED. The bold-claim shape, your most-picked: וואטסאפ הפסיק להתריע "
     "לי / הבעיה לא היתה בוואטסאפ. Names the recognizable thing in the frame and opens the loop in "
     "six words. Everything else in the post is the answer to it."),
    ("3", "the exchange", "STRONG CONTENDER. Calls rang / messages did not - the two-cell contrast, "
     "which is the shape you broke the streak for on pricing-the-phase. This story IS a contrast, "
     "and this frame is also the actual diagnostic clue, so the image teaches something on its own."),
    ("8", "the claim + the fix", "The claim that I found it and shipped the fix upstream, with the "
     "one-line guard / regression test / 410 tests pills, and שקט → התראות underneath. The most "
     "'I did the work' frame, but it sells the ending rather than the mystery."),
    ("1", "the one big number", "שורה אחת - one line of my own code stopped my phone from ever "
     "notifying me. Closest thing here to a measured number, which is what carried cache-economics "
     "to 25k with no famous logo."),
    ("5", "the payoff quote", "שיחות צלצלו. הודעות לא. The whole diagnosis in four words, huge. "
     "The most screenshot-able frame, and the one a reader can act on without reading the post."),
    ("4", "what I checked", "The dead-end grid: every iOS setting, focus modes, reset, reinstall - "
     "and then my own bridge. The lived sequence as a frame, which is the shape you rewrite my "
     "drafts INTO. Weakness: it is a list, and lists read as reports."),
    ("6", "the three-link chain", "The comparison misfires / the attribute is dropped / bare means "
     "online. The actual mechanism, and the most useful frame for a technical reader - but it needs "
     "the post to make sense, so it is a weak scroll-stop."),
]

post = POST.read_text(encoding="utf-8").strip()
chars = len(post)


def img(num, lang):
    p = HERE / f"hero-{num}-{lang}.png"
    if not p.exists():
        return ""
    prev = HERE / f".preview-{num}-{lang}.jpg"
    if not prev.exists():
        subprocess.run(["sips", "-Z", "1000", "-s", "format", "jpeg", "-s", "formatOptions", "72",
                        str(p), "--out", str(prev)], check=True, capture_output=True)
    b64 = base64.b64encode(prev.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code> <b>{num}-{lang.upper()}</b></p>'
            f'<img src="data:image/jpeg;base64,{b64}" alt="hero {num} {lang}">')


def option(num, name, why, lang, tag=""):
    code = f"{num}-{lang.upper()}"
    im = img(num, lang)
    if not im:
        return ""
    t = f' <span class="rec">{tag}</span>' if tag else ""
    return (f'<div class="opt" data-value="{code}">'
            f'<div class="opt-head"><span class="dot"></span>'
            f'<b>{code}</b> &middot; {html.escape(name)}{t}</div>'
            f'<p class="why">{html.escape(why)}</p>{im}</div>')


TAGS = {"2-HE": "RECOMMENDED", "3-HE": "CONTENDER", "5-HE": "MOST SCREENSHOT-ABLE"}
opts = ""
for num, name, why in DESIGNS:
    for lang in ("en", "he"):
        opts += option(num, name, why, lang, TAGS.get(f"{num}-{lang.upper()}", ""))

FIRST_COMMENT = """הסיפור המלא - כל הדד־אנדים, שרשרת שלושת השלבים שגורמת לזה, והתיקון:
https://gal.tidhar.org.il/blog/whatsapp-presence/

הPR שפתחתי (שורת הגנה אחת + טסט רגרסיה, 410 טסטים עוברים):
https://github.com/WhiskeySockets/Baileys/pull/2789

הissue המקורי, פתוח מ־12 במאי:
https://github.com/WhiskeySockets/Baileys/issues/2553

מי שרוצה לתקן אצלו עכשיו בלי לחכות למרג׳ - זה עוקף את הבאג דרך ה־API הפומבי בלבד, בלי לגעת בnode_modules:

const _emit = sock.ev.emit.bind(sock.ev)
sock.ev.emit = (event, data) => {
  if (event === 'creds.update' && data && data.me === undefined && state.creds?.me) {
    return _emit(event, { ...data, me: state.creds.me })
  }
  return _emit(event, data)
}

ואם וואטסאפ שקט אצלכם ואין לכם שום בריידג׳ - תבדקו קודם Linked Devices ותנתקו כל דבר שאתם לא זוכרים."""

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn &middot; the silent WhatsApp</p>
  <h1>WhatsApp went silent for two weeks. The bug was mine. Pick the hero, settle three calls.</h1>
  <p class="lede">Hebrew post for the Israeli side. Line 1 names וואטסאפ - the most recognizable
  thing you could put there - and opens the loop immediately by taking it away again: the problem
  was not WhatsApp. The spine is one mechanism all the way down: a linked device that reports you
  online tells WhatsApp not to push, calls ride a separate path that ignores presence, and that
  asymmetry is the entire diagnosis. The ending is not "I found a bad default" - it is that you
  traced it to a three-step chain in the library and shipped the fix upstream with the regression
  test the earlier attempt was missing.</p>
</div>

<section class="step">
  <h2>The post</h2>
  <p class="sub">{chars:,} characters (cap 3,000). Hebrew, אמ!לק opener, וואטסאפ in line 1, the
  dead-end sequence in the order you actually walked it, and it closes on a usable tip plus the
  first-comment pointer.</p>
  <div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
  <pre id="post-text" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(post)}</pre>
</section>

<section class="step">
  <h2>01 &middot; Hero image - pick one</h2>
  <p class="sub">Seven designs, English and Hebrew. Click one; your pick saves in this page. The full
  local path above each image pastes straight into LinkedIn's file picker.</p>
  <div id="hero" data-persist-choice class="opts">{opts}</div>
</section>

<section class="step">
  <h2>02 &middot; The angry paragraph</h2>
  <p class="q">Paragraph four is the unpunctuated one about the two weeks - sending yourself a
  message and watching nothing happen, not knowing if you are stupid or the phone is broken, missing
  messages from clients and from your wife. I drafted it in deliberately, per the fleeceware
  lesson. It is the one paragraph a model should not be writing for you.</p>
  <div id="raw-para" data-persist-choice class="opts small">
    <div class="opt" data-value="rewrite"><div class="opt-head"><span class="dot"></span>
      <b>You rewrite it in your own words</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Mine is a guess at your anger. On fleeceware you wrote your own and it was the
      best thing in the post. Two minutes, badly punctuated, exactly as it felt.</p></div>
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep it as drafted</b></div>
      <p class="why">On finance-audit-beta you left my version intact, so this is not automatic.
      If it already sounds like you, leave it.</p></div>
    <div class="opt" data-value="cut"><div class="opt-head"><span class="dot"></span>
      <b>Cut it</b></div>
      <p class="why">Shortest version. Costs the post its only emotional beat, and this story is
      mostly mechanism otherwise.</p></div>
  </div>
</section>

<section class="step">
  <h2>03 &middot; The wife line</h2>
  <p class="q">The angry paragraph says you missed messages "מלקוחות ומאשתי". Per the privacy rule
  the relationship stays and the circumstances go, and nothing here is a circumstance - but it does
  put a real person into a post about your phone being broken.</p>
  <div id="wife-line" data-persist-choice class="opts small">
    <div class="opt" data-value="keep"><div class="opt-head"><span class="dot"></span>
      <b>Keep "מלקוחות ומאשתי"</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">It is the line that makes the stakes real rather than technical, and it says
      nothing about her. Flattening it to "מכולם" is exactly the anonymising you push back on.</p></div>
    <div class="opt" data-value="clients-only"><div class="opt-head"><span class="dot"></span>
      <b>Clients only</b></div>
      <p class="why">Keeps the business stakes, drops the family entirely.</p></div>
  </div>
</section>

<section class="step">
  <h2>04 &middot; The close</h2>
  <p class="q">Drafted as a usable tip (check Linked Devices) plus the first-comment pointer, no
  question. The tip is the gift - it is the one thing a reader with the same symptom can act on
  without any of your infrastructure.</p>
  <div id="closing" data-persist-choice class="opts small">
    <div class="opt" data-value="tip-only"><div class="opt-head"><span class="dot"></span>
      <b>Tip + pointer (as drafted)</b> <span class="rec">RECOMMENDED</span></div>
      <p class="why">Ends on something useful to a stranger, which is what separated your top posts
      from the ones that asked for something.</p></div>
    <div class="opt" data-value="add-question"><div class="opt-head"><span class="dot"></span>
      <b>Add one short question</b></div>
      <p class="why">e.g. מה הבאג הכי מטופש שחיפשתם שבועיים והיה אצלכם בקוד? Plain, and the answers
      would be genuinely good reading.</p></div>
  </div>
</section>

<section class="step">
  <h2>The first comment - ready to paste</h2>
  <div class="copybar"><button class="copybtn" data-copy="first-comment">Copy first comment</button></div>
  <pre id="first-comment" class="term" style="direction:rtl;text-align:right;white-space:pre-wrap"
    >{html.escape(FIRST_COMMENT)}</pre>
</section>

<section class="step">
  <h2>Honest notes, and what I checked</h2>
  <ul>
    <li><b>The original angle did not survive verification.</b> You asked for "this feature should be
      off by default, it doesn't help at all". Baileys documents it explicitly in the README -
      "If you want to receive notifications in whatsapp app, set markOnlineOnConnect to false" - so
      the hidden-footgun framing was not available. What replaced it is stronger and it is the
      truth: the flag alone does not actually work, because of a separate bug.</li>
    <li><b>Everything technical in the post was verified in source this run,</b> not recalled:
      <code>Defaults/index.js:62</code> (the default is true), <code>Socket/chats.js:1065</code>
      (sends 'available' on connect), <code>socket.ts:1054</code> (the comparison misfires on a
      partial update), <code>encode.ts:226</code> (undefined attributes are stripped),
      <code>chats.ts:885</code> (a typeless presence node reads as available). Present in both your
      installed 7.0.0-rc14 and current master.</li>
    <li><b>The PR is real and open:</b> <code>WhiskeySockets/Baileys#2789</code>. One-line guard plus
      a three-case regression test. Verified the test fails on master before it passes with the fix
      (1 failed / 2 passed, then 3 passed). Full suite 410 tests / 29 suites. tsc, eslint and
      prettier all clean. All three CI checks green.</li>
    <li><b>The "closed by a stale bot" claim is checked.</b> #2627 proposed the identical guard and
      was closed 21 Jul with state_reason <code>completed</code>, with nothing changed - master still
      carried the code when I forked it today. Worth keeping in the post because it is the reason
      the test matters, but it is a mild swipe at a maintainer's automation, so say the word and I
      will soften it to "נסגר בלי שטופל".</li>
    <li><b>Your machine is already fixed</b> and does not depend on the merge - the shim lives in
      <code>wa.js</code>, not in node_modules, so it survives reinstalls and re-pairing.</li>
    <li><b>Not in the post, in the blog:</b> the full three-step chain with file and line numbers,
      the local workaround snippet, the note that the repo's own <code>mockWebSocket()</code> helper
      is a no-op under ESM because <code>jest.mock</code> inside a function body is not hoisted, and
      the "what I would not do again" list.</li>
    <li><b>Privacy pass:</b> no phone numbers, no chat contents, no contact names anywhere in the
      post, the heroes, the blog or the page metadata. The bridge is described as a read-only
      WhatsApp bridge with no detail about what it feeds. Your wife appears only as "אשתי" with no
      circumstances (decision 03).</li>
    <li><b>Known weakness, flagged rather than hidden:</b> there is no big checkable number here.
      Cache-economics reached 25k on a number the reader could verify on their own account; this
      post's proof is a story plus a link to a PR. What carries it is the diagnostic tip - calls
      ring, messages do not, look at Linked Devices - which is genuinely useful to anyone with the
      same symptom, and there are a lot of them.</li>
    <li><b>On your hero pick</b> I set og.png to its EN twin, commit and push the blog, and the
      first-comment links go live.</li>
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
                  "<title>WhatsApp went silent - LinkedIn post")
(HERE / "out-choices.html").write_text(doc, encoding="utf-8")
(HERE / "choices-body.html").write_text(BODY, encoding="utf-8")
print("wrote out-choices.html", len(doc), "bytes")
