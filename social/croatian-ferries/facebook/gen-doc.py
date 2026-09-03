#!/usr/bin/env python3
"""ZaZet doc: one card per Facebook group - post text in the group's language with the right
port link, Copy button, and the site-themed hero for that port. Groups come from groups.json."""
import base64, html, json, pathlib, subprocess

HERE = pathlib.Path(__file__).parent
WRAP_SRC = HERE.parent.parent / "whatsapp-presence" / "out-choices.html"
WRAP_BODY = HERE.parent.parent / "whatsapp-presence" / "choices-body.html"
POSTS = {l: (HERE / f"post-{l}.txt").read_text(encoding="utf-8").strip() for l in ("en", "hr", "de", "it")}
GROUPS = json.loads((HERE / "groups.json").read_text(encoding="utf-8"))
PORT_NAMES = {"split": "Split", "zadar": "Zadar", "valbiska": "Valbiska (Krk)", "brestova": "Brestova",
              "prizna": "Prizna", "supetar": "Supetar (Brač)", "stari-grad": "Stari Grad (Hvar)",
              "orebic": "Orebić", "prapratno": "Prapratno (Pelješac)", "drvenik": "Drvenik",
              "dubrovnik": "Dubrovnik", "ploce": "Ploče", "trogir": "Trogir", "biograd": "Biograd",
              "makarska": "Makarska", "merag": "Merag (Cres)", "lopar": "Lopar (Rab)",
              "porozina": "Porozina (Cres)", "zigljen": "Žigljen (Pag)", "preko": "Preko (Ugljan)",
              "sobra": "Sobra (Mljet)", "domince": "Dominče (Korčula)", "trpanj": "Trpanj",
              "sucuraj": "Sućuraj (Hvar)", "rogac": "Rogač (Šolta)", "vela-luka": "Vela Luka (Korčula)",
              "vis": "Vis", "tkon": "Tkon (Pašman)", "brbinj": "Brbinj (Dugi otok)"}
FOR_GROUP = {"en": "For this group", "hr": "Za ovu grupu", "de": "Für diese Gruppe", "it": "Per questo gruppo"}


def img(port, lang):
    p = HERE / f"hero-{port}-{lang}.png"
    if not p.exists():
        return ""
    prev = HERE / f".preview-{port}-{lang}.jpg"
    if not prev.exists():
        subprocess.run(["sips", "-Z", "620", "-s", "format", "jpeg", "-s", "formatOptions", "55",
                        str(p), "--out", str(prev)], check=True, capture_output=True)
    b64 = base64.b64encode(prev.read_bytes()).decode()
    return (f'<p class="pathline"><code>{p}</code></p>'
            f'<img src="data:image/jpeg;base64,{b64}" alt="hero {port} {lang}">')


def post_for(lang, port):
    text = POSTS[lang]
    if port:
        link = f"https://croatianferries.com/{lang}/port/{port}/"
        return text.replace("{PORT_LINK}", f"{PORT_NAMES[port]}: {link}")
    # a general group: drop the port line entirely
    return "\n".join(l for l in text.splitlines() if "{PORT_LINK}" not in l).replace("\n\n\n", "\n\n")


cards, seen = "", set()
for i, g in enumerate(GROUPS, 1):
    lang, port = g["lang"], g.get("port")
    key = (lang, port)
    pid = f"p-{i}"
    text = post_for(lang, port)
    hero = img(port, lang) if port else img("split", lang)
    cards += f"""
<section class="step">
  <h2>{i:02d} &middot; {html.escape(g["name"])}</h2>
  <p class="sub"><a href="{html.escape(g["url"])}" target="_blank" rel="noopener">{html.escape(g["url"])}</a>
  &middot; {html.escape(g.get("members",""))} &middot; {html.escape(g.get("privacy",""))} &middot; language <b>{lang}</b>
  &middot; hero port <b>{html.escape(PORT_NAMES.get(port, "general (Split)") if port else "general (Split)")}</b></p>
  {('<p class="why">' + html.escape(g["why"]) + '</p>') if g.get("why") else ''}
  <div class="copybar"><button class="copybtn" data-copy="{pid}">Copy post</button></div>
  <pre id="{pid}" class="term" style="white-space:pre-wrap">{html.escape(text)}</pre>
  {hero}
  <div id="done-{i}" data-persist-choice class="opts small">
    <div class="opt" data-value="posted"><div class="opt-head"><span class="dot"></span><b>Posted</b></div></div>
    <div class="opt" data-value="skip"><div class="opt-head"><span class="dot"></span><b>Skip this group</b></div></div>
  </div>
</section>"""

BODY = f"""
<div class="title">
  <p class="eyebrow">Facebook &middot; croatianferries.com</p>
  <h1>One post per group, in its language, with its port.</h1>
  <p class="lede">{len(GROUPS)} groups from today's sweep, biggest first. Each card has the post in the group's
  language with the matching port page linked, a Copy button, and a hero in the site's own look showing that
  port's real departures for today (from the spine, same data as the site). Click Posted as you go; it saves.
  Rules of thumb: post from your personal profile, not a page; one group every 20-30 minutes, not all at once,
  or Facebook flags it as spam; in private groups read the rules first, several ban links and want you to
  answer questions instead - there, comment the link under a "when is the ferry" question rather than posting.</p>
</div>
<section class="step">
  <h2>The four texts</h2>
  <p class="sub">Same story in each language. The line "For this group: PORT: link" is swapped per card; for
  general travel groups it is dropped and the hero is Split.</p>
</section>
{cards}
<style>
.copybar{{display:flex;justify-content:flex-end;margin:0 0 8px}}
.copybtn{{background:#012169;color:#fff;border:0;padding:8px 18px;font:inherit;font-size:14px;cursor:pointer;border-radius:2px}}
.opts{{display:flex;flex-direction:row;gap:14px;margin-top:12px}}
.opt{{border:1px solid rgba(10,22,40,.18);padding:10px 14px;cursor:pointer;background:#fff;flex:1}}
.opt.chosen{{border-color:#012169;border-width:2px;box-shadow:0 0 0 3px rgba(1,33,105,.10)}}
.opt-head{{display:flex;align-items:center;gap:10px;font-size:14px}}
.dot{{width:13px;height:13px;border-radius:50%;border:2px solid #012169;display:inline-block;flex:none}}
.opt.chosen .dot{{background:#012169;box-shadow:inset 0 0 0 2px #fff}}
.opt.chosen .opt-head::after{{content:"CHOSEN";margin-inline-start:auto;font-size:11px;letter-spacing:.12em;color:#012169;font-weight:700}}
.why{{color:#4a5e78;font-size:14px;margin:6px 0 12px}}
.pathline{{margin:14px 0 6px}} .pathline code{{font-size:12px;word-break:break-all}}
.step img{{width:100%;display:block;border:1px solid rgba(10,22,40,.12)}}
</style>
<script src="/copy.js"></script>
<script src="/persist.js"></script>
"""
shell = WRAP_SRC.read_text(encoding="utf-8")
old_body = WRAP_BODY.read_text(encoding="utf-8")
i = shell.find(old_body.strip()[:80]); j = shell.find(old_body.strip()[-60:]) + 60
assert i > 0 and j > i
doc = shell[:i] + BODY + shell[j:]
doc = doc.replace("<title>WhatsApp went silent - LinkedIn post", "<title>Croatian ferries - Facebook groups")
(HERE / "out-fb.html").write_text(doc, encoding="utf-8")
print("wrote out-fb.html", len(doc))
