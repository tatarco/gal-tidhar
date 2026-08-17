#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the money-audit post."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / MONEY AUDIT',
   'big':'10x',
   'big_unit':'off. before anyone was told.',
   'big_sub':'the bank data said my parents owed 350,000.<br>three agents re-derived it. it was 70,000.',
   'claim':'I was about to tell my<br>83-year-old father he owed<br><span class="hi">350,000</span>.<br>Three agents checked me first.',
   'claim_foot':'The real number was 70,307. I never had to make that call.',
   'before_l':'WHAT THE BANK<br>FEED ADDED UP TO',
   'before_v':'ILS 350,000<br><span class="sm">26 "loans"</span>',
   'after_l':'WHAT WAS<br>ACTUALLY OWED',
   'after_v':'ILS 70,307<br><span class="sm">2 rolling cards</span>',
   'grid_title':'WHAT A YEAR OF BANK DATA HELD',
   'grid': [('Card rolling since 2006','17.69%'),
            ('Idle cash next to that debt','ILS 40k'),
            ('PayPal agreements, no emails','ILS 11k/yr'),
            ('Health policies stacked','3'),
            ('App-store junk, still billing','ILS 900/mo')],
   'grid_foot':'Recoverable: ILS 3,000-4,500 a month. Nothing they enjoy gets cut.',
   'quote':'"13 months on file<br>read as 13 loans."',
   'quote_sub':'A revolving card reports one row per cycle.<br>Sum them and you multiply the debt by the months.',
   'arch':[('PULL','open banking,<br>read-only,<br>into SQLite'),
           ('ASK','SQL over 2,410<br>transactions,<br>not PDFs'),
           ('VERIFY','3 agents<br>re-derive it<br>before anyone hears it')],
   'arch_foot':'The second opinion cost cents. It was worth 280,000.',
   'foot':'gal.tidhar.org.il',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'פי 10',
   'big_unit':'טעות. לפני שמישהו שמע אותה.',
   'big_sub':'הדאטה מהבנק אמרה שההורים שלי חייבים 350 אלף.<br>שלושה אייג\'נטים גזרו את זה מחדש. זה היה 70 אלף.',
   'claim':'עמדתי להגיד לאבא שלי<br>בן ה-83 שהוא חייב<br><span class="hi">350 אלף</span>.<br>שלושה אייג\'נטים בדקו אותי קודם.',
   'claim_foot':'המספר האמיתי היה 70,307. לא הייתי צריך להרים את הטלפון הזה.',
   'before_l':'מה שיצא מסיכום<br>הנתונים של הבנק',
   'before_v':'350,000 ש"ח<br><span class="sm">26 "הלוואות"</span>',
   'after_l':'מה שבאמת<br>היה חייב',
   'after_v':'70,307 ש"ח<br><span class="sm">2 כרטיסים מתגלגלים</span>',
   'grid_title':'מה שהיה בשנה של נתוני בנק',
   'grid': [('כרטיס שמתגלגל מ-2006','17.69%'),
            ('כסף שוכב ליד אותו חוב','40 אלף'),
            ('הסכמי פייפאל בלי מיילים','11 אלף בשנה'),
            ('פוליסות בריאות אחת על השנייה','3'),
            ('זבל מחנות האפליקציות, עדיין מחייב','900 בחודש')],
   'grid_foot':'חוזר: 3,000 עד 4,500 ש"ח בחודש. בלי לוותר על שום דבר שהם נהנים ממנו.',
   'quote':'"13 חודשים בקובץ<br>נקראים כמו 13 הלוואות."',
   'quote_sub':'כרטיס מתגלגל מדווח כשורה לכל מחזור.<br>מי שסוכם אותן מכפיל את החוב במספר החודשים.',
   'arch':[('משיכה','אופן בנקינג,<br>קריאה בלבד,<br>לתוך SQLite'),
           ('שאלה','SQL על 2,410<br>תנועות,<br>לא PDF-ים'),
           ('אימות','3 אייג\'נטים<br>גוזרים מחדש<br>לפני שמישהו שומע')],
   'arch_foot':'חוות הדעת השנייה עלתה אגורות. היא הייתה שווה 280 אלף.',
   'foot':'gal.tidhar.org.il',
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
"""

TPL = """<!doctype html><html dir="{dir}" lang="{lang}"><meta charset="utf-8">
<style>{css}{extra}</style><body><div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def design1(s):  # the one big number
    extra = """
    .num{font-size:180px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
    .unit{font-size:34px;color:#7dd3fc;margin-top:10px}
    .sub{font-size:28px;color:#cbd5e1;margin-top:30px;max-width:960px;line-height:1.5}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:56px;font-weight:700;line-height:1.34;max-width:1030px}
    .cfoot{font-size:26px;color:#94a3b8;margin-top:34px}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="claim">{s["claim"]}</div>' \
           f'<div class="cfoot">{s["claim_foot"]}</div></div>'
    return extra, body


def design3(s):  # the exchange
    extra = """
    .cells{display:flex;gap:30px;margin-bottom:auto;align-items:stretch}
    .cell{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:34px 30px;background:rgba(125,211,252,.04)}
    .cell.hot{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .lbl{font-size:16px;letter-spacing:.13em;color:#7dd3fc;line-height:1.5;margin-bottom:22px}
    .cell.hot .lbl{color:#fef08a}
    .val{font-size:40px;font-weight:700;line-height:1.35}
    .strike{text-decoration:line-through;text-decoration-color:#ef4444;text-decoration-thickness:4px}
    .strike .sm{display:inline-block;text-decoration:none}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val strike">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val hi">{s["after_v"]}</div></div></div>'
    return extra, body


def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 22px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:12px 0;border-block-end:1px solid #16304f;font-size:27px}
    .row .amt{color:#fef08a;font-weight:700;white-space:nowrap}
    .gf{font-size:24px;color:#94a3b8;margin-top:22px;margin-bottom:auto}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the payoff quote
    extra = """
    .q{font-size:76px;font-weight:700;color:#fef08a;line-height:1.25;margin-top:10px}
    .qs{font-size:30px;color:#cbd5e1;margin-top:36px;line-height:1.5;margin-bottom:auto}"""
    body = f'<div class="q">{s["quote"]}</div><div class="qs">{s["quote_sub"]}</div>'
    return extra, body


def design6(s):  # the pipeline
    extra = """
    .steps{display:flex;gap:22px;align-items:stretch;margin-bottom:26px}
    .st{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:28px 24px;background:rgba(125,211,252,.04)}
    .st:last-child{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .sn{font-size:19px;letter-spacing:.15em;color:#7dd3fc;margin-bottom:16px}
    .st:last-child .sn{color:#fef08a}
    .sd{font-size:23px;line-height:1.5;color:#e2e8f0}
    .af{font-size:27px;color:#fef08a;font-weight:700;margin-bottom:auto}"""
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
