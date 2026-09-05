BASE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:#0a1628;color:#bae6fd;direction:%(dir)s;
  font-family:'IBM Plex Mono','Arial Hebrew','Arial Unicode MS',system-ui,monospace;
  background-image:linear-gradient(rgba(125,211,252,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(125,211,252,.06) 1px,transparent 1px);
  background-size:40px 40px;display:flex;flex-direction:column;justify-content:center;align-items:center;
  text-align:center;padding:52px;position:relative}
.top{position:absolute;top:36px;inset-inline-end:56px;font-size:19px;color:#7dd3fc;font-weight:700}
.rev{position:absolute;top:38px;inset-inline-start:56px;font-size:14px;letter-spacing:.14em;
  color:rgba(186,230,253,.45)}
.rev span{direction:ltr;unicode-bidi:isolate}
.num{direction:ltr;unicode-bidi:isolate;display:inline-block}
.kicker{font-size:27px;color:rgba(186,230,253,.62);margin-bottom:14px;max-width:1020px;line-height:1.34}
.claim{font-size:52px;font-weight:800;color:#e0f2fe;line-height:1.34;max-width:1060px}
.claim b{color:#fef08a}
.foot{position:absolute;bottom:34px;font-size:20px;color:rgba(186,230,253,.6)}
.foot b{color:#e0f2fe}
%(extra)s
</style></head><body>
<div class="top">%(top)s</div><div class="rev"><span>gal.tidhar.org.il</span></div>
%(body)s
<div class="foot">%(foot)s</div>
</body></html>"""

D2 = """
.card{border:2px solid rgba(125,211,252,.55);width:1050px;text-align:start;padding:0 0 6px}
.card .hd{background:rgba(125,211,252,.12);padding:14px 28px;font-size:28px;font-weight:800;color:#7dd3fc;
  border-block-end:2px solid rgba(125,211,252,.35)}
.card .r{display:flex;gap:20px;padding:11px 28px;align-items:baseline}
.card .k{font-size:21px;color:#fef08a;font-weight:700;min-width:210px;flex:none}
.card .v{font-size:21px;color:rgba(186,230,253,.82);line-height:1.36}
.note{font-size:30px;color:#e0f2fe;font-weight:700;margin-top:26px;max-width:1020px;line-height:1.36}
.note b{color:#fef08a}
"""

D3 = """
.pair{display:flex;align-items:stretch;gap:40px;margin-top:6px}
.cell{padding:26px 34px;border:2px solid;width:420px;display:flex;flex-direction:column;justify-content:center}
.cell.bad{border-color:rgba(248,113,113,.65)}
.cell.good{border-color:rgba(125,211,252,.7)}
.cell .lab{font-size:21px;color:rgba(186,230,253,.66);margin-bottom:14px}
.cell .val{font-size:46px;font-weight:800;line-height:1.24}
.cell.bad .val{color:#f87171}
.cell.good .val{color:#7dd3fc;text-shadow:0 0 40px rgba(125,211,252,.45)}
.cell .sm{font-size:20px;color:rgba(186,230,253,.62);margin-top:14px;line-height:1.4}
.arw{font-size:52px;color:rgba(186,230,253,.5);align-self:center}
.note{font-size:30px;color:#e0f2fe;font-weight:700;margin-top:34px;max-width:1020px;line-height:1.36}
.note b{color:#fef08a}
"""

D4 = """
.title{font-size:34px;font-weight:800;color:#e0f2fe;margin-bottom:26px;max-width:1040px;line-height:1.3}
.map{display:flex;flex-direction:column;gap:13px;width:1060px}
.mr{display:flex;align-items:baseline;gap:18px;text-align:start}
.mr .k{font-size:24px;color:#7dd3fc;font-weight:800;min-width:230px;flex:none}
.mr .eq{color:rgba(186,230,253,.4);font-size:22px;flex:none}
.mr .v{font-size:22px;color:rgba(186,230,253,.75);line-height:1.36}
"""

D5 = """
.list{display:flex;flex-direction:column;gap:19px;width:1060px;margin-top:10px}
.item{display:flex;align-items:baseline;gap:18px;border-inline-start:3px solid rgba(125,211,252,.55);
  padding-inline-start:22px;text-align:start}
.item .t{font-size:26px;color:#7dd3fc;font-weight:800;min-width:250px;flex:none}
.item .d{font-size:23px;color:rgba(186,230,253,.72);line-height:1.4}
.note{font-size:30px;color:#fef08a;font-weight:800;margin-top:32px;max-width:1020px;line-height:1.36}
"""

D6 = """
.quote{font-size:48px;font-weight:800;color:#e0f2fe;line-height:1.38;max-width:1080px}
.quote b{color:#fef08a;text-shadow:0 0 45px rgba(254,240,138,.35)}
.punch{font-size:27px;color:rgba(186,230,253,.7);margin-top:34px;max-width:980px;line-height:1.4}
"""


