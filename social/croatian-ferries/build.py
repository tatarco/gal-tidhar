#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the croatian-ferries post (your next ferry: in 23 min)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# ponytail: every Latin run inside Hebrew text is isolated with .ltr, learned across four bidi incidents.
L = '<span class="ltr">{}</span>'.format

PDF_EN = ('14:30<span class="ast">*</span> &nbsp; 16:00<span class="ast">**</span> &nbsp; 18:30<br>'
          '<span class="sm">* Sails 20.06. &amp; 27.06.<br>** 20.06. &amp; 27.06. departs at 18:00.<br>'
          'Does not sail on Sundays and holidays.</span>')

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / CROATIANFERRIES.COM',
   'big':'in 23 min',
   'big_unit':'Your next ferry. Valbiska → Merag, 14:30.',
   'big_sub':'Every ferry timetable in Croatia is a PDF: three seasons side by side,<br>'
             'asterisks, footnotes on page 2. <span class="cy">23 lines, 52 ports, 4 languages</span>,<br>'
             'read once so <span class="hi">nobody has to decrypt it from the car again</span>.',
   'claim':'I was done decrypting PDFs<br>to find my next ferry.<br>'
           '<span class="hi">So I built the answer: in 23 min.</span>',
   'claim_foot':'croatianferries.com. Open the port, get the next departure and the minutes until it. Every car-ferry line in Croatia, in Croatian, English, German and Italian, with the live port camera next to the time.',
   'before_l':'THE TIMETABLE, TODAY',
   'before_v':PDF_EN,
   'after_l':'THE SAME QUESTION, ANSWERED',
   'after_v':'Your next ferry<br>in 23 min<br><span class="sm">Valbiska → Merag, 14:30</span>',
   'grid_title':'WHAT THE PORT PAGE ANSWERS',
   'grid': [('When is the next ferry?','14:30, in 23 min'),
            ('How long is the crossing?','25 min, from the timetable itself'),
            ('Do I need to book?','yes / no, per line'),
            ('What does the queue look like?','the live port camera, in place'),
            ('Can my in-laws read it?','hr · en · de · it')],
   'grid_foot':'23 car-ferry lines · 52 ports · no cookies, no third-party requests',
   'quote':'Every ferry timetable<br>in Croatia is a PDF.',
   'quote_sub':'Three seasons side by side, asterisks next to half the times,<br>'
               'and the footnotes that decide whether your 14:30 exists today<br>'
               'are on page 2. I read all 23 of them once, so a tourist in a<br>'
               'car at the port never has to.',
   'arch':[('THE PDF','a printed table:<br>seasons as columns,<br>asterisks, footnotes<br>in three languages'),
           ('THE JUDGMENT','one small file per line<br>says which column is<br>which season and what<br>each footnote restricts'),
           ('THE ANSWER','code copies the times<br>from the PDF’s own text,<br>the page computes<br>“in 23 min” for you')],
   'arch_foot':'Reading a timetable is judgment. Copying 600 times out of it is not - that is where the mistakes come from.',
   'foot':'croatianferries.com',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'בעוד 23 דקות',
   'big_unit':'המעבורת הבאה שלך. ולביסקה ← מראג, 14:30.',
   'big_sub':'כל לוח זמנים של מעבורת בקרואטיה הוא PDF: שלוש עונות אחת ליד השניה,<br>'
             'כוכביות, הערות שוליים בעמוד 2. <span class="cy">23 קווים, 52 נמלים, 4 שפות</span>,<br>'
             'קראתי פעם אחת כדי <span class="hi">שאף אחד לא יצטרך לפענח את זה מהאוטו שוב</span>.',
   'claim':'נמאס לי לפענח PDF<br>כדי לדעת מתי המעבורת הבאה.<br>'
           '<span class="hi">אז בניתי את התשובה: בעוד 23 דקות.</span>',
   'claim_foot':'croatianferries.com. פותחים את הנמל, מקבלים את ההפלגה הבאה ואת הדקות עד אליה. כל קווי מעבורות הרכב בקרואטיה, בקרואטית, אנגלית, גרמנית ואיטלקית, עם המצלמה החיה של הנמל ליד השעה.',
   'before_l':'לוח הזמנים, היום',
   'before_v':L(PDF_EN),
   'after_l':'אותה שאלה, עם תשובה',
   'after_v':'המעבורת הבאה שלך<br>בעוד 23 דקות<br><span class="sm">ולביסקה ← מראג, 14:30</span>',
   'grid_title':'מה עמוד הנמל עונה',
   'grid': [('מתי המעבורת הבאה?','14:30, בעוד 23 דקות'),
            ('כמה זמן החצייה?','25 דקות, מהלוח עצמו'),
            ('צריך להזמין מראש?','כן / לא, לפי קו'),
            ('איך נראה התור?','המצלמה החיה של הנמל, במקום'),
            ('החמות שלי תוכל לקרוא את זה?','קרואטית · אנגלית · גרמנית · איטלקית')],
   'grid_foot':'23 קווי מעבורות רכב · 52 נמלים · בלי עוגיות, בלי בקשות לצד שלישי',
   'quote':'כל לוח זמנים של מעבורת<br>בקרואטיה הוא PDF.',
   'quote_sub':'שלוש עונות אחת ליד השניה, כוכביות ליד חצי מהשעות,<br>'
               'והערות השוליים שקובעות אם ה-14:30 שלך קיימת היום<br>'
               'נמצאות בעמוד 2. קראתי את כל 23 פעם אחת, כדי שתייר<br>'
               'באוטו בנמל לא יצטרך לעולם.',
   'arch':[('ה-PDF','טבלה מודפסת:<br>עונות בעמודות,<br>כוכביות, הערות שוליים<br>בשלוש שפות'),
           ('השיפוט','קובץ קטן אחד לכל קו<br>אומר איזו עמודה היא<br>איזו עונה ומה כל<br>כוכבית מגבילה'),
           ('התשובה','הקוד מעתיק את השעות<br>מהטקסט של ה-PDF עצמו,<br>והעמוד מחשב לך<br>"בעוד 23 דקות"')],
   'arch_foot':'לקרוא לוח זמנים זה שיפוט. להעתיק ממנו 600 שעות זה לא - ושם נופלות הטעויות.',
   'foot':'croatianferries.com',
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
.sm{font-size:.55em;color:#94a3b8;font-weight:400}
.ast{color:#f87171}
.ltr{direction:ltr;unicode-bidi:isolate;display:inline-block;text-align:left}
"""

TPL = """<!doctype html><html dir="{dir}" lang="{lang}"><meta charset="utf-8">
<style>{css}{extra}</style><body><div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def design1(s):  # the one big number
    extra = """
    .num{font-size:120px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
    .unit{font-size:32px;color:#7dd3fc;margin-top:18px}
    .sub{font-size:26px;color:#cbd5e1;margin-top:30px;max-width:1040px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:54px;font-weight:700;line-height:1.34;max-width:1040px}
    .cfoot{font-size:24px;color:#94a3b8;margin-top:32px;max-width:1000px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="claim">{s["claim"]}</div>' \
           f'<div class="cfoot">{s["claim_foot"]}</div></div>'
    return extra, body


def design3(s):  # the exchange
    extra = """
    .cells{display:flex;gap:30px;margin-bottom:auto;align-items:stretch}
    .cell{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:34px 30px;background:rgba(125,211,252,.04)}
    .cell.hot{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .lbl{font-size:17px;letter-spacing:.13em;color:#7dd3fc;line-height:1.5;margin-bottom:22px}
    .cell.hot .lbl{color:#fef08a}
    .val{font-size:36px;font-weight:700;line-height:1.45}
    .cell:not(.hot) .val{font-size:34px}
    .cell:not(.hot) .sm{font-size:.62em;line-height:1.6;display:inline-block;margin-top:14px}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val hi">{s["after_v"]}</div></div></div>'
    return extra, body


def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 24px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:15px 0;border-block-end:1px solid #16304f;font-size:26px;line-height:1.4}
    .row .amt{color:#fef08a;font-weight:600;text-align:end;max-width:62%}
    .gf{font-size:22px;color:#94a3b8;margin-top:26px;margin-bottom:auto}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the payoff quote
    extra = """
    .q{font-size:66px;font-weight:700;color:#fef08a;line-height:1.25;margin-top:10px}
    .qs{font-size:27px;color:#cbd5e1;margin-top:36px;line-height:1.6;margin-bottom:auto}"""
    body = f'<div class="q">{s["quote"]}</div><div class="qs">{s["quote_sub"]}</div>'
    return extra, body


def design6(s):  # the pipeline
    extra = """
    .steps{display:flex;gap:22px;align-items:stretch;margin-bottom:28px}
    .st{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:28px 24px;background:rgba(125,211,252,.04)}
    .st:last-child{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .sn{font-size:19px;letter-spacing:.15em;color:#7dd3fc;margin-bottom:16px}
    .st:last-child .sn{color:#fef08a}
    .sd{font-size:23px;line-height:1.5;color:#e2e8f0}
    .af{font-size:24px;color:#fef08a;font-weight:700;margin-bottom:auto;line-height:1.45}"""
    steps = "".join(f'<div class="st"><div class="sn">{n}</div><div class="sd">{d}</div></div>'
                    for n, d in s['arch'])
    body = f'<div class="steps">{steps}</div><div class="af">{s["arch_foot"]}</div>'
    return extra, body


DESIGNS = [design1, design2, design3, design4, design5, design6]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    for i, fn in enumerate(DESIGNS, 1):
        for lang in ('en', 'he'):
            s = S[lang]
            extra, body = fn(s)
            eb = f'<div class="eyebrow">{s["eyebrow"]}</div>' if s['eyebrow'] else '<div style="margin-bottom:auto"></div>'
            page = TPL.format(dir=s['dir'], lang=s['lang'], css=CSS, extra=extra,
                              eyebrow_block=eb, body=body, foot=s['foot'])
            hp = os.path.join(HERE, f'hero-{i}-{lang}.html')
            pp = os.path.join(HERE, f'hero-{i}-{lang}.png')
            open(hp, 'w', encoding='utf-8').write(page)
            subprocess.run([CHROME, '--headless=new', '--hide-scrollbars',
                            '--force-device-scale-factor=2', '--window-size=1200,630',
                            '--virtual-time-budget=1800', f'--screenshot={pp}',
                            f'file://{hp}'], capture_output=True)
            print('rendered', os.path.basename(pp))


if __name__ == '__main__':
    main()
