#!/usr/bin/env python3
"""Generate 6 hero designs x 2 languages for the usage-grade post.

One strings table, six layouts. Run, then screenshot each with headless Chrome.
"""
import json
import os
import pathlib

HERE = pathlib.Path(__file__).parent

S = {
    "en": {
        "dir": "ltr",
        "eyebrow": "CLAUDE CODE / CACHE ECONOMICS",
        "foot": "gal.tidhar.org.il",
        # 1 report card
        "r_title": "I graded my own usage",
        "r_rows": [
            ("cache reads", "96.4%", "A"),
            ("cold restarts", "0.9%", "A"),
            ("median context", "243k", "C"),
            ("longest session", "24d / 7,196 turns", "F"),
        ],
        "r_grade": "GRADE",
        "r_gradeval": "C",
        "r_fix": "One session open 24 days = 17% of my month.",
        # 2 big number
        "b_kicker": "one session I forgot to close",
        "b_num": "24",
        "b_unit": "days",
        "b_sub": "It ate a sixth of my month on its own.",
        # 3 the claim
        "c_lead": "Every word in the conversation",
        "c_hit": "is re-read on every turn",
        "c_tail": "until the session ends.",
        "c_sub": "Cost = size x turns remaining.",
        # 4 exchange
        "x_q_who": "the pushback",
        "x_q": "Measure what comes back from a subagent, not what goes in.",
        "x_a_who": "the logs",
        "x_a": "Right, and sharper: it is not one payment. It is one per remaining turn.",
        # 5 grid
        "g_title": "Four numbers that decide your bill",
        "g_cells": [
            ("cache reads", "is the prefix stable"),
            ("cold restarts", "did you return after an hour"),
            ("median context", "how big is every re-read"),
            ("longest session", "how many times is it re-read"),
        ],
        # 6 quote
        "q_strike": "discipline",
        "q_real": "tempo",
        "q_lead": "I thought it was",
        "q_mid": "It was",
        "q_sub": "92% of my messages are sent under a minute after the last one.",
    },
    "he": {
        "dir": "rtl",
        "eyebrow": "קלוד קוד / כלכלת המטמון",
        "foot": "gal.tidhar.org.il",
        "r_title": "נתתי לעצמי ציון",
        "r_rows": [
            ("קריאות מטמון", "96.4%", "A"),
            ("התחלות קרות", "0.9%", "A"),
            ("חציון קונטקסט", "243k", "C"),
            ("הסשן הארוך ביותר", "24 ימים", "F"),
        ],
        "r_grade": "ציון",
        "r_gradeval": "C",
        "r_fix": "סשן אחד פתוח 24 יום = שישית מהחודש שלי.",
        "b_kicker": "סשן אחד ששכחתי לסגור",
        "b_num": "24",
        "b_unit": "ימים",
        "b_sub": "הוא לבדו אכל שישית מהחודש.",
        "c_lead": "כל מילה שנמצאת בשיחה",
        "c_hit": "נקראת מחדש בכל תור",
        "c_tail": "עד שהסשן נסגר.",
        "c_sub": "העלות = גודל כפול תורים שנשארו.",
        "x_q_who": "התגובה",
        "x_q": "תמדוד מה חוזר מסאב-אייג'נט, לא מה נכנס אליו.",
        "x_a_who": "הלוגים",
        "x_a": "נכון, ואפילו חד יותר: זה לא תשלום אחד. זה אחד לכל תור שנשאר.",
        "g_title": "ארבעה מספרים שקובעים את החשבון",
        "g_cells": [
            ("קריאות מטמון", "האם הפרפיקס יציב"),
            ("התחלות קרות", "חזרת אחרי שעה"),
            ("חציון קונטקסט", "כמה גדולה כל קריאה"),
            ("הסשן הארוך ביותר", "כמה פעמים נקרא מחדש"),
        ],
        "q_strike": "משמעת",
        "q_real": "קצב",
        "q_lead": "חשבתי שזו",
        "q_mid": "זה היה",
        "q_sub": "92% מההודעות שלי נשלחות פחות מדקה אחרי הקודמת.",
    },
}

CSS = """
@font-face{font-family:'IBM Plex Mono';font-weight:400;src:url('FONTDIR/ibm-plex-mono-400.woff2') format('woff2');}
@font-face{font-family:'IBM Plex Mono';font-weight:600;src:url('FONTDIR/ibm-plex-mono-600.woff2') format('woff2');}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0a1628;--grid:rgba(125,211,252,.07);--cyan:#7dd3fc;--ink:#e0f2fe;
--muted:rgba(186,230,253,.55);--accent:#fef08a;--red:#fca5a5;--border:rgba(125,211,252,.45)}
html,body{width:1200px;height:630px}
body{font-family:'IBM Plex Mono','Arial Hebrew','Arial Unicode MS',monospace;background:var(--bg);
color:var(--ink);overflow:hidden;
background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
background-size:32px 32px}
.wrap{width:1200px;height:630px;padding:52px 64px;display:flex;flex-direction:column;position:relative}
.eyebrow{font-size:17px;letter-spacing:.16em;color:var(--cyan);opacity:.85;font-weight:600}
.foot{position:absolute;inset-inline-start:64px;bottom:34px;font-size:16px;color:var(--muted);direction:ltr}
.spacer{flex:1}
.accent{color:var(--accent)}.cy{color:var(--cyan)}.red{color:var(--red)}
"""


def page(lang, body, extra=""):
    d = S[lang]["dir"]
    fontdir = "file://" + os.path.expanduser("~/PycharmProjects/gal-tidhar/fonts")
    css = CSS.replace("FONTDIR", fontdir) + extra
    return f"""<!DOCTYPE html><html lang="{lang}" dir="{d}"><head><meta charset="utf-8">
<style>{css}</style></head><body><div class="wrap">{body}</div></body></html>"""


def d1_report(t):
    rows = "".join(
        f'<div class="row"><span class="k">{k}</span><span class="v">{v}</span>'
        f'<span class="g g{g}">{g}</span></div>'
        for k, v, g in t["r_rows"]
    )
    body = f"""<div class="eyebrow">{t['eyebrow']}</div>
<div class="h">{t['r_title']}</div>
<div class="card">{rows}
<div class="rule"></div>
<div class="row total"><span class="k">{t['r_grade']}</span><span class="v"></span><span class="g gC">{t['r_gradeval']}</span></div>
</div>
<div class="fix">{t['r_fix']}</div>
<div class="spacer"></div><div class="foot">{t['foot']}</div>"""
    extra = """
.h{font-size:44px;font-weight:600;margin:18px 0 22px}
.card{border:1px solid var(--border);border-radius:10px;padding:22px 30px;background:rgba(15,40,71,.5)}
.row{display:flex;align-items:center;gap:20px;padding:9px 0;font-size:27px}
.k{flex:1;color:var(--ink)}.v{color:var(--muted);font-size:24px}
.g{width:52px;text-align:center;font-weight:600;font-size:31px}
.gA{color:var(--cyan)}.gC{color:var(--accent)}.gF{color:var(--red)}
.rule{height:1px;background:var(--border);margin:12px 0}
.total .k{font-weight:600;letter-spacing:.1em}
.fix{margin-top:22px;font-size:25px;color:var(--accent)}
"""
    return body, extra


def d2_bignum(t):
    body = f"""<div class="eyebrow">{t['eyebrow']}</div>
<div class="spacer"></div>
<div class="kick">{t['b_kicker']}</div>
<div class="numline"><span class="num">{t['b_num']}</span><span class="unit">{t['b_unit']}</span></div>
<div class="sub">{t['b_sub']}</div>
<div class="spacer"></div><div class="foot">{t['foot']}</div>"""
    extra = """
.kick{font-size:30px;color:var(--muted)}
.numline{display:flex;align-items:baseline;gap:22px;margin:6px 0 14px}
.num{font-size:210px;font-weight:600;line-height:1;color:var(--red)}
.unit{font-size:56px;color:var(--ink)}
.sub{font-size:31px;color:var(--accent)}
"""
    return body, extra


def d3_claim(t):
    body = f"""<div class="eyebrow">{t['eyebrow']}</div>
<div class="spacer"></div>
<div class="line">{t['c_lead']}</div>
<div class="hit">{t['c_hit']}</div>
<div class="line">{t['c_tail']}</div>
<div class="sub">{t['c_sub']}</div>
<div class="spacer"></div><div class="foot">{t['foot']}</div>"""
    extra = """
.line{font-size:46px;line-height:1.35;color:var(--ink)}
.hit{font-size:52px;font-weight:600;color:var(--accent);line-height:1.35;
border-bottom:3px solid var(--accent);align-self:flex-start;padding-bottom:4px;margin:4px 0}
.sub{margin-top:30px;font-size:29px;color:var(--cyan)}
"""
    return body, extra


def d4_exchange(t):
    body = f"""<div class="eyebrow">{t['eyebrow']}</div>
<div class="spacer"></div>
<div class="blk q"><div class="who">{t['x_q_who']}</div><div class="txt">{t['x_q']}</div></div>
<div class="blk a"><div class="who cy">{t['x_a_who']}</div><div class="txt">{t['x_a']}</div></div>
<div class="spacer"></div><div class="foot">{t['foot']}</div>"""
    extra = """
.blk{border-inline-start:4px solid var(--border);padding-inline-start:26px;margin:20px 0}
.blk.a{border-inline-start-color:var(--accent)}
.who{font-size:20px;letter-spacing:.14em;color:var(--muted);margin-bottom:10px}
.txt{font-size:36px;line-height:1.4}
.blk.a .txt{color:var(--accent)}
"""
    return body, extra


def d5_grid(t):
    cells = "".join(
        f'<div class="cell"><div class="n">{i + 1}</div><div class="ct">{k}</div>'
        f'<div class="cs">{v}</div></div>'
        for i, (k, v) in enumerate(t["g_cells"])
    )
    body = f"""<div class="eyebrow">{t['eyebrow']}</div>
<div class="h">{t['g_title']}</div>
<div class="grid">{cells}</div>
<div class="spacer"></div><div class="foot">{t['foot']}</div>"""
    extra = """
.h{font-size:42px;font-weight:600;margin:16px 0 26px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.cell{border:1px solid var(--border);border-radius:10px;padding:20px 24px;background:rgba(15,40,71,.5)}
.n{font-size:20px;color:var(--cyan);font-weight:600;margin-bottom:6px}
.ct{font-size:30px;font-weight:600;color:var(--ink)}
.cs{font-size:22px;color:var(--muted);margin-top:6px}
"""
    return body, extra


def d6_quote(t):
    body = f"""<div class="eyebrow">{t['eyebrow']}</div>
<div class="spacer"></div>
<div class="l1">{t['q_lead']} <span class="strike">{t['q_strike']}</span></div>
<div class="l2">{t['q_mid']} <span class="real">{t['q_real']}</span></div>
<div class="sub">{t['q_sub']}</div>
<div class="spacer"></div><div class="foot">{t['foot']}</div>"""
    extra = """
.l1{font-size:56px;color:var(--muted);line-height:1.3}
.strike{position:relative;color:var(--muted)}
.strike::after{content:'';position:absolute;inset-inline:-6px;top:52%;height:5px;
background:var(--red);border-radius:3px}
.l2{font-size:74px;font-weight:600;margin-top:10px;line-height:1.25}
.real{color:var(--accent)}
.sub{margin-top:34px;font-size:28px;color:var(--cyan)}
"""
    return body, extra


DESIGNS = [
    ("1-report", d1_report),
    ("2-bignum", d2_bignum),
    ("3-claim", d3_claim),
    ("4-exchange", d4_exchange),
    ("5-grid", d5_grid),
    ("6-quote", d6_quote),
]

if __name__ == "__main__":
    made = []
    for lang in ("en", "he"):
        for name, fn in DESIGNS:
            body, extra = fn(S[lang])
            out = HERE / f"hero-{name}-{lang}.html"
            out.write_text(page(lang, body, extra), encoding="utf-8")
            made.append(out.name)
    print("\n".join(made))
