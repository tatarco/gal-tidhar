#!/usr/bin/env python3
"""Build the full choices-doc for the Claude Code remote-control LinkedIn post.
Self-contained HTML, dark field-note theme, references the portal's /copy.js + /persist.js."""
import base64, html, pathlib

HERO_DIR = pathlib.Path(__file__).resolve().parent.parent.parent / "blog" / "remote-control"
OUT = pathlib.Path(__file__).parent / "doc.html"

POST = """אמ!לק -> שורה אחת ב-settings.json, ואני שולט בקלוד קוד מהנייד. כל סשן, אוטומטית, בלי להקליד כלום.

כבר שבועות שאני עושה אותו טקס: פותח טרמינל, מריץ קלוד קוד, ואז מקליד /remote-control כדי שאוכל להמשיך לעקוב אחריו מהאפליקציה בנייד. פיצ'ר מעולה, טקס מטומטם - כי הפעם היחידה שתשכח היא הפעם שבה יצאת מהבית, והסשן תקוע על אישור הרשאה, ואף אחד לא ליד המקלדת כדי ללחוץ "אשר".

היום נשבר לי. פתחתי את settings.json לחפש אם אפשר להדליק את זה כברירת מחדל.

אפשר. שורה אחת, ב-~/.claude/settings.json:

"remoteControlAtStartup": true

זהו. כל סשן חדש כבר עולה מחובר לנייד, בלי שאני נוגע בכלום.

הדבר הלא-מובן-מאליו: זה לא שיפור נוחות, זה שינה מתי אני מתחיל משימות. פתאום אני מריץ ריפקטור כבד או ביקורת קוד דווקא לפני שאני יוצא מהבית, ובודק את זה מהטלפון בדרך. המחשב הוא ה-runner, הנייד הוא השלט. הפסקתי להיות כבול לכיסא רק כדי לראות אם משהו נתקע.

מה עוד יש לכם ב-settings.json שאתם עושים ידנית כל יום בלי לדעת שיש הגדרה?

המדריך המלא + השורה המדויקת - בתגובה הראשונה."""

COMMENT = "המדריך המלא + השורה המדויקת: https://gal.tidhar.org.il/blog/remote-control/"

DESIGNS = [
    ("1", "ההחלפה", "כל סשן (אדום, x) מול הגדרה אחת (ציאן, +), עם חץ ביניהם. מסביר את כל המהלך במבט אחד."),
    ("2", "הטענה", "משפט אחד ענק: ״שורה אחת, ואני שולט בקלוד קוד מהנייד״. זה הפורמט שבחרת ב-3 הפוסטים האחרונים, והוא הגיע ל-16.6k ול-133k."),
    ("3", "השורה עצמה", "\"remoteControlAtStartup\": true בענק, כמו קוד. האמינות היא הקונקרטיות - זו השורה המדויקת."),
    ("4", "הארכיטקטורה", "מק ← → נייד, אותו סשן. מסביר את מודל ה-runner/שלט חזותית."),
    ("5", "מה יוצא לך מזה", "רשת של ארבעה: אישור / מעקב / להתחיל וללכת / אוטומטי. הכי אינפורמטיבי, הכי פחות עוצר גלילה."),
    ("6", "המספר", "1 בענק - שורה אחת, כל סשן, לתמיד. מוכר את הפשטות."),
]

REC = "2-he"  # the bold-claim format is his proven winner


def img_block(stem):
    p = HERO_DIR / f"{stem}.png"
    b64 = base64.b64encode(p.read_bytes()).decode()
    return (f'<code class="path">{p}</code>'
            f'<img class="hero" alt="{stem}" src="data:image/png;base64,{b64}">')


opts = []
for n, name, why in DESIGNS:
    for lang, label in (("en", "אנגלית"), ("he", "עברית")):
        stem = f"hero-{n}-{lang}"
        rec = ' <span class="rec">מומלץ</span>' if stem == f"hero-{REC}" else ""
        opts.append(
            f'<div class="opt" data-value="{n}-{lang}">'
            f'<div class="opt-head"><b>{n} · {html.escape(name)} — {label}</b>{rec}</div>'
            f'<p class="why">{html.escape(why)}</p>'
            f'{img_block(stem)}</div>')
heroes = "\n".join(opts)

PAGE = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>פוסט לינקדאין - remoteControlAtStartup · Gal Tidhar</title>
<style>
:root{{--bg:#0a1628;--panel:rgba(15,40,71,.55);--cyan:#7dd3fc;--ink:#e0f2fe;
  --text:#bae6fd;--muted:rgba(186,230,253,.55);--accent:#fef08a;--border:rgba(125,211,252,.45)}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"IBM Plex Mono","Arial Hebrew",system-ui,monospace;background:var(--bg);
  color:var(--text);line-height:1.7;padding:40px 20px;
  background-image:linear-gradient(rgba(125,211,252,.05) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(125,211,252,.05) 1px,transparent 1px);
  background-size:24px 24px}}
.wrap{{max-width:900px;margin:0 auto}}
.eyebrow{{color:var(--cyan);letter-spacing:.14em;font-size:13px;text-transform:uppercase}}
h1{{color:var(--ink);font-size:28px;line-height:1.3;margin:8px 0 12px}}
h1 em{{color:var(--accent);font-style:normal}}
.lede{{color:var(--muted);font-size:15px;margin-bottom:30px}}
.step{{border:1px solid var(--border);background:var(--panel);padding:22px 24px;margin-bottom:22px}}
.step-head{{display:flex;gap:14px;align-items:baseline;margin-bottom:16px;border-bottom:1px dashed var(--border);padding-bottom:12px}}
.num{{color:var(--accent);font-weight:600;font-size:14px;letter-spacing:.1em}}
.step h2{{color:var(--ink);font-size:17px;font-weight:600}}
.sub{{color:var(--muted);font-size:13px}}
.copybar{{display:flex;justify-content:flex-start;margin:6px 0}}
.copybtn{{font:600 13px/1 system-ui;background:var(--cyan);color:#0a1628;border:0;border-radius:6px;
  padding:10px 18px;cursor:pointer;letter-spacing:.02em}}
.copybtn:hover{{background:var(--accent)}}
pre.term{{border:1px solid var(--border);background:rgba(0,0,0,.28);padding:16px 18px;
  white-space:pre-wrap;font-size:13.5px;line-height:1.7;color:var(--text);margin:4px 0 8px}}
pre.term.he{{direction:rtl;text-align:right}}
pre.term.ltr{{direction:ltr;text-align:left}}
.note{{border:1px dashed var(--border);padding:12px 16px;font-size:13.5px;color:var(--text);margin:10px 0}}
.note b{{color:var(--cyan)}}
.note.rec b{{color:var(--accent)}}
.choices{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:12px}}
@media(max-width:720px){{.choices{{grid-template-columns:1fr}}}}
.opt{{border:2px solid var(--border);border-radius:10px;padding:14px 16px;cursor:pointer;
  transition:border-color .12s,background .12s;background:rgba(10,22,40,.5)}}
.opt:hover{{border-color:var(--cyan)}}
.opt.chosen{{border-color:var(--accent);background:rgba(254,240,138,.08);box-shadow:inset 0 0 0 1px var(--accent)}}
.opt.chosen .opt-head::after{{content:"נבחר";margin-inline-start:10px;font:700 10px/1 system-ui;
  letter-spacing:.12em;background:var(--accent);color:#0a1628;padding:5px 8px;border-radius:4px;vertical-align:middle}}
.opt-head{{font-size:14px;color:var(--ink);margin-bottom:4px}}
.rec{{font:700 10px/1 system-ui;letter-spacing:.1em;color:var(--accent);border:1px solid var(--accent);
  padding:4px 7px;border-radius:4px;margin-inline-start:8px}}
.why{{color:var(--muted);font-size:13px;margin:0 0 10px}}
code.path{{display:block;font-size:11px;direction:ltr;text-align:left;word-break:break-all;
  color:var(--cyan);margin-bottom:8px}}
img.hero{{width:100%;height:auto;display:block;border-radius:6px;border:1px solid var(--border)}}
table{{width:100%;border-collapse:collapse;font-size:13.5px;margin-top:6px}}
th,td{{border:1px solid var(--border);padding:8px 12px;text-align:right;vertical-align:top}}
th{{color:var(--muted);font-size:12px;letter-spacing:.06em;background:rgba(0,0,0,.2)}}
</style>
</head>
<body>
<div class="wrap">
  <p class="eyebrow">LinkedIn · Claude Code · remoteControlAtStartup</p>
  <h1>שורה אחת, <em>ובחירה אחת</em> של תמונה.</h1>
  <p class="lede">הטקסט מוכן. מה שנשאר: לבחור תמונה אחת מתוך 12 (6 קונספטים × עברית/אנגלית), ולאשר את התגובה הראשונה. לוחצים ישירות על הדף - הבחירה נשמרת ואני רואה אותה.</p>

  <section class="step">
    <div class="step-head"><div class="num">01</div><div class="step-title">
      <h2>הטקסט לפוסט</h2><p class="sub">מוכן להדבקה. הלינק בתגובה הראשונה - לא בגוף הפוסט, בכוונה.</p>
    </div></div>
    <div class="copybar"><button class="copybtn" data-copy="post-text">העתקת טקסט הפוסט</button></div>
    <pre id="post-text" class="term he">{html.escape(POST)}</pre>
    <div class="copybar"><button class="copybtn" data-copy="comment-text">העתקת התגובה הראשונה</button></div>
    <pre id="comment-text" class="term he">{html.escape(COMMENT)}</pre>
    <div class="note"><b>למה הלינק בתגובה:</b> לינקדאין מדכא הפצה של פוסטים עם לינק חיצוני בגוף. בדיוק העריכה שעשית בעצמך בפוסט של ה-dictation.</div>
  </section>

  <section class="step">
    <div class="step-head"><div class="num">02</div><div class="step-title">
      <h2>בחירת התמונה</h2><p class="sub">שישה קונספטים, כל אחד בעברית ובאנגלית. תמונה בודדת - לא קרוסלה.</p>
    </div></div>
    <div class="note rec"><b>ההמלצה שלי: 2 · עברית - הטענה.</b> שלושת הפוסטים הכי גדולים שלך (133k, 37k, 16.6k) היו כולם תמונה בודדת עם משפט־טענה ענק. זה הפורמט שאתה בוחר בו כל פעם, וזה הפורמט שמגיע. שם מוכר בשורה 1 (קלוד קוד) כבר יש לנו בטקסט.</div>
    <div class="choices" id="hero" data-persist-choice>
      {heroes}
    </div>
  </section>

  <section class="step">
    <div class="step-head"><div class="num">03</div><div class="step-title">
      <h2>מה בניתי, בקצרה</h2>
    </div></div>
    <table>
      <tr><th>מה</th><th>איפה</th></tr>
      <tr><td>פוסט בלוג מלא (המדריך + הקאוויאטים הכנים)</td><td>gal.tidhar.org.il/blog/remote-control/ - הולך לתגובה הראשונה</td></tr>
      <tr><td>כרטיס בעמוד הבית (Writing · field notes)</td><td>נוסף ראשון, למעלה</td></tr>
      <tr><td>og.png</td><td>מוגדר ל-2-EN (יתעדכן אם תבחר אחרת)</td></tr>
      <tr><td>ההגדרה עצמה</td><td>נוספה כבר ל-~/.claude/settings.json שלך</td></tr>
    </table>
    <div class="note"><b>שאלת הסיום נשארה בטיוטה,</b> אבל בפוסט הקודם (ego-lite) חתכת אותה וסיימת על ה-pointer לתגובה. אם בא לך לחתוך גם כאן - פשוט מחק את השורה עם סימן השאלה.</div>
  </section>
</div>
<script src="/copy.js"></script>
<script src="/persist.js"></script>
</body>
</html>
"""

OUT.write_text(PAGE, encoding="utf-8")
print(OUT)
