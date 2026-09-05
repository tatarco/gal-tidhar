#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the finance-audit-app testers post."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / HOME FINANCE AUDIT',
   # 1 - the one big number: three sources, each half-blind
   'big':'3 sources,',
   'big_unit':'each one half-blind on its own',
   'big_sub':'Mail knows <span class="cy">why</span> but not every charge.<br>'
             'The card knows <span class="cy">how much</span> but not why.<br>'
             'The bank never sees the <span class="hi">revolving debt</span>.<br>'
             'Throw them together and the real crap floats up.',
   # 2 - the bold claim (recommended shape)
   'claim':'I’m building a free app<br>that finds where your<br>'
           '<span class="hi">parents’ money leaks quietly.</span>',
   'claim_foot':'Installs in one line, brew-style. Runs on your machine only. Looking for patient testers.',
   # 3 - the exchange
   'before_l':'EACH SOURCE<br>ON ITS OWN',
   'before_v':'half the story<br><span class="sm">mail, card and bank each hide a piece</span>',
   'after_l':'ALL THREE<br>THROWN TOGETHER',
   'after_v':'the leaks surface<br><span class="sm">double insurance, forgotten subs, revolving debt</span>',
   # 4 - the breakdown grid
   'grid_title':'WHAT EACH SOURCE CANNOT SEE',
   'grid': [('Your inbox','knows why - misses charges'),
            ('Your credit card','knows amounts - no detail'),
            ('Your bank','never sees the card’s revolving debt'),
            ('Double insurance','invisible in any single feed'),
            ('A sub forgotten 2 years ago','only the cross-check finds it')],
   'grid_foot':'One profile per person. One report. Nothing leaves the machine.',
   # 5 - the payoff quote
   'quote':'“Let’s help<br>everyone’s parents.”',
   'quote_sub':'A free tool to audit your parents’ finances - and yours.<br>'
               'Local only, read-only, passwords never stored.<br>Looking for patient testers.',
   # 6 - the pipeline
   'arch':[('ONE LINE','a brew-style installer<br>sets up everything,<br>even Claude'),
           ('A FEW CLICKS','profiles, banks,<br>cards, inbox -<br>all on this machine'),
           ('A REPORT','revolving credit,<br>double insurance,<br>what to do about it')],
   'arch_foot':'Free. Local. Read-only. GitHub is invite-only while I fix the sharp edges.',
   'foot':'gal.tidhar.org.il',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'3 מקורות,',
   'big_unit':'כל אחד מהם חצי עיוור לבד',
   'big_sub':'המייל יודע <span class="cy">למה</span> אבל לא מכיל כל חיוב.<br>'
             'האשראי יודע <span class="cy">כמה</span> אבל בלי פרטים.<br>'
             'הבנק לא רואה את <span class="hi">החוב המתגלגל</span> בכלל.<br>'
             'זורקים הכל ביחד - והחרא האמיתי צף.',
   'claim':'אני בונה אפליקציה חינמית<br>שמוצאת לאן הכסף של<br>'
           '<span class="hi">ההורים שלכם דולף בשקט.</span>',
   'claim_foot':'מותקנת בשורה אחת, כמו brew. רצה רק על המחשב שלכם. מחפש בודקים עם סבלנות.',
   'before_l':'כל מקור<br>לבד',
   'before_v':'חצי סיפור<br><span class="sm">מייל, אשראי ובנק - כל אחד מסתיר חתיכה</span>',
   'after_l':'שלושתם<br>ביחד',
   'after_v':'הדליפות צפות<br><span class="sm">כפל ביטוח, מנוי שנשכח, אשראי מתגלגל</span>',
   'grid_title':'מה כל מקור לא מסוגל לראות',
   'grid': [('תיבת המייל','יודעת למה - מפספסת חיובים'),
            ('כרטיס האשראי','יודע כמה - בלי פרטים'),
            ('הבנק','לא רואה את החוב המתגלגל של הכרטיס'),
            ('ביטוח כפול','בלתי נראה בכל פיד בודד'),
            ('מנוי שנשכח לפני שנתיים','רק ההצלבה מוצאת אותו')],
   'grid_foot':'פרופיל לכל אדם. דוח אחד. שום דבר לא יוצא מהמחשב.',
   'quote':'"בואו נעזור יחד<br>להורים של כולנו."',
   'quote_sub':'כלי חינמי לביקורת פיננסית להורים - וגם לכם.<br>'
               'מקומי בלבד, קריאה בלבד, הסיסמאות לא נשמרות.<br>מחפש בודקים עם סבלנות.',
   'arch':[('שורה אחת','מתקין בסגנון brew<br>שמתקין הכל,<br>אפילו קלוד'),
           ('כמה קליקים','פרופילים, בנקים,<br>כרטיסים, מייל -<br>הכל על המחשב הזה'),
           ('דוח','אשראי מתגלגל,<br>כפל ביטוחים,<br>ומה לעשות עם זה')],
   'arch_foot':'חינמי. מקומי. קריאה בלבד. הגיטהאב במוזמנים בלבד עד שאתקן את הקצוות החדים.',
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
    .num{font-size:110px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
    .unit{font-size:32px;color:#7dd3fc;margin-top:12px}
    .sub{font-size:27px;color:#cbd5e1;margin-top:28px;max-width:1000px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:56px;font-weight:700;line-height:1.34;max-width:1030px}
    .cfoot{font-size:25px;color:#94a3b8;margin-top:34px;max-width:1000px;line-height:1.5}
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
    .val{font-size:38px;font-weight:700;line-height:1.4}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val hi">{s["after_v"]}</div></div></div>'
    return extra, body


def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 24px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:13px 0;border-block-end:1px solid #16304f;font-size:25px;line-height:1.4}
    .row .amt{color:#fef08a;font-weight:600;text-align:end;max-width:56%}
    .gf{font-size:24px;color:#94a3b8;margin-top:24px;margin-bottom:auto}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the payoff quote
    extra = """
    .q{font-size:72px;font-weight:700;color:#fef08a;line-height:1.25;margin-top:10px}
    .qs{font-size:29px;color:#cbd5e1;margin-top:36px;line-height:1.55;margin-bottom:auto}"""
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
    .af{font-size:25px;color:#fef08a;font-weight:700;margin-bottom:auto;line-height:1.45}"""
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


def build8():
    """Combined 1+2: the claim as headline, the 3-sources mechanism as proof."""
    for lang in ('en', 'he'):
        s = S[lang]
        extra = """
    .claim{font-size:46px;font-weight:700;line-height:1.3;max-width:1040px}
    .mech{margin-top:38px;border-inline-start:3px solid #1e3a5f;padding-inline-start:28px}
    .m{font-size:26px;line-height:1.75;color:#cbd5e1}
    .punch{font-size:27px;color:#e2e8f0;font-weight:700;margin-top:20px}
    .cfoot{font-size:21px;color:#94a3b8;margin-top:30px;margin-bottom:auto}"""
        if lang == 'he':
            mech = ('המייל יודע <span class="cy">למה</span> אבל לא מכיל כל חיוב.<br>'
                    'האשראי יודע <span class="cy">כמה</span> אבל בלי פרטים.<br>'
                    'הבנק לא רואה את <span class="hi">החוב המתגלגל</span> בכלל.')
            punch = 'זורקים הכל ביחד - והחרא האמיתי צף.'
        else:
            mech = ('Mail knows <span class="cy">why</span> but not every charge.<br>'
                    'The card knows <span class="cy">how much</span> but not why.<br>'
                    'The bank never sees the <span class="hi">revolving debt</span>.')
            punch = 'Throw them together and the real crap floats up.'
        body = (f'<div style="margin-bottom:auto"></div>'
                f'<div class="claim">{s["claim"]}</div>'
                f'<div class="mech"><div class="m">{mech}</div>'
                f'<div class="punch">{punch}</div></div>'
                f'<div class="cfoot">{s["claim_foot"]}</div>')
        eb = f'<div class="eyebrow">{s["eyebrow"]}</div>' if s['eyebrow'] else ''
        page = TPL.format(dir=s['dir'], lang=s['lang'], css=CSS, extra=extra,
                          eyebrow_block=eb, body=body, foot=s['foot'])
        hp = os.path.join(HERE, f'hero-8-{lang}.html')
        pp = os.path.join(HERE, f'hero-8-{lang}.png')
        open(hp, 'w', encoding='utf-8').write(page)
        subprocess.run([CHROME, '--headless=new', '--hide-scrollbars',
                        '--force-device-scale-factor=2', '--window-size=1200,630',
                        '--virtual-time-budget=1800', f'--screenshot={pp}',
                        f'file://{hp}'], capture_output=True)
        print('rendered', os.path.basename(pp))
