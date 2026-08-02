// 6 hero designs x 2 languages, one strings table.
const fs = require('fs'), path = require('path'), OUT = __dirname

const S = {
  en: {
    dir: 'ltr', eyebrow: 'RESEARCH FINDINGS / EGO LITE BROWSER',
    arc: ['One comment asked the right question.', 'I found ghost clicks.', 'So I measured ego lite properly.'],
    arcSub: 'The agent clicks. The page receives nothing. The tool reports success.',
    claim: 'Ghost clicks.',
    claimSub: 'Claude clicked the button. The button was not clicked. The tool said everything went fine.',
    rHead: 'What the tool reported vs what the page actually got',
    rows: [
      ['click under a transparent overlay', 'fine', '0'],
      ['click on pointer-events: none', 'fine', '0'],
      ['click on empty coordinates', 'fine', '0'],
      ['type into a locked field', 'fine', 'empty'],
      ['selector that does not exist', 'ERROR', '-'],
    ],
    rCol: ['ACTION', 'TOOL SAID', 'ACTUALLY'],
    verdict: 'An agent browser\'s click is<br>Playwright\'s force: true.<br>Always on.',
    verdictSub: 'Playwright checks that the element is attached, visible, stable, enabled, and really receives the click. force skips all of it.',
    lineHead: 'THE BOUNDARY',
    lineA: 'Found the button? Yes.',
    lineB: 'Did anything happen? No.',
    lineC: '"cannot find the button"  ->  error\n"found it, clicked, nothing"  ->  fine',
    phantomHead: 'AN EDIT THAT NEVER HAPPENED',
    phantomBody: 'I typed into a locked field. The value stayed empty - but the page still got input and change events. An app listening for those will light up its Save button over an edit that never happened.',
    fixHead: 'THE FIX: ONE LINE',
    fixCode: 'const before = await js(`window.__clicks`)\nawait click(\'#target\')\nconst after  = await js(`window.__clicks`)\n// after === before  ->  it never landed',
    fixSub: 'Do not ask whether the action succeeded. Ask whether anything changed.',
    foot: 'gal.tidhar.org.il',
  },
  he: {
    dir: 'rtl', eyebrow: 'תוצאות מחקר / דפדפן ego lite',
    arc: ['תגובה אחת שאלה בדיוק את השאלה הנכונה.', 'מצאתי לחיצות רפאים.', 'אז מדדתי את ego lite ברצינות.'],
    arcSub: 'האייג׳נט לוחץ, הדף לא מקבל כלום, והכלי מדווח שהכל עבר בהצלחה.',
    claim: 'לחיצות רפאים.',
    claimSub: 'קלוד לחץ על הכפתור. הכפתור לא נלחץ. הכלי אמר שהכל תקין.',
    rHead: 'מה הכלי דיווח מול מה שהדף באמת קיבל',
    rows: [
      ['לחיצה מתחת ל-overlay שקוף', 'תקין', '0'],
      ['לחיצה על pointer-events: none', 'תקין', '0'],
      ['לחיצה על קואורדינטות ריקות', 'תקין', '0'],
      ['כתיבה לשדה נעול', 'תקין', 'ריק'],
      ['סלקטור שלא קיים', 'שגיאה', '-'],
    ],
    rCol: ['פעולה', 'הכלי אמר', 'בפועל'],
    verdict: 'הקליק של דפדפן אייג׳נטי<br>הוא force: true של Playwright.<br>תמיד דלוק.',
    verdictSub: 'Playwright בודק לפני כל פעולה שהאלמנט מחובר, נראה, יציב, מאופשר, ושהוא באמת מקבל את הלחיצה. force מדלג על הכל.',
    lineHead: 'איפה עובר הגבול',
    lineA: 'מצא את הכפתור? כן.',
    lineB: 'קרה משהו? לא.',
    lineC: '"לא מצאתי את הכפתור"  ->  שגיאה\n"מצאתי, לחצתי, כלום"  ->  תקין',
    phantomHead: 'עריכה שלא קרתה',
    phantomBody: 'כתבתי לשדה נעול. הערך נשאר ריק, אבל הדף בכל זאת קיבל אירועי input ו-change. אפליקציה שמאזינה להם תדליק כפתור שמירה על עריכה שלא היתה.',
    fixHead: 'התיקון: שורה אחת',
    fixCode: 'const before = await js(`window.__clicks`)\nawait click(\'#target\')\nconst after  = await js(`window.__clicks`)\n// after === before  ->  זה לא נחת',
    fixSub: 'לא לשאול אם הפעולה הצליחה. לשאול אם משהו השתנה.',
    foot: 'gal.tidhar.org.il',
  }
}

const BASE = `
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  html,body{width:1200px;height:630px}
  body{font-family:"IBM Plex Mono","Arial Hebrew","Arial Unicode MS",monospace;
    background:#0a1628;color:#bae6fd;overflow:hidden;
    background-image:linear-gradient(rgba(125,211,252,.06) 1px,transparent 1px),
                     linear-gradient(90deg,rgba(125,211,252,.06) 1px,transparent 1px);
    background-size:24px 24px;-webkit-font-smoothing:antialiased}
  .frame{position:absolute;inset:28px;border:1px solid rgba(125,211,252,.45);padding:34px 42px;display:flex;flex-direction:column}
  .eyebrow{font-size:14px;letter-spacing:.16em;color:#7dd3fc;text-transform:uppercase}
  .foot{position:absolute;bottom:42px;inset-inline-start:72px;font-size:13px;color:rgba(186,230,253,.5);letter-spacing:.04em}
`
const page = (lang, body, extra='') =>
  `<!doctype html><html lang="${lang}" dir="${S[lang].dir}"><head><meta charset="utf-8"><style>${BASE}${extra}</style></head><body>${body}</body></html>`

const designs = {
  1: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="cw"><div class="arc">${t.arc.map((l,i)=>`<div class="arcl a${i}">${l}</div>`).join('')}</div>
    <div class="csub">${t.arcSub}</div></div>
    <div class="foot">${t.foot}</div></div>`,
  2: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="rh">${t.rHead}</div>
    <table class="tbl"><thead><tr>${t.rCol.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>
    ${t.rows.map(([a,b,c])=>`<tr><td class="act">${a}</td><td class="${b.match(/ERROR|שגיאה/)?'thr':'ok'}">${b}</td><td class="land">${c}</td></tr>`).join('')}
    </tbody></table>
    <div class="foot">${t.foot}</div></div>`,
  3: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="vw"><div class="verdict">${t.verdict}</div><div class="vsub">${t.verdictSub}</div></div>
    <div class="foot">${t.foot}</div></div>`,
  4: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="lh">${t.lineHead}</div>
    <div class="lw"><div class="la">${t.lineA}</div><div class="lb">${t.lineB}</div>
    <pre class="lc">${t.lineC}</pre></div>
    <div class="foot">${t.foot}</div></div>`,
  5: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="ph"><div class="phh">${t.phantomHead}</div>
    <div class="phbox"><span class="lbl">value</span><span class="empty">""</span></div>
    <div class="phev">input <span class="syn">synthetic</span> &nbsp; change <span class="syn">synthetic</span></div>
    <div class="phb">${t.phantomBody}</div></div>
    <div class="foot">${t.foot}</div></div>`,
  7: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="gw"><div class="gclaim">${t.claim}</div><div class="gsub">${t.claimSub}</div></div>
    <div class="foot">${t.foot}</div></div>`,
  6: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="fh">${t.fixHead}</div>
    <pre class="code">${t.fixCode}</pre>
    <div class="fsub">${t.fixSub}</div>
    <div class="foot">${t.foot}</div></div>`,
}

const CSS = {
  1:`.cw{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:36px}
     .arcl{font-size:42px;line-height:1.42;font-weight:600}
     .a0{color:#7dd3fc} .a1{color:#f87171} .a2{color:#e0f2fe}
     .csub{margin-top:30px;font-size:21px;color:rgba(186,230,253,.7);line-height:1.6;max-width:30em}`,
  2:`.rh{margin-top:20px;font-size:19px;color:#e0f2fe;letter-spacing:.02em}
     .tbl{flex:1;width:100%;border-collapse:collapse;margin:20px 0 46px;font-size:20px}
     .tbl th{font-size:13px;letter-spacing:.12em;color:rgba(186,230,253,.55);text-transform:uppercase;
       text-align:start;padding:0 14px 10px;border-bottom:1px solid rgba(125,211,252,.35);font-weight:400}
     .tbl td{padding:13px 14px;border-bottom:1px solid rgba(125,211,252,.14);text-align:start}
     .act{color:#bae6fd} .ok{color:#4ade80} .thr{color:#fef08a} .land{color:#f87171;font-weight:600}`,
  3:`.vw{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:36px}
     .verdict{font-size:50px;line-height:1.34;font-weight:600;color:#fef08a}
     .vsub{margin-top:30px;font-size:21px;color:#bae6fd;line-height:1.62;max-width:30em}`,
  4:`.lh{margin-top:20px;font-size:15px;letter-spacing:.14em;color:rgba(186,230,253,.55);text-transform:uppercase}
     .lw{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:36px}
     .la{font-size:34px;color:#4ade80;margin-bottom:10px}
     .lb{font-size:34px;color:#f87171;margin-bottom:34px}
     .lc{font-size:22px;line-height:1.9;color:#e0f2fe;border-inline-start:3px solid #7dd3fc;
       padding-inline-start:22px;direction:ltr;unicode-bidi:isolate;display:inline-block;text-align:start}`,
  5:`.ph{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:36px}
     .phh{font-size:15px;letter-spacing:.14em;color:rgba(186,230,253,.55);text-transform:uppercase;margin-bottom:22px}
     .phbox{border:1px solid #f87171;padding:16px 22px;font-size:30px;display:inline-flex;gap:18px;align-items:center;align-self:flex-start}
     .lbl{color:rgba(186,230,253,.55);font-size:17px;letter-spacing:.1em}
     .empty{color:#f87171}
     .phev{margin-top:18px;font-size:22px;color:#e0f2fe;direction:ltr;unicode-bidi:isolate;display:inline-block;align-self:flex-start}
     .syn{color:#4ade80;font-size:16px;letter-spacing:.08em}
     .phb{margin-top:26px;font-size:20px;color:#bae6fd;line-height:1.6;max-width:32em}`,
  6:`.fh{margin-top:20px;font-size:30px;color:#e0f2fe}
     .code{flex:1;margin:22px 0 10px;font-size:19px;line-height:1.85;color:#7dd3fc;
       border:1px solid rgba(125,211,252,.35);background:rgba(0,0,0,.28);padding:22px 26px;
       direction:ltr;unicode-bidi:isolate;text-align:start;white-space:pre}
     .fsub{font-size:21px;color:#fef08a;margin-bottom:38px}`,
  7:`.gw{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:36px}
     .gclaim{font-size:96px;line-height:1.1;font-weight:600;color:#f87171;letter-spacing:.01em}
     .gsub{margin-top:34px;font-size:26px;color:#e0f2fe;line-height:1.55;max-width:24em}`,
}

for (const n of Object.keys(designs))
  for (const lang of ['en','he'])
    fs.writeFileSync(path.join(OUT, `hero-${n}-${lang}.html`), page(lang, designs[n](S[lang]), CSS[n]))
console.log('wrote 12')
