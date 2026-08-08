#!/usr/bin/env python3
"""Build the ZaZet choices doc for the cmux post.

Copy button is wired via the portal's /copy.js (the doc CSP is script-src 'self',
so an inline onclick would silently never fire). Choices persist via /persist.js.
"""
import base64, html, pathlib

HERE = pathlib.Path(__file__).parent
ABS = str(HERE)
POST = (HERE / "post-he.txt").read_text(encoding="utf-8")
COMMENT = (HERE / "comment-he.txt").read_text(encoding="utf-8")

DESIGNS = [
    ("1", "The one big number", "26, with the workspace count under it and three chips."),
    ("2", "The claim as one huge sentence",
     "His proven winner shape - 133k / 37k / 16.6k were all this. RECOMMENDED."),
    ("3", "The before/after", "The same notification in a normal terminal vs in cmux."),
    ("4", "The mechanism", "The file-managed config bar: uncommented key vs commented out."),
    ("5", "The three real deviations", "The settings list, all three turning something off."),
    ("6", "Mine vs the schema default", "The receipts table, with the one real deviation lit up."),
    ("7", "The memory ledger",
     "26 agents at 3-4 GB, cmux at 0.82, and PyCharm not running since 11 June. The new angle."),
]


def img(n, lang):
    p = HERE / ".preview" / f"hero-{n}-{lang}.png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    full = f"{ABS}/hero-{n}-{lang}.png"
    return (f'<div class="shot"><div class="pathline"><b>{n}-{lang.upper()}</b> &nbsp; '
            f'<code>{full}</code></div>'
            f'<img src="data:image/png;base64,{b64}" alt="hero {n} {lang}"></div>')


def picker(pid, options):
    opts = "".join(f'<span data-value="{html.escape(v)}">{t}</span>' for v, t in options)
    return f'<div class="picker" id="{pid}" data-persist-choice>{opts}</div>'


CSS = """
:root{--paper:#F0F7FC;--ink:#0A1628;--royal:#012169;--muted:#4a5e78;--line:#0A1628}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font-family:system-ui,-apple-system,'Segoe UI',sans-serif;line-height:1.65;font-size:16px}
.wrap{max-width:900px;margin:0 auto;padding:48px 24px 80px}
.mark{font-weight:800;letter-spacing:.04em;font-size:20px;border-bottom:2px solid var(--line);
 padding-bottom:10px;margin-bottom:34px}
h1{font-size:clamp(26px,4.4vw,38px);line-height:1.18;margin:0 0 10px;letter-spacing:-.015em}
.lede{color:var(--muted);font-size:17px;margin:0 0 12px;max-width:64ch}
h2{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--royal);
 margin:52px 0 14px;display:flex;align-items:center;gap:12px}
h2::after{content:'';flex:1;height:1px;background:rgba(10,22,40,.18)}
h3{font-size:17px;margin:26px 0 4px}
.why{color:var(--muted);font-size:14px;margin:0 0 14px;max-width:62ch}
.rec{background:var(--royal);color:#fff;font-size:10px;letter-spacing:.1em;padding:3px 8px;
 vertical-align:middle;margin-inline-start:8px}
.copybar{display:flex;justify-content:flex-end;margin-bottom:8px}
.copybtn{background:var(--ink);color:#fff;border:0;padding:10px 20px;font:inherit;font-size:14px;
 font-weight:600;cursor:pointer;letter-spacing:.02em}
.copybtn:hover{background:var(--royal)}
pre.term{direction:rtl;text-align:right;white-space:pre-wrap;word-wrap:break-word;
 background:#fff;border:1px solid rgba(10,22,40,.18);padding:24px 26px;font:inherit;font-size:15.5px;
 line-height:1.75;margin:0;max-height:520px;overflow:auto}
pre.code{direction:ltr;text-align:left;white-space:pre;overflow:auto;background:#fff;
 border:1px solid rgba(10,22,40,.18);padding:18px 20px;font-family:ui-monospace,Menlo,monospace;
 font-size:13px;line-height:1.6;margin:0}
.shot{margin:16px 0 22px}
.pathline{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--muted);margin-bottom:6px;
 word-break:break-all}
.pathline b{color:var(--royal)}
.pathline code{user-select:all}
.shot img{width:100%;display:block;border:1px solid rgba(10,22,40,.2)}
.picker{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0 8px}
.picker span{border:1.5px solid rgba(10,22,40,.28);padding:9px 18px;cursor:pointer;font-size:14px;
 user-select:none;display:flex;align-items:center;gap:9px;background:#fff}
.picker span::before{content:'';width:12px;height:12px;border-radius:50%;
 border:1.5px solid rgba(10,22,40,.4);flex:none}
.picker span:hover{border-color:var(--royal)}
.picker span.chosen{border-color:var(--royal);border-width:2px;background:#fff;font-weight:700}
.picker span.chosen::before{background:var(--royal);border-color:var(--royal);
 box-shadow:inset 0 0 0 2.5px #fff}
.picker span.chosen::after{content:'CHOSEN';font-size:9.5px;letter-spacing:.1em;color:#fff;
 background:var(--royal);padding:2px 6px}
.design{border-top:1px solid rgba(10,22,40,.14);padding-top:22px;margin-top:30px}
table{width:100%;border-collapse:collapse;font-size:14.5px;margin:6px 0 16px}
th,td{border:1px solid rgba(10,22,40,.18);padding:9px 12px;text-align:left;vertical-align:top}
th{background:rgba(1,33,105,.06);font-size:12px;letter-spacing:.07em;text-transform:uppercase}
.note{border-inline-start:3px solid var(--royal);background:rgba(1,33,105,.05);
 padding:14px 18px;margin:14px 0;font-size:15px}
ul{max-width:64ch} li{margin-bottom:6px}
code{font-family:ui-monospace,Menlo,monospace;font-size:.9em}
.foot{margin-top:60px;padding-top:18px;border-top:2px solid var(--line);font-size:13px;color:var(--muted)}
"""

shots = ""
for num, name, why in DESIGNS:
    rec = ' <span class="rec">RECOMMENDED</span>' if num == "2" else ""
    shots += (f'<div class="design"><h3>{num} &middot; {name}{rec}</h3>'
              f'<p class="why">{why}</p>{img(num, "en")}{img(num, "he")}</div>')

hero_opts = []
for num, name, _ in DESIGNS:
    hero_opts += [(f"{num}-HE", f"{num}-HE &middot; {name}"), (f"{num}-EN", f"{num}-EN")]

CMUX_JSON = (HERE.parent.parent / "blog" / "cmux" / "index.html")

DOC = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LinkedIn post - cmux, the terminal nobody installed</title>
<style>{CSS}</style></head><body><div class="wrap">
<div class="mark">ZaZet</div>

<h1>The post: the terminal I run 26 Claude Code sessions in</h1>
<p class="lede">Hebrew post, one single image, blog link in the first comment. Everything below is
either the copy, a hero to pick, or a decision I need from you. Your picks save into the page -
just click, no need to type codes back at me.</p>

<div class="note"><b>New in this pass: the memory angle.</b> Added as its own beat in the post, a
new section in the blog, and <b>hero 7</b>. The numbers are measured, not estimated: 26 Claude Code
panes hold <b>3 - 4 GB</b> (it swings by a gigabyte depending on what they are doing at that
instant), cmux plus 174 shells and helpers hold <b>0.82 GB</b>, on a 24 GB machine - about 5 GB at
the top of the swing.
The row that makes it work is PyCharm - Spotlight says you last opened it on <b>11 June</b>.
That is also what justifies turning
<code>agentHibernation</code> off: it is a RAM decision, and the RAM came from the IDE. The post
says plainly that you stopped reading code in an editor and now read the diff instead.</div>

<div class="note"><b>The angle.</b> cmux is the subject, but <b>Claude Code is the name in line 1</b>
- cmux is the thing nobody has heard of, so it cannot carry the hook on its own. The non-obvious
payoff is self-correcting: I diffed my &ldquo;tuned&rdquo; config against the published schema
defaults and <b>three quarters of it was just the defaults, written down</b>. Only three settings
actually change behaviour, and all three turn something off.</div>

<h2>01 &middot; The post text</h2>
<p class="why">{len(POST)} characters. Claude Code named in line 1, TL;DR opener, raw origin story,
the file-managed mechanism taught, three settings with reasons, closing question. Copy button is
above the box.</p>
<div class="copybar"><button class="copybtn" data-copy="post-text">Copy post text</button></div>
<pre id="post-text" class="term">{html.escape(POST)}</pre>

<h2>01b &middot; The first comment</h2>
<p class="why">The blog link never goes in the post body - LinkedIn suppresses reach on it. Post
first, then paste this as your own first comment. The post body already ends on the question, with
the pointer line one paragraph above it.</p>
<div class="copybar"><button class="copybtn" data-copy="comment-text">Copy first comment</button></div>
<pre id="comment-text" class="term">{html.escape(COMMENT)}</pre>
<div class="note"><b>The link is live</b> - <code>gal.tidhar.org.il/blog/cmux/</code> returns 200,
verified just now. Safe to paste the moment you have posted.</div>

<h2>02 &middot; Pick the hero</h2>
<p class="why">Six designs, each in English and Hebrew. The post is Hebrew, so the Hebrew version is
the one that ships - the English ones are here so you can read the composition, and one of them
becomes the blog og:image. All twelve Hebrew and English PNGs were opened and checked for bidi bugs;
one real one was found and fixed (a path starting with <code>~/.</code> had its leading characters
thrown to the far end of the line).</p>
{picker("hero", hero_opts)}
{shots}

<h2>03 &middot; Decisions</h2>

<h3>03a &middot; Keep the closing question?</h3>
<p class="why">&ldquo;Which setting in a tool you open every morning have you never checked is even
the default?&rdquo; You kept the question on the remote-control post and cut it on the ego-lite one.
Recommendation: keep - it invites people to post their own config, which is exactly the comment
thread this post wants.</p>
{picker("question", [("keep", "Keep it &middot; recommended"), ("cut", "Cut it, end on the first-comment pointer")])}

<h3>03b &middot; Blog post language</h3>
<p class="why">The blog post is written in English, like every other post on the site, and it carries
the full <code>cmux.json</code> plus the Claude Code settings table. The post text points at it in
the first comment.</p>
{picker("bloglang", [("en", "English &middot; recommended, matches the site"), ("he", "Translate the blog post to Hebrew too")])}

<h3>03c &middot; Push the cmux config into the starter repo?</h3>
<p class="why">The blog post links <code>tatarco/claude-code-starter</code>. I could add the
<code>cmux.json</code> to that repo as a second file so the post has one clone-and-go target instead
of a code block to copy. Costs nothing, but it widens what that repo claims to be.</p>
{picker("repo", [("no", "No &middot; recommended, keep the repo about Claude Code only"), ("yes", "Yes, add cmux.json to the starter repo")])}

<div class="note"><b>The 26 is verified two ways.</b> The cmux session file has <b>26 terminal
panes across 7 workspaces</b>, and a process count taken at the same moment found <b>26 live
<code>claude</code> processes</b>, 25 of them children of cmux. The session file alone would only
have proved pane count, so the process count was added.
Two other things the skeptic caught and I fixed: the README says &ldquo;macOS only, for now&rdquo;,
not that no port is planned; and it says cmux <i>can</i> orchestrate (Claude Code teams, multi-model
runs), so the flat &ldquo;it is not an orchestrator&rdquo; line is gone from the post, the blog and
hero 3.</div>

<h2>04 &middot; What I removed and why</h2>
<ul>
<li><b>The workspace names.</b> My real cmux session file has workspaces named after live client
projects. The post says &ldquo;7 workspaces&rdquo; and never names them. Nothing about a client is
recoverable from the numbers.</li>
<li><b>A paragraph comparing cmux to Warp and to claude-squad.</b> It delayed the payoff and I had
not used either hard enough to be fair about them.</li>
<li><b>The Founder's Edition.</b> Mentioned once in the blog post as a fact, kept out of the
LinkedIn post entirely - naming a paid tier in a &ldquo;this is free&rdquo; post reads as a pitch.</li>
</ul>

<h2>05 &middot; Facts, and where each one came from</h2>
<table>
<tr><th>Claim</th><th>Source</th></tr>
<tr><td>26 panes, 7 workspaces</td><td>Counted out of
<code>~/Library/Application Support/cmux/session-com.cmuxterm.app.json</code></td></tr>
<tr><td>cmux 0.64.20</td><td><code>cmux --version</code></td></tr>
<tr><td>~25.7k stars, GPL-3.0-or-later, macOS only, Ghostty-based</td><td>The cmux README</td></tr>
<tr><td>Every default in the comparison table</td><td>The published
<code>cmux.schema.json</code>, fetched at build time</td></tr>
<tr><td>My config, verbatim</td><td><code>~/.config/cmux/cmux.json</code></td></tr>
</table>

<h2>06 &middot; Ready to ship</h2>
<ul>
<li>Blog post written: <code>blog/cmux/index.html</code> - full config, settings table, the diff
against defaults.</li>
<li>Homepage card added.</li>
<li>12 heroes rendered, Hebrew ones opened and checked.</li>
<li>Not yet pushed. Tell me the hero and I will set <code>og.png</code>, commit and push.</li>
</ul>

<p class="foot">ZaZet &middot; internal &middot; the post ships only after you pick a hero.</p>
</div>
<script src="/copy.js"></script>
<script src="/persist.js"></script>
</body></html>"""

out = HERE / "choices-doc.html"
out.write_text(DOC, encoding="utf-8")
print("wrote", out, len(DOC), "bytes")
