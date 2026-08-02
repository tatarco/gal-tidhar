// 6 hero designs x 2 languages, one strings table.
const fs = require('fs'), path = require('path'), OUT = __dirname

const S = {
  en: {
    dir: 'ltr', eyebrow: 'FIELD NOTE / AGENTS',
    claim: 'Claude clicked the button.<br>The button was not clicked.<br>Claude said it went fine.',
    claimSub: 'Five ways an agent action silently does nothing - and the one line that catches all of them.',
    rHead: 'WHAT THE TOOL SAID vs WHAT THE PAGE SAW',
    rows: [
      ['click, covered by a transparent overlay', 'ok', '0'],
      ['click, pointer-events: none', 'ok', '0'],
      ['click on empty coordinates', 'ok', '0'],
      ['type into a disabled field', 'ok', 'empty'],
      ['selector that does not exist', 'THREW', '-'],
    ],
    rCol: ['ACTION', 'RETURNED', 'LANDED'],
    verdict: 'ego lite\'s click is<br>Playwright\'s force: true,<br>always on.',
    verdictSub: 'Playwright checks attached, visible, stable, enabled, receives events. force skips all five. That is the default here.',
    lineHead: 'THE LINE THAT MATTERS',
    lineA: 'It verifies it FOUND the target.',
    lineB: 'It does not verify anything HAPPENED.',
    lineC: '"cannot find the button"  ->  error\n"found it, clicked, nothing"  ->  ok',
    phantomHead: 'THE PHANTOM EDIT',
    phantomBody: 'Typing into a disabled field left the value empty - but the page still received synthetic input and change events. The app can react to a change that never happened. The agent is told nothing.',
    fixHead: 'THE FIX IS ONE LINE',
    fixCode: 'const before = await js(`window.__clicks`)\nawait click(\'#target\')\nconst after  = await js(`window.__clicks`)\n// after === before  ->  it did not land',
    fixSub: 'Do not assert the action succeeded. Assert something changed.',
    foot: 'gal.tidhar.org.il - measured, not assumed',
  },
  he: {
    dir: 'rtl', eyebrow: 'הערת שטח / אייג׳נטים',
    claim: 'קלוד לחץ על הכפתור.<br>הכפתור לא נלחץ.<br>קלוד אמר שהכל בסדר.',
    claimSub: 'חמש דרכים שבהן פעולה של אייג׳נט לא עושה כלום בשקט - ושורה אחת שתופסת את כולן.',
    rHead: 'מה הכלי דיווח מול מה שהדף באמת ראה',
    rows: [
      ['לחיצה מתחת ל-overlay שקוף', 'בסדר', '0'],
      ['לחיצה על pointer-events: none', 'בסדר', '0'],
      ['לחיצה על קואורדינטות ריקות', 'בסדר', '0'],
      ['כתיבה לשדה disabled', 'בסדר', 'ריק'],
      ['סלקטור שלא קיים', 'זרק שגיאה', '-'],
    ],
    rCol: ['פעולה', 'הוחזר', 'נחת'],
    verdict: 'הקליק של ego lite<br>הוא force: true<br>של Playwright, תמיד דלוק.',
    verdictSub: 'Playwright בודק מחובר, נראה, יציב, מאופשר, ומקבל אירועים. force מדלג על כל החמישה. פה זו ברירת המחדל.',
    lineHead: 'הגבול האמיתי',
    lineA: 'הוא מאמת שהוא מצא את המטרה.',
    lineB: 'הוא לא מאמת שקרה משהו.',
    lineC: '"לא מצאתי את הכפתור"  ->  שגיאה\n"מצאתי, לחצתי, כלום"  ->  בסדר',
    phantomHead: 'העריכה שלא קרתה',
    phantomBody: 'כתיבה לשדה disabled השאירה אותו ריק - אבל הדף כן קיבל אירועי input ו-change סינתטיים. האפליקציה יכולה להגיב לשינוי שמעולם לא קרה. האייג׳נט לא יודע כלום.',
    fixHead: 'התיקון הוא שורה אחת',
    fixCode: 'const before = await js(`window.__clicks`)\nawait click(\'#target\')\nconst after  = await js(`window.__clicks`)\n// after === before  ->  זה לא נחת',
    fixSub: 'לא לבדוק שהפעולה הצליחה. לבדוק שמשהו השתנה.',
    foot: 'gal.tidhar.org.il - נמדד, לא הונח',
  },
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
    <div class="cw"><div class="claim">${t.claim}</div><div class="csub">${t.claimSub}</div></div>
    <div class="foot">${t.foot}</div></div>`,
  2: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="rh">${t.rHead}</div>
    <table class="tbl"><thead><tr>${t.rCol.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>
    ${t.rows.map(([a,b,c])=>`<tr><td class="act">${a}</td><td class="${b.match(/THREW|זרק/)?'thr':'ok'}">${b}</td><td class="land">${c}</td></tr>`).join('')}
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
  6: t => `<div class="frame"><div class="eyebrow">${t.eyebrow}</div>
    <div class="fh">${t.fixHead}</div>
    <pre class="code">${t.fixCode}</pre>
    <div class="fsub">${t.fixSub}</div>
    <div class="foot">${t.foot}</div></div>`,
}

const CSS = {
  1:`.cw{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:36px}
     .claim{font-size:52px;line-height:1.32;font-weight:600;color:#e0f2fe}
     .csub{margin-top:28px;font-size:22px;color:#7dd3fc;line-height:1.6;max-width:26em}`,
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
}

for (const n of Object.keys(designs))
  for (const lang of ['en','he'])
    fs.writeFileSync(path.join(OUT, `hero-${n}-${lang}.html`), page(lang, designs[n](S[lang]), CSS[n]))
console.log('wrote 12')
