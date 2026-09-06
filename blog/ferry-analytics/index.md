<!-- I rank 5th for a port camera I never tried to rank for · Gal Tidhar — https://gal.tidhar.org.il/blog/ferry-analytics/ -->

FIELD NOTE / SEARCH

Croatia · Search · Long tail · croatianferries.com

# I rank 5th for a port camera I never tried to rank for

2026-09-06  ·  ~8 min read  ·  by Gal Tidhar

Episode 1 of this series was distribution: 52 Facebook groups and the comments as my issue tracker. This one is the silent loop. croatianferries.com has been live for less than a week, so this is the week-one problem: getting a search engine to know 3,164 pages exist at all, and then reading the first scraps of data honestly. The numbers are embarrassing - 1 click, 172 impressions - but the shape of those 172 impressions says something I would not have guessed and would not have chosen: the pages winning are the ones nobody aimed at, a live port camera and a page for one named pair of ports.

## Week one: getting 3,164 pages known

The deploy that added the island pages and the port-pair pages took the sitemap from 316 URLs to 3,164. Search Console read it and reported Success, with 3,164 discovered (its own count, on 5 September; the sitemap itself lists 1,960 <loc> entries today, each carrying four hreflang alternates). Discovered is not indexed, and that is the whole of the first week's work.

The thing that surprised me: the Search Console API can report a page's index status, but it cannot request indexing. The URL Inspection endpoint is read-only for that purpose - asking Google to crawl a specific URL is a manual click in the UI, and the quota is roughly 7 to 8 requests a day, shared across the whole property. 3,164 pages at 7 a day is over a year, so pushing pages in one by one is not a strategy. The sitemap does the bulk on Google's own schedule; the daily quota is a scalpel, spent in priority order:

        

- English island pages - the broadest intent, and the language most likely to be searched by a visitor planning a trip

- Italian, then German, then Croatian

- Pair pages last, ordered by expected search volume: Split–Hvar, Split–Brač, Zadar–Dugi otok, Krk–Lošinj

        

On the first day the quota was already spent before I got to it and every request came back "you've exceeded your daily quota, please try submitting this again tomorrow", which is its own useful lesson: the budget is per day and per property, not per session.

## The half of search that does not make you wait

The seven-a-day ceiling is Google's, and only Google's. Bing, Yandex and Seznam accept IndexNow: one POST, up to 10,000 URLs, no daily quota, and ownership proved by serving a key file at /<key>.txt. There is no equivalent from Google - they have said publicly they are evaluating it and that is where it has stayed.

So ops/gsc/indexnow.py reads the same live sitemap and submits the lot in a single call. It refuses to submit an empty sitemap, and refuses if the sitemap holds a URL on another host, because a bulk submit is exactly the kind of thing that should fail loudly rather than quietly ping a stranger's domain. First run: 1,960 URLs, HTTP 200, and Bing Webmaster Tools confirms them arriving. The sitemap itself had never been registered there - Google had it from day one, Bing did not, and nothing tells you. The key file is not written on preview builds - a preview branch must not be able to submit URLs for the live domain.

This matters more than it used to, and not because of Bing's search share. Bing's index is what several AI assistants read when they answer a question about a place, so being in it quickly is part of being quotable at all - the same reason the site publishes llms.txt, an OpenAPI spec and a JSON endpoint per route and per port, and lets every AI crawler in on purpose in robots.txt.

## The job that counts it every morning

Submitting is manual. Knowing where you stand should not be, and this is the part that actually keeps the work honest. ops/gsc/indexed.py runs from launchd every morning at 09:40:

        

- It reads the live sitemap and pulls the island URLs out of it. Never a hand-typed list - a hand-typed list is stale the next time a page is added, and then the tally is quietly measuring the wrong thing.

- It asks the URL Inspection API for each page's coverageState, one at a time, and a failure on one URL is recorded as that URL's state rather than losing the run.

- It writes the tally as a comment on the tracking issue, per language, plus the list of English pages still not indexed.

        

Which turns a vague feeling into a line you can watch move:

        Day one: en 0/45 · it 0/45 · de 0/45 · hr 0/45Today: en 43/45 · it 20/45 · de 32/45 · hr 15/45

110 of 180 island pages indexed, and the states are specific enough to act on: Discovered - currently not indexed means Google knows and has not bothered, URL is unknown to Google means the sitemap has not carried it yet, and Crawled - currently not indexed means it looked and declined. Two English pages are still out: /en/island/pag/ is unknown to Google, and /en/island/silba/ was crawled and passed over.

The pair pages - 586 of them - are deliberately not in this tally. They ride the sitemap. They go on the list only if they are still unknown once the islands are in, which is the ponytail rule written into the top of the script: do not measure what you are not going to act on.

## The honest baseline

        1 click  ·  172 impressions  ·  0.58% CTR  ·  average position 20.7  ·  2026-08-07 to 2026-09-03

There is no way to dress that up and I am not going to try. It is a site that has been live for less than a week, in a market with entrenched incumbents, and Google is showing it to almost nobody. GA4 has nothing at all for the period - the consent gate was blocking it until 5 September, which is its own lesson and not this post's.

What a month of near-zero traffic is good for is direction. 172 impressions is too small to prove anything about volume, and just big enough to show which kind of page a search engine is willing to put in front of a person.

## What I expected to rank

The head terms. The phrases you would put on a whiteboard if someone asked what a Croatian ferry site should rank for:

          | Query | Position | Impressions |

          | fähre kroatien | 49 | 1 |

          | fähren kroatien | 44 | 1 |

          | dubrovnik to split ferry schedule | 67 | 1 |

          | fähre split supetar | 57 | 1 |

          | fähre supetar split | 55 | 1 |

          | brac split ferry timetable | 58 | 1 |

        
Split - Supetar is the busiest car ferry crossing in Croatia and the site is on page six for it. That is not a defect in the page, and this is where the analytics run first sent me wrong.

## The recommendation I retracted the same day

The run's advice was: Split - Supetar sits at 57, over-invest in that page. So I opened it. The German title already reads Fähre Split – Supetar (Brač) · Fahrplan 631 - a near-exact match for the query, with the crossing duration and the reservation rules already inside the result snippet. There is nothing to fix on the page.

Then I checked where "position 57" came from. One impression. A single time, someone in Germany was shown this site somewhere down page six, and that one sample became an average position, and the average position became a finding. Position from n=1 is noise. It was presented to me as a number and I nearly spent a day on it.

A second recommendation went the same way: "http:// is indexed, we have a canonical split." I had read dist/_redirects, seen only / /en/ 302, and concluded the scheme redirect was missing. One curl -I showed Cloudflare returning a 301 before _redirects is ever consulted. The redirect file was not the only redirect layer, and the file was the only thing I looked at.

Two of nine recommendations retracted the same day they were written, both for the same reason: the data was read without opening the artifact it describes. And chasing the first bad one is what found the real bug, further down.

## What actually ranks

Sorted by position rather than by what I hoped for, a different site appears:

          | Query | Position | What it is |

          | hak merag | 5 | the live camera at the port of Merag |

          | gazenica brbinj trajekt | 7 | one named pair of ports |

          | hak kamera porozina | 8 | a live port camera |

          | domince korcula | 8 | one named port |

          | fähre sumartin makarska fahrplan | 9 | one named pair, plus "timetable" |

          | hak kamera brestova | 9 | a live port camera |

          | dominče orebić | 9.5 | one named pair |

          | fähre zadar dugi otok fahrplan | 11 | one named pair, plus "timetable" |

        
And the pages behind them: de/ferry/sumartin-brac-makarska at 6.3, de/ferry/zadar-gazenica-preko-ugljan at 9, de/port/lopar at 11. Every single one is a page about one specific thing with its full name on it. Nothing generic appears anywhere near the top.

This is not a clever insight, it is how a new site with no authority ranks at all. But it is very different reading it as a general principle and reading it as a list of the exact eight phrases your own site is currently winning.

## The cameras: the one thing nobody else has

Three of the eight are camera queries. Somebody in Croatia types hak kamera porozina into Google because they are about to drive to the port and they want to see how long the line is. HAK - the Croatian automobile club, which runs the national road camera network - publishes those feeds. I embed the relevant one on the page of every port that has one, next to the timetable, so the answer to "should I leave now" is on a single page.

Three things about this that I did not appreciate until the Search Console data:

        

- No competing ferry site carries them at all. Not the operators, not the aggregators, not the apps. The queue camera is the thing everyone standing in a ferry line actually wants, and it lives on a road-authority site that nobody thinks to check.

- It was already ranking without any effort. Position 5, 8 and 9, with zero optimisation, zero links, and a two month old domain.

- The page titles never said the word camera. The one asset that is genuinely mine and genuinely rare was invisible in the only text Google shows a person.

        

## And then the titles

Going to fix that is what surfaced the larger bug. Here is what a port page was telling Google it was:

```
Trajekti i katamarani iz luke Zadar Liburnska obala · plovidbeni red · Croatian Ferries
                                                                       87 characters
```

Google shows about 60. Route pages have had a guard for this for a while - past 60 characters the · Croatian Ferries suffix is dropped so the route name survives. Port pages never got the same guard. Nobody decided that; the port templates were written later and the guard simply was not carried across.

        278 of 396 port titles were over length. Seven out of ten port pages were advertising themselves in search results with the end sawn off.

The fix is a shorter stem plus the same guard the routes already had: Trajekti iz luke {port}, Fähren ab {port}. 278 over-length titles down to 6, and those 6 are the longest Croatian port names, which can stay. 146 site tests pass on it.

The uncomfortable part is how long this sat there. The site's whole reason to exist is reading badly formatted schedules so a person does not have to, and in the one line a person actually reads before deciding to click, the text was cut mid-word on most of the site.

## Saying it in the title, without lying

With room in the titles, the camera could go in them:

```
de/merag     Fähren ab Merag (Cres) · Fahrplan und Live-Kamera
en/supetar   Supetar (Brač) ferry timetable and live camera
en/bol       Bol (Brač) ferry timetable · Croatian Ferries      <- no camera, no claim
```

16 of the 99 ports have a camera. The tempting version is to put "live camera" on all 99 and let the click-through sort it out. That is how you teach a search engine, and a person, that your titles are not to be trusted - and the whole value of this site over an operator PDF is that it does not waste your time. So the 16 are resolved against the camera map at build time rather than asserted, and the other 83 promise nothing they do not have.

## Postscript: two of the best-ranking pages were 404s

After this was written I ran Cloudflare's agent-readiness scan on the domain, and its demand signals panel - paths AI assistants ask for and do not get - was the most useful thing in the whole exercise. The dead paths were route URLs without their disambiguating suffix. When a second operator or a second line with the same endpoints appeared, the slug gained a suffix (split-supetar-brac became split-supetar-brac-631 and split-supetar-brac-krilo) and the original URL was left to die.

Search Console was still serving those old URLs. de/ferry/zadar-gazenica-preko-ugljan/, position 9. de/ferry/zadar-gazenica-brbinj-dugi-otok/, position 11. Both 404. Two of the best-ranking pages on the site, in the table I had just finished celebrating three paragraphs earlier, were dead links - and the ranking table cannot tell you that, because it reports the URL Google shows, not the status code it gets. Every superseded slug now 301s to a real page in all four languages, 124 rules generated from the route list.

The other number from that scan puts the whole post in proportion. In 24 hours: 596 AI answer retrievals - ChatGPT-User 363, Applebot 213, PerplexityBot 20 - against 1 Google click in a month. The audience that has actually found this site is not human yet.

## What is still open

        

- The traffic is German, the visitors are Croatian. Nearly every impression lands on a /de/ page, and the German pages are the ones ranking - yet 98 of the 172 impressions come from Croatia. Locals are finding the German tree. The /en/ and /hr/ trees barely surface at all, and I do not yet understand why.

- The head routes stay where they are. Split - Supetar is an authority problem, not a title problem. No amount of on-page work moves it this year.

- www serves a full duplicate at 200. Every page exists on two hostnames; the www copy does emit a canonical pointing at the apex, so it is crawl budget and ambiguity rather than a split. A Cloudflare redirect rule fixes it. Low value, still open.

        

## What I would do differently

        

- Never accept a position from a single impression. An average of one number is that number, and it will be presented in the same table, in the same font, as a real one.

- Open the artifact the data describes. Both retractions this run came from reading a file or a metric and not looking at the live thing. The redirect file was not the only redirect layer; the "underperforming" page was already near-perfect.

- Check the guard on every template, not the one you wrote it for. The routes had it, the ports did not, and nothing told me for two months.

- Do not try to force a big site in through the daily quota. 7 a day against 3,164 pages is a rounding error. The sitemap is the mechanism; the quota is for the handful of pages you actually care about this week.

- Read the ranking table by what is at the top, not by what you wanted at the top. The eight phrases at positions 5 to 11 were sitting in the same export as the ones at 49 to 67, and they are the entire strategy.

        

The analytics skill that produced this run now keeps a ledger: every recommendation is written down with the one metric it will be judged on, so the next run scores this one instead of generating fresh advice forever. Two of the nine are already marked retracted, with the reasoning, which is the part I would have quietly forgotten. SEO changes take three to four weeks to register, so there is nothing to report yet, and an unmoved number next week means too early, not failed.

          
### The site

croatianferries.com is free, has no cookies and no third-party requests, and answers one question: when does the next ferry leave, and in how many minutes. On the 16 ports that have one, it also shows you the queue.

            croatianferries.com·
            A port page with a camera: Merag (Cres)·
            Episode 1: 52 Facebook groups·
            How the 23 PDFs were read
