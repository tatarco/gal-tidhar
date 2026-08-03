// Generates 6 hero designs x 2 languages = 12 HTML files, driven by ONE strings table.
const fs = require('fs')
const path = require('path')
const OUT = __dirname

const S = {
  en: {
    dir: 'ltr', arrow: '&rarr;', backArrow: '&larr;',
    eyebrow: 'FIELD NOTE / CLAUDE CODE',
    claim: 'Never type /remote-control<br>again. It is always on.',
    claimSub: 'One line arms it at startup - every session, automatically. No ritual, no forgetting.',
    oldLabel: 'EVERY SESSION',
    oldLines: ['type /remote-control by hand', 'forget once = stuck at the desk', 'away from keys = blind'],
    newLabel: 'ONE SETTING',
    newLines: ['always on, every session', 'nothing to type, ever', 'leave - it stays connected'],
    quote: '"remoteControlAtStartup": true',
    quoteSub: 'In ~/.claude/settings.json. You already know /remote-control. This line makes it permanent - on by default, every session.',
    archYou: 'MAC',
    archAgent: 'PHONE',
    archSpace: 'THE REMOTE',
    archNote: 'always connected, over claude.ai and the mobile app',
    archBrowser: 'ONE SESSION, TWO SCREENS',
    gridTitle: 'What always-on buys you',
    grid: [
      ['ALWAYS ON', 'No /remote-control ritual. Every new session boots already connected.'],
      ['NEVER FORGET', 'The one time you forget is the time it matters. Now there is nothing to forget.'],
      ['START & GO', 'Kick off heavy work before you leave. Approve the steps from the road.'],
      ['ONE LINE', 'remoteControlAtStartup: true. Set it once, done forever.'],
    ],
    bigNum: '1',
    bigNumLabel: 'line, always on, forever',
    bigNumSub: 'You were retyping /remote-control every session. This makes it permanent - on by default, automatically.',
    foot: 'Claude Code - remoteControlAtStartup: true - gal.tidhar.org.il',
  },
  he: {
    dir: 'rtl', arrow: '&larr;', backArrow: '&rarr;',
    eyebrow: 'הערת שטח / קלוד קוד',
    claim: 'לא להקליד <span class="cmd">/remote-control</span><br>שוב. הוא תמיד דלוק.',
    claimSub: 'שורה אחת מדליקה אותו בהפעלה - כל סשן, אוטומטית. בלי טקס, בלי לשכוח.',
    oldLabel: 'כל סשן',
    oldLines: ['להקליד <span class="cmd">/remote-control</span> ידנית', 'שכחת פעם אחת = תקוע במחשב', 'לא ליד המקלדת = עיוור'],
    newLabel: 'הגדרה אחת',
    newLines: ['תמיד דלוק, כל סשן', 'אין מה להקליד, אף פעם', 'יוצאים - נשאר מחובר'],
    quote: '"remoteControlAtStartup": true',
    quoteSub: 'ב-<span class="cmd">~/.claude/settings.json</span>. את <span class="cmd">/remote-control</span> כולם מכירים. השורה הזאת הופכת אותו לקבוע - דלוק כברירת מחדל, בכל סשן.',
    archYou: 'מק',
    archAgent: 'נייד',
    archSpace: 'השלט',
    archNote: 'תמיד מחובר, דרך claude.ai והאפליקציה בנייד',
    archBrowser: 'סשן אחד, שני מסכים',
    gridTitle: 'מה נותן לך ״תמיד דלוק״',
    grid: [
      ['תמיד דלוק', 'בלי טקס <span class="cmd">/remote-control</span>. כל סשן חדש עולה כבר מחובר.'],
      ['לא לשכוח', 'הפעם שתשכח היא הפעם שזה חשוב. עכשיו אין מה לשכוח.'],
      ['להתחיל וללכת', 'מריצים עבודה כבדה לפני שיוצאים. מאשרים צעדים מהדרך.'],
      ['שורה אחת', 'remoteControlAtStartup: true. מגדירים פעם אחת, נגמר.'],
    ],
    bigNum: '1',
    bigNumLabel: 'שורה, תמיד דלוק, לתמיד',
    bigNumSub: 'הקלדת <span class="cmd">/remote-control</span> בכל סשן. זה הופך אותו לקבוע - דלוק כברירת מחדל, אוטומטית.',
    foot: 'Claude Code - remoteControlAtStartup: true - gal.tidhar.org.il',
  },
}

const BASE = `
  @font-face { font-family:'IBM Plex Mono'; src:local('IBM Plex Mono'); }
  *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
  html,body{width:1200px;height:630px}
  body{
    font-family:"IBM Plex Mono","Arial Hebrew","Arial Unicode MS",monospace;
    background:#0a1628;color:#bae6fd;overflow:hidden;position:relative;
    background-image:linear-gradient(rgba(125,211,252,.06) 1px,transparent 1px),
                     linear-gradient(90deg,rgba(125,211,252,.06) 1px,transparent 1px);
    background-size:24px 24px;-webkit-font-smoothing:antialiased;
  }
  .frame{position:absolute;inset:28px;border:1px solid rgba(125,211,252,.45);padding:38px 44px;display:flex;flex-direction:column}
  .eyebrow{font-size:14px;letter-spacing:.16em;color:#7dd3fc;text-transform:uppercase}
  .foot{position:absolute;bottom:44px;inset-inline-start:74px;font-size:13px;color:rgba(186,230,253,.5);direction:ltr;letter-spacing:.04em}
  .cyan{color:#7dd3fc} .ink{color:#e0f2fe} .amber{color:#fef08a}
  .muted{color:rgba(186,230,253,.55)}
  .cmd{direction:ltr;unicode-bidi:isolate;display:inline-block}
`

const page = (lang, body, extra = '') => `<!doctype html><html lang="${lang}" dir="${S[lang].dir}"><head><meta charset="utf-8"><style>${BASE}${extra}</style></head><body>${body}</body></html>`

const designs = {
  // 1 - the exchange (before / after)
  1: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="cols">
      <div class="col old">
        <div class="col-label">${t.oldLabel}</div>
        ${t.oldLines.map(l => `<div class="li x">${l}</div>`).join('')}
      </div>
      <div class="mid">${t.arrow}</div>
      <div class="col new">
        <div class="col-label new-label">${t.newLabel}</div>
        ${t.newLines.map(l => `<div class="li ok">${l}</div>`).join('')}
      </div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 2 - the claim
  2: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="claim-wrap">
      <div class="claim">${t.claim}</div>
      <div class="claim-sub">${t.claimSub}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 3 - the literal setting line
  3: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="q-wrap">
      <div class="q-bar"><div class="q-term">${t.quote}</div></div>
      <div class="q-sub">${t.quoteSub}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 4 - the architecture
  4: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="arch-title">${t.archBrowser}</div>
    <div class="arch">
      <div class="node">${t.archYou}</div>
      <div class="bar"><span class="hand">${t.arrow}</span><span class="hand back">${t.backArrow}</span></div>
      <div class="node agent">${t.archAgent}<div class="space">${t.archSpace}</div></div>
    </div>
    <div class="arch-note">${t.archNote}</div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 5 - the breakdown grid
  5: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="grid-title">${t.gridTitle}</div>
    <div class="grid">
      ${t.grid.map(([h, b]) => `<div class="cell"><div class="cell-h">${h}</div><div class="cell-b">${b}</div></div>`).join('')}
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 6 - the one big number
  6: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="num-wrap">
      <div class="num">${t.bigNum}</div>
      <div class="num-label">${t.bigNumLabel}</div>
      <div class="num-sub">${t.bigNumSub}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
}

const CSS = {
  1: `
    .cols{flex:1;display:flex;align-items:center;gap:26px;margin-top:8px}
    .col{flex:1;border:1px solid rgba(125,211,252,.28);padding:26px 24px;min-height:300px}
    .col.new{border-color:#7dd3fc;background:rgba(125,211,252,.06)}
    .col-label{font-size:16px;letter-spacing:.12em;color:rgba(186,230,253,.55);margin-bottom:20px;text-transform:uppercase}
    .new-label{color:#fef08a}
    .li{font-size:22px;line-height:1.6;margin-bottom:14px;padding-inline-start:26px;position:relative;color:#bae6fd}
    .li::before{position:absolute;inset-inline-start:0}
    .li.x::before{content:'x';color:#f87171}
    .li.ok::before{content:'+';color:#7dd3fc}
    .col.new .li{color:#e0f2fe}
    .mid{font-size:40px;color:#fef08a}
  `,
  2: `
    .claim-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .claim{font-size:64px;line-height:1.22;font-weight:600;color:#e0f2fe;letter-spacing:.01em}
    .claim-sub{margin-top:30px;font-size:24px;color:#7dd3fc;line-height:1.6;max-width:22em}
  `,
  3: `
    .q-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .q-bar{border-inline-start:4px solid #7dd3fc;padding-inline-start:24px}
    .q-term{direction:ltr;unicode-bidi:isolate;display:inline-block;font-size:44px;color:#fef08a;letter-spacing:.01em}
    .q-sub{margin-top:34px;font-size:25px;color:#e0f2fe;line-height:1.65;max-width:24em}
  `,
  4: `
    .arch-title{margin-top:22px;font-size:18px;letter-spacing:.18em;color:rgba(186,230,253,.55);text-transform:uppercase}
    .arch{flex:1;display:flex;align-items:center;gap:20px;margin-top:-10px}
    .node{flex:1;border:1px solid #7dd3fc;padding:34px 26px;font-size:34px;color:#e0f2fe;text-align:center;background:rgba(125,211,252,.06)}
    .node.agent{border-color:#fef08a;background:rgba(254,240,138,.06)}
    .space{margin-top:14px;font-size:17px;color:#fef08a;letter-spacing:.1em}
    .bar{display:flex;flex-direction:column;gap:12px;font-size:34px;color:#7dd3fc}
    .hand.back{color:#fef08a}
    .arch-note{font-size:20px;color:rgba(186,230,253,.6);margin-bottom:34px}
  `,
  5: `
    .grid-title{margin-top:18px;font-size:34px;color:#e0f2fe}
    .grid{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0 40px}
    .cell{border:1px solid rgba(125,211,252,.3);padding:18px 20px;background:rgba(15,40,71,.5)}
    .cell-h{font-size:15px;letter-spacing:.12em;color:#fef08a;text-transform:uppercase;margin-bottom:10px}
    .cell-b{font-size:18px;line-height:1.55;color:#bae6fd}
  `,
  6: `
    .num-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .num{font-size:180px;line-height:.9;color:#fef08a;font-weight:600}
    .num-label{margin-top:14px;font-size:44px;color:#e0f2fe}
    .num-sub{margin-top:26px;font-size:23px;color:#7dd3fc;line-height:1.6;max-width:26em}
  `,
}

for (const n of Object.keys(designs)) {
  for (const lang of ['en', 'he']) {
    const html = page(lang, designs[n](S[lang]), CSS[n])
    fs.writeFileSync(path.join(OUT, `hero-${n}-${lang}.html`), html)
  }
}
console.log('wrote 12 html files')
