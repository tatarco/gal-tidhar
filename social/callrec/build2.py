#!/usr/bin/env python3
"""Icon variants of design 2 (his pick), per Gal: visual cues over text.

2b - the claim, with a red REC dot above it and the platform icons -> Claude below.
2c - icon-forward: the row IS the message, the sentence shrinks to one line.

Icon paths are simple-icons (CC0), inlined so the PNG needs no network.
Run: python3 build2.py && ./shoot.sh
"""
import pathlib, re

HERE = pathlib.Path(__file__).parent
SI = pathlib.Path("/private/tmp/claude-501/-Users-galtidhar-PycharmProjects-unicargo"
                  "/d56bf923-7bec-4fd5-9572-d9b2de2d5818/scratchpad")


def icon(name, color, size=64):
    d = re.search(r'<path d="([^"]+)"', (SI / f"si-{name}.svg").read_text()).group(1)
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="{color}">'
            f'<path d="{d}"/></svg>')


ZOOM = icon("zoom", "#4A8CFF")
MEET = icon("googlemeet", "#00AC47")
WA = icon("whatsapp", "#25D366")
CLAUDE = icon("claude", "#D97757", 72)

# a phone on speaker, drawn rather than branded - there is no logo for "a phone on a table"
PHONE = ('<svg viewBox="0 0 24 24" width="64" height="64" fill="none" stroke="#7dd3fc" '
         'stroke-width="1.6"><rect x="6" y="2" width="12" height="20" rx="2.5"/>'
         '<path d="M9.2 18.4h5.6"/><path d="M3.2 9.5c0 0 -.9 2.5 0 5"/>'
         '<path d="M20.8 9.5c0 0 .9 2.5 0 5"/></svg>')

REC = ('<div class="rec"><span class="ring"></span><span class="dot"></span></div>')

S = {
    "en": {
        "dir": "ltr", "arrow": "&rarr;",
        "top": "callrec &middot; local call recording",
        "claim": "Every call - Zoom, Meet, WhatsApp, a phone on speaker - recorded, transcribed on "
                 "this Mac, and <b>handed straight to Claude</b> as the client's own words.",
        "short": "Any call. Any platform.<br><b>Straight into Claude.</b>",
        "sub": "Recorded and transcribed on this Mac. No bot in the call, nothing monthly, "
               "not a byte uploaded.",
        "recording": "REC",
        "foot": "350 lines, open source &middot; gal.tidhar.org.il",
    },
    "he": {
        "dir": "rtl", "arrow": "&larr;",
        "top": '<span class="num">callrec</span> &middot; הקלטת שיחות מקומית',
        "claim": "כל שיחה - זום, מיט, וואטסאפ, טלפון על רמקול - מוקלטת, מתומללת על המק הזה, "
                 "ונכנסת <b>ישר לקלוד</b> במילים של הלקוח עצמו.",
        "short": "כל שיחה. כל פלטפורמה.<br><b>ישר לקלוד.</b>",
        "sub": "מוקלטת ומתומללת על המק הזה. בלי בוט בשיחה, בלי תשלום חודשי, בלי בייט אחד שעולה לענן.",
        "recording": "REC",
        "foot": '<span class="num">350</span> שורות, קוד פתוח &middot; <span class="num">gal.tidhar.org.il</span>',
    },
}

CSS = """
.rec{display:flex;align-items:center;gap:16px;margin-bottom:30px}
.rec .dot{width:34px;height:34px;border-radius:50%;background:#ef4444;
  box-shadow:0 0 34px rgba(239,68,68,.85),0 0 90px rgba(239,68,68,.45)}
.rec .ring{position:absolute;width:62px;height:62px;border-radius:50%;
  border:2px solid rgba(239,68,68,.35);margin-inline-start:-14px}
.reclab{font-size:22px;letter-spacing:.32em;color:#ef4444;font-weight:700;direction:ltr}
.flow{display:flex;align-items:center;gap:26px;margin-top:38px}
.apps{display:flex;align-items:center;gap:22px;border:1px solid rgba(125,211,252,.35);
  padding:18px 26px}
.arw{font-size:44px;color:rgba(186,230,253,.55)}
.dest{display:flex;align-items:center;gap:16px;border:2px solid rgba(217,119,87,.75);
  padding:16px 28px;background:rgba(217,119,87,.08)}
.dest .lab{font-size:30px;font-weight:800;color:#e0f2fe;direction:ltr}
.short{font-size:64px;font-weight:800;color:#e0f2fe;line-height:1.28;max-width:1060px}
.short b{color:#fef08a}
.subline{font-size:26px;color:rgba(186,230,253,.72);margin-top:26px;max-width:900px;line-height:1.45}
svg{display:block}
"""

BASE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#0a1628;color:#bae6fd;direction:%(dir)s;
  font-family:'IBM Plex Mono','Arial Hebrew','Arial Unicode MS',system-ui,monospace;
  background-image:linear-gradient(rgba(125,211,252,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(125,211,252,.06) 1px,transparent 1px);
  background-size:40px 40px;display:flex;flex-direction:column;justify-content:center;align-items:center;
  text-align:center;padding:52px;position:relative}
.top{position:absolute;top:36px;inset-inline-end:56px;font-size:19px;color:#7dd3fc;font-weight:700}
.rv{position:absolute;top:38px;inset-inline-start:56px;font-size:14px;letter-spacing:.14em;
  color:rgba(186,230,253,.45)}
.rv span{direction:ltr;unicode-bidi:isolate}
.num{direction:ltr;unicode-bidi:isolate;display:inline-block}
.claim{font-size:48px;font-weight:800;color:#e0f2fe;line-height:1.34;max-width:1040px}
.claim b{color:#fef08a}
.foot{position:absolute;bottom:34px;font-size:20px;color:rgba(186,230,253,.6)}
%(css)s
</style></head><body>
<div class="top">%(top)s</div><div class="rv"><span>gal.tidhar.org.il</span></div>
%(body)s
<div class="foot">%(foot)s</div>
</body></html>"""


def flow(s):
    return (f'<div class="flow">'
            f'<div class="apps">{ZOOM}{MEET}{WA}{PHONE}</div>'
            f'<div class="arw">{s["arrow"]}</div>'
            f'<div class="dest">{CLAUDE}<span class="lab">Claude</span></div>'
            f'</div>')


for lang, s in S.items():
    rec = f'{REC}<span class="reclab">{s["recording"]}</span>'
    rec_row = f'<div class="rec">{REC}<span class="reclab">{s["recording"]}</span></div>'

    b = (f'<div class="rec"><span class="dot"></span>'
         f'<span class="reclab">{s["recording"]}</span></div>'
         f'<div class="claim">{s["claim"]}</div>{flow(s)}')
    (HERE / f"hero-2b-{lang}.html").write_text(
        BASE % {"dir": s["dir"], "css": CSS, "top": s["top"], "body": b, "foot": s["foot"]},
        encoding="utf-8")

    c = (f'<div class="rec"><span class="dot"></span>'
         f'<span class="reclab">{s["recording"]}</span></div>'
         f'<div class="short">{s["short"]}</div>{flow(s)}'
         f'<div class="subline">{s["sub"]}</div>')
    (HERE / f"hero-2c-{lang}.html").write_text(
        BASE % {"dir": s["dir"], "css": CSS, "top": s["top"], "body": c, "foot": s["foot"]},
        encoding="utf-8")

print("wrote 4 html files")
