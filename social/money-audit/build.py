#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the money-audit post."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / MONEY AUDIT',
   'big':'17.69%',
   'big_unit':'rolling since 2006',
   'big_sub':"the most expensive thing in my parents' accounts<br>was not a scam app. it was interest nobody ever sees.",
   'claim':'The interest is not a line<br>on the statement.<br><span class="hi">It is already inside<br>the balance.</span>',
   'claim_foot':'ILS 1,000 a month, running since 2006. Nobody ever showed them that number.',
   'before_l':'WHAT THEY OWE<br>AT 13-18%',
   'before_v':'ILS 70,000',
   'after_l':'WHAT SITS IDLE<br>IN A DIFFERENT BANK',
   'after_v':'ILS 40,000<br><span class="sm">earning nothing</span>',
   'grid_title':'FOUR LEAKS, EACH INVISIBLE FOR A DIFFERENT REASON',
   'grid': [('Interest rolling since 2006','ILS 1,000/mo'),
            ('Idle cash next to that debt','ILS 700/mo'),
            ('PayPal billing agreements','ILS 900/mo'),
            ('Three health policies, one event','ILS 1,500/mo'),
            ('App-store junk, still billing','ILS 900/mo')],
   'grid_foot':'Nobody broke a law. Nothing here is a scam. It is all just invisible.',
   'quote':'"A billing agreement<br>is not a subscription."',
   'quote_sub':'It renews with no email from the merchant,<br>and it appears in no subscription list you are told to check.',
   'arch':[('CHECK 1','how much interest<br>are they paying<br>this month?'),
           ('CHECK 2','PayPal, under<br>automatic payments'),
           ('CHECK 3','how many private<br>health policies<br>do they hold?')],
   'arch_foot':'Three questions, no tooling. Most people cannot answer one of them.',
   'foot':'gal.tidhar.org.il',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'17.69%',
   'big_unit':'מתגלגל מ-2006',
   'big_sub':'הדבר הכי יקר בחשבונות של ההורים שלי<br>לא היה אפליקציית סקאם. זו ריבית שאף אחד לא רואה.',
   'claim':'הריבית היא לא שורה<br>בדף החשבון.<br><span class="hi">היא כבר בתוך<br>היתרה.</span>',
   'claim_foot':'בערך 1,000 ש"ח בחודש, מ-2006. אף אחד מעולם לא הראה להם את המספר הזה.',
   'before_l':'החוב שלהם<br>בריבית 13-18 אחוז',
   'before_v':'70,000 ש"ח',
   'after_l':'הכסף ששוכב<br>בבנק אחר',
   'after_v':'40,000 ש"ח<br><span class="sm">בלי לעשות כלום</span>',
   'grid_title':'ארבע נזילות, כל אחת בלתי נראית מסיבה אחרת',
   'grid': [('ריבית שמתגלגלת מ-2006','1,000 בחודש'),
            ('כסף שוכב ליד אותו חוב','700 בחודש'),
            ('הסכמי חיוב בפייפאל','900 בחודש'),
            ('שלוש פוליסות, אירוע אחד','1,500 בחודש'),
            ('זבל מחנות האפליקציות','900 בחודש')],
   'grid_foot':'אף אחד לא עבר על החוק. שום דבר פה הוא לא הונאה. הכל פשוט בלתי נראה.',
   'quote':'"הסכם חיוב<br>הוא לא מנוי."',
   'quote_sub':'הוא מתחדש בלי מייל מהסוחר,<br>ולא מופיע באף רשימת מנויים שאומרים לכם לבדוק.',
   'arch':[('בדיקה 1','כמה ריבית הם<br>משלמים החודש?'),
           ('בדיקה 2','פייפאל,<br>תשלומים אוטומטיים'),
           ('בדיקה 3','כמה פוליסות בריאות<br>פרטיות יש להם?')],
   'arch_foot':'שלוש שאלות, בלי שום כלי. רוב האנשים לא יודעים לענות על אחת מהן.',
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
           f'<div class="val">{s["before_v"]}</div></div>' \
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
