#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the subscription-audit post."""
import os, subprocess, html

HERE = os.path.dirname(os.path.abspath(__file__))

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / SUBSCRIPTION AUDIT',
   'big':'16,000',
   'big_unit':'ILS / year',
   'big_sub':'my 83-year-old father was paying this. for nothing.',
   'claim':'He paid ILS 54.90<br><span class="hi">every week</span><br>for a QR code reader.',
   'claim_foot':'and he was subscribed to the same wallet app twice.',
   'before_l':'WHAT HE THOUGHT<br>HE PAID FOR',
   'before_v':'a phone bill',
   'after_l':'WHAT WAS ACTUALLY<br>IN THE BILL',
   'after_v':'ILS 337 / mo<br>of kitchen appliances',
   'grid_title':'FIVE WEEKLY SUBSCRIPTIONS',
   'grid': [('Wallet app','75.00 / wk'),('QR code reader','54.90 / wk'),
            ('Photo recovery','54.90 / wk'),('File recovery','46.00 / wk'),
            ('Wallet app (again)','31.00 / wk')],
   'grid_foot':'ILS 261.80 a week. Same wallet app, twice.',
   'quote':'"0 devices protected."',
   'quote_sub':'Eight years of antivirus renewals.<br>It was never installed on anything.',
   'arch':[('SCAN','1 year of mail,<br>ranked by sender'),
           ('PARSE','every invoice PDF,<br>amount + card'),
           ('CANCEL','agent logs in,<br>kills each one')],
   'arch_foot':'ILS 3,658 claimed back. First refund already paid.',
   'foot':'gal.tidhar.org.il',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'16,000',
   'big_unit':'ש"ח בשנה',
   'big_sub':'אבא שלי בן ה-83 שילם את זה. על כלום.',
   'claim':'הוא שילם 54.90 ש"ח<br><span class="hi">כל שבוע</span><br>על אפליקציה שקוראת ברקודים.',
   'claim_foot':'ועל אותה אפליקציית ארנק הוא היה מנוי פעמיים.',
   'before_l':'מה שהוא חשב<br>שהוא משלם עליו',
   'before_v':'חשבון סלולר',
   'after_l':'מה שבאמת היה<br>בתוך החשבון',
   'after_v':'337 ש"ח בחודש<br>של מוצרי חשמל',
   'grid_title':'חמישה מנויים שבועיים',
   'grid': [('אפליקציית ארנק','75.00 לשבוע'),('קריאת ברקודים','54.90 לשבוע'),
            ('שחזור תמונות','54.90 לשבוע'),('שחזור קבצים','46.00 לשבוע'),
            ('אפליקציית ארנק (שוב)','31.00 לשבוע')],
   'grid_foot':'261.80 ש"ח בשבוע. אותה אפליקציית ארנק, פעמיים.',
   'quote':'"0 מכשירים מוגנים."',
   'quote_sub':'שמונה שנים של חידושי אנטי וירוס.<br>הוא אף פעם לא הותקן על שום דבר.',
   'arch':[('סריקה','שנה של מיילים,<br>מדורגים לפי שולח'),
           ('פענוח','כל חשבונית PDF,<br>סכום וכרטיס'),
           ('ביטול','אייג\'נט נכנס<br>ומבטל אחד אחד')],
   'arch_foot':'3,658 ש"ח בתביעת החזר. ההחזר הראשון כבר אושר.',
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
"""

TPL = """<!doctype html><html dir="{dir}" lang="{lang}"><meta charset="utf-8">
<style>{css}{extra}</style><body><div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""

def design1(s):  # the one big number
    extra = """
    .num{font-size:210px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
    .unit{font-size:34px;color:#7dd3fc;margin-top:6px}
    .sub{font-size:29px;color:#cbd5e1;margin-top:30px;max-width:900px;line-height:1.45}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body

def design2(s):  # the bold claim
    extra = """
    .claim{font-size:62px;font-weight:700;line-height:1.32;max-width:1010px}
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
    .val{font-size:40px;font-weight:700;line-height:1.3}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val hi">{s["after_v"]}</div></div></div>'
    return extra, body

def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 26px}
    .row{display:flex;justify-content:space-between;align-items:baseline;
     padding:13px 0;border-block-end:1px solid #16304f;font-size:30px}
    .row .amt{color:#fef08a;font-weight:700}
    .gf{font-size:25px;color:#94a3b8;margin-top:24px;margin-bottom:auto}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body

def design5(s):  # the payoff quote
    extra = """
    .q{font-size:88px;font-weight:700;color:#fef08a;line-height:1.2;margin-top:10px}
    .qs{font-size:32px;color:#cbd5e1;margin-top:36px;line-height:1.5;margin-bottom:auto}"""
    body = f'<div class="q">{s["quote"]}</div><div class="qs">{s["quote_sub"]}</div>'
    return extra, body

def design6(s):  # the pipeline
    extra = """
    .steps{display:flex;gap:22px;align-items:stretch;margin-bottom:26px}
    .st{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:28px 24px;background:rgba(125,211,252,.04)}
    .sn{font-size:19px;letter-spacing:.15em;color:#7dd3fc;margin-bottom:16px}
    .sd{font-size:24px;line-height:1.45;color:#e2e8f0}
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
