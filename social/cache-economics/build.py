#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for the cache-economics post.

One strings table drives every design so EN and HE never drift.
Run: python3 build.py && ./shoot.sh
"""
import pathlib

OUT = pathlib.Path(__file__).parent

S = {
    "en": {
        "dir": "ltr", "arrow": "&rarr;", "align": "left",
        "top": "Claude Code · cost",
        "d1_kicker": "of every token I send",
        "d1_big": "96.3%",
        "d1_sub": "is the model <b>re-reading</b> context it already saw.",
        "d1_chips": ["13.9B tokens", "59 days", "Max 20x plan"],
        "d2": "I ran 13.9 billion tokens through Claude Code in two months.<br>I still have not hit the limit on a <b>Max 20x</b> plan.",
        "d2_kicker": "the thing nobody measures",
        "d3_kicker": "same work, two worlds",
        "d3_a_label": "list price without caching", "d3_a": "65,628",
        "d3_b_label": "list price with caching", "d3_b": "9,778",
        "d3_foot": "Neither is my bill. Caching is <b>85%</b> of the difference.",
        "d4_kicker": "why it works",
        "d4_title": "The cache is a <b>prefix match</b>",
        "d4_stable": "stable prefix", "d4_stable_note": "served at 0.1x price",
        "d4_volatile": "your new line", "d4_volatile_note": "full price",
        "d4_warn": "Change one byte upstream and the whole prefix is rebuilt at up to 2x.",
        "d5_kicker": "one rule, five ways to keep it",
        "d5": [("Never switch model mid-session", "a model swap invalidates the entire cache"),
               ("Push research into subagents", "clean context in, conclusion out, nothing re-read"),
               ("Compact early, around 40%", "an 85%-full window is re-read at 85% every turn"),
               ("Never wake a huge stale session", "one line pays to re-upload the whole conversation"),
               ("Keep the shelf deep, but frozen", "164 skills, 16,500 tokens - free, because they never move")],
        "d6_kicker": "where the tokens actually went",
        "d6_head": ["model", "tokens", "at API list price"],
        "d6": [("Opus 4.8", "9,751M", "8,332"), ("Opus 5", "2,565M", "2,032"),
               ("Haiku 4.5", "957M", "172"), ("Sonnet 5", "529M", "217")],
        "d6_foot": "Haiku did <b>957 million</b> tokens for the price of a nice dinner.",
        "foot": "Real token counts at API list rates. Actual spend: <b>one Max 20x plan</b> · gal.tidhar.org.il",
    },
    "he": {
        "dir": "rtl", "arrow": "&larr;", "align": "right",
        "top": "קלוד קוד · עלות",
        "d1_kicker": "מכל טוקן שאני שולח",
        "d1_big": "96.3%",
        "d1_sub": "זה המודל <b>קורא מחדש</b> קונטקסט שהוא כבר ראה.",
        "d1_chips": ["13.9 מיליארד טוקנים", "59 ימים", "מסלול Max 20x"],
        "d2": "העברתי 13.9 מיליארד טוקנים בקלוד קוד בחודשיים.<br>ועוד לא נגעתי בלימיט של מסלול <b>Max 20x</b>.",
        "d2_kicker": "המספר שאף אחד לא מודד",
        "d3_kicker": "אותה עבודה, שני עולמות",
        "d3_a_label": "לפי מחירון, בלי caching", "d3_a": "65,628",
        "d3_b_label": "לפי מחירון, עם caching", "d3_b": "9,778",
        "d3_foot": "אף אחד מהם הוא לא מה ששילמתי. קאשינג הוא <b>85%</b> מהפער.",
        "d4_kicker": "למה זה עובד",
        "d4_title": "ה-cache הוא <b>התאמת תחילית</b>",
        "d4_stable": "תחילית יציבה", "d4_stable_note": "עשירית מהמחיר",
        "d4_volatile": "השורה החדשה שלך", "d4_volatile_note": "מחיר מלא",
        "d4_warn": "בייט אחד שמשתנה למעלה, וכל התחילית נבנית מחדש עד כפול מחיר.",
        "d5_kicker": "כלל אחד, חמש דרכים לא לשבור אותו",
        "d5": [("לא מחליפים מודל באמצע סשן", "החלפת מודל מוחקת את כל ה-cache"),
               ("דוחפים מחקר לסאב-אייג'נטים", "קונטקסט נקי נכנס, מסקנה יוצאת, כלום לא נקרא מחדש"),
               ("עושים compact מוקדם, בערך ב-40%", "חלון מלא ב-85% נקרא מחדש ב-85% בכל תור"),
               ("לא מעירים סשן ענק וישן", "שורה אחת משלמת על העלאה מחדש של הכל"),
               ("מדף עמוק זה בסדר. מדף שזז זה לא", "164 סקילים, 16,500 טוקנים, בעשירית מחיר כי הם קפואים")],
        "d6_kicker": "לאן הטוקנים באמת הלכו",
        "d6_head": ["מודל", "טוקנים", "לפי מחירון API"],
        "d6": [("Opus 4.8", "9,751M", "8,332"), ("Opus 5", "2,565M", "2,032"),
               ("Haiku 4.5", "957M", "172"), ("Sonnet 5", "529M", "217")],
        "d6_foot": "הייקו עשה <b>957 מיליון</b> טוקנים במחיר של ארוחת ערב.",
        "foot": 'ספירת טוקנים אמיתית לפי מחירון <span class="num">API</span>. בפועל: <b>מסלול <span class="num">Max 20x</span></b> · <span class="num">gal.tidhar.org.il</span>',
    },
}

BASE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#0a1628;color:#bae6fd;direction:%(dir)s;
  font-family:'IBM Plex Mono','Arial Hebrew','Arial Unicode MS',system-ui,monospace;
  background-image:linear-gradient(rgba(125,211,252,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(125,211,252,.06) 1px,transparent 1px);
  background-size:40px 40px;display:flex;flex-direction:column;justify-content:center;align-items:center;
  text-align:center;padding:52px;position:relative}
.top{position:absolute;top:36px;inset-inline-end:56px;font-size:19px;color:#7dd3fc;font-weight:700}
/* direction:ltr must live on an inner span - putting it on the positioned
   element flips its own inline-start and collides it with .top in RTL. */
.rev{position:absolute;top:38px;inset-inline-start:56px;font-size:14px;letter-spacing:.14em;
  color:rgba(186,230,253,.45)}
.rev span{direction:ltr;unicode-bidi:isolate}
.kicker{font-size:27px;color:rgba(186,230,253,.62);margin-bottom:10px}
.num{unicode-bidi:isolate}
.big{font-size:190px;font-weight:800;line-height:.92;color:#7dd3fc;text-shadow:0 0 55px rgba(125,211,252,.5);direction:ltr}
.sub{font-size:38px;color:#e0f2fe;font-weight:700;margin-top:14px;max-width:960px;line-height:1.34}
.sub b,.claim b{color:#fef08a}
.claim{font-size:56px;font-weight:800;color:#e0f2fe;line-height:1.32;max-width:1020px}
.row{display:flex;gap:14px;margin-top:30px;flex-wrap:wrap;justify-content:center}
.chip{border:1px solid rgba(125,211,252,.5);padding:9px 20px;color:#7dd3fc;font-size:21px}
.foot{position:absolute;bottom:34px;font-size:20px;color:rgba(186,230,253,.6)}
.foot b{color:#e0f2fe}
%(extra)s
</style></head><body>
<div class="top">%(top)s</div><div class="rev"><span>gal.tidhar.org.il</span></div>
%(body)s
<div class="foot">%(foot)s</div>
</body></html>"""

D3 = """
.pair{display:flex;align-items:center;gap:46px;margin-top:6px}
.cell{padding:26px 40px;border:2px solid;min-width:340px}
.cell.bad{border-color:rgba(248,113,113,.65)}
.cell.good{border-color:rgba(125,211,252,.7)}
.cell .lab{font-size:22px;color:rgba(186,230,253,.66);margin-bottom:12px}
.cell .val{font-size:66px;font-weight:800}
.cell.bad .val{color:#f87171;text-decoration:line-through;text-decoration-thickness:3px}
.cell.good .val{color:#7dd3fc;text-shadow:0 0 40px rgba(125,211,252,.45)}
.arw{font-size:52px;color:rgba(186,230,253,.5)}
.note{font-size:34px;color:#e0f2fe;font-weight:700;margin-top:34px}
.note b{color:#fef08a}
"""

D4 = """
.title{font-size:46px;font-weight:800;color:#e0f2fe;margin-bottom:34px}
.title b{color:#fef08a}
.bar{display:flex;width:1000px;border:2px solid rgba(125,211,252,.55)}
.seg{padding:24px 18px}
.seg.s{flex:5;background:rgba(125,211,252,.14);border-inline-end:2px dashed rgba(125,211,252,.55)}
.seg.v{flex:1;background:rgba(254,240,138,.12)}
.seg .n{font-size:24px;font-weight:700;color:#e0f2fe}
.seg .p{font-size:20px;color:rgba(186,230,253,.7);margin-top:8px}
.seg.v .n{color:#fef08a}
.warn{font-size:28px;color:rgba(186,230,253,.8);margin-top:34px;max-width:940px;line-height:1.45}
"""

D5 = """
.list{display:flex;flex-direction:column;gap:15px;width:1030px;margin-top:6px}
.item{display:flex;align-items:baseline;gap:18px;border-inline-start:3px solid rgba(125,211,252,.55);
  padding-inline-start:20px;text-align:start}
.item .n{font-size:25px;color:#fef08a;font-weight:800;direction:ltr;min-width:26px}
.item .t{font-size:26px;color:#e0f2fe;font-weight:700}
.item .d{font-size:20px;color:rgba(186,230,253,.62);margin-top:4px}
"""

D6 = """
table{border-collapse:collapse;width:900px;margin-top:8px}
th{font-size:21px;color:rgba(186,230,253,.55);font-weight:400;padding:0 20px 14px;text-align:start;
  border-bottom:1px solid rgba(125,211,252,.3)}
td{font-size:30px;color:#e0f2fe;padding:16px 20px;text-align:start;border-bottom:1px solid rgba(125,211,252,.12)}
td.n{color:#7dd3fc;font-weight:700}
td .num{unicode-bidi:isolate}
tr.hi td{color:#fef08a}
tr.hi td.n{color:#fef08a}
.note{font-size:29px;color:#e0f2fe;margin-top:30px}
.note b{color:#fef08a}
"""


def money(lang, n):
    """Currency must never be baked into an LTR run with the digits."""
    return f"${n}" if lang == "en" else f'<span class="num">{n}</span> דולר'


def render(lang):
    s = S[lang]
    designs = {}

    # 1 - the one big number
    chips = "".join(f'<span class="chip">{c}</span>' for c in s["d1_chips"])
    designs[1] = ("", f'<div class="kicker">{s["d1_kicker"]}</div>'
                      f'<div class="big">{s["d1_big"]}</div>'
                      f'<div class="sub">{s["d1_sub"]}</div><div class="row">{chips}</div>')

    # 2 - the claim as one huge sentence (his proven winner)
    designs[2] = ("", f'<div class="kicker">{s["d2_kicker"]}</div><div class="claim">{s["d2"]}</div>')

    # 3 - the concrete before/after
    designs[3] = (D3, f'<div class="kicker">{s["d3_kicker"]}</div><div class="pair">'
                      f'<div class="cell bad"><div class="lab">{s["d3_a_label"]}</div>'
                      f'<div class="val">{money(lang, s["d3_a"])}</div></div>'
                      f'<div class="arw">{s["arrow"]}</div>'
                      f'<div class="cell good"><div class="lab">{s["d3_b_label"]}</div>'
                      f'<div class="val">{money(lang, s["d3_b"])}</div></div></div>'
                      f'<div class="note">{s["d3_foot"]}</div>')

    # 4 - the mechanism
    designs[4] = (D4, f'<div class="kicker">{s["d4_kicker"]}</div>'
                      f'<div class="title">{s["d4_title"]}</div><div class="bar">'
                      f'<div class="seg s"><div class="n">{s["d4_stable"]}</div>'
                      f'<div class="p">{s["d4_stable_note"]}</div></div>'
                      f'<div class="seg v"><div class="n">{s["d4_volatile"]}</div>'
                      f'<div class="p">{s["d4_volatile_note"]}</div></div></div>'
                      f'<div class="warn">{s["d4_warn"]}</div>')

    # 5 - the levers grid
    items = "".join(f'<div class="item"><div class="n">{i}</div><div><div class="t">{t}</div>'
                    f'<div class="d">{d}</div></div></div>'
                    for i, (t, d) in enumerate(s["d5"], 1))
    designs[5] = (D5, f'<div class="kicker">{s["d5_kicker"]}</div><div class="list">{items}</div>')

    # 6 - the receipts table
    head = "".join(f"<th>{h}</th>" for h in s["d6_head"])
    rows = "".join(f'<tr class="{"hi" if m.startswith("Haiku") else ""}"><td>{m}</td>'
                   f'<td class="n"><span class="num">{t}</span></td>'
                   f'<td class="n">{money(lang, c)}</td></tr>' for m, t, c in s["d6"])
    designs[6] = (D6, f'<div class="kicker">{s["d6_kicker"]}</div>'
                      f'<table><tr>{head}</tr>{rows}</table><div class="note">{s["d6_foot"]}</div>')

    for n, (extra, body) in designs.items():
        html = BASE % {"dir": s["dir"], "extra": extra, "top": s["top"],
                       "body": body, "foot": s["foot"]}
        (OUT / f"hero-{n}-{lang}.html").write_text(html, encoding="utf-8")


for lang in ("en", "he"):
    render(lang)
print("wrote 12 html files to", OUT)
