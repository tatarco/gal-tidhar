// 6 hero designs x EN/HE = 12 files, one strings table. Style matches blog/agent-browser/gen.js.
const fs = require('fs')
const path = require('path')
const OUT = __dirname

const S = {
  en: {
    dir: 'ltr', arrow: '&rarr;',
    eyebrow: 'FIELD NOTE / AGENTS',
    claim: 'You sent 8 alternatives.<br>I sent 5 agents.',
    claimSub: 'Every tool from the comments, audited in parallel with the same six questions.',
    score: '8 &rarr; 3',
    scoreLabel: 'tools recommended &rarr; tools still standing',
    scoreSub: 'One dies in 6 days. One was steered into a 1Password vault. Only three even play "acts as me".',
    question: 'Who wins when both hands<br>are on the wheel?',
    questionSub: 'The one question that separates agentic browsers. Not price. Not speed.',
    listTitle: 'THE VERDICT',
    list: [
      ['Atlas', 'shutting down Aug 9', 'x'],
      ['Comet', '1Password vault exfil PoC', 'x'],
      ['Firecrawl', 'scraper, different game', 'x'],
      ['Lightpanda', 'no rendering at all', 'x'],
      ['DevTools MCP', 'no login inheritance', 'x'],
      ['Anchor', 'contender - cloud, paid', 'ok'],
      ['agent-browser', 'contender - no handoff', 'ok'],
      ['ego lite', 'handoff + user wins', 'win'],
    ],
    gridTitle: 'The six-question sheet',
    grid: [
      ['01 LOGINS', 'Does it inherit my sessions?'],
      ['02 WALLS', 'Captcha/2FA: stuck, or handoff?'],
      ['03 THE WHEEL', 'Who wins when both grab it?'],
      ['04 FAN-OUT', 'Parallel isolated tasks?'],
      ['05 COST', 'Tool call per click, or a script?'],
      ['06 BLAST RADIUS', 'What can a hijacked agent reach?'],
    ],
    tomb: 'ATLAS',
    tombDates: '2025 - 2026',
    tombSub: 'OpenAI shuts its browser down on Aug 9. One of the 8 tools the comments recommended.',
    foot: 'the full audit - gal.tidhar.org.il/blog/browser-audit',
  },
  he: {
    dir: 'rtl', arrow: '&larr;',
    eyebrow: 'הערת שטח / אייג׳נטים',
    claim: 'שלחתם 8 חלופות.<br>שלחתי 5 אייג׳נטים.',
    claimSub: 'כל כלי מהתגובות, נבדק במקביל עם אותן שש שאלות בדיוק.',
    score: '3 &larr; 8',
    scoreLabel: 'כלים שהומלצו &larr; כלים שנשארו עומדים',
    scoreSub: 'אחת מתה בעוד 6 ימים. אחת הוסטה לתוך כספת 1Password. רק שלוש בכלל משחקות ב"פועל בתור אני".',
    question: 'מי מנצח כששתי ידיים<br>על ההגה?',
    questionSub: 'השאלה האחת שמפרידה בין דפדפני אייג׳נטים. לא מחיר. לא מהירות.',
    listTitle: 'השורה התחתונה',
    list: [
      ['Atlas', 'נסגרת ב-9 באוגוסט', 'x'],
      ['Comet', 'נפרצה לכספת 1Password', 'x'],
      ['Firecrawl', 'סקרייפר, משחק אחר', 'x'],
      ['Lightpanda', 'בלי רינדור בכלל', 'x'],
      ['DevTools MCP', 'לא יורש התחברויות', 'x'],
      ['Anchor', 'מתחרה - ענן, בתשלום', 'ok'],
      ['agent-browser', 'מתחרה - בלי מסירה', 'ok'],
      ['ego lite', 'מסירה + המשתמש מנצח', 'win'],
    ],
    gridTitle: 'שאלון שש השאלות',
    grid: [
      ['01 התחברויות', 'יורש את הסשנים שלי?'],
      ['02 חומות', 'קאפצ׳ה/2FA: נתקע, או מוסר?'],
      ['03 ההגה', 'מי מנצח כששניים תופסים?'],
      ['04 מקביליות', 'משימות מבודדות במקביל?'],
      ['05 עלות', 'קריאת כלי לקליק, או סקריפט?'],
      ['06 רדיוס פיצוץ', 'לאן מגיע אייג׳נט חטוף?'],
    ],
    tomb: 'ATLAS',
    tombDates: '2025 - 2026',
    tombSub: 'OpenAI סוגרת את הדפדפן שלה ב-9 באוגוסט. אחד משמונת הכלים שהומלצו בתגובות.',
    foot: 'the full audit - gal.tidhar.org.il/blog/browser-audit',
  },
}

const BASE = `
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
`

const page = (lang, body, extra = '') => `<!doctype html><html lang="${lang}" dir="${S[lang].dir}"><head><meta charset="utf-8"><style>${BASE}${extra}</style></head><body>${body}</body></html>`

const designs = {
  // 1 - the scoreboard (8 -> 3)
  1: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="num-wrap">
      <div class="num" dir="ltr">${t.score}</div>
      <div class="num-label">${t.scoreLabel}</div>
      <div class="num-sub">${t.scoreSub}</div>
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
  // 3 - the verdict list
  3: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="list-title">${t.listTitle}</div>
    <div class="rows">
      ${t.list.map(([name, verdict, cls]) => `<div class="row ${cls}">
        <span class="mark">${cls === 'x' ? 'x' : cls === 'ok' ? '~' : '+'}</span>
        <span class="name" dir="ltr">${name}</span>
        <span class="verdict">${verdict}</span>
      </div>`).join('')}
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 4 - the one question
  4: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="q-wrap">
      <div class="q">${t.question}</div>
      <div class="q-sub">${t.questionSub}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 5 - the six-question grid
  5: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="grid-title">${t.gridTitle}</div>
    <div class="grid">
      ${t.grid.map(([h, b]) => `<div class="cell"><div class="cell-h">${h}</div><div class="cell-b">${b}</div></div>`).join('')}
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 6 - the tombstone
  6: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="tomb-wrap">
      <div class="tomb" dir="ltr">${t.tomb}</div>
      <div class="tomb-dates" dir="ltr">${t.tombDates}</div>
      <div class="tomb-sub">${t.tombSub}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
}

const CSS = {
  1: `
    .num-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .num{font-size:150px;line-height:1;color:#fef08a;font-weight:600;letter-spacing:.02em;unicode-bidi:isolate;width:max-content}
    .num-label{margin-top:18px;font-size:26px;color:#e0f2fe}
    .num-sub{margin-top:22px;font-size:22px;color:#7dd3fc;line-height:1.6;max-width:30em}
  `,
  2: `
    .claim-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .claim{font-size:64px;line-height:1.22;font-weight:600;color:#e0f2fe;letter-spacing:.01em}
    .claim-sub{margin-top:30px;font-size:24px;color:#7dd3fc;line-height:1.6;max-width:24em}
  `,
  3: `
    .list-title{margin-top:14px;font-size:26px;color:#e0f2fe;letter-spacing:.06em}
    .rows{flex:1;display:flex;flex-direction:column;justify-content:center;gap:9px;margin-bottom:34px}
    .row{display:flex;align-items:baseline;gap:18px;font-size:22px}
    .mark{width:22px;text-align:center;flex:none}
    .row.x .mark{color:#f87171}.row.ok .mark{color:#7dd3fc}.row.win .mark{color:#fef08a}
    .name{color:#e0f2fe;font-weight:600;min-width:250px;unicode-bidi:isolate;text-align:start}
    .row.x .name{color:rgba(224,242,254,.55);text-decoration:line-through;text-decoration-color:rgba(248,113,113,.6)}
    .verdict{color:#bae6fd}
    .row.win .name,.row.win .verdict{color:#fef08a}
  `,
  4: `
    .q-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .q{font-size:60px;line-height:1.25;font-weight:600;color:#e0f2fe}
    .q-sub{margin-top:30px;font-size:24px;color:#7dd3fc;line-height:1.6;max-width:24em}
  `,
  5: `
    .grid-title{margin-top:16px;font-size:32px;color:#e0f2fe}
    .grid{flex:1;display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin:20px 0 40px}
    .cell{border:1px solid rgba(125,211,252,.3);padding:18px 18px;background:rgba(15,40,71,.5);display:flex;flex-direction:column;justify-content:flex-start}
    .cell-h{font-size:15px;letter-spacing:.1em;color:#fef08a;margin-bottom:10px}
    .cell-b{font-size:19px;line-height:1.5;color:#bae6fd}
  `,
  6: `
    .tomb-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;padding-bottom:40px;text-align:center}
    .tomb{font-size:120px;line-height:1;color:#e0f2fe;font-weight:600;letter-spacing:.08em}
    .tomb-dates{margin-top:12px;font-size:34px;color:#f87171;letter-spacing:.2em}
    .tomb-sub{margin-top:26px;font-size:22px;color:#7dd3fc;line-height:1.6;max-width:26em}
  `,
}

for (const n of Object.keys(designs)) {
  for (const lang of ['en', 'he']) {
    fs.writeFileSync(path.join(OUT, `hero-${n}-${lang}.html`), page(lang, designs[n](S[lang]), CSS[n]))
  }
}
console.log('wrote 12 html files')
