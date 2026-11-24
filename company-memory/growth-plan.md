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

**Updated 2026-11-24 (77th cycle).** Read directly, `GET /api/v0/stats/total`
etc., token present and working (confirmed via `/api/v0/me`).

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
| 76th (2026-11-23, first Monetization-owned action) | FAQ page (`faq.html`, PR #48, shipped and deploy-verified live) | Small new-page hits; possibly more AI-assistant citation over weeks | **Reviewed 77th cycle (2026-11-24), ~1 day live: 0 hits to `/faq.html` so far.** Implementation verified correct (live, footer-linked, in sitemap) — too early for a traffic verdict, not a defect. The one nearby traffic spike (16 hits, 2026-11-23) does not trace to the FAQ (0 of those hits went to `/faq.html`; no new/FAQ-shaped referrer). Re-check again once the page has had 1-2 full weeks to be crawled. |
| 77th (2026-11-24, this cycle) | Weekly "what changed this week" rollup on `history.html`, extending the existing daily change-note logic (G5) to a 7-day comparison (drafted below) | A second, differently-cadenced fresh dated paragraph for crawlers/assistants; plausible small effect on AI-assistant citation and return visits, not a measured prediction | To be reviewed next cycle once Build implements and it has been live at least a few days |

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
