#!/usr/bin/env python3
"""Per-port Facebook heroes in the site's own look, from the spine's real timetable.

    python3 heroes.py                 # every port below x 4 languages
    python3 heroes.py split hr en     # one port, chosen languages
"""
import base64, datetime as dt, html, os, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo

FW = Path.home() / "PycharmProjects/ferry-watch"
sys.path.insert(0, str(FW / "src"))
os.chdir(FW)
from ferry_watch.spine import db                      # noqa: E402
from ferry_watch.site.build import T, load_routes, port_board_data  # noqa: E402
from ferry_watch.site.timetable import port_departures, DAY_NAMES     # noqa: E402

HERE = Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT = base64.b64encode((FW / "src/ferry_watch/site/fonts/archivo.woff2").read_bytes()).decode()
ZG = ZoneInfo("Europe/Zagreb")
TODAY = dt.datetime.now(ZG)

# ponytail: the popular line per port is the busiest one out of it; override where a
# group cares about a different island than the busiest boat.
PORTS = ["split", "zadar", "valbiska", "brestova", "prizna", "supetar", "stari-grad",
         "orebic", "prapratno", "drvenik", "dubrovnik", "ploce", "trogir", "biograd",
         "makarska", "merag", "lopar", "porozina", "zigljen", "preko", "sobra",
         "domince", "trpanj", "sucuraj", "rogac", "vela-luka", "vis", "tkon", "brbinj"]

S = {
 "hr": dict(kicker="Luka · vozni red za danas", today="Danas, {day} {date}", to="Trajekt za",
            dur="plovidba {d}", season="Sezona vrijedi {a} – {b}", next_season="od {a} zimski vozni red",
            camera="HAK kamera luke uživo na stranici", promise="Sljedeći trajekt za 23 min. Otvoriš, pročitaš, zatvoriš.",
            more="+ još {n}", book_v="rezervacija vozila moguća", book_n="bez rezervacije, karta vrijedi za bilo koji polazak",
            none="Danas nema polazaka na ovoj liniji"),
 "en": dict(kicker="Port · today's timetable", today="Today, {day} {date}", to="Ferry to",
            dur="{d} crossing", season="Season timetable {a} – {b}", next_season="winter timetable from {a}",
            camera="live HAK port camera on the page", promise="Your next ferry in 23 min. Open, read, close.",
            more="+ {n} more", book_v="vehicle reservation possible", book_n="no reservation, ticket valid for any sailing",
            none="No departures on this line today"),
 "de": dict(kicker="Hafen · Fahrplan für heute", today="Heute, {day} {date}", to="Fähre nach",
            dur="{d} Überfahrt", season="Saisonfahrplan {a} – {b}", next_season="Winterfahrplan ab {a}",
            camera="Live-Hafenkamera (HAK) auf der Seite", promise="Deine nächste Fähre in 23 Min. Öffnen, lesen, schließen.",
            more="+ {n} weitere", book_v="Fahrzeugreservierung möglich", book_n="keine Reservierung, Ticket gilt für jede Abfahrt",
            none="Heute keine Abfahrten auf dieser Linie"),
 "it": dict(kicker="Porto · orario di oggi", today="Oggi, {day} {date}", to="Traghetto per",
            dur="traversata {d}", season="Orario stagionale {a} – {b}", next_season="orario invernale dal {a}",
            camera="telecamera live del porto (HAK) sul sito", promise="Il tuo prossimo traghetto tra 23 min. Apri, leggi, chiudi.",
            more="+ altri {n}", book_v="prenotazione veicolo possibile", book_n="senza prenotazione, biglietto valido per ogni partenza",
            none="Oggi nessuna partenza su questa linea"),
}
LONG_DAYS = {"hr": ["ponedjeljak","utorak","srijeda","četvrtak","petak","subota","nedjelja"],
             "en": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
             "de": ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"],
             "it": ["lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica"]}


def d_short(iso, lang):
    y, m, d = iso.split("-")
    return f"{int(d)}.{int(m)}." if lang in ("hr", "de") else (f"{int(d)}/{int(m)}" if lang == "it" else f"{int(d)} {['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][int(m)-1]}")


def dur_text(minutes, lang):
    h, m = divmod(minutes, 60)
    if h and m:
        return {"hr": f"{h} h {m} min", "en": f"{h} h {m} min", "de": f"{h} Std. {m} Min.", "it": f"{h} h {m} min"}[lang]
    if h:
        return {"hr": f"{h} h", "en": f"{h} h", "de": f"{h} Std.", "it": f"{h} h"}[lang]
    return {"hr": f"{m} min", "en": f"{m} min", "de": f"{m} Min.", "it": f"{m} min"}[lang]


def pick(conn, port_id, port_names, routes):
    """Busiest service out of the port, its window valid today, today's times."""
    today = TODAY.strftime("%Y-%m-%d")
    wd = TODAY.weekday()
    best = None
    for svc in port_departures(conn, port_id, port_names):
        for w in svc.windows:
            if not any((not a or a <= today) and (not b or today <= b) for a, b in w.ranges):
                continue
            times = sorted({dep for mask, ts in w.days if mask & (1 << wd) for dep, _ in ts})
            spans = [(int(a[:2])*60+int(a[3:])) - (int(d[:2])*60+int(d[3:]))
                     for mask, ts in w.days for d, a in ts if a]
            spans = sorted(s + (1440 if s < 0 else 0) for s in spans)
            cand = dict(svc=svc, window=w, times=times, dur=spans[len(spans)//2] if spans else None)
            if best is None or len(times) > len(best["times"]):
                best = cand
    return best


def render(lang, port_id, port_name, c, route):
    s, t = S[lang], T[lang]
    w = c["window"]
    rng = next((r for r in w.ranges if (not r[0] or r[0] <= TODAY.strftime("%Y-%m-%d")) and (not r[1] or TODAY.strftime("%Y-%m-%d") <= r[1])), w.ranges[0])
    season = s["season"].format(a=d_short(rng[0], lang) if rng[0] else "…", b=d_short(rng[1], lang) if rng[1] else "…")
    nxt = ""
    if rng[1]:
        after = (dt.date.fromisoformat(rng[1]) + dt.timedelta(days=1)).isoformat()
        if TODAY.month >= 9:
            nxt = s["next_season"].format(a=d_short(after, lang))
    times = c["times"]
    shown, rest = times[:14], len(times) - 14
    chips = "".join(f'<span class="chip">{x}</span>' for x in shown)
    if rest > 0:
        chips += f'<span class="chip more">{s["more"].format(n=rest)}</span>'
    if not times:
        chips = f'<span class="none">{s["none"]}</span>'
    dur = s["dur"].format(d=dur_text(c["dur"], lang)) if c["dur"] else (s["dur"].format(d=dur_text(route.duration, lang)) if route and route.duration else "")
    book = s["book_v"] if route and route.booking == "vehicle" else (s["book_n"] if route and route.booking == "none" else "")
    dest = c["svc"].terminus
    via = f' <span class="via">via {", ".join(c["svc"].via)}</span>' if c["svc"].via else ""
    dayname = LONG_DAYS[lang][TODAY.weekday()]
    date = d_short(TODAY.strftime("%Y-%m-%d"), lang)
    facts = " · ".join(x for x in (dur, book) if x)
    page = f"""<!doctype html><html lang="{lang}"><meta charset="utf-8"><style>
@font-face{{font-family:'Archivo';src:url(data:font/woff2;base64,{FONT}) format('woff2-variations');font-weight:400 800;font-stretch:100% 125%}}
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:oklch(0.979 0.006 214);--foam:oklch(0.965 0.014 214);--ink:oklch(0.205 0.030 214);--muted:oklch(0.452 0.026 214);
--sea:oklch(0.305 0.058 214);--sea-deep:oklch(0.245 0.052 214);--tile:oklch(0.585 0.158 41);--tile-lite:oklch(0.780 0.126 55);--rule:oklch(0.820 0.014 214)}}
body{{width:1200px;height:630px;background:var(--bg);color:var(--ink);font-family:'Archivo',system-ui,sans-serif;overflow:hidden;display:flex;flex-direction:column}}
.mast{{background:var(--sea-deep);color:var(--foam);padding:0 56px;height:64px;display:flex;align-items:center;justify-content:space-between;font-size:20px}}
.mast b{{font-weight:800;letter-spacing:.01em}} .mast span{{opacity:.72}}
.head{{background:var(--sea);color:var(--foam);padding:34px 56px 30px;flex:none}}
.kicker{{font-weight:600;font-size:15px;letter-spacing:.09em;text-transform:uppercase;color:var(--tile-lite)}}
h1{{font-weight:800;font-size:64px;line-height:1.02;margin-top:8px;letter-spacing:-.015em;font-stretch:110%}}
.to{{margin-top:14px;font-size:26px;opacity:.9}} .to b{{font-weight:700;opacity:1}} .via{{opacity:.7;font-size:.8em}}
.body{{padding:26px 56px 0;flex:1}}
.today{{font-weight:700;font-size:22px;color:var(--sea)}}
.chips{{display:flex;flex-wrap:wrap;gap:10px 12px;margin-top:14px}}
.chip{{font-weight:700;font-size:31px;letter-spacing:-.01em;background:var(--foam);border:1px solid var(--rule);border-radius:8px;padding:6px 14px;font-variant-numeric:tabular-nums}}
.chip:first-child{{background:var(--tile);color:#fff;border-color:var(--tile)}}
.chip.more{{background:transparent;border-style:dashed;color:var(--muted);font-weight:600;font-size:24px;align-self:center}}
.none{{font-size:26px;color:var(--muted)}}
.facts{{margin-top:16px;font-size:21px;color:var(--muted)}}
.season{{margin-top:6px;font-size:19px;color:var(--muted)}} .season b{{color:var(--tile);font-weight:700}}
.foot{{background:var(--foam);border-top:1px solid var(--rule);padding:0 56px;height:70px;display:flex;align-items:center;justify-content:space-between;font-size:21px;color:var(--sea)}}
.foot .p{{font-weight:700}} .foot .u{{font-weight:600;color:var(--tile)}}
</style><body>
<div class="mast"><b>Croatian Ferries</b><span>{html.escape(t["tagline"])}</span></div>
<div class="head"><div class="kicker">{html.escape(s["kicker"])}</div><h1>{html.escape(port_name)}</h1>
<div class="to">{html.escape(s["to"])} <b>{html.escape(dest)}</b>{via}</div></div>
<div class="body"><div class="today">{html.escape(s["today"].format(day=dayname, date=date))}</div>
<div class="chips">{chips}</div>
<div class="facts">{html.escape(facts)}{(" · " + html.escape(s["camera"])) if port_has_cam else ""}</div>
<div class="season">{html.escape(season)}{(" · <b>" + html.escape(nxt) + "</b>") if nxt else ""}</div></div>
<div class="foot"><span class="p">{html.escape(s["promise"])}</span><span class="u">croatianferries.com/{lang}/port/{port_id}/</span></div>
</body></html>"""
    hp = HERE / f"hero-{port_id}-{lang}.html"
    pp = HERE / f"hero-{port_id}-{lang}.png"
    hp.write_text(page, encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1200,630", "--virtual-time-budget=2500", f"--screenshot={pp}",
                    f"file://{hp}"], capture_output=True)
    hp.unlink()
    return pp.name, dest, times


if __name__ == "__main__":
    args = sys.argv[1:]
    ports = [a for a in args if a in PORTS] or PORTS
    langs = [a for a in args if a in S] or list(S)
    conn = db.connect()
    routes = load_routes(conn)
    by_line = {r.line: r for r in routes}
    port_names = {r["id"]: r["name"] for r in conn.execute("SELECT id, name FROM ports")}
    cams = {r["id"] for r in conn.execute("SELECT id FROM ports WHERE hak_camera_ids IS NOT NULL")}
    for pid in ports:
        c = pick(conn, pid, port_names, routes)
        if not c:
            print("skip", pid, "(no current service)"); continue
        port_has_cam = pid in cams
        for lang in langs:
            name, dest, times = render(lang, pid, port_names[pid], c, by_line.get(c["svc"].route_line))
            print(name, "->", dest, len(times), "today")
