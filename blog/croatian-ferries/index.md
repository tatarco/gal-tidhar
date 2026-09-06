<!-- I was done decrypting PDFs to find my next ferry · Gal Tidhar — https://gal.tidhar.org.il/blog/croatian-ferries/ -->

# I was done decrypting PDFs to find my next ferry

_Croatia · Ferries · Timetables · croatianferries.com_

**2026-09-03**  ·  ~8 min read  ·  by Gal Tidhar

Every car-ferry timetable in Croatia is a PDF. Three seasons side by side, asterisks next to half the times, and the footnotes that decide whether your 14:30 exists today are on page 2. I read all 23 of them once so that nobody sitting in a car at the port has to. The result is [croatianferries.com](https://croatianferries.com/): open the port, get the next departure and the minutes until it. This is how the timetables were read, where it went wrong, and what is still missing.

## The moment

You are in the car, in the lane at the port, and you want to know whether the 14:30 sails today. The operator, Jadrolinija, publishes each line as a PDF. It is a printed table: columns for the low season and the high season, sometimes a third for a shoulder week, times with asterisks after them, and below the table the footnotes. A real one, from line 332 Valbiska - Merag:

`* Sails 20.06. & 27.06.
** 20.06. & 27.06. departs at 18:00.
Does not sail on Sundays and holidays.`
 Others from the same set of 23 files: _"Does not operate on Sat, Sun & Hol. until 30.03."_, _"On mondays departs from Valbiska at 21:00."_, _"From 01.01. to 22.02. & from 06.12. to 31.12. on Sundays and holidays..."_. Now answer, on a phone screen, from the car: is there a ferry in ten minutes?

This is not a Croatian-only problem. The families who drive down from Germany and Italy every summer hit exactly the same page 2, in a language they cannot read. That is who the site is for: locals with a car, and the tourist who is at the port for the first time.

## What the site does

Open a port and the page answers, in order: when the next ferry leaves and in how many minutes, how long the crossing takes, whether the line takes a reservation at all, and the live port camera from HAK so you see the actual queue and not only the timetable. Every car-ferry line the operator runs: 23 lines, 52 departure ports, four languages (Croatian, English, German, Italian; the German and Italian were reviewed by native speakers). No cookies, no third-party requests of any kind, no consent banner because there is nothing to consent to. The "in 23 min" is computed in the browser from the timetable that is already on the page; with scripting off the page still answers, just without the minutes.

## How the PDFs were read

This is the part that took the longest, and the part I would defend. Reading one of these tables is judgment: which column belongs to which season, which port a column belongs to, what each asterisk restricts, whether a footnote means "this departure does not exist in this season" or "this departure exists but at a different time on two days". Copying six hundred times out of it is not judgment, and copying by hand is exactly where transcription errors come from.

So each line has a small spec file that records only the judgment. For 332 it says: two seasons, these date ranges, the table body is lines 12 to 24 of the PDF text, column 0 is Merag and column 1 is Valbiska, and here is what the footnote markers mean. The code then copies the times straight out of the PDF's own text, never from a human retyping. The judgment is 30 lines a person can review. The copying is mechanical and tested.

`"seasons": [
 {"label": "LOW SEASON 01.01. - 02.07. & 01.10. - 31.12.",
 "ranges": [("2026-01-01", "2026-07-02"), ("2026-10-01", "2026-12-31")],
 "lines": range(12, 24),
 "legs": _legs(0, 1),
 "note": "Does not sail on Sundays and holidays. * from 01.01. until 22.03. ..."},
 {"label": "HIGH SEASON 03.07. - 30.09.", ...}
]`
 The output of all 23 specs is a validated spine: 1,076 sailings across 105 seasons, in SQLite, with a deterministic validator that quarantines anything that does not fit (a departure after its own arrival, a port that appears under two spellings, a season with no dates). The site is generated from that spine, statically, so a page is a file and nothing is computed per request.

The PDFs themselves are watched. Each operator route page is crawled daily, the PDF is fetched only when its hash changes, and a change lands as a new snapshot that has to pass the same validator before it replaces anything. When Jadrolinija quietly publishes a new file in June, we know.

## Where it went wrong

Crossing durations are derived, not scraped: the timetable prints arrival times on most lines, so the duration is arrival minus departure from the PDF itself. Where the PDF only prints departures, a prose fallback reads the operator's route page, which says things like "the crossing takes 25 minutes".

That fallback matched only "N minutes". So "1 hour and 40 minutes" became **40**, and line 434 Zadar - Brbinj shipped, for a moment, with a 40-minute crossing for a trip that takes an hour and forty. On a ferry site a wrong number is worse than a missing one: a missing duration makes you check, a wrong one makes you miss the boat. It is fixed, and every hour phrasing the operator uses is now a test case. Two lines still have no duration, correctly: 634 Orebić - Dominče states none anywhere, and 431 Zadar - Ošljak - Preko quotes 25 minutes on the route page, which is the direct line's number and cannot be right for a line that calls at Ošljak on the way. The multi-stop guard refuses it, which is the right call.

## What is deliberately not there

No analytics script unless the environment says so, and the only one that fits is Cloudflare's cookieless beacon. No map tiles from a third party, which is why the pick-a-port map is not built yet: it will be an inline SVG coastline, not a tile CDN. No ad network, because Croatia enforces prior opt-in consent for ad cookies and a consent wall on a page whose whole promise is "open, read, close" would be self-defeating.

And no queue number yet. The project actually started from the other end, in June, with the HAK traffic cameras at Merag: count the cars in the lane, watch the berth, and tell you whether you will make this ferry or the next one. That is still the real product, and it needs the first always-on piece of infrastructure. Every port page with a camera says "queue reading coming", and the code path self-heals: the moment capture produces readings the verdict appears with no site change. The timetable was the thing I could give people this week.

## Honest numbers

The site is days old. In the last seven days it had 20 real visits, and most of them were me checking it. Nobody knows it exists yet. If you are on the Croatian coast this summer, or know someone who drives there, that is what the link is for.

[croatianferries.com](https://croatianferries.com/) · [A port page: Valbiska (Krk)](https://croatianferries.com/en/port/valbiska/)
