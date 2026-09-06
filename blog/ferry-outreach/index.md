<!-- I posted a ferry site into 52 Facebook groups and used the comments as my issue tracker · Gal Tidhar — https://gal.tidhar.org.il/blog/ferry-outreach/ -->

FIELD NOTE / DISTRIBUTION

Croatia · Distribution · Feedback loops · croatianferries.com

# I posted a ferry site into 52 Facebook groups and used the comments as my issue tracker

2026-09-05  ·  ~9 min read  ·  by Gal Tidhar

There is no marketing budget for a free project. So distribution for croatianferries.com is 52 posts into Croatian, German and English island groups, and then a loop: sweep the comments, translate them, file the real complaints as issues, fix, deploy, and reply on the thread in the language the person wrote in. 11 issues in the repo were opened by people I have never met. This is the machinery, the numbers including the part nobody measures, the comments that were rude and useful at the same time, and the measurement bug that spent a week reporting a stranger's engagement as mine.

## The machinery

Three files in ops/fb/, all driven from a browser session on my own account. Nothing here is clever; the point is that it is a loop rather than a launch.

          | File | Job |

          | outreach.py | stateful ten-a-day group outreach: plan, join, post. Groups move through planned → joined → posted, so a run can die halfway and the next one picks up. |

          | collect.sh | walks every post in posts.json and prints every comment not already in the ledger. |

          | measure.sh | reads likes, comments and shares per post into metrics.json. |

          | seen.json | the dedup ledger, keyed on permalink + author + text. Skip the marking step and the next sweep files your own reply as fresh user feedback. |

          | answers.json | truthful answers to group-membership questionnaires. Most island groups ask three. |

        
A full comment sweep takes about 13 minutes; a full metrics run about 25. Both drive a real browser, which means memory is the actual constraint, not rate limits: the collector gets killed under roughly 2 GB free.

## The numbers, including the part nobody measures

52 posts. On 37 of them I can read the counters at all:

        1,211 likes  ·  153 comments  ·  39 shares  ·  across 37 measurable posts

Then the honest part. 8 of those 37 sit at a flat zero. And 15 posts I cannot measure at all: 6 are still held for admin approval and may never appear, and 9 do not render their own toolbar so there is no number to read. Nearly a third of the outreach either did not happen or cannot be proven to have happened. Every marketing report I have ever seen counts the posts that ran.

The top of the table, and the pattern in it:

          | Group | Likes | Comments | Shares |

          | OTOK HVAR | 194 | 15 | 4 |

          | Oglasnik otoka Korčule | 193 | 10 | 5 |

          | Pag Portal | 139 | 14 | 2 |

          | Croatia Travel - 2026 | 100 | 25 | 0 |

          | Otok CRES | 90 | 15 | 0 |

          | Tužibaba Cres - Lošinj | 74 | 6 | 7 |

        
Five of those six are a single island. The large pan-Croatia travel groups, the ones with tens of thousands of members that look like the prize when you are picking where to post, mostly returned nothing - and they are also where the six posts are sitting in a moderation queue. A group about one island is a group of people who take one ferry. A group about "Croatia travel" is a group of people who might, someday, take any ferry.

## Comments as a bug tracker

This is the part I would keep if I had to throw the rest away. Praise is noise - Svaka čast, Bravo, Hvala, dozens of them, and they tell you nothing you can act on. A complaint is a free bug report from someone standing at the port. Every one that survives triage becomes a GitHub issue with the original quote pasted into it, so the fix is checkable against what the person actually said.

          | The comment | What it became | Open → deployed |

          | "Samo pls prominite u Plovidbeni red, bokun vozni para uši. Nije primjereno." - the word vozni red grates on the ear, that is what a bus timetable is called; a ferry has a plovidbeni red | issue #11, wording fixed site-wide in Croatian | 31 min |

          | "ovo vrijedi do 6.9. ne 27.9." | issue #14 - a real parsing bug in the footnote that narrows a season's validity | 34 min |

          | "A Stinica - Mišnjak-Stinica ne najdem?" | issue #13 - the operator Rapska plovidba was not on the site at all; added with its full annual schedule | 58 min |

          | "Broj vozila u redu po kameri na Prizni se ne može procijeniti, kamera ne pokriva..." - you cannot estimate the queue from the Prizna camera, it does not cover it | issue #3 - he is right, I went and looked. A person who physically stands there beats my camera survey | same day |

          | "Jeli to samo Jadrolinija?" | issue #12 - operator coverage made explicit: 64 lines, 13 operators, stated on the page | 3 h |

          | "any chance for all the catamaran routes under one roof?" and then, unprompted, a full argument for keeping car and foot traffic separate | issues #9 and #22 - the by-car / on-foot toggle on the home page | next day |

          | "found some small styling issues on mobile phone if you are interested" | issue #16 | next day |

        
The plovidbeni red one is the one I think about. No amount of research would have handed me that word. It is not in a dictionary lookup, it is not in a competitor's page, it is the difference between a site written by someone from there and a site written by someone with a translation. A stranger gave it to me for free, in public, thirty-one minutes before it was live.

And every one of these got a reply on the thread itself - in Croatian, German or English, whichever they wrote in - naming what changed. That reply is not politeness. It is the only signal a person gets that commenting on a stranger's post did something.

## The rude ones

Not everything was warm.

> "Ti treba app i da predes cestu?" - do you need an app to cross the road too?
        "Or just download their app????"
        "Really dont understand what is here hard to understand"
        "What PDF? They have a regular search on their site."
        "Hvala na trudu ali bezpotrebno jer na stranicama putovnica.hr imate apsolutno..." - thanks for the effort but it is unnecessary

My first instinct was to argue. I wrote one of them a long, reasoned reply about what he had missed and how bad the alternative he was recommending is, and then deleted the whole thing. A person who bothers to tell you your thing is pointless is the exact user you have to win, and he has just told you, for free and in public, where the bar is. Arguing wins the thread and loses the user.

So it became issue #10, a standing competitor issue, and the rule that every "you already have X" comment goes there as a comment rather than becoming a new issue. That thread is now the best competitive research I have, and I did not do any of it:

        putovnica.net · the Vapor app · pickapp.hr · ferryrab.com · pagferry.com · qr.vapor-dalmatia.com · the operator's own app · a "Supetar ferry" page for Brač

I had not heard of a single one. A consultant would have charged me for that list and produced a worse version of it.

## The measurement bug I only found because the numbers were too tidy

Twelve posts, in twelve different groups, all reported exactly 12 likes and 7 comments. The run before that, ten posts all reported 1 and 13. Plausible-looking numbers, identical across unrelated groups, which is the only reason I looked.

Two failures were stacked. First, Facebook navigates in-app, so document.title updated to the new post while the counters did not: one German group's value stuck to the next ten reads. Second, and worse, the DOM anchor climbed out of the post entirely and settled on a container that was the whole page - navigation, stories, sidebar. That container had exactly one comment toolbar, belonging to an unrelated post Facebook had rendered into the sidebar feed. The tool was reporting a stranger's engagement as mine. The real post, further down the same DOM dump, had one reaction.

Five guards before the right one, each of them reasonable, each defeated by the page in a different way:

          | # | The guard | How the page beat it |

          | 1 | reject a container holding another post's permalink id | two ids appear on every group page - site chrome, not neighbours |

          | 2 | require exactly one comment toolbar | the page-level container had exactly one: the foreign post's |

          | 3 | detect the "pending admin approval" banner | correct for 6 posts, but the banner renders after the wait and races the read |

          | 4 | require our own croatianferries.com text in the container | the whole page contains our post too, so it passed |

          | 5 | reject a container holding nav, banner or sidebar landmarks | held. A post never contains page chrome |

        
The fix that actually matters is not any of those five. It is the rule underneath them: never write a reading that could not be anchored. Record pending admin approval or unreadable as a status instead of inventing a number. That is why the honest section above can say "15 posts I cannot measure" rather than quietly averaging them in at zero - a metric that cannot fail loudly will fail quietly, and it will look completely normal while it does.

The comment collector had the same class of bug. Its bleed filter only caught the same author and text under two permalinks; eleven different people commenting on an unrelated giveaway post that Facebook rendered into one group's page all had a single permalink, so they sailed through and were filed as feedback on my ferry site. Same containment rule fixed it: a comment is mine only if some ancestor holds my own post text before the climb reaches page level.

## What I would do differently

        

- Start small and local, not big and general. The instinct is to chase the 70,000-member group. It returned nothing, and it is where posts go to sit in a moderation queue.

- Record a status, never a zero. Any measurement that cannot distinguish "nobody engaged" from "I could not read it" is worse than no measurement, because you will trust it.

- Reply on the thread, not in a changelog. The fix is cheap; being visibly answered is what makes someone comment a second time.

- Keep the quote in the issue. Nine of the eleven comment-born issues carry the original sentence in the person's own language. It stops the fix drifting into what I would rather they had meant.

        

Still open: the 6 posts held for admin approval. Chasing a moderator is a cold DM to a volunteer, and the honest expected value is low. The 10 groups sitting at planned in outreach.json are the next batch, and the queue-camera work - the thing this project actually started from - is what the next post in this series is about.

          
### The site

croatianferries.com is free, has no cookies and no third-party requests, and answers one question: when does the next ferry leave, and in how many minutes. If you are on the Croatian coast, or know someone who drives there, that is what it is for. If you find something wrong with it, the fastest way to get it fixed is still to tell me rudely in public.

            croatianferries.com·
            A port page: Valbiska (Krk)·
            How the 23 PDFs were read
