#!/usr/bin/env python3
"""Render the same 6 hero concepts in the ZaZet house style (paper/ink/royal, Fraunces). Hebrew only."""
import base64, pathlib

D = pathlib.Path(__file__).parent
FONTS = pathlib.Path.home() / ".claude/skills/zazet-doc/assets/fonts"
FR = base64.b64encode((FONTS / "fraunces-700-latin.woff2").read_bytes()).decode()

S = dict(
    eyebrow="לבעלי עסקים",
    d1_top="וייב קודינג מגיע עד לפה",
    d1_deep="ומכאן צריך צוללן",
    d1_chips=["ארכיטקטורה", "הרשאות", "ריבוי לקוחות", "בקאנד"],
    d2_big='וייב קודינג<br>זה <em>שנירקול</em>.',
    d2_sub="יש עומק שבו צריך צוללן.",
    d3_kicker="בלי מצגת. בלי מכירה.",
    d3_big="חצי שעה.<br><em>בחינם.</em>",
    d3_chips=["מה לבנות ראשון", "מה לא לבנות בכלל", "איפה זה יישבר"],
    d4_num="5",
    d4_label="סלוטים",
    d4_sub="זה כל מה שיש לי החודש.",
    d4_foot="אני על החוף בקרואטיה עם הילדים.",
    d5_title="מה תצאו איתו מחצי השעה",
    d5_rows=[("01", "מפה של מה לבנות ראשון", "ומה לא לבנות בכלל"),
             ("02", "מה אתם בונים לבד", "ואיפה זה יישבר"),
             ("03", "שם אחד של כלי", "שמתאים בדיוק לכם")],
    d5_price="חינם.",
    d6_quote="ויבוא יום<br>שתגיעו לעומק<br>שלא נוח בו.",
    d6_attr="אולי אז תבחרו בי כצוללן.",
)

BASE = """<!DOCTYPE html><html dir="rtl" lang="he"><head><meta charset="utf-8"><style>
@font-face{{font-family:Fraunces;font-weight:700;font-display:block;
  src:url(data:font/woff2;base64,%s) format('woff2')}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{background:#F0F7FC;color:#0A1628;direction:rtl;
  font-family:'Arial Hebrew','SF Hebrew',system-ui,sans-serif;
  padding:44px 56px 40px;display:flex;flex-direction:column;position:relative}}
.mast{{display:flex;align-items:baseline;justify-content:space-between;
  border-bottom:2px solid #0A1628;padding-bottom:14px}}
.wm{{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:27px;letter-spacing:-.01em;direction:ltr}}
.eyebrow{{font-size:14px;font-weight:700;letter-spacing:.16em;color:#012169}}
.foot{{margin-top:auto;padding-top:16px;border-top:1px solid rgba(10,22,40,.18);
  display:flex;justify-content:space-between;align-items:baseline;
  font-size:16px;color:#4a5e78;direction:ltr}}
.foot b{{font-family:Fraunces,Georgia,serif;font-weight:700;color:#0A1628}}
em{{font-style:normal;color:#012169}}
{css}
</style></head><body>
<div class="mast"><span class="wm">ZaZet</span><span class="eyebrow">%s</span></div>
{body}
<div class="foot"><b>ZaZet Solutions</b><span>zazet-solutions.hr</span></div>
</body></html>""" % (FR, S["eyebrow"])


def d1():
    chips = "".join(f'<span class="chip">{c}</span>' for c in S["d1_chips"])
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center;gap:0}
.shallow{font-size:58px;font-weight:800;line-height:1.12;margin-bottom:26px}
.deepzone{background:#0A1628;color:#F0F7FC;margin-inline:-56px;padding:30px 56px 34px}
.deep{font-size:30px;color:#8fb3e0;font-weight:700;margin-bottom:20px}
.chips{display:flex;flex-wrap:wrap;gap:12px}
.chip{border:1px solid rgba(240,247,252,.32);padding:10px 20px;font-size:24px}
"""
    body = (f'<div class="wrap"><div class="shallow">{S["d1_top"]}</div>'
            f'<div class="deepzone"><div class="deep">{S["d1_deep"]}</div>'
            f'<div class="chips">{chips}</div></div></div>')
    return BASE.format(css=css, body=body)


def d2():
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.big{font-size:112px;font-weight:800;line-height:1.04;letter-spacing:-.02em}
.sub{font-size:38px;color:#4a5e78;margin-top:28px;font-weight:600}
"""
    body = f'<div class="wrap"><div class="big">{S["d2_big"]}</div><div class="sub">{S["d2_sub"]}</div></div>'
    return BASE.format(css=css, body=body)


def d3():
    chips = "".join(f'<span class="chip">{c}</span>' for c in S["d3_chips"])
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.kicker{font-size:27px;color:#4a5e78;margin-bottom:12px}
.big{font-size:100px;font-weight:800;line-height:1.03;letter-spacing:-.02em}
.chips{display:flex;flex-wrap:wrap;gap:12px;margin-top:34px}
.chip{border:1px solid rgba(1,33,105,.35);color:#012169;padding:10px 20px;font-size:23px;font-weight:600}
"""
    body = (f'<div class="wrap"><div class="kicker">{S["d3_kicker"]}</div>'
            f'<div class="big">{S["d3_big"]}</div><div class="chips">{chips}</div></div>')
    return BASE.format(css=css, body=body)


def d4():
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.num{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:220px;line-height:.86;color:#012169;direction:ltr}
.label{font-size:54px;font-weight:800;margin-top:10px}
.sub{font-size:32px;color:#4a5e78;margin-top:20px}
.small{font-size:24px;color:#4a5e78;opacity:.75;margin-top:8px}
"""
    body = (f'<div class="wrap"><div class="num">{S["d4_num"]}</div>'
            f'<div class="label">{S["d4_label"]}</div><div class="sub">{S["d4_sub"]}</div>'
            f'<div class="small">{S["d4_foot"]}</div></div>')
    return BASE.format(css=css, body=body)


def d5():
    rows = "".join(
        f'<div class="row"><span class="n">{n}</span>'
        f'<span class="t"><b class="m">{a}</b><span class="s">{b}</span></span></div>'
        for n, a, b in S["d5_rows"])
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.title{font-size:34px;font-weight:800;color:#012169;margin-bottom:14px}
.row{display:flex;align-items:baseline;gap:22px;padding:14px 0;border-top:1px solid rgba(10,22,40,.15)}
.n{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:38px;color:rgba(1,33,105,.42);direction:ltr}
.t{display:flex;flex-direction:column;gap:2px}
.m{font-size:30px;font-weight:700}
.s{font-size:22px;color:#4a5e78}
.price{margin-top:20px;font-size:46px;font-weight:800;color:#012169}
"""
    body = f'<div class="wrap"><div class="title">{S["d5_title"]}</div>{rows}<div class="price">{S["d5_price"]}</div></div>'
    return BASE.format(css=css, body=body)


def d6():
    css = """
.wrap{flex:1;margin-block:26px 22px;display:flex;flex-direction:column;justify-content:center;
  border-inline-start:4px solid #012169;padding-inline-start:34px}
.q{font-size:74px;font-weight:800;line-height:1.12;letter-spacing:-.02em}
.attr{font-size:32px;color:#012169;margin-top:28px;font-weight:600}
"""
    body = f'<div class="wrap"><div class="q">{S["d6_quote"]}</div><div class="attr">{S["d6_attr"]}</div></div>'
    return BASE.format(css=css, body=body)


for i, fn in enumerate([d1, d2, d3, d4, d5, d6], 1):
    p = D / f"hero-z{i}-he.html"
    p.write_text(fn(), encoding="utf-8")
    print(p)
