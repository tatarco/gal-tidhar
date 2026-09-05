#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the agent-handoff post (the agent fills the cart, I press Pay)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# ponytail: every Latin run inside Hebrew text is isolated with .ltr (direction + isolate),
# learned across four bidi incidents in this repo's earlier heroes.
LTR = '<span class="ltr">{}</span>'

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / NANOCLAW AGENT HANDOFF',
   # 1 - the one big number
   'big':'925 seconds',
   'big_unit':'the browser waited for me, and the session survived',
   'big_sub':'My agent shops in a real Chrome in the cloud.<br>'
             'At the login it sends <span class="cy">its browser to my phone</span>.<br>'
             'I type the password, hand it back, it carries on.<br>'
             '<span class="hi">It never sees a single character.</span>',
   # 2 - the bold claim (recommended)
   'claim':'I gave my agent a real browser.<br>When it hits a password -<br>'
           '<span class="hi">it hands the browser to my phone.</span>',
   'claim_foot':'I do the human part, it carries on with the login intact. The agent fills the cart, I press Pay. NanoClaw, open source; Cloudflare Browser Run, $5/month.',
   # 3 - the exchange
   'before_l':'EVERY BROWSER AGENT<br>UNTIL NOW',
   'before_v':'hits the login,<br>gets stuck<br><span class="sm">or worse - you give it your password</span>',
   'after_l':'HANDOFF',
   'after_v':'sends its browser<br>to my phone<br><span class="sm">I log in, it continues. It saw nothing.</span>',
   # 4 - the breakdown grid
   'grid_title':'WHAT GETS HANDED TO THE HUMAN',
   'grid': [('Password','typed on my phone, never seen by the agent'),
            ('2FA code','the human part stays human'),
            ('CAPTCHA','it proves I am not a robot. Fair.'),
            ('The Pay button','always me - the agent only fills the cart')],
   'grid_foot':'A live view of the agent’s own browser, on my phone, mid-task.',
   # 5 - the payoff quote
   'quote':'“$5/month,<br>10 browser-hours included.”',
   'quote_sub':'Cloudflare Browser Run - the cheapest of the four I compared<br>'
               '(Browserbase $20, Steel $29, Anchor $50), and the only one where<br>'
               'handing the browser to a human is part of the protocol.',
   # 6 - the pipeline
   'arch':[('THE AGENT','a real Chrome<br>in the cloud -<br>searches, compares,<br>fills the cart'),
           ('THE WALL','password, 2FA,<br>CAPTCHA, Pay -<br>things it must<br>not touch'),
           ('MY PHONE','its browser, live,<br>in my hand -<br>I log in,<br>it carries on')],
   'arch_foot':'The agent never sees a password, a cookie or a token.',
   'foot':'gal.tidhar.org.il',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'925 שניות',
   'big_unit':'הדפדפן חיכה לי, והסשן נשאר בחיים',
   'big_sub':'האייג׳נט שלי קונה בכרום אמיתי בענן.<br>'
             'כשהוא מגיע ללוגין הוא שולח <span class="cy">את הדפדפן שלו לטלפון שלי</span>.<br>'
             'אני מקליד סיסמה, מחזיר לו, והוא ממשיך.<br>'
             '<span class="hi">הוא לא רואה ממנה אות אחת.</span>',
   'claim':'נתתי לאייג׳נט שלי דפדפן אמיתי.<br>כשהוא מגיע לסיסמה -<br>'
           '<span class="hi">הוא שולח לי את הדפדפן לטלפון.</span>',
   'claim_foot':'אני עושה את החלק האנושי, והוא ממשיך עם הלוגין ביד. האייג׳נט ממלא את העגלה, אני לוחץ על '
                + LTR.format('Pay') + '. רץ על ' + LTR.format('NanoClaw') + ', קוד פתוח; ' + LTR.format('Cloudflare') + ', 5 דולר לחודש.',
   'before_l':'כל אייג׳נט דפדפן<br>עד היום',
   'before_v':'מגיע ללוגין,<br>נתקע<br><span class="sm">או גרוע יותר - נותנים לו את הסיסמה</span>',
   'after_l':'העברת שליטה',
   'after_v':'שולח את הדפדפן<br>לטלפון שלי<br><span class="sm">אני מתחבר, הוא ממשיך. הוא לא ראה כלום.</span>',
   'grid_title':'מה עובר לידיים של הבנאדם',
   'grid': [('סיסמה','מוקלדת בטלפון שלי, האייג׳נט לא רואה אותה'),
            ('קוד אימות','החלק האנושי נשאר אנושי'),
            ('קאפצ׳ה','הוא מוכיח שאני לא רובוט. הוגן.'),
            ('כפתור התשלום','תמיד אני - האייג׳נט רק ממלא את העגלה')],
   'grid_foot':'תצוגה חיה של הדפדפן של האייג׳נט, בטלפון שלי, באמצע משימה.',
   'quote':'"5 דולר לחודש,<br>10 שעות דפדפן כלולות."',
   'quote_sub':LTR.format('Cloudflare Browser Run') + ' - הזול מבין הארבעה שבדקתי<br>'
               '(' + LTR.format('Browserbase') + ' ב-20 דולר, ' + LTR.format('Steel') + ' ב-29, ' + LTR.format('Anchor') + ' ב-50), והיחיד<br>'
               'שהעברת הדפדפן לבנאדם היא חלק מהפרוטוקול אצלו.',
   'arch':[('האייג׳נט','כרום אמיתי<br>בענן -<br>מחפש, משווה,<br>ממלא עגלה'),
           ('הקיר','סיסמה, קוד אימות,<br>קאפצ׳ה, תשלום -<br>דברים שאסור לו<br>לגעת בהם'),
           ('הטלפון שלי','הדפדפן שלו, לייב,<br>אצלי ביד -<br>אני מתחבר,<br>הוא ממשיך')],
   'arch_foot':'האייג׳נט אף פעם לא רואה סיסמה, עוגיה או טוקן.',
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
.ltr{direction:ltr;unicode-bidi:isolate}
"""

TPL = """<!doctype html><html dir="{dir}" lang="{lang}"><meta charset="utf-8">
<style>{css}{extra}</style><body><div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def design1(s):  # the one big number
    extra = """
    .num{font-size:104px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
    .unit{font-size:32px;color:#7dd3fc;margin-top:14px}
    .sub{font-size:27px;color:#cbd5e1;margin-top:30px;max-width:1010px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:56px;font-weight:700;line-height:1.34;max-width:1040px}
    .cfoot{font-size:25px;color:#94a3b8;margin-top:34px;max-width:1000px;line-height:1.55}
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
    .val{font-size:37px;font-weight:700;line-height:1.4}"""
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
    .gf{font-size:24px;color:#94a3b8;margin-top:26px;margin-bottom:auto}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the payoff quote
    extra = """
    .q{font-size:70px;font-weight:700;color:#fef08a;line-height:1.25;margin-top:10px}
    .qs{font-size:28px;color:#cbd5e1;margin-top:36px;line-height:1.6;margin-bottom:auto}"""
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
