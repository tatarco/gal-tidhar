#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the ferry-outreach post (comments as a bug tracker)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
# ponytail: every Latin run inside Hebrew text is isolated with .ltr, learned across four bidi incidents.
L = '<span class="ltr">{}</span>'.format

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / CROATIANFERRIES.COM',
   'big':'31 minutes',
   'big_unit':'From a stranger correcting my Croatian to the fix live in production.',
   'big_sub':'I posted a ferry site into <span class="cy">52 Facebook groups</span> in Croatia and treated<br>'
             'the comments as my issue tracker. <span class="hi">11 of the 25 issues in the repo were<br>'
             'opened by people I have never met.</span> All 11 are closed.',
   'claim':'The comments are<br>my bug tracker.<br>'
           '<span class="hi">52 groups, 153 comments,<br>11 issues opened by strangers.</span>',
   'claim_foot':'One script sweeps all 52 posts and prints every comment I have not seen. I translate it. Anything that is a real complaint becomes an issue, gets fixed, and I reply on the thread in the language the person wrote in.',
   'before_l':'THE COMMENT, HOUR 0',
   'before_v':'“The word <span class="hi">vozni red</span> grates<br>on the ear. That is what a<br>bus timetable is called.<br>A ferry has a <span class="hi">plovidbeni red</span>.”'
              '<br><span class="sm">Mirela, in a Croatian island group</span>',
   'after_l':'SHIPPED, 31 MINUTES LATER',
   'after_v':'Wording fixed<br>site-wide, deployed,<br>answered on the thread<br>in Croatian.'
             '<br><span class="sm">No market research was going to hand me that word.</span>',
   'grid_title':'WHAT A FACEBOOK COMMENT TURNED INTO',
   'grid': [('“vozni red” is bus language, not ferry','fixed + deployed, 31 min'),
            ('“valid to 6.9, not 27.9”','footnote parser bug, 34 min'),
            ('“I cannot find Stinica - Mišnjak”','whole operator added, 58 min'),
            ('“the Prizna camera misses the queue”','he was right, I checked'),
            ('“Or just download their app????”','the competitor issue')],
   'grid_foot':'11 of the 25 issues in the repo were opened by strangers in the comments. All 11 are closed.',
   'quote':'“Do you need an app<br>to cross the road too?”',
   'quote_sub':'The rudest comment I got was also the most useful one.<br>'
               'My first instinct was to write him a long reasoned reply.<br>'
               'I deleted it and opened an issue instead, because he had<br>'
               'just told me for free where the bar is.',
   'arch':[('SWEEP','one script walks all 52<br>posts and prints every<br>comment not yet<br>in the ledger'),
           ('TRIAGE','translate it. Praise is<br>noise. A complaint<br>becomes a GitHub issue<br>with the quote in it'),
           ('REPLY','fix, deploy, then answer<br>on the thread itself in<br>Croatian, German or<br>English, whichever he used')],
   'arch_foot':'52 posts. 37 I can measure: 1,211 likes, 153 comments. 15 I cannot measure at all - 6 still held for admin approval.',
   'foot':'croatianferries.com',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'31 דקות',
   'big_unit':'מהרגע שזר תיקן לי את הקרואטית ועד שהתיקון עלה לאוויר.',
   'big_sub':'פרסמתי אתר מעבורות ב<span class="cy">-52 קבוצות פייסבוק</span> בקרואטיה, והפכתי את<br>'
             'התגובות לבאג טראקר. <span class="hi">11 מתוך 25 האישיוז בריפו נפתחו על ידי<br>'
             'אנשים שלא פגשתי מעולם.</span> כל ה-11 סגורים.',
   'claim':'התגובות בפייסבוק<br>הן הבאג טראקר שלי.<br>'
           '<span class="hi">52 קבוצות, 153 תגובות,<br>11 אישיוז שזרים פתחו לי.</span>',
   'claim_foot':'סקריפט אחד עובר על כל 52 הפוסטים ומוציא כל תגובה שעוד לא ראיתי. אני מתרגם. כל דבר שהוא תלונה אמיתית הופך לאישיו, מתוקן, ואני חוזר לתגובה עצמה בשפה שבה האדם כתב.',
   'before_l':'התגובה, שעה 0',
   'before_v':'"המילה <span class="hi">'+L('vozni red')+'</span> צורמת לאוזניים. ככה קוראים ללוח זמנים של אוטובוס. למעבורת קוראים <span class="hi">'+L('plovidbeni red')+'</span>."'
              '<br><span class="sm">מירלה, בקבוצה של אי קרואטי</span>',
   'after_l':'באוויר, 31 דקות אחר כך',
   'after_v':'הניסוח תוקן בכל<br>האתר, עלה לפרודקשן,<br>וחזרתי אליה בתגובה<br>בקרואטית.'
             '<br><span class="sm">שום מחקר שוק לא היה נותן לי את המילה הזאת.</span>',
   'grid_title':'למה הפכה תגובה בפייסבוק',
   'grid': [('"'+L('vozni red')+' זה אוטובוס, לא מעבורת"','תוקן ועלה לאוויר, 31 דקות'),
            ('"תקף עד 6.9, לא עד 27.9"','באג בפרסור הערות שוליים, 34 דקות'),
            ('"אני לא מוצאת את '+L('Stinica - Mišnjak')+'"','מפעיל שלם נוסף, 58 דקות'),
            ('"המצלמה בפריזנה לא מכסה את התור"','הוא צדק, הלכתי לבדוק'),
            ('"'+L('Or just download their app????')+'"','האישיו של המתחרים')],
   'grid_foot':'11 מתוך 25 האישיוז בריפו נפתחו על ידי זרים בתגובות. כל ה-11 סגורים.',
   'quote':'"אתה צריך אפליקציה<br>גם כדי לחצות את הכביש?"',
   'quote_sub':'התגובה הכי גסה שקיבלתי הייתה גם הכי שימושית.<br>'
               'התגובה הראשונה שלי הייתה לכתוב לו תשובה ארוכה ומנומקת.<br>'
               'מחקתי אותה ופתחתי אישיו במקום, כי הוא בדיוק<br>'
               'אמר לי בחינם איפה הרף.',
   'arch':[('סריקה','סקריפט אחד עובר על<br>כל 52 הפוסטים ומוציא<br>כל תגובה שעוד לא<br>נמצאת בלוג'),
           ('טריאז׳','לתרגם. מחמאה היא<br>רעש. תלונה הופכת<br>לאישיו בגיטהאב עם<br>הציטוט בפנים'),
           ('חזרה','לתקן, לעלות לאוויר,<br>ואז לענות בתגובה עצמה<br>בקרואטית, גרמנית או<br>אנגלית, לפי מה שהוא כתב')],
   'arch_foot':'52 פוסטים. 37 אני מודד: 1,211 לייקים, 153 תגובות. 15 אני לא מודד בכלל - 6 מהם עדיין תקועים באישור מנהל.',
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
.sm{font-size:.55em;color:#94a3b8;font-weight:400;display:inline-block;margin-top:14px;line-height:1.5}
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
    .unit{font-size:30px;color:#7dd3fc;margin-top:18px}
    .sub{font-size:25px;color:#cbd5e1;margin-top:30px;max-width:1060px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:52px;font-weight:700;line-height:1.34;max-width:1060px}
    .cfoot{font-size:23px;color:#94a3b8;margin-top:32px;max-width:1010px;line-height:1.55}
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
    .val{font-size:29px;font-weight:700;line-height:1.5}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val hi">{s["after_v"]}</div></div></div>'
    return extra, body


def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 22px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:14px 0;border-block-end:1px solid #16304f;font-size:24px;line-height:1.4}
    .row .amt{color:#fef08a;font-weight:600;text-align:end;max-width:46%;flex:none}
    .gf{font-size:21px;color:#94a3b8;margin-top:24px;margin-bottom:auto;line-height:1.5}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the payoff quote (the hate comment)
    extra = """
    .q{font-size:60px;font-weight:700;color:#fef08a;line-height:1.28;margin-top:10px}
    .qs{font-size:26px;color:#cbd5e1;margin-top:36px;line-height:1.6;margin-bottom:auto}"""
    body = f'<div class="q">{s["quote"]}</div><div class="qs">{s["quote_sub"]}</div>'
    return extra, body


def design6(s):  # the pipeline
    extra = """
    .steps{display:flex;gap:22px;align-items:stretch;margin-bottom:28px}
    .st{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:28px 24px;background:rgba(125,211,252,.04)}
    .st:last-child{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .sn{font-size:19px;letter-spacing:.15em;color:#7dd3fc;margin-bottom:16px}
    .st:last-child .sn{color:#fef08a}
    .sd{font-size:22px;line-height:1.5;color:#e2e8f0}
    .af{font-size:23px;color:#fef08a;font-weight:700;margin-bottom:auto;line-height:1.45}"""
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
