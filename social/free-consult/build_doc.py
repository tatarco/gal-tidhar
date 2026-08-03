#!/usr/bin/env python3
"""Build the choices-doc body fragment for the free-consult LinkedIn post."""
import base64, html, pathlib

D = pathlib.Path(__file__).parent

POST = """אמ!לק -> חצי שעה איתי בחינם, לבעלי עסקים שכבר בנו משהו ב-Base44 או בלאבל ונתקעו.

וייב קודינג זה שנירקול. מדהים, אמיתי, ורואים המון - עד עומק מסוים.
ואז מגיע העומק שבו כבר לא שוחים טוב: ארכיטקטורה, ניהול הרשאות, Multi Tenancy, בקאנד שמחזיק כשיש יותר מלקוח אחד. שם צריך צוללן.

אני טוען משהו: הדרישה לתוכנה מותאמת אישית לעסקים קטנים תעלה בעשרות סדרי גודל. ואת החלק של הממשק והחוויה - אין מי שיעשה אותו טוב יותר מבעל העסק עצמו, לפחות בהתחלה. מה שחסר זו הדחיפה בכיוון הנכון, כדי שהדבר שתבנו אשכרה יביא תוצאות.

מה תצאו איתו מחצי השעה:
- מפה של מה לבנות ראשון (ומה לא לבנות בכלל)
- מה אתם יכולים לבנות לבד, ואיפה זה יישבר
- שם קונקרטי אחד של כלי שמתאים לכם

מה יוצא לי מזה?
- גיליתי עולם בעיה חדש. זה לבד שווה את זה.
- הכרתי חבר חדש.
- פתחתי לאדם חדש את הראש. באמת מסב לי אושר לראות את הרעב שנוצר אצל מישהו שמגלה איך טכנולוגיה יכולה לעזור.
- ויבוא יום שהיא או הוא יגיעו לעומק שלא נוח בו. אולי אז יבחרו בי כצוללן.

למי זה כן: בעלי עסקים עם עסק פעיל ובעיה אמיתית.
למי זה לא: מפתחים, מחפשי עבודה, ומי שרוצה שאבנה לו משהו בחינם.

5 סלוטים. אני לבד עם הילדים על החוף בקרואטיה והסקרנות אוכלת אותי, לא בא לי לחכות לספטמבר.

הלינק לקביעה בתגובה הראשונה."""

COMMENT = "קובעים כאן, 5 סלוטים: https://cal.com/gal-tidhar/discovery"

DESIGNS = [
    ("1", "קו העומק", "השכבה הרדודה למעלה, החושך והמונחים הקשים מתחת לקו המקווקו. מסביר את כל התזה במבט אחד."),
    ("2", "הטענה", "משפט אחד ענק: ״וייב קודינג זה שנירקול״. זה הפורמט שבחרת בפוסט הקודם (2-HE) והוא הגיע ל-16.6k."),
    ("3", "ההצעה", "חצי שעה. בחינם. עם שלושת הצ׳יפים של מה מקבלים. הכי CTA-י מכולם."),
    ("4", "המספר", "5 סלוטים בענק. מוכר את הנדירות, לא את התוכן."),
    ("5", "מה תצאו איתו", "רשימת שלושת התוצרים + ״חינם״. הכי אינפורמטיבי, הכי פחות עוצר גלילה."),
    ("6", "הציטוט", "״ויבוא יום שתגיעו לעומק שלא נוח בו״. הפויינט הרגשי, בלי למכור."),
]


def img(stem):
    p = D / f"{stem}.png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (f'<code>{p}</code>'
            f'<img class="hero" alt="{stem}" src="data:image/png;base64,{b64}">')


opts = []
for n, name, why in DESIGNS:
    for style, stem, label in (
            ("dark", f"hero-{n}-he", "כהה · פילד־נוט"),
            ("zazet", f"hero-z{n}-he", "ZaZet · נייר")):
        val = f"{n}-{style}"
        rec = ' <span class="rec">מומלץ</span>' if val == "1-dark" else ""
        opts.append(
            f'<div class="opt" data-value="{val}">'
            f'<div class="opt-head"><b>{n} · {html.escape(name)} — {label}</b>{rec}</div>'
            f'<p class="why">{html.escape(why)}</p>'
            f'{img(stem)}</div>')

heroes = "\n".join(opts)

BODY = f"""
<div class="title">
  <p class="eyebrow">LinkedIn · פוסט קריאה לייעוץ חינם</p>
  <h1>חצי שעה בחינם, <em>ובחירה</em> אחת של תמונה.</h1>
  <p class="lede">הטקסט נעול (אישרת אותו). מה שנשאר: לבחור תמונה אחת מתוך 12, ולהחליט מה הולך לתגובה הראשונה. לוחצים ישירות על הדף - הבחירה נשמרת ואני רואה אותה.</p>
</div>

<section class="step">
  <div class="step-head"><div class="num">01</div><div class="step-title">
    <h2>הטקסט לפוסט</h2>
    <p class="sub">מוכן להדבקה. הלינק לא בגוף הפוסט - בכוונה.</p>
  </div></div>
  <div class="body">
    <div class="copybar"><button class="copybtn" data-copy="post-text">העתקת טקסט הפוסט</button></div>
    <pre id="post-text" class="term he">{html.escape(POST)}</pre>
    <div class="copybar"><button class="copybtn" data-copy="comment-text">העתקת התגובה הראשונה</button></div>
    <pre id="comment-text" class="term he">{html.escape(COMMENT)}</pre>
    <div class="note-box"><b>למה הלינק בתגובה ולא בגוף:</b> לינקדאין מדכא הפצה של פוסטים עם לינק חיצוני בגוף. זה בדיוק העריכה שעשית בעצמך בפוסט של ה-dictation.</div>
  </div>
</section>

<section class="step">
  <div class="step-head"><div class="num">02</div><div class="step-title">
    <h2>בחירת התמונה</h2>
    <p class="sub">שש קונספציות, כל אחת בשתי שפות עיצוב. עברית בלבד. תמונה בודדת - לא קרוסלה.</p>
  </div></div>
  <div class="body">
    <div class="note-box"><b>שתי שפות עיצוב, זו לצד זו.</b> משמאל בכל זוג: <b>כהה / פילד־נוט</b> - נייבי, גריד ציאן, צהוב. מימין: <b>ZaZet / נייר</b> - נייר קריר, דיו, רויאל, Fraunces, בדיוק כמו המסמכים והאתר. שים לב ש-Fraunces הוא פונט לטיני בלבד, ולכן הכותרות בעברית רצות בסאנס נקי והפונט המותגי מופיע בוורדמארק ובמספרים.</div>
    <div class="note-box err"><b>ההמלצה שלי, וזו המלצה לא נוחה: 1 · כהה.</b> שני הפוסטים הכי גדולים שלך (133k ו-16.6k) היו בסגנון הכהה. זו הראיה היחידה שיש לנו, והיא לא על טעם - היא על הגעה. הסגנון של ZaZet יפה יותר וגם עקבי יותר עם המותג, אבל הוא לא נבחן בפיד. אם המטרה היא הפצה - כהה. אם המטרה היא שהתמונה תיראה כמו ZaZet בכל מקום שבו היא תופיע - <b>z1</b> היא הגרסה הכי חזקה בין הנייריות.</div>
    <div class="choices pairs" id="hero" data-persist-choice>
      {heroes}
    </div>
  </div>
</section>

<section class="step">
  <div class="step-head"><div class="num">03</div><div class="step-title">
    <h2>מה הולך לתגובה הראשונה</h2>
    <p class="sub">החלטה אחת: לינק לקביעה בלבד, או גם פוסט בלוג.</p>
  </div></div>
  <div class="body">
    <div class="choices tight" id="firstcomment" data-persist-choice>
      <div class="opt" data-value="cal-only">
        <div class="opt-head"><b>רק cal.com</b> <span class="rec">מומלץ</span></div>
        <p class="why">פוסט CTA. כל קליק שהולך לבלוג הוא קליק שלא הפך לפגישה. זו הסטייה היחידה שלי מהנוהל הרגיל (שדורש פוסט בלוג נלווה) - וזו סטייה מכוונת.</p>
      </div>
      <div class="opt" data-value="cal-plus-blog">
        <div class="opt-head"><b>cal.com + פוסט בלוג</b></div>
        <p class="why">אני כותב פוסט בגל.תדהר על ״העומק שבו וייב קודינג נעצר״ ומוסיף אותו לתגובה. יותר עומק, פחות המרה. אם תבחר בזה - אני בונה אותו עכשיו.</p>
      </div>
    </div>
  </div>
</section>

<section class="step">
  <div class="step-head"><div class="num">04</div><div class="step-title">
    <h2>מה הורדתי מהטיוטה שלך, ולמה</h2>
  </div></div>
  <div class="body">
    <div class="tbl-wrap"><table>
      <tr><th>מה ירד</th><th>למה</th></tr>
      <tr><td>הלינק ל-cal.com מגוף הפוסט</td><td>מדכא הפצה. עבר לתגובה הראשונה.</td></tr>
      <tr><td>״אני עושה Fullstack כנראה טוב כמו המפתח הממוצע״</td><td>עוגן עצמי נמוך. אתה גובה 130k על kollate. הענווה הזאת עולה כסף.</td></tr>
      <tr><td>ההתנצלות על החוף בקרואטיה</td><td>לא ירדה - הוזזה למעלה והפכה לנדירות אמיתית עם מספר (5 סלוטים). זה נכס, לא תירוץ.</td></tr>
      <tr><th>מה נוסף</th><th>למה</th></tr>
      <tr><td>Base44 / לאבל בשורה הראשונה</td><td>המכפיל היחיד שהוכח אצלך: Wiz → 133k, קלוד → 16.6k. שם מוכר בשורה 1.</td></tr>
      <tr><td>״מה תצאו איתו״</td><td>חצי שעה זו יחידת זמן, לא הצעה. עכשיו יש תוצר.</td></tr>
      <tr><td>למי זה כן / למי זה לא</td><td>בלי זה תקבל מפתחים ומחפשי עבודה. חמישה סלוטים לא סובלים סינון גרוע.</td></tr>
      <tr><td>״5 סלוטים״</td><td>נדירות אמיתית וניתנת לאימות - לא טריק שיווקי.</td></tr>
    </table></div>
    <div class="note-box err"><b>מה עוד חסר, ואין לי:</b> הוכחה אחת קונקרטית. ״עשיתי את זה עם הרבה אנשים״ היא טענה. ציטוט אחד מבעל עסק אמיתי (פיטנסאנה?) היה מחזק את הפוסט יותר מכל שינוי ניסוח. אם יש לך משפט כזה - שלח ואני משחיל אותו.</div>
  </div>
</section>

<script src="/copy.js"></script>
<script src="/persist.js"></script>
<style>
.copybar{{display:flex;justify-content:flex-end;margin:18px 0 6px}}
.copybtn{{font:600 13px/1 system-ui;background:#012169;color:#fff;border:0;border-radius:6px;
  padding:9px 16px;cursor:pointer;letter-spacing:.02em}}
.copybtn:hover{{background:#0A1628}}
pre.term.he{{direction:rtl;text-align:right;white-space:pre-wrap;line-height:1.75}}
.choices{{display:grid;gap:18px;margin-top:8px}}
.choices.tight,.choices.pairs{{grid-template-columns:1fr 1fr}}
@media (max-width:720px){{.choices.tight,.choices.pairs{{grid-template-columns:1fr}}}}
.opt{{border:2px solid rgba(10,22,40,.13);border-radius:10px;padding:16px 18px;cursor:pointer;
  transition:border-color .12s,background .12s;background:#fff}}
.opt:hover{{border-color:rgba(1,33,105,.45)}}
.opt.chosen{{border-color:#012169;background:#e8f1fb;box-shadow:inset 0 0 0 1px #012169}}
.opt.chosen .opt-head::after{{content:"נבחר";margin-inline-start:10px;font:700 11px/1 system-ui;
  letter-spacing:.12em;background:#012169;color:#fff;padding:5px 9px;border-radius:4px;vertical-align:middle}}
.opt-head{{font-size:15px;margin-bottom:4px}}
.rec{{font:700 11px/1 system-ui;letter-spacing:.1em;color:#012169;border:1px solid #012169;
  padding:4px 8px;border-radius:4px;margin-inline-start:8px}}
.why{{color:#4a5e78;font-size:14px;margin:0 0 12px}}
.lbl2{{font:700 11px/1 system-ui;letter-spacing:.14em;color:#012169;margin:0 0 6px}}
.opt code{{display:block;font-size:11.5px;direction:ltr;text-align:left;word-break:break-all;
  color:#4a5e78;margin-bottom:8px}}
img.hero{{width:100%;height:auto;display:block;border-radius:6px;border:1px solid rgba(10,22,40,.12)}}
</style>
"""

(D / "doc-body.html").write_text(BODY, encoding="utf-8")
print(D / "doc-body.html")
