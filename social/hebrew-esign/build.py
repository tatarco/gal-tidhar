#!/usr/bin/env python3
"""Render 6 hero designs x EN/HE for the hebrew-esign post (free Hebrew e-signature, Tofes 101)."""
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))

# ponytail: every Latin run inside Hebrew text is isolated with .ltr (direction + isolate),
# learned across four bidi incidents in this repo's earlier heroes.
LTR = '<span class="ltr">{}</span>'

S = {
 'en': {
   'dir':'ltr','lang':'en',
   'eyebrow':'FIELD NOTE / HEBREW E-SIGNATURE',
   'big':'173 fields',
   'big_unit':'on Israel\u2019s most hated form. I placed zero of them by hand.',
   'big_sub':'Deterministic code reads the PDF\u2019s own text layer and anchors<br>'
             'every field to a printed label. Then it renders the page with the<br>'
             'boxes drawn on, and <span class="cy">the agent just looks and says what moved</span>.<br>'
             '<span class="hi">Final seal accuracy: 0.14% off.</span>',
   'claim':'I built a free e-signature<br>that speaks Hebrew -<br>'
           '<span class="hi">and ran it on Tofes 101.</span>',
   'claim_foot':'A fork of Documenso, open source, on a small VPS I already had. Software cost: zero. The documents never leave my server. Click the demo and you get your own private 101.',
   'before_l':'EVERY E-SIGN TOOL',
   'before_v':'drag a box<br>onto the PDF<br><span class="sm">put it roughly there, hope</span>',
   'after_l':'FORM MODE',
   'after_v':'a labeled Hebrew form<br>+ the document live<br><span class="sm">the value lands on the page as you type</span>',
   'grid_title':'WHAT I TRIED, AND WHAT STOPPED IT',
   'grid': [('DocuSign','costs money per envelope'),
            ('FillFaster','a client\u2019s project, not mine to use'),
            ('DocuSeal','the API I needed is behind the paid tier'),
            ('Documenso','open source - but Hebrew sealed as empty squares')],
   'grid_foot':'So I forked it, and fixed the Hebrew.',
   'quote':'\u25a1\u25a1\u25a1\u25a1 \u25a1\u25a1\u25a1\u25a1',
   'quote_sub':'That is what my signed PDF looked like. The sealing engine<br>'
               'did not carry a single Hebrew font. Every open-source e-sign<br>'
               'stack I tried had the same hole - so I fixed it and I am<br>'
               'sending the RTL work back upstream. It unlocks Arabic too.',
   'arch':[('THE CODE MEASURES','reads the PDF text<br>layer, anchors each<br>field to a printed<br>label or a checkbox'),
           ('THE AGENT LOOKS','at a render of the<br>page with the boxes<br>drawn on, and says<br>which ones moved'),
           ('0.14% OFF','173 fields placed,<br>none of them<br>by hand')],
   'arch_foot':'Do not ask a model for coordinates. Ask code to measure, and the model to look.',
   'claim8':'I built an e-signature<br>that speaks Hebrew.',
   'pillars':['OPEN SOURCE','ON MY OWN SERVER','FREE'],
   'fix_before':'WHAT IT SEALED',
   'fix_after':'WHAT IT SEALS NOW',
   'fix_arrow':'\u2192',
   'claim8_foot':'The sealing engine carried no Hebrew font, so every signed name came out as empty boxes. Fixed - then proven on Tofes 101, all 173 fields.',
   'foot':'sign.zazet-solutions.hr/try101',
 },
 'he': {
   'dir':'rtl','lang':'he',
   'eyebrow':'',
   'big':'173 \u05e9\u05d3\u05d5\u05ea',
   'big_unit':'\u05d1\u05d8\u05d5\u05e4\u05e1 \u05d4\u05db\u05d9 \u05e9\u05e0\u05d5\u05d0 \u05d1\u05d9\u05e9\u05e8\u05d0\u05dc. \u05de\u05d9\u05e7\u05de\u05ea\u05d9 \u05d0\u05e4\u05e1 \u05de\u05d4\u05dd \u05d1\u05d9\u05d3.',
   'big_sub':'\u05e7\u05d5\u05d3 \u05d3\u05d8\u05e8\u05de\u05d9\u05e0\u05d9\u05e1\u05d8\u05d9 \u05e7\u05d5\u05e8\u05d0 \u05d0\u05ea \u05e9\u05db\u05d1\u05ea \u05d4\u05d8\u05e7\u05e1\u05d8 \u05e9\u05dc \u05d4-PDF \u05e2\u05e6\u05de\u05d5<br>'
             '\u05d5\u05de\u05e2\u05d2\u05df \u05db\u05dc \u05e9\u05d3\u05d4 \u05dc\u05ea\u05d5\u05d5\u05d9\u05ea \u05de\u05d5\u05d3\u05e4\u05e1\u05ea. \u05d0\u05d7\u05e8 \u05db\u05da \u05d4\u05d5\u05d0 \u05de\u05e6\u05d9\u05d9\u05e8 \u05d0\u05ea<br>'
             '\u05d4\u05e9\u05d3\u05d5\u05ea \u05e2\u05dc \u05d4\u05e2\u05de\u05d5\u05d3, <span class="cy">\u05d5\u05d4\u05d0\u05d9\u05d9\u05d2\u05f3\u05e0\u05d8 \u05e8\u05e7 \u05de\u05e1\u05ea\u05db\u05dc \u05d5\u05d0\u05d5\u05de\u05e8 \u05de\u05d4 \u05d6\u05d6</span>.<br>'
             '<span class="hi">\u05e1\u05d8\u05d9\u05d9\u05d4 \u05e1\u05d5\u05e4\u05d9\u05ea: 0.14%.</span>',
   'claim':'\u05d1\u05e0\u05d9\u05ea\u05d9 \u05d7\u05ea\u05d9\u05de\u05d4 \u05d3\u05d9\u05d2\u05d9\u05d8\u05dc\u05d9\u05ea \u05d7\u05d9\u05e0\u05de\u05d9\u05ea<br>\u05e9\u05de\u05d3\u05d1\u05e8\u05ea \u05e2\u05d1\u05e8\u05d9\u05ea -<br>'
           '<span class="hi">\u05d5\u05d4\u05e8\u05e6\u05ea\u05d9 \u05d0\u05d5\u05ea\u05d4 \u05e2\u05dc \u05d8\u05d5\u05e4\u05e1 101.</span>',
   'claim_foot':'\u05e4\u05d5\u05e8\u05e7 \u05e9\u05dc ' + LTR.format('Documenso') + ', \u05e7\u05d5\u05d3 \u05e4\u05ea\u05d5\u05d7, \u05e2\u05dc ' + LTR.format('VPS') + ' \u05e7\u05d8\u05df \u05e9\u05db\u05d1\u05e8 \u05d4\u05d9\u05d4 \u05dc\u05d9. \u05e2\u05dc\u05d5\u05ea \u05d4\u05ea\u05d5\u05db\u05e0\u05d4: \u05d0\u05e4\u05e1. \u05d4\u05de\u05e1\u05de\u05db\u05d9\u05dd \u05dc\u05d0 \u05e2\u05d5\u05d6\u05d1\u05d9\u05dd \u05d0\u05ea \u05d4\u05e9\u05e8\u05ea \u05e9\u05dc\u05d9.',
   'before_l':'\u05db\u05dc \u05db\u05dc\u05d9 \u05d7\u05ea\u05d9\u05de\u05d4<br>\u05d1\u05e2\u05d5\u05dc\u05dd',
   'before_v':'\u05d2\u05d5\u05e8\u05e8 \u05e8\u05d9\u05d1\u05d5\u05e2<br>\u05e2\u05dc \u05d4-PDF<br><span class="sm">\u05e9\u05d9\u05dd \u05d0\u05d5\u05ea\u05d5 \u05d1\u05e2\u05e8\u05da \u05e9\u05dd, \u05ea\u05e7\u05d5\u05d5\u05d4</span>',
   'after_l':'\u05de\u05e6\u05d1 \u05d8\u05d5\u05e4\u05e1',
   'after_v':'\u05d8\u05d5\u05e4\u05e1 \u05e2\u05d1\u05e8\u05d9 \u05de\u05ea\u05d5\u05d9\u05d2<br>\u05d5\u05d4\u05de\u05e1\u05de\u05da \u05d7\u05d9 \u05dc\u05d9\u05d3\u05d5<br><span class="sm">\u05de\u05d4 \u05e9\u05d4\u05e7\u05dc\u05d3\u05ea \u05e0\u05d5\u05d7\u05ea \u05e2\u05dc \u05d4\u05d3\u05e3 \u05ea\u05d5\u05da \u05db\u05d3\u05d9 \u05db\u05ea\u05d9\u05d1\u05d4</span>',
   'grid_title':'\u05de\u05d4 \u05e0\u05d9\u05e1\u05d9\u05ea\u05d9, \u05d5\u05de\u05d4 \u05e2\u05e6\u05e8 \u05d0\u05ea \u05d6\u05d4',
   'grid': [(LTR.format('DocuSign'),'\u05e2\u05d5\u05dc\u05d4 \u05db\u05e1\u05e3 \u05dc\u05db\u05dc \u05de\u05e2\u05d8\u05e4\u05d4'),
            (LTR.format('FillFaster'),'\u05e4\u05e8\u05d5\u05d9\u05e7\u05d8 \u05e9\u05dc \u05dc\u05e7\u05d5\u05d7 \u05e9\u05dc\u05d9, \u05dc\u05d0 \u05e9\u05dc\u05d9 \u05dc\u05d4\u05e9\u05ea\u05de\u05e9 \u05d1\u05d5'),
            (LTR.format('DocuSeal'),'\u05d4-API \u05e9\u05e6\u05e8\u05d9\u05db\u05ea\u05d9 \u05d9\u05d5\u05e9\u05d1 \u05d1\u05d2\u05e8\u05e1\u05d4 \u05d1\u05ea\u05e9\u05dc\u05d5\u05dd'),
            (LTR.format('Documenso'),'\u05e7\u05d5\u05d3 \u05e4\u05ea\u05d5\u05d7 - \u05d0\u05d1\u05dc \u05e2\u05d1\u05e8\u05d9\u05ea \u05e0\u05e6\u05e8\u05d1\u05d4 \u05db\u05e8\u05d9\u05d1\u05d5\u05e2\u05d9\u05dd \u05e8\u05d9\u05e7\u05d9\u05dd')],
   'grid_foot':'\u05d0\u05d6 \u05e2\u05e9\u05d9\u05ea\u05d9 \u05e4\u05d5\u05e8\u05e7, \u05d5\u05ea\u05d9\u05e7\u05e0\u05ea\u05d9 \u05d0\u05ea \u05d4\u05e2\u05d1\u05e8\u05d9\u05ea.',
   'quote':'\u25a1\u25a1\u25a1\u25a1 \u25a1\u25a1\u25a1\u25a1',
   'quote_sub':'\u05db\u05da \u05e0\u05e8\u05d0\u05d4 \u05d4-PDF \u05d4\u05d7\u05ea\u05d5\u05dd \u05e9\u05dc\u05d9. \u05de\u05e0\u05d5\u05e2 \u05d4\u05d7\u05ea\u05d9\u05de\u05d4 \u05dc\u05d0 \u05d4\u05db\u05d9\u05e8<br>'
               '\u05d0\u05e3 \u05d2\u05d5\u05e4\u05df \u05e2\u05d1\u05e8\u05d9. \u05ea\u05d9\u05e7\u05e0\u05ea\u05d9, \u05d5\u05d4\u05e2\u05d1\u05d5\u05d3\u05d4 \u05e2\u05dc \u05d4-RTL \u05d7\u05d5\u05d6\u05e8\u05ea<br>'
               '\u05d0\u05e4\u05e1\u05d8\u05e8\u05d9\u05dd. \u05d6\u05d4 \u05e4\u05d5\u05ea\u05d7 \u05d2\u05dd \u05e2\u05e8\u05d1\u05d9\u05ea.',
   'arch':[('\u05d4\u05e7\u05d5\u05d3 \u05de\u05d5\u05d3\u05d3','\u05e7\u05d5\u05e8\u05d0 \u05d0\u05ea \u05e9\u05db\u05d1\u05ea<br>\u05d4\u05d8\u05e7\u05e1\u05d8 \u05e9\u05dc \u05d4-PDF<br>\u05d5\u05de\u05e2\u05d2\u05df \u05db\u05dc \u05e9\u05d3\u05d4<br>\u05dc\u05ea\u05d5\u05d5\u05d9\u05ea \u05de\u05d5\u05d3\u05e4\u05e1\u05ea'),
           ('\u05d4\u05d0\u05d9\u05d9\u05d2\u05f3\u05e0\u05d8 \u05de\u05e1\u05ea\u05db\u05dc','\u05e2\u05dc \u05e8\u05e0\u05d3\u05d5\u05e8 \u05e9\u05dc \u05d4\u05e2\u05de\u05d5\u05d3<br>\u05e2\u05dd \u05d4\u05e9\u05d3\u05d5\u05ea \u05de\u05e6\u05d5\u05d9\u05e8\u05d9\u05dd,<br>\u05d5\u05d0\u05d5\u05de\u05e8 \u05de\u05d4 \u05d6\u05d6<br>\u05d5\u05dc\u05d0\u05df'),
           ('0.14% \u05e1\u05d8\u05d9\u05d9\u05d4','173 \u05e9\u05d3\u05d5\u05ea \u05de\u05de\u05d5\u05e7\u05de\u05d9\u05dd,<br>\u05d0\u05e3 \u05d0\u05d7\u05d3 \u05de\u05d4\u05dd<br>\u05dc\u05d0 \u05d1\u05d9\u05d3')],
   'arch_foot':'\u05d0\u05dc \u05ea\u05d1\u05e7\u05e9\u05d5 \u05de\u05de\u05d5\u05d3\u05dc \u05e7\u05d5\u05d0\u05d5\u05e8\u05d3\u05d9\u05e0\u05d8\u05d5\u05ea. \u05ea\u05e0\u05d5 \u05dc\u05e7\u05d5\u05d3 \u05dc\u05de\u05d3\u05d5\u05d3, \u05d5\u05dc\u05de\u05d5\u05d3\u05dc \u05dc\u05d4\u05e1\u05ea\u05db\u05dc.',
   'claim8':'\u05d1\u05e0\u05d9\u05ea\u05d9 \u05d7\u05ea\u05d9\u05de\u05d4 \u05d3\u05d9\u05d2\u05d9\u05d8\u05dc\u05d9\u05ea<br>\u05e9\u05de\u05d3\u05d1\u05e8\u05ea \u05e2\u05d1\u05e8\u05d9\u05ea.',
   'pillars':['\u05e7\u05d5\u05d3 \u05e4\u05ea\u05d5\u05d7','\u05e8\u05e5 \u05e2\u05dc \u05d4\u05e9\u05e8\u05ea \u05e9\u05dc\u05d9','\u05d7\u05d9\u05e0\u05dd'],
   'fix_before':'\u05de\u05d4 \u05e9\u05d4\u05d5\u05d0 \u05e6\u05e8\u05d1',
   'fix_after':'\u05de\u05d4 \u05e9\u05d4\u05d5\u05d0 \u05e6\u05d5\u05e8\u05d1 \u05d4\u05d9\u05d5\u05dd',
   'fix_arrow':'\u2190',
   'claim8_foot':'\u05de\u05e0\u05d5\u05e2 \u05d4\u05d7\u05ea\u05d9\u05de\u05d4 \u05dc\u05d0 \u05d4\u05db\u05d9\u05e8 \u05d0\u05e3 \u05d2\u05d5\u05e4\u05df \u05e2\u05d1\u05e8\u05d9, \u05d0\u05d6 \u05db\u05dc \u05e9\u05dd \u05d9\u05e6\u05d0 \u05db\u05e8\u05d9\u05d1\u05d5\u05e2\u05d9\u05dd \u05e8\u05d9\u05e7\u05d9\u05dd. \u05ea\u05d9\u05e7\u05e0\u05ea\u05d9 - \u05d5\u05d0\u05d6 \u05d4\u05e8\u05e6\u05ea\u05d9 \u05d0\u05ea \u05d6\u05d4 \u05e2\u05dc \u05d8\u05d5\u05e4\u05e1 101, \u05db\u05dc 173 \u05d4\u05e9\u05d3\u05d5\u05ea.',
   'foot':'sign.zazet-solutions.hr/try101',
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
.sm{font-size:.55em;color:#94a3b8;font-weight:400}
.ltr{direction:ltr;unicode-bidi:isolate}
"""

TPL = """<!doctype html><html dir="{dir}" lang="{lang}"><meta charset="utf-8">
<style>{css}{extra}</style><body><div class="wrap">
{eyebrow_block}
{body}
<div class="foot">{foot}</div>
</div></body></html>"""


def design1(s):  # the one big number
    extra = """
    .num{font-size:104px;font-weight:700;color:#fef08a;line-height:.95;letter-spacing:-.02em}
    .unit{font-size:32px;color:#7dd3fc;margin-top:14px}
    .sub{font-size:27px;color:#cbd5e1;margin-top:30px;max-width:1010px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="num">{s["big"]}</div><div class="unit">{s["big_unit"]}</div>' \
           f'<div class="sub">{s["big_sub"]}</div></div>'
    return extra, body


def design2(s):  # the bold claim
    extra = """
    .claim{font-size:56px;font-weight:700;line-height:1.34;max-width:1040px}
    .cfoot{font-size:25px;color:#94a3b8;margin-top:34px;max-width:1000px;line-height:1.55}
    .mid{margin-bottom:auto}"""
    body = f'<div class="mid"><div class="claim">{s["claim"]}</div>' \
           f'<div class="cfoot">{s["claim_foot"]}</div></div>'
    return extra, body


def design3(s):  # the exchange
    extra = """
    .cells{display:flex;gap:30px;margin-bottom:auto;align-items:stretch}
    .cell{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:34px 30px;background:rgba(125,211,252,.04)}
    .cell.hot{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .lbl{font-size:17px;letter-spacing:.13em;color:#7dd3fc;line-height:1.5;margin-bottom:22px}
    .cell.hot .lbl{color:#fef08a}
    .val{font-size:37px;font-weight:700;line-height:1.4}"""
    body = f'<div class="cells"><div class="cell"><div class="lbl">{s["before_l"]}</div>' \
           f'<div class="val">{s["before_v"]}</div></div>' \
           f'<div class="cell hot"><div class="lbl">{s["after_l"]}</div>' \
           f'<div class="val hi">{s["after_v"]}</div></div></div>'
    return extra, body


def design4(s):  # the breakdown grid
    extra = """
    .gt{font-size:20px;letter-spacing:.16em;color:#7dd3fc;margin:6px 0 24px}
    .row{display:flex;justify-content:space-between;align-items:baseline;gap:24px;
     padding:15px 0;border-block-end:1px solid #16304f;font-size:26px;line-height:1.4}
    .row .amt{color:#fef08a;font-weight:600;text-align:end;max-width:62%}
    .gf{font-size:24px;color:#94a3b8;margin-top:26px;margin-bottom:auto}"""
    rows = "".join(f'<div class="row"><span>{n}</span><span class="amt">{v}</span></div>'
                   for n, v in s['grid'])
    body = f'<div class="gt">{s["grid_title"]}</div>{rows}<div class="gf">{s["grid_foot"]}</div>'
    return extra, body


def design5(s):  # the payoff quote
    extra = """
    .q{font-size:70px;font-weight:700;color:#fef08a;line-height:1.25;margin-top:10px}
    .qs{font-size:28px;color:#cbd5e1;margin-top:36px;line-height:1.6;margin-bottom:auto}"""
    body = f'<div class="q">{s["quote"]}</div><div class="qs">{s["quote_sub"]}</div>'
    return extra, body


def design6(s):  # the pipeline
    extra = """
    .steps{display:flex;gap:22px;align-items:stretch;margin-bottom:28px}
    .st{flex:1;border:1px solid #1e3a5f;border-radius:12px;padding:28px 24px;background:rgba(125,211,252,.04)}
    .st:last-child{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .sn{font-size:19px;letter-spacing:.15em;color:#7dd3fc;margin-bottom:16px}
    .st:last-child .sn{color:#fef08a}
    .sd{font-size:23px;line-height:1.5;color:#e2e8f0}
    .af{font-size:25px;color:#fef08a;font-weight:700;margin-bottom:auto;line-height:1.45}"""
    steps = "".join(f'<div class="st"><div class="sn">{n}</div><div class="sd">{d}</div></div>'
                    for n, d in s['arch'])
    body = f'<div class="steps">{steps}</div><div class="af">{s["arch_foot"]}</div>'
    return extra, body


def design8(s):  # the claim + the three pillars + the real before/after
    extra = """
    .c8{font-size:44px;font-weight:700;line-height:1.28;max-width:1040px;margin-bottom:22px}
    .pill{display:flex;gap:12px;margin-bottom:30px;flex-wrap:wrap}
    .pill span{border:1px solid #7dd3fc;color:#7dd3fc;border-radius:999px;
     padding:8px 20px;font-size:20px;font-weight:600;letter-spacing:.04em}
    .fix{display:flex;align-items:center;gap:24px;margin-bottom:18px}
    .fcell{border:1px solid #1e3a5f;border-radius:12px;padding:16px 24px;background:rgba(125,211,252,.04)}
    .fcell.hot{border-color:#fef08a;background:rgba(254,240,138,.07)}
    .flbl{font-size:13px;letter-spacing:.14em;color:#7dd3fc;margin-bottom:8px}
    .fcell.hot .flbl{color:#fef08a}
    .fval{font-size:40px;font-weight:700;color:#94a3b8;line-height:1.15;white-space:nowrap}
    .fcell.hot .fval{color:#fef08a}
    .arw{font-size:36px;color:#7dd3fc;flex:none}
    .c8f{font-size:21px;color:#94a3b8;max-width:1010px;line-height:1.5;margin-bottom:auto}
    .mid{margin-bottom:auto}"""
    pills = "".join(f'<span>{x}</span>' for x in s['pillars'])
    body = (f'<div class="mid"><div class="c8">{s["claim8"]}</div>'
            f'<div class="pill">{pills}</div>'
            f'<div class="fix">'
            f'<div class="fcell"><div class="flbl">{s["fix_before"]}</div>'
            f'<div class="fval">\u25a1\u25a1\u25a1\u25a1 \u25a1\u25a1\u25a1\u25a1</div></div>'
            f'<div class="arw">{s["fix_arrow"]}</div>'
            f'<div class="fcell hot"><div class="flbl">{s["fix_after"]}</div>'
            f'<div class="fval">\u05d9\u05e9\u05e8\u05d0\u05dc \u05d9\u05e9\u05e8\u05d0\u05dc\u05d9</div></div>'
            f'</div><div class="c8f">{s["claim8_foot"]}</div></div>')
    return extra, body


DESIGNS = [design1, design2, design3, design4, design5, design6, None, design8]
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    for i, fn in enumerate(DESIGNS, 1):
        if fn is None:
            continue
        for lang in ('en', 'he'):
            s = S[lang]
            extra, body = fn(s)
            eb = f'<div class="eyebrow">{s["eyebrow"]}</div>' if s['eyebrow'] else '<div style="margin-bottom:auto"></div>'
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
