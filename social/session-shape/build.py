#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for the session-shape post (follow-up to cache-economics).

One strings table drives every design so EN and HE never drift.
Run: python3 build.py && ./shoot.sh
"""
import pathlib

OUT = pathlib.Path(__file__).parent

S = {
    "en": {
        "dir": "ltr", "arrow": "&rarr;", "align": "left",
        "top": "Claude Code · limits",
        "d1_kicker": "my tokens per session, before and after fixing my habits",
        "d1_big": "&divide;5",
        "d1_sub": "and the cache ratio <b>never moved</b>. I was measuring the wrong thing.",
        "d1_chips": ["1,088 sessions", "8 months of logs", "5 subagents sent to check"],
        "d2": "People burn a Claude Code Max plan in days.<br>I dug through 8 months of my own logs.<br><b>These habits are the difference.</b>",
        "d2_kicker": "how not to hit your Claude Code limit",
        "d2_sub": "I built a skill that shows where you stand. I got a <b>C</b>. You?",
        "d3_kicker": "same workload, before and after the habits",
        "d3_a_label": "May", "d3_a": "9M / session",
        "d3_b_label": "August", "d3_b": "1.7M / session",
        "d3_foot": "The cache ratio between the two months: <b>76.8% vs 77.7%</b>. Not the driver.",
        "d4_kicker": "hitting your limit? you are probably measuring the wrong thing",
        "d4_wrong_label": "was measuring", "d4_wrong": "cache read %",
        "d4_right_label": "now measuring", "d4_right": "tokens per finished session",
        "d4_warn": "A high cache ratio is what a well-shaped session <b>produces</b>, not a goal.",
        "d5_kicker": "five habits that keep you under the Claude Code limit",
        "d5": [("The main thread steers, subagents work", "reads, greps and browsing go to throwaway contexts; only conclusions return"),
               ("Model routing written into CLAUDE.md", "haiku by default for read/count work - a default, not a decision"),
               ("New task = new session", "and close the one you forgot - mine ran 24 days"),
               ("Hygiene as automation", "compact at 40%, deny .env/node_modules/logs, disconnect unused MCP"),
               ("Recurring chores leave the chat", "scheduled headless runs with a fresh, tiny context")],
        "d6_kicker": "8 months of my own session logs, month by month",
        "d6_head": ["month", "sessions", "tokens/session", "quality"],
        "d6": [("April", "207", "6.4M", "67"), ("May", "188", "9.0M", "63"),
               ("June", "247", "3.2M", "63"), ("July", "259", "6.8M", "67"),
               ("August", "187", "1.7M", "77")],
        "d6_foot": "35% of historical sessions graded <b>D</b> - almost all 14-hour marathons. Learned, not talent.",
        "foot": "Measured from 8 months of my own session logs · <b>gal.tidhar.org.il</b>",
    },
    "he": {
        "dir": "rtl", "arrow": "&larr;", "align": "right",
        "top": "קלוד קוד · לימיטים",
        "d1_kicker": "הטוקנים לסשן שלי, לפני ואחרי שתיקנתי את ההרגלים",
        "d1_big": "&divide;5",
        "d1_sub": "ואחוז הקאש <b>כמעט לא זז</b>. מדדתי את הדבר הלא נכון.",
        "d1_chips": ["1,088 סשנים", "8 חודשים של לוגים", "5 סאב-אייג'נטים נשלחו לבדוק"],
        "d2": "אנשים שורפים מסלול Max תוך ימים.<br>חפרתי ב-8 חודשים של הלוגים של עצמי.<br><b>אלה ההרגלים שעושים את ההבדל.</b>",
        "d2_kicker": "איך לא להגיע ללימיט של קלוד קוד",
        "d2_sub": "בניתי סקיל שבודק איפה אתם עומדים. אני קיבלתי <b>C</b>. ואתם?",
        "d3_kicker": "אותו עומס עבודה, לפני ואחרי ההרגלים",
        "d3_a_label": "מאי", "d3_a": "9 מיליון לסשן",
        "d3_b_label": "אוגוסט", "d3_b": "1.7 מיליון לסשן",
        "d3_foot": 'אחוז הקאש בין שני החודשים: <b><span class="num">76.8%</span> מול <span class="num">77.7%</span></b>. זה לא הסיפור.',
        "d4_kicker": "נתקעים בלימיט? כנראה אתם מודדים את הדבר הלא נכון",
        "d4_wrong_label": "מדדתי", "d4_wrong": "אחוז cache reads",
        "d4_right_label": "מודד עכשיו", "d4_right": "טוקנים לסשן שהסתיים",
        "d4_warn": "אחוז קאש גבוה הוא מה שסשן בצורה טובה <b>מייצר</b>, לא מטרה.",
        "d5_kicker": "חמישה הרגלים שמשאירים אתכם מתחת ללימיט",
        "d5": [("הראשי מנווט, סאב-אייג'נטים עובדים", "קריאה, חיפוש ודפדפן יוצאים לקונטקסט זריק, חוזרת רק המסקנה"),
               ("ניתוב מודלים כתוב ב-CLAUDE.md", "הייקו כברירת מחדל לקריאה ולספירה. הגדרה, לא החלטה"),
               ("משימה חדשה = סשן חדש", "ולסגור את מה ששכחתם. אצלי אחד רץ 24 יום"),
               ("היגיינה כאוטומציה", "compact ב-40%, חסימת env./node_modules/לוגים, ניתוק MCP שלא בשימוש"),
               ("משימות חוזרות יוצאות מהצ'אט", "ריצות מתוזמנות ברקע עם קונטקסט טרי וקטן")],
        "d6_kicker": "8 חודשים של הלוגים שלי, חודש אחרי חודש",
        "d6_head": ["חודש", "סשנים", "טוקנים לסשן", "ציון"],
        "d6": [("אפריל", "207", "6.4M", "67"), ("מאי", "188", "9.0M", "63"),
               ("יוני", "247", "3.2M", "63"), ("יולי", "259", "6.8M", "67"),
               ("אוגוסט", "187", "1.7M", "77")],
        "d6_foot": '35% מהסשנים ההיסטוריים קיבלו <b>D</b>, כמעט כולם מרתונים של 14 שעות. נלמד, לא כישרון.',
        "foot": 'נמדד מ-8 חודשים של הלוגים שלי · <b><span class="num">gal.tidhar.org.il</span></b>',
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
.num{unicode-bidi:isolate;direction:ltr}
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
.cell .val{font-size:46px;font-weight:800}
.cell.bad .val{color:#f87171}
.cell.good .val{color:#7dd3fc;text-shadow:0 0 40px rgba(125,211,252,.45)}
.arw{font-size:52px;color:rgba(186,230,253,.5)}
.note{font-size:34px;color:#e0f2fe;font-weight:700;margin-top:34px}
.note b{color:#fef08a}
"""

D4 = """
.pair{display:flex;flex-direction:column;gap:22px;margin-top:6px;align-items:center}
.cell{padding:22px 44px;border:2px solid;min-width:640px}
.cell.bad{border-color:rgba(248,113,113,.65)}
.cell.good{border-color:rgba(125,211,252,.7)}
.cell .lab{font-size:21px;color:rgba(186,230,253,.66);margin-bottom:8px}
.cell .val{font-size:42px;font-weight:800}
.cell.bad .val{color:#f87171;text-decoration:line-through;text-decoration-thickness:4px}
.cell.good .val{color:#fef08a;text-shadow:0 0 40px rgba(254,240,138,.35)}
.warn{font-size:29px;color:rgba(186,230,253,.85);margin-top:30px;max-width:940px;line-height:1.45}
.warn b{color:#fef08a}
"""

D5 = """
.list{display:flex;flex-direction:column;gap:22px;width:1050px;margin-top:6px}
.item{display:flex;align-items:baseline;gap:18px;border-inline-start:3px solid rgba(125,211,252,.55);
  padding-inline-start:20px;text-align:start}
.item .n{font-size:25px;color:#fef08a;font-weight:800;direction:ltr;min-width:26px}
.item .t{font-size:28px;color:#e0f2fe;font-weight:700}
.item .d{font-size:21px;color:rgba(186,230,253,.62);margin-top:4px}
"""

D6 = """
table{border-collapse:collapse;width:940px;margin-top:8px}
th{font-size:21px;color:rgba(186,230,253,.55);font-weight:400;padding:0 20px 14px;text-align:start;
  border-bottom:1px solid rgba(125,211,252,.3)}
td{font-size:29px;color:#e0f2fe;padding:13px 20px;text-align:start;border-bottom:1px solid rgba(125,211,252,.12)}
td.n{color:#7dd3fc;font-weight:700}
td .num{unicode-bidi:isolate}
tr.hi td{color:#fef08a}
tr.hi td.n{color:#fef08a}
.note{font-size:27px;color:#e0f2fe;margin-top:28px}
.note b{color:#fef08a}
"""


def render(lang):
    s = S[lang]
    designs = {}

    # 1 - the one big number (the 5x drop)
    chips = "".join(f'<span class="chip">{c}</span>' for c in s["d1_chips"])
    designs[1] = ("", f'<div class="kicker">{s["d1_kicker"]}</div>'
                      f'<div class="big">{s["d1_big"]}</div>'
                      f'<div class="sub">{s["d1_sub"]}</div><div class="row">{chips}</div>')

    # 2 - the claim as one huge sentence (his proven winner)
    designs[2] = ('.skl{font-size:30px;color:rgba(186,230,253,.85);margin-top:34px}.skl b{color:#fef08a}',
                  f'<div class="kicker">{s["d2_kicker"]}</div><div class="claim">{s["d2"]}</div>'
                  f'<div class="skl">{s["d2_sub"]}</div>')

    # 3 - May vs August cells
    designs[3] = (D3, f'<div class="kicker">{s["d3_kicker"]}</div><div class="pair">'
                      f'<div class="cell bad"><div class="lab">{s["d3_a_label"]}</div>'
                      f'<div class="val">{s["d3_a"]}</div></div>'
                      f'<div class="arw">{s["arrow"]}</div>'
                      f'<div class="cell good"><div class="lab">{s["d3_b_label"]}</div>'
                      f'<div class="val">{s["d3_b"]}</div></div></div>'
                      f'<div class="note">{s["d3_foot"]}</div>')

    # 4 - wrong metric struck through, right metric highlighted
    designs[4] = (D4, f'<div class="kicker">{s["d4_kicker"]}</div><div class="pair">'
                      f'<div class="cell bad"><div class="lab">{s["d4_wrong_label"]}</div>'
                      f'<div class="val">{s["d4_wrong"]}</div></div>'
                      f'<div class="cell good"><div class="lab">{s["d4_right_label"]}</div>'
                      f'<div class="val">{s["d4_right"]}</div></div></div>'
                      f'<div class="warn">{s["d4_warn"]}</div>')

    # 5 - the three objections verdict list
    items = "".join(f'<div class="item"><div class="n">{i}</div><div><div class="t">{t}</div>'
                    f'<div class="d">{d}</div></div></div>'
                    for i, (t, d) in enumerate(s["d5"], 1))
    designs[5] = (D5, f'<div class="kicker">{s["d5_kicker"]}</div><div class="list">{items}</div>')

    # 6 - the monthly trend table
    head = "".join(f"<th>{h}</th>" for h in s["d6_head"])
    rows = "".join(f'<tr class="{"hi" if i in (1, 4) else ""}"><td>{m}</td>'
                   f'<td class="n"><span class="num">{c}</span></td>'
                   f'<td class="n"><span class="num">{t}</span></td>'
                   f'<td class="n"><span class="num">{q}</span></td></tr>'
                   for i, (m, c, t, q) in enumerate(s["d6"]))
    designs[6] = (D6, f'<div class="kicker">{s["d6_kicker"]}</div>'
                      f'<table><tr>{head}</tr>{rows}</table><div class="note">{s["d6_foot"]}</div>')

    # 7 - the real setup-audit scorecard (terminal output stays Latin, chrome localized)
    card = ("CLAUDE SETUP AUDIT v1\n"
            "  delegation      3.2 subagents/session       <b>A</b>\n"
            "  cheap models    60% haiku dispatches        <b>A</b>\n"
            "  prompt shape    median 56 chars             <b>A</b>\n"
            "  main context    median 244k                 <span class='c'>C</span>\n"
            "  session cost    22.9M tokens/session        <span class='f'>F</span>\n"
            "  marathons       longest ran 24d             <span class='f'>F</span>\n"
            "  setup overhead  ~6.7k before turn one       <span class='c'>C</span>\n"
            "  ----------------------------------------------\n"
            "  AUDIT           <span class='c'>C</span>")
    d7_kicker = ("בניתי סקיל שנותן לסטאפ הקלוד קוד שלכם ציון. אני קיבלתי C." if lang == "he"
                 else "I built a skill that grades your Claude Code setup. I got a C.")
    d7_foot = ("setup-audit: חינם, רץ לוקאלית, לינק בתגובה הראשונה. תדביקו את הבלוק שלכם" if lang == "he"
               else "setup-audit: free, runs locally, link in the first comment - paste your block")
    D7 = """
.card{direction:ltr;text-align:left;font-size:21px;line-height:1.55;color:#bae6fd;
  border:2px solid rgba(125,211,252,.55);padding:18px 36px;background:rgba(0,0,0,.25);
  white-space:pre}
.card b{color:#7dd3fc;font-weight:800}
.card .c{color:#fef08a;font-weight:800}
.card .f{color:#f87171;font-weight:800}
.k2{font-size:29px;color:#e0f2fe;font-weight:700;margin:26px 0 16px}
.f2{font-size:21px;color:rgba(186,230,253,.7);margin:16px 0 30px}
"""
    designs[7] = (D7, f'<div class="k2">{d7_kicker}</div>'
                      f'<div class="card">{card}</div>'
                      f'<div class="f2">{d7_foot}</div>')

    for n, (extra, body) in designs.items():
        html = BASE % {"dir": s["dir"], "extra": extra, "top": s["top"],
                       "body": body, "foot": s["foot"]}
        (OUT / f"hero-{n}-{lang}.html").write_text(html, encoding="utf-8")


for lang in ("en", "he"):
    render(lang)
print("wrote html files to", OUT)
