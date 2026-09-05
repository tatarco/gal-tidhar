#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for "pricing the phase" (series 2/6).

One strings table drives every design so EN and HE never drift.
Chassis (BASE + per-design CSS) is shared with post 1 via _chassis.py.

Run: python3 build.py && ./shoot.sh
"""
import pathlib

OUT = pathlib.Path(__file__).parent
exec(open(OUT / "_chassis.py", encoding="utf-8").read())


def n(t):
    return f'<span class="num">{t}</span>'


S = {
    "en": {
        "dir": "ltr", "arrow": "&rarr;", "align": "left",
        "top": "freelance, part 2 of 6",

        "d1_kicker": "the hardest thing to say out loud in 2026",
        "d1": "Hours are a bad denominator, because typing is the one thing that "
              "got cheaper. <b>Risk did not. Uncertainty did not. Waiting certainly did not.</b>",

        "d2_kicker": "three anchors, all computed before I say a word",
        "d2_title": "what actually sets the number",
        "d2_rows": [("floor", "what it costs me to deliver. Never the price - it only tells me where \"I would rather not\" begins."),
                    ("value", "what this phase is worth to the client in year one."),
                    ("alternative", "what they would pay otherwise. An agency, a hire, or doing nothing.")],
        "d2_foot": "Value and alternative set the price. <b>The floor only holds a veto.</b>",

        "d3_kicker": "one week, quoted",
        "d3_a_label": "what I counted",
        "d3_a": "the work",
        "d3_a_note": "And the work really was a week.",
        "d3_b_label": "what it actually cost",
        "d3_b": "10 weeks",
        "d3_b_note": "None of the difference was hours.",
        "d3_foot": "A fixed price is not a price on work. It is <b>a price on certainty</b>.",

        "d4_kicker": "what turned one week into two and a half months",
        "d4_title": "none of it was typing",
        "d4_rows": [("2 weeks", "waiting on one person who had gone on holiday"),
                    ("4 requests", "small ones, already done before I noticed they were requests"),
                    ("1 file", "a CSV I saw for the first time the day I started the import")],

        "d5_kicker": "the class decides what you can promise, not your confidence",
        "d5": [(n("fixed"), "definable and in your hands. Commit to it."),
               (n("metered"), "depends on a system you have never seen. Meter it, or go look first."),
               (n("gated"), "waiting on an app store or a bank. Their delay, stated up front."),
               (n("not-a-build"), "cannot be typed at all. This is a discovery gate, not a build.")],
        "d5_foot": "A phase you cannot type is a guess wearing a number.",

        "d6_kicker": "the part I got backwards for a year",
        "d6": "A fixed price is not a price on the work.<br>"
              "It is a price on certainty, and <b>you are the one selling it</b>.",
        "d6_foot": "So if nothing closes the phase when the other side goes quiet, you sold certainty you do not control.",

        "foot": "2 of 6 &middot; zazet-solutions.hr",
    },
    "he": {
        "dir": "rtl", "arrow": "&larr;", "align": "right",
        "top": "פרילנס, פוסט 2 מתוך 6",

        "d1_kicker": "הדבר שהכי קשה להגיד בקול ב-2026",
        "d1": "שעות זה מכנה גרוע, כי הקלדה זה הדבר היחיד שהוזל. "
              "<b>הסיכון לא הוזל. אי הוודאות לא הוזלה. ההמתנה בטח שלא.</b>",

        "d2_kicker": "שלושה עוגנים, כולם מחושבים לפני שאני אומר מילה",
        "d2_title": "מה באמת קובע את המספר",
        "d2_rows": [("רצפה", "כמה עולה לי לספק. אף פעם לא המחיר - היא רק אומרת איפה מתחיל \"אני מעדיף לא\"."),
                    ("ערך", "כמה השלב הזה שווה ללקוח בשנה הראשונה."),
                    ("אלטרנטיבה", "מה הוא היה משלם אחרת. סוכנות, שכיר, או לא לעשות כלום.")],
        "d2_foot": "ערך ואלטרנטיבה קובעים את המחיר. <b>לרצפה יש רק זכות וטו.</b>",

        "d3_kicker": "תמחרתי שבוע עבודה",
        "d3_a_label": "מה שספרתי",
        "d3_a": "את העבודה",
        "d3_a_note": "והעבודה באמת היתה שבוע.",
        "d3_b_label": "מה שזה עלה בפועל",
        "d3_b": "חודשיים וחצי",
        "d3_b_note": "שום דבר מההפרש הזה לא היה שעות.",
        "d3_foot": "מחיר קבוע הוא לא מחיר על עבודה. הוא <b>מחיר על ודאות</b>.",

        "d4_kicker": "מה שהפך שבוע לחודשיים וחצי",
        "d4_title": "שום דבר מזה הוא לא הקלדה",
        "d4_rows": [("שבועיים", "המתנה לאדם אחד שנסע לחופש"),
                    ("4 בקשות", "קטנות, שכבר עשיתי לפני שהבנתי שהן בקשות"),
                    ("קובץ אחד", f'{n("CSV")} שראיתי בפעם הראשונה ביום שהתחלתי לכתוב את הייבוא')],

        "d5_kicker": "הסיווג קובע על מה מותר להתחייב, לא הביטחון שלך",
        "d5": [(n("fixed"), "ניתן להגדרה ובשליטה שלך. אפשר להתחייב."),
               (n("metered"), "תלוי במערכת שלא ראית. מונה, או שהולכים להסתכל קודם."),
               (n("gated"), "ממתין לחנות אפליקציות או לבנק. העיכוב שלהם, נאמר מראש."),
               (n("not-a-build"), "אי אפשר להקליד אותו בכלל. זה שלב גילוי, לא שלב בנייה.")],
        "d5_foot": "שלב שאי אפשר להקליד הוא ניחוש שלובש מספר.",

        "d6_kicker": "החלק שהבנתי הפוך במשך שנה",
        "d6": "מחיר קבוע הוא לא מחיר על העבודה.<br>"
              "הוא מחיר על ודאות, <b>ואתה זה שמוכר אותה</b>.",
        "d6_foot": "אז אם אין משפט שסוגר את השלב כשהצד השני שותק, מכרת ודאות שאתה לא שולט בה.",

        "foot": f'2 מתוך 6 &middot; {n("zazet-solutions.hr")}',
    },
}

D2B = """
.title{font-size:36px;font-weight:800;color:#e0f2fe;margin-bottom:24px}
.map{display:flex;flex-direction:column;gap:20px;width:1060px}
.mr{display:flex;align-items:baseline;gap:20px;text-align:start}
.mr .k{font-size:30px;color:#7dd3fc;font-weight:800;min-width:220px;flex:none}
.mr .v{font-size:22px;color:rgba(186,230,253,.75);line-height:1.38}
.note{font-size:29px;color:#e0f2fe;font-weight:700;margin-top:32px;max-width:1020px;line-height:1.36}
.note b{color:#fef08a}
"""

D4B = """
.title{font-size:34px;font-weight:800;color:#e0f2fe;margin-bottom:30px}
.map{display:flex;flex-direction:column;gap:22px;width:1020px}
.mr{display:flex;align-items:baseline;gap:24px;text-align:start;
  border-inline-start:3px solid rgba(254,240,138,.5);padding-inline-start:22px}
.mr .k{font-size:38px;color:#fef08a;font-weight:800;min-width:230px;flex:none}
.mr .v{font-size:23px;color:rgba(186,230,253,.75);line-height:1.38}
"""


def render(lang):
    s = S[lang]
    d = {}

    d[1] = ("", f'<div class="kicker">{s["d1_kicker"]}</div><div class="claim">{s["d1"]}</div>')

    rows = "".join(f'<div class="mr"><div class="k">{k}</div><div class="v">{v}</div></div>'
                   for k, v in s["d2_rows"])
    d[2] = (D2B, f'<div class="kicker">{s["d2_kicker"]}</div>'
                 f'<div class="title">{s["d2_title"]}</div><div class="map">{rows}</div>'
                 f'<div class="note">{s["d2_foot"]}</div>')

    # estimate -> reality, so the SECOND cell is the bad one here (inverted vs post 1)
    d[3] = (D3, f'<div class="kicker">{s["d3_kicker"]}</div><div class="pair">'
                f'<div class="cell good"><div class="lab">{s["d3_a_label"]}</div>'
                f'<div class="val">{s["d3_a"]}</div><div class="sm">{s["d3_a_note"]}</div></div>'
                f'<div class="arw">{s["arrow"]}</div>'
                f'<div class="cell bad"><div class="lab">{s["d3_b_label"]}</div>'
                f'<div class="val">{s["d3_b"]}</div><div class="sm">{s["d3_b_note"]}</div></div></div>'
                f'<div class="note">{s["d3_foot"]}</div>')

    rows4 = "".join(f'<div class="mr"><div class="k">{k}</div><div class="v">{v}</div></div>'
                    for k, v in s["d4_rows"])
    d[4] = (D4B, f'<div class="kicker">{s["d4_kicker"]}</div>'
                 f'<div class="title">{s["d4_title"]}</div><div class="map">{rows4}</div>')

    items = "".join(f'<div class="item"><div class="t">{t}</div><div class="d">{dd}</div></div>'
                    for t, dd in s["d5"])
    d[5] = (D5, f'<div class="kicker">{s["d5_kicker"]}</div><div class="list">{items}</div>'
                f'<div class="note">{s["d5_foot"]}</div>')

    d[6] = (D6, f'<div class="kicker">{s["d6_kicker"]}</div>'
                f'<div class="quote">{s["d6"]}</div><div class="punch">{s["d6_foot"]}</div>')

    for num, (extra, body) in d.items():
        html = BASE % {"dir": s["dir"], "extra": extra, "top": s["top"],
                       "body": body, "foot": s["foot"]}
        (OUT / f"hero-{num}-{lang}.html").write_text(html, encoding="utf-8")


for lang in ("en", "he"):
    render(lang)
print("wrote 12 html files to", OUT)
