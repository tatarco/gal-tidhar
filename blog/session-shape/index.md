<!-- The comments were right: cache ratio is a symptom, session shape is the cause · Gal Tidhar — https://gal.tidhar.org.il/blog/session-shape/ -->

# The comments were right: cache ratio is a symptom, session shape is the cause

_Claude Code · 1,088 sessions · 8 months of logs_

Published **2026-08-10** · follows [cache economics](/blog/cache-economics/) · every number below is from my own local logs, nothing estimated

Two days ago I wrote that 96.3% of my tokens are cache reads and that this is why I cannot hit my Claude Code limit. The comments took the thesis apart from three directions. Instead of defending it, I sent five subagents into everything I have: 1,088 logged sessions since April, 2.8 GB of transcripts, every checkpoint my measurement tooling ever wrote. **The commenters were mostly right, and the drilldown found a better number than the one I led with.**

## Objection one: a ratio is not a cost

> "96% is a ratio, not a cost. You can hold an excellent ratio and still burn more, simply because you did three times as many turns. What I would measure is what a finished task cost." - Omri Pitaru

He is right, and my own logs prove it better than I expected. A background tool has been grading every one of my sessions since April. Here is the month-by-month picture:

| Month | Sessions | Avg input tokens / session | Quality score | Cache hit rate |
|---|---|---|---|---|
| April | 207 | 6.4M | 67.2 | 74.3% |
| May | 188 | 9.0M | 63.2 | 76.8% |
| June | 247 | 3.2M | 62.9 | 78.2% |
| July | 259 | 6.8M | 67.2 | 79.7% |
| August (partial) | 187 | 1.7M | 76.5 | 77.7% |

Look at May against August. Same session volume, same workload, a **5x drop in tokens per session**, best quality score in the log. And the cache hit rate between those two months barely moved: 76.8% against 77.7%. If cache ratio were the driver, May and August should have cost the same. They did not, because what changed is the shape of the sessions, not the ratio.

**A note on two cache numbers.** The 96.3% in the original post is the share of my input volume served as cache reads, measured from transcripts. The grader above scores cache hits per request, a stricter cut, which is why it reads in the 70s. They measure different things; the point here is only that the grader's metric is _flat_ between my cheapest and most expensive months.

So the metric I led with in part one was the wrong one. A high cache ratio is what a well-shaped session _produces_, not something you optimize directly. The number worth tracking is **tokens per finished session**, exactly as Omri said. Mine went from 9M to 1.7M while the ratio stood still.

## What the trend actually says: this is learnable

Out of 1,088 graded sessions, **385 (35%) got a D**. Nearly all of them share one pattern: marathons. The worst three in the log ran 5.4M, 5.5M and 7.3M input tokens, two of them over 14 hours of wall time. The best sessions in the log (quality 100) are the opposite shape: under 3 minutes, ~100K tokens, 85-91% cache hits.

I was the person burning a plan, and the habits were learned inside that log - which is exactly why they are teachable and why "I just use it less" is the wrong takeaway. My session count never dropped. The shape changed, and the bill followed.

## Objection two: subagents start cold

> "Subagents keep the parent prefix stable, but each one starts cold, so you pay full price for its context. Net loss when it hands back something long that gets pasted into the parent. What I watch now is the size of what comes back, not the size of what goes in." - Roki Hasan

Also right, and worth quantifying rather than arguing. The trade in my logs:

- **1,679 subagent transcripts against 418 main sessions** - about four dispatches per session. The bulk of my 2.8 GB of transcripts lives in the subagents, not the main threads.
- The main-thread context fill across recent checkpoints: **median 14%, never above 31%**. The expensive model's window stays nearly empty because file dumps land in throwaway contexts.
- My input-to-output ratio across all sessions is roughly **150:1**. Almost everything I am billed for is context being re-read, so anything that keeps the main window small wins compound interest every turn until the session ends.
- The honest cost: my own tooling flags **agent dispatch overhead** as the single weakest signal in otherwise good sessions - firing five-plus dispatches in one burst scores as low as 71 on that metric. The savings mechanism is also the one measured cost center.

Roki's rule survives contact with the data and I have adopted it as stated: **watch what comes back, not what goes in.** A subagent that returns a paragraph pays for itself; one that returns a wall of text into the parent defeats the purpose.

## Objection three: what about switching models mid-session

> "If you start with Haiku you will have to shift up at some point and switch models, and then your whole cache resets. What do you do about that?" - Roy Perez

The data answers this cleanly: the main thread never switches because it is **always Opus**. The Haiku-by-default rule in my CLAUDE.md applies to subagents, which live for minutes and die. 58% of last month's 1,085 dispatches ran Haiku explicitly. A cache reset on a context that is about to be discarded costs nothing; a cache reset on the long-lived main thread is the thing to avoid - which is rule one from part one, unchanged.

## What survived, what fell

| Claim from part one | Verdict after the drilldown |
|---|---|
| Never break the prefix (no model switches, no stale-session wakeups) | **Survived.** Still the mechanism underneath everything. |
| Defaults beat discipline (Haiku-by-default in CLAUDE.md) | **Survived.** The transcripts show the rule actually holds under load. |
| Push noisy work into subagents | **Survived, with Roki's amendment:** meter the return payload, not the dispatch. |
| Lots of skills is fine because they are frozen prefix | **Survived**, with Omri's caveat: a skill that loads mid-session, an edited CLAUDE.md, or an MCP server connecting all rewrite the prefix without any model switch. My mitigation, mostly by accident: almost no MCP servers, and skills usually execute inside subagents. |
| 96.3% cache reads as the headline metric | **Fell.** It is a symptom. The causal metric is tokens per finished session: mine dropped 5x while the ratio moved less than one point. |

## Run the same audit on yourself: setup-audit

Chaim asked for an importable skill, so the whole drilldown is now one: [**claude-setup-audit**](https://github.com/tatarco/claude-setup-audit). It reads your local logs (nothing leaves your machine), scores you against the seven habits, and prints a versioned block that is comparable between people line by line. One command, no install:

`curl -fsSL https://raw.githubusercontent.com/tatarco/claude-setup-audit/main/setup-audit.py \
 -o /tmp/setup-audit.py && python3 /tmp/setup-audit.py --share`
 Or as a skill, so `/setup-audit` works in any session:

`git clone https://github.com/tatarco/claude-setup-audit ~/.claude/skills/setup-audit`
 Here is my real output, after everything this post describes:

`CLAUDE SETUP AUDIT v1 - last 30 days
399 sessions, 1,301 subagent runs

 delegation 3.2 subagents/session A
 cheap models 60% of dispatches on haiku A
 prompt shape median 56 chars A
 main context median 244k C
 session cost 22.9M input tokens/session F
 marathons longest ran 24d / 3,536 turns F
 setup overhead ~6.7k tokens before turn one (3 MCP) C
 ----------------------------------------------------------
 AUDIT C

 FIX FIRST: session cost - the number that drains a plan - watch
 its trend, not your cache ratio.`
 A C, with two F's - both caused by one session I forgot to close for 24 days. The habit metrics (delegation, routing, prompt shape) are A's because they are written defaults, not discipline; the failure metrics are exactly where no default was guarding me. That is the whole thesis in one block, and it is why the grades are worth comparing: they point at your leak, not your virtue.

**Measurement note.** The script counts total input volume per session including cache reads, so its "session cost" runs higher than the grader's monthly averages in the table above - different instruments, each consistent with itself. Compare script output only with script output; the thresholds are printed in the source so you can argue with them.

The config side (statusline, pre-limit warning hook, the model-routing CLAUDE.md block, deny rules) lives in the [starter repo](https://github.com/tatarco/claude-code-starter) from part one.

### The one-line version

Stop asking what your cache ratio is. Ask what a finished session costs you in tokens, and watch that number month over month. Everything in part one is still how you lower it - part one just measured the wrong thing while doing the right things.

[claude-setup-audit](https://github.com/tatarco/claude-setup-audit) · [Part one: cache economics](/blog/cache-economics/) · [claude-code-starter](https://github.com/tatarco/claude-code-starter) · [LinkedIn](https://www.linkedin.com/in/galtidhar/)
