#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the helmet-clip post (Claude Code + OpenSCAD, never saw the helmet)."""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
L = '<span class="ltr">{}</span>'.format

S = {
 'en': {
   'dir': 'ltr', 'lang': 'en',
   'eyebrow': 'CLAUDE CODE + OPENSCAD / A PART IT NEVER SAW',
   'shot_title': 'Sena BiKom 20 on a woom kids helmet. Version 20.',
   'chips': [('THE PART', 'Two curved arms into a vent hole,<br>J-tips that latch, leaf springs on the rim.'),
             ('THE DESIGNER', 'Claude Code writing OpenSCAD.<br>Never saw the helmet. I was the eyes.'),
             ('THE WHY', 'My son stops turning around<br>to check I am still there.')],
   'claim': 'CAD written as text<br>is CAD a language<br>model can do.<br>'
            '<span class="hi">20 versions. 2 days.<br>It never saw the helmet.</span>',
   'claim_foot': 'A clip for a Sena BiKom 20 intercom on a woom kids helmet, designed in OpenSCAD by Claude Code from '
                 'two iPhone measurements, a Thingiverse plate and a YouTube timestamp. Every request became a '
                 'parameter; every version is a one-line diff.',
   'before_l': 'WHAT I GAVE IT',
   'before_v': '<div class="r">Photos, two numbers,<br>a YouTube timestamp</div>'
               '<span class="sm">7 cm rim-to-vent outside, 6 cm inside (iPhone Measure). A Thingiverse STL of the '
               'Sena plate. Slant 3D on snap fits at 5:56. Slicer screenshots of what came out wrong.</span>',
   'after_l': 'WHAT CAME BACK',
   'after_v': '<div class="r">' + L('rim_t = 24; hook_o = 140;<br>shell_r = 130; seam_at = 0.85;') + '</div>'
              '<span class="sm">Concentric arcs on the shell radius, J-teeth that cross in the vent, a cantilever '
              'button cut into each arm, zip-tie holes at 80% and a snap-off seam at 85%.</span>',
   'draw_title': 'v20, side profile, as rendered by OpenSCAD',
   'callouts': [('J-teeth', 'cross inside the vent hole from both sides and latch'),
                ('zip-tie holes', 'plan B at 80% of each arm'),
                ('snap seam', '0.8 mm left at 85%, break the tip off by hand'),
                ('leaf springs', 'cut out of the arm wall, button pressing the rim'),
                ('the plate', 'Thingiverse STL, imported, unit clicks on')],
   'grid_title': 'TWENTY VERSIONS IN TWO DAYS',
   'grid': [('v1', 'a C-clip with a shelf. Wrong direction entirely.'),
            ('v5', 'a tapered spring arm with a bump'),
            ('v8', 'both arms curved, hooking the vent hole'),
            ('v10', 'measured: 70 mm outside, 60 mm inside'),
            ('v15', 'J-teeth that latch; compliant wings'),
            ('v16', 'the bridge had filled the rail slot. Fixed.'),
            ('v19', 'both buttons pointed out. Measured the STL, not the render.'),
            ('v20', 'zip-tie holes + snap-off seam, plan B')],
   'grid_foot': 'Each one: a slicer screenshot, one sentence, a new STL within a minute.',
   'big': '20',
   'big_unit': 'versions of a helmet clip, designed by something that cannot see',
   'big_sub': 'Claude Code, OpenSCAD, a Thingiverse plate, two iPhone measurements.<br>'
              '<span class="cy">I was QA. It was the modeller.</span> '
              '<span class="hi">The hard part was explaining "inward".</span>',
   'foot_pos': 'left:44px',
   'foot': 'gal.tidhar.org.il',
 },
 'he': {
   'dir': 'rtl', 'lang': 'he',
   'eyebrow': 'קלוד קוד + OpenSCAD / חלק שהוא אף פעם לא ראה',
   'shot_title': 'Sena BiKom 20 על קסדת woom של ילד. גרסה 20.',
   'chips': [('החלק', 'שתי זרועות מעוקלות לחור האוורור,<br>קצוות J שננעלים, קפיצי עלה על השפה.'),
             ('המעצב', 'קלוד קוד כותב OpenSCAD.<br>לא ראה את הקסדה. אני הייתי העיניים.'),
             ('בשביל מה', 'שהבן שלי יפסיק להסתובב אחורה<br>לבדוק שאני עוד שם.')],
   'claim': 'CAD שכתוב בטקסט<br>זה CAD שמודל שפה<br>יודע לעשות.<br>'
            '<span class="hi">20 גרסאות. יומיים.<br>הוא לא ראה את הקסדה.</span>',
   'claim_foot': 'קליפס לאינטרקום Sena BiKom 20 על קסדת woom של ילד, מעוצב ב-OpenSCAD על ידי קלוד קוד משתי מדידות '
                 'אייפון, פלטה מ-Thingiverse ו-timestamp ביוטיוב. כל בקשה הפכה לפרמטר, כל גרסה היא diff של שורה.',
   'before_l': 'מה נתתי לו',
   'before_v': '<div class="r">תמונות, שני מספרים,<br>timestamp ביוטיוב</div>'
               '<span class="sm">7 ס"מ מהשפה לחור מבחוץ, 6 מבפנים (אפליקציית המדידה). STL של הפלטה של Sena '
               'מ-Thingiverse. סרטון של Slant 3D על snap fits ב-5:56. צילומי מסך מהסלייסר של מה שיצא לא נכון.</span>',
   'after_l': 'מה חזר',
   'after_v': '<div class="r">' + L('rim_t = 24; hook_o = 140;<br>shell_r = 130; seam_at = 0.85;') + '</div>'
              '<span class="sm">קשתות קונצנטריות ברדיוס של הקסדה, שיני J שנפגשות בחור האוורור, כפתור קפיצי '
              'חתוך בכל זרוע, חורים לאזיקונים ב-80% ותפר שבירה ב-85%.</span>',
   'draw_title': 'גרסה 20, פרופיל מהצד, כמו ש-OpenSCAD רינדר אותו',
   'callouts': [('שיני J', 'נכנסות לחור האוורור משני הצדדים וננעלות'),
                ('חורים לאזיקונים', 'תוכנית ב׳ ב-80% מכל זרוע'),
                ('תפר שבירה', '0.8 מ"מ נשארים ב-85%, שוברים את הקצה ביד'),
                ('קפיצי עלה', 'חתוכים מתוך דופן הזרוע, כפתור לוחץ על השפה'),
                ('הפלטה', 'STL מ-Thingiverse, מיובא, היחידה ננעלת עליו')],
   'grid_title': 'עשרים גרסאות ביומיים',
   'grid': [('v1', 'קליפס C עם מדף. כיוון שגוי לגמרי.'),
            ('v5', 'זרוע קפיצית מתחדדת עם בליטה'),
            ('v8', 'שתי זרועות מעוקלות שנתפסות בחור האוורור'),
            ('v10', 'מדוד: 70 מ"מ מבחוץ, 60 מבפנים'),
            ('v15', 'שיני J שננעלות, כנפיים גמישות'),
            ('v16', 'הגשר מילא את מסילת ההרכבה. תוקן.'),
            ('v19', 'שני הכפתורים החוצה. מדדנו את ה-STL, לא את הרנדר.'),
            ('v20', 'חורים לאזיקונים + תפר שבירה, תוכנית ב׳')],
   'grid_foot': 'כל אחת: צילום מסך מהסלייסר, משפט אחד, STL חדש תוך דקה.',
   'big': '20',
   'big_unit': 'גרסאות של קליפס לקסדה, מעוצב על ידי משהו שלא רואה',
   'big_sub': 'קלוד קוד, OpenSCAD, פלטה מ-Thingiverse, שתי מדידות אייפון.<br>'
              '<span class="cy">אני הייתי בקרת האיכות. הוא היה המודלר.</span> '
              '<span class="hi">הקשה היה להסביר "פנימה".</span>',
   'foot_pos': 'right:44px',
   'foot': 'gal.tidhar.org.il',
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
<style>{css}{extra}</style><body>{raw}<div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def design1(s):  # the photo: the real part on the real helmet
    extra = """
    .shot{position:absolute;inset:0 0 148px 0;overflow:hidden}
    .shot img{width:100%;height:100%;object-fit:cover;object-position:38% 62%}
    .veil{position:absolute;inset:0 0 148px 0;
     background:linear-gradient(180deg,rgba(10,22,40,.88) 0,rgba(10,22,40,0) 200px)}
    .wrap{padding:34px 44px 0}
    .eyebrow{margin-bottom:12px}
    .st{font-size:27px;font-weight:700;color:#fff;text-shadow:0 2px 14px rgba(10,22,40,.9)}
    .bar{position:absolute;inset-block-end:0;inset-inline:0;height:148px;background:#0a1628;
     border-block-start:1px solid #1e3a5f;display:flex;align-items:center;padding:0 44px;gap:26px}
    .chip{flex:1;display:flex;gap:14px;align-items:flex-start}
    .chip b{font-size:13px;letter-spacing:.18em;color:#fef08a;white-space:nowrap;padding-top:3px}
    .chip span{font-size:14px;color:#cbd5e1;line-height:1.45}
    .foot{display:none}
    """
    raw = (f'<div class="shot"><img src="file://{HERE}/helmet.jpg"></div><div class="veil"></div>'
           '<div class="bar">' + ''.join(f'<div class="chip"><b>{a}</b><span>{b}</span></div>' for a, b in s['chips']) + '</div>')
    body = f'<div class="st">{s["shot_title"]}</div>'
    return extra, body, raw


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:54px;line-height:1.16;font-weight:700;color:#fff;margin-block-end:26px}
    .cf{font-size:16px;line-height:1.55;color:#94a3b8;max-width:900px}
    """
    body = f'<div class="claim">{s["claim"]}</div><div class="cf">{s["claim_foot"]}</div>'
    return extra, body, ''


def design3(s):  # the exchange
    extra = """
    .cols{display:flex;gap:44px;margin-block-end:40px}
    .col{flex:1;border-inline-start:3px solid #1e3a5f;padding-inline-start:22px}
    .col.b{border-color:#fef08a}
    .lab{font-size:13px;letter-spacing:.2em;color:#7dd3fc;margin-block-end:14px}
    .col.b .lab{color:#fef08a}
    .r{font-size:30px;line-height:1.25;font-weight:700;color:#fff}
    """
    body = (f'<div class="cols"><div class="col"><div class="lab">{s["before_l"]}</div>{s["before_v"]}</div>'
            f'<div class="col b"><div class="lab">{s["after_l"]}</div>{s["after_v"]}</div></div>')
    return extra, body, ''


def design4(s):  # the drawing with callouts
    extra = """
    .lay{display:flex;gap:30px;align-items:center;margin-block-end:30px}
    .pic{width:470px;height:470px;flex:none;position:relative}
    .pic img{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 0 18px rgba(125,211,252,.25))}
    .dt{font-size:14px;color:#7dd3fc;margin-block-end:14px;letter-spacing:.06em}
    .co{list-style:none}
    .co li{font-size:16px;color:#cbd5e1;line-height:1.45;margin-block-end:12px;
     padding-inline-start:18px;border-inline-start:2px solid #fef08a}
    .co b{color:#fef08a;display:block;font-size:15px;letter-spacing:.08em}
    """
    body = (f'<div class="lay"><div class="pic"><img src="file://{HERE}/profile-v20.png"></div>'
            f'<div><div class="dt">{s["draw_title"]}</div><ul class="co">' +
            ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in s['callouts']) + '</ul></div></div>')
    return extra, body, ''


def design5(s):  # the version timeline grid
    extra = """
    .gt{font-size:17px;letter-spacing:.2em;color:#fef08a;margin-block-end:26px}
    .eyebrow{margin-bottom:60px}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px 44px;margin-block-end:30px}
    .cell{display:flex;gap:16px;align-items:baseline;border-block-end:1px solid #1e3a5f;padding-block-end:8px}
    .cell b{font-size:28px;color:#fff;width:70px;flex:none}
    .cell span{font-size:18px;color:#cbd5e1;line-height:1.35}
    .gf{font-size:17px;color:#7dd3fc}
    """
    body = (f'<div class="gt">{s["grid_title"]}</div><div class="grid">' +
            ''.join(f'<div class="cell"><b>{a}</b><span>{b}</span></div>' for a, b in s['grid']) +
            f'</div><div class="gf">{s["grid_foot"]}</div>')
    return extra, body, ''


def design6(s):  # the one big number
    extra = """
    .big{font-size:230px;line-height:.9;font-weight:700;color:#fff;letter-spacing:-.02em}
    .bu{font-size:26px;color:#fef08a;margin-block:18px 26px;font-weight:700}
    .bs{font-size:17px;line-height:1.6;color:#94a3b8;max-width:980px}
    """
    body = f'<div class="big">{s["big"]}</div><div class="bu">{s["big_unit"]}</div><div class="bs">{s["big_sub"]}</div>'
    return extra, body, ''


DESIGNS = [design1, design2, design3, design4, design5, design6]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    for i, fn in enumerate(DESIGNS, 1):
        for lang in ('en', 'he'):
            s = S[lang]
            extra, body, raw = fn(s)
            eb = f'<div class="eyebrow">{s["eyebrow"]}</div>'
            page = TPL.format(dir=s['dir'], lang=s['lang'], css=CSS, extra=extra,
                              eyebrow_block=eb, body=body, foot=s['foot'], raw=raw)
            hp = os.path.join(HERE, f'hero-{i}-{lang}.html')
            pp = os.path.join(HERE, f'hero-{i}-{lang}.png')
            open(hp, 'w', encoding='utf-8').write(page)
            subprocess.run([CHROME, '--headless=new', '--hide-scrollbars',
                            '--force-device-scale-factor=2', '--window-size=1200,630',
                            '--virtual-time-budget=2500', f'--screenshot={pp}',
                            f'file://{hp}'], capture_output=True)
            print('rendered', os.path.basename(pp))


if __name__ == '__main__':
    main()
