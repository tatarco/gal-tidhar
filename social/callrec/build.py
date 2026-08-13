#!/usr/bin/env python3
"""Render 6 hero designs x {en,he} for the callrec post.

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
        "top": "callrec · local call recording",

        # 1 - the one big number
        "d1_kicker": "per month for call recording. And no bytes leaving the laptop.",
        "d1_big": "0",
        "d1_sub": "Any platform. Both sides of the call. <b>Transcript straight into Claude.</b>",
        "d1_chips": ["Zoom, Meet, WhatsApp", "records both sides", "open source"],

        # 2 - the claim (his proven winner shape)
        "d2_kicker": "no bot in the call, no monthly bill",
        "d2": "Every call - Zoom, Meet, WhatsApp, a phone on speaker - recorded, transcribed on "
              "this Mac, and <b>handed straight to Claude</b> as the client's own words.",

        # 3 - the exchange: what you get with and without the virtual driver
        "d3_kicker": "the same call, two setups",
        "d3_a_label": "microphone only",
        "d3_a": "a monologue",
        "d3_a_note": "Everything the other side said is missing.",
        "d3_b_label": "microphone + BlackHole",
        "d3_b": "a conversation",
        "d3_b_note": "System audio looped back in as an input.",
        "d3_foot": "macOS records <b>inputs</b>. Your speakers are an output, and no API hands you what goes to them.",

        # 4 - the architecture
        "d4_kicker": "three pieces, each replaceable",
        "d4_title": "what actually runs",
        "d4_steps": [("BlackHole 2ch", "virtual driver. Turns system output into a recordable input."),
                     ("ffmpeg", "records mic + system, mixes to one track."),
                     ("whisper.cpp", "transcribes on the GPU. Auto-detects language per segment.")],
        "d4_warn": "Everything on this list was already installable on your machine. This is the glue.",

        # 5 - the breakdown: the undocumented bit
        "d5_kicker": "the part that is not written down anywhere obvious",
        "d5": [("A Multi-Output Device is just an aggregate device with kAudioAggregateDeviceIsStackedKey = 1",
                "So you can create it in code instead of asking someone to click it together in Audio MIDI Setup."),
               ("Real hardware is the clock master, drift correction goes on the virtual device",
                "BlackHole has no crystal of its own and slides out of sync without it."),
               ("Selecting a Multi-Output Device kills your volume keys",
                "Which is why the script switches to it on start and switches back on stop. Otherwise you stop using it.")],

        # 6 - the payoff quote
        "d6_kicker": "why I actually built it",
        "d6": "My memory of a client call is a summary<br>written by the guy who wanted the deal to go well.",
        "d6_foot": "The transcript is not.",

        "foot": "350 lines, MIT &middot; gal.tidhar.org.il",
    },
    "he": {
        "dir": "rtl", "arrow": "&larr;", "align": "right",
        "top": f'{n("callrec")} &middot; הקלטת שיחות מקומית',

        "d1_kicker": "שקלים בחודש על הקלטת שיחות. וגם אפס בייטים שיוצאים מהלפטופ.",
        "d1_big": "0",
        "d1_sub": "כל פלטפורמה. שני צדדי השיחה. <b>והתמלול נכנס ישר לקלוד.</b>",
        "d1_chips": ["זום, מיט, וואטסאפ", "מקליט את שני הצדדים", "קוד פתוח"],

        "d2_kicker": "בלי בוט בשיחה, בלי חיוב חודשי",
        "d2": "כל שיחה - זום, מיט, וואטסאפ, טלפון על רמקול - מוקלטת, מתומללת על המק הזה, "
              "ונכנסת <b>ישר לקלוד</b> במילים של הלקוח עצמו.",

        "d3_kicker": "אותה שיחה, שני סטאפים",
        "d3_a_label": "מיקרופון בלבד",
        "d3_a": "מונולוג",
        "d3_a_note": "כל מה שהצד השני אמר פשוט חסר.",
        "d3_b_label": f'מיקרופון + {n("BlackHole")}',
        "d3_b": "שיחה",
        "d3_b_note": "פלט המערכת חוזר פנימה בתור קלט.",
        "d3_foot": "מק מקליט <b>קלטים</b>. הרמקולים הם פלט, ואין שום ממשק שנותן לך את מה שהולך אליהם.",

        "d4_kicker": "שלושה חלקים, כל אחד מהם ניתן להחלפה",
        "d4_title": "מה באמת רץ שם",
        "d4_steps": [(n("BlackHole 2ch"), "דרייבר וירטואלי. הופך את פלט המערכת לקלט שאפשר להקליט."),
                     (n("ffmpeg"), "מקליט מיקרופון ומערכת, ומערבב לטראק אחד."),
                     (n("whisper.cpp"), "מתמלל על ה-GPU. מזהה שפה לכל סגמנט בנפרד.")],
        "d4_warn": "כל מה שברשימה הזאת כבר היה מותקן אצלך במרחק פקודה. זה רק הדבק.",

        "d5_kicker": "החלק שלא כתוב בשום מקום ברור",
        "d5": [(f'{n("Multi-Output Device")} הוא פשוט {n("aggregate device")} עם {n("kAudioAggregateDeviceIsStackedKey")} על 1',
                "כלומר אפשר לייצר אותו בקוד, במקום לבקש מאנשים להרכיב אותו בעכבר במסך ההגדרות."),
               ("החומרה האמיתית היא שעון המאסטר, ותיקון הסחיפה יושב על המכשיר הווירטואלי",
                f'ל-{n("BlackHole")} אין גביש משלו, ובלי זה הוא נסחף מהסנכרון לאט לאט.'),
               ("כשמכשיר פלט מרובה נבחר, מקשי עוצמת הקול מפסיקים לעבוד",
                "ובגלל זה הסקריפט מחליף אליו בהתחלה ומחזיר בסוף. אחרת פשוט מפסיקים להשתמש בזה.")],

        "d6_kicker": "למה בכלל בניתי את זה",
        "d6": "הזיכרון שלי משיחה עם לקוח הוא סיכום<br>שכתב הבחור שרצה שהעסקה תצא לפועל.",
        "d6_foot": "התמלול הוא לא.",

        "foot": f'350 שורות, קוד פתוח &middot; {n("gal.tidhar.org.il")}',
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
.cell .val{font-size:46px;font-weight:800;line-height:1.24}
.cell.bad .val{color:#f87171}
.cell.good .val{color:#7dd3fc;text-shadow:0 0 40px rgba(125,211,252,.45)}
.cell .sm{font-size:20px;color:rgba(186,230,253,.62);margin-top:14px;line-height:1.4}
.arw{font-size:52px;color:rgba(186,230,253,.5);align-self:center}
.note{font-size:30px;color:#e0f2fe;font-weight:700;margin-top:36px;max-width:1020px;line-height:1.36}
.note b{color:#fef08a}
"""

D4 = """
.title{font-size:40px;font-weight:800;color:#e0f2fe;margin-bottom:28px}
.chain{display:flex;align-items:stretch;gap:0;width:1060px}
.box{flex:1;border:2px solid rgba(125,211,252,.55);padding:22px 18px;display:flex;
  flex-direction:column;justify-content:flex-start}
.box+.box{border-inline-start:none}
.box .n{font-size:25px;font-weight:800;color:#7dd3fc;margin-bottom:10px}
.box .p{font-size:19px;color:rgba(186,230,253,.7);line-height:1.42}
.warn{font-size:26px;color:rgba(186,230,253,.8);margin-top:32px;max-width:980px;line-height:1.45}
"""

D5 = """
.list{display:flex;flex-direction:column;gap:22px;width:1070px;margin-top:14px}
.item{display:flex;align-items:baseline;gap:18px;border-inline-start:3px solid rgba(125,211,252,.55);
  padding-inline-start:20px;text-align:start}
.item .n{font-size:25px;color:#fef08a;font-weight:800;direction:ltr;min-width:26px}
.item .t{font-size:24px;color:#7dd3fc;font-weight:700;line-height:1.36}
.item .d{font-size:20px;color:rgba(186,230,253,.68);margin-top:7px;line-height:1.42}
"""

D6 = """
.quote{font-size:50px;font-weight:800;color:#e0f2fe;line-height:1.38;max-width:1060px}
.punch{font-size:56px;font-weight:800;color:#fef08a;margin-top:34px;
  text-shadow:0 0 45px rgba(254,240,138,.35)}
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

    # 3 - the exchange
    designs[3] = (D3, f'<div class="kicker">{s["d3_kicker"]}</div><div class="pair">'
                      f'<div class="cell bad"><div class="lab">{s["d3_a_label"]}</div>'
                      f'<div class="val">{s["d3_a"]}</div><div class="sm">{s["d3_a_note"]}</div></div>'
                      f'<div class="arw">{s["arrow"]}</div>'
                      f'<div class="cell good"><div class="lab">{s["d3_b_label"]}</div>'
                      f'<div class="val">{s["d3_b"]}</div><div class="sm">{s["d3_b_note"]}</div></div></div>'
                      f'<div class="note">{s["d3_foot"]}</div>')

    # 4 - the architecture
    boxes = "".join(f'<div class="box"><div class="n">{t}</div><div class="p">{d}</div></div>'
                    for t, d in s["d4_steps"])
    designs[4] = (D4, f'<div class="kicker">{s["d4_kicker"]}</div>'
                      f'<div class="title">{s["d4_title"]}</div>'
                      f'<div class="chain">{boxes}</div>'
                      f'<div class="warn">{s["d4_warn"]}</div>')

    # 5 - the breakdown of the undocumented parts
    items = "".join(f'<div class="item"><div class="n">{i}</div><div><div class="t">{t}</div>'
                    f'<div class="d">{d}</div></div></div>'
                    for i, (t, d) in enumerate(s["d5"], 1))
    designs[5] = (D5, f'<div class="kicker">{s["d5_kicker"]}</div><div class="list">{items}</div>')

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
