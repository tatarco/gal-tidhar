// Generates 6 hero designs x 2 languages = 12 HTML files, driven by ONE strings table.
const fs = require('fs')
const path = require('path')
const OUT = __dirname

const S = {
  en: {
    dir: 'ltr', arrow: '&rarr;', backArrow: '&larr;',
    eyebrow: '<b class="brandmark">ego lite</b> / AGENT IDENTITY',
    claim: 'My agent cannot<br>browse as me.',
    claimSub: 'One ego lite profile per client, declared by email, and an agent that is refused the wrong one.',
    oldLabel: 'BEFORE',
    oldLines: ['task space is born on the active profile', 'the option was accepted and ignored', 'client work, personal account'],
    newLabel: 'AFTER / EGO LITE',
    newLines: ['project declares one email', 'space pinned to that profile', 'unscoped run is rejected'],
    quote: 'accepted, then ignored',
    quoteSub: 'I passed a profile. The function took it, said nothing, and dropped it. Three times I asked for the client. Three times I got myself.',
    archYou: 'PROJECT',
    archAgent: 'TASK SPACE',
    archSpace: 'client profile',
    archNote: '.claude/ego-profile declares the email. The map from email to profile builds itself.',
    archBrowser: 'EGO LITE - ONE BROWSER, MANY IDENTITIES',
    gridTitle: 'The guard, in front of every ego lite run',
    grid: [
      ['BY EMAIL', 'Projects name an account, never "Profile 4". Ids shift, and two profiles share a name.'],
      ['SELF-MAPPING', 'It opens each profile and reads who is signed in. Add a client, nothing to edit.'],
      ['PINNED', 'createTaskSpace(name, profile) binds the space, even while the browser sits elsewhere.'],
      ['REFUSED', 'A command that does not name its scope never reaches the browser.'],
    ],
    bigNum: '1',
    bigNumLabel: 'email per project',
    bigNumSub: 'The client hands me an internal account, and everything I build stays inside it. ego lite was the last hole, and now it is shut.',
    askLabel: 'YOU',
    ask: 'open github.com/acme/checkout-api',
    replyLabel: 'AGENT',
    reply: '404 - Not Found',
    reveal: 'The repo is fine. The task space was born on a random profile, and to <b>that</b> account the repo does not exist.',
    nf: 'NOT FOUND',
    nfSub: 'A private repo does not say &ldquo;wrong account&rdquo;. It says the thing is not there.',
    nfList: ['the client repo', 'the Supabase project', 'the Base44 app'],
    nfFoot: 'Same resource, seen from the profile nobody chose.',
    foot: 'ego lite 0.4.6 - gal.tidhar.org.il',
  },
  he: {
    dir: 'rtl', arrow: '&larr;', backArrow: '&rarr;',
    eyebrow: '<b class="brandmark">ego lite</b> / זהות של אייג׳נט',
    claim: 'האייג׳נט שלי<br>לא יכול לגלוש בתור אני.',
    claimSub: 'פרופיל ego lite לכל לקוח, מוצהר לפי מייל, ואייג׳נט שנחסם כשהוא מנסה את הלא נכון.',
    oldLabel: 'לפני',
    oldLines: ['המרחב נולד על הפרופיל הפעיל', 'הפרמטר התקבל והתעלמו ממנו', 'עבודה של לקוח, חשבון פרטי'],
    newLabel: 'אחרי / EGO LITE',
    newLines: ['הפרויקט מצהיר מייל אחד', 'המרחב ננעל לפרופיל הזה', 'ריצה בלי סקופ נדחית'],
    quote: 'התקבל, ואז נזרק',
    quoteSub: 'העברתי פרופיל. הפונקציה קיבלה אותו, לא אמרה כלום, וזרקה אותו. שלוש פעמים ביקשתי את הלקוח. שלוש פעמים קיבלתי את עצמי.',
    archYou: 'פרויקט',
    archAgent: 'מרחב משימה',
    archSpace: 'פרופיל הלקוח',
    archNote: 'הפרויקט מצהיר מייל בקובץ. המפה ממייל לפרופיל בונה את עצמה.',
    archBrowser: 'EGO LITE - דפדפן אחד, הרבה זהויות',
    gridTitle: 'ההוק, לפני כל ריצה ב-ego lite',
    grid: [
      ['לפי מייל', 'פרויקט מצהיר על חשבון, לא על "פרופיל 4". המספרים זזים, ולשניים קוראים אותו דבר.'],
      ['ממפה את עצמה', 'פותחת כל פרופיל ובודקת מי מחובר שם. לקוח חדש, אין מה לערוך.'],
      ['ננעל', 'createTaskSpace עם מזהה פרופיל נועל את המרחב, גם כשהדפדפן פעיל על אחר.'],
      ['נדחה', 'פקודה שלא אומרת באיזה סקופ היא עובדת לא מגיעה בכלל לדפדפן.'],
    ],
    bigNum: '1',
    bigNumLabel: 'מייל לכל פרויקט',
    bigNumSub: 'הלקוח פותח לי חשבון פנימי, וכל מה שאני בונה נשאר בתוכו. ego lite היה החור האחרון, ועכשיו הוא סגור.',
    askLabel: 'אתה',
    ask: 'תפתח את github.com/acme/checkout-api',
    replyLabel: 'אייג׳נט',
    reply: '404 - לא נמצא',
    reveal: 'הריפו במקומו. מרחב המשימה נולד על פרופיל אקראי, ולחשבון <b>הזה</b> הריפו פשוט לא קיים.',
    nf: 'לא נמצא',
    nfSub: 'ריפו פרטי לא אומר &rdquo;חשבון לא נכון&ldquo;. הוא אומר שהדבר לא קיים.',
    nfList: ['הריפו של הלקוח', 'הפרויקט בסופהבייס', 'הדשבורד של הלקוח'],
    nfFoot: 'אותו משאב, מהפרופיל שאף אחד לא בחר.',
    foot: 'ego lite 0.4.6 - gal.tidhar.org.il',
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
  .eyebrow{font-size:15px;letter-spacing:.16em;color:#7dd3fc;text-transform:uppercase}
  .brandmark{color:#fef08a;font-weight:600;letter-spacing:.06em;direction:ltr;unicode-bidi:isolate;text-transform:none}
  .foot{position:absolute;bottom:44px;inset-inline-start:74px;font-size:13px;color:rgba(186,230,253,.5);direction:ltr;letter-spacing:.04em}
  .cyan{color:#7dd3fc} .ink{color:#e0f2fe} .amber{color:#fef08a}
  .muted{color:rgba(186,230,253,.55)}
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
  // 3 - the payoff quote (the silently dropped option)
  3: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="q-wrap">
      <div class="q-code">useOrCreateTaskSpace(name, { profileId })</div>
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
      <div class="bar"><span class="hand">${t.arrow}</span></div>
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
  // 7 - the exchange that fails (the pain)
  7: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="ex-wrap">
      <div class="ex-line"><span class="ex-who">${t.askLabel}</span><span class="ex-say">${t.ask}</span></div>
      <div class="ex-line fail"><span class="ex-who">${t.replyLabel}</span><span class="ex-say err">${t.reply}</span></div>
      <div class="ex-reveal">${t.reveal}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 8 - NOT FOUND as the whole image
  8: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="nf-wrap">
      <div class="nf">${t.nf}</div>
      <div class="nf-sub">${t.nfSub}</div>
      <div class="nf-list">${t.nfList.map(l => `<span>${l}</span>`).join('')}</div>
      <div class="nf-foot">${t.nfFoot}</div>
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
    .li{font-size:21px;line-height:1.6;margin-bottom:14px;padding-inline-start:26px;position:relative;color:#bae6fd}
    .li::before{position:absolute;inset-inline-start:0}
    .li.x::before{content:'x';color:#f87171}
    .li.ok::before{content:'+';color:#7dd3fc}
    .col.new .li{color:#e0f2fe}
    .mid{font-size:40px;color:#fef08a}
  `,
  2: `
    .claim-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .claim{font-size:62px;line-height:1.22;font-weight:600;color:#e0f2fe;letter-spacing:.01em}
    .claim-sub{margin-top:30px;font-size:23px;color:#7dd3fc;line-height:1.6;max-width:24em}
  `,
  3: `
    .q-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;padding-bottom:30px}
    .q-code{direction:ltr;unicode-bidi:isolate;display:inline-block;font-size:24px;color:rgba(186,230,253,.65);margin-bottom:26px}
    .q-bar{border-inline-start:4px solid #f87171;padding-inline-start:24px}
    .q-term{font-size:52px;color:#f87171;letter-spacing:.01em}
    .q-sub{margin-top:30px;font-size:23px;color:#e0f2fe;line-height:1.65;max-width:26em}
  `,
  4: `
    .arch-title{margin-top:22px;font-size:18px;letter-spacing:.18em;color:rgba(186,230,253,.55);text-transform:uppercase}
    .arch{flex:1;display:flex;align-items:center;gap:20px;margin-top:-10px}
    .node{flex:1;border:1px solid #7dd3fc;padding:34px 26px;font-size:32px;color:#e0f2fe;text-align:center;background:rgba(125,211,252,.06)}
    .node.agent{border-color:#fef08a;background:rgba(254,240,138,.06)}
    .space{margin-top:14px;font-size:17px;color:#fef08a;letter-spacing:.1em}
    .bar{display:flex;flex-direction:column;gap:12px;font-size:34px;color:#7dd3fc}
    .arch-note{font-size:19px;color:rgba(186,230,253,.6);margin-bottom:34px;line-height:1.5;max-width:34em}
  `,
  5: `
    .grid-title{margin-top:18px;font-size:32px;color:#e0f2fe}
    .grid{flex:1;display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:22px 0 40px}
    .cell{border:1px solid rgba(125,211,252,.3);padding:18px 20px;background:rgba(15,40,71,.5)}
    .cell-h{font-size:15px;letter-spacing:.12em;color:#fef08a;text-transform:uppercase;margin-bottom:10px}
    .cell-b{font-size:17px;line-height:1.55;color:#bae6fd}
  `,
  7: `
    .ex-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;gap:20px;padding-bottom:34px}
    .ex-line{display:flex;align-items:baseline;gap:20px}
    .ex-who{font-size:14px;letter-spacing:.14em;color:rgba(186,230,253,.5);min-width:5.5em;text-transform:uppercase}
    .ex-say{font-size:34px;color:#e0f2fe;direction:ltr;unicode-bidi:isolate}
    .ex-say.err{color:#f87171;font-size:52px;font-weight:600;letter-spacing:.01em}
    .ex-reveal{margin-top:16px;border-inline-start:4px solid #7dd3fc;padding-inline-start:22px;
      font-size:24px;line-height:1.6;color:#bae6fd;max-width:30em}
    .ex-reveal b{color:#fef08a}
  `,
  8: `
    .nf-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:30px}
    .nf{font-size:118px;line-height:1;color:#f87171;font-weight:600;letter-spacing:.02em}
    .nf-sub{margin-top:24px;font-size:26px;color:#e0f2fe;line-height:1.55;max-width:26em}
    .nf-list{margin-top:26px;display:flex;flex-wrap:wrap;gap:12px}
    .nf-list span{border:1px solid rgba(248,113,113,.5);padding:8px 16px;font-size:19px;color:#bae6fd}
    .nf-foot{margin-top:24px;font-size:20px;color:#7dd3fc}
  `,
  6: `
    .num-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .num{font-size:180px;line-height:.9;color:#fef08a;font-weight:600}
    .num-label{margin-top:14px;font-size:42px;color:#e0f2fe}
    .num-sub{margin-top:26px;font-size:22px;color:#7dd3fc;line-height:1.6;max-width:27em}
  `,
}

for (const n of Object.keys(designs)) {
  for (const lang of ['en', 'he']) {
    fs.writeFileSync(path.join(OUT, `hero-${n}-${lang}.html`), page(lang, designs[n](S[lang]), CSS[n]))
  }
}
console.log('wrote 12 html files')
