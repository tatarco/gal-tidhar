#!/usr/bin/env python3
"""Build the ZaZet choices doc for the agent-identity post: post text with a copy
button, all 12 heroes inline with their local paths, and persisted click-choices."""
import base64, html, pathlib

HERE = pathlib.Path(__file__).parent
POST = pathlib.Path.home() / ".claude/skills/linkedin/drafts/agent-identity.txt"
COMMENT = HERE / "comment-he.txt"

DESIGNS = [
    ("7", "the 404 (the pain)", "Ask for the client's repo, get 404 - because the space loaded a "
     "random profile. The failure everyone has had and misread as a broken link."),
    ("8", "NOT FOUND", "The same pain as one word, plus the reason it fools you: a private "
     "resource does not say wrong account, it says the thing is not there."),
    ("2", "the claim", "The sentence as the whole image. This shape won on the last ego-lite post."),
    ("3", "the dropped option", "The real artifact: the call that was accepted and ignored, in red."),
    ("1", "the exchange", "Before / after: what decided the identity, and what decides it now."),
    ("4", "the architecture", "Project -> task space -> client profile."),
    ("5", "the grid", "The four things the guard enforces."),
    ("6", "one big number", "1 email per project."),
]
REC = "7"


def img(name):
    b = base64.b64encode((HERE / name).read_bytes()).decode()
    return f"data:image/png;base64,{b}"


shots = []
for n, title, why in DESIGNS:
    rec = '<span class="rec">RECOMMENDED</span>' if n == REC else ""
    blocks = []
    for lang in ("en", "he"):
        f = f"hero-{n}-{lang}.png"
        blocks.append(
            f'<div class="shot"><div class="pathline"><b>{n}-{lang.upper()}</b> '
            f'<code>{HERE / f}</code></div>'
            f'<img src="{img(f)}" alt="hero {n} {lang}"></div>')
    shots.append(f'<div class="design"><h3>{n} - {title}{rec}</h3>'
                 f'<p class="why">{why}</p>{"".join(blocks)}</div>')

picker = "".join(f'<span data-value="{n}-{l}">{n}-{l.upper()}</span>'
                 for n, _, _ in DESIGNS for l in ("en", "he"))

post = html.escape(POST.read_text().strip())
comment = html.escape(COMMENT.read_text().strip())

DOC = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LinkedIn post - my agent cannot browse as me</title>
<style>
:root{{--paper:#F0F7FC;--ink:#0A1628;--royal:#012169;--muted:#4a5e78;--line:#0A1628}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);
 font-family:system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.65;font-size:16px}}
.wrap{{max-width:900px;margin:0 auto;padding:48px 24px 80px}}
.mark{{font-weight:800;letter-spacing:.04em;font-size:20px;border-bottom:2px solid var(--line);
 padding-bottom:10px;margin-bottom:34px}}
h1{{font-size:clamp(26px,4.4vw,38px);line-height:1.18;margin:0 0 10px;letter-spacing:-.015em}}
.lede{{color:var(--muted);font-size:17px;margin:0 0 12px;max-width:64ch}}
h2{{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--royal);
 margin:52px 0 14px;display:flex;align-items:center;gap:12px}}
h2::after{{content:'';flex:1;height:1px;background:rgba(10,22,40,.18)}}
h3{{font-size:17px;margin:26px 0 4px}}
.why{{color:var(--muted);font-size:14px;margin:0 0 14px;max-width:62ch}}
.rec{{background:var(--royal);color:#fff;font-size:10px;letter-spacing:.1em;padding:3px 8px;
 vertical-align:middle;margin-inline-start:8px}}
.copybar{{display:flex;justify-content:flex-end;margin-bottom:8px}}
.copybtn{{background:var(--ink);color:#fff;border:0;padding:10px 20px;font:inherit;font-size:14px;
 font-weight:600;cursor:pointer;letter-spacing:.02em}}
.copybtn:hover{{background:var(--royal)}}
pre.term{{direction:rtl;text-align:right;white-space:pre-wrap;word-wrap:break-word;
 background:#fff;border:1px solid rgba(10,22,40,.18);padding:24px 26px;font:inherit;font-size:15.5px;
 line-height:1.75;margin:0;max-height:560px;overflow:auto}}
.shot{{margin:16px 0 22px}}
.pathline{{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--muted);margin-bottom:6px;
 word-break:break-all}}
.pathline b{{color:var(--royal)}}
.pathline code{{user-select:all}}
.shot img{{width:100%;display:block;border:1px solid rgba(10,22,40,.2)}}
.picker{{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 8px}}
.picker span{{border:1.5px solid rgba(10,22,40,.28);padding:9px 18px;cursor:pointer;font-size:14px;
 user-select:none;display:flex;align-items:center;gap:9px;background:#fff}}
.picker span::before{{content:'';width:12px;height:12px;border-radius:50%;
 border:1.5px solid rgba(10,22,40,.4);flex:none}}
.picker span:hover{{border-color:var(--royal)}}
.picker span.chosen{{border-color:var(--royal);border-width:2px;background:#fff;font-weight:700}}
.picker span.chosen::before{{background:var(--royal);border-color:var(--royal);
 box-shadow:inset 0 0 0 2.5px #fff}}
.picker span.chosen::after{{content:'CHOSEN';font-size:9.5px;letter-spacing:.1em;color:#fff;
 background:var(--royal);padding:2px 6px}}
.design{{border-top:1px solid rgba(10,22,40,.14);padding-top:22px;margin-top:30px}}
.note{{border-inline-start:3px solid var(--royal);background:rgba(1,33,105,.05);
 padding:14px 18px;margin:14px 0;font-size:15px}}
ul{{max-width:64ch}} li{{margin-bottom:6px}}
code{{font-family:ui-monospace,Menlo,monospace;font-size:.9em}}
.foot{{margin-top:60px;padding-top:18px;border-top:2px solid var(--line);font-size:13px;color:var(--muted)}}
</style></head><body><div class="wrap">
<div class="mark">ZaZet</div>

<h1>The post: my agent cannot browse as me</h1>
<p class="lede">Hebrew post, one single image, blog link in the first comment. Below: the copy,
the heroes to pick from, and three decisions. Click your picks - they save into the page, no
codes to type back at me.</p>

<div class="note"><b>Why this one is worth posting.</b> It is the sequel to your #3 all-time post
(ego lite, 16.6k impressions), it names a real bug with a receipt, and it converts your freelance
practice - one internal email per client - into a rule other people can copy. The employee angle
(cinema tickets vs QA-ing the app you are paid to build) widens it past freelancers.</div>

<h2>01 - The post text</h2>
<p class="why">Hebrew, 3 beats: the practice (internal email), the hole (browser identity decided
by the active tab), the fix. Ends on a short question, then the first-comment pointer.</p>
<script src="/copy.js"></script>
<div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
<pre id="post-text" class="term">{post}</pre>

<h2>01b - The first comment (paste right after posting)</h2>
<p class="why">The links never go in the body - LinkedIn suppresses reach on posts with an
external link. The post ends on the pointer, and this goes in as the first comment: blog, repo,
part one.</p>
<div class="copybar"><button class="copybtn" data-copy="comment-text">Copy first comment</button></div>
<pre id="comment-text" class="term">{comment}</pre>

<h2>02 - Pick the hero</h2>
<p class="why">Six designs, each in English and Hebrew. Hebrew post wants a Hebrew hero.
<b>Every hero now names ego lite</b> - amber brandmark top of frame, the browser named again in
the body line, and the version in the footer - so a cold reader knows this is a fix for that
specific browser and not a generic take on agent identity.
My recommendation is now <b>7-HE</b>: the pain itself, in the reader's own words - "open the
client's repo" and back comes <b>404</b>, because the task space was born on a random profile.
That is the moment people have already lived and misread as a broken link or a dead session.
<b>8-HE</b> is the same idea compressed to one word. <b>2-HE</b> (the claim) is still there as the
shape you picked last time, if you would rather lead with the fix than the pain.</p>
<div id="hero" data-persist-choice class="picker">{picker}</div>
{"".join(shots)}

<h2>03 - The repo (built, waiting to be pushed)</h2>
<p class="why">You asked for something people can pick up and use, not a nail-biter. It is built
and anonymized: <code>~/PycharmProjects/ego-profile-guard/</code> - README with the problem, the
trap and honest limitations, both hooks, an idempotent <code>install.sh</code> (verified), example
files, MIT. No client name, no real address, no project of yours in it. It cannot be pushed from
the Kollate session (gh there is locked to the client account), so it goes up from a session
outside that directory, as <b>tatarco</b>.</p>
<div id="repo" data-persist-choice class="picker">
  <span data-value="repo-push">Push it as tatarco, link it in the post<span class="rec">RECOMMENDED</span></span>
  <span data-value="repo-hold">Hold the repo, blog post only</span>
</div>
<p class="why">If you push it, I add the repo link to the blog post and to the first comment
alongside the blog link.</p>

<h2>04 - How hard to name the tool</h2>
<p class="why">The post currently says the bug plainly and links the upstream issue. The softer
version keeps the mechanism and drops the "accepted and ignored" framing. I would keep it hard -
it is accurate, it is documented in their own source, and the maintainers have an open issue
saying the API is planned. Your call, since you are also about to open a PR there.</p>
<div id="tone" data-persist-choice class="picker">
  <span data-value="tone-hard">Keep it as written<span class="rec">RECOMMENDED</span></span>
  <span data-value="tone-soft">Soften the bug section</span>
</div>

<h2>Publishing status - one thing is blocked</h2>
<p class="why">The blog post is written, committed and anonymized, and the repo is complete on
disk. Neither is live yet: this session runs inside the Kollate project, where git and gh are
pinned to the client account, so pushing to your <b>tatarco</b> repos returns 403. That is your
own guard doing its job. Both go up from a session outside that directory - the blog is a
<code>git push</code> of a commit that already exists, the repo is a
<code>gh repo create</code> plus a first push.</p>
<p class="why"><b>Do not post the LinkedIn post before those two are live</b> - the first comment
links to both.</p>

<h2>What I removed</h2>
<ul>
  <li>The client's name and the real internal email. A skeptic pass caught the first blog draft
      pasting the real resolver output - your client's provisioned address, a second business
      address of yours, and a third person's email. All four are now generic placeholders.</li>
  <li>The two specific profile numbers in the "I guessed the mapping and got it wrong" story.
      The point survives without mapping your real accounts to real slots.</li>
  <li>Nothing was removed from the Hebrew post - it never carried an address or a profile id.</li>
</ul>

<h2>Where things are</h2>
<ul>
  <li>Blog post: <code>~/PycharmProjects/gal-tidhar/blog/agent-identity/</code> (live once pushed)</li>
  <li>Heroes: <code>{HERE}/hero-&lt;n&gt;-&lt;lang&gt;.png</code></li>
  <li>The guard + resolver: <code>~/.claude/hooks/ego-profile-guard.py</code>,
      <code>~/.claude/hooks/ego-resolve-profile.sh</code></li>
  <li>Upstream: <a href="https://github.com/citrolabs/ego-lite/issues/176">citrolabs/ego-lite#176</a>,
      PR brief at <code>~/ego-lite-pr-brief.md</code></li>
</ul>

<div class="foot">ZaZet Solutions - post prep, 2026-08-11. Pick a hero and answer 03 and 04, and I
will finish the blog post, set og.png to match, push, and hand you the live URL.</div>
<script src="/persist.js"></script>
</div></body></html>"""

out = HERE / "choices-doc.html"
out.write_text(DOC)
print(out, f"{out.stat().st_size/1024/1024:.1f} MB")
