#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for the "a phase is a function" post (series 1/6).

One strings table drives every design so EN and HE never drift.
Bidi rules (see the linkedin skill): every Latin run gets .num
(direction:ltr + isolate), never direction on a positioned element,
no currency symbol inside Hebrew text.

Run: python3 build.py && ./shoot.sh
"""
import pathlib

OUT = pathlib.Path(__file__).parent


def n(t):
    """Isolate a Latin/numeric run so RTL reflow cannot reorder it."""
    return f'<span class="num">{t}</span>'


S = {
    "en": {
        "dir": "ltr", "arrow": "&rarr;", "align": "left",
        "top": "freelance, part 1 of 6",

        # 1 - the claim (his proven winner shape)
        "d1_kicker": "the thing nobody teaches a salaried developer who goes solo",
        "d1": "A phase in a project is <b>a function</b>. Without a signature, the client "
              "passes in whatever they want and you are obliged to return something.",

        # 2 - the signature (the real artifact)
        "d2_kicker": "the whole fix, in one block",
        "d2_title": "Phase 2 &middot; customer import",
        "d2_rows": [("in", "agreed CSV format, up to 50k rows"),
                    ("out", "customers in the system + an error report"),
                    ("payment", "30% deposit, balance on delivery"),
                    ("done when", "your sample file imports, bad rows are reported and do not kill the run"),
                    ("signed off by", "Dana, within 5 business days. Unavailable = approved automatically, payment released."),
                    ("not included", "data cleaning, dedupe, other formats")],
        "d2_foot": "A phase without this is <b>a function without types</b>.",

        # 3 - the exchange
        "d3_kicker": "same work, two contracts",
        "d3_a_label": "no acceptance tests",
        "d3_a": "scope creep",
        "d3_a_note": "“Great, just one more small thing.” You have no sentence to point at.",
        "d3_b_label": "acceptance test, agreed up front",
        "d3_b": "done, and paid",
        "d3_b_note": "A change request becomes a new ticket, not a free fix.",
        "d3_foot": "It is not a bad client. It is <b>a bad signature</b>.",

        # 4 - the mapping
        "d4_kicker": "you have been doing this for a decade",
        "d4_title": "you have just never seen it written in a contract",
        "d4_rows": [("the signature", "what goes in, and what has to be done with it. Scope."),
                    ("the return value", "what done looks like."),
                    ("the test", "the acceptance criterion. Written before the work, approved by the client."),
                    (n("the PR"), "the payment milestone. It does not land until it is green."),
                    ("a change request", "a new ticket. Not a free fix to a function already open.")],

        # 5 - the four jobs
        "d5_kicker": "as an employee, four other people held these and you never noticed",
        "d5": [("A product manager", "wrote what was in and what was out."),
               ("QA", "decided when it passed."),
               ("Somebody else", "defined what the output was supposed to be."),
               ("Payroll", "paid you on the 10th whether the feature shipped or not.")],
        "d5_foot": "Go freelance and all four land on you the same day.",

        # 6 - the payoff quote
        "d6_kicker": "the part that took me too long",
        "d6": "A boundary between phases is not a line on a Gantt chart.<br>"
              "It is where <b>the risk changes hands</b>.",
        "d6_foot": "Which is why discovery can cost more than build. It is not labour, it is insurance.",

        "foot": "1 of 6 &middot; zazet-solutions.hr",
    },
    "he": {
        "dir": "rtl", "arrow": "&larr;", "align": "right",
        "top": "פרילנס, פוסט 1 מתוך 6",

        "d1_kicker": "מה שאף אחד לא מלמד מתכנת שכיר שהופך לעצמאי",
        "d1": "שלב בפרויקט הוא <b>פונקציה</b>. בלי חתימה, הלקוח מעביר לתוכה מה שבא לו "
              "ואתה מחויב להחזיר משהו.",

        "d2_kicker": "כל הפתרון, בבלוק אחד",
        "d2_title": f'שלב 2 &middot; ייבוא לקוחות',
        "d2_rows": [("נכנס", f'קובץ {n("CSV")} בפורמט שסוכם, עד 50 אלף שורות'),
                    ("יוצא", "הלקוחות במערכת + דוח שגיאות"),
                    ("תשלום", "30% מקדמה, השאר במסירה"),
                    ("גמור כש", "ייבוא של קובץ הדוגמה שלכם עובר, שורות פגומות מדווחות ולא מפילות את הריצה"),
                    ("מי מאשר", "דנה, עד 5 ימי עסקים. לא זמינה - מאושר אוטומטית ותשלום משוחרר."),
                    ("לא כלול", "ניקוי דאטא, מיזוג כפילויות, פורמטים אחרים")],
        "d2_foot": "שלב בלי זה הוא <b>פונקציה בלי טייפים</b>.",

        "d3_kicker": "אותה עבודה, שני חוזים",
        "d3_a_label": "ללא מבחני קבלה",
        "d3_a": f'{n("scope creep")}',
        "d3_a_note": "“מעולה, רק עוד דבר קטן.” ואין לך שום משפט להצביע עליו.",
        "d3_b_label": "קריטריון קבלה שסוכם מראש",
        "d3_b": "גמור, ומשולם",
        "d3_b_note": "בקשת שינוי הופכת לטיקט חדש, לא לתיקון חינם.",
        "d3_foot": "זה לא לקוח רע. זו <b>חתימה גרועה</b>.",

        "d4_kicker": "אתה עושה את זה כבר עשור",
        "d4_title": "רק שמעולם לא ראית את זה כתוב בחוזה",
        "d4_rows": [("החתימה", f'מה נכנס ומה צריך לעשות איתו. {n("scope")}.'),
                    ("ערך ההחזר", "איך נראה גמור."),
                    ("הטסט", "קריטריון הקבלה. נכתב לפני העבודה, ומאושר על ידי הלקוח."),
                    (n("PR"), "אבן הדרך לתשלום. זה לא נכנס עד שזה ירוק."),
                    ("בקשת שינוי", "טיקט חדש. לא תיקון חינם לפונקציה שכבר פתוחה.")],

        "d5_kicker": "כששכיר, ארבעה אנשים אחרים החזיקו את זה בשבילך ולא שמת לב",
        "d5": [("מנהל מוצר", "כתב מה נכנס ומה לא."),
               (f'{n("QA")}', "החליט מתי זה עובר."),
               ("מישהו אחר", "הגדיר מה הפלט אמור להיות."),
               ("חשבות שכר", "העבירה משכורת ב-10 לחודש בין אם הפיצ'ר יצא ובין אם לא.")],
        "d5_foot": "ברגע שאתה עצמאי, כל הארבעה נוחתים עליך באותו יום.",

        "d6_kicker": "החלק שלקח לי יותר מדי זמן",
        "d6": "גבול בין שלבים הוא לא קו בגאנט.<br>"
              "זה המקום שבו <b>הסיכון עובר ידיים</b>.",
        "d6_foot": "ובגלל זה שלב גילוי יכול לעלות יותר משלב בנייה. הוא לא עבודה, הוא ביטוח.",

        "foot": f'1 מתוך 6 &middot; {n("zazet-solutions.hr")}',
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
.rev{position:absolute;top:38px;inset-inline-start:56px;font-size:14px;letter-spacing:.14em;
  color:rgba(186,230,253,.45)}
.rev span{direction:ltr;unicode-bidi:isolate}
.num{direction:ltr;unicode-bidi:isolate;display:inline-block}
.kicker{font-size:27px;color:rgba(186,230,253,.62);margin-bottom:14px;max-width:1020px;line-height:1.34}
.claim{font-size:52px;font-weight:800;color:#e0f2fe;line-height:1.34;max-width:1060px}
.claim b{color:#fef08a}
.foot{position:absolute;bottom:34px;font-size:20px;color:rgba(186,230,253,.6)}
.foot b{color:#e0f2fe}
%(extra)s
</style></head><body>
<div class="top">%(top)s</div><div class="rev"><span>gal.tidhar.org.il</span></div>
%(body)s
<div class="foot">%(foot)s</div>
</body></html>"""

D2 = """
.card{border:2px solid rgba(125,211,252,.55);width:1050px;text-align:start;padding:0 0 6px}
.card .hd{background:rgba(125,211,252,.12);padding:14px 28px;font-size:28px;font-weight:800;color:#7dd3fc;
  border-block-end:2px solid rgba(125,211,252,.35)}
.card .r{display:flex;gap:20px;padding:11px 28px;align-items:baseline}
.card .k{font-size:21px;color:#fef08a;font-weight:700;min-width:210px;flex:none}
.card .v{font-size:21px;color:rgba(186,230,253,.82);line-height:1.36}
.note{font-size:30px;color:#e0f2fe;font-weight:700;margin-top:26px;max-width:1020px;line-height:1.36}
.note b{color:#fef08a}
"""

D3 = """
.pair{display:flex;align-items:stretch;gap:40px;margin-top:6px}
.cell{padding:26px 34px;border:2px solid;width:420px;display:flex;flex-direction:column;justify-content:center}
.cell.bad{border-color:rgba(248,113,113,.65)}
.cell.good{border-color:rgba(125,211,252,.7)}
.cell .lab{font-size:21px;color:rgba(186,230,253,.66);margin-bottom:14px}
.cell .val{font-size:46px;font-weight:800;line-height:1.24}
.cell.bad .val{color:#f87171}
.cell.good .val{color:#7dd3fc;text-shadow:0 0 40px rgba(125,211,252,.45)}
.cell .sm{font-size:20px;color:rgba(186,230,253,.62);margin-top:14px;line-height:1.4}
.arw{font-size:52px;color:rgba(186,230,253,.5);align-self:center}
.note{font-size:30px;color:#e0f2fe;font-weight:700;margin-top:34px;max-width:1020px;line-height:1.36}
.note b{color:#fef08a}
"""

D4 = """
.title{font-size:34px;font-weight:800;color:#e0f2fe;margin-bottom:26px;max-width:1040px;line-height:1.3}
.map{display:flex;flex-direction:column;gap:13px;width:1060px}
.mr{display:flex;align-items:baseline;gap:18px;text-align:start}
.mr .k{font-size:24px;color:#7dd3fc;font-weight:800;min-width:230px;flex:none}
.mr .eq{color:rgba(186,230,253,.4);font-size:22px;flex:none}
.mr .v{font-size:22px;color:rgba(186,230,253,.75);line-height:1.36}
"""

D5 = """
.list{display:flex;flex-direction:column;gap:19px;width:1060px;margin-top:10px}
.item{display:flex;align-items:baseline;gap:18px;border-inline-start:3px solid rgba(125,211,252,.55);
  padding-inline-start:22px;text-align:start}
.item .t{font-size:26px;color:#7dd3fc;font-weight:800;min-width:250px;flex:none}
.item .d{font-size:23px;color:rgba(186,230,253,.72);line-height:1.4}
.note{font-size:30px;color:#fef08a;font-weight:800;margin-top:32px;max-width:1020px;line-height:1.36}
"""

D6 = """
.quote{font-size:48px;font-weight:800;color:#e0f2fe;line-height:1.38;max-width:1080px}
.quote b{color:#fef08a;text-shadow:0 0 45px rgba(254,240,138,.35)}
.punch{font-size:27px;color:rgba(186,230,253,.7);margin-top:34px;max-width:980px;line-height:1.4}
"""


def render(lang):
    s = S[lang]
    designs = {}

    # 1 - the claim (his proven winner)
    designs[1] = ("", f'<div class="kicker">{s["d1_kicker"]}</div><div class="claim">{s["d1"]}</div>')

    # 2 - the signature card (the real artifact)
    rows = "".join(f'<div class="r"><div class="k">{k}</div><div class="v">{v}</div></div>'
                   for k, v in s["d2_rows"])
    designs[2] = (D2, f'<div class="kicker">{s["d2_kicker"]}</div>'
                      f'<div class="card"><div class="hd">{s["d2_title"]}</div>{rows}</div>'
                      f'<div class="note">{s["d2_foot"]}</div>')

    # 3 - the exchange
    designs[3] = (D3, f'<div class="kicker">{s["d3_kicker"]}</div><div class="pair">'
                      f'<div class="cell bad"><div class="lab">{s["d3_a_label"]}</div>'
                      f'<div class="val">{s["d3_a"]}</div><div class="sm">{s["d3_a_note"]}</div></div>'
                      f'<div class="arw">{s["arrow"]}</div>'
                      f'<div class="cell good"><div class="lab">{s["d3_b_label"]}</div>'
                      f'<div class="val">{s["d3_b"]}</div><div class="sm">{s["d3_b_note"]}</div></div></div>'
                      f'<div class="note">{s["d3_foot"]}</div>')

    # 4 - the mapping, code term = deal term
    mrows = "".join(f'<div class="mr"><div class="k">{k}</div><div class="eq">=</div>'
                    f'<div class="v">{v}</div></div>' for k, v in s["d4_rows"])
    designs[4] = (D4, f'<div class="kicker">{s["d4_kicker"]}</div>'
                      f'<div class="title">{s["d4_title"]}</div>'
                      f'<div class="map">{mrows}</div>')

    # 5 - the four jobs you never owned
    items = "".join(f'<div class="item"><div class="t">{t}</div><div class="d">{d}</div></div>'
                    for t, d in s["d5"])
    designs[5] = (D5, f'<div class="kicker">{s["d5_kicker"]}</div><div class="list">{items}</div>'
                      f'<div class="note">{s["d5_foot"]}</div>')

    # 6 - the payoff quote
    designs[6] = (D6, f'<div class="kicker">{s["d6_kicker"]}</div>'
                      f'<div class="quote">{s["d6"]}</div>'
                      f'<div class="punch">{s["d6_foot"]}</div>')

    for num, (extra, body) in designs.items():
        html = BASE % {"dir": s["dir"], "extra": extra, "top": s["top"],
                       "body": body, "foot": s["foot"]}
        (OUT / f"hero-{num}-{lang}.html").write_text(html, encoding="utf-8")


for lang in ("en", "he"):
    render(lang)
print("wrote 12 html files to", OUT)
