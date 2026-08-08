#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for the cmux post.

One strings table drives every design so EN and HE never drift.
Bidi rules learned the hard way (see the linkedin skill):
  - every Latin run gets its own .num span with unicode-bidi:isolate,
    including two Latin runs that sit next to each other
  - direction:ltr never goes on a positioned element, only on an inner span
  - no currency symbol inside Hebrew text

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
        "top": "cmux · the terminal",

        # 1 - the one big number
        "d1_kicker": "Claude Code sessions open in one window",
        "d1_big": "26",
        "d1_sub": "across <b>7 workspaces</b>. I can tell which one wants me without opening any of them.",
        "d1_chips": ["cmux 0.64.20", "free, GPL-3", "macOS only"],

        # 2 - the claim (his proven winner shape)
        "d2_kicker": "the tool nobody I know installed",
        "d2": "I run 26 Claude Code sessions at once.<br>The terminal that makes that survivable is free, has "
              "<b>25,000 stars</b>, and almost nobody I know has heard of it.",

        # 3 - the concrete before/after
        "d3_kicker": "the same notification, two terminals",
        "d3_a_label": "any normal terminal",
        "d3_a": "&ldquo;Claude is waiting&rdquo;",
        "d3_a_note": "26 candidates. Go find it.",
        "d3_b_label": "cmux",
        "d3_b": "that pane rings",
        "d3_b_note": "Branch, PR and port, in the sidebar.",
        "d3_foot": "It does not run the work for you. It is <b>a terminal that knows an agent is running in it.</b>",

        # 4 - the mechanism
        "d4_kicker": "the mechanism worth knowing",
        "d4_title": "<b>~/.config/cmux/cmux.json</b> beats the Settings UI",
        "d4_stable": "uncommented key",
        "d4_stable_note": "file-managed. The UI cannot change it.",
        "d4_volatile": "// commented out",
        "d4_volatile_note": "handed back to the UI.",
        "d4_warn": "JSON with comments. Comment a line out to give the setting back. Reload with Cmd+Shift+, - no restart.",

        # 5 - the list
        "d5_kicker": "three settings that are not defaults. all three turn something off.",
        "d5": [("app.reorderOnNotification: false",
                "the default floats noisy workspaces to the top. At 7 workspaces that kills muscle memory."),
               ("browser.openTerminalLinksInCmuxBrowser: false",
                "cmux ships a browser. My agents already have one. Links go to the browser I am logged into."),
               ("terminal.agentHibernation.enabled: false",
                "it frees RAM by killing idle agents. I can refuse it because the IDE is not running.")],

        # 6 - the receipts
        "d6_kicker": "I diffed my tuned config against the schema defaults",
        "d6_head": ["setting", "mine", "default"],
        "d6": [("suppressSubagentNotifications", "true", "true"),
               ("autoResumeAgentSessions", "true", "true"),
               ("socketControlMode", "cmuxOnly", "cmuxOnly"),
               ("reorderOnNotification", "false", "true"),
               ("agentHibernation.enabled", "false", "false")],
        "d6_foot": "Most of my &ldquo;tuning&rdquo; was <b>the defaults, written down.</b>",

        # 7 - the memory ledger
        "d7_kicker": "where 24 GB of laptop actually goes",
        "d7_head": ["what", "resident memory"],
        "d7": [("26 Claude Code panes", "3 - 4 GB"),
               ("cmux, plus 174 shells and helpers", "0.82 GB"),
               ("PyCharm", "not running")],
        "d7_foot": "Spotlight says I last opened it on <b>11 June</b>. All my projects live in a folder called PycharmProjects.",

        "foot": "26 panes, 7 workspaces, read out of my own session file &middot; gal.tidhar.org.il",
    },
    "he": {
        "dir": "rtl", "arrow": "&larr;", "align": "right",
        "top": "cmux &middot; הטרמינל",

        "d1_kicker": "סשנים של קלוד קוד פתוחים בחלון אחד",
        "d1_big": "26",
        "d1_sub": 'ב-<b>7 מרחבי עבודה</b>. אני יודע מי מהם רוצה אותי בלי לפתוח אף אחד מהם.',
        "d1_chips": [n("cmux 0.64.20"), "חינם, קוד פתוח", "מק בלבד"],

        "d2_kicker": "הכלי שאף אחד שאני מכיר לא התקין",
        "d2": 'אני מריץ 26 סשנים של קלוד קוד במקביל.<br>הטרמינל שהופך את זה לאפשרי הוא חינמי, יש לו '
              '<b>25 אלף כוכבים</b>, וכמעט אף אחד שאני מכיר לא שמע עליו.',

        "d3_kicker": "אותה התראה, שני טרמינלים",
        "d3_a_label": "כל טרמינל רגיל",
        "d3_a": "&rdquo;קלוד מחכה לך&ldquo;",
        "d3_a_note": "26 חשודים. לך תמצא.",
        "d3_b_label": n("cmux"),
        "d3_b": "הפאנל הזה מהבהב",
        "d3_b_note": "בראנץ׳, פול ריקווסט ופורט, בסיידבר.",
        "d3_foot": "הוא לא מריץ לך את העבודה. הוא <b>טרמינל שיודע שרץ בתוכו אייג׳נט.</b>",

        "d4_kicker": "המנגנון ששווה להכיר",
        "d4_title": f'<b>{n("~/.config/cmux/cmux.json")}</b> גובר על מסך ההגדרות',
        "d4_stable": "מפתח לא מסומן כהערה",
        "d4_stable_note": "מנוהל מהקובץ. המסך לא יכול לשנות אותו.",
        "d4_volatile": n("// בהערה"),
        "d4_volatile_note": "חוזר לשליטת המסך.",
        "d4_warn": f'{n("JSON")} עם הערות. שמים שורה בהערה, וההגדרה חוזרת למסך. טוענים מחדש עם '
                   f'{n("Cmd+Shift+,")} בלי לסגור כלום.',

        "d5_kicker": "שלוש הגדרות שהן לא ברירת מחדל. שלושתן מכבות משהו.",
        "d5": [(n("app.reorderOnNotification: false"),
                "ברירת המחדל מקפיצה מרחב עבודה רועש לראש הרשימה. בשבעה מרחבים זה הורג את זיכרון השרירים."),
               (n("browser.openTerminalLinksInCmuxBrowser: false"),
                "ל-cmux יש דפדפן משלו. לאייג׳נטים שלי כבר יש אחד. הלינקים נפתחים בדפדפן שאני מחובר בו."),
               (n("terminal.agentHibernation.enabled: false"),
                "הוא משחרר זיכרון בזה שהוא הורג אייג׳נטים בטלים. אני יכול לוותר על זה כי אין לי IDE פתוח.")],

        "d6_kicker": "עשיתי דיף בין הקונפיג ה״מכוונן״ שלי לברירות המחדל בסכימה",
        "d6_head": ["הגדרה", "אצלי", "ברירת מחדל"],
        "d6": [(n("suppressSubagentNotifications"), n("true"), n("true")),
               (n("autoResumeAgentSessions"), n("true"), n("true")),
               (n("socketControlMode"), n("cmuxOnly"), n("cmuxOnly")),
               (n("reorderOnNotification"), n("false"), n("true")),
               (n("agentHibernation.enabled"), n("false"), n("false"))],
        "d6_foot": "רוב ה״כיוונון״ שלי היה <b>ברירות המחדל, כתובות בכתב יד.</b>",

        "d7_kicker": "לאן באמת הולכים 24 ג׳יגה של לפטופ",
        "d7_head": ["מה", "זיכרון בשימוש"],
        "d7": [("26 פאנלים של קלוד קוד", n("3 - 4 GB")),
               ("cmux, ועוד 174 שלים ועוזרים", n("0.82 GB")),
               ("פייצ׳ארם", "לא רץ")],
        "d7_foot": f'הספוטלייט אומר שפתחתי אותו לאחרונה ב-<b>11 ביוני</b>. כל הפרויקטים שלי יושבים בתיקייה שנקראת {n("PycharmProjects")}.',

        "foot": f'26 פאנלים, 7 מרחבי עבודה, נקראו מקובץ הסשן שלי &middot; {n("gal.tidhar.org.il")}',
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
/* isolate is not enough: a Latin run that starts with neutrals (~ / . + ,)
   takes the paragraph direction and the neutrals jump to the far end.
   The run needs its own direction, not just its own boundary. */
.num{direction:ltr;unicode-bidi:isolate;display:inline-block}
.kicker{font-size:27px;color:rgba(186,230,253,.62);margin-bottom:10px;max-width:1020px;line-height:1.34}
.big{font-size:210px;font-weight:800;line-height:.92;color:#7dd3fc;text-shadow:0 0 55px rgba(125,211,252,.5);direction:ltr}
.sub{font-size:38px;color:#e0f2fe;font-weight:700;margin-top:14px;max-width:960px;line-height:1.34}
.sub b,.claim b{color:#fef08a}
.claim{font-size:52px;font-weight:800;color:#e0f2fe;line-height:1.34;max-width:1040px}
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
.pair{display:flex;align-items:stretch;gap:40px;margin-top:6px}
.cell{padding:26px 34px;border:2px solid;width:420px;display:flex;flex-direction:column;justify-content:center}
.cell.bad{border-color:rgba(248,113,113,.65)}
.cell.good{border-color:rgba(125,211,252,.7)}
.cell .lab{font-size:21px;color:rgba(186,230,253,.66);margin-bottom:14px}
.cell .val{font-size:40px;font-weight:800;line-height:1.24}
.cell.bad .val{color:#f87171}
.cell.good .val{color:#7dd3fc;text-shadow:0 0 40px rgba(125,211,252,.45)}
.cell .sm{font-size:20px;color:rgba(186,230,253,.62);margin-top:14px;line-height:1.4}
.arw{font-size:52px;color:rgba(186,230,253,.5);align-self:center}
.note{font-size:32px;color:#e0f2fe;font-weight:700;margin-top:36px;max-width:1000px;line-height:1.36}
.note b{color:#fef08a}
"""

D4 = """
.title{font-size:42px;font-weight:800;color:#e0f2fe;margin-bottom:34px}
.title b{color:#fef08a}
.bar{display:flex;width:1000px;border:2px solid rgba(125,211,252,.55)}
.seg{padding:24px 18px}
.seg.s{flex:5;background:rgba(125,211,252,.14);border-inline-end:2px dashed rgba(125,211,252,.55)}
.seg.v{flex:3;background:rgba(254,240,138,.12)}
.seg .n{font-size:24px;font-weight:700;color:#e0f2fe}
.seg .p{font-size:20px;color:rgba(186,230,253,.7);margin-top:8px}
.seg.v .n{color:#fef08a}
.warn{font-size:26px;color:rgba(186,230,253,.8);margin-top:34px;max-width:960px;line-height:1.45}
"""

D5 = """
.list{display:flex;flex-direction:column;gap:24px;width:1050px;margin-top:14px}
.item{display:flex;align-items:baseline;gap:18px;border-inline-start:3px solid rgba(125,211,252,.55);
  padding-inline-start:20px;text-align:start}
.item .n{font-size:25px;color:#fef08a;font-weight:800;direction:ltr;min-width:26px}
.item .t{font-size:25px;color:#7dd3fc;font-weight:700}
.item .d{font-size:21px;color:rgba(186,230,253,.68);margin-top:7px;line-height:1.42}
"""

D6 = """
table{border-collapse:collapse;width:960px;margin-top:8px}
th{font-size:20px;color:rgba(186,230,253,.55);font-weight:400;padding:0 20px 14px;text-align:start;
  border-bottom:1px solid rgba(125,211,252,.3)}
td{font-size:25px;color:#e0f2fe;padding:14px 20px;text-align:start;border-bottom:1px solid rgba(125,211,252,.12)}
td.d{color:rgba(186,230,253,.55)}
tr.same td{color:rgba(186,230,253,.42)}
tr.hi td{color:#fef08a;font-weight:700}
.note{font-size:30px;color:#e0f2fe;margin-top:32px}
.note b{color:#fef08a}
"""


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
                      f'<div class="val">{s["d3_a"]}</div><div class="sm">{s["d3_a_note"]}</div></div>'
                      f'<div class="arw">{s["arrow"]}</div>'
                      f'<div class="cell good"><div class="lab">{s["d3_b_label"]}</div>'
                      f'<div class="val">{s["d3_b"]}</div><div class="sm">{s["d3_b_note"]}</div></div></div>'
                      f'<div class="note">{s["d3_foot"]}</div>')

    # 4 - the mechanism
    designs[4] = (D4, f'<div class="kicker">{s["d4_kicker"]}</div>'
                      f'<div class="title">{s["d4_title"]}</div><div class="bar">'
                      f'<div class="seg s"><div class="n">{s["d4_stable"]}</div>'
                      f'<div class="p">{s["d4_stable_note"]}</div></div>'
                      f'<div class="seg v"><div class="n">{s["d4_volatile"]}</div>'
                      f'<div class="p">{s["d4_volatile_note"]}</div></div></div>'
                      f'<div class="warn">{s["d4_warn"]}</div>')

    # 5 - the three real deviations
    items = "".join(f'<div class="item"><div class="n">{i}</div><div><div class="t">{t}</div>'
                    f'<div class="d">{d}</div></div></div>'
                    for i, (t, d) in enumerate(s["d5"], 1))
    designs[5] = (D5, f'<div class="kicker">{s["d5_kicker"]}</div><div class="list">{items}</div>')

    # 6 - the receipts: mine vs the schema default
    head = "".join(f"<th>{h}</th>" for h in s["d6_head"])
    rows = ""
    for k, mine, dflt in s["d6"]:
        same = mine == dflt
        rows += (f'<tr class="{"same" if same else "hi"}"><td>{k}</td>'
                 f'<td>{mine}</td><td class="d">{dflt}</td></tr>')
    designs[6] = (D6, f'<div class="kicker">{s["d6_kicker"]}</div>'
                      f'<table><tr>{head}</tr>{rows}</table><div class="note">{s["d6_foot"]}</div>')

    # 7 - the memory ledger: what the IDE used to hold
    rows7 = "".join(f'<tr class="{"hi" if "PyCharm" in w or "פייצ" in w else ""}">'
                    f'<td>{w}</td><td class="r">{v}</td></tr>' for w, v in s["d7"])
    head7 = "".join(f"<th>{h}</th>" for h in s["d7_head"])
    designs[7] = (D6 + ".r{color:#7dd3fc;font-weight:700}\ntable{width:820px}\n"
                       "td{font-size:29px;padding:17px 20px}\n",
                  f'<div class="kicker">{s["d7_kicker"]}</div>'
                  f'<table><tr>{head7}</tr>{rows7}</table>'
                  f'<div class="note">{s["d7_foot"]}</div>')

    for num, (extra, body) in designs.items():
        html = BASE % {"dir": s["dir"], "extra": extra, "top": s["top"],
                       "body": body, "foot": s["foot"]}
        (OUT / f"hero-{num}-{lang}.html").write_text(html, encoding="utf-8")


for lang in ("en", "he"):
    render(lang)
print("wrote 12 html files to", OUT)
