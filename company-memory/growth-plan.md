# Growth plan (G3)

Owner: Monetization agent (day-to-day, since 2026-11-22), worked out with the
CEO. First drafted 2026-11-23 (76th cycle), the second cycle of Monetization
ownership. Supersedes nothing — this is the first version of this file.
Keep it current: update the measured-results section every cycle, revise the
target/threshold when the evidence changes, and append rather than delete
history.

Binding limits on everything below (do not re-litigate per cycle, just obey):
GOVERNANCE.md → "Standing goals" (accuracy beats traffic; the "will not do"
list), "Who owns growth", and the homepage-layout constraint (owner,
2026-11-16: homepage stays title/subtitle/estimate/chart; growth content
goes on other pages, linked from the footer). No posting, accounts or
outward contact until the owner and CEO agree a posting persona. No spend
beyond the weekly ceiling (currently ~$0). No monetization work — dormant
until Phase 2 is approved.

## 1. Measured traffic (GoatCounter, hits not unique visitors)

**Updated 2026-11-26 (79th cycle).** Read directly, `GET /api/v0/stats/total`
etc., token present and working (confirmed via `/api/v0/me`).

- **Cumulative total: 176 hits over 2026-09-28 through 2026-11-26 (partial
  day, 0 hits so far; `total_utc` 176, same convention this time).** Up from
  175 at the last reading — the single +1 hit landed on 2026-11-25, which
  was still a partial-day 0 when last cycle read it. Re-read via the daily
  series directly: 2026-11-25 = 1, 2026-11-26 (today, partial) = 0.
- **The last four *complete* weeks are unchanged: 28, 23, 33, 29 —
  trailing-4-week total still 113.** Re-summed directly from the raw daily
  series this cycle, not carried forward unchecked: week of 2026-10-26
  (1+5+7+3+7+4+1=28), week of 2026-11-02 (2+2+2+6+4+5+2=23), week of
  2026-11-09 (1+8+6+3+6+3+6=33), week of 2026-11-16 (15+2+3+2+0+3+4=29). No
  new complete week exists yet — the week of 2026-11-23 closes 2026-11-29,
  still 3 days off.
- **The week of 2026-11-23 is now 4 of 7 days in (Mon-Thu): 25 hits so far
  (16 + 8 + 1 + 0)** — the 0 on Thursday (today, 2026-11-26) is a partial
  day, not a complete reading. Compared to every prior week's own first-4-day
  mark: week of 11-16 had 22 (15+2+3+2) by day 4, eventual 29; week of 11-09
  had 18, eventual 33; week of 11-02 had 12, eventual 23; week of 10-26 had
  16, eventual 28. This week's 25 is the highest 4-day mark of the five, but
  **the same single hot day (16 on Monday 2026-11-23) is still doing almost
  all of the lift**, exactly the pattern the week of 11-16 showed (a 15-hit
  Monday) before settling back into the 23-33 band by week's end at 29.
  **Read plainly: still too early to call this a break from the plateau** —
  three more days (Fri/Sat/Sun) remain before the week closes on 2026-11-29,
  and the one prior example of a hot start ended up ordinary. This is not a
  restatement of last cycle's framing: the underlying numbers moved (24 to
  25, one more complete day read: Wednesday closed at 1, not the 0 last
  cycle saw mid-day), and the comparison was re-run against four prior weeks
  rather than carried forward, but the conclusion is unchanged because the
  evidence that would change it (the week closing) has not yet arrived.
  - **Page breakdown, in-progress week (2026-11-23 through 2026-11-26):**
    `/` 20, `/history.html` 4, `/sources.html` 1, `/faq.html` 0 — still
    homepage-dominant, nothing unusual, FAQ still zero.
  - **Referrers, same window:** no-referrer 12, `www.bing.com` 4,
    `chatgpt.com` 4, `duckduckgo.com` 3. The `chatgpt.com` count is
    re-confirmed, day by day, to be the *identical* four hits already
    logged last cycle, all on 2026-11-24, none added since: 2026-11-23 = 0,
    2026-11-24 = 4, 2026-11-25 = 0, 2026-11-26 = 0 (so far). This is not a
    new or growing signal, just the same single-day event re-appearing in a
    wider window — re-checked explicitly rather than assumed carried over.
    Page breakdown for 2026-11-24 specifically, re-pulled this cycle: 7 to
    `/`, 1 to `/history.html` — identical to last cycle's finding, so the
    "doesn't trace to the rollup" conclusion stands on the same, not new,
    evidence.
- **Top pages, 2026-11-09 through 2026-11-26 (comparable window): `/` 75,
  `/history.html` 6, `/sources.html` 5, `/strait.html` 1.** `/faq.html`
  **still does not appear in the returned set at all** — a genuine zero, not
  a cutoff artifact (same check as before: `/strait.html` shows at 1 in the
  same window, so a path with ≥1 hit would show). `/history.html`'s count
  (6) is unchanged from last cycle's reading of the same comparable window
  (also 6) — one hit was added on 2026-11-25 but it went to `/` or
  elsewhere, not `/history.html` (confirmed by the per-day breakdown above).
- **Top referrers, same window:** no/empty referrer 30, `duckduckgo.com` 26
  (+1 vs last cycle's 25, traced to the single new hit on 2026-11-25),
  `www.bing.com` 14, `chatgpt.com` 7, "Yahoo" 3 — otherwise unchanged.
- **Top countries, same window:** identical to last cycle's reading (United
  States 37, Hungary 12, United Kingdom 9, Canada 7, South Korea 4, Vietnam
  3, Australia 2, Switzerland 2, Italy 2, then nine single hits) — the one
  new hit (2026-11-25, duckduckgo referrer) fell inside an already-counted
  country/bucket in this view, not a new country.

*(Prior reading, 2026-11-25/78th cycle, kept for the trail:)* Read directly,
`GET /api/v0/stats/total` etc., token present and working (confirmed via
`/api/v0/me`).

- **Cumulative total: 175 hits over 2026-09-28 through 2026-11-25 (partial
  day, 0 hits so far; `total_utc` 176 on the slightly different day-boundary
  convention).** Up from 167 at the last reading (through 2026-11-24
  partial) — +8 hits, all landing on 2026-11-24 (matches that day's own
  `stats/total` row exactly).
- **The last four *complete* weeks are unchanged: 28, 23, 33, 29 —
  trailing-4-week total still 113.** No new complete week has closed (the
  next one closes 2026-11-29); the week of 2026-11-16 re-confirmed at 29
  again this cycle from the raw daily series (15+2+3+2+0+3+4). The plateau
  reading from the last two cycles stands unchanged on the complete-week
  evidence — it has neither broken nor been confirmed to hold, because no
  new complete week exists yet to test it against.
- **The week of 2026-11-23 is in progress (3 of 7 days — Mon/Tue/Wed read):
  24 hits so far (16 + 8 + 0).** This is a hot start relative to most prior
  weeks' first three days (week of 11-09: 15 of its eventual 33; week of
  11-02: 6 of its eventual 23; week of 10-26: 13 of its eventual 28) but
  comparable in kind to the week of 11-16's own hot start (20 of its
  eventual 29) — that week opened hot on a single 15-hit day and then
  settled back down to a fairly ordinary 29 by week's end. **Read plainly:
  too early to call this either a break from the plateau or more of the
  same** — one busy day (16 hits on 2026-11-23, in the same range as
  11-16's 15-hit day) is doing almost all of the work, and the single
  prior example of a hot start (11-16) ended up inside the existing 23-33
  band once the week closed. The honest position is "wait for this week to
  close on 2026-11-29," not read a trend into 3 days.
  - **Where that hit data lands:** of the 24 hits so far this week, page
    breakdown for 2026-11-22 through 2026-11-25 (the surrounding window,
    28 hits, includes one extra day): `/` 21, `/history.html` 4,
    `/sources.html` 3, `/faq.html` 0 — still homepage-dominant, nothing
    unusual.
  - **Referrers, same window:** no-referrer 14, `www.bing.com` 5,
    `chatgpt.com` 4, `duckduckgo.com` 2. The `chatgpt.com` count (4) is
    concentrated entirely on 2026-11-24 (checked day-by-day: 0 on
    2026-11-22, 0 on 2026-11-23, 4 on 2026-11-24) — the single day the
    weekly rollup (§9/§10 below) went live. **Checked whether this traces
    to the rollup and it doesn't isolate that way**: of 2026-11-24's 8
    total hits, 7 went to `/` and only 1 to `/history.html` (where the
    rollup actually lives), so the chatgpt.com referrals that day
    overwhelmingly landed on the homepage, not the page the new content is
    on. Locations that day: Hungary 3, Italy 2, Canada/Finland/UK/US 1
    each — no new or AI-assistant-shaped geography. Read as ordinary
    variance in the chatgpt.com referrer bucket (7 in 16 days this cycle vs.
    3 in each of the last two cycles' same-length windows — within the
    range this bucket has shown before, not a step change), not a
    measured rollup effect. See §5a below for the full two-part review.
- **Top pages, 2026-11-09 through 2026-11-25 (16 days, the comparable
  window to prior cycles): `/` 74, `/history.html` 6, `/sources.html` 5,
  `/strait.html` 1, `/faq.html` 0.** Homepage still ~86% of traffic.
  `/faq.html` remains at **zero** hits in this window — explicit, not an
  artifact of the page being below a reporting cutoff (it would show as a
  listed path at 0 the same way `/strait.html` shows at 1; it simply isn't
  in the returned set at all because GoatCounter only lists paths with at
  least one hit).
- **Top referrers, same window:** no/empty referrer 30, `duckduckgo.com`
  25, `www.bing.com` 14, `chatgpt.com` 7, "Yahoo" 3. Broadly the same mix
  as last cycle, proportionally; absolute counts rose with the rise in
  total hits.
- **Top countries, same window:** United States 37, Hungary 12, United
  Kingdom 9, Canada 7, South Korea 4, Vietnam 3, Australia 2, Switzerland 2,
  Italy 2, then single hits from China, Finland, France, India, Iran,
  Japan, New Zealand, Romania, Thailand — **18 countries in 16 days**, up
  from 16 in the prior 16-day window. Continued real external reach, same
  trend as every prior cycle.

**One process note for the record, not a traffic-measurement concern:** this
cycle's CEO review found and fixed a CI bug that had left the live site
serving a stale `for_date` (2026-11-22) for about 3 days until just before
this reading. That does not affect these hit counts — GoatCounter counts
page loads regardless of what content the page served — but it means some
of the 2026-11-23/24 visitors referenced above may have seen a stale
headline figure rather than a current one. That is a data-freshness
finding, not a growth one; flagged here only so this plan's numbers aren't
read in isolation from it.

*(Prior reading, 2026-11-24/77th cycle, kept for the trail:)* Read directly,
`GET /api/v0/stats/total` etc., token present and working (confirmed via
`/api/v0/me`).

- **Cumulative total: 167 hits over 2026-09-28 through 2026-11-24 (partial
  day).** Up from 151 (through 2026-11-23 partial)/155 `total_utc` at the
  last reading (76th cycle, 2026-11-23) — +16 hits since then, almost all
  of it (16) landing on a single day, 2026-11-23, the day the FAQ page
  (`faq.html`, PR #48) went live.
- **Full-week series unchanged from last cycle for the last closed week**:
  the week of 2026-11-16 is still **29** (re-confirmed by re-summing the
  daily series: 15+2+3+2+0+3+4 = 29). The last four *complete* weeks are
  still 28, 23, 33, 29 — trailing-4-week total **113**, unchanged, since no
  new complete week has closed yet (the next one closes 2026-11-29).
- **The week of 2026-11-23 is in progress (1.3 of 7 days read): 16 hits so
  far** — all 16 on 2026-11-23 itself (11-24 shows 0 so far, very early in
  the day). This is the single busiest day since launch except 2026-11-16's
  15. **Checked for an FAQ-launch cause, found none isolable**: of the 16
  hits that day, 12 went to `/`, 3 to `/history.html`, 1 to `/sources.html`,
  and **0 to `/faq.html` itself**. Referrers for the surrounding 2026-11-22
  through 2026-11-24 window: 11 no-referrer, 5 `www.bing.com`, 1
  `duckduckgo.com` — no `chatgpt.com`, no new or unusual referrer. Countries
  that day: South Korea 4, United States 4, Hungary 3, Vietnam 3, China 1,
  Romania 1 — three countries (South Korea, China, Romania) not seen in any
  prior reading. **Read plainly: this looks like ordinary ongoing
  organic/crawler variance spread across new geographies, the same
  unexplained-spike pattern as 2026-11-16's 15-hit day, not a measurable
  FAQ effect** — the FAQ page itself has had zero visits in the ~1 day it
  has been live, which is the honest, expected reading at this stage, not a
  defect (see §5 below for the full FAQ review).
- **Top pages, 2026-11-09 through 2026-11-24 (16 days, the last full window
  read): `/` 67, `/sources.html` 5, `/history.html` 5, `/strait.html` 1,
  `/faq.html` 0.** Homepage remains ~86% of traffic.
- **Top referrers, same window:** no/empty referrer 27, `duckduckgo.com`
  24, `www.bing.com` 14, "Yahoo" 3, `chatgpt.com` 3. Search and
  AI-assistant-attributable share is similar to last cycle's reading;
  absolute referrer counts rose roughly with the rise in total hits, not
  disproportionately toward any one source.
- **Top countries, same window:** United States 36, Hungary 9, United
  Kingdom 8, Canada 6, South Korea 4 (new in the top list), Vietnam 3,
  Australia 2, Switzerland 2, then single hits from China, France, India,
  Iran, Japan, New Zealand, Romania, Thailand — 16 countries in 16 days,
  up from 13 in the prior 15-day window. Continued real external reach.

*(Prior reading, 2026-11-23/76th cycle, kept for the trail:)* Read directly
2026-11-23 (76th cycle), `GET /api/v0/stats/total` etc.,
token present and working (confirmed via `/api/v0/me`).

- **Cumulative total: 151 hits over 2026-09-28 through 2026-11-23
  (partial day; `total_utc` 155 on a slightly different day-boundary
  convention).** Up from 147 at the last reading (2026-11-22) — +4 hits in
  the latest ~24h, unremarkable day-to-day variance.
- **Full-week series (GoatCounter's own weekly rollup, Mon-anchored),
  reconstructed from the daily breakdown now that a new week has closed:**

  | Week starting | Hits |
  |---|---|
  | 2026-09-28 | 5 |
  | 2026-10-05 | 7 |
  | 2026-10-12 | 9 |
  | 2026-10-19 | 17 |
  | 2026-10-26 | 28 |
  | 2026-11-02 | 23 |
  | 2026-11-09 | 33 |
  | **2026-11-16 (now a complete week)** | **29** |

  **This is the first full-week reading that is a decrease, not flat or up.**
  `okrs.md`'s G3 revisit condition ("two more consecutive non-decreasing
  full-week totals at/above ~33") is **not met** — the week of 11-16 came in
  at 29, below 33, breaking the streak before a second confirming week was
  even reached. Read plainly: the last four full weeks (28, 23, 33, 29)
  oscillate in a band roughly 23-33 rather than climbing cleanly. This reads
  as **a plateau, not a reversal** — nothing here suggests traffic is
  trending down structurally, four points is not enough to call either a
  plateau or a stall with confidence, and the 2026-10-12 lesson about
  false-precision targets at low n still applies at these volumes. But it
  is also not the clean "still climbing" story the last two cycles reported,
  and this plan should say that plainly rather than carry the celebratory
  framing forward unexamined.

- **Top pages, 2026-11-09 through 2026-11-23 (15 days): `/` 55, `/sources.html`
  4, `/history.html` 2, `/strait.html` 1.** The homepage is still ~89% of
  all traffic; the content pages that exist get read by a small minority of
  visitors, not zero.
- **Top referrers, same 15-day window:** `duckduckgo.com` 23, no/empty
  referrer 18, `www.bing.com` 10, "Yahoo" 3, `chatgpt.com` 3. (58% is
  search-engine or AI-assistant attributable; the "no referrer" bucket is
  genuinely ambiguous — it covers direct navigation/bookmarks, privacy
  browsers that strip referrers, and some AI assistants that answer from a
  page without a click-through referrer, and GoatCounter cannot distinguish
  these from here.)
- **Top countries, same window:** United States 33, United Kingdom 8,
  Canada 6, Hungary 6, Vietnam 3, Australia 2, Switzerland 2, then single
  hits from France, India, Iran, Japan, New Zealand, Thailand. Thirteen
  countries in two weeks — still real external reach, not one browser.

**What this does and doesn't tell us.** Measured fact: discovery via search
engines (DuckDuckGo, Bing, a little Yahoo) and AI-assistant citation
(chatgpt.com) continues, spread across many countries, and the prior two
cycles' "no outward contact needed" causal story for the climb through
mid-November still holds — nothing changed there. Inference, not fact: why
the week of 11-16 dipped from 33 to 29. No specific cause is visible in the
referrer/page data (no single page or source collapsed); the most honest
reading is ordinary variance at a volume this small (a difference of 4 hits
across a week is easily one or two fewer good crawl/citation events, not a
trend). We should not invent a story for it, the same discipline this
company applied to the earlier climb.

## 2. Audience — who actually needs this, and why

Concrete, not generic. In descending order of how well the site currently
serves them:

1. **People searching "how much oil goes through the Strait of Hormuz"
   style queries right now** (general public, students, people reacting to
   Gulf security news) — want a quick, honestly-labelled number and enough
   context to know whether to trust it. This is most of our current
   traffic (homepage-dominant, DuckDuckGo/Bing-sourced) and the site serves
   it reasonably well already.
2. **AI assistants answering that same question on a user's behalf**
   (ChatGPT and similar, evidenced by the `chatgpt.com` referrer and
   plausibly some of the unattributed "no referrer" hits) — want a citable,
   clearly-sourced, clearly-labelled-as-an-estimate figure they can quote
   without passing along something that reads as a measurement. This is a
   real and distinct channel from human search, and content written in
   direct, quotable, honestly-hedged Q&A form serves it specifically well
   (see the FAQ proposal below).
3. **Journalists, policy researchers and Gulf-security-adjacent writers**
   who need an accessible number to cite instead of wading into EIA's own
   quarterly PDF supplement — served today by `sources.html`/`strait.html`,
   but there's no page shaped the way these people's "quick fact check"
   searches are typically phrased (short Q&A, not long prose).
4. **Oil-market-adjacent readers (traders, analysts, maritime-risk
   watchers)** who want a directional read on current Hormuz-specific flow
   between EIA's quarterly releases — the thinnest-served audience right
   now, since our honest answer to "is there a live number" is "no, this is
   a modelled estimate with a wide band," which is correct but means this
   audience's actual want (a validated, frequent, narrow-band number) isn't
   something we can honestly offer yet. Not a reason to oversell; a reason
   this audience stays small until the model itself narrows (G1's job, not
   G3's).

No audience here needs the page to claim more certainty than it has — the
corrective instinct ("just state a number more confidently") would serve
none of these groups better and would breach category 4. The highest-value,
lowest-risk growth lever is making the honestly-hedged content easier to
find and easier to quote, not making the figure sound more certain.

## 3. Channels

- **Organic search** (DuckDuckGo, Bing, residual Yahoo) — measured,
  working, the dominant channel. Google presence is unmeasured (no Search
  Console access; `backlog.md`).
- **AI-assistant citation** (ChatGPT confirmed; others plausible but
  unattributed) — measured at a small but real and recurring volume.
  Growing this means writing content assistants can quote cleanly and
  honestly: direct Q&A, explicit "this is a model estimate, not a
  measurement" framing repeated in the content itself (not just on one
  methodology page), stable URLs, structured data.
- **Direct/unattributed** — can't be attributed further from here; not a
  channel we can act on beyond continuing to be the kind of answer people
  bookmark or re-visit.
- **Outward/social/outreach** — explicitly not available until the owner
  and CEO agree a posting persona. Not a channel today.

## 4. Content ideas (homepage-layout-neutral; linked from the footer)

Already shipped (G4/G5, not re-proposing): sitemap + `<lastmod>`, canonical
URLs, OG/Twitter cards carrying the live estimate and range, JSON-LD
`Dataset`/`DataDownload` structured data, feed autodiscovery parity across
all five pages, estimate history page + JSON/CSV download + Atom feed, the
strait explainer, a live-generated share description.

**Not yet shipped — candidates for coming cycles:**

- **An FAQ page with `FAQPage` structured data** (this cycle's proposal,
  drafted in full below) — direct, quotable Q&A answering the exact
  phrasing people and AI assistants actually ask ("is this live data",
  "how is it calculated", "why a range not a number"), cross-linking the
  existing `sources.html`/`strait.html`/`history.html` content rather than
  duplicating it. No structured-data type on the site answers this query
  shape today.
- **A short "what changed this week" rollup** extending the existing daily
  change-note (G5) to a weekly cadence, on `history.html` — gives search
  engines and assistants a fresh, dated, quotable paragraph more often than
  the current per-day note alone, without a new page.
- **An explicit "ask it a question" framing on `sources.html`** pointing AI
  assistants at the FAQ and methodology content via clearer internal
  linking — cheap, no new content, just cross-links. Could fold into the
  FAQ page's launch instead of a separate action.
- **A plain-language "what the range means" callout reused verbatim across
  pages** (sources.html already has one; repeating the same honestly-worded
  sentence on strait.html and the FAQ makes it the thing that gets quoted,
  deliberately, since an honest sentence quoted widely is a feature, not a
  risk).

None of these touch the homepage. All are additive pages/sections linked
from the shared footer nav, matching the pattern `sources.html`/
`history.html`/`strait.html`/`terms.html` already use.

## 5. 76th cycle's growth-action: an FAQ page — SHIPPED, reviewed 77th cycle

**77th-cycle review (2026-11-24), one day after merge.** `faq.html` is live
(HTTP 200, independently re-checked), footer-linked on all five pages
(confirmed in the live `index.html` HTML, `<a href="faq.html">FAQ</a>`),
and listed in `sitemap.xml` (confirmed by direct fetch). Implementation
looks correct and complete — no defect found.

**Traffic verdict: no measurable effect yet, and explicitly too early to
expect one.** `/faq.html` shows **0 hits** in `stats/hits` for the
2026-11-09 through 2026-11-24 window, i.e. zero visits in the roughly one
day it has been live. The one notable traffic event since merge — a
16-hit day on 2026-11-23 — does not trace to the FAQ: none of those 16
hits went to `/faq.html`, the referrer mix shows nothing new or FAQ-shaped
(mostly no-referrer and Bing, no `chatgpt.com` uptick), and the day reads
as the same kind of unexplained organic/crawler variance this plan has
already seen (e.g. 2026-11-16's 15-hit day), not a FAQ-driven effect. This
is the expected, honest result at one day old — search engines and AI
assistants typically take days to weeks to crawl and surface a new page
even with a sitemap entry — and should not be read as the page
underperforming. **Re-check again next cycle(s)** once it has had a more
realistic window (1-2 full weeks) to be crawled.

**78th-cycle re-check (2026-11-25), ~2 days live: still 0 hits.** Re-read
directly — `/faq.html` does not appear at all in `stats/hits` for the
2026-11-09 through 2026-11-25 window (GoatCounter only lists paths with at
least 1 hit; `/strait.html` still shows at 1 in the same window, so this is
a genuine zero, not a reporting cutoff artifact). Still the expected,
honest reading at two days old, not a defect. **Re-check again once it has
had a full 1-2 weeks live** — same standard as last cycle, not stretched
into a finding either way yet.

**79th-cycle re-check (2026-11-26), ~3 days live: still 0 hits, independently
re-confirmed, not carried forward unread.** Re-pulled `stats/hits` fresh
this cycle for both the 17-day comparable window (2026-11-09 through
2026-11-26) and the narrower in-progress-week window (2026-11-23 through
2026-11-26) — `/faq.html` is absent from the returned path list in both,
while `/strait.html` (1 hit) and `/sources.html` (1-5 hits depending on
window) both show, so the absence is a genuine zero again, not a cutoff
artifact. Three days live is still well short of the 1-2 week window this
plan has consistently said it needs before reading an effect either way —
**no verdict change, and this is not a case for extending patience
indefinitely: the full-week mark lands 2026-11-30, four cycles from now at
the current ~daily cadence, which is the next natural re-check point.**

---

### Original proposal (76th cycle, for the record)

**What:** a new `faq.html`, linked from the footer nav on all five existing
pages (same list pattern: Sources & methodology / Estimate history / The
strait, explained / **FAQ** / Terms / Project repository), with `FAQPage`
JSON-LD structured data. Full copy draft below, ready for Build to
implement verbatim or adapt.

**Why this, now:** it is genuinely new (not a repeat of the sitemap/feed/OG
actions of the last three cycles), it targets a content shape — direct
Q&A — that nothing on the site currently offers and that both search
engines' "People also ask" boxes and AI-assistant citation specifically
favor, and it directly serves audience #2 and #3 above (AI assistants and
journalists/researchers) who are underserved by the existing long-prose
pages. It costs nothing, needs no new data, and every answer is either a
restatement of something already published (methodology, range, licence,
update cadence) or a plain "here's why not" — no new claim, no new number,
nothing that could narrow the band or overstate certainty.

**Expected effect:** a small, specific lift in (a) hits to a new page that
didn't exist before (comparable in kind to `/strait.html`'s 1 hit/15 days
or `/sources.html`'s 4/15 days — i.e., expect single digits, not a step
change in homepage traffic) and (b) possibly more AI-assistant citations
over a period of weeks, since direct Q&A is the shape these systems quote
most readily — this is a plausible mechanism, not a measured prediction.

**How it will be measured next cycle:** GoatCounter hits to `/faq.html`
specifically (new row in `stats/hits`), and whether `chatgpt.com`/other
assistant referrers or the unattributed "no-referrer" bucket move at all
over the following 1-2 full weeks. Given the volumes involved, a null
result (no visible change) is the likely honest outcome and should be
reported as such, not stretched into a finding.

**Draft copy** (for Build to implement; Monetization does not edit `site/`):

---

```html
<!-- faq.html — draft body content and suggested <head> additions -->

<!-- Suggested <title> -->
Frequently asked questions — Estimated oil flow through the Strait of Hormuz

<!-- Suggested meta description -->
Is the Hormuz oil-flow figure live data? How is it calculated, and why does
it carry a range? Answers to the most common questions about this site's
daily estimate and what it is not.

<!-- Suggested FAQPage JSON-LD (Build: wire real values, do not hand-type) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is the number on this site a live measurement?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "No. Nobody publishes a free, daily, direct measurement of oil flow through the Strait of Hormuz. The figure on this site is a model estimate, built from quarterly and monthly official data plus publicly reported signals, and it always carries an uncertainty range. It is never a substitute for a real measurement, and we say so on every page that shows it."
      }
    },
    {
      "@type": "Question",
      "name": "How is the estimate calculated?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "It starts from the most recent official quarterly figure (EIA's Global Energy Security Data), then adjusts between releases using higher-frequency signals we have cleared for use — see the full, specific method on our Sources & methodology page. We do not use satellite or tanker-tracking data; that is explicitly outside the model."
      }
    },
    {
      "@type": "Question",
      "name": "Why does the figure show a range instead of one precise number?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Because a single number would overstate how confident the model actually is. The range reflects how far the model's past estimates have been from the official figures once they were published, back-tested openly on our Sources & methodology page. The range is never narrowed to make the figure look more precise than the evidence supports, and it widens further whenever the model is extrapolating beyond the period it has been tested against."
      }
    },
    {
      "@type": "Question",
      "name": "How accurate has this estimate been?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "We score every past estimate against the official data once it is published and publish the result either way, including the misses — see our estimate history page for the full day-by-day record and our Sources & methodology page for how each quarter scored against the actual figure."
      }
    },
    {
      "@type": "Question",
      "name": "Where does the data behind the estimate come from?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Primarily the U.S. Energy Information Administration's quarterly Global Energy Security Data release, a U.S. government public-domain source, supplemented by other officially published statistics and publicly reported facts that we cite individually. Every input is listed, dated and sourced on our Sources & methodology page; nothing is used without checking its licence first."
      }
    },
    {
      "@type": "Question",
      "name": "How often does the figure update?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "The page refreshes daily. The underlying anchor data is quarterly, so most days' changes come from the model's own pacing adjustments rather than new official data — a new quarterly release, when one lands, is the biggest single move the figure makes."
      }
    },
    {
      "@type": "Question",
      "name": "Can I get this data as a feed or download?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes. Our own daily estimate history is available as JSON, CSV and an Atom feed from the Estimate history page — always our own modelled figures, never a re-hosting of a source we do not have redistribution rights to."
      }
    }
  ]
}
</script>
```

**Prose body (same seven questions, same answers, as readable HTML
headings/paragraphs rather than only JSON-LD — assistants and search
engines read both, and a human visitor needs the visible version)**:
structure as `<h2>` per question, `<p>` per answer, in the order above,
each answer linking out to the specific existing page it restates
(`sources.html#how`, `sources.html#range`, `history.html`), exactly matching
the JSON-LD text so the two never drift apart. Footer nav on all five
existing pages gains one more entry, `<a href="faq.html">FAQ</a>`, in the
same position/style as the existing links.

**Honesty check against the "will not do" list, run explicitly:** no
answer states the figure as a measurement; every answer either repeats or
points to the existing range/methodology language; no claim of live,
satellite, official or tanker-tracking data (the opposite — one answer
explicitly says we don't use it); no superlatives; nothing here could be
read as implying more certainty or authority than the rest of the site
already claims. This should pass rubric §3.2's "would a reader who sees
only that line believe something the band and methodology page do not
support" test on every answer, since every answer *is* the hedge, not a
headline competing with it. Flagging this explicitly rather than assuming
it: if the CEO's own rubric run disagrees on any individual answer, drop or
rewrite that answer, not the whole page.

## 5a. 77th cycle's growth action — a weekly "what changed this week" rollup on `history.html` — reviewed 78th cycle, still too fresh for a verdict

**78th-cycle review (2026-11-25), ~1 day after merge/deploy.** Implementation
verified correct and live: the `<!-- GENERATED:weekly_change_note -->` block
on `history.html` is present and rendering a real comparison (checked by
direct fetch of the live page), currently reading "Over the past week
(since 2026-11-17): The point estimate itself did not change, but the
published range moved... This is the band-gate... activating" — a real,
attributable, honestly-worded sentence drawn from the model's own recorded
fields, exactly as designed.

**Traffic verdict: no isolable effect, and explicitly too early to expect
one** — same discipline as the FAQ review at the same age. `/history.html`
shows 6 hits in the 16-day window ending 2026-11-25, against 5 in the
comparable window a cycle ago — one more hit, not a measurable lift, and
well within normal variance at this volume. The one notable nearby signal —
a `chatgpt.com` referrer spike of 4 hits concentrated entirely on
2026-11-24, the day the rollup went live — does not trace to the rollup
itself: of that day's 8 total hits, 7 went to `/` and only 1 to
`/history.html`, so the chatgpt.com referrals landed almost entirely on the
homepage, not the page carrying the new content. Read plainly: this is the
same kind of unattributable referrer variance this plan has already logged
for `chatgpt.com` (3/16 days, twice before) and for unexplained spike days
generally (2026-11-16's 15, 2026-11-23's 16) — not a rollup-driven effect.
**Re-check again once the page has had a more realistic window (1-2 full
weeks) to be crawled**, same standard applied to the FAQ page.

**79th-cycle re-check (2026-11-26), ~2 days live: still no isolable effect,
re-verified rather than assumed unchanged.** `/history.html` hits in the
comparable 17-day window (2026-11-09 through 2026-11-26): **6**, identical
to last cycle's 16-day reading (also 6) — the one new hit added to the
cumulative total this cycle (2026-11-25) went elsewhere, not to
`/history.html` (confirmed from the day-by-day page breakdown in §1). The
2026-11-24 `chatgpt.com` referrer spike (4 hits) is re-confirmed this cycle
to still be exactly those same 4 hits, all still dated 2026-11-24, none
added on 2026-11-25 or 2026-11-26 — not a growing signal, and the
page-breakdown re-check for that day (7 to `/`, 1 to `/history.html`) is
unchanged. Two days live is still short of the 1-2 week standard; the full
one-week mark for the rollup lands 2026-12-01. No verdict change.

## 6. Numeric G3 target — proposed

**Proposal: grow the trailing 4-week hits total from ~113 (28+23+33+29, the
last four full weeks) to at least 180 (≈45/week average) within 6 weeks,
i.e. by the week ending 2027-01-04.** That is roughly +60% over current,
deliberately modest given:

- the last four full weeks oscillate 23-33 rather than climbing cleanly —
  treating 33 as "the new normal" and demanding growth on top of it risks
  exactly the false-precision failure `okrs.md` has twice already named
  and avoided (2026-10-12, 2026-11-17);
- no outward contact is available to force the number up — everything in
  this plan is organic/findability-only, and that channel moves slowly;
- it is large enough to be a real signal if hit (not noise at this n), and
  specific enough that missing it is informative rather than dismissible.

**If missed:** that is useful information, not a failure to paper over —
it would mean organic/AI-assistant discovery alone, without outward
contact, has a ceiling somewhere in the 25-45/week range at this site's
current content depth, and the honest next conversation with the owner is
whether more content (cheap, slow) or outward contact (the owner's call,
currently withheld) is the actual unlock.

**If hit or exceeded:** reasonable to propose a second, larger target next,
rather than declaring victory — six weeks of data at these volumes is still
a short, noisy series.

The CEO sets the actual target recorded in `okrs.md`; this is Monetization's
proposal and reasoning, not the final number.

## 7. Phase 2 evaluation threshold — proposed, with assumptions shown

**Proposal: a Phase 2 evaluation becomes worth doing once GoatCounter shows
a trailing 4-week average of at least ~1,000 hits/week (≈4,300/month),
sustained for 4 consecutive weeks** — roughly **34x current traffic**
(current trailing-4-week average ≈28/week). This is deliberately a high,
conservative bar. Reasoning and assumptions, shown explicitly:

**Today's numbers, for scale.** At ~28-33 hits/week (~120-140/month), hits
are not unique visitors (per GOVERNANCE.md's own terminology rule) and the
true unique-visitor count is lower still. Any monetization approach
evaluated against today's traffic produces revenue estimates that round to
cents per month — not a basis for a serious proposal.

**Display ads.** Needs real ad-exchange scale to clear even a minimum
payout threshold, and niche informational sites typically see modest CPMs
(conservatively $2-4 RPM, i.e. revenue per 1,000 impressions; generously
up to $8 RPM for a finance/energy-adjacent niche — using the low end to
stay conservative). At the proposed threshold (≈4,300 hits/month, assuming
~1 ad impression per hit as an upper bound since hits include non-homepage
pages too): **4,300 ÷ 1,000 × $2-4 ≈ $9-17/month.** At today's
traffic (~130/month): **$0.26-0.52/month** — not worth the third-party
script, page-weight cost, or the honesty-bar risk of an ad that could blend
with the data (GOVERNANCE.md's own concern). Even at the proposed
threshold the number is small, which is the point: this is the floor where
it stops being obviously zero, not where it becomes a real income line.

**Affiliate.** No natural affiliate product exists for this content today
(there is no "buy this" step adjacent to a Hormuz flow estimate) — a
placeholder assumption only: even a generous 0.5% click-through to a
hypothetical relevant product and 5% of clicks converting at a $20 average
commission, at the proposed threshold (~4,300/month) would be
**4,300 × 0.005 × 0.05 × $20 ≈ $21/month.** This is the
weakest-fitting option for this site's content and traffic shape, flagged
as such, not recommended even at the threshold without a concrete product
fit found first.

**Sponsorship.** Doesn't scale directly with traffic the way ads do, but a
sponsor still needs a credible audience size to justify any outreach
(which stays the owner's call regardless). ~4,300 hits/month across ~13+
countries is a more credible pitch than ~130/month from mostly-unverified
sources; still thin for a maritime/insurance/energy-data sponsor, who would
reasonably want tens of thousands of monthly readers before paying real
money. No number attached here — it depends entirely on outward contact
that is not available, and is the most speculative of the four options.

**Paid tier / API access.** Scales differently from the others: revenue
depends on a handful of professional subscribers, not raw ad impressions,
so it needs *reach into the right niche*, not necessarily *volume*.
Conservatively, at the proposed threshold, assume 1% of monthly hits are
from genuinely professional/repeat visitors (≈43/month) and 5% of those
convert to a modest $15/month subscription: **43 × 0.05 × $15 ≈
$32/month.** This is the option that could plausibly outperform its
traffic-implied share, since it doesn't need display-ad-style scale — but
it is also the option most exposed to data-licence restrictions (several
of our tier-1 inputs are public-domain or non-commercial-use-cleared for a
free public site; a paid product changes that calculus and needs its own
licence re-check before anything is built, independent of the traffic
threshold).

**Why ~1,000/week and not lower or higher.** Below it, every option above
rounds to single-digit dollars a month — not worth the CEO's/Monetization's
evaluation time, let alone the honesty-bar and page-weight costs ads or
scripts would add. Materially above it (e.g. waiting for 10,000/week)
would mean giving up a real evaluation opportunity for a long time, given
current growth is slow and organic-only. ~1,000/week is the point where at
least one option (paid tier) plausibly clears "tens of dollars a month,"
which is still small in absolute terms but is the first point where the
numbers stop being uniformly negligible. **This is not a revenue forecast
and not a recommendation to monetize at that level — it is the point where
evaluating is worth the time, which GOVERNANCE.md is explicit is not the
same as approval.**

The CEO records the actual threshold in `okrs.md`; this is Monetization's
proposed number and the assumptions behind it.

## 8. Posting-persona options — for the owner to choose between, later

Not proposing any of these be used yet; no posting, account creation or
outward contact happens until the owner and CEO agree on one. Sketched
here only so that conversation has concrete options to react to when it
happens, per the owner's 2026-11-22 "persona is agreed after the plan"
sequencing.

1. **The project, speaking plainly as itself** — e.g. a account/handle named
   for the tracker ("Hormuz Oil Tracker" or similar), posting only factual,
   hedged updates ("today's estimate: X, range Y-Z — see methodology"),
   never commentary or opinion. Lowest risk of the three: easiest to keep
   inside the honesty bar because the account's entire identity is "the
   place that publishes this specific hedged number," so a hedge-dropping
   post would be obviously off-brand as well as a governance breach.
2. **The owner, personally, occasionally sharing it** — the owner's own
   existing voice/network, used occasionally rather than as a dedicated
   channel. Needs no new account, but ties the site's public honesty
   record directly to the owner's personal credibility, and needs the
   owner's own time/attention each time, which doesn't scale.
3. **A named-but-anonymous "maintainer" persona** (a human-sounding voice,
   not tied to the owner's real identity, explicitly presented as "built
   and run by one person as a side project") — can build some warmth/trust
   lacking in option 1, but adds the most new judgment calls (what tone,
   what to say about itself, consistency over time) and the most new
   things that could go wrong relative to the governance limits, for a
   channel that doesn't exist yet and whose value is unproven.

No recommendation between these yet — that is explicitly the owner's and
CEO's conversation once posting is actually being considered, not
something to pre-decide here.

## 9. Actions tried and their measured results (updated each cycle)

| Cycle | Action | Expected effect | Measured result |
|---|---|---|---|
| 71st (2026-11-20, pre-Monetization-ownership) | Sitemap `<lastmod>` dates (PR #43) | Possible crawl-frequency signal improvement | Inconclusive — no attributable effect isolable from a flat traffic day (per 74th-cycle review) |
| 74th (2026-11-21, pre-Monetization-ownership) | Feed-autodiscovery parity across all 5 pages (PR #44) | Marginal feed-reader/aggregator discoverability | Not yet reviewed for effect in a dedicated readout; folded into the general flat-to-29/week reading this cycle |
| 75th (2026-11-22, pre-Monetization-ownership) | Live-generated OG/Twitter share description (PR #46) | Any future share of a link shows the live estimate+range, not placeholder text | No shares have happened yet (no outward contact); no effect measurable until one does |
| 76th (2026-11-23, first Monetization-owned action) | FAQ page (`faq.html`, PR #48, shipped and deploy-verified live) | Small new-page hits; possibly more AI-assistant citation over weeks | **Re-checked 78th cycle (2026-11-25), ~2 days live: still 0 hits to `/faq.html`.** Implementation remains correct and live (HTTP 200, confirmed this cycle). Still too early for a traffic verdict, not a defect — re-check again once it has had 1-2 full weeks to be crawled. |
| 77th (2026-11-24) | Weekly "what changed this week" rollup on `history.html`, extending the existing daily change-note logic (G5) to a 7-day comparison | A second, differently-cadenced fresh dated paragraph for crawlers/assistants; plausible small effect on AI-assistant citation and return visits, not a measured prediction | **Reviewed 78th cycle (2026-11-25), ~1 day live: implementation verified correct and rendering a real comparison on the live page.** `/history.html` hits (6 in 16 days) essentially flat vs. the prior comparable window (5) — no measurable lift yet. A same-day `chatgpt.com` referrer spike (4 hits, all on 2026-11-24) does not trace to the rollup: 7 of that day's 8 hits went to `/`, only 1 to `/history.html`. Too early for a verdict; re-check again once it has had 1-2 full weeks to be crawled. See §5a. |
| 78th (2026-11-25) | **None proposed.** Both of the last two actions (FAQ, ~2 days live; weekly rollup, ~1 day live) are still too fresh to show any traffic effect — shipping a third change now would make it harder, not easier, to later tell which of three concurrent changes caused any future uptick. See §11. | — | — |
| 79th (2026-11-26, this cycle) | **None proposed.** Re-checked rather than restated: FAQ is now ~3 days live (still 0 hits, re-confirmed fresh this cycle), rollup ~2 days live (still no isolable lift, re-confirmed fresh this cycle). Both remain short of this plan's own 1-2 week standard; their full-week marks are 2026-11-30 and 2026-12-01 respectively. See §12. | — | — |
| 80th (2026-11-27, this cycle) | **None proposed.** FAQ now 4 days live (still 0 hits), rollup now 3 days live (still no isolable lift). Neither has reached its full-week mark (2026-11-30 / 2026-12-01). The in-progress week (2026-11-23) is now 5/7 days read, tracking above every prior week's own day-5 mark, but does not close until 2026-11-29. See §13. | — | — |

## 10. This cycle's (77th) growth-action proposal: a weekly change-note rollup on `history.html`

**What:** extend the existing daily "what changed and why" mechanism
(`build_change_note()` in `scripts/refresh_estimate.py`, G5, shipped PR
#22) with a second, weekly-grain comparison. Today's run already compares
the published point estimate to the previous day's; this adds a comparison
to the entry from 7 days prior (looked up from `history.json` by date),
using the exact same honesty rules already coded and tested in
`build_change_note()`:

- Only ever cite a cause already in `model['estimator']` (re-anchor, a
  revised transit-share ratio, or a new/revised GPCI production figure) or
  a structural state (extrapolated past the tested horizon, suppressed) —
  never news, geopolitics, or anything not already a cleared model input.
- Fall back to an honest neutral sentence when: there's no entry 7 days
  back yet (early in the series), either end is suppressed, the point is
  unchanged, or the recorded fields don't explain the move.
- Written into a new `<!-- GENERATED:weekly_change_note -->` marker on
  `history.html`, next to the existing daily `change-note` paragraph,
  computed and written on every daily refresh run (not a separate weekly
  cron) so it is always current the moment someone reads the page, exactly
  like the daily note.

**Suggested function shape** (for Build, reusing not duplicating logic):
a `build_weekly_change_note(est, model, history, for_date)` that finds the
`history.json` entry whose `for_date` is exactly 7 days before the current
`for_date` (falling back to "no comparison available" if absent, same as
`build_change_note()`'s `prev_entry is None` case), then calls the same
attribution logic `build_change_note()` already uses on that pair rather
than reimplementing it — ideally by factoring the shared
compare-two-entries logic out of `build_change_note()` into a helper both
functions call, so there is exactly one place that decides what counts as
an honest attributable cause.

**Why this, now:** it is the next idea already named in §4 above, not a
new one invented this cycle. It reuses tested, already-shipped logic
(lower implementation risk than a new content type), adds no new claim or
number (every sentence is a comparison of our own two already-published
figures), and gives search engines and AI assistants a second,
differently-cadenced fresh dated paragraph — plausibly useful for
"what's changed this week" / digest-style queries, a different query
shape than the daily note or the FAQ serve. It is also deliberately a
smaller, cheaper action than the FAQ page, appropriate while the FAQ's own
effect (if any) is still unknown — this is additive polish on existing,
working infrastructure, not a second big bet before the first one has had
time to show a result.

**Honesty check against the "will not do" list:** identical bar to the
existing daily note, since it's the same code path and same source fields
— no causal claim beyond what's in `model['estimator']`; a neutral
fallback sentence when attribution isn't honestly available; no estimate
is restated without being clearly the same already-published figure (not
a new number). Passes the same test the daily note already passes in
production.

**Expected effect:** a plausible small effect on AI-assistant citation and
return-visit value of `history.html` (currently ~5 hits/16 days) — not a
measured prediction, and likely too small to isolate on its own at this
site's traffic, same caveat as every prior findability action.

**How it will be measured next cycle:** `history.html`'s hit count in
`stats/hits`, and whether the page content (once live) correctly renders a
real weekly comparison once there's 7+ days of history to compare against
— the mechanism itself can be verified correct even before any traffic
signal exists, the same two-part check this cycle ran on the FAQ page
(implementation-correct vs. traffic-effect, kept separate).

**Nothing here needs outward contact, spend, or a governance judgment
call** — it's a code change inside an existing, already-approved
mechanism, $0, no new data source, no new page, homepage untouched.

## 11. 78th cycle (2026-11-25): no new growth action proposed this cycle

**Decision: ship nothing new for growth this cycle.** The last two actions
are both still live but unreviewable for a traffic effect:

- The FAQ page (`faq.html`, 76th cycle) is ~2 days live, still 0 hits (§5).
- The weekly change-note rollup (`history.html`, 77th cycle) is ~1 day
  live, implementation-correct but with no isolable traffic signal yet
  (§5a).

**Why "none" rather than a third action:** both of these need 1-2 more full
weeks before their effect (if any) can honestly be read, per this plan's
own stated standard (§5, §5a, and the FAQ's original proposal in §5's
"Original proposal" section). Shipping a third homepage-layout-neutral
change now, before either of the first two has shown a result, would not
speed up learning anything — at this site's traffic volume (single-digit
hits/day to any one non-homepage page), three concurrent un-aged changes
would make it *harder*, not easier, to attribute a future uptick to any one
of them, the same lesson this plan has already applied to not reading a
single hot day as a trend (§1). This is explicitly not "nothing to do" —
§4 still lists two more unshipped ideas (the `sources.html` "ask it a
question" cross-link, and the repeated "what the range means" callout)
that remain candidates for a future cycle once there is room to attribute
an effect to them individually.

**What happens instead this cycle:** continued measurement only — the
reading in §1, and the two reviews in §5/§5a. The current in-progress week
(2026-11-23, 24 hits in 3 days, §1) and the FAQ/rollup traffic verdicts
should all get a real read at the **next** cycle or two, once the week of
2026-11-23 closes (2026-11-29) and the FAQ/rollup have had closer to the
full 1-2 week crawl window this plan has consistently asked for before
calling either a result. If both are still flat at that point, that is
useful information about the ceiling of pure findability-content actions
at this site's current reach, not a reason to have shipped a third thing
sooner.

**Honesty/governance check:** no copy drafted, no page touched, no spend,
no outward contact — this section is a measurement-and-sequencing decision,
not a publish.

## 12. 79th cycle (2026-11-26): still no new growth action — re-verified against fresh numbers, not restated

**Decision: ship nothing new for growth this cycle, same call as 78th, but
re-derived from this cycle's own fresh GoatCounter reads, not carried
forward unchecked.** What actually changed since 78th cycle, checked
explicitly:

- Cumulative total 175 -> 176 (+1, landed 2026-11-25, a `duckduckgo.com`
  referral, unremarkable).
- Trailing 4-week total re-summed from the raw daily series directly this
  cycle (not assumed): still 113 (28+23+33+29), no new complete week yet.
- The in-progress week (2026-11-23) now has a fourth day read: 25 hits
  (16+8+1+0) vs last cycle's 24 (16+8+0, with Wednesday still partial at
  the time). Compared freshly against all four prior weeks' own 4-day
  marks (22, 18, 12, 16) — this week's 25 is the highest, but a single hot
  Monday is still carrying nearly two-thirds of it, the same shape the
  week of 11-16 showed before settling into the existing band. Three days
  remain before the week closes (2026-11-29).
- FAQ page: 3 days live now (was 2), re-checked fresh in both a 17-day and
  a 4-day window — still 0 hits, not inferred from last cycle's reading.
- Weekly rollup: 2 days live now (was 1), re-checked fresh — `/history.html`
  still flat (6 in the comparable window, unchanged), the one prior
  `chatgpt.com` referrer spike re-confirmed to still be the same 4 hits
  from 2026-11-24 with none added since.

**Why "none" again, not a restatement:** every number above was re-pulled
and re-compared this cycle, and every one of them still points the same
way the 78th cycle's did — both in-flight actions remain below this plan's
own stated 1-2 week standard for a traffic verdict (FAQ needs to 2026-11-30
for one full week live; the rollup to 2026-12-01), and the in-progress week
that would resolve "is the plateau breaking" does not close until
2026-11-29. Shipping a third homepage-layout-neutral change into this
window would still blur attribution for whichever of the first two (if
either) eventually shows an effect, which is the same reasoning §11 gave
and remains true on fresh evidence rather than stale repetition.

**What would change the call next cycle:** if the week of 2026-11-23 closes
2026-11-29 at or above 33 (breaking the 23-33 plateau band) or markedly
below it, that is new information the CEO should see plainly, independent
of what ships. If, at that point, the FAQ and rollup are also at or past
their full-week marks and both still show no measurable effect, the honest
next conversation is whether to ship one of the two remaining §4 ideas (the
`sources.html` "ask it a question" cross-link, or the repeated "what the
range means" callout) or to treat "pure findability content at this site's
current reach has a visible ceiling" as a real finding to bring to the
owner alongside the Phase 2 threshold conversation.

**Honesty/governance check:** no copy drafted, no page touched, no spend, no
outward contact — measurement and re-verification only.

## 13. 80th cycle (2026-11-27): still no new growth action — fresh reads, and the holding pattern is close to resolving but not resolved yet

**Decision: ship nothing new for growth this cycle.** Same call as 78th and
79th, re-derived from this cycle's own fresh GoatCounter reads (`/me` 404s —
a dead endpoint, not an auth failure; `stats/total`, `stats/hits` and
`stats/toprefs` all returned real data with the configured token, so the
read is live, not unmeasured).

**Fresh numbers this cycle:**

- **Cumulative total: 177 hits** over 2026-09-28 through 2026-11-27
  (`total`/`total_utc` both 177; today, 2026-11-27, is a partial day at 0
  so far). Up from 176 last cycle — the one new hit landed on 2026-11-26
  (closed at 1; the surrounding 2026-11-25–27 `toprefs` window shows only
  `duckduckgo.com` 1 and `html.duckduckgo.com` 1, consistent with the two
  hits recorded on 11-25 and 11-26, no new chatgpt.com entry).
- **Trailing 4-week total: still 113 (28+23+33+29).** No new complete week
  exists — the week of 2026-11-23 closes 2026-11-29, still 2 days off.
- **The in-progress week (2026-11-23) is now 5 of 7 days in: 26 hits
  (16+8+1+1+0)** — Thursday (2026-11-26) has now closed at 1 (was a
  partial 0 at last cycle's reading); Friday (today, 2026-11-27) is
  partial at 0. GoatCounter's own `weekly` rollup field on 2026-11-23's row
  independently confirms 26, matching the manual sum.
  - **Compared freshly against all four prior weeks' own day-5 marks**
    (re-derived from the full daily series, not carried forward): week of
    10-26 reached 23 by day 5 (eventual 28); week of 11-02 reached 16
    (eventual 23); week of 11-09 reached 24 (eventual 33); week of 11-16
    reached 22 (eventual 29). **This week's 26 is now the highest day-5
    mark of the five** — a new fact this cycle, not a restatement; last
    cycle's day-4 comparison already had this week ahead, and it has
    stayed ahead one day further in.
  - **Worth flagging, not yet a verdict: the concentration pattern is
    slightly different from prior hot-start weeks.** Monday (16) and
    Tuesday (8) together account for 24 of this week's 26 hits (92%).
    Tuesday's 8 ties the single highest Tuesday seen in any prior week
    (week of 11-09 also had an 8-hit Tuesday); no prior week had *both* an
    unusually hot Monday and an unusually hot Tuesday in the same week —
    week of 11-16's hot start was one 15-hit Monday followed by an
    ordinary 2-hit Tuesday. **This is a mild reason for slightly more
    attention than the single-hot-day pattern already logged twice before,
    but not a changed conclusion**: no referrer or page-breakdown anomaly
    explains it (see below), the week still has two days left
    (Sat/Sun 28-29), and the one clean prior example of a hot start
    (11-16) still ended up inside the existing band. If the remaining two
    days add a typical amount (the last-two-days addition in the four
    prior weeks ranged +5 to +9), this week would land roughly 31-35 —
    at or just above the top of the existing 23-33 band for the first
    time. **That arithmetic is a plausible range, not a prediction** — it
    assumes the remaining days behave like prior weeks' remaining days,
    which is exactly the kind of inference this plan has repeatedly
    declined to make before the data exists. **Flagging for the CEO per
    this cycle's brief, not burying it**: this is the first week where the
    day-5 trajectory plausibly points above the plateau's top end, but it
    is a progress read, not a result — it resolves one way or the other
    on 2026-11-29, two days from now.
  - **Page breakdown, in-progress week (2026-11-23 through 2026-11-27):**
    `/` 21, `/history.html` 4, `/sources.html` 1 — `/faq.html` absent
    (genuine zero; see below). Still homepage-dominant, nothing new in
    shape.
  - **Referrers, same window:** no-referrer 12, `www.bing.com` 4,
    `chatgpt.com` 4, `duckduckgo.com` 3, `html.duckduckgo.com` 1. The
    `chatgpt.com` count is re-confirmed, independently, to still be
    exactly the same 4 hits dated 2026-11-24 — the narrower 2026-11-25
    through 2026-11-27 `toprefs` read (above) shows zero `chatgpt.com`
    referrals in those three days. Not a growing signal, re-verified
    rather than assumed.
- **FAQ page (`faq.html`): still 0 hits, re-checked fresh, now ~4 days
  live.** Absent from the returned path list in both the 2026-11-09
  through 2026-11-27 window (18 days) and the narrower in-progress-week
  window — `/strait.html` shows 1 hit in the 18-day window, confirming the
  FAQ's absence is a genuine zero, not a reporting cutoff artifact, same
  check as every prior cycle. **Full one-week mark is 2026-11-30, 3 days
  from now.**
- **Weekly rollup on `history.html`: still flat, re-checked fresh, now ~3
  days live.** `/history.html` shows 6 hits in the 2026-11-09 through
  2026-11-27 (18-day) window — identical to the last two cycles' readings
  of the same page (6, 6) despite the window growing by two days; the one
  new hit added to the cumulative total since last cycle (2026-11-26) went
  elsewhere, not to `/history.html` (confirmed by the page breakdown
  above). The 2026-11-24 `chatgpt.com` referrer spike (4 hits) is
  re-confirmed to remain exactly those same 4 hits, none added since.
  **Full one-week mark is 2026-12-01, 4 days from now.**
- **Top countries, comparable 18-day window (2026-11-09 through
  2026-11-27):** United States 38 (+1 vs last cycle's 37), Hungary 12,
  United Kingdom 9, Canada 7, South Korea 4, Vietnam 3, Australia 2,
  Switzerland 2, Italy 2, then single hits — 18 countries, same list as
  last cycle; the one new hit fell inside an already-counted
  country/bucket.

**Why "none" again, and why this is the cycle to say the hold is close to
ending rather than open-ended:** every one of this plan's own stated
unlock conditions is now visibly close but **none has actually arrived**:
the in-progress week closes in 2 days (2026-11-29), the FAQ's full-week
mark is in 3 days (2026-11-30), the rollup's is in 4 days (2026-12-01).
Shipping a third homepage-layout-neutral change today, with all three
still open, would repeat exactly the attribution-blurring problem this
plan has declined three cycles running (§11, §12) — and would do so just
before the data that resolves all three arrives anyway. **The honest call
is to hold one more cycle, not indefinitely**: the next 1-2 cycles should
see all three conditions resolve within days of each other, which is the
natural, pre-committed point to decide whether to ship one of the two
remaining §4 ideas (the `sources.html` "ask it a question" cross-link, or
the repeated "what the range means" callout) — not a further extension of
patience past that point without a reason tied to fresh evidence.

**What would change the call next cycle:** if the week of 2026-11-23
closes 2026-11-29 at or above 33 (breaking the plateau's top end, which
this cycle's day-5 arithmetic makes plausible but not established) or
markedly below the 23-33 band, that is new information for the CEO,
independent of what ships. If, by the cycle after the week closes, the
FAQ and rollup have also reached their full-week marks and both still show
no measurable effect, that is the point to either ship one of the two
remaining §4 ideas or treat "pure findability content has a visible
ceiling at this site's current reach" as a real finding for the Phase 2
threshold conversation, per §12's framing (unchanged this cycle).

**Phase 2 evaluation threshold: no change.** The trailing 4-week average is
still ~28/week (113/4) against the proposed ~1,000/week threshold — nowhere
close. Nothing this cycle (including the day-5 trajectory flagged above)
moves that conversation; even the optimistic 31-35 scenario for the
in-progress week would still be two orders of magnitude below the
threshold. This cycle's reads are a growth-plateau/content-attribution
question, not a Phase 2 question.

**Honesty/governance check:** no copy drafted, no page touched, no spend,
no outward contact, no monetization work (no owner-approved Phase 2
decision exists in `decisions-log.md` as of this cycle) — measurement,
re-verification and sequencing judgment only.

## 14. 81st cycle (2026-11-28): hold continues — none of the three pre-committed unlock conditions has landed yet, confirmed on fresh reads

**Decision: ship nothing new for growth this cycle.** Same call as 78th
through 80th. All three pre-committed unlock conditions (in-progress week
closes 2026-11-29; FAQ full-week mark 2026-11-30; rollup full-week mark
2026-12-01) are 1-3 days out, not reached. GoatCounter read directly this
cycle with the configured token (`stats/total`, `stats/hits`, `stats/toprefs`,
`stats/locations` all returned real data).

**Fresh numbers this cycle:**

- **Cumulative total: 178 hits** over 2026-09-28 through 2026-11-28
  (`total`/`total_utc` both 178). Up from 177 last cycle — the one new hit
  closed on 2026-11-27 (Friday), which last cycle saw as a still-partial 0;
  it carried a `www.bing.com` referrer (confirmed in a narrow
  2026-11-25-to-11-28 `toprefs` read: `duckduckgo.com` 1, `html.duckduckgo.com`
  1, `www.bing.com` 1 — exactly the three single hits on 11-25/11-26/11-27,
  no new source, not a spike).
- **Trailing 4-week total: still 113 (28+23+33+29).** No new complete week
  yet — the week of 2026-11-23 closes tomorrow, 2026-11-29.
- **The in-progress week (2026-11-23) now has all five weekdays closed:
  27 hits through day 5 (16+8+1+1+1)** — Friday (2026-11-27), partial at 0
  last cycle, has now closed at 1. Day 6 (Saturday, today, 2026-11-28) is
  partial at 0 so far, as expected for a day still in progress (re-derived
  from the full daily series via `stats/total`, not assumed: 2026-11-23
  through 2026-11-28 = 16, 8, 1, 1, 1, 0).
  - **Day-5-closed comparison against all four prior weeks' own day-5
    closed marks**, recomputed from the raw series this cycle: week of
    10-26 = 23 (eventual 28); week of 11-02 = 16 (eventual 23); week of
    11-09 = 24 (eventual 33); week of 11-16 = 22 (eventual 29). **This
    week's 27 is now the highest day-5 mark of the five, on a fully closed
    day-5 figure rather than last cycle's partial-day read of 26** — the
    trajectory flagged last cycle as "plausibly above the plateau" has
    held one more day, on firmer footing (closed days, not a partial one).
  - **Days 6-7 addition in the four prior weeks, recomputed directly**:
    10-26 added +5 (day6 4, day7 1) to reach 28; 11-02 added +7 (5+2) to
    reach 23; 11-09 added +9 (3+6) to reach 33; 11-16 added +7 (3+4) to
    reach 29. Range +5 to +9, average ~+7. Applied to this week's closed
    day-5 figure of 27 (not a prediction, the same bounding arithmetic as
    last cycle, now anchored to a closed number): a plausible eventual
    range of **32-36**, which would put this week at or above the top of
    the existing 23-33 band. Day 6 (today) reading 0 so far is not
    informative yet — every one of the four prior weeks' day-6 figures
    (4, 5, 3, 3) came from a day that, read mid-day, would also have shown
    a partial low number; this is the same partial-day-undercount pattern
    already flagged repeatedly in this plan, not a new finding.
  - **Referrers, in-progress week (2026-11-23 through 2026-11-28, whole
    week to date):** no-referrer 12, `www.bing.com` 5, `chatgpt.com` 4,
    `duckduckgo.com` 3, `html.duckduckgo.com` 1. The `chatgpt.com` count is
    re-confirmed still exactly the same 4 hits dated 2026-11-24 — the
    narrower 2026-11-25-to-11-28 window shows zero `chatgpt.com` referrals.
    `www.bing.com` ticked from 4 to 5 (the new 2026-11-27 hit), not a
    spike.
  - **Page breakdown, cumulative (since 2026-09-28): `/` 164,
    `/history.html` 8, `/sources.html` 5, `/strait.html` 1 — total 178.**
    `/faq.html` is absent from the full path list entirely, confirming it
    remains a genuine zero (see below), not a reporting artefact.
- **FAQ page (`faq.html`): still 0 hits, re-checked fresh, now ~5 days
  live.** Absent from both the full-cumulative path list (178 hits across
  only 4 paths, above) and a 19-day window (2026-11-09 through 2026-11-28:
  `/` 77, `/history.html` 6, `/sources.html` 5, `/strait.html` 1, total 89
  — no `/faq.html` row). **Full one-week mark is 2026-11-30, 2 days from
  now — still not reached.**
- **Weekly rollup on `history.html`: still flat, re-checked fresh, now ~4
  days live.** `/history.html` shows 6 hits in the 2026-11-09 through
  2026-11-28 (19-day) window — identical to the last three cycles' reads
  of the same page (6, 6, 6) despite the window growing by a day each
  time; the one new cumulative hit since last cycle (the 2026-11-27 bing
  referral) went to `/` , not to `/history.html` (confirmed by the
  cumulative page breakdown above). **Full one-week mark is 2026-12-01, 3
  days from now — still not reached.**
- **Top countries, 19-day window (2026-11-09 through 2026-11-28):**
  identical list and counts to last cycle's 18-day read — United States
  38, Hungary 12, United Kingdom 9, Canada 7, South Korea 4, Vietnam 3,
  Australia 2, Switzerland 2, Italy 2, then 10 more single-hit countries,
  18 countries total, unchanged. The window grew by a day but today
  (2026-11-28) is still a partial day with 0 hits recorded so far, so no
  new country entries — consistent, not a stall.

**Why "none" again, confirmed rather than carried forward:** every one of
this plan's own three pre-committed unlock conditions is checked fresh
this cycle and **none has arrived**: the in-progress week closes tomorrow
(2026-11-29), the FAQ's full-week mark is in 2 days (2026-11-30), the
rollup's is in 3 days (2026-12-01). Nothing this cycle changes that
timing or those conditions — the brief for this cycle asked explicitly
whether anything had shifted the requirements, and nothing has: the three
conditions are exactly as set in §12/§13, re-verified, not re-defined.
Shipping a third homepage-layout-neutral change today, one cycle before
all three resolve, would repeat the same attribution-blurring problem
this plan has now declined four cycles running (§11-§13). **This is a
confirmed hold, not a new judgment call** — the decision point itself
(ship one of the two remaining §4 ideas, or record a flat FAQ/rollup
result as a real finding about the ceiling of pure findability content at
current reach) is the CEO's and owner's to make together with
Monetization once the three marks land, not Monetization's to pre-empt.
Flagging this plainly per this cycle's brief rather than deciding
unilaterally: **the decision point has not arrived, but it is very close
— the next cycle (on or after 2026-11-29) is the first one where it
plausibly can.**

**What would change the call next cycle:** if the week of 2026-11-23
closes 2026-11-29 at or above 33 (breaking the plateau's top end — this
cycle's day-5-closed arithmetic puts a plausible eventual range of 32-36,
slightly firmer than last cycle's partial-day-based 31-35) or markedly
below the 23-33 band, that is new information for the CEO independent of
what ships. Once the week is closed and, in the cycle after that, the FAQ
and rollup have also reached their full-week marks with both still
showing no measurable effect, that is the point to either ship one of the
two remaining §4 ideas (the `sources.html` "ask it a question" cross-link,
or the repeated "what the range means" callout) or treat "pure
findability content has a visible ceiling at this site's current reach"
as a real finding for the Phase 2 threshold conversation, per §12's
framing (unchanged this cycle).

**Phase 2 evaluation threshold: no change.** The trailing 4-week average is
still ~28/week (113/4) against the proposed ~1,000/week threshold —
nowhere close. This cycle's numbers (including the firmer 32-36 eventual
range for the in-progress week) do not move that conversation; even the
upper end of that range is still two orders of magnitude below the
threshold. This cycle's reads remain a growth-plateau/content-attribution
question, not a Phase 2 question.

**Honesty/governance check:** no copy drafted, no page touched, no spend,
no outward contact, no monetization work (no owner-approved Phase 2
decision exists in `decisions-log.md` as of this cycle, re-checked this
cycle) — measurement, re-verification and sequencing judgment only.
