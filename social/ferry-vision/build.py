#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the ferry-vision post (episode 3: the queue light)."""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
L = '<span class="ltr">{}</span>'.format

# The real distribution, if it has been measured (scratchpad/hist.py writes it).
HIST = os.path.join(HERE, 'hist.json')
BINS = json.load(open(HIST))['bins'] if os.path.exists(HIST) else \
    [31, 58, 44, 22, 11, 6, 4, 3, 5, 7, 9, 8, 6, 4, 3, 2, 1, 1, 0, 0]

S = {
 'en': {
   'dir': 'ltr', 'lang': 'en',
   'eyebrow': 'THE BEST MARITIME PORTAL IN CROATIA / EPISODE 3',
   'shot_title': 'Merag, 10 Sept, 17:16. The light is red.',
   'chips': [('GREEN', 'The queue has reached the approach road.<br>Median 18 minutes to full.'),
             ('YELLOW', 'The queue is halfway up the road.<br>Median 14 minutes to full.'),
             ('RED', 'A vehicle standing at the far bend.<br>The port is full.')],
   'inset_cap': 'Green and yellow, camera 487',
   'claim': 'The hard part to copy<br>is not the model.<br>'
            '<span class="hi">It is the picture of that<br>road empty at 07:00.</span>',
   'claim_foot': 'Every marked square has a reference of what it looks like empty at that hour - a per-pixel '
                 'median across nine days. A car does not survive a median; tarmac, paint and shadows do. '
                 'A detector is a five-minute pip install. 311,537 frames of one road at every hour is thirteen days of standing there.',
   'before_l': 'WHAT I STOPPED MEASURING',
   'before_v': '<div class="r">How many cars are waiting</div>'
               '<span class="sm">A ferry here takes 100+ vehicles and the camera sees a small part of them. '
               'Any number I print is falsely precise. Gal\'s rule: never print a count.</span>',
   'after_l': 'WHAT I MEASURE INSTEAD',
   'after_v': '<div class="r">Is this patch of road<br>still road</div>'
              '<span class="sm">Appearance, not detection. The fraction of pixels that no longer match '
              'an empty-road reference for that hour. Two humps, and the threshold sits in the valley.</span>',
   'hist_title': 'ONE ZONE, THREE DAYS, EVERY FIVE MINUTES',
   'hist_x': 'fraction of the square that no longer looks like empty road',
   'hist_a': 'empty road',
   'hist_b': 'occupied',
   'hist_thr': 'threshold 0.20',
   'hist_note': 'The threshold is the valley between the two humps. Nobody picked it by hand.',
   'grid_title': 'WHAT THE CAMERA SAW AT MERAG, 8 SEPTEMBER',
   'grid': [('Departures printed in the timetable', '13'),
            ('Departures the ramp camera actually saw', '16'),
            ('How the ship is told from the sea', 'edge density'),
            ('Empty ramp / ship alongside', '0.05-0.14 / 0.21-0.28'),
            ('Ship alongside, relative to its printed time', '-25 min to +5'),
            ('Frames kept, five cameras, since 29 Aug', '311,537')],
   'grid_foot': 'The timetable says what was printed in June. The camera says what left today.',
   'big': '50 minutes',
   'big_unit': 'From a queue past the bend back to an empty road. One sailing.',
   'big_sub': 'Red at 17:17. <span class="cy">One ferry left at 17:33 and took all of it.</span><br>'
              'Green at 18:07. So the page stopped writing your sailing off when<br>'
              'the road is full - <span class="hi">it says what it measured and leaves you the photograph.</span>',
   'foot_pos': 'left:44px',
   'foot': 'croatianferries.com',
 },
 'he': {
   'dir': 'rtl', 'lang': 'he',
   'eyebrow': 'הפורטל הימי הכי טוב בקרואטיה / פרק 3',
   'shot_title': 'מרג, 10.9, 17:16. הרמזור אדום.',
   'chips': [('ירוק', 'התור הגיע לכביש הגישה.<br>חציון 18 דקות עד מלא.'),
             ('צהוב', 'התור באמצע הדרך.<br>חציון 14 דקות עד מלא.'),
             ('אדום', 'רכב עומד בסיבוב הרחוק.<br>הנמל מלא.')],
   'inset_cap': 'ירוק וצהוב, מצלמה 487',
   'claim': 'מה שקשה להעתיק פה<br>זה לא המודל.<br>'
            '<span class="hi">זו התמונה של הכביש<br>הריק בשבע בבוקר.</span>',
   'claim_foot': 'לכל ריבוע מסומן יש תמונת ייחוס של איך הוא נראה ריק בשעה הזאת, חציון פר-פיקסל על תשעה ימים. '
                 'מכונית לא שורדת חציון, אספלט וסימוני צבע כן. דיטקטור זה '
                 + L('pip install') + ' של חמש דקות. 311,537 פריימים של כביש אחד בכל שעה זה שלושה עשר ימים של לעמוד שם.',
   'before_l': 'מה הפסקתי למדוד',
   'before_v': '<div class="r">כמה מכוניות מחכות</div>'
               '<span class="sm">מעבורת פה לוקחת 100 רכבים ומעלה והמצלמה רואה חלק קטן מהם. '
               'כל מספר שאדפיס יהיה מדויק לכאורה. הכלל: לא מדפיסים ספירה.</span>',
   'after_l': 'מה אני מודד במקום',
   'after_v': '<div class="r">האם החתיכה הזאת<br>עדיין כביש</div>'
              '<span class="sm">מראה, לא זיהוי. איזה אחוז מהפיקסלים כבר לא מתאים לתמונת ייחוס של כביש ריק '
              'באותה שעה. שתי גבנוניות, והסף יושב בעמק שביניהן.</span>',
   'hist_title': 'אזור אחד, שלושה ימים, כל חמש דקות',
   'hist_x': 'איזה חלק מהריבוע כבר לא נראה ככביש ריק',
   'hist_a': 'כביש ריק',
   'hist_b': 'תפוס',
   'hist_thr': 'הסף, 0.20',
   'hist_note': 'הסף הוא העמק שבין שתי הגבנוניות. אף אחד לא בחר אותו ביד.',
   'grid_title': 'מה המצלמה ראתה במרג, 8 בספטמבר',
   'grid': [('יציאות שמודפסות בלוח הזמנים', '13'),
            ('יציאות שמצלמת הרמפה באמת ראתה', '16'),
            ('איך מבדילים אונייה מים', 'צפיפות קצוות'),
            ('רמפה ריקה / אונייה עליה', L('0.05-0.14 / 0.21-0.28')),
            ('אונייה על הרמפה, יחסית לשעה המודפסת', L('25- עד 5+ דקות')),
            ('פריימים שמורים, חמש מצלמות, מאז 29.8', '311,537')],
   'grid_foot': 'לוח הזמנים אומר מה הודפס ביוני. המצלמה אומרת מה יצא היום.',
   'big': '50 דקות',
   'big_unit': 'מתור שעבר את הסיבוב עד כביש ריק. הפלגה אחת.',
   'big_sub': 'אדום ב-17:17. <span class="cy">מעבורת אחת יצאה ב-17:33 ולקחה את כולם.</span><br>'
              'ירוק ב-18:07. אז הדף הפסיק למחוק לך את ההפלגה כשהכביש מלא -<br>'
              '<span class="hi">הוא אומר מה שהוא מדד ומשאיר לך את התמונה.</span>',
   'foot_pos': 'right:44px',
   'foot': 'croatianferries.com',
 },
}

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#0a1628;color:#e2e8f0;
 font-family:"IBM Plex Mono","Arial Hebrew","Arial Unicode MS",monospace;
 overflow:hidden;position:relative}
body::before{content:"";position:absolute;inset:0;
 background-image:linear-gradient(rgba(125,211,252,.055) 1px,transparent 1px),
                  linear-gradient(90deg,rgba(125,211,252,.055) 1px,transparent 1px);
 background-size:44px 44px}
.wrap{position:relative;height:100%;padding:56px 68px;display:flex;flex-direction:column}
.eyebrow{font-size:15px;letter-spacing:.22em;color:#7dd3fc;opacity:.85;margin-bottom:auto}
.foot{position:absolute;inset-block-end:34px;inset-inline-start:68px;
 font-size:15px;color:#64748b;direction:ltr}
.hi{color:#fef08a}
.cy{color:#7dd3fc}
.sm{font-size:.55em;color:#94a3b8;font-weight:400;display:inline-block;margin-top:14px;line-height:1.5}
.ltr{direction:ltr;unicode-bidi:isolate;display:inline-block;text-align:left}
"""

TPL = """<!doctype html><html dir="{dir}" lang="{lang}"><meta charset="utf-8">
<style>{css}{extra}</style><body>{raw}<div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def design1(s):  # the frame itself, with the three zones drawn on it
    extra = """
    body{padding:0}
    .shot{position:absolute;inset:0 0 148px 0;overflow:hidden}
    .shot img{width:100%;height:100%;object-fit:cover;object-position:50% 42%}
    .veil{position:absolute;inset:0 0 148px 0;
     background:linear-gradient(180deg,rgba(10,22,40,.86) 0,rgba(10,22,40,0) 190px)}
    .wrap{padding:34px 44px 0}
    .eyebrow{margin-bottom:12px}
    .st{font-size:27px;font-weight:700;color:#fff;text-shadow:0 2px 14px rgba(10,22,40,.9)}
    .inset{position:absolute;inset-block-start:150px;inset-inline-end:44px;width:352px;
     border:2px solid #7dd3fc;border-radius:6px;overflow:hidden;
     box-shadow:0 10px 30px rgba(0,0,0,.5)}
    .inset img{width:100%;display:block}
    .icap{position:absolute;inset-block-start:352px;inset-inline-end:44px;width:352px;
     font-size:14px;color:#cbd5e1;text-align:center;margin-top:8px;
     text-shadow:0 2px 10px rgba(10,22,40,.95)}
    .bar{position:absolute;inset-block-end:0;inset-inline:0;height:148px;background:#0a1628;
     border-block-start:1px solid #1e3a5f;display:flex;align-items:center;padding:0 44px;gap:26px}
    .chip{flex:1;display:flex;gap:14px;align-items:flex-start}
    .dot{width:16px;height:16px;border-radius:50%;flex:none;margin-top:5px}
    .c0 .dot{background:#78dc50}.c1 .dot{background:#facc15}.c2 .dot{background:#ef4444}
    .cn{font-size:17px;font-weight:700;letter-spacing:.1em;margin-bottom:7px}
    .c0 .cn{color:#78dc50}.c1 .cn{color:#facc15}.c2 .cn{color:#ef4444}
    .cd{font-size:16px;color:#cbd5e1;line-height:1.45}
    .foot{top:auto;bottom:162px;FP;inset-inline-start:auto;inset-inline-end:auto;
     font-size:15px;color:#e2e8f0;text-shadow:0 2px 10px rgba(10,22,40,.95)}""".replace('FP', s['foot_pos'])
    chips = "".join(
        f'<div class="chip c{i}"><div class="dot"></div><div><div class="cn">{n}</div>'
        f'<div class="cd">{d}</div></div></div>'
        for i, (n, d) in enumerate(s['chips']))
    raw = ('<div class="shot"><img src="frame-488.png"></div><div class="veil"></div>'
           '<div class="inset"><img src="frame-487.png"></div>'
           f'<div class="icap">{s["inset_cap"]}</div>'
           f'<div class="bar">{chips}</div>')
    body = f'<div class="st">{s["shot_title"]}</div>'
    return extra, body, raw


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:52px;font-weight:700;line-height:1.34;max-width:1060px}
    .cfoot{font-size:21px;color:#94a3b8;margin-top:32px;max-width:1010px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="claim">{s["claim"]}</div>' \
           f'<div class="cfoot">{s["claim_foot"]}</div></div>'
    return extra, body, ''


def design3(s):  # the exchange - stopped measuring vs measure instead
    extra = """
    .cells{display:flex;gap:30px;margin-bottom:auto;align-items:stretch}
    .cell{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:34px 30px;background:rgba(125,211,252,.04)}
    .cell.hot{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .lbl{font-size:17px;letter-spacing:.13em;color:#7dd3fc;line-height:1.5;margin-bottom:22px}
    .cell.hot .lbl{color:#fef08a}
    .val{font-size:31px;font-weight:700;line-height:1.45}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val">{s["after_v"]}</div></div></div>'
    return extra, body, ''


def design4(s):  # the two humps and the valley
    extra = """
    .gt{font-size:19px;letter-spacing:.16em;color:#7dd3fc;margin:4px 0 26px}
    .plot{position:relative;direction:ltr}
    .chart{display:flex;align-items:flex-end;gap:5px;height:248px}
    .b{flex:1;background:#7dd3fc;border-radius:2px 2px 0 0;min-height:2px}
    .b.occ{background:#fef08a}
    .thr{position:absolute;inset-block:-14px 30px;inset-inline-start:20%;
     border-inline-start:2px dashed #ef4444}
    .thrl{position:absolute;inset-block-start:-38px;inset-inline-start:20%;
     transform:translateX(-50%);font-size:16px;color:#ef4444;white-space:nowrap}
    .axis{display:flex;justify-content:space-between;direction:ltr;font-size:14px;
     color:#64748b;margin-top:10px;border-block-start:1px solid #1e3a5f;padding-top:8px}
    .tags{display:flex;gap:26px;font-size:17px;margin-top:16px}
    .ta{color:#7dd3fc}.tb{color:#fef08a}
    .xc{font-size:15px;color:#64748b;margin-top:10px}
    .note{font-size:21px;color:#e2e8f0;margin-top:20px;margin-bottom:auto;line-height:1.5}"""
    top = max(BINS) or 1
    bars = "".join(
        f'<div class="b{" occ" if i >= 5 else ""}" '
        f'style="height:{max(2, round(v / top * 248))}px"></div>'
        for i, v in enumerate(BINS))
    body = (f'<div class="gt">{s["hist_title"]}</div>'
            f'<div class="plot"><div class="thrl">{s["hist_thr"]}</div>'
            f'<div class="chart">{bars}</div><div class="thr"></div>'
            f'<div class="axis"><span>0%</span><span>25%</span><span>50%</span>'
            f'<span>75%</span><span>100%</span></div></div>'
            f'<div class="tags"><span class="ta">&#9632; {s["hist_a"]}</span>'
            f'<span class="tb">&#9632; {s["hist_b"]}</span></div>'
            f'<div class="xc">{s["hist_x"]}</div>'
            f'<div class="note">{s["hist_note"]}</div>')
    return extra, body, ''


def design5(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 18px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:12px 0;border-block-end:1px solid #16304f;font-size:23px;line-height:1.4}
    .row .amt{color:#fef08a;font-weight:600;text-align:end;flex:none}
    .gf{font-size:21px;color:#94a3b8;margin-top:22px;margin-bottom:auto;line-height:1.5}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body, ''


def design6(s):  # the one big number
    extra = """
    .num{font-size:118px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
    .unit{font-size:30px;color:#7dd3fc;margin-top:18px}
    .sub{font-size:25px;color:#cbd5e1;margin-top:30px;max-width:1060px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body, ''


DESIGNS = [design1, design2, design3, design4, design5, design6]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    for i, fn in enumerate(DESIGNS, 1):
        for lang in ('en', 'he'):
            s = S[lang]
            extra, body, raw = fn(s)
            eb = f'<div class="eyebrow">{s["eyebrow"]}</div>'
            page = TPL.format(dir=s['dir'], lang=s['lang'], css=CSS, extra=extra,
                              eyebrow_block=eb, body=body, foot=s['foot'], raw=raw)
            hp = os.path.join(HERE, f'hero-{i}-{lang}.html')
            pp = os.path.join(HERE, f'hero-{i}-{lang}.png')
            open(hp, 'w', encoding='utf-8').write(page)
            subprocess.run([CHROME, '--headless=new', '--hide-scrollbars',
                            '--force-device-scale-factor=2', '--window-size=1200,630',
                            '--virtual-time-budget=2500', f'--screenshot={pp}',
                            f'file://{hp}'], capture_output=True)
            print('rendered', os.path.basename(pp))


if __name__ == '__main__':
    main()
