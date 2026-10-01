// Generates 6 hero designs x 2 languages = 12 HTML files, driven by ONE strings table.
// Angle: starting Claude Code on your Mac from your phone is great - if you keep a terminal open
// and it does not die first. launchd removes both catches.
const fs = require('fs')
const path = require('path')
const OUT = __dirname

const S = {
  en: {
    dir: 'ltr', arrow: '&rarr;',
    eyebrow: 'FIELD NOTE / CLAUDE CODE',
    // 1 - phone mockup
    phoneApp: 'Claude Code',
    phoneEnv: 'MacBook · Projects',
    phoneOnline: 'online',
    phoneBtn: '+ New session',
    phoneRun: 'refactor the export script',
    phoneRunState: 'running on the Mac',
    phoneClaim: 'I start Claude Code<br>on my Mac<br><span class="amber">from my phone.</span>',
    phoneSub: 'No terminal left open. When it dies, it comes back.',
    // 2 - claim
    claim: 'Claude Code on my Mac.<br>Started from my phone.<br><span class="amber">Always online.</span>',
    claimSub: 'No terminal window to babysit. When claude rc dies, launchd brings it back.',
    // 3 - the window you could never close
    termTitle: 'claude rc - the window you could never close',
    termLines: ['<span class="g">✔ Connected</span> · PycharmProjects', 'Reconnected after 2s', 'Reconnected after 1s', 'Reconnected after 14s', '<span class="r">Error: Persistent errors for 10 minutes, giving up.</span>'],
    termNote: 'Now it runs in the background, and never stays dead.',
    // 4 - flow
    flowPhone: 'PHONE',
    flowPhoneSub: 'tap New session',
    flowMac: 'MAC',
    flowMacSub: 'a real session, your files',
    flowKeeper: 'launchd keeps claude rc alive - no terminal, restarts on its own',
    // 5 - exchange
    oldLabel: 'claude rc, the default',
    oldLines: ['a terminal you can never close', 'quits after 10 min of errors', 'you find out from the phone'],
    newLabel: 'claude rc + launchd',
    newLines: ['no window at all', 'restarts itself in under a minute', 'there when you reach for the phone'],
    // 6 - big number
    bigNum: '24/7',
    bigNumLabel: 'Claude Code on my Mac, one tap from my phone',
    bigNumSub: 'No terminal to keep open. Nothing to restart by hand.',
    foot: 'Claude Code - claude rc + launchd - gal.tidhar.org.il',
  },
  he: {
    dir: 'rtl', arrow: '&larr;',
    eyebrow: 'הערת שטח / קלוד קוד',
    phoneApp: 'קלוד קוד',
    phoneEnv: 'המק · פרויקטים',
    phoneOnline: 'מחובר',
    phoneBtn: '+ סשן חדש',
    phoneRun: 'לסדר את סקריפט הייצוא',
    phoneRunState: 'רץ על המק',
    phoneClaim: 'אני פותח קלוד קוד<br>על המק<br><span class="amber">מהנייד.</span>',
    phoneSub: 'בלי טרמינל פתוח. וכשהוא מת, הוא קם לבד.',
    claim: 'קלוד קוד על המק.<br>נפתח מהנייד.<br><span class="amber">תמיד אונליין.</span>',
    claimSub: 'בלי חלון טרמינל לשמור עליו. כש-<span class="cmd">claude rc</span> מת, המק מרים אותו מחדש.',
    termTitle: 'claude rc - החלון שאסור היה לסגור',
    termLines: ['<span class="g">✔ Connected</span> · PycharmProjects', 'Reconnected after 2s', 'Reconnected after 1s', 'Reconnected after 14s', '<span class="r">Error: Persistent errors for 10 minutes, giving up.</span>'],
    termNote: 'עכשיו הוא רץ ברקע, ולא נשאר מת.',
    flowPhone: 'נייד',
    flowPhoneSub: 'לוחצים סשן חדש',
    flowMac: 'מק',
    flowMacSub: 'סשן אמיתי, הקבצים שלך',
    flowKeeper: 'launchd שומר על <span class="cmd">claude rc</span> חי - בלי טרמינל, קם לבד',
    oldLabel: 'ברירת המחדל',
    oldLines: ['טרמינל שאסור לסגור לעולם', 'נסגר אחרי 10 דקות של שגיאות', 'מגלים את זה מהנייד'],
    newLabel: 'עם launchd',
    newLines: ['אין שום חלון', 'קם לבד תוך פחות מדקה', 'מחכה כשמוציאים את הנייד'],
    bigNum: '24/7',
    bigNumLabel: 'קלוד קוד על המק, לחיצה אחת מהנייד',
    bigNumSub: 'אין טרמינל לשמור פתוח. אין מה להרים ביד.',
    foot: 'Claude Code - claude rc + launchd - gal.tidhar.org.il',
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
  .amber{color:#fef08a}
  .cmd{direction:ltr;unicode-bidi:isolate;display:inline-block}
  .g{color:#86efac} .r{color:#f87171}
`

const page = (lang, body, extra = '') => `<!doctype html><html lang="${lang}" dir="${S[lang].dir}"><head><meta charset="utf-8"><style>${BASE}${extra}</style></head><body>${body}</body></html>`

const designs = {
  // 1 - the phone itself
  1: (t) => `<div class="frame row">
    <div class="phone">
      <div class="notch"></div>
      <div class="app">${t.phoneApp}</div>
      <div class="env"><span>${t.phoneEnv}</span><span class="on"><i></i>${t.phoneOnline}</span></div>
      <div class="btn">${t.phoneBtn}</div>
      <div class="run"><div class="run-t">${t.phoneRun}</div><div class="run-s"><i></i>${t.phoneRunState}</div></div>
      <div class="run dim"></div>
    </div>
    <div class="side">
      <div class="eyebrow">${t.eyebrow}</div>
      <div class="pclaim">${t.phoneClaim}</div>
      <div class="psub">${t.phoneSub}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 2 - the claim
  2: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="claim-wrap"><div class="claim">${t.claim}</div><div class="claim-sub">${t.claimSub}</div></div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 3 - the terminal you could never close
  3: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="term">
      <div class="bar"><span class="tl r1"></span><span class="tl r2"></span><span class="tl r3"></span><span class="tt">${t.termTitle}</span></div>
      <div class="body">${t.termLines.map(l => `<div>${l}</div>`).join('')}</div>
    </div>
    <div class="tnote">${t.termNote}</div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 4 - phone to mac flow
  4: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="flow">
      <div class="node"><div class="nh">${t.flowPhone}</div><div class="ns">${t.flowPhoneSub}</div></div>
      <div class="arr">${t.arrow}</div>
      <div class="node mac"><div class="nh">${t.flowMac}</div><div class="ns">${t.flowMacSub}</div></div>
    </div>
    <div class="keeper">${t.flowKeeper}</div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 5 - the exchange
  5: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="cols">
      <div class="col"><div class="col-label">${t.oldLabel}</div>${t.oldLines.map(l => `<div class="li x">${l}</div>`).join('')}</div>
      <div class="mid">${t.arrow}</div>
      <div class="col new"><div class="col-label nl">${t.newLabel}</div>${t.newLines.map(l => `<div class="li ok">${l}</div>`).join('')}</div>
    </div>
    <div class="foot">${t.foot}</div>
  </div>`,
  // 6 - the one big number
  6: (t) => `<div class="frame">
    <div class="eyebrow">${t.eyebrow}</div>
    <div class="num-wrap"><div class="num">${t.bigNum}</div><div class="num-label">${t.bigNumLabel}</div><div class="num-sub">${t.bigNumSub}</div></div>
    <div class="foot">${t.foot}</div>
  </div>`,
}

const CSS = {
  1: `
    .frame.row{flex-direction:row;align-items:center;gap:56px;padding:30px 56px}
    .phone{flex:none;width:270px;height:500px;border:3px solid #7dd3fc;border-radius:38px;background:#0f2847;padding:40px 18px 18px;position:relative;box-shadow:0 0 60px rgba(125,211,252,.18)}
    .notch{position:absolute;top:12px;left:50%;transform:translateX(-50%);width:84px;height:18px;border-radius:10px;background:#0a1628}
    .app{font-size:20px;color:#e0f2fe;font-weight:600;margin-bottom:16px}
    .env{display:flex;justify-content:space-between;align-items:center;border:1px solid rgba(125,211,252,.35);padding:12px;font-size:14px;color:#bae6fd;border-radius:10px}
    .on{color:#86efac;display:flex;align-items:center;gap:6px}
    .on i,.run-s i{width:9px;height:9px;border-radius:50%;background:#86efac;display:inline-block;box-shadow:0 0 10px #86efac}
    .btn{margin:16px 0;background:#fef08a;color:#0a1628;text-align:center;padding:14px;font-size:18px;font-weight:600;border-radius:10px}
    .run{border:1px solid rgba(125,211,252,.25);padding:12px;border-radius:10px;margin-bottom:10px;min-height:66px}
    .run-t{font-size:15px;color:#e0f2fe}
    .run-s{margin-top:6px;font-size:13px;color:#86efac;display:flex;align-items:center;gap:6px}
    .run.dim{opacity:.35}
    .side{flex:1;display:flex;flex-direction:column;gap:26px;padding-bottom:30px}
    .pclaim{font-size:58px;line-height:1.18;font-weight:600;color:#e0f2fe}
    .psub{font-size:24px;color:#7dd3fc;line-height:1.5}
    [dir=ltr] .foot{left:auto;right:84px}
  `,
  2: `
    .claim-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .claim{font-size:64px;line-height:1.2;font-weight:600;color:#e0f2fe}
    .claim-sub{margin-top:28px;font-size:24px;color:#7dd3fc;line-height:1.6;max-width:24em}
  `,
  3: `
    .term{margin-top:26px;border:1px solid rgba(125,211,252,.4);border-radius:10px;background:#1e2030;direction:ltr;overflow:hidden}
    .bar{display:flex;align-items:center;gap:8px;padding:12px 16px;background:#2a2d40}
    .tl{width:13px;height:13px;border-radius:50%}
    .r1{background:#ff5f57} .r2{background:#febc2e} .r3{background:#28c840}
    .tt{margin-left:14px;font-size:15px;color:#cbd5e1;unicode-bidi:plaintext}
    .body{padding:18px 22px;font-size:21px;line-height:1.75;color:#cbd5e1}
    .tnote{margin-top:26px;font-size:34px;color:#fef08a;font-weight:600}
  `,
  4: `
    .flow{flex:1;display:flex;align-items:center;gap:30px}
    .node{flex:1;border:1px solid #7dd3fc;padding:40px 26px;text-align:center;background:rgba(125,211,252,.06)}
    .node.mac{border-color:#fef08a;background:rgba(254,240,138,.06)}
    .nh{font-size:44px;color:#e0f2fe;font-weight:600}
    .ns{margin-top:12px;font-size:20px;color:#7dd3fc}
    .node.mac .ns{color:#fef08a}
    .arr{font-size:60px;color:#fef08a}
    .keeper{border-top:1px dashed rgba(125,211,252,.45);padding-top:18px;font-size:21px;color:#e0f2fe;margin-bottom:40px}
  `,
  5: `
    .cols{flex:1;display:flex;align-items:center;gap:26px;margin-top:8px;padding-bottom:30px}
    .col{flex:1;border:1px solid rgba(125,211,252,.28);padding:26px 24px;min-height:290px}
    .col.new{border-color:#7dd3fc;background:rgba(125,211,252,.06)}
    .col-label{font-size:17px;letter-spacing:.06em;color:rgba(186,230,253,.6);margin-bottom:22px}
    .nl{color:#fef08a}
    .li{font-size:23px;line-height:1.5;margin-bottom:16px;padding-inline-start:28px;position:relative;color:#bae6fd}
    .li::before{position:absolute;inset-inline-start:0}
    .li.x::before{content:'x';color:#f87171}
    .li.ok::before{content:'+';color:#7dd3fc}
    .col.new .li{color:#e0f2fe}
    .mid{font-size:42px;color:#fef08a}
  `,
  6: `
    .num-wrap{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
    .num{font-size:190px;line-height:.9;color:#fef08a;font-weight:600;direction:ltr;unicode-bidi:isolate;align-self:flex-start}
    .num-label{margin-top:22px;font-size:40px;color:#e0f2fe}
    .num-sub{margin-top:20px;font-size:24px;color:#7dd3fc}
  `,
}

for (const n of Object.keys(designs)) {
  for (const lang of ['en', 'he']) {
    fs.writeFileSync(path.join(OUT, `hero-${n}-${lang}.html`), page(lang, designs[n](S[lang]), CSS[n]))
  }
}
console.log('wrote 12 html files')
