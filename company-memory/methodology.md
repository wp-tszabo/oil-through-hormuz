# Daily Best-Guess Estimation Methodology — design v1

> **2026-09-23: the estimator has been replaced and the replacement is LIVE. Read
> §19 first.** Persistence (§3) was replaced by the GPCI transit-share estimator
> ("option C", critical issue #9). **PR #11 was merged by the CEO on 2026-09-23
> (`2d98638`) under its new publishing authority** (GOVERNANCE.md → "Publishing
> authority"). The deploy was verified live: 5.6, range 4.9–10.8.
> Methodology decisions are now the CEO's under GOVERNANCE.md → "Methodology
> authority" (owner grant, 2026-09-23).

**Status**: ACTIVE — the publication question in §6 was **decided by the owner
on 2026-09-17** (see §10). The model's daily estimate is now the site's
headline figure, labelled as an estimate and shown with its band. §6 records
the CEO's original recommendation and is retained for the record; **§10
supersedes it.**

**Directed by**: owner, 2026-09-17 (see `decisions-log.md`) — "build a daily
best-guess estimation methodology rather than waiting for a true daily
source."

**Written by**: CEO (the Agent/subagent tool was unavailable for a third
consecutive cycle, so Research could not be dispatched; see §8).

**Governing constraints**: `rubric.md` §1.6 — a modeled figure may only
publish if its methodology is published and linked, **all** its inputs are
independently licence-cleared, and it carries a visible uncertainty range
rather than a falsely precise single number.

---

## 1. What this model is for

Produce, for any given day, a best estimate of the volume of crude oil,
condensate and petroleum products transiting the Strait of Hormuz, expressed
in million barrels per day (m b/d), using only inputs the company is legally
permitted to republish — and state honestly how uncertain that estimate is.

## 2. Input inventory: what is actually available

### 2.1 Cleared — usable

| Input | What it gives | Cadence | Lag | Licence |
|---|---|---|---|---|
| **EIA Global Energy Security Data** (`eia.gov/outlooks/steo/report/energysecurity/article.php`), Table 4 | Hormuz total oil, crude+condensate, products, and LNG, by quarter | **Quarterly** | ~6 weeks after quarter end | US federal public domain — free to use and distribute, attribution requested |
| EIA Short-Term Energy Outlook (parent publication) | Middle East production/forecast context | Monthly | ~1 week | Same |
| EIA World Oil Transit Chokepoints table | Hormuz annual 2020–2024 + 1H25 | Annual | long | Same |

**This is a significant correction to what company memory previously
recorded.** Two earlier cycles concluded EIA's only Hormuz output was the
annual chokepoints table, freshest figure 1H25 (20.9 m b/d), ~14 months
stale. That was wrong. EIA launched the **Global Energy Security Data**
release on 2026-05-13 specifically to publish chokepoint flows quarterly. The
current release (2026-08-12) carries data through **2Q26**. The free tier is
far better than this company believed: the real lag is roughly **6–10 weeks**,
not 14 months.

*Care with the release date*: the Global Energy Security Data supplement
carries its own release date (2026-08-12) and is **not** on the same schedule
as its parent Short-Term Energy Outlook (released 2026-09-09, next 2026-10-06).
A first draft of this document and of the homepage copy wrongly quoted the
STEO's next-release date as the Hormuz data's. EIA does not publish a specific
next-release date for the supplement, so Build must **derive staleness from the
supplement's own release date and the coverage period of the latest row**, and
copy must not assert a next-release date we have not seen EIA state.

Cleared series as published on 2026-08-12 (m b/d):

| | 1Q25 | 2Q25 | 3Q25 | 4Q25 | 1Q26 | 2Q26 |
|---|---|---|---|---|---|---|
| Total oil | 20.9 | 21.0 | 21.3 | 21.6 | 14.9 | **4.9** |
| Crude oil & condensate | 14.8 | 14.9 | 15.0 | 15.9 | 10.9 | 3.7 |
| Petroleum products | 6.2 | 6.2 | 6.3 | 5.7 | 4.0 | 1.1 |
| LNG (bcf/d) | 11.7 | 11.0 | 10.9 | 10.5 | 7.4 | 0.8 |

### 2.2 Rejected — must not be used, including as a hidden model input

| Input | Why rejected |
|---|---|
| **IMF PortWatch** (daily, AIS-derived) | Licence. `license: custom` → IMF terms forbidding systematic downloading, redistribution, compilation and derivative works. Verified 2026-09-17. Rejected regardless of how useful it would be. |
| **WTO Strait of Hormuz Trade Tracker** (`datalab.wto.org`, daily, AIS-derived) | **New candidate found and rejected this cycle.** Daily cadence, exactly the shape we want — but the underlying data is **AXSMarine (Signal Group)**, a commercial vendor, surfaced under "© WTO 2026" with no open-data grant and a "contact AXSMarine for data terms" pointer. Commercial vendor data behind an unstated licence is a no under GOVERNANCE.md's guilty-until-checked rule. Not ingested, not used for calibration. |
| **IEA** commentary and market reports | Restrictive licence; not republishable. |
| Any AIS/tanker-tracking feed (Vortexa, Kpler, Lloyd's List, AISHub) | Commercial and/or membership-restricted. Note EIA's Hormuz numbers are *derived from* Vortexa — we republish **EIA's analysis** with attribution to EIA, and must never imply we hold or license Vortexa data. |

**Rule restated because it is the easy one to break:** an uncleared source may
not be used "just to calibrate" or "just to sanity-check" a published number.
If it moves the number, it is an input, and it needs a licence.

### 2.3 The gap, stated plainly

**There is no licence-cleared source of daily-resolution Hormuz flow data.**
Every daily source found (PortWatch, WTO/AXSMarine) is legally closed to us.
The best cleared resolution is a **quarterly average**.

Therefore any daily figure this company publishes is not a measurement and
not an interpolation between daily observations — it is a model *inventing*
within-quarter shape it cannot observe. That is legitimate if and only if the
uncertainty is shown honestly. §5 and §6 are about whether it currently is.

## 3. Model structure

Let `Q_last` = most recent EIA-published quarterly total, `t_end` = the last
day of that quarter, `d` = the day being estimated.

```
estimate(d) = Q_last × shape(d)        [the point estimate]
band(d)     = estimate(d) × [1 − lo(d), 1 + hi(d)]
```

- **Anchor** `Q_last`: the EIA figure. Never modeled, always a real published
  number, always displayed alongside the estimate with its coverage period.
- **Shape function** `shape(d)`: the within/beyond-quarter adjustment. With no
  cleared higher-frequency input, `shape(d) = 1` — persistence. We do not
  have the information to justify anything more elaborate, and a more
  elaborate curve would be false precision dressed as sophistication.
- **Band** `lo/hi`: empirically derived in §4, widening with `d − t_end`.
- **Recalibration**: on each EIA supplement release, `Q_last` and
  `t_end` are replaced, the prior estimate is scored against the new actual,
  and that error is appended to the backtest in §4. The band is re-derived
  from the updated error record. This is the part that makes the model
  honest over time rather than just at launch.

## 4. Backtest — what persistence would actually have got wrong

Predicting each quarter from the one before, using only the cleared series:

| Target | Predicted (prior qtr) | Actual | Error vs actual |
|---|---|---|---|
| 2Q25 | 20.9 | 21.0 | −0.5% |
| 3Q25 | 21.0 | 21.3 | −1.4% |
| 4Q25 | 21.3 | 21.6 | −1.4% |
| 1Q26 | 21.6 | 14.9 | **+45%** |
| 2Q26 | 14.9 | 4.9 | **+204%** |

Two regimes, and they are not close to each other:

- **Stable regime** (through 4Q25): persistence is excellent, max error 1.4%.
  A ±3% band (≈2× worst observed error) would be defensible and useful.
- **Disrupted regime** (1Q26 onward): persistence overestimates by 45%, then
  by 204%. A band wide enough to have contained 2Q26 would have to run from
  roughly −70% to +40% of the anchor — on today's 4.9 anchor, that is
  **"somewhere between about 1.5 and 7 m b/d."**

A second, independent reason for caution: EIA itself states that *"since the
end of February 2026, AIS signal data for ships transiting the Strait of
Hormuz have become especially unreliable. For 2026 Hormuz volumes, tanker
tracking data are being revised frequently."* The anchor itself is provisional
— the 1Q26 figure has already moved (14.6 → 14.9 between releases). So in the
current regime we have a wide model band *around a moving anchor*.

## 5. Regime detection

The model must know which regime it is in, because publishing a ±3% band
during a disruption would be the worst failure available to us.

Cleared, mechanical test — no judgement call, no uncleared inputs:

- **Disrupted** if the latest quarter-on-quarter change in the cleared series
  exceeds ±10%, or if fewer than two consecutive quarters have been within
  ±10%. Otherwise **stable**.
- Current state: 21.6 → 14.9 → 4.9. **Disrupted**, unambiguously.

Regime is displayed to the reader, not just used internally.

## 6. The publication question — for the owner, not the CEO

> **SUPERSEDED 2026-09-17 by the owner's decision in §10.** Kept unedited
> because it is the argument the owner overruled, and hiding it would make the
> record useless. The recommendation below is no longer what the site does.

The model above is buildable today. The question is whether its **output is
publishable today**, and the honest answer is:

- **The trend chart: yes.** Six quarters of cleared, attributable, real EIA
  data. Genuinely informative, and it shows the collapse clearly. Publish it.
- **The latest measured figure (4.9 m b/d, 2Q26): yes**, provided it is
  labelled with its coverage period and its provisional status.
- **A daily headline number for "yesterday": no, not yet.** In the current
  disrupted regime the honest band (≈1.5–7 m b/d) is wider than the quantity
  being estimated. A single number at that uncertainty is not a best guess,
  it is a guess wearing a number's clothing — and putting it under a headline
  reading "the amount of oil that passed through the Strait of Hormuz
  yesterday" would tell the reader it was measured, when nothing we are
  allowed to republish measured it. That is rubric §1.4 and §3.2, and it is
  GOVERNANCE.md critical-issue category 4 (misrepresenting the data's
  authority). The CEO will not publish that on its own authority.

**Recommendation**: ship the honest version now (latest measured quarter +
trend + explicit "no one we may republish measures this daily"), and switch
the headline to a modeled daily estimate **with its band** when the regime
detector returns to stable, where the band is ±3% and the number is worth
something. If the owner wants a daily figure on the page before then, it
should be shown as a **range**, not a number, and the CEO needs that decision
explicitly.

## 7. What would actually close the gap

In rough order of cost:

1. **Wait for regime stabilisation** — $0. The model becomes genuinely good
   the moment flows are boring again.
2. **A daily cleared input.** None exists free today. Asking the IMF for
   written PortWatch permission is still $0 and still unsent (owner's call) —
   but note it has become *less* attractive this cycle, because PortWatch is
   raw-AIS-derived and EIA has documented that Hormuz AIS is unreliable
   precisely now. We would be paying a licence negotiation to obtain a daily
   number that is itself systematically understated during a disruption.
3. **Paid tanker-tracking data** (Phase 2). Only justifiable after 1 and 2,
   and not proposed here.

## 8. Provenance of this document

Written by the CEO, not by the Research specialist, because the Agent tool
was unavailable for a third consecutive cycle. It therefore has **no
independent review** — the same agent found the sources, cleared the
licences, built the model and judged it publishable-or-not. That is a real
weakness in a document whose whole job is to decide what is honest to
publish, and it is recorded here rather than left implicit.

## 9. Attribution string for any published figure

> Source: U.S. Energy Information Administration, Global Energy Security
> Data, released 12 August 2026. EIA volumes are based on Vortexa tanker
> tracking data with additional EIA analysis.

## 10. Owner decision, 2026-09-17 — the daily estimate is the headline

The CEO escalated §6 rather than deciding it (critical issue #5, PR #4). The
owner answered on PR #4 (comment `5716791659`, 2026-09-17T15:16:58Z):

> "The daily figure is the estimate. That is the real value of the whole page
> thta we develop a model that make that estimate. So let's add 'estimated '
> keyword to the title but let's keep the daily figure"

**Decision, as implemented:** the model's daily point estimate is the headline
number; the title and the figure are explicitly labelled as an estimate; the
band is shown next to the number, not buried in the methodology.

This resolves §6's question in favour of publishing. It does **not** waive
`rubric.md` §1.6, which the owner has not been asked to and should not have to
waive: a modelled figure publishes only with its methodology linked, all inputs
licence-cleared, and **a visible uncertainty range**. So the page shows both —
the point estimate the owner asked for *and* the range the rubric requires,
with the copy telling the reader to treat the range as the answer. The two
requirements are compatible; only "a bare number with no range" would have been
in conflict, and that is not what shipped.

**Published parameters as of 2026-09-17:**

| Field | Value |
|---|---|
| Estimate date | 2026-09-16 |
| Point estimate | 4.9 m b/d |
| Band | 1.5 – 6.9 m b/d |
| Band derivation | −70% / +40% of anchor (disrupted-regime back-test, §4), applied to 4.9, rounded to 1 d.p. |
| Anchor | 2Q26 = 4.9 m b/d, EIA release 2026-08-12 |
| Shape function | persistence, `shape(d) = 1` (§3) |
| Regime | disrupted (§5) |

**Consequence the owner should know about — see also §11:** the page now carries a *dated*
figure, so it goes stale by construction — a page still reading "16 September
2026" a week later is stale data under GOVERNANCE.md category 1, even though
every word on it is true. Until the refresh is automated, the estimate date is
hand-maintained in `site/data/hormuz.json`. Automating it is now the top Build
item; because `shape(d) = 1`, the daily job only has to re-date the estimate,
widen the band with distance from the anchor, and re-anchor when EIA publishes.

## 11. Standing mandate, 2026-09-17 — the method is the product, and the CEO owns improving it

This section is **standing**, not a cycle note. It is the reason the rest of
this document exists.

Owner, 2026-09-17:

> "The whole purpose of the site is to develop a proprietary method for
> calculating/estimating the flow by aggregating different data sources, news,
> reports, etc... It is the CEO's responsibility to keep improving this
> proprietary methodology."

### What this changes

The company's product is no longer "republish the freshest cleared number with
a model on top". It is **the estimation method itself**, and the method is
expected to get better over time by widening what feeds it. The CEO owns that
improvement — it is not a backlog item that can be completed and closed.

Concretely, every cycle the CEO must do one of three things and record which:

1. **Add a cleared input** to the model, and re-derive the band with it in.
2. **Improve the model or its calibration** without a new input — e.g. a better
   shape function, a better regime detector, a scored recalibration against a
   newly published quarter.
3. **Record a specific, evidenced reason neither was possible this cycle.**
   Silence is not an acceptable third option. "Nothing found" is only
   acceptable with the list of what was checked and why each failed.

Tracked as `okrs.md` Phase 1 **KR6**.

### The bar a new input must clear — unchanged, and restated here on purpose

A mandate to add inputs is exactly the pressure under which a licence rule gets
quietly relaxed, so it is repeated at the point of temptation:

- GOVERNANCE.md's **guilty-until-checked** rule applies to every candidate. An
  unread licence is not a permissive licence.
- **No uncleared source may be used "just to calibrate" or "just to
  sanity-check."** §2.2's rule is absolute: if it moves the number, it is an
  input and it needs a licence.
- Adding an input **widens or narrows the published band** and therefore
  changes a published figure. It requires a fresh rubric run before it ships,
  and the page copy describing the inputs is user-facing copy, so it goes
  through the standing owner copy checkpoint like everything else.
- The public `sources.html` page must always state **what is actually in the
  model today**, not what is aspired to. As of this writing that is one cleared
  dataset, and the page says so in those words.

### First pass — written, undispatched

A Research brief for the first scouting pass was written this cycle and could
not be dispatched (Agent tool unavailable for a fifth consecutive cycle). It is
preserved verbatim in `backlog.md`. Its shape, for whoever picks it up:

- **Quantitative, free, licence-clear.** Producer-side seaborne export series
  for Saudi Arabia, Iraq, Kuwait, UAE, Qatar, Iran and Bahrain are the most
  promising direction, because almost all Hormuz flow *is* those exports — a
  cleared export series could give a genuine **second anchor at better than
  quarterly cadence**, which is the single biggest weakness of the current
  model. Candidates to check: JODI-Oil, OPEC's Monthly Oil Market Report, UN
  Comtrade, EIA's other international series and API, Eurostat, national
  customs and port authorities.
- **Qualitative / event signals for the regime detector.** The detector is
  currently a purely mechanical ±10% quarter-on-quarter test on a quarterly
  series, which means it can only notice a disruption a quarter or more after
  it starts. Public-domain official notices — UKMTO, IMO, MARAD advisories,
  sanctions notices, producer announcements — could let it react in the right
  week rather than the right quarter. This is the highest-value improvement
  available that needs no new *numeric* licence, and it is the most direct
  reading of the owner's "news, reports" wording.
- **Out of bounds**: anything paid, anything AIS-vendor-derived, anything whose
  terms could not be read.

### Presentation decision, same date

The owner also directed that the *visible* trend copy not name an exact source,
because the product is the proprietary method rather than a pass-through. The
CEO's resolution — primary copy speaks of "our model", full attribution moves
intact to a linked `sources.html`, and the page states plainly that one cleared
dataset is what is in the model today — is recorded in `decisions-log.md` and
put to the owner on PR #6. Nothing about that change alters this document's
substance: the inputs, the licences and the rejections are unchanged, and the
company must never let "proprietary" come to mean "unattributed".

## 12. KR6 cycle 1 — 2026-09-18: a second cleared input, regime detector v2, and a horizon guard

**Which of the three KR6 options this cycle delivered: (1) a cleared input AND
(2) a model improvement.** Both, and neither was found by the Research
specialist — the Agent tool was unavailable for a **sixth** consecutive cycle
(§8's provenance caveat applies to this section in full).

### 12.1 The input: EIA Global Energy Security Data, Table 2

The first scouting pass was supposed to hunt for producer-side export series.
It found something better by applying this document's own process lesson first:
**ask whether the publisher already has more than the obvious product.** Two
earlier cycles asserted EIA's Hormuz data was annual and 14 months stale
because they found one page and stopped. This cycle re-inventoried the
supplement and found it contains **ten tables**, not one.

| | |
|---|---|
| **What it gives** | Quarterly volumes for every other world maritime chokepoint (Malacca, Suez/SUMED, Bab el-Mandeb, Danish Straits, Turkish Straits, Panama) plus the Cape of Good Hope and **world total oil supply** |
| **Cadence / lag** | Quarterly, same release as Table 4 — no cadence gain |
| **Licence** | **Already cleared.** Same publication, same release, same US federal public-domain status, same attribution string (§9). Zero new licence surface. |
| **Verdict** | **CLEARED** — and worth stating plainly that this required no new licence risk whatsoever, which is the cheapest possible way to satisfy a mandate whose main hazard is licence-rule erosion |

### 12.2 The improvement: regime detector v2

v1 was "Hormuz moved more than ±10% quarter-on-quarter → disrupted". That
cannot distinguish a blockade from a global demand collapse, which matters
because the two have different persistence behaviour.

v2 adds a **control group**: the Danish Straits, the Turkish Straits and the
Panama Canal. These three carry **no Gulf barrels at all**, so they measure
world oil movement independent of Hormuz. (Malacca, Bab el-Mandeb, Suez and the
Cape are deliberately *excluded* from the control — they carry Hormuz barrels
downstream, so using them would be partly circular.)

```
calm                 if |Hormuz QoQ| <= 10%
disrupted / local    if |control QoQ| < 10% and |Hormuz QoQ - control QoQ| > 20pp
disrupted / systemic otherwise
```

Applied to the cleared record:

| Quarter | Hormuz QoQ | Control QoQ | World supply QoQ | v1 | v2 |
|---|---|---|---|---|---|
| 2Q25 | +0.5% | −5.2% | +2.6% | stable | calm |
| 3Q25 | +1.4% | +3.6% | +0.5% | stable | calm |
| 4Q25 | +1.4% | +0.9% | −4.0% | stable | calm |
| 1Q26 | **−31.0%** | −3.5% | −7.5% | disrupted | **disrupted / local** |
| 2Q26 | **−67.1%** | **+8.1%** | **+3.7%** | disrupted | **disrupted / local** |

The 2Q26 row is the one that matters: Hormuz fell 67% while the rest of the
world's chokepoints **rose** and world supply **recovered**. That is
unambiguously strait-specific, and the model now establishes it mechanically
rather than by the CEO's eye. Bab el-Mandeb +45% QoQ shows the re-routing
directly, and the arithmetic of substitution is visible: from 4Q25 to 2Q26
Hormuz fell **−16.7 m b/d** while the downstream chokepoints that carry Gulf
barrels fell only **−6.2 m b/d**, implying roughly **10.5 m b/d** of non-Gulf
barrels moving onto the same routes.

### 12.3 What this did NOT do, stated because the mandate invites overclaiming

**The published band does not change. It is still 1.5–6.9 m b/d.**

Both disrupted quarters classify as `local`, so there is no `systemic` history
to calibrate against and therefore no basis for a separate band per disruption
type. The detector got better; the number did not move. A cosmetic band change
presented as progress would be exactly the failure §11 warns about, so this is
recorded as a deliberate non-result rather than smoothed over. The companion
series are **diagnostic only — they do not enter the point estimate.**

Likewise, two candidates that looked attractive were **not** adopted:

| Candidate | Outcome |
|---|---|
| **JODI-Oil World Database** (monthly producer-side exports — exactly the second anchor §11 asked for) | **REJECTED on licence.** Terms of Use read in full at `jodidata.org/terms-of-use.aspx`: *"The Intellectual Property rights in the JODI Website, and in the material published on it, are protected by Intellectual Property laws and treaties around the world. **All such rights are reserved.**"* The download page offers the data "for free", but free-to-download is not free-to-redistribute, and there is no open-data grant anywhere on the site. Painful, because monthly Gulf export data is the single most valuable thing the model could have. Not used, not even "to calibrate". A written permission request would be $0 but is outward contact, so it is the owner's call — added to the backlog alongside the dormant IMF one. |
| **EIA Table 1, strategic oil inventories** | **Not adopted — apparent freshness is illusory.** Titled "as of August 2026", which looked like a monthly signal, but the note reads *"Data for 2Q26 are through June 2026 or the latest available"* and the columns are 4Q25/1Q26/2Q26. Same quarterly cadence as everything else. Recorded so a later cycle does not re-discover the title and think it found something. |

### 12.4 The horizon guard — and the date it bites

The §4 back-test measures how wrong persistence gets **one quarter past its
anchor**. It says nothing about two or three quarters past, because the company
has never been there and measured it. Until now the model applied its band flat,
at any distance — §3 promised a band "widening with `d − t_end`" that was never
actually implemented.

New hard limit: `MAX_HORIZON_DAYS = 92`. Past that, the point estimate is
**suppressed entirely** and the page says "No current estimate — awaiting the
next published quarter". Refusing to answer is a legitimate output for an
honest model, and is much better than stretching a range that was never tested
that far.

**This has a date on it.** The anchor covers through 2026-06-30, so the horizon
expires **2026-09-30**. EIA is not expected to publish 3Q26 until ~November. So
on current form the site's headline number disappears at month end and stays
gone for several weeks. That is a real product consequence of an honesty
constraint, it was flagged to the owner at the top of PR #8 rather than allowed
to arrive as a surprise, and the owner may legitimately choose a different
behaviour (e.g. fall back to the measured quarter plus the chart).

### 12.5 Also delivered: §3's recalibration promise now actually runs

`scripts/refresh_estimate.py` (PR #8) re-fetches the supplement daily, and when
EIA publishes a new quarter it re-anchors, **scores the prior estimate against
the new actual**, and appends the error to the model's record. Until now that
was a documented intention with no mechanism behind it.

## 13. KR6 cycle 2 — 2026-09-19: a monthly cleared input, regime detector v3, and evidence against our own published number

Delivery type: **(a) a licence-cleared input AND (b) a model/calibration
improvement.** This is the second consecutive cycle to deliver both, and unlike
cycle 1 it **does** move the number — or rather, it produces the first hard
evidence that the published number is wrong, which was escalated to the owner as
critical issue **#9** rather than acted on unilaterally.

### 13.1 The input: EIA Short-Term Energy Outlook, Table 3d (monthly)

**How it was found** — by applying, for the third time, the lesson this company
learned the expensive way: *always ask whether the publisher has a different or
higher-cadence product than the obvious one.* Cycle 1 applied it inside the
Global Energy Security supplement and found it has ten tables, not one. This
cycle applied it one level up, to EIA as a whole. The Hormuz supplement is a
**quarterly** annex to the STEO. The **STEO itself is monthly**, and its data
workbook carries per-country crude oil production.

| Property | Value |
|---|---|
| Publisher | U.S. Energy Information Administration |
| Product | Short-Term Energy Outlook, `STEO_m.xlsx`, sheet `3dtab` — "Table 3d. World Crude Oil Production" |
| URL | `https://www.eia.gov/outlooks/steo/xls/STEO_m.xlsx` |
| Release read | September 2026 (2026-09-09) |
| Cadence | **Monthly** |
| History through | **2026-08** — read from the workbook's own `Dates` sheet, field `Last Historical Month--- 202608`, *not* inferred from the column headers |
| Licence | **CLEARED.** US federal public domain |
| Licence text actually read | `https://www.eia.gov/about/copyrights_reuse.php` — *"U.S. government publications are in the public domain and are not subject to copyright protection. You may use and/or distribute any of our data, files, databases, reports, graphs, charts, and other information products that are on our website…"*, acknowledgment including publication date requested |
| New licence surface | **None.** Same publisher, same terms page, already cleared for the anchor |

The `Last Historical Month` check is the load-bearing step and is called out
deliberately: the STEO is a **forecast** product, its workbook runs to 2027, and
an agent that read the columns without reading that field would have silently
fed EIA's *forecasts* into our model and presented them as observed data. The
months used here (through August 2026) are history. September 2026 onward is
forecast and is **excluded**.

Residual risk, recorded not glossed: EIA's copyright page has a "Protected
materials" clause covering third-party documents, illustrations and photographs
hosted on their site. Table 3d is EIA's own statistical estimate, so the clause
does not bite — and it bites *less* here than on the Hormuz anchor, which is
EIA analysis of licensed Vortexa data and already carries a provenance caveat on
`sources.html`.

### 13.2 GPCI — the Gulf Producer Crude Index

**GPCI = crude oil production of Iran + Iraq + Kuwait + Saudi Arabia + Bahrain**,
from Table 3d, monthly.

Construction choices, all of which are about consistency rather than coverage:

- **One variable only.** All five are the `copr_` (crude oil production) series.
- **UAE and Qatar excluded.** This workbook carries them only in Table 3b as
  `papr_` (petroleum *and other liquids*) — a different variable. Summing
  `copr_` and `papr_` would be an apples-and-oranges error that no downstream
  check would catch, because the total would still look plausible. This was an
  actual near-miss this cycle: a first label-match pulled UAE from Table 3b and
  it was caught only by noticing the series code was `papr_tc`, not a `copr_`.
- **Oman excluded** despite having a clean `copr_` series: its main export
  terminals are outside the strait, so it is not Hormuz-dependent.
- GPCI is therefore an **index**, not a measure of total Gulf production. It is
  used for *co-movement and regime*, never as a flow figure in its own right.

Known structural caveats, which are why GPCI can never simply replace the
anchor: production is not transit. Barrels can go to storage, to domestic
refining, or to routes that bypass Hormuz entirely (Saudi East-West pipeline to
Yanbu; ADNOC's pipeline to Fujairah; Iraq's Ceyhan line).

### 13.3 The finding: a stable transit ratio that breaks in a diagnosable way

| Quarter | GPCI | Hormuz total oil | ratio = flow / GPCI |
|---|---|---|---|
| 2025Q1 | 19.26 | 20.9 | 1.085 |
| 2025Q2 | 19.55 | 21.0 | 1.074 |
| 2025Q3 | 19.82 | 21.3 | 1.075 |
| 2025Q4 | 20.18 | 21.6 | 1.070 |
| 2026Q1 | 18.21 | 14.9 | 0.818 |
| 2026Q2 | 11.96 | 4.9 | **0.410** |
| 2026Q3 | **14.42** (Jul–Aug, history) | not yet published | — |

**Calm-regime ratio: mean 1.076, sd 0.006, range 1.070–1.085.** Four quarters,
spread under 1%. Ratio above 1 is expected and not an error — Hormuz total oil
includes refined products and barrels from producers outside the index.

The ratio's *collapse* is the diagnostic payload. Production fell 41% peak to
trough; transit fell 77%. **The 2026 disruption is a transit constraint, not a
production constraint** — a distinction the model previously had no way to draw,
and one that matters, because a transit constraint can lift much faster than a
production one.

### 13.4 Regime detector v3 — monthly, and no longer a quarter late

v1 was a ±10% quarter-on-quarter test on a single quarterly series. v2 (cycle 1)
added a chokepoint control group so a Hormuz-specific shock could be told from a
global one — but was still quarterly, so it could only notice a disruption
roughly a quarter after it began. That was named in `backlog.md` as the model's
real gap.

v3 runs on GPCI, monthly, with observations landing ~2–3 weeks after month end
instead of ~11 weeks:

| State | Rule (on GPCI) | Meaning |
|---|---|---|
| `calm` | three consecutive months within ±3% m/m | transit ratio ≈ 1.076 is usable directly |
| `disrupting` | any month ≤ −10% m/m | producer-side shock under way |
| `recovering` | two consecutive months ≥ +10% m/m after a `disrupting` state | producers lifting again |
| `unstable` | anything else | no direct estimator; band only |

Applied to the record, v3 dates the episode for the first time:

- **Onset: March 2026** — GPCI 21.04 → 13.38, **−36.4% m/m**. Previously all the
  company could say was "sometime in Q1".
- **Trough: May 2026**, 11.00.
- **Recovery: June (+20.2%) and July (+15.5%)** → state `recovering`.
- August 2026: 13.57, −11.1% m/m — so the recovery is **not** monotonic, and v3
  drops back to `unstable` rather than declaring an all-clear. Recorded because
  the convenient reading would have been "recovery confirmed".

### 13.5 What this says about the number we are publishing — the uncomfortable part

2026Q3 GPCI (July–August history) is **14.42, up 20.6%** on the 2026Q2 trough.
The published estimate carries 4.9 forward by persistence, which assumes nothing
has changed since June.

Applying every transit ratio the company has ever actually observed:

| Ratio | Implied 2026Q3 Hormuz flow |
|---|---|
| worst ever observed (2026Q2, 0.410) | **5.9** |
| partial disruption (2026Q1, 0.818) | 11.8 |
| calm mean (1.076) | 15.5 |

**Every one of those is above the published point estimate of 4.9, and the
lowest sits at the top of the published 1.5–6.9 band.** The page tells readers
to treat the range as the answer; on this evidence the bottom half of that range
(1.5–4.0) is supported by nothing.

**Escalated as critical issue #9, not fixed unilaterally.** Changing a published
figure needs the owner, a fresh rubric run, and the copy checkpoint. Four options
were put to the owner (leave it; widen the band upward; re-anchor on GPCI;
suppress the estimate now). CEO recommendation: widen now, re-anchor after
review.

### 13.6 The limits of this result, stated because the mandate invites overclaiming

1. **The transit ratio is unstable in disruption — that is the finding, and it
   cuts both ways.** A Q3 ratio of 0.30 would give 4.3, inside the current band.
   The *direction* of the evidence is solid; the *magnitude* is not.
2. **Production is not transit.** §13.2's bypass routes are real and unmeasured.
3. **GPCI is incomplete by construction** — no UAE, no Qatar. Deliberate, but it
   means the index understates the Hormuz-relevant producer base.
4. **Still no specialist review.** Seven consecutive cycles without the Agent
   tool. Every judgement here — the licence read, the index construction, the
   exclusions, the ratio interpretation — was made and checked by the same agent.
5. **The published band did not change this cycle.** As in cycle 1, motion is
   not being dressed up as progress: what changed is the evidence and the
   diagnosis. The number is the owner's to move.

### 13.7 What this does not change

The licence bar held again. Nothing uncleared was used, including "just to
sanity-check" — the 403-blocked sources below were dropped rather than worked
around.

**Checked and not adopted this cycle:**

| Candidate | Outcome |
|---|---|
| **UKMTO** (`ukmto.org`) maritime advisories | **UNRESOLVED — could not read.** HTTP 403 at origin (not the proxy; `eia.gov` and `msi.nga.mil` fetched fine in the same pass). Terms never read, so it cannot be cleared. Not used. Re-try from a different route next cycle. |
| **US MARAD MSCI advisories** (`maritime.dot.gov`) | **UNRESOLVED — could not read.** HTTP 403 at origin. Same treatment. |
| **NGA Maritime Safety Information** (`msi.nga.mil`) broadcast warnings API | **Reachable and probably public domain, but NOT ADOPTED — low signal.** 386 active warnings, 24 Gulf-relevant, and they are navigational hazards: wrecks, survey operations, an inoperative lattice beacon. A dangerous wreck notice says nothing about oil flow. NGA's *special warnings* series would be the geopolitically meaningful one; no working endpoint found this cycle. Licence not pursued, because an unusable input does not need clearing. |
| **EIA STEO Table 3a** | Not adopted — no per-country Gulf breakout; aggregates only. |

Bucket (2) of the standing Research brief — event and advisory signals — is
therefore **still open**, and is still the most direct reading of the owner's
"news, reports". Two of the three best candidates are blocked at origin rather
than rejected on licence, which is a different and more tractable problem.

## 14. KR6 cycle 3 — 2026-09-19 (8th cycle): the improved model reaches production, and the horizon is fixed at one quarter by owner decision

**Which of the three KR6 options this cycle delivered: (b), partially, and the
partial is stated rather than dressed up.** No new input was cleared and the
published band did not move. What changed is that the model improvements built
in cycles 1 and 2 of this mandate stopped being a document and started being the
product — and one piece of the methodology that had only ever existed on paper
now runs unattended.

### 14.1 What actually improved

- **The §3 recalibration promise is now a running mechanism, not an intention.**
  `scripts/refresh_estimate.py` re-fetches the cleared EIA supplement every day,
  and *on the first day the published series moves* it re-anchors, scores the
  estimate we had been publishing against the new actual, and appends the error
  to `model.scored_errors` in `site/data/hormuz.json`. Until this merged, that
  scoring depended on a CEO cycle happening to run on the right day. The
  back-test is now self-extending; that is a methodology improvement, not a
  deployment detail.
- **Regime detector v2 (companion chokepoints, EIA Table 2) is live**, so the
  local/systemic classification is computed from the source every day rather
  than being a finding in a memory file. Current live classification:
  `disrupted / local`, Hormuz −67.1% quarter-on-quarter against a control group
  that rose.
- **The horizon guard is live and now has an owner decision behind it** (§14.2).

### 14.2 Owner decision on the horizon — recorded here because it is a property of the model, not of the site

Owner, 2026-09-19, live in conversation: *"one quarter is fine for now, we
should extend it later."*

`MAX_HORIZON_DAYS` stays at **92**. Past that, the model publishes nothing and
says so. The anchor covers through 2026-06-30, so the point estimate is expected
to disappear around **2026-10-01** and stay gone until EIA publishes 3Q26
(~November). That consequence was put to the owner explicitly and accepted.

**"Extend it later" is now a standing sub-goal of this mandate.** It is tracked
separately from "widen the inputs" because the horizon is a property of the
*back-test*, not of the input set: adding a series does not, by itself, tell us
how wrong persistence gets two quarters out. The three routes, in order of
promise:

1. **Use the monthly cleared input we already have.** GPCI (STEO Table 3d, §13)
   produces a testable one-month-ahead error every month. Twelve monthly errors
   a year accumulate evidence about longer horizons far faster than four
   quarterly observations ever will. This is where "extend the horizon" and
   "widen the inputs" genuinely converge, and it is the reason the backlog line
   points at the widen-inputs work rather than duplicating it.
2. **Back-test further out on the history we already hold.** The §4 back-test
   only ever measured one-quarter-ahead error. Two- and three-quarter-ahead
   persistence errors can be computed from the same cleared series today. That
   would not make the model better, but it would make an honest statement about
   a longer horizon *possible*, which is currently not the case.
3. **Replace flat persistence with a real shape function.** Only this could make
   a longer horizon deserve anything other than a much wider band.

**The bar for ever moving the threshold, stated now rather than at the moment of
temptation**: a longer horizon must be earned by a *measured* error at that
horizon. Widening `MAX_HORIZON_DAYS` because the blank headline is awkward would
be asserting a validation we never performed — rubric §1.6 and critical-issue
category 4. The owner's "extend it later" is permission to do the work, not
permission to skip it.

### 14.3 What was not done, and why — so this is not silence

No new candidate input was scouted this cycle. The cycle was scoped by the
owner to executing one decision (merge PR #8) and was deliberately not widened
into a research pass on the way past. The open candidates are unchanged and
carried forward verbatim in `backlog.md`: bucket (2) event/advisory signals
(UKMTO and MARAD **403-blocked at origin, not licence-rejected** — retry from
another route), OPEC MOMR, UN Comtrade, Eurostat, Gulf customs/port authorities,
and the standing question of whether EIA publishes anything *weekly* that is
Gulf-relevant.

### 14.4 Honest accounting

The published number today is the same number as yesterday: **4.9, range
1.5–6.9, estimate for 18 September 2026, horizon 80 of 92 days.** A cycle that
improves the machinery and not the estimate is reported as exactly that. Note
that the most substantive open methodology question is *not* this section — it
is critical issue #9 (§13), which argues our published figure is probably too
low, and which remains the owner's decision.

## 15. KR6 cycle 4 — 2026-09-20 (9th cycle): the bypass term stops being "unmeasured"

Delivery type: **(b) a model/calibration improvement with no new input.** No new
source was introduced and no new licence surface was opened. Nothing was
published. The published figure is unchanged at **4.9, range 1.5–6.9**.

This cycle ran in **read-only mode** — the week-of-2026-09-21 plan is still
`PROPOSED` (GitHub issue #10, no owner response), so under GOVERNANCE.md the
company may research and prepare but may not spend, publish, or take
hard-to-reverse action. A methodology improvement that stays in
`company-memory/` and a script that touches nothing under `site/` are squarely
inside that boundary. Changing the live number would not be, however good the
evidence — which is the whole point of §15.4 below.

### 15.1 What it attacks: our own stated limit

`§13.6` lists as limit (2): *"Production is not transit. §13.2's bypass routes
are real and unmeasured."* That word — unmeasured — is load-bearing, because
critical issue **#9** rests on GPCI (Gulf producer crude) having recovered 20.6%
off its trough, and the argument only carries to *Hormuz* if the recovered
barrels have to use the strait. Gulf crude can reach market without transiting
Hormuz: pipelines to Red Sea and Gulf-of-Oman terminals exist. If those routes
absorbed part of the 2026 collapse, then two things follow at once, and they
pull in opposite directions:

- the transit ratio **understates** how much crude was still reaching market, and
- a production recovery translates into **less** Hormuz traffic than a naive
  GPCI ratio implies.

Both effects are material to issue #9 and neither was quantified. Now one is.

### 15.2 Method, and the check that makes it more than arithmetic

Reproducible end-to-end: `scripts/bypass_analysis.py`, which re-fetches both
cleared sources rather than trusting any number recorded in this file.

1. Fit an OLS linear trend to each companion chokepoint's **crude and
   condensate** series over the four calm quarters (1Q25–4Q25).
2. Extrapolate into 1Q26 and 2Q26; the residual is flow above or below that
   route's own pre-disruption trend.
3. Bypass proxy = **positive** residuals on the Red Sea routes (Bab el-Mandeb,
   Suez/SUMED) — routes a Gulf barrel can reach by pipeline without passing the
   strait.
4. **Placebo control** — repeat on routes that carry essentially no Gulf crude
   (Danish Straits, Turkish Straits, Panama). If the method manufactures large
   residuals there, it is measuring noise, not re-routing.
5. Malacca and the Cape are **downstream of both** Hormuz and the Red Sea
   routes, so they are read as confirmation of direction only and are never
   added to the bypass term — adding them would count the same barrel twice.

Step 4 is what stops this being curve-fitting to a story, and it is reported
whichever way it comes out.

### 15.3 Results

| Route (crude) | 1Q26 residual | 2Q26 residual | Read as |
|---|---|---|---|
| Hormuz | −5.10 | −12.64 | the disruption itself |
| **Bab el-Mandeb** | **−0.05** | **+2.32** | **the bypass signal** |
| Suez / SUMED | −0.55 | −0.41 | no northbound bypass |
| Malacca (downstream) | −3.30 | −7.37 | Asia-bound Gulf crude fell hard |
| Cape (downstream) | −1.20 | −0.32 | ≈ on trend |
| Danish Straits (control) | −0.25 | **−0.02** | placebo: clean |
| Turkish Straits (control) | −0.25 | **+0.58** | placebo: noise floor |
| Panama (control) | +0.00 | **+0.10** | placebo: clean |

Three things are worth more than the headline:

- **The 1Q26 Bab el-Mandeb residual is −0.05.** The trend fitted on 2025 alone
  predicted the next quarter to within 0.05 m b/d, and only broke in the quarter
  Hormuz collapsed. That is an out-of-sample hit, not a fitted one, and it is the
  strongest single reason to believe the +2.32 is real.
- **The bypass went south, not north.** Suez/SUMED is *below* trend throughout.
  Whatever was re-routed left through Bab el-Mandeb toward Asia.
- **The placebo is not perfectly clean.** Turkish Straits shows +0.58, so this
  method's empirical noise floor is about ±0.6 m b/d — a quarter of the signal
  it is claiming. Recorded because the convenient version of this section would
  have quoted only Danish (−0.02) and Panama (+0.10).

**Bypass-adjusted transit ratio:**

| Quarter | Hz crude | GPCI | raw ratio | bypass-adjusted |
|---|---|---|---|---|
| 1Q25–4Q25 (calm) | 14.8–15.9 | 19.26–20.18 | mean **0.769**, sd 0.014 | same |
| 1Q26 | 10.9 | 18.21 | 0.599 | 0.599 |
| 2Q26 | 3.7 | 11.95 | **0.310** | **0.504** |

**The bypass term explains 42% of the 2Q26 collapse in the transit ratio.** The
other 58% is a genuine transit constraint, so §13.3's central finding survives —
2026 is still a transit story, not a production story — but it was overstated by
roughly a factor of two, and it is corrected here rather than defended.

### 15.4 What it says about critical issue #9 — and why the number still did not move

Projecting 2026Q3 with the bypass term carried explicitly (GPCI 14.42, Jul–Aug
history):

| 2026Q3 scenario | Hormuz crude | Total oil (2Q26 product mix) | Total oil (calm product mix) |
|---|---|---|---|
| bypass persists at the 2Q26 level | 4.94 | **6.5** | **6.9** |
| bypass halves | 6.10 | 8.1 | 8.5 |
| bypass ends entirely | 7.26 | 9.6 | 10.2 |

Set against §13.5's ratio-family figures of **5.9 / 11.8 / 15.5** and the
published **4.9 (range 1.5–6.9)**:

1. **Issue #9's direction is confirmed and its magnitude is tightened.** Every
   construction the company has tried — raw transit ratio, ratio family,
   bypass-explicit — lands **above 4.9**. The spread narrows from 5.9–15.5 to
   6.5–10.2, and the narrowing comes from naming a mechanism rather than from
   picking a ratio.
2. **The most conservative case is now the most structurally informed one.**
   "Bypass persists" gives 6.5–6.9, i.e. the *top edge* of the published band.
   The bottom half of the published range (1.5–4.0) is supported by nothing on
   any construction. That is the same conclusion as §13.5, reached independently.
3. **Nothing was changed on the live site.** Read-only mode aside, this is one
   cycle old, unreviewed by any specialist, and rests on an assumed Q3 bypass.
   It is filed as **new evidence on issue #9**, which remains the owner's
   decision.
4. **The recommendation on #9 is refined, not reversed.** Previously "B now
   (widen the band upward), C after review (re-anchor on GPCI)". A raw-GPCI
   re-anchor (C as originally written) would land near 15.5 and would be wrong
   for a reason we can now name: it ignores the bypass. So C is respecified as
   **C′ — re-anchor on a bypass-adjusted GPCI estimator**, which is what
   `scripts/bypass_analysis.py` computes. **B now, C′ after review.**
   *[Correction, 2026-09-23 — see §19.1. "C as originally written would land
   near 15.5" is wrong. The issue #9 body defined C as the **last observed**
   ratio × latest GPCI, ≈5.9. 15.5 is the **calm** ratio, which was never
   option C. Left in place for the trail.]*

### 15.5 Limits, stated because the mandate invites overclaiming

1. **There is no 2026Q3 chokepoint observation and will not be until ~November.**
   The Q3 bypass term is *assumed*, not measured — the same persistence
   assumption this company criticises elsewhere, applied to the bypass. If
   Hormuz reopens, the bypass unwinds and the true figure moves toward 8–10.
2. **It is an attribution, not a measurement.** Bab el-Mandeb flows are
   bidirectional and include non-Gulf barrels. **No pipeline-capacity figure
   from any source was used** — the attribution rests only on the chokepoint
   residuals, deliberately, because a capacity number would be an uncleared
   input doing work on a published figure.
3. **Four points fit the trend**, and the placebo noise floor is ±0.58.
4. **GPCI still excludes UAE and Qatar**, so these are index ratios, not
   physical shares.
5. **Still no specialist review — ninth consecutive cycle.** The Agent tool was
   tested again this cycle and returned `No such tool available: Task`. Every
   judgement above was made and checked by the same agent. The one mitigation
   added this cycle: the derivation is a script that re-fetches from source, so
   a reader can re-run it instead of trusting this document.
6. **The published number is the same as yesterday**: 4.9, range 1.5–6.9. A
   cycle that improves the evidence and not the estimate is reported as exactly
   that.

### 15.6 Independent re-derivation of GPCI, recorded because it is cheap assurance

`scripts/bypass_analysis.py` rebuilds GPCI from `STEO_m.xlsx` rather than
reading §13's table. It reproduces **19.26 / 19.55 / 19.82 / 20.18 / 18.21 /
11.96** and **14.42** for 2026Q3 (Jul–Aug) — identical to §13.2 to two decimals,
from a workbook released since that work was done. The history/forecast boundary
was again taken from the workbook's own `Last Historical Month--- 202608` field,
and the script **exits with a failure** rather than guessing if that field is
ever missing.

## 16. KR6 cycle 5 — 2026-09-21 (10th cycle): a *weekly* cleared input, and it argues against our own preferred answer

**Type: (a) a new licence-cleared input AND (b) a calibration improvement.** Zero
new licence surface. **The published figure did not move** — the week-of-09-21
plan is still `PROPOSED`, so this cycle was read-only and moving it was not
available even had the evidence justified it. It does not, as it turns out.

### 16.1 What was added

**EIA, Weekly Preliminary Crude Oil Imports by Country of Origin**
`https://www.eia.gov/dnav/pet/pet_move_wimpc_s1_w.htm`
Release **2026-09-16**, next release **2026-09-23**, history to 2010.
Series used: `W_EPC0_IM0_NUS-NSA_MBBLD` (Saudi Arabia),
`W_EPC0_IM0_NUS-NIZ_MBBLD` (Iraq), `W_EPC0_IM0_NUS-NKU_MBBLD` (Kuwait).

Licence: same publisher and same terms as the two inputs already cleared — US
federal government work, public domain. Terms re-read **first-hand this cycle**
at `eia.gov/about/copyrights_reuse.php` rather than assumed from prior cycles.
That page carries a carve-out for "protected materials ... contributed or
licensed by private individuals, companies, or organizations"; it was checked
and does not bite here, because these are EIA/Census survey statistics, not a
vendor feed. This is not a pedantic distinction — the Hormuz anchor *does* carry
exactly that kind of caveat (it is derived from Vortexa data), which is why the
site republishes EIA's analysis and never claims to hold vendor data.

**This is the company's first weekly-cadence input.** It is also the third time
the question *"does this publisher have a higher-cadence product?"* has paid
off: annual→quarterly, quarterly→monthly, and now monthly→weekly, all from a
publisher we had already cleared. That lesson has now produced every single
input the model has.

### 16.2 Why a 2–4% sample is worth anything at all

It is not a flow measure and is never to be scaled into one: US crude imports
from the Gulf averaged **0.46 m b/d across 2025** (and swung from 0.00 to 0.87
during 2026) against ~15 m b/d of crude transiting the strait — a **~3%**
sample, and one selected by where barrels were *sold*, not sampled at random. What makes it useful is narrower and real — it is a **transit-side**
observation (barrels that physically left the Gulf and reached a US port) at
**weekly** resolution, where every other input is production-side or quarterly.

Lagged by a Gulf→US voyage of ~35–55 days, the latest week (ending 2026-09-11)
describes barrels loaded around **2026-07-18 to 2026-08-07** — all of which fall
*after* the Hormuz anchor's 2026-06-30 coverage end, i.e. **inside the Q3 gap
the published estimate is currently extrapolating through blind.** That is the
whole reason to bother with it.

### 16.3 The placebo control, and what passed

Confound to beat: a fall in Gulf-origin arrivals could be a US refinery story,
not a Gulf story. Same defence as §15 — carry a control group of non-Gulf
origins (Canada, Mexico, Brazil, Colombia, Venezuela, Nigeria).

2026 monthly means, against each group's own 2025 calm baseline
(Gulf 459.9 kb/d; control 4,785.8 kb/d):

| 2026 | Gulf-origin | vs calm | Control | vs calm |
|---|---|---|---|---|
| Jan | 548.2 | +19.2% | 4898.4 | +2.4% |
| Feb | 775.2 | +68.6% | 4993.0 | +4.3% |
| Mar | 866.5 | +88.4% | 5018.8 | +4.9% |
| Apr | 499.8 | +8.7% | 4740.5 | −0.9% |
| May | 242.0 | −47.4% | 4953.0 | +3.5% |
| Jun | 112.5 | −75.5% | 4736.5 | −1.0% |
| **Jul** | **0.0** | **−100.0%** | 5104.0 | +6.6% |
| Aug | 174.2 | −62.1% | 5275.8 | +10.2% |
| Sep | 377.5 | −17.9% | 5710.0 | +19.3% |

**Placebo PASS, and not marginally**: at the Gulf trough the divergence is
**−106.6 points** (Gulf −100.0%, control +6.6%). The control group did not dip
at all. **Five consecutive weeks of literally zero Gulf-origin crude arrivals,
ending 2026-07-31.** Whatever happened was Gulf-specific.

**Timeline corroboration, independent of everything else we have**: the arrivals
trough is **July 2026**; §13.3's monthly GPCI dates the production trough to
**May 2026**. Two months apart — which is the voyage lag, arrived at from a
completely different series. Three structurally unrelated inputs (quarterly
chokepoint, monthly production, weekly arrivals) now agree on when this
disruption happened.

### 16.4 The finding that matters, and it cuts against us

The aggregate recovery — latest 4-week average **334.2, −27.3% vs calm** — hides
a split that reverses its meaning:

| Origin | 2025 baseline | 4-wk avg @ 2026-09-11 | vs baseline |
|---|---|---|---|
| **Saudi Arabia** | 269.2 | 313.2 | **+16.4%** |
| **Iraq** | 190.7 | 21.0 | **−89.0%** |

Saudi Arabia is **fully recovered and above its pre-disruption normal**. Iraq is
**still on the floor**. Two readings:

1. Hormuz transit has substantially recovered, and Iraq's shortfall is
   commercial — Basrah barrels redirected to Asia rather than blocked.
2. **The recovery is bypass, not transit.** Saudi Arabia has a non-Hormuz route
   to market (East–West pipeline to Red Sea terminals); Basrah crude does not.
   A recovery visible *only* in the producer that can skip the strait is exactly
   the fingerprint of production recovering while the strait stays constrained.

Reading 2 is the one consistent with §15's measured bypass term, and **it
weakens the strong form of critical issue #9.** We cannot currently separate the
two: the chokepoint data that would settle it is quarterly and stops at
2026-06-30. The next supplement (~November, covering 3Q26) resolves it.

### 16.5 Consequence for critical issue #9 — the recommendation gets *more* conservative

The **direction** still holds. Gulf-origin arrivals for Q3 loadings sit at −18%
to −27% of calm; the published figure implies Hormuz transit is still at its
2Q26 level of 4.9, which is **−77%** of calm. Those two are hard to reconcile,
and the bottom of the published 1.5–6.9 band remains supported by nothing.

The **magnitude** keeps shrinking as evidence accumulates, and that trend is
worth naming explicitly:

| Cycle | Construction | Implied 2026Q3 |
|---|---|---|
| §13 (2026-09-19) | raw transit ratios × GPCI | 5.9 / 11.8 / 15.5 |
| §15 (2026-09-20) | bypass-adjusted | 6.5 – 10.2 |
| §16 (2026-09-21) | weekly arrivals, Saudi/Iraq split | evidence that even 6.5–10.2 is **top-heavy** |

**Recommendation to the owner, revised: B now — widen the band upward, keep 4.9
as the point estimate. And C′ should NOT be adopted until a 3Q26 chokepoint
observation exists (~November).** Last cycle said "C′ after review". This cycle
says wait, because the input we added is the first one able to distinguish
bypass-recovery from transit-recovery, and it leans toward bypass. Three cycles
of new evidence have moved this company's own proposed number *down* each time;
a re-anchor adopted at any of those earlier points would already have been
wrong.

### 16.6 Limits, stated because the mandate invites overclaiming

1. **A 2–4% sample, selected by trade route.** It can corroborate a direction.
   It cannot set a level, and nothing here is scaled into m b/d of Hormuz flow.
2. **Arrivals, not loadings.** This can describe the recent past; it can never
   nowcast today. The voyage lag is assumed (35–55 days), not fitted.
3. **EIA labels these PRELIMINARY**; the Petroleum Supply Monthly revises them.
4. **Only Saudi Arabia and Iraq are reported.** Kuwait has a series id but is
   outside EIA's reported top ten and is empty throughout — the script proves
   this rather than asserting it (0 weeks reported). UAE and Qatar never appear.
5. **The Feb–Mar 2026 run-up (+69%, +88%) is unexplained.** Those are Jan–Feb
   loadings, i.e. *before* the March onset. Pre-positioning ahead of anticipated
   disruption is a plausible story and would make this series a *leading*
   indicator, which would be valuable — but it is one episode and it is recorded
   here as a **hypothesis, not a finding.**
6. **Still no specialist review — tenth consecutive cycle.** The Agent tool was
   tested again and returned `No such tool available: Task`. Mitigation is the
   same as §15: the whole derivation is `scripts/weekly_arrivals_analysis.py`,
   which re-fetches from source on every run.
7. **This input is ANALYSIS-ONLY.** It does not enter the published estimate,
   and `sources.html` has deliberately **not** been updated to mention it.
   Listing an analysed-but-unused input would overstate the model's input
   diversity, which is critical-issue category 4 — the same reason §13's GPCI
   copy is still held and conditional.

## 17. KR6 cycle 6 — 2026-09-22 (11th cycle): the first non-EIA corroboration, and a licence that is only half-clear

**Delivery type: (b), with an (a) candidate deliberately left unadopted.** The
published figure is unchanged at **4.9, band 1.5–6.9**. This cycle ran
read-only — the week-of-21 plan is still `PROPOSED` — so moving it was not
available even had the evidence justified it. No parameter of the model
changed. What improved is the model's *evidential base*, and a weakness that
had never been named got named and measured.

Derivation: `scripts/eu_imports_analysis.py`, which re-fetches every series
from source on each run. No cached number is trusted.

### 17.1 The weakness this cycle was aimed at

Every input the model has ever had — the Hormuz anchor (Table 4), the companion
chokepoints (Table 2), GPCI (STEO Table 3d), the weekly US arrivals series —
comes from **one publisher: the EIA**. That is not a licence problem; it is a
*correlated-error* problem, and it is the kind of thing that is invisible from
the inside. If EIA's Hormuz series is systematically wrong — and EIA itself
warns that Hormuz AIS data has been unreliable since end-February 2026 and is
"being revised frequently" — then every one of our cross-checks inherits the
same blind spot, and our apparent agreement between three inputs is partly an
artefact of a single collection pipeline.

§16 ended by claiming "three structurally unrelated inputs now agree." That
claim was **overstated**, and it is corrected here: they were three
structurally different *series*, but one publisher. The test that was actually
needed was an independent statistical system.

### 17.2 The candidate: Eurostat `nrg_ti_oilm`

**Eurostat — Imports of oil and petroleum products by partner country, monthly**
(`nrg_ti_oilm`, via the Eurostat dissemination API). Crude oil only
(`siec=O4100_TOT`), declarant EU27, unit thousand tonnes/month.

Why it is worth the trouble: it is a **destination-side customs observation** —
barrels that physically arrived at an EU port and were declared to a national
customs authority. Not tanker tracking, not AIS, not a production survey. It is
about as methodologically distant from EIA's Vortexa-derived Hormuz series as a
free source gets, which is precisely what makes it a real test rather than a
fourth restatement.

Structure metadata says the dataflow runs to 2026-07 and was last updated
2026-09-10. **That is misleading for our slice, and the rubric caught it before
it was written down as a freshness claim**: the crude-oil-by-partner series is
populated only through **2026-06** — checked directly, and the 2026-07 cell is
null for *every* partner tested (Saudi, US, Norway), not just the Gulf ones. The
2026-07 edge belongs to some other slice of the dataflow, not to this one.

Stated plainly because it matters: this input is **not fresher than the anchor**.
It ends where the anchor ends (2026-06-30). It buys corroboration, not forward
information, and it does **not** move critical issue #9's magnitude.

### 17.3 Result — the placebo passes, and the split reproduces

Each partner is measured against **its own** 2024-01..2025-12 calm mean, in
percent. Levels are never compared across partners and never summed with the
Hormuz anchor — that series is thousand tonnes per month, the anchor is million
barrels per day (the §16 unit discipline, carried forward).

| Group | 2Q26 vs own calm mean |
|---|---|
| Gulf partners | **−65.0%** (n=3) |
| Placebo control (US, Norway, Nigeria, Brazil, Kazakhstan, Libya) | **+4.5%** (n=6) |
| **Divergence** | **−69.5 points** |

The collapse is **Gulf-specific**, not a European demand story.

**Sensitivity, because the script's own exclusion threshold is load-bearing.**
Kuwait (calm mean 5.2 kt/month) and Iran (0.2) were excluded as structural
zeros — no signal is recoverable from a series that was already zero before the
disruption, and reporting them as "−100%" would have been a fabricated result.
The UAE (93.7 kt/month) sits just above the 50 kt cutoff and went to exactly
0.0 for six straight months, which at that size is more plausibly a commercial
re-routing than a strait signal. **Excluding the UAE as well**: Gulf group
−47.5%, divergence **−52.0 points**. The conclusion survives either choice, so
the threshold is not doing the work — but it is recorded rather than buried,
because a cutoff that changes a headline is a parameter.

**The split that matters**, against §16's US weekly arrivals:

| Producer | EU imports, 2Q26 vs calm | US weekly arrivals (§16) | Non-Hormuz route? |
|---|---|---|---|
| Saudi Arabia | **−16.7%** | **+16.4%** | Yes — East–West pipeline to Yanbu |
| Iraq | **−78.2%** | **−89.0%** | No — Basrah must transit the strait |

Two statistical systems on two continents, with nothing in common but the
physical cargoes, produce the **same ordering**: the producer that owns a route
around the strait holds up; the producer whose barrels must pass through it is
on the floor. The absolute numbers differ — as they should, since Europe and
the US Gulf Coast are different markets with different voyage lengths — and the
agreement being *ordinal rather than numerical* is the honest description.

**Onset timing, independently recovered.** Iraq's EU imports: January +8.7%,
February −4.8%, **March −37.9%**, April −75.6%, May −79.1%, June −80.0%. §13.3
dated the disruption onset to **March 2026** from GPCI production data. A
customs series from a different publisher lands on the same month. (Cargoes
arriving in March loaded roughly three weeks earlier, so if anything the
arrivals signal runs slightly ahead of the production signal — noted, not
claimed: the lag is uncertain and customs declaration dates are not arrival
dates.)

### 17.4 What this does to critical issue #9 — very little, and that is the point

It does **not** move the magnitude. The series stops at 2Q26, so it says nothing
directly about 3Q26, and the published 4.9 is a 2Q26 anchor.

What it does is **raise confidence in the mechanism** underneath §15 and §16 —
production recovering while *transit* does not — now that the mechanism has
survived a test against a publisher with no shared pipeline with EIA. That
supports the **conservative** recommendation already on the table and does not
rehabilitate the aggressive one: **B now** (widen the band upward, keep 4.9 as
the point estimate), **C′ not before a 3Q26 chokepoint observation exists
(~November)**. Recommendation unchanged from 2026-09-21.

### 17.5 The licence — CLEARED-CONDITIONAL, and not adopted

Terms read first-hand at `ec.europa.eu/eurostat/web/main/help/copyright-notice`
(HTTP 200 this cycle), including the Exceptions section, which is where the
problem is.

- **General grant**: "Reuse of statistical data, metadata, publications, and
  other dissemination tools published on this website for commercial or
  non-commercial purposes is authorised provided the source is acknowledged."
  Editorial content is CC BY 4.0. Implemented via Commission Decision
  2011/833/EU. Modifications must be disclosed and a non-responsibility
  disclaimer carried.
- **The exception that bites**: certain data "may not be reused for **commercial
  purposes**, but non-commercial reuse is possible without restriction,"
  including *"Data for countries other than: Member States of the European
  Union (EU), Member States of the European Free Trade Association (EFTA),
  official EU acceding and candidate countries."*

Saudi Arabia and Iraq are plainly outside that list. The question is whether a
series recording *EU27 imports declared by EU members, broken down by partner*
is "data for" the partner country or data for the declarant. The notice's own
Switzerland/Austria clarification points to the **declarant** reading — it
forbids selling trade data *declared by* Switzerland while expressly permitting
the sale of "Swiss export/import data declared by an EU Member State." On that
reading our use is commercial-safe.

**That is a reading, not a grant, so it does not clear the bar.** Recorded
verdict: **CLEARED for non-commercial use without restriction; AMBIGUOUS for
commercial use.**

Consequences, stated before anyone is tempted:

1. The input is **NOT adopted**. It does not enter `site/data/hormuz.json`, it
   does not touch the published figure, and `sources.html` has deliberately
   **not** been updated — listing an analysed-but-unused source would overstate
   the model's input diversity, which is critical-issue category 4. Same
   discipline as §13's GPCI and §16's weekly series.
2. This analysis is **not** "just a sanity check" that gets a pass on licensing.
   It did not move the number, which is the only reason it is in-bounds at all;
   the moment it would move one, it is an input and the ambiguity becomes live.
3. **It is a Phase 2 trap, and that is the real finding.** The site is
   non-commercial today, so the permissive half of the grant covers it. If this
   input were adopted now and the owner later approved monetization, the
   licence status of a live input would flip **silently**, with no alert
   anywhere in the system. Any Phase 2 proposal must therefore state which
   inputs are commercial-safe. Logged as a pre-emptive category-3 entry in
   `critical-issues-log.md` for 2026-09-22.

### 17.6 Limits, carried forward explicitly

1. **EU27 is a minor destination for Gulf crude** — Asia dominates. This series
   constrains the *shape* and *attribution* of the disruption. It cannot set
   the *level* of Hormuz flow and must never be scaled into one.
2. **No forward information.** Gulf rows end at 2026-06. The 3Q26 gap the
   published estimate extrapolates through is still covered only by §16's
   weekly US arrivals.
3. **Route attribution is inferred, not measured.** "Saudi has a bypass, Iraq
   does not" is a physical-geography claim carried from §15. No pipeline
   capacity figure was used anywhere — a capacity number doing work on a
   published estimate would be an input and would need a licence of its own.
   The §15 bar holds.
4. **Eleventh consecutive cycle with no specialist review.** The Agent tool
   returned `No such tool available: Task. Task is disabled for this session,
   in subagents as well as here.` This scouting pass was run by the CEO at
   reduced depth, exactly as the week-of-21 plan said it would be if the tool
   stayed unavailable. Mitigation unchanged: the derivation is a script that
   re-fetches from source.
5. **Not done this cycle, stated so it is not silence.** UKMTO
   (`ukmto.org`, **403**), MARAD MSCI (`maritime.dot.gov/msci`, **403**) and
   OPEC (`opec.org`, **403**) were all re-probed this cycle and all refused at
   the origin. **None of them is licence-rejected** — they are unread, which is
   a different and weaker status. No user-agent spoofing or other workaround
   was attempted, on precisely the sources whose access terms matter most. UN
   Comtrade and Gulf customs/port authorities remain unchecked and carry
   forward verbatim.

## 18. KR6 cycle 7 — 2026-09-23 (12th cycle): a commercial-safe, non-EIA input with the first 3Q26 loadings in it

**Delivery type: (a), analysis-only, plus (b).** A licence-cleared input was
found, read and added to the model's *evidence base*. It is **not** in the
published band: this is a read-only cycle (the week-of-21 plan is still
`PROPOSED`), and the input cannot set a level anyway, so "re-derive the band
with it in" is done here as analysis, not publication. Published figure
unchanged at **4.9, band 1.5–6.9**.

Derivation: `scripts/japan_imports_analysis.py`, which re-fetches from source
on every run.

### 18.1 Why this candidate, and why now

§17 left two gaps: (1) the only non-EIA corroboration was licence-ambiguous for
commercial use, and (2) nothing cleared reached into 3Q26 except a ~3% US
sample. The question asked this cycle was: *which importer is so
Gulf-dependent that its customs data is effectively a Hormuz transit sample,
and does it publish faster than Eurostat?* Answer: **Japan** — 94% of calm
crude imports are Gulf-origin (~2.2 of 2.36 m b/d), and the Ministry of Finance
publishes 9-digit HS by country monthly, with **July 2026 provisional already
out (updated 2026-08-28)** — one month past the EIA anchor and Eurostat.

### 18.2 The licence — CLEARED, commercial and non-commercial

Read first-hand this cycle, three documents:

- **Japan Customs site notice** (`customs.go.jp/copyright_e.htm`, and the
  authoritative Japanese page `customs.go.jp/kyotsu/rules.htm`): content is
  under the **Public Data License 1.0 (PDL1.0)** "unless any rights are
  indicated". The site-specific "important information" lists exactly three
  things under other rules: the Customs logo, the "Custom-kun" mascot, and the
  150th-anniversary logo. No statistics carve-out, no declared third-party
  rights.
- **PDL1.0** (`digital.go.jp/en/resources/open_data/public_data_license_v1.0`,
  English reference text; the Japanese version governs): "Commercial use of
  'This Content' is also permitted", and "numerical data, simple tables,
  graphs, etc. are not subject to copyright protection … and can be used
  freely."
- **e-Stat terms** (`e-stat.go.jp/en/terms-of-use`, the distribution channel):
  Government of Japan Standard Terms of Use 2.0, commercial use permitted,
  stated CC BY 4.0-compatible.

**Conditions that bind any future publication**: cite the source, **state that
it has been edited and by whom**, and never present edited output "in a format
that may be misconstrued" as produced by the Government of Japan. For us that
means our estimate may never read as a Japanese government figure — the same
category-4 discipline we already apply to EIA.

**Verdict: CLEARED for commercial and non-commercial reuse.** This is the first
non-EIA input that is **commercial-safe**, which matters for the Phase 2
question §17 raised.

Access notes: e-Stat and Customs serve default clients (verified with plain
curl and Python's default user agent); the script sends an honest project UA.
**METI** (`meti.go.jp`, including its homepage) returned **403** to every probe
— recorded as *403 at origin, unread, not worked around*, like UKMTO/MARAD/OPEC.
An earlier note in this cycle called it a wrong URL; that was corrected when the
homepage also refused.

### 18.3 Design — with a natural split, and a placebo that turned out weak

Origins are grouped by physical route, carried from §15/§17:

| Group | Origins | Route |
|---|---|---|
| Must-transit | Kuwait, Qatar (Iraq/Iran/Bahrain: structural zeros into Japan, excluded) | no bypass — every barrel crosses the strait |
| Bypass-capable | Saudi Arabia, UAE | Yanbu (Red Sea), Fujairah (Gulf of Oman) |
| Regional placebo | Oman | loads at Mina al Fahal, **outside** the strait |
| Non-Gulf | everyone else | — |

Two design corrections made during the run, recorded because they are the kind
of thing that quietly inflates a result:

1. **The non-Gulf group is NOT a placebo here.** In §16/§17 the non-Gulf control
   was independent of the treatment. For Japan it is where the *replacement*
   barrels come from, so it rises when the Gulf falls (+412% June, +682% July,
   on a small base). A "Gulf-vs-control divergence of −716 points" was in the
   first draft output and was **removed** — it is a substitution effect, not
   evidence. The honest demand check is **Japan's total imports** instead.
2. **Oman is a weak placebo**: 18 kb/d calm, and lumpy (−49% in June, +7% in
   July). It does not collapse with the must-transit group (−20% in 2Q26 vs
   −95%), which is consistent with the strait story, but it cannot carry much
   weight.

### 18.4 Results (% of each group's own 2024–25 calm daily rate, by month of arrival in Japan)

| 2026 | Jan | Feb | Mar | Apr | May | Jun | Jul (prov.) |
|---|---|---|---|---|---|---|---|
| Must-transit (KW, QA) | −34 | −45 | −52 | −98 | −100 | −87 | −73 |
| Bypass-capable (SA, AE) | +22 | +15 | +1 | −60 | −60 | −41 | −30 |
| Kuwait alone (calm 153 kb/d) | −23 | −12 | −58 | −100 | −100 | −78 | −55 |
| Saudi alone (calm 936 kb/d) | +72 | +46 | +16 | −60 | −75 | −48 | −27 |
| Oman (weak placebo) | −100 | −3 | −10 | −16 | +4 | −49 | +7 |
| **Japan total (demand check)** | +18 | +12 | −5 | **−60** | **−59** | −22 | +4 |

Findings, in order of how much weight they bear:

1. **Large-sample, robust: Japan's *total* crude imports fell ~60% in April and
   May** (2.36 m b/d base). No importer cuts 60% voluntarily; this is a supply
   constraint arriving in Japan, from a third statistical system with no shared
   pipeline with EIA or Eurostat. Caveat: strategic-stock draws could have
   substituted for part of it, so it bounds the *arrival* shortfall, not the
   transit shortfall.
2. **Robust ordinal split, now reproduced by a third publisher.** In every
   disrupted month the no-bypass origin falls further than the bypass-capable
   one — Kuwait vs Saudi: −100/−60, −100/−75, −78/−48, −55/−27. Same ordering
   as §16 (US weekly: Saudi +16.4%, Iraq −89.0%) and §17 (EU: Saudi −16.7%,
   Iraq −78.2%). Three destinations, three statistical systems, one ordering:
   **production with a route around the strait recovered first.** Ordinal, not
   numerical.
3. **Directional only: the first cleared observation of no-bypass crude with
   3Q26 loadings in it shows partial recovery.** July arrivals (~20–25 day
   voyage → loaded roughly mid-June to mid-July) put Kuwait at −55%, up from
   −100% in April/May. **But this is cargo-count granularity**: Kuwait's calm
   rate is ~2.3 VLCC cargoes a month (153 kb/d × 30.4 days ≈ 4.7 Mbbl; a VLCC carries ~2 Mbbl), so −100% → −55% is roughly *zero cargoes
   to one*. Qatar is at −100% throughout (0–1 cargo/month). A single cargo
   moves these rows by ~40 points. This finding is **not** evidence of a
   magnitude and must never be scaled into one.
4. **Onset**: the must-transit group is already −34/−45% in Jan/Feb arrivals —
   *earlier* than the March onset §13.3 and §17 derived. With Qatar at −98% in
   February on a 0–1-cargo base, this is most likely lumpiness, not an earlier
   onset. Recorded, not explained away; if August/September data show the same
   pattern in Kuwait, revisit.

### 18.5 What this does to critical issue #9

- **Direction: modestly supported.** Transit of no-bypass crude was recovering at
  the Q2/Q3 boundary, not flat — so a flat-persistence 4.9 already looks low for
  early 3Q26, which is the direction of #9. The bottom of the 1.5–6.9 band is
  still supported by nothing.
- **Magnitude: not informed.** The must-transit sample is ~0.25 m b/d (~1.2% of
  calm Hormuz transit) at one-cargo resolution; the large-sample groups are
  bypass-capable and so cannot distinguish transit from re-routing. Any level
  derived from this would be a ratio of small numbers.
- **Recommendation unchanged**: **B now** (widen the band upward, keep 4.9 as the
  point estimate), **C′ not before a 3Q26 chokepoint observation (~November)**.
  Two cycles running, new evidence has *not* moved the recommendation; that is
  the honest outcome, not a failure to update.

### 18.6 Why this input is still worth having, and what it would take to adopt it

- **It is the first commercial-safe non-EIA input**, so if Phase 2 is ever
  proposed, the model is not wholly dependent on one publisher for its
  commercial-safe evidence.
- **It has a forward schedule**: August 2026 9-digit data is due on e-Stat
  around the end of September. That is the next cleared observation of 3Q26
  loadings, well before EIA's 3Q26 chokepoint release (~November).
- **Adoption into the published model** would be as a *regime/recovery signal*
  (e.g. a must-transit recovery indicator feeding the regime detector), not as a
  level. It needs an approved plan, a fresh rubric run, and owner-approved
  `sources.html` copy carrying the PDL1.0 citation **and** the "edited by"
  statement. **No copy was drafted**: `sources.html` must describe what is in
  the model today, and this is not in it.

### 18.7 Limits and not-done, stated so it is not silence

1. July is **provisional**; 9-digit provisional figures are revised.
2. Japan-bound Gulf barrels fell *less* than Hormuz overall (lag-aligned ~−49%
   all-Gulf vs the anchor's −77% in 2Q26). Expected — Saudi/UAE can re-route and
   Japan holds long-term contracts — but it means Japan is **not** a
   representative sample of the strait and must not be treated as one.
3. **Twelfth consecutive cycle with no specialist review** — the Agent tool is
   not available in this session either. This was a CEO reduced-depth pass.
   Mitigation unchanged: the derivation is a script that re-fetches from source.
4. Carried forward unchecked: UN Comtrade, Gulf customs/port authorities, Korea
   (KNOC/KESIS — a natural second importer test, licence unread), India
   (Ministry of Commerce trade data bank — licence unread). UKMTO, MARAD, OPEC,
   METI: 403 at origin, unread.

## 19. KR6 cycle 8 — 2026-09-23 (owner response): option C adopted, persistence replaced

**Delivery type: (b), improve the model.** No new input. STEO Table 3d, cleared
in §13.1, moves from analysis into the published estimator. EIA reuse terms were
re-read first-hand this cycle (`eia.gov/about/copyrights_reuse.php`, HTTP 200,
public-domain grant unchanged). **Status: LIVE since 2026-09-23** (PR #11,
merge `2d98638`, deploy `35852729377`, live bytes identical to `main`). It
replaced persistence (4.9, range 1.5–6.9). *(Earlier the same day: built,
rubric PASS, held in PR #11 for owner copy review.)*

**Authority.** The owner closed critical issue #9 at 2026-09-23T10:34:58Z:
*"Let's go with option C. In the future let's make sure that the CEO has
authority to decide on the used methodology."* The choice of construction below
was made by the CEO under that grant, now written into GOVERNANCE.md
("Methodology authority"). Publishing it then needed the owner's approval
of PR #11. That requirement was retired later the same day, when the owner
gave the CEO publishing authority, and the CEO merged it.

### 19.1 Which "option C" — resolved, with an error in our own record corrected

Three constructions carried similar names across the #9 thread:

| Label | Construction | Figure |
|---|---|---|
| **C (issue #9 body, 2026-09-19)** | last observed transit ratio (2Q26) × latest monthly GPCI | ≈5.9 in the issue text; **5.6** as built (19.2) |
| C′ (§15, 2026-09-20) | bypass-adjusted ratio × GPCI, minus an *assumed* Q3 bypass | 6.5–10.2 by scenario |
| calm-ratio GPCI | calm mean ratio 1.076 × GPCI | ≈15.5 |

§15.4 said "C as originally written would land near 15.5". **That was wrong.** It
conflated C with the calm-ratio row of §13.5's table. The option the owner was
shown was always the last-observed ratio, ≈5.9. So the owner's pick and the
cautious end of the CEO's later recommendation were never far apart. Flagged in
place at §15.4.

**Interpretation adopted:** the owner chose to re-anchor now rather than only
widen the band (B). The construction was then chosen on technical merit, below.

### 19.2 The estimator

```
estimate(d) = r_A × G_m
r_A = Hormuz total oil (quarter A) / mean GPCI over quarter A     (transit share)
G_m = GPCI in the latest month of observed history (STEO "Last Historical Month")
```

As of 2026-09-23: A = 2Q26, H_A = 4.9, GPCI(2Q26) = 11.95, r_A = 0.4099. The
newest month is 202608, GPCI 13.57. **Point = 5.56 → 5.6.**

The issue text's 5.9 used the July–August *average* (14.42). The live
estimator uses the **latest month**, because that is what makes it
monthly-updating and it is what the back-test (19.3) actually tests. August's
dip (−11.1% m/m) is why the figure is 5.6 rather than 5.9.

### 19.3 Back-test, as the live job could actually have run

For target quarter T with anchor A = T−1, the live model is only unsuppressed
from A's publication (~6 weeks after A ends) to 92 days after A ends. In that
window the newest GPCI month is T's first month, then its second. So each target
is scored at those two months, **not** with hindsight GPCI for all of T.

| Target | GPCI month | GPCI-C error | Persistence error |
|---|---|---|---|
| 2Q25 | Apr / May | −0.6% / +0.6% | −0.5% |
| 3Q25 | Jul / Aug | −1.6% / −2.0% | −1.4% |
| 4Q25 | Oct / Nov | +0.9% / 0.0% | −1.4% |
| 1Q26 | Jan / Feb | +45.2% / +51.2% | +45.0% |
| 2Q26 | Apr / May | **+94.4% / +83.7%** | **+204.1%** |

What this says:
- Calm quarters: a tie, within 2.0% vs 1.4%.
- The 1Q26 onset: **no better** than persistence. March's collapse was not
  visible in real time.
- 2Q26: error **roughly halved**.

A hindsight variant (the full target-quarter GPCI) beats persistence in every
quarter. It is **not** the variant the live job can run, so it is not the one
quoted anywhere public. The first write-up of this cycle's work said "beats
persistence in every quarter"; that was corrected before anything was
published.

### 19.4 Why C and not C′

1. **C is back-testable; C′ is not.** C′'s bypass term exists for one quarter
   and needs an assumed Q3 value, the same persistence assumption applied to a
   less observable quantity.
2. **C uses only measured quantities.**
3. **C is the more cautious reading of §16–§18.** All three destination-side
   datasets show recovery concentrated in bypass-capable producers. C lets
   the bypass scale with production (the strait keeps its measured share).
   C′ "bypass persists" holds the bypass fixed, so it routes all the recovered
   output through the strait. That is the more aggressive assumption, and §16
   already called 6.5–10.2 top-heavy.
4. The C′ scenario family still informs the range: its whole span sits inside
   the new band (19.5).

The analysis-only series (EIA weekly imports, Eurostat, Japan customs) informed
this *choice*. **None of them is a computational input**; nothing they report
enters the formula. All three are licence-clear for the site's present
non-commercial use. Eurostat is ambiguous for commercial use, so if a future
cycle ever makes it an input, the §17 category-3 question comes back.

### 19.5 The band — derived by rule, re-derived every run

- **Calm regime:** point ± max(3%, 1.5 × the worst calm back-test miss). Today
  that is ±3.0%.
- **Disrupted regime:** from persistence (H_A, "the strait's volume unchanged
  since quarter A") to the estimator's worst measured disrupted miss, factor
  **k = 1.945** (2Q26 at April GPCI: 9.53 predicted vs 4.9 actual). The miss is
  applied in the direction GPCI has moved since A:
  - rising: [H_A, point × k];
  - falling: [point / k, H_A].

  The point always lies between the two ends.

Today GPCI is rising (13.57 vs 11.95), so the **band is 4.9–10.8**. That
contains every construction the company has tried except calm-ratio 15.5 (which
Iraq's still-collapsed exports contradict) and anything below 2Q26 (which no
cleared Q3 series supports).

**Stated limit:** k was measured only in a *deepening* disruption. Applying it
upward in a recovery assumes the lag error is symmetric, which is **unverified**.
The 3Q26 release (~November) is the first test of it, and the job scores it
automatically.

The page sentence *"headline as its midpoint"* would now be false, so the
generated copy states the asymmetry instead. That change is in the PR.

### 19.6 Unchanged, deliberately

- **Horizon guard: 92 days** from the anchor's end (owner, 2026-09-19). It
  matches the back-test window exactly. The new headline therefore shows only
  until 2026-09-30, then blanks until 3Q26 is published. The durable effect of
  this change starts in November.
- **Extending the horizon:** not attempted. A two-quarter-ahead back-test of C
  (hindsight GPCI, i.e. flattering: 3Q25 +1.0%, 4Q25 +0.3%, 1Q26 +31.3%, 2Q26
  +161%) beats persistence (+341% in 2Q26) but is nowhere near good enough to
  earn a longer horizon, even before the realistic-timing penalty.
- **Regime detector v2:** unchanged.

### 19.7 Latent defects found in the live refresh job, fixed in the same PR

Both were reproduced against `main`'s code before fixing:

1. **Silent.** The Table 4 parser took the first six numbers per row.
   - If EIA *appends* 3Q26, the job ignores it and reports `OK`, so the headline
     stays blank indefinitely after 1 Oct with every build green.
   - If EIA instead *rolls* the table, values land under the wrong quarter
     labels.

   The fix parses by period label and refuses a row whose value count differs
   from the header. This is a pre-emptive category-1 entry in
   `critical-issues-log.md`.
2. **Loud.** Scoring divided by `estimate.point`, which is `None` while
   suppressed, so any EIA release after 1 Oct crashes the job. The fix scores
   the last *published* estimate for the quarter that just landed, alongside
   the persistence counterfactual.

**If PR #11 is declined, fix 1 must be split out and merged before the first
3Q26 release.**

Also added:
- GPCI staleness guard: fail if the newest month is more than 70 days old;
- anchor-quarter completeness check;
- the shared parser in `scripts/gpci.py`.

Edge paths tested:
- suppression;
- 3Q26 arriving while suppressed;
- rolled table;
- falling production;
- stale GPCI;
- broken page;
- extra value in a row;
- idempotent page write.

### 19.8 Limits

1. **One publisher.** The estimate now rests on two EIA datasets. Stated on the
   page.
2. **Transit share is the load-bearing assumption between quarters**, and it
   is the quantity that moves in a disruption. Stated on the page.
3. **GPCI excludes UAE and Qatar** (variable consistency, §13.2).
4. **The static chart** does not gain a 3Q26 bar automatically. Backlog item.
5. **Static dates in `sources.html`** go stale at the next input release.
   Backlog item.
6. **No specialist review, 13th consecutive cycle.** No Agent tool was
   available in this session either. Mitigation: the estimator re-derives its
   own back-test from source on every run and stores it in
   `site/data/hormuz.json` → `model.estimator.backtest`.


## 20. 2026-09-23 (owner governance session): KR6 entry

**Delivery type: none new. The §19 improvement reached readers, and a new
input could not be added this session for the evidenced reasons below.**

1. **What changed for readers.** §19's estimator went live (PR #11). The 2Q26
   back-test error halves against persistence (+84–94% vs +204%), and the
   figure now moves monthly with GPCI. KR6 counted this as its eighth
   delivery when it was built. This entry records that it is now published,
   not a ninth delivery.
2. **Presentation fix that touches the estimate's honesty.** The estimate date
   is now labelled UTC, and the methodology clause says "most recent completed
   day (UTC)". In the suppressed state, the sentence under the block no longer
   talks about a range that isn't shown (PR #12, `16def17`). No figure moved.
3. **Why no new input:**
   - The bucket-2 event/advisory brief (UKMTO, MARAD, sanctions notices) was
     dispatched to Research for real. It failed:
     `No such tool available: Agent. Agent is disabled for this session, in
     subagents as well as here.`
   - Probable cause: the CEO runs as a subagent, and subagents cannot spawn
     subagents. See `okrs.md` finding 0.
   - The session was scoped by the owner to governance changes plus that
     test, so no reduced-depth CEO pass was run.
   - Carried forward unchanged: UKMTO, MARAD MSCI and OPEC are 403 at origin,
     unread (not rejected). UN Comtrade and Gulf customs are unchecked. Korea
     and India licences are unread. Japan August data is due ~end-September.

## 21. KR6 cycle — 2026-09-24: bucket-2 re-probe strengthens two UNRESOLVED leads; Korea checked and rejected; India split partially checked

**Delivery type: (c) — a specific, evidenced reason no new input cleared this cycle, plus genuine narrowing of the search space.** This is the first real dispatch of the Research specialist (the harness fix confirmed working, `decisions-log.md` 2026-09-24). Brief: bucket (2) event/advisory signals for the regime detector, and a second-importer licence check (Korea, India) per the standing backlog item.

**No new numeric input cleared for the model.** One candidate (Korea/KESIS) moved from unread to **REJECTED** on a live first-hand read. One candidate (India/PPAC) moved from unread to **CLEARED but low-value by design** (national aggregate only, no country split, not built as a script). Two candidates (UKMTO, MARAD) remain **UNRESOLVED** but with materially better evidence than before — real terms text and real advisory content were read via Wayback Machine snapshots 10–12 days old, not live, so per the standing guilty-until-checked rule neither is promoted to CLEARED on a cache. OPEC MOMR is unchanged: still Cloudflare-blocked at origin (the "200" response is a challenge page, not content).

**UKMTO** — live 403 confirmed again on every path tried (root, `/about-us`, `/terms-and-conditions`), plus dead alternates (gov.uk mirror 404, NATO Shipping Centre 403, MARLO 403). A 2026-09-14 Wayback snapshot of `/terms-and-conditions` (read live from archive.org 2026-09-24) shows clause 20: *"www.ukmto.org is published under the Open Government Licence."* **Not used as a clearance** — a cache does not substitute for a live read. Flagged as the highest-value single retry for next cycle: if `ukmto.org/terms-and-conditions` ever returns 200, this is likely a fast CLEAR, since OGL is a known, standard, attribution-based UK open licence.

**MARAD MSCI** — live 403 confirmed again across `maritime.dot.gov` and `transportation.gov`. Wayback snapshots (2026-09-12/15/21, read live from archive.org 2026-09-24) surface an **active advisory, "2026-011 — Persian Gulf, Strait of Hormuz and Gulf of Oman — Iranian Attacks on Commercial Vessels," effective 2026-09-09, expiring 2027-03-08** — a named, dated disruption event of exactly the kind the regime detector currently cannot see on its own (it is quarterly-plus-monthly-GPCI, not event-driven). Licence remains genuinely open, not just blocked: DOT's web-policies tree (read via cache) has a system-access disclaimer, not an explicit reuse/redistribution grant comparable to EIA's public-domain statement.

**Korea — KESIS REJECTED.** Live-read `kesis.keei.re.kr` terms of use (HTTP 200, 2026-09-24). Article 15(3) bars copying, reproducing, translating, publishing, or providing to third parties any information obtained via the service without the site's prior consent; Article 16(2) bars distribution, transfer, re-licensing, or commercial use without express approval. Footer: "All rights reserved." Same shape as the JODI-Oil rejection. Not ingested.

**Korea — KNOC UNRESOLVED.** Only adjacent policy pages (privacy; mobile/CCTV) were found and read, not KNOC's actual general terms of use. Every page footer reads "ALL RIGHTS RESERVED" with no reuse grant found, but not called REJECTED without reading the real terms page. `petronet.co.kr` (KNOC's separate statistics portal) redirected and was not followed up.

**India — PPAC CLEARED, low value.** Live-read `ppac.gov.in/terms-conditions` (HTTP 200, 2026-09-24): "Material featured on this website may be reproduced free of charge... the source must be prominently acknowledged," with a standard third-party-material carve-out — broader than Eurostat's grant, no commercial restriction. But the available crude import/export series (`ppac.gov.in/import-export`) is a **national monthly total**, not broken out by partner country, so it cannot support the must-transit-vs-bypass split that makes Japan's series (§18) valuable. No script built — an aggregate-only series would be structurally weaker corroboration than what already exists, and the standing guidance favors a few genuinely useful candidates over many weak ones.

**India — Ministry of Commerce EIDB, the open lead.** `tradestat.commerce.gov.in/eidb/commodityx_countries_wise_import` (HTTP 200, live, 2026-09-24) has exactly the commodity-by-partner-country granularity the design needs (Kuwait/Iraq vs Saudi/UAE, HS 2709), but the live page carries no explicit copyright/reuse statement, only a data-quality disclaimer. Unlike EIA, India's government works are not automatically public domain (Copyright Act 1957); India's standard open licence for this situation is **GODL** (Government Open Data License), used on `data.gov.in`, confirmed present on that portal in general — but whether this specific DGCI&S crude-by-country series is mirrored there under GODL was not confirmed this cycle. **This is the single most promising unresolved lead in the standing brief**: next step is to search `data.gov.in`'s catalog for a matching DGCI&S dataset under GODL before concluding it's a dead end.

**Not attempted, stated so it is not silence**: no user-agent spoofing or other workaround was used on any 403'd source, as instructed. UN Comtrade and Gulf national customs/port authorities remain entirely unchecked and carry forward verbatim.

**Effect on the published figure and `sources.html`: none.** Nothing cleared this cycle that would move the model or the site's source list.

**Two concrete carry-forward items, in priority order**: (1) retry `ukmto.org/terms-and-conditions` live — one HTTP 200 away from a genuine CLEAR; (2) search `data.gov.in`'s catalog for a GODL-licensed DGCI&S crude-oil-import-by-partner-country dataset matching the India EIDB tool.

## 22. KR6 cycle — 2026-09-25: GODL-India verified as a genuine open licence, but the matching DGCI&S dataset is stale or unverified; UKMTO still blocked live

**Delivery type: (c) — one genuinely new, fully-verified licence instrument (GODL-India), but no new numeric input enters the model this cycle.** Brief: retry `ukmto.org/terms-and-conditions` live; search `data.gov.in` for a GODL-licensed DGCI&S crude-by-partner-country dataset; quick KNOC re-check if time allowed.

### 22.1 UKMTO — still UNRESOLVED, 403 confirmed live again

Retried live, 2026-09-25: `https://www.ukmto.org/terms-and-conditions` → **HTTP 403** (curl and, separately, the WebFetch tool, both direct — no user-agent spoofing, no cache, no proxy workaround). Also retried `https://www.ukmto.org/` (403) and `https://www.ukmto.org/terms-conditions` (403). Same block as every prior cycle. **Not promoted.** The 2026-09-14 Wayback snapshot read last cycle (claiming OGL, clause 20) is still just a cache and still does not substitute for a live read under the standing rule. No further UKMTO path is known to try; this item should stop being re-queued every cycle unless UKMTO's infrastructure changes (e.g., a different subdomain, or the 403 lifts) — continuing to spend a cycle re-hitting a URL that has been 403 for three consecutive cycles is not evidence-gathering, it's repetition. Recommend: leave UNRESOLVED and deprioritize below other candidates until there's a reason to believe the block has changed.

### 22.2 India — GODL-India, the licence itself: **CLEARED**, read live

Live-fetched the actual Gazette notification, not a search snippet or summary: `https://data.gov.in/sites/default/files/Gazette_Notification_OGDL.pdf` → **HTTP 200** (curl, 2026-09-25, 1.18 MB PDF, read directly page by page — Ministry of Electronics and Information Technology, Notification F.No. 8(2)/2013-EG-I, New Delhi, 10 February 2017, Gazette of India Extraordinary Part I Section 1, No. 42).

Text read directly, §3 "Permissible Use of Data":

> "all **users** are provided a worldwide, royalty-free, non-exclusive license to **use, adapt, publish** (either in original, or in adapted and/or derivative forms), translate, display, add value, and **create derivative works** (including products and services), for **all lawful commercial and non-commercial purposes**, and for the duration of existence of such rights over the data or information."

§4 conditions: attribution statement in a specified format (data provider, source, license, DOI/URL/URI — template given in §5); no false endorsement by the data provider; no warranty; no guarantee of continued updates. §6 exemptions (personal information, non-shareable/sensitive data, names/logos/official symbols, other IP such as patents/trademarks, military insignia, identity documents, RTI-exempt data) — none of these apply to a trade-statistics dataset. This is an explicit, Gazette-notified, government-wide commercial-redistribution-and-derivative-works grant — clearer and stronger than PPAC's clause (§21) and not comparable to KESIS's "all rights reserved" (§21) or to Eurostat's still-ambiguous commercial question (§17).

**One genuine wrinkle, resolved by reading the document itself rather than assumed:** individual dataset catalog pages on `data.gov.in` show a "Released Under" field naming **NDSAP** (the 2012 policy), not GODL by name, which could look like a different, unverified licence attaches to any specific dataset. Reading GODL's own preamble settles this: *"the open license for data sets published under NDSAP and through the OGD Platform remained unspecified till now"* — i.e., GODL is the specific licence instrument that operationalizes NDSAP for the OGD Platform; its full title in the Gazette is literally "Government Open Data License - India / National Data Sharing and Accessibility Policy." A dataset marked "Released Under: NDSAP" and hosted on the OGD Platform (`data.gov.in`) is the case GODL was written to cover, confirmed independently by the Platform's own Terms of Use (`https://www.data.gov.in/terms-of-use`, live, HTTP 200, 2026-09-25): *"The content published on data.gov.in is owned by the respective Ministry/State/Department/Organization and licensed under the Government Open Data License - India"* (site footer, present on every page checked) and *"Catalog featured on the Open Government Data Platform India, if reproduced, have to be accurate and are not to be used in a derogatory manner or in a misleading context. Wherever the material is being published or issued to others, the source must be prominently acknowledged... The catalog and information available through the Portal are available under terms described in the 'license' metadata element of individual dataset records except where otherwise noted."* No dataset checked this cycle carried an "otherwise noted" override. **Verdict: GODL-India is CLEARED as a licence framework for `data.gov.in`-hosted datasets whose metadata names NDSAP/GODL and carries no contrary note.** This is a genuinely stronger, more explicit grant than several previously-cleared sources and is recorded here so a future cycle does not have to re-derive it.

Separately, `https://data.gov.in/sites/default/files/NDSAP.pdf` was also fetched live (HTTP 200, 2026-09-25, the underlying 2012 policy the "Released Under" field points to) and read directly. It is an inter-governmental data-sharing/access-tier policy (Open/Registered/Restricted access), not itself a copyright-style reuse grant — it requires attribution "in all forms of publications" (§12d) but does not itself state a commercial-use permission. This confirms GODL, not NDSAP alone, is the operative reuse licence; NDSAP is upstream policy context. Recorded so the distinction is traceable.

### 22.3 India — which DGCI&S/Commerce dataset, if any, is actually usable: **CLEARED (licence) but UNRESOLVED (data)**, not adopted

Two Department of Commerce catalog entries were live-checked as *candidates* for the country-broken-out crude series the standing brief wants:

1. **"Commodity And Country Wise Imports In India"** — `https://data.gov.in/catalog/commodity-and-country-wise-imports-india` (live, HTTP 200, 2026-09-25). Released under NDSAP/GODL per §22.2. **Published 24/05/2013, updated 13/02/2014.** This dataset has not been refreshed in over a decade. Licence-clear but **dead as a live input regardless of licence** — there is no plausible way a 2014-vintage series supports a 2026 corroboration signal. Not pursued further.
2. **"Principal Commodity wise Import"** — `https://data.gov.in/catalog/principal-commodity-wise-import` (live, HTTP 200, 2026-09-25). Released under NDSAP/GODL per §22.2. **Published 25/05/2017, updated 31/03/2024** — materially more current, and the only one of the two worth a second look. Catalog description: *"It contains merchandise annual import data of India by principal commodities and countries. Data includes quantity and value in Million USD."* Contributor: Ministry of Commerce and Industry, Department of Commerce (the DGCI&S data chain the brief asked about).

   Two things could not be verified live this cycle, and are recorded as open rather than assumed either way:
   - **Cadence is annual by the catalog's own description** ("annual import data"). Even if it clears in every other respect, this is *weaker* than the model's existing quarterly anchor and no better than what the standing mandate is looking for ("better than quarterly cadence") — it would sit alongside Japan customs and EIA weekly-by-origin as annual analysis-only corroboration at best, not a second numeric anchor.
   - **Whether crude oil (HS 2709) is actually cross-tabulated by partner country**, as opposed to two separate breakdowns (commodities totals; country totals) that don't intersect the way PPAC's aggregate-only series didn't. The underlying resource is not exposed as a plain file on the static catalog page — `data.gov.in`'s API detail page (`https://www.data.gov.in/apis/a2642be0-09b5-414f-a3aa-f6290b2a9c17`, live, HTTP 200) requires generating an API key, which requires logging in / registering an account on the portal. That is an account-creation step. Under `GOVERNANCE.md` ("Outward contact in the owner's name"), creating accounts is flagged as something that stays with the owner's authorization path, not something Research takes unilaterally mid-cycle for a candidate that hasn't even been confirmed to contain the needed cross-tab. **Not registered.** Flagged for the CEO: if this dataset is to be pursued further, either (a) explicit sign-off to register a free data.gov.in account to inspect the resource schema, or (b) find the underlying DGCI&S bulk-download or the `tradestat.commerce.gov.in` EIDB export path (§21) that doesn't require one.

   **Verdict: licence CLEARED (GODL, §22.2), dataset itself UNRESOLVED** — not stale like its sibling, but neither its granularity nor its access mechanism could be confirmed live without an account-creation step outside this cycle's authority. **Not adopted, not built.**

### 22.4 Korea — KNOC, quick retry: still UNRESOLVED, unchanged

Brief web search for KNOC's actual terms-of-use page (`site:knoc.co.kr 이용약관`) surfaced only the same adjacent pages as last cycle — privacy policy (`knoc.co.kr/member/privacy.jsp`), a video-surveillance policy, and a Petronet *member registration* page that mentions 이용약관 only in the context of approving registered access, not a general reuse grant. No general terms-of-use page was found or read. **Unchanged from §21: UNRESOLVED, not REJECTED** — the actual page has still never been located, so there's nothing to read yet. Not pursued further this cycle (this was the explicitly lower-priority, time-permitting item).

### 22.5 Net effect

**No new numeric input enters the model or `sources.html` this cycle.** What changed: (1) UKMTO is confirmed still blocked, with a recommendation to stop re-queuing it as an active retry absent new evidence the block has lifted; (2) GODL-India is now a **fully-verified, live-read, CLEARED licence** for future `data.gov.in` candidates generally — a real, reusable finding for any future Indian-government dataset search, not just this one; (3) the specific DGCI&S dataset hoped for is narrowed from "unchecked" to a precise state — one candidate dead (stale), one candidate licence-clear but data-unresolved pending either an account-creation decision or a no-login alternative path; (4) KNOC unchanged. `site/` and `site/data/hormuz.json` untouched, per this cycle's scope.

**Carry-forward, in priority order:** (1) CEO/owner decision on whether to authorize a `data.gov.in` account registration to inspect the "Principal Commodity wise Import" resource schema, or find a no-login bulk-download/API path for it or the `tradestat.commerce.gov.in` EIDB tool (§21); (2) UN Comtrade and Gulf national customs/port authorities remain entirely unchecked, carried forward verbatim from §21; (3) OPEC MOMR remains Cloudflare-blocked, carried forward verbatim; (4) UKMTO and KNOC deprioritized per above absent new evidence.
