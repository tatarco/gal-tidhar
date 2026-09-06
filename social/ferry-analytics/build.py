#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the ferry-analytics post (episode 2: what Google says ranks)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
L = '<span class="ltr">{}</span>'.format

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'THE BEST MARITIME PORTAL IN CROATIA / EPISODE 2',
   'big':'Position 5',
   'big_unit':'For the live port camera at Merag. I never tried to rank for it.',
   'big_sub':'The one thing <span class="cy">no competing ferry site has</span> was already in the<br>'
             'top ten, and <span class="hi">the page title never said the word camera.</span><br>'
             'Meanwhile the busiest crossing in Croatia sits at 57.',
   'claim':'The only thing I have<br>that nobody else has<br>was already ranking.<br>'
           '<span class="hi">My own title never<br>mentioned it.</span>',
   'claim_foot':'Live port cameras, embedded per port. Position 5 on "hak merag", 8 on "hak kamera porozina", 9 on "hak kamera brestova". No competing ferry site carries them at all. 16 of my 99 ports have one, and until this week not one title said so.',
   'before_l':'WHAT I AIMED AT',
   'before_v':'<div class="r">“fähre kroatien” <span class="hi">49</span></div>'
              '<div class="r">“fähre split supetar” <span class="hi">57</span></div>'
              '<div class="r">“dubrovnik to split ferry” <span class="hi">67</span></div>'
              '<span class="sm">The head terms. A week old site is not winning these.</span>',
   'after_l':'WHAT ACTUALLY RANKS',
   'after_v':'<div class="r">“hak merag” <span class="hi">5</span></div>'
             '<div class="r">“hak kamera porozina” <span class="hi">8</span></div>'
             '<div class="r">Sumartin - Makarska <span class="hi">6</span></div>'
             '<div class="r">Zadar - Preko <span class="hi">9</span></div>'
             '<span class="sm">Live cameras and one named pair of ports. Nobody aimed at these.</span>',
   'grid_title':'WHAT GOOGLE ACTUALLY SHOWS PEOPLE',
   'grid': [('“hak merag” - the live port camera','position 5'),
            ('“hak kamera porozina”','position 8'),
            ('Sumartin - Makarska, one named pair','position 6'),
            ('Zadar - Preko, one named pair','position 9'),
            ('“ferries croatia”, the head term','position 49'),
            ('Split - Supetar, the busiest crossing','position 57')],
   'grid_foot':'Nobody aimed at the top four. Every phrase I would have chosen on purpose is at the bottom.',
   'cut_l':'WHAT GOOGLE SHOWED, 278 OF 396 PORT PAGES',
   'cut_v':'Trajekti i katamarani iz luke Zadar Libu',
   'cut_n':'87 characters. Google shows about 60.',
   'fix_l':'WHAT IT SHOWS NOW',
   'fix_v':'Fähren ab Merag (Cres) · Fahrplan und Live-Kamera',
   'fix_n':'Under 60, and it finally says the thing nobody else has.',
   'arch':[('3,164 IN THE SITEMAP','up from 316 in one<br>deploy. Google finds<br>them on its own<br>schedule'),
           ('7 A DAY','the API reports<br>index status but<br>cannot request it.<br>That is a manual click'),
           ('110 OF 180 INDEXED','island pages, four<br>languages, counted<br>every morning at 09:40<br>from the live sitemap')],
   'arch_foot':'en 43/45 &middot; it 20/45 &middot; de 32/45 &middot; hr 15/45. It was 0/45 across the board when the pages shipped.',
   'foot':'croatianferries.com',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'הפורטל הימי הכי טוב בקרואטיה / פרק 2',
   'big':'מקום 5',
   'big_unit':'על המצלמה החיה של הנמל במרג. לא ניסיתי להגיע לשם.',
   'big_sub':'הדבר היחיד ש<span class="cy">אין לאף אתר מעבורות מתחרה</span> כבר היה בעשירייה<br>'
             'הראשונה, ו<span class="hi">הכותרת של העמוד לא אמרה את המילה מצלמה.</span><br>'
             'במקביל, המעבר הכי עמוס בקרואטיה יושב במקום 57.',
   'claim':'הדבר היחיד שיש לי<br>ואין לאף אחד אחר<br>כבר היה מדורג.<br>'
           '<span class="hi">הכותרת שלי בכלל<br>לא הזכירה אותו.</span>',
   'claim_foot':'מצלמות נמל חיות, מוטמעות בעמוד של כל נמל. מקום 5 על '+L('hak merag')+', 8 על '+L('hak kamera porozina')+', 9 על '+L('hak kamera brestova')+'. לאף אתר מעבורות מתחרה אין את זה בכלל. ל-16 מ-99 הנמלים שלי יש מצלמה, ועד השבוע אף כותרת לא אמרה את זה.',
   'before_l':'למה כיוונתי',
   'before_v':'<div class="r">'+L('"fähre kroatien"')+' <span class="hi">49</span></div>'
              '<div class="r">'+L('"fähre split supetar"')+' <span class="hi">57</span></div>'
              '<div class="r">'+L('"dubrovnik to split ferry"')+' <span class="hi">67</span></div>'
              '<span class="sm">ביטויי הראש. אתר בן שבוע לא מנצח עליהם.</span>',
   'after_l':'מה באמת מדורג',
   'after_v':'<div class="r">'+L('"hak merag"')+' <span class="hi">5</span></div>'
             '<div class="r">'+L('"hak kamera porozina"')+' <span class="hi">8</span></div>'
             '<div class="r">'+L('Sumartin - Makarska')+' <span class="hi">6</span></div>'
             '<div class="r">'+L('Zadar - Preko')+' <span class="hi">9</span></div>'
             '<span class="sm">מצלמות חיות וזוג נמלים אחד בשם מלא. אף אחד לא כיוון לשם.</span>',
   'grid_title':'מה גוגל באמת מראה לאנשים',
   'grid': [('"'+L('hak merag')+'", המצלמה החיה של הנמל','מקום 5'),
            ('"'+L('hak kamera porozina')+'"','מקום 8'),
            (L('Sumartin - Makarska')+', זוג נמלים בשם מלא','מקום 6'),
            (L('Zadar - Preko')+', זוג נמלים בשם מלא','מקום 9'),
            ('"'+L('fähre kroatien')+'", ביטוי הראש','מקום 49'),
            (L('Split - Supetar')+', המעבר הכי עמוס','מקום 57')],
   'grid_foot':'לארבעת הראשונים אף אחד לא כיוון. כל ביטוי שהייתי בוחר בכוונה נמצא בתחתית.',
   'cut_l':'מה גוגל הציג, ב-278 מתוך 396 עמודי נמל',
   'cut_v':'Trajekti i katamarani iz luke Zadar Libu',
   'cut_n':'87 תווים. גוגל מציג בערך 60.',
   'fix_l':'מה מוצג עכשיו',
   'fix_v':'Trajekti iz luke Merag (Cres) · red plovidbe i kamera uživo',
   'fix_n':'מתחת ל-60, וסוף סוף אומר את הדבר שאין לאף אחד אחר: '+L('kamera uživo')+', מצלמה חיה.',
   'arch':[('3,164 בסייטמאפ','עלה מ-316 בדיפלוי<br>אחד. גוגל מוצא<br>אותם בקצב שלו'),
           ('7 ביום','ה-'+L('API')+' יודע להגיד<br>אם עמוד מאונדקס,<br>אבל לא לבקש. הבקשה<br>היא קליק ידני'),
           ('110 מתוך 180','עמודי איים, ארבע<br>שפות, נספרים כל בוקר<br>ב-9:40 מהסייטמאפ החי')],
   'arch_foot':L('en 43/45')+' &middot; '+L('it 20/45')+' &middot; '+L('de 32/45')+' &middot; '+L('hr 15/45')+'. ביום שהעמודים עלו זה היה 0/45 בכל השפות.',
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
    .cfoot{font-size:22px;color:#94a3b8;margin-top:32px;max-width:1010px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="claim">{s["claim"]}</div>' \
           f'<div class="cfoot">{s["claim_foot"]}</div></div>'
    return extra, body


def design3(s):  # the exchange - aimed at vs actually ranks
    extra = """
    .cells{display:flex;gap:30px;margin-bottom:auto;align-items:stretch}
    .cell{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:34px 30px;background:rgba(125,211,252,.04)}
    .cell.hot{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .lbl{font-size:17px;letter-spacing:.13em;color:#7dd3fc;line-height:1.5;margin-bottom:22px}
    .cell.hot .lbl{color:#fef08a}
    .val{font-size:27px;font-weight:700;line-height:1.6}
    .r{margin-bottom:10px}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val">{s["after_v"]}</div></div></div>'
    return extra, body


def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 18px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:12px 0;border-block-end:1px solid #16304f;font-size:23px;line-height:1.4}
    .row .amt{color:#fef08a;font-weight:600;text-align:end;flex:none}
    .gf{font-size:21px;color:#94a3b8;margin-top:22px;margin-bottom:auto;line-height:1.5}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the artifact - the sawn-off title itself
    extra = """
    .lbl{font-size:17px;letter-spacing:.13em;color:#94a3b8;margin-bottom:16px}
    .serp{font-size:34px;font-weight:700;direction:ltr;text-align:left;line-height:1.35;
     color:#cbd5e1;border-inline-start:4px solid #ef4444;padding-inline-start:22px}
    .serp .saw{color:#ef4444}
    .note{font-size:21px;color:#94a3b8;margin-top:14px}
    .gap{height:40px}
    .lbl2{font-size:17px;letter-spacing:.13em;color:#fef08a;margin-bottom:16px}
    .serp2{font-size:34px;font-weight:700;direction:ltr;text-align:left;line-height:1.35;
     color:#fef08a;border-inline-start:4px solid #fef08a;padding-inline-start:22px}
    .mid{margin-bottom:auto}"""
    body = (f'<div class="mid"><div class="lbl">{s["cut_l"]}</div>'
            f'<div class="serp">{s["cut_v"]}<span class="saw">&#9608;</span></div>'
            f'<div class="note">{s["cut_n"]}</div><div class="gap"></div>'
            f'<div class="lbl2">{s["fix_l"]}</div>'
            f'<div class="serp2">{s["fix_v"]}</div>'
            f'<div class="note">{s["fix_n"]}</div></div>')
    return extra, body


def design6(s):  # 99 / 16 / 83
    extra = """
    .steps{display:flex;gap:22px;align-items:stretch;margin-bottom:28px}
    .st{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:28px 24px;background:rgba(125,211,252,.04)}
    .st:nth-child(2){border-color:#fef08a;background:rgba(254,240,138,.07)}
    .sn{font-size:19px;letter-spacing:.15em;color:#7dd3fc;margin-bottom:16px}
    .st:nth-child(2) .sn{color:#fef08a}
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
            eb = f'<div class="eyebrow">{s["eyebrow"]}</div>'
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
