#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the money-audit post."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / FINANCE AUDIT - BETA',
   'big':'4 of 6',
   'big_unit':'ways to get a family audit wrong',
   'big_sub':'are interpretation errors, not arithmetic.<br>Checking the maths catches none of them.',
   'claim':'If you have Claude Code<br>and a Gmail account,<br><span class="hi">you can audit your<br>parents’ money.</span>',
   'claim_foot':'Runs on your machine. I never see a byte. Looking for 5-10 beta testers.',
   'before_l':'A WEBSITE THAT<br>COLLECTS BANK DATA',
   'before_v':'needs a licence<br><span class="sm">no free exemption in the law</span>',
   'after_l':'SOFTWARE YOU RUN<br>ON YOUR OWN MACHINE',
   'after_v':'does not<br><span class="sm">regulation chose the architecture</span>',
   'grid_title':'THE SIX WAYS TO BE CONFIDENTLY WRONG',
   'grid': [('Inflow is not income','a loan looks like a salary'),
            ('Co-occurrence is not duplication','two insurers can be a handover'),
            ('A feed that starts late','looks like a brand new expense'),
            ('A partial boundary month','reads as a deficit'),
            ('One person, two spellings','drops whole cards from a filter'),
            ('A revolving card reports per cycle','summing multiplies the debt')],
   'grid_foot':'Four of these six pass an arithmetic review. That checklist is the actual product.',
   'quote':'"Money arriving<br>is not income."',
   'quote_sub':'A savings drawdown, a loan and a cash advance<br>all look the same. One audit reported a deficit<br>three times too small because of it.',
   'arch':[('LOCAL','your bank, in a<br>Chrome window<br>you can watch'),
           ('YOUR MAIL','Gmail headers,<br>no OAuth, no<br>cloud project'),
           ('YOUR AGENT','claude -p reads<br>the local SQLite<br>and writes it up')],
   'arch_foot':'Nothing leaves the machine. Built on israeli-bank-scrapers (MIT, 2017).',
   'foot':'gal.tidhar.org.il',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'4 מתוך 6',
   'big_unit':'מהדרכים לטעות בביקורת פיננסית',
   'big_sub':'הן טעויות פרשנות, לא טעויות חשבון.<br>בדיקה אריתמטית לא תופסת אף אחת מהן.',
   'claim':'אם יש לכם קלוד קוד<br>וחשבון ג’ימייל,<br><span class="hi">אתם יכולים לעשות<br>ביקורת פיננסית להורים.</span>',
   'claim_foot':'רץ אצלכם על המחשב. אני לא מקבל בייט. מחפש 5-10 בודקי ביתא.',
   'before_l':'אתר שאוסף<br>נתוני בנק',
   'before_v':'צריך רישיון<br><span class="sm">אין בחוק פטור לבחינם</span>',
   'after_l':'תוכנה שרצה על<br>המחשב שלכם',
   'after_v':'לא צריך<br><span class="sm">הרגולציה בחרה את הארכיטקטורה</span>',
   'grid_title':'שש הדרכים לטעות בביטחון מלא',
   'grid': [('תזרים נכנס זה לא הכנסה','הלוואה נראית כמו משכורת'),
            ('חפיפה זה לא כפילות','שתי חברות ביטוח יכולות להיות מעבר תקין'),
            ('פיד שמתחיל באיחור','נראה בדיוק כמו הוצאה חדשה'),
            ('חודש חלקי בקצה','נקרא כמו גירעון'),
            ('אותו אדם, שני איותים','מפיל כרטיסים שלמים מהסינון'),
            ('כרטיס בקרדיט מדווח לפי מחזור','סכימה מכפילה את החוב')],
   'grid_foot':'ארבע מהשש עוברות בדיקה אריתמטית בשלום. רשימת המלכודות הזאת היא המוצר.',
   'quote':'"כסף שנכנס<br>זה לא הכנסה."',
   'quote_sub':'משיכה מחיסכון, הלוואה ומשיכת מזומן<br>נראות אותו דבר. בגלל זה דיווחתי פעם<br>על גירעון קטן פי שלושה מהאמיתי.',
   'arch':[('מקומי','הבנק שלכם, בחלון<br>כרום שאתם<br>רואים'),
           ('הדואר שלכם','כותרות מג’ימייל,<br>בלי OAuth ובלי<br>פרויקט בענן'),
           ('הסוכן שלכם','claude -p קורא<br>SQLite מקומי<br>וכותב דוח')],
   'arch_foot':'שום דבר לא יוצא מהמחשב. בנוי מעל israeli-bank-scrapers (MIT, 2017).',
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
