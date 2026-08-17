#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for the SAP-business-card origin story.

One strings table drives every design so EN and HE never drift.
Bidi rules (see the linkedin skill): every Latin/numeric run gets .num
(direction:ltr + isolate), logical CSS only, no currency symbol inside
Hebrew text ("400 יורו", not "400€").

Run: python3 build.py && ./shoot.sh
"""
import base64
import pathlib

OUT = pathlib.Path(__file__).parent
CARD = base64.b64encode((OUT / "card.jpg").read_bytes()).decode()


def n(t):
    """Isolate a Latin/numeric run so RTL reflow cannot reorder it."""
    return f'<span class="num">{t}</span>'


S = {
    "en": {
        "dir": "ltr", "align": "left", "arrow": "&rarr;",
        "top": "how I got into tech",
        "foot": "gal.tidhar.org.il",

        "d1_kicker": "Berlin, 2013. A shopping-mall cart, Dead Sea cosmetics.",
        "d1": "An <b>SAP</b> manager bought hand cream off me for <b>400 euro</b>, "
              "then told me I was in the wrong job. That is why I write code.",

        "d2_cap": "This card sat in my wallet for years. It is the reason I learned to program.",

        "d3_a_label": "what he told me",
        "d3_a": "go do tech sales",
        "d3_a_note": "“You are selling me hand cream with the energy people sell a million-euro SAP deal with.”",
        "d3_b_label": "what I actually did",
        "d3_b": "learned to code instead",
        "d3_b_note": "Signed up for the course, fell in love with the code, never made the sale.",
        "d3_foot": "I took exactly <b>half</b> the advice.",

        "d4_quote": "“You are selling me hand cream with the energy people sell a "
                    "million-euro SAP deal with. You are in the wrong place.”",
        "d4_by": "Husain, PR manager at SAP, at a cart in Alexa mall, Berlin",

        "d5_kicker": "one stranger, thirteen years",
        "d5_rows": [("2013", "a cosmetics cart in Berlin, full time"),
                    ("2013", "he buys 400 euro of cream and hands me his card"),
                    ("later", "I sign up to study, to get into tech sales"),
                    ("a decade", "I fall in love with the code and never sell a thing"),
                    ("2026", "someone asks me to sell again. First time since Berlin.")],

        "d6_kicker": "what a mall cart teaches you about selling software",
        "d6_rows": [("Open with a question, not the product",
                     "Nobody stops for “Dead Sea cosmetics”. They stop for “can I ask you something?” "
                     "Nobody stops for “I build automations” either."),
                    ("Demo on their hand, not yours",
                     "At the cart I rubbed the cream into their skin. In software that means a demo "
                     "on their data, not my polished one.")],
    },
    "he": {
        "dir": "rtl", "align": "right", "arrow": "&larr;",
        "top": "איך הגעתי להייטק",
        "foot": "gal.tidhar.org.il",

        "d1_kicker": "ברלין, 2013. עגלה בקניון, קוסמטיקה מים המלח.",
        "d1": "מנהל ב-<b>SAP</b> קנה ממני קרם ידיים ב-<b>400 יורו</b>, "
              "ואז אמר לי שאני בעבודה הלא נכונה. בגלל זה אני כותב קוד.",

        "d2_cap": "הכרטיס הזה שכב לי בארנק שנים. בגללו למדתי לתכנת.",

        "d3_a_label": "מה שהוא אמר לי",
        "d3_a": "לך תעשה מכירות בטק",
        "d3_a_note": "״אתה מוכר לי קרם ידיים באנרגיה שבה מוכרים SAP במיליון.״",
        "d3_b_label": "מה שבאמת עשיתי",
        "d3_b": "למדתי לתכנת במקום",
        "d3_b_note": "נרשמתי ללימודים, התאהבתי בקוד, ומכירה אחת לא עשיתי.",
        "d3_foot": "לקחתי בדיוק <b>חצי</b> מהעצה.",

        "d4_quote": "״אתה מוכר לי קרם ידיים באותה אנרגיה שבה מוכרים SAP במיליון. "
                    "אתה במקום הלא נכון.״",
        "d4_by": "חוסיין, מנהל ב-SAP, ליד עגלה בקניון אלכסה בברלין",

        "d5_kicker": "אדם אחד שנעצר, שלוש עשרה שנה",
        "d5_rows": [("2013", "עגלת קוסמטיקה בברלין, במשרה מלאה"),
                    ("2013", "הוא קונה ב-400 יורו ומוציא כרטיס ביקור"),
                    ("אחר כך", "נרשמתי ללמוד, כדי להיכנס למכירות בטק"),
                    ("עשור", "התאהבתי בקוד ולא מכרתי כלום"),
                    ("2026", "מבקשים ממני למכור. בפעם הראשונה מאז ברלין.")],

        "d6_kicker": "מה שעגלה בקניון מלמדת על למכור תוכנה",
        "d6_rows": [("פותחים בשאלה, לא במוצר",
                     "אף אחד לא נעצר בשביל ״קוסמטיקה מים המלח״. עוצרים בשביל ״אפשר לשאול אותך משהו?״ "
                     "גם בשביל ״אני בונה אוטומציות״ אף אחד לא נעצר."),
                    ("מדגימים על היד שלהם, לא על שלך",
                     "בעגלה שפשפתי את הקרם על היד שלהם. בתוכנה זה דמו על הדאטה שלהם, "
                     "לא הדמו המלוטש שלי.")],
    },
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#0a1628;color:#bae6fd;direction:%(dir)s;
  font-family:'IBM Plex Mono','Arial Hebrew','Arial Unicode MS',system-ui,monospace;
  background-image:linear-gradient(rgba(125,211,252,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(125,211,252,.06) 1px,transparent 1px);
  background-size:40px 40px;display:flex;flex-direction:column;justify-content:center;align-items:center;
  text-align:center;padding:52px;position:relative}
.top{position:absolute;top:36px;inset-inline-end:56px;font-size:19px;color:#7dd3fc;font-weight:700}
.rev{position:absolute;top:38px;inset-inline-start:56px;font-size:14px;letter-spacing:.14em;
  color:rgba(186,230,253,.45)}
.rev span{direction:ltr;unicode-bidi:isolate}
.num{direction:ltr;unicode-bidi:isolate;display:inline-block}
.kicker{font-size:26px;color:rgba(186,230,253,.62);margin-bottom:18px;max-width:1020px;line-height:1.34}
.claim{font-size:50px;font-weight:800;color:#e0f2fe;line-height:1.36;max-width:1050px}
.claim b{color:#fef08a}
.foot{position:absolute;bottom:34px;font-size:19px;color:rgba(186,230,253,.6)}
.foot span{direction:ltr;unicode-bidi:isolate}
.thumb{margin-top:26px;width:250px;border:2px solid rgba(125,211,252,.4)}
"""


def page(lang, css, body):
    s = S[lang]
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>'
            f'{CSS % s}{css}</style></head><body>'
            f'<div class="top">{s["top"]}</div>'
            f'<div class="rev"><span>{s["foot"]}</span></div>'
            f'{body}</body></html>')


def build(lang):
    s = S[lang]
    card = f'data:image/jpeg;base64,{CARD}'
    out = {}

    # 1 - the claim (his most-picked shape)
    out[1] = page(lang, "", (
        f'<div class="kicker">{s["d1_kicker"]}</div>'
        f'<div class="claim">{s["d1"]}</div>'
        f'<img class="thumb" src="{card}">'))

    # 2 - the artifact: the card itself, full bleed
    out[2] = page(lang, """
body{padding:0;justify-content:flex-end}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(10,22,40,.96) 0%,rgba(10,22,40,.55) 42%,rgba(10,22,40,.15) 100%)}
.cap{position:relative;font-size:40px;font-weight:800;color:#e0f2fe;line-height:1.4;
  max-width:1000px;margin-bottom:78px;text-shadow:0 2px 18px rgba(10,22,40,.9)}
.top,.rev{z-index:2;text-shadow:0 2px 10px rgba(10,22,40,.9)}
""", (
        f'<div class="bg" style="background-image:url({card})"></div>'
        f'<div class="scrim"></div>'
        f'<div class="cap">{s["d2_cap"]}</div>'))

    # 3 - the exchange (two cells)
    out[3] = page(lang, """
.cells{display:flex;gap:26px;margin-bottom:26px}
.cell{width:492px;border:2px solid rgba(125,211,252,.35);padding:26px 24px;text-align:start}
.cell.b{border-color:rgba(254,240,138,.55)}
.lab{font-size:19px;color:rgba(186,230,253,.6);margin-bottom:12px}
.big{font-size:38px;font-weight:800;color:#7dd3fc;line-height:1.3;min-height:100px}
.cell.b .big{color:#fef08a}
.note{font-size:19px;color:rgba(186,230,253,.75);line-height:1.45;margin-top:14px}
.pay{font-size:34px;font-weight:800;color:#e0f2fe}
.pay b{color:#fef08a}
""", (
        f'<div class="cells">'
        f'<div class="cell a"><div class="lab">{s["d3_a_label"]}</div>'
        f'<div class="big">{s["d3_a"]}</div><div class="note">{s["d3_a_note"]}</div></div>'
        f'<div class="cell b"><div class="lab">{s["d3_b_label"]}</div>'
        f'<div class="big">{s["d3_b"]}</div><div class="note">{s["d3_b_note"]}</div></div>'
        f'</div><div class="pay">{s["d3_foot"]}</div>'))

    # 4 - the quote
    out[4] = page(lang, """
.q{font-size:46px;font-weight:800;color:#e0f2fe;line-height:1.42;max-width:1000px}
.by{font-size:22px;color:#7dd3fc;margin-top:30px}
.thumb{margin-top:24px;width:210px}
""", (
        f'<div class="q">{s["d4_quote"]}</div>'
        f'<div class="by">{s["d4_by"]}</div>'
        f'<img class="thumb" src="{card}">'))

    # 5 - the timeline
    rows = "".join(
        f'<div class="r"><div class="y">{n(y)}</div><div class="v">{v}</div></div>'
        for y, v in s["d5_rows"])
    out[5] = page(lang, """
.kicker{margin-bottom:24px}
.rows{width:1020px;text-align:start}
.r{display:flex;gap:26px;align-items:baseline;padding:13px 4px;
  border-block-end:1px solid rgba(125,211,252,.16)}
.r:last-child{border-block-end:0}
.y{font-size:26px;font-weight:800;color:#fef08a;min-width:96px;flex:none}
.v{font-size:26px;color:#e0f2fe;line-height:1.36}
""", (
        f'<div class="kicker">{s["d5_kicker"]}</div><div class="rows">{rows}</div>'))

    # 6 - the two rules
    rules = "".join(
        f'<div class="rule"><div class="h">{h}</div><div class="p">{p}</div></div>'
        for h, p in s["d6_rows"])
    out[6] = page(lang, """
.kicker{font-size:28px;color:#7dd3fc;margin-bottom:28px}
.rules{display:flex;flex-direction:column;gap:22px;width:1030px;text-align:start}
.rule{border-inline-start:4px solid #fef08a;padding-inline-start:24px}
.h{font-size:33px;font-weight:800;color:#e0f2fe;margin-bottom:9px}
.p{font-size:21px;color:rgba(186,230,253,.78);line-height:1.5}
""", (
        f'<div class="kicker">{s["d6_kicker"]}</div><div class="rules">{rules}</div>'))

    # 7 - design 2's layout (card full bleed) carrying design 4's text (the quote)
    out[7] = page(lang, """
body{padding:0;justify-content:flex-end}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.scrim{position:absolute;inset:0;background:linear-gradient(to top,rgba(10,22,40,.97) 0%,rgba(10,22,40,.62) 46%,rgba(10,22,40,.15) 100%)}
.q{position:relative;font-size:35px;font-weight:800;color:#e0f2fe;line-height:1.42;
  max-width:1010px;padding:0 52px;text-shadow:0 2px 18px rgba(10,22,40,.95)}
.by{position:relative;font-size:20px;color:#7dd3fc;margin:18px 0 74px;padding:0 52px;
  text-shadow:0 2px 12px rgba(10,22,40,.95)}
.top,.rev{z-index:2;text-shadow:0 2px 10px rgba(10,22,40,.9)}
""", (
        f'<div class="bg" style="background-image:url({card})"></div>'
        f'<div class="scrim"></div>'
        f'<div class="q">{s["d4_quote"]}</div>'
        f'<div class="by">{s["d4_by"]}</div>'))

    for i, html in out.items():
        (OUT / f"hero-{i}-{lang}.html").write_text(html, encoding="utf-8")


for lang in ("en", "he"):
    build(lang)
print("wrote", len(list(OUT.glob("hero-*.html"))), "hero HTML files")
