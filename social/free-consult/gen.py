#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for the free-consult LinkedIn post."""
import pathlib

OUT = pathlib.Path(__file__).parent

S = {
    "he": dict(
        dir="rtl", font="'Arial Hebrew','SF Hebrew',system-ui,sans-serif", arrow="←",
        eyebrow="לבעלי עסקים",
        d1_top="וייב קודינג מגיע עד לפה",
        d1_deep="ומכאן צריך צוללן",
        d1_chips=["ארכיטקטורה", "הרשאות", "ריבוי לקוחות", "בקאנד"],
        d2_big="וייב קודינג<br>זה שנירקול.",
        d2_sub="יש עומק שבו צריך <b>צוללן</b>.",
        d3_kicker="בלי מצגת. בלי מכירה.",
        d3_big="חצי שעה.<br>בחינם.",
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
        foot="ZaZet Solutions · zazet-solutions.hr",
    ),
    "en": dict(
        dir="ltr", font="system-ui,-apple-system,'Helvetica Neue',sans-serif", arrow="→",
        eyebrow="FOR BUSINESS OWNERS",
        d1_top="Vibe coding gets you this far",
        d1_deep="from here you need a diver",
        d1_chips=["Architecture", "Permissions", "Multi-tenancy", "Backend"],
        d2_big="Vibe coding<br>is snorkeling.",
        d2_sub="There's a depth that needs a <b>diver</b>.",
        d3_kicker="No deck. No pitch.",
        d3_big="Half an hour.<br>Free.",
        d3_chips=["What to build first", "What not to build", "Where it will break"],
        d4_num="5",
        d4_label="slots",
        d4_sub="That's all I have this month.",
        d4_foot="I'm on a beach in Croatia with my kids.",
        d5_title="What you walk away with",
        d5_rows=[("01", "A map of what to build first", "and what not to build at all"),
                 ("02", "What you can build alone", "and where it will break"),
                 ("03", "One named tool", "that actually fits you")],
        d5_price="Free.",
        d6_quote="One day you'll<br>reach a depth<br>you're not<br>comfortable in.",
        d6_attr="Maybe then you'll pick me as the diver.",
        foot="ZaZet Solutions · zazet-solutions.hr",
    ),
}

BASE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1200px;height:630px;overflow:hidden}}
body{{background:#0a1628;color:#bae6fd;font-family:{font};direction:{dir};
  background-image:linear-gradient(rgba(125,211,252,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(125,211,252,.06) 1px,transparent 1px);
  background-size:40px 40px;position:relative;padding:56px;display:flex;flex-direction:column}}
.eyebrow{{position:absolute;top:36px;inset-inline-start:56px;font-size:19px;color:#7dd3fc;font-weight:700;letter-spacing:.04em}}
.foot{{position:absolute;bottom:34px;inset-inline-start:56px;font-size:20px;color:rgba(186,230,253,.55);direction:ltr}}
.foot b{{color:#e0f2fe}}
b{{color:#fef08a}}
{css}
</style></head><body>{body}</body></html>"""


def page(lang, css, body, foot=True):
    s = S[lang]
    f = f'<div class="foot">{s["foot"]}</div>' if foot else ""
    return BASE.format(font=s["font"], dir=s["dir"], css=css, body=body + f)


def d1(lang):
    s = S[lang]
    chips = "".join(f'<span class="chip">{c}</span>' for c in s["d1_chips"])
    css = """
body{padding:0}
.eyebrow{top:36px;inset-inline-start:56px;z-index:3}
.foot{bottom:34px;inset-inline-start:56px;z-index:3}
.zone{position:absolute;inset-inline:0;display:flex;flex-direction:column;justify-content:center;padding:0 56px}
.up{top:0;height:300px}
.dn{top:300px;bottom:0;background:linear-gradient(to bottom,rgba(2,6,16,.92),rgba(2,6,16,1))}
.rule{position:absolute;inset-inline:0;top:300px;height:0;border-top:2px dashed rgba(125,211,252,.6);z-index:2}
.shallow{font-size:62px;font-weight:800;color:#7dd3fc;line-height:1.1;text-shadow:0 0 45px rgba(125,211,252,.4)}
.deep{font-size:36px;color:#fef08a;font-weight:700;margin-bottom:28px}
.chips{display:flex;flex-wrap:wrap;gap:14px}
.chip{border:1px solid rgba(125,211,252,.3);padding:12px 24px;font-size:28px;color:rgba(186,230,253,.75)}
"""
    body = f'<div class="eyebrow">{s["eyebrow"]}</div>' \
           f'<div class="zone up"><div class="shallow">{s["d1_top"]}</div></div>' \
           f'<div class="rule"></div>' \
           f'<div class="zone dn"><div class="deep">{s["d1_deep"]}</div>' \
           f'<div class="chips">{chips}</div></div>'
    return page(lang, css, body)


def d2(lang):
    s = S[lang]
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.big{font-size:126px;font-weight:800;line-height:1.02;color:#7dd3fc;text-shadow:0 0 55px rgba(125,211,252,.45)}
.sub{font-size:44px;color:#e0f2fe;margin-top:36px;font-weight:600}
"""
    body = f'<div class="eyebrow">{s["eyebrow"]}</div><div class="wrap">' \
           f'<div class="big">{s["d2_big"]}</div><div class="sub">{s["d2_sub"]}</div></div>'
    return page(lang, css, body)


def d3(lang):
    s = S[lang]
    chips = "".join(f'<span class="chip">{c}</span>' for c in s["d3_chips"])
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.kicker{font-size:30px;color:rgba(186,230,253,.6);margin-bottom:14px}
.big{font-size:112px;font-weight:800;line-height:1.0;color:#fef08a;text-shadow:0 0 55px rgba(254,240,138,.28)}
.chips{display:flex;flex-wrap:wrap;gap:14px;margin-top:40px}
.chip{border:1px solid rgba(125,211,252,.4);padding:12px 24px;font-size:26px;color:#bae6fd}
"""
    body = f'<div class="eyebrow">{s["eyebrow"]}</div><div class="wrap">' \
           f'<div class="kicker">{s["d3_kicker"]}</div><div class="big">{s["d3_big"]}</div>' \
           f'<div class="chips">{chips}</div></div>'
    return page(lang, css, body)


def d4(lang):
    s = S[lang]
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center}
.num{font-size:250px;font-weight:800;line-height:.9;color:#fef08a;text-shadow:0 0 70px rgba(254,240,138,.35)}
.label{font-size:62px;font-weight:800;color:#7dd3fc;margin-top:4px}
.sub{font-size:36px;color:#e0f2fe;margin-top:26px}
.small{font-size:27px;color:rgba(186,230,253,.55);margin-top:12px}
"""
    body = f'<div class="eyebrow">{s["eyebrow"]}</div><div class="wrap">' \
           f'<div class="num">{s["d4_num"]}</div><div class="label">{s["d4_label"]}</div>' \
           f'<div class="sub">{s["d4_sub"]}</div><div class="small">{s["d4_foot"]}</div></div>'
    return page(lang, css, body)


def d5(lang):
    s = S[lang]
    rows = "".join(
        f'<div class="row"><span class="n">{n}</span>'
        f'<span class="t"><b class="m">{a}</b><span class="s">{b}</span></span></div>'
        for n, a, b in s["d5_rows"])
    css = """
.wrap{flex:1;display:flex;flex-direction:column;justify-content:center}
.title{font-size:40px;font-weight:800;color:#7dd3fc;margin-bottom:26px}
.row{display:flex;align-items:baseline;gap:20px;padding:16px 0;border-top:1px solid rgba(125,211,252,.18)}
.n{font-family:'SF Mono',Menlo,monospace;font-size:22px;color:rgba(254,240,138,.85);direction:ltr}
.t{display:flex;flex-direction:column;gap:4px}
.m{font-size:33px;color:#e0f2fe;font-weight:700}
.s{font-size:24px;color:rgba(186,230,253,.55)}
.price{margin-top:26px;font-size:56px;font-weight:800;color:#fef08a}
"""
    body = f'<div class="eyebrow">{s["eyebrow"]}</div><div class="wrap">' \
           f'<div class="title">{s["d5_title"]}</div>{rows}' \
           f'<div class="price">{s["d5_price"]}</div></div>'
    return page(lang, css, body)


def d6(lang):
    s = S[lang]
    css = """
.wrap{flex:1;margin-block:34px 30px;display:flex;flex-direction:column;justify-content:center;
  border-inline-start:5px solid rgba(254,240,138,.75);padding-inline-start:38px}
.q{font-size:82px;font-weight:800;line-height:1.1;color:#e0f2fe}
.attr{font-size:38px;color:#7dd3fc;margin-top:34px;font-weight:600}
"""
    body = f'<div class="eyebrow">{s["eyebrow"]}</div><div class="wrap">' \
           f'<div class="q">{s["d6_quote"]}</div><div class="attr">{s["d6_attr"]}</div></div>'
    return page(lang, css, body)


for i, fn in enumerate([d1, d2, d3, d4, d5, d6], 1):
    for lang in ("en", "he"):
        p = OUT / f"hero-{i}-{lang}.html"
        p.write_text(fn(lang), encoding="utf-8")
        print(p)
