<!-- WhatsApp went silent for two weeks. The bug was mine. · Gal Tidhar — https://gal.tidhar.org.il/blog/whatsapp-presence/ -->

# WhatsApp went silent for two weeks. The bug was mine.

_WhatsApp · Baileys · Presence · Self-hosted_

**2026-08-28**  ·  ~7 min read  ·  by Gal Tidhar

WhatsApp on my iPhone stopped showing message notifications - no banner, no sound, locked or unlocked. Voice calls still rang fine. It lasted two weeks, I checked every setting Apple exposes, and I was one tap from deleting and reinstalling the app. The actual cause was **a bridge I had built myself**, quietly telling WhatsApp's servers I was online around the clock. The root cause underneath that was a one-line assumption bug in the open-source library the bridge runs on, which I've now filed upstream with a regression test.

## The symptom, and the dead ends

No notifications, at all, from WhatsApp. Not muted, not delayed - just absent. I went through Settings > Notifications > WhatsApp: every toggle on, Lock Screen ticked. Focus modes: off, and checked anyway. Per-chat mutes: none set. WhatsApp's own in-app "Reset Notification Settings": no change. Show Previews: on. Background App Refresh: on. Face ID & Passcode > Allow Access When Locked > Notification Center: allowed. I was one click from deleting the app and reinstalling it, which is usually where this kind of thing ends - a shrug and a fresh install that happens to fix it without ever explaining why.

The detail that stopped me: **voice calls kept ringing normally** the entire two weeks.

## The clue that actually mattered

Calls on WhatsApp arrive over CallKit, a separate VoIP push path that doesn't care about presence. If calls ring and messages don't, the network path to my phone is fine and the OS-level permissions are fine. Something else was telling WhatsApp that I was already reading my messages. WhatsApp suppresses push notifications to the phone whenever any linked device reports the account as online - if a device says you're already looking at the chat, there's no need to buzz your pocket.

I run a self-hosted, read-only WhatsApp bridge, linked as a device, built on [Baileys](https://github.com/WhiskeySockets/Baileys) (Node, version 7.0.0-rc14). That bridge was a linked device. That was the thread to pull.

## Root cause, part one: a default nobody unsets

My bridge calls `makeWASocket` without setting `markOnlineOnConnect`. Baileys defaults that option to `true` (`Defaults/index.js:62`), and on connect, `Socket/chats.js:1065` sends a presence update of `'available'`. So from the day I stood the bridge up, it had been announcing me online 24 hours a day. Setting `markOnlineOnConnect: false` restored notifications within seconds of restarting the bridge.

To be fair to the library: this is documented. The Baileys README says outright, "If you want to receive notifications in whatsapp app, set markOnlineOnConnect to false." The footgun here is the default value, not a missing page in the docs.

## Root cause, part two: the one that actually explains two weeks

That fix alone regresses. `Socket/socket.ts` announces the account's push name on every `creds.update` event:

`const name = update.me?.name
if (creds.me?.name !== name) {
 sendNode({ tag: 'presence', attrs: { name: name! } })
}`
 Three things stack up here. First, a partial credential update carries no `me` field at all, so `name` is `undefined` - and the comparison is true for any session that already has a stored push name, because `undefined` never equals a real string. The `name!` non-null assertion is exactly the assumption that fails. Second, `WABinary/encode.ts:226` strips undefined attributes during serialisation, so `attrs: { name: undefined }` goes out on the wire as a bare `` node with no attributes at all. Third, Baileys' own inbound presence reader, `Socket/chats.ts:885`, treats a presence node with no `type` attribute as `available` rather than as nothing (`attrs.type === 'unavailable' ? 'unavailable' : 'available'`).

Chain those together: a partial `creds.update` with no `me` field produces a bare presence node, and that bare node reads as "online." And `creds.update` fires constantly from ordinary key churn, including from `Socket/messages-recv.ts` on incoming traffic - so this fires again on every message received, even with `markOnlineOnConnect` set to `false`. The net effect: the account goes back online with every message it gets. I confirmed this is present in both the rc14 release my bridge runs and current `master`.

## The fix, and proving it

I forked the repo and added a one-line guard, dropping the now-unnecessary `name!` assertion along with it:

`if (typeof name === 'string' && name.length > 0 && creds.me?.name !== name) {`
 Then a regression test, `src/__tests__/binary/presence-on-creds-update.test.ts`, with three cases: a partial update carrying no `me` sends nothing (this one fails on unpatched `master`); an update with an unchanged push name sends nothing; a genuinely new push name is still announced, because that's a real behaviour change that should still fire. I verified this by stashing my own source fix and running the suite both ways: 1 failed / 2 passed without the fix, 3 passed with it. The full suite is 410 tests across 29 suites, all passing. `tsc --noEmit` is clean, eslint is clean on the changed file, and prettier reports it unchanged.

One thing worth flagging honestly rather than fixing quietly: the repo's existing `mockWebSocket()` helper, in `src/__tests__/TestUtils/session.ts`, calls `jest.mock` inside a function body - which is not hoisted, so under ESM it's currently a no-op. The existing test suite has been running against the real websocket client without anyone noticing. I left that alone for this PR to keep it to one behaviour change, and wrote the new test with `jest.unstable_mockModule` instead, which does work correctly under ESM.

## Upstream

The PR is [#2789](https://github.com/WhiskeySockets/Baileys/pull/2789), open, CI green. The underlying issue is [#2553](https://github.com/WhiskeySockets/Baileys/issues/2553), open since 12 May 2026. The exact same one-line guard was proposed earlier, in #2627, and closed by a stale-bot with state reason "completed" on 21 July - nothing was actually changed, and `master` still carries the bug today. The difference this time is the regression test: a fix with no test attached to a low-traffic issue is easy for a bot to file away as stale, whether or not it was ever applied.

## If you can't wait for the merge

A workaround that normalises the payload before the library's own listener sees it, using only the public event surface - no fork required:

`const _emit = sock.ev.emit.bind(sock.ev)
sock.ev.emit = (event, data) => {
 if (event === 'creds.update' && data && data.me === undefined && state.creds?.me) {
 return _emit(event, { ...data, me: state.creds.me })
 }
 return _emit(event, data)
}`

 What I would not do again
 
 **I didn't suspect my own linked devices for two weeks.** The symptom was account-wide, not device-specific, and I kept looking at iOS settings instead of asking what else was attached to the account.
 **I treated "the README documents it" as the end of the investigation instead of the start.** Finding `markOnlineOnConnect` in the docs felt like the answer. It was the first half of one.
 **I nearly stopped at the first fix that appeared to work.** `markOnlineOnConnect: false` silenced the symptom immediately, and if I hadn't kept watching, I would have shipped that as the fix and left the real bug - the bare presence node on every message - live in my own bridge and everyone else's.
 

 The actual point
 An always-on client attached to a live system is not an observer, it's a participant. I built a bridge to read WhatsApp, and the bridge changed how WhatsApp behaved toward me. The reason it took two weeks to find is the oldest reason there is: self-built infrastructure is the last place anyone looks.

### Links

[PR #2789: the fix + regression test](https://github.com/WhiskeySockets/Baileys/pull/2789) · [Issue #2553](https://github.com/WhiskeySockets/Baileys/issues/2553) · [The earlier, closed PR #2627](https://github.com/WhiskeySockets/Baileys/pull/2627) · [More about me](/)
