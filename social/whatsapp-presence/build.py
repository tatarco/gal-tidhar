#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the whatsapp-presence post (my own bridge silenced my phone)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# ponytail: every Latin run inside Hebrew text is isolated with .ltr (direction + isolate),
# learned across four bidi incidents in this repo's earlier heroes.
LTR = '<span class="ltr">{}</span>'
L = LTR.format

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / WHATSAPP WENT SILENT',
   'big':'One line',
   'big_unit':'of my own code stopped my phone from ever notifying me again.',
   'big_sub':'A linked device that reports you as online tells WhatsApp not to<br>'
             'bother pushing to your phone. My bridge announced me online<br>'
             '<span class="cy">24/7, from the day I built it</span>.<br>'
             '<span class="hi">Two weeks of silence. The bug was mine.</span>',
   'claim':'WhatsApp stopped notifying me.<br>'
           '<span class="hi">The problem was not WhatsApp.</span>',
   'claim_foot':'Every iOS setting was correct. Calls still rang. I was one click from reinstalling the app - and the cause was a default in a library I had linked to my own number.',
   'before_l':'CALLS',
   'before_v':'rang perfectly<br><span class="sm">a separate VoIP path that ignores presence</span>',
   'after_l':'MESSAGES',
   'after_v':'total silence<br><span class="sm">push is skipped while any device says you are online</span>',
   'grid_title':'WHAT I CHECKED, AND WHAT IT WAS NOT',
   'grid': [('Every iOS notification setting','on, lock screen ticked'),
            ('Focus modes, per-chat mutes','all clear'),
            ('Reset notification settings','no change'),
            ('Reinstall the app','about to, would not have helped'),
            ('My own WhatsApp bridge','this one')],
   'grid_foot':'The one thing I never suspected was the thing I built myself.',
   'quote':'Calls rang.<br>Messages did not.',
   'quote_sub':'That is the whole diagnosis. Calls come in over CallKit, a<br>'
               'separate push path that ignores presence. If calls work and<br>'
               'messages do not, the network is fine and the permissions are<br>'
               'fine - something is telling WhatsApp you are already reading.',
   'arch':[('THE COMPARISON MISFIRES','a partial update<br>carries no name, so<br>the push-name check<br>is true every time'),
           ('THE ATTRIBUTE IS DROPPED','undefined attrs are<br>stripped on encode,<br>so the node goes<br>out completely bare'),
           ('BARE MEANS ONLINE','a presence node<br>with no type reads<br>as "available" -<br>on every message')],
   'arch_foot':'Three correct-looking steps. Together they silence a real person’s phone.',
   'claim8':'I found it, traced it,<br>and shipped the fix upstream.',
   'pillars':['ONE-LINE GUARD','REGRESSION TEST','410 TESTS PASS'],
   'fix_before':'BEFORE',
   'fix_after':'AFTER',
   'fix_arrow':'→',
   'fix_bv':'silence',
   'fix_av':'notifications',
   'claim8_foot':'The same fix was proposed in an earlier PR and closed by a stale bot with nothing changed. It had no test. That is the part I added.',
   'foot':'gal.tidhar.org.il/blog/whatsapp-presence',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'שורה אחת',
   'big_unit':'בקוד שאני כתבתי השתיקה לי את ההתראות בטלפון.',
   'big_sub':'מכשיר מקושר שמדווח שאתה אונליין אומר לוואטסאפ שאין טעם<br>'
             'לדחוף לך התראה לטלפון. הבריידג׳ שלי הכריז עלי אונליין<br>'
             '<span class="cy">24/7, מהיום שבניתי אותו</span>.<br>'
             '<span class="hi">שבועיים של שקט. הבאג היה שלי.</span>',
   'claim':'וואטסאפ הפסיק להתריע לי.<br>'
           '<span class="hi">הבעיה לא היתה בוואטסאפ.</span>',
   'claim_foot':'כל הגדרה באייפון היתה תקינה. שיחות דווקא צלצלו. הייתי קליק אחד ממחיקה והתקנה מחדש - והסיבה היתה ברירת מחדל בספרייה שאני עצמי קישרתי למספר שלי.',
   'before_l':'שיחות',
   'before_v':'צלצלו מצוין<br><span class="sm">ערוץ נפרד לגמרי, שלא מסתכל על נוכחות</span>',
   'after_l':'הודעות',
   'after_v':'שקט מוחלט<br><span class="sm">כשמכשיר כלשהו אומר שאתה אונליין, לא נשלחת התראה</span>',
   'grid_title':'מה בדקתי, ומה זה לא היה',
   'grid': [('כל הגדרות ההתראות באייפון','דלוקות, מסך נעילה מסומן'),
            ('מצבי פוקוס, השתקת צ׳אטים','הכל נקי'),
            ('איפוס הגדרות ההתראות','שום שינוי'),
            ('מחיקה והתקנה מחדש','כמעט עשיתי. לא היה עוזר'),
            ('הבריידג׳ שאני כתבתי','זה היה זה'),],
   'grid_foot':'הדבר היחיד שלא חשדתי בו היה הדבר שבניתי בעצמי.',
   'quote':'שיחות צלצלו.<br>הודעות לא.',
   'quote_sub':'זו כל האבחנה. שיחות בוואטסאפ נכנסות בערוץ נפרד שלא<br>'
               'מסתכל בכלל על נוכחות. אם שיחות עובדות והודעות לא,<br>'
               'הרשת בסדר וההרשאות בסדר - ומשהו אומר לוואטסאפ<br>'
               'שאתה כבר קורא את ההודעה עכשיו.',
   'arch':[('ההשוואה נכשלת','עדכון חלקי מגיע<br>בלי שם, אז הבדיקה<br>של שם התצוגה<br>יוצאת נכונה תמיד'),
           ('התכונה נזרקת','ערכים לא מוגדרים<br>נמחקים בקידוד, אז<br>הצומת יוצא ריק<br>לגמרי'),
           ('ריק = אונליין','צומת נוכחות בלי<br>סוג נקרא כ"זמין"<br>- וזה קורה בכל<br>הודעה נכנסת')],
   'arch_foot':'שלושה שלבים שכל אחד מהם נראה נכון. ביחד הם משתיקים טלפון של בנאדם אמיתי.',
   'claim8':'מצאתי, עקבתי לשורש,<br>ושלחתי את התיקון אפסטרים.',
   'pillars':['שורת הגנה אחת','טסט רגרסיה','410 טסטים עוברים'],
   'fix_before':'לפני',
   'fix_after':'אחרי',
   'fix_arrow':'←',
   'fix_bv':'שקט',
   'fix_av':'התראות',
   'claim8_foot':'אותו תיקון בדיוק כבר הוצע בפול־ריקווסט קודם, ונסגר על ידי בוט אחרי חודש בלי ששינו כלום. לא היה לו טסט. זה החלק שהוספתי.',
   'foot':'gal.tidhar.org.il/blog/whatsapp-presence',
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


def design8(s):  # the claim + the three pillars + the real before/after
    extra = """
    .c8{font-size:44px;font-weight:700;line-height:1.28;max-width:1040px;margin-bottom:22px}
    .pill{display:flex;gap:12px;margin-bottom:30px;flex-wrap:wrap}
    .pill span{border:1px solid #7dd3fc;color:#7dd3fc;border-radius:999px;
     padding:8px 20px;font-size:20px;font-weight:600;letter-spacing:.04em}
    .fix{display:flex;align-items:center;gap:24px;margin-bottom:18px}
    .fcell{border:1px solid #1e3a5f;border-radius:12px;padding:16px 24px;background:rgba(125,211,252,.04)}
    .fcell.hot{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .flbl{font-size:13px;letter-spacing:.14em;color:#7dd3fc;margin-bottom:8px}
    .fcell.hot .flbl{color:#fef08a}
    .fval{font-size:36px;font-weight:700;color:#94a3b8;line-height:1.15;white-space:nowrap}
    .fcell.hot .fval{color:#fef08a}
    .arw{font-size:36px;color:#7dd3fc;flex:none}
    .c8f{font-size:21px;color:#94a3b8;max-width:1010px;line-height:1.5;margin-bottom:auto}
    .mid{margin-bottom:auto}"""
    pills = "".join(f'<span>{x}</span>' for x in s['pillars'])
    body = (f'<div class="mid"><div class="c8">{s["claim8"]}</div>'
            f'<div class="pill">{pills}</div>'
            f'<div class="fix">'
            f'<div class="fcell"><div class="flbl">{s["fix_before"]}</div>'
            f'<div class="fval">{s["fix_bv"]}</div></div>'
            f'<div class="arw">{s["fix_arrow"]}</div>'
            f'<div class="fcell hot"><div class="flbl">{s["fix_after"]}</div>'
            f'<div class="fval">{s["fix_av"]}</div></div>'
            f'</div><div class="c8f">{s["claim8_foot"]}</div></div>')
    return extra, body


DESIGNS = [design1, design2, design3, design4, design5, design6, None, design8]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    for i, fn in enumerate(DESIGNS, 1):
        if fn is None:
            continue
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
