#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the dont-punt post."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
L = '<span class="ltr">{}</span>'.format  # isolate Latin runs inside Hebrew

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / CLAUDE CODE',
   'big':'don\'t punt',
   'big_unit':'Two words. Claude Code stops handing me work it can do itself.',
   'big_sub':'Five times in one evening it ended with "click Import, choose your account,<br>'
             'then <span class="cy">reply continue and I\'ll take over</span>". It has its own browser.<br>'
             'It was not stuck. <span class="hi">It decided the boring part was mine.</span>',
   'claim':'The model wasn\'t stuck.<br>It decided the boring part was mine.<br>'
           '<span class="hi">Two words fixed it: don\'t punt.</span>',
   'claim_foot':'A punt is the fourth-down kick: you hand the ball over on purpose because you judged you won\'t advance. Not a failure, a decision. Name the move and Claude Code takes the ball back.',
   'before_l':'CLAUDE CODE, 20:34',
   'before_v':'1. Click <b>New key event</b><br>2. Type <b>generate_lead</b><br>3. Save<br><span class="sm">Then reply "continue" and I\'ll verify it registered.</span>',
   'me_l':'ME',
   'me_v':'don\'t punt',
   'after_l':'CLAUDE CODE, 20:35',
   'after_v':'Taking over and driving it through myself.',
   'grid_title':'THE THREE GRADES OF PUNT',
   'grid': [('1 &middot; the list','"here are 5 clicks, reply continue"'),
            ('2 &middot; the option','"neither blocks anything. try again, or call it done?"'),
            ('3 &middot; the judgment','"you don\'t actually need this. I\'ll stop pushing."')],
   'grid_foot':'The third one is the dangerous one. It arrives exactly when the work gets boring, and it sounds like advice.',
   'quote':'Every answer that ends with<br>"reply continue"<br>is a punt.',
   'quote_sub':'Claude Code has its own browser and every one of those buttons.<br>'
               'A numbered list of clicks is not help, it is handing the ball back.<br>'
               'Two words take it back: don\'t punt.',
   'arch':[('"JUST DO IT"','a mood.<br>the model answers a mood<br>with a shorter version<br>of the same list of clicks'),
           ('"DON\'T PUNT"','the name of a move.<br>giving up possession<br>on purpose, because you<br>judged you can\'t advance'),
           ('WHY IT LANDS','the model already carries<br>the rule against this and<br>calls it stopping short.<br>two words point at it')],
   'arch_foot':'It does not need convincing. It needs the thing called by its name.',
   'foot':'gal.tidhar.org.il/blog/dont-punt',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'don\'t punt',
   'big_unit':'שתי מילים. Claude Code מפסיק להחזיר לי עבודה שהוא יכול לעשות בעצמו.',
   'big_sub':'חמש פעמים בערב אחד זה נגמר ב"לחץ על Import, בחר את החשבון,<br>'
             '<span class="cy">ואז תכתוב לי continue ואני אמשיך</span>". יש לו דפדפן משלו.<br>'
             'הוא לא היה תקוע. <span class="hi">הוא החליט שהקטע המשעמם שלי.</span>',
   'claim':'המודל לא היה תקוע.<br>הוא החליט שהקטע המשעמם שלי.<br>'
           '<span class="hi">שתי מילים תיקנו את זה: don\'t punt.</span>',
   'claim_foot':'פאנט זו הבעיטה בדאון הרביעי: מוסרים את הכדור בכוונה כי שפטת שלא תתקדם. לא כישלון, החלטה. קוראים למהלך בשם, ו-Claude Code לוקח את הכדור בחזרה.',
   'before_l':'Claude Code, 20:34',
   'before_v':'1. לחץ על <b>New key event</b><br>2. הקלד <b>generate_lead</b><br>3. שמור<br><span class="sm">ואז תכתוב לי continue ואני אוודא שזה נרשם.</span>',
   'me_l':'אני',
   'me_v':'don\'t punt',
   'after_l':'Claude Code, 20:35',
   'after_v':'לוקח את זה ומסיים בעצמי.',
   'grid_title':'שלוש דרגות של פאנט',
   'grid': [('1 · הרשימה','"הנה 5 קליקים, תכתוב לי continue"'),
            ('2 · האופציה','"שום דבר לא חוסם. לנסות שוב, או לסגור את זה?"'),
            ('3 · השיפוט','"אתה בכלל לא צריך את זה. אני מפסיק לדחוף."')],
   'grid_foot':'השלישי הוא המסוכן. הוא מגיע בדיוק כשהעבודה נהיית משעממת, ונשמע כמו עצה.',
   'quote':'כל תשובה שנגמרת<br>ב"תכתוב לי continue"<br>היא פאנט.',
   'quote_sub':'ל-Claude Code יש דפדפן משלו וכל אחד מהכפתורים האלה.<br>'
               'רשימה ממוספרת של קליקים היא לא עזרה, היא מסירת הכדור.<br>'
               'שתי מילים לוקחות אותו בחזרה: don\'t punt.',
   'arch':[('"תעשה את זה בעצמך"','מצב רוח.<br>המודל עונה למצב רוח<br>בגרסה קצרה יותר<br>של אותה רשימת קליקים'),
           ('"don\'t punt"','שם של מהלך.<br>ויתור על הכדור בכוונה,<br>כי שפטת שלא<br>תצליח להתקדם'),
           ('למה זה נוחת','המודל כבר נושא את הכלל<br>נגד זה, וקורא לזה<br>stopping short.<br>שתי מילים מצביעות עליו')],
   'arch_foot':'הוא לא צריך להשתכנע. הוא צריך שיקראו לדבר בשם.',
   'foot':'gal.tidhar.org.il/blog/dont-punt',
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
.ltr{direction:ltr;unicode-bidi:isolate;display:inline-block;text-align:left}
b{color:#e2e8f0}
"""

TPL = """<!doctype html><html dir="{dir}" lang="{lang}"><meta charset="utf-8">
<style>{css}{extra}</style><body><div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def design1(s):  # the two words, huge
    extra = """
    .num{font-size:128px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em;direction:ltr;text-align:start}
    .unit{font-size:30px;color:#7dd3fc;margin-top:22px}
    .sub{font-size:25px;color:#cbd5e1;margin-top:28px;max-width:1040px;line-height:1.55}
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


def design3(s):  # the exchange, three bubbles
    extra = """
    .wrap{padding-top:44px}
    .chat{display:flex;flex-direction:column;gap:14px;margin-bottom:auto;max-width:1000px}
    .msg{border:1px solid #1e3a5f;border-radius:12px;padding:16px 24px;background:rgba(125,211,252,.04)}
    .msg.me{border-color:#fef08a;background:rgba(254,240,138,.08);align-self:flex-end;min-width:380px;display:flex;align-items:baseline;gap:22px}
    .msg.me .val{color:#fef08a;font-size:50px;font-weight:700;direction:ltr;text-align:start;line-height:1}
    .lbl{font-size:14px;letter-spacing:.13em;color:#7dd3fc;margin-bottom:8px}
    .msg.me .lbl{color:#fef08a;margin:0}
    .val{font-size:24px;line-height:1.45}
    .msg.last{border-color:#7dd3fc;background:rgba(125,211,252,.09)}
    .msg.last .val{font-size:28px;font-weight:700;color:#7dd3fc}"""
    body = (f'<div class="chat"><div class="msg"><div class="lbl">{s["before_l"]}</div><div class="val">{s["before_v"]}</div></div>'
            f'<div class="msg me"><div class="lbl">{s["me_l"]}</div><div class="val">{s["me_v"]}</div></div>'
            f'<div class="msg last"><div class="lbl">{s["after_l"]}</div><div class="val">{s["after_v"]}</div></div></div>')
    return extra, body


def design4(s):  # the three grades
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 24px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:18px 0;border-block-end:1px solid #16304f;font-size:27px;line-height:1.4}
    .row .amt{color:#cbd5e1;text-align:end;max-width:66%}
    .row:last-of-type .amt{color:#fef08a;font-weight:600}
    .row span:first-child{color:#7dd3fc;white-space:nowrap}
    .gf{font-size:23px;color:#94a3b8;margin-top:28px;margin-bottom:auto;line-height:1.5}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the payoff quote
    extra = """
    .q{font-size:64px;font-weight:700;color:#fef08a;line-height:1.25;margin-top:10px}
    .qs{font-size:27px;color:#cbd5e1;margin-top:36px;line-height:1.6;margin-bottom:auto}"""
    body = f'<div class="q">{s["quote"]}</div><div class="qs">{s["quote_sub"]}</div>'
    return extra, body


def design6(s):  # the mechanism
    extra = """
    .steps{display:flex;gap:22px;align-items:stretch;margin-bottom:28px}
    .st{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:28px 24px;background:rgba(125,211,252,.04)}
    .st:last-child{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .sn{font-size:19px;letter-spacing:.12em;color:#7dd3fc;margin-bottom:16px}
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
