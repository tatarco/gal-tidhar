#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the money-audit post."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / MONEY AUDIT',
   'big':'232 &rarr; 6,028',
   'big_unit':'ILS. same debt. 2006 to today.',
   'big_sub':'one card, 17.69%, never paid off.<br>nobody bought anything. it just sat there.',
   'claim':'A loan has an end date.<br><span class="hi">Revolving credit<br>has none.</span><br>It doubles every 4.3 years.',
   'claim_foot':'Rolling on my parents\u2019 card since 2006. Nobody ever showed them the number.',
   'before_l':'WHAT A LOAN<br>GIVES YOU',
   'before_v':'a schedule<br><span class="sm">and a date it ends</span>',
   'after_l':'WHAT REVOLVING<br>CREDIT GIVES YOU',
   'after_v':'neither<br><span class="sm">it just keeps doubling</span>',
   'grid_title':'WHY NOBODY EVER SEES THIS DEBT',
   'grid': [('Interest is not a statement line','it is inside the balance'),
            ('It is not a charge','so searching transactions misses it'),
            ('The minimum payment looks responsible','it is what keeps it alive'),
            ('A loan ends, this does not','no schedule, no end date'),
            ('It is the most profitable debt there is','nobody will call to tell you')],
   'grid_foot':'ILS 70,000 at 13-18%, costing about ILS 1,000 a month. Legal, quiet, permanent.',
   'quote':'"The interest is<br>not a line you read.<br>It is already inside<br>the balance."',
   'quote_sub':'Twenty years of it, never once written<br>in front of the two people paying it.',
   'arch':[('ASK 1','how much interest<br>did they pay<br>last month?'),
           ('ASK 2','is any card set to<br>minimum payment<br>or revolving?'),
           ('THAT IS IT','most people cannot<br>answer either one')],
   'arch_foot':'Two questions, no tooling, tonight.',
   'foot':'gal.tidhar.org.il',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'232 &larr; 6,028',
   'big_unit':'ש"ח. אותו חוב. מ-2006 עד היום.',
   'big_sub':'כרטיס אחד, 17.69%, שאף פעם לא נסגר.<br>אף אחד לא קנה כלום. הוא פשוט ישב שם.',
   'claim':'להלוואה יש תאריך סיום.<br><span class="hi">לחוב מתגלגל<br>אין.</span><br>הוא מכפיל את עצמו כל 4.3 שנים.',
   'claim_foot':'מתגלגל על הכרטיס של ההורים שלי מ-2006. אף אחד לא הראה להם את המספר.',
   'before_l':'מה שהלוואה<br>נותנת לך',
   'before_v':'לוח סילוקין<br><span class="sm">ותאריך שבו זה נגמר</span>',
   'after_l':'מה שחוב מתגלגל<br>נותן לך',
   'after_v':'שום דבר מזה<br><span class="sm">הוא פשוט ממשיך להכפיל</span>',
   'grid_title':'למה אף אחד לא רואה את החוב הזה',
   'grid': [('הריבית היא לא שורה בדף החשבון','היא בתוך היתרה'),
            ('זה לא נראה כמו חיוב','אז חיפוש בתנועות לא ימצא'),
            ('התשלום המינימלי נראה אחראי','הוא מה שמשאיר את זה בחיים'),
            ('הלוואה נגמרת, זה לא','בלי לוח סילוקין, בלי תאריך'),
            ('זה החוב הכי רווחי שיש','אף אחד לא יתקשר להגיד לך')],
   'grid_foot':'70 אלף ש"ח בריבית 13-18 אחוז, בערך 1,000 ש"ח בחודש. חוקי, שקט, בלי סוף.',
   'quote':'"הריבית היא לא שורה<br>שקוראים.<br>היא כבר בתוך<br>היתרה."',
   'quote_sub':'עשרים שנה של זה, ואף פעם היא לא נכתבה<br>מול העיניים של שני האנשים שמשלמים אותה.',
   'arch':[('שאלה 1','כמה ריבית הם<br>שילמו החודש?'),
           ('שאלה 2','יש כרטיס שמוגדר<br>בקרדיט או בתשלום<br>מינימלי?'),
           ('זהו','רוב האנשים לא יודעים<br>לענות על אף אחת')],
   'arch_foot':'שתי שאלות, בלי שום כלי, הערב.',
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
    .num{font-size:132px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
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
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val hi">{s["after_v"]}</div></div></div>'
    return extra, body


def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 22px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:11px 0;border-block-end:1px solid #16304f;font-size:23px;line-height:1.35}
    .row .amt{color:#fef08a;font-weight:600;text-align:end;max-width:46%}
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
