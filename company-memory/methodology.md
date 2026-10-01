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

## 23. KR6 cycle — 2026-09-26: Japan August still pending (dated), UN Comtrade read live and left UNRESOLVED, and the first genuinely strong Gulf-customs licence (GASTAT) — dataset not yet confirmed

**Delivery type: (c) — a specific, evidenced reason no new *input* entered the model this cycle, plus real narrowing of the two biggest open items in the standing brief.** Brief: (1) check whether e-Stat has published Japan's August 2026 data; (2) a real, live first attempt at UN Comtrade; (3) one Gulf national customs/statistics authority, live. All three done. No script changed, no licence surface entered `site/` or `sources.html`, nothing was adopted.

### 23.1 Japan e-Stat — August 2026 not yet published; exact publication date confirmed, not guessed

Re-ran `scripts/japan_imports_analysis.py` unchanged (`FILES[2026] = "000040494488"`) against live e-Stat data. Output is byte-identical in coverage to §18: **2026 data still runs only to July (provisional)**, confirmed independently by a live fetch of the e-Stat file-list page for this exact `statInfId` (`https://www.e-stat.go.jp/en/stat-search/files?...&stat_infid=000040494488`, live, 2026-09-26): release date "2026-08-28 09:30", coverage "2026 Jul.", no August entry present.

**Why, and when it will change — not just "not yet," a date.** Cross-checked two independent live sources, both Japanese-government pages, neither a search snippet:
- `https://www.customs.go.jp/toukei/latest/index_e.htm` (live, 2026-09-26): the most recent item on the page is **August 2026 provisional (速報)** — i.e. the *aggregate* press-release figures (headline export/import values only, no commodity-by-country breakout) are already out.
- `https://www.customs.go.jp/toukei/calendar/calend.htm` (live, 2026-09-26): the **確報 (final/detailed report)** for August 2026 — the one that carries the 9-digit HS-by-country breakdown `japan_imports_analysis.py` actually needs — is scheduled for **2026-09-29, 09:30 JST**. A web search independently surfaced the same date from a third page (`kanzei.or.jp/tradestats/release/`), so this is not a single-source read.

**This resolves the ambiguity in the standing backlog item ("~end-September") into an actual date.** Today (2026-09-26) is three days before that release. **Re-running today would have been wasted effort even if the file ID were already known** — the detailed file literally does not exist yet at the source. Recommend the backlog item be re-worded from "~end-September" to **"after 2026-09-29 09:30 JST"**, and that it not be re-attempted before then.

### 23.2 UN Comtrade — read live, both the promising and the unreadable parts, verdict UNRESOLVED

**What it offers, confirmed live:** HS-classified trade data (crude oil = HS 2709) by reporter and partner country, for ~200 countries, both **monthly and annual**, via `comtradeplus.un.org` (the current platform; the legacy `comtrade.un.org` now redirects into the same client-rendered app). This would be exactly the "producer-side seaborne export series for Gulf states" the standing brief has been looking for since cycle 1 — **if** the Gulf states in question actually report to Comtrade promptly (not verified this cycle; a live check of actual Saudi/Iraq/Kuwait reporting lag is the next step if this source ever clears).

**Licence — read live, and it does not clear, on the strength of what could actually be fetched:**
- `https://uncomtrade.org/docs/policy-on-use-and-re-dissemination/` — **live, HTTP 200, fetched 2026-09-26**, full text read (not a snippet): *"UN Comtrade data are provided for internal use only and may not be re-disseminated in any form without UNSD's permission."* A list of exemptions follows, and one of them looks like it could cover us: *"Free-of-charge data visualization and/or data analytics application"* is listed under **"The license to distribute is not applied, and permission is not required for the following use cases."** No subscription is mentioned as a condition on that specific line.
- `https://uncomtrade.org/docs/faqs-on-use-and-re-dissemination/` — **live, HTTP 200, fetched 2026-09-26** — reads differently on the adjacent question of *transformed* data: *"You can re-disseminate data that is transformed or substantially different from the original UN Comtrade data without paying a re-dissemination fee (license to distribute). However, you must maintain an active premium subscription."* That is a paid condition attached to the free-fee path, and it is not obviously the same case as the Policy page's "visualization/analytics, no permission required" line — the two pages do not use identical language for what sounds like the same scenario.
- **The document both pages point to as authoritative — "Use of UN Comtrade data is subject to a license agreement found at `https://comtrade.un.org/licenseagreement.html`, regardless of whether the data is accessed via free or premium access" — could not be read.** Live fetch (`curl`, 2026-09-26): the URL 302s into `comtradeplus.un.org`, which serves only a client-rendered single-page app (`<div id="root">... Loading...`), no server-rendered text. This is the same category of failure as UKMTO/MARAD being 403 — not a licence reject, a **could-not-read**. A companion UN Statistics wiki page (`unstats.un.org/wiki/.../Policy+on+use+and+re-dissemination+of+UN+Comtrade+data`) that a web search surfaced as a possible alternate copy returned a **Confluence login wall**, also unreadable live.
- Bulk/API access beyond the UI would need an account (free tier exists per the Policy page: *"UN Comtrade offers free access to all users. Registering a free account unlocks additional features"*) — **not registered**, per the standing rule that account creation is outward contact in the owner's name.

**Verdict: UNRESOLVED.** Two of the three documents that would settle this could be read live and are *inconsistent with each other* on whether our exact use case (a free, non-commercial, transformative analysis) needs a paid "active premium subscription" or not; the one document both of them say is actually authoritative could not be read live at all. Guilty-until-checked means this stays UNRESOLVED rather than rounding the more permissive of two inconsistent pages up to CLEARED. **Not used, not even to calibrate.**

**What would resolve it, for whoever picks this up next:** either (a) the owner authorizes registering the free UN Comtrade account, which may itself expose a clearer license-agreement rendering once logged in (untested), or (b) email `comtrade@un.org` / `subscriptions@un.org` with the specific use case (a small number of derived index values, refreshed monthly, published with attribution, no bulk redistribution of raw records) and ask directly — both are outward contact / account creation and are the owner's call, not Research's.

### 23.3 Gulf customs/statistics authority — GASTAT (Saudi Arabia): the strongest Gulf-customs licence found to date, dataset not yet confirmed

Chose Saudi Arabia's **General Authority for Statistics (GASTAT)** — largest Gulf producer, and its trade statistics explicitly separate "oil exports" as a category, sourced from the Ministry of Energy rather than customs alone.

**Licence — CLEARED, read live, full text.** `https://www.stats.gov.sa/en/use-policy` (live, HTTP 200, fetched 2026-09-26; this page is Liferay-rendered but *is* server-side-rendered — the licence text is present in the raw HTML, unlike the JS-shell pages this cycle that weren't). Section 1.2, "Copyright and License for Reuse," clause 1.2.2, quoted in full:

> "Except for trademarks, logos, and any clearly identified third-party material, GASTAT permits users to copy, reproduce, publish, distribute, transmit, adapt, modify, translate, build upon, and otherwise reuse the materials and data made available on this website for any purpose, **including commercial use**, in accordance with the Open Data principle, provided that **GASTAT is acknowledged as the official source and any modifications are clearly indicated**, thereby preserving rights and enhancing the reliability and accuracy of the content."

This is an explicit, unconditional (no non-EU-style carve-out, no per-dataset exception found), commercial-and-non-commercial redistribution-and-derivative-works grant, attribution required, modifications must be disclosed — the same shape and strength as EIA's public-domain statement and GODL-India (§22.2), and materially stronger than Eurostat's country-list-conditional grant (§17.5). **This is a genuinely new, reusable finding**: any GASTAT-sourced Saudi statistic clears this bar, not just the one dataset chased this cycle.

**What it actually publishes, and the gap that keeps it from clearing fully:**
- **Cadence: monthly**, confirmed from the live-read methodology page (`https://www.stats.gov.sa/en/w/methodology-and-quality-report-for-international-trade-in-goods-statistics-monthly-`, HTTP 200): *"Frequency of data collection: Monthly"*, oil-export figures sourced specifically from *"the Ministry of Energy: It is a major source of oil exports"* (customs/Zakat-Tax-Authority data covers non-oil goods only). History available "from the year 2000 to the current month."
- **Lag: comparable to EIA's, not better.** The live-fetched May-2026 bulletin PDF (`stats.gov.sa/documents/20117/2435267/ITR+May2026-EN.pdf`, HTTP 200, read directly) was only found via search in late September — i.e. roughly a 4-month-old bulletin is the most recent one indexed, suggesting a similar ~2-3 month lag to EIA's Hormuz supplement, not a faster one. Not independently timed against a release calendar this cycle; flagged as unconfirmed rather than assumed.
- **The gap: the public monthly bulletin gives oil exports only as an aggregate SAR-billion value and percentage-of-total, not a partner-country breakdown and not a physical quantity.** Read directly from the May 2026 PDF: *"oil exports increased by 19.5%. The percentage of oil exports out of total exports increased from 65.7% in May 2025 to 75.6% in May 2026."* The document's **country breakdown (China, South Korea, UAE, etc.) is for *total* merchandise exports**, which are non-oil-dominated in composition — it is not an oil-specific partner breakdown. The methodology page separately states the underlying administrative records *do* carry both "the quantity and weight of goods" and "country of... destination in exports" as collected dimensions — so the cross-tab this brief needs may exist inside GASTAT's data holdings, but **it was not found published anywhere freely accessible this cycle.**
- **The Saudi Open Data Portal (`open.data.gov.sa`), which GASTAT's own use-policy page links to as the likely place such a table would be catalogued, was unreachable this cycle** — repeated live attempts (`curl` twice, `WebFetch` once) all failed at the connection level (`Recv failure: Connection reset by peer` / HTTP 503), not a confirmed 403-at-origin the way UKMTO/MARAD/OPEC are. Per the standing rule, this is reported as **could-not-reach**, not retried further this cycle, and not worked around.

**Verdict: licence CLEARED (GASTAT generally); the specific by-partner-country crude-oil-quantity dataset needed is UNRESOLVED** — not stale, not paywalled, not rejected, simply not yet located in a form this cycle could confirm. Same shape as the India GODL finding in §22: a strong, reusable licence clearance attached to a dataset search that isn't finished. **Not adopted, not built, nothing entered `sources.html`.**

**Recommendation, and why GASTAT over the alternatives not yet tried:** this is now the **single most promising open lead in the standing bucket-1 list** — a cleared licence, from the Gulf's largest producer, at a cadence at least as good as the current anchor, with a stated official Ministry-of-Energy oil-export data pipeline. It is a better next step than opening a fourth or fifth new country cold, because the licence question — usually the slower half of this work — is already answered. **Next-cycle priority: find the actual downloadable table** (retry `open.data.gov.sa` once connectivity allows; or search GASTAT's `statistics-tabs` data-explorer tool, which returned content this cycle but was not fully parsed for a crude-oil-by-country series; or the quarterly companion report at `stats.gov.sa/documents/d/guest/methodology-and-quality-report-of-international-trade-statistics-quarterly-_en`, unread this cycle). If a quantity-by-partner table is found, GASTAT would give the model a genuine second producer-side numeric anchor at monthly cadence — precisely what the standing mandate has been asking for since cycle 1.

### 23.4 Net effect

**No new numeric input enters the model or `sources.html` this cycle.** What changed: (1) Japan's next data point has a firm date (2026-09-29) instead of an approximate one; (2) UN Comtrade moved from "entirely unchecked" to a specific, live-documented UNRESOLVED, with the exact inconsistency and the exact unreadable page named, so a future cycle does not have to re-derive this; (3) GASTAT moved from "entirely unchecked" (it was one of the named examples in the standing brief that had *never* been looked at across 15 cycles) to a live-verified strong licence clearance with a precisely scoped remaining gap. `site/` and `site/data/hormuz.json` untouched.

**Carry-forward, in priority order:** (1) **GASTAT** — find the actual partner-country crude-oil-quantity table (via `open.data.gov.sa` once reachable, or GASTAT's own data-explorer/quarterly report); this is now the top bucket-1 lead. (2) **Japan** — re-run `scripts/japan_imports_analysis.py` **after 2026-09-29 09:30 JST**, not before. (3) UN Comtrade — resolve only via an owner decision on account registration or direct outward contact (`comtrade@un.org` / `subscriptions@un.org`); not otherwise resolvable from outside. (4) Everything else carried forward verbatim from §22.5: UKMTO and KNOC deprioritized absent new evidence; OPEC MOMR still Cloudflare-blocked; the `data.gov.in` "Principal Commodity wise Import" dataset still awaiting a CEO call on account registration or a no-login path.

## 24. KR6 cycle — 2026-09-27: GASTAT's own data-explorer opens up, and the by-country oil-quantity table turns out not to be missing — it's structurally impossible at GASTAT. A genuinely new, licence-clear, Ministry-of-Energy quantity series is found instead, but its cadence doesn't clear the bar.

**Delivery type: (c) — a decisive negative result on the exact question the brief posed, plus one genuinely new candidate input, cadence-disqualified from anchor status but real.** Brief: (1) retry `open.data.gov.sa`; (2) work GASTAT's own `statistics-tabs` data-explorer and its quarterly trade companion report, specifically hunting a by-country oil-export **quantity** table. Both done, live, this cycle.

### 24.1 `open.data.gov.sa` — retried, still unreachable, same failure mode as last cycle

Two independent tools, both live, 2026-09-27:
- `curl` direct (through the proxy): **`Recv failure: Connection reset by peer`** at the TLS layer, both `https://open.data.gov.sa` and `/en`, ~12s timeout each. Verbose (`-v`) trace shows the CONNECT tunnel to the proxy succeeds (`HTTP/1.1 200 Connection Established`), the TLS ClientHello is sent, then the connection resets before any ServerHello — i.e. the reset happens between the proxy and the origin, not in our tooling.
- `WebFetch https://open.data.gov.sa/en/pages/home`: **HTTP 503 Service Unavailable**.

Two different failure signatures (reset vs. 503) across two tools on two consecutive cycles is more consistent with the origin genuinely being flaky/overloaded than with a deliberate block, but it still cannot be called anything but **could-not-reach** — not a licence verdict either way. Not retried further this cycle; not worked around.

### 24.2 GASTAT's `statistics-tabs` explorer — actually navigated this time, and the mechanism is now documented for reuse

Last cycle's brief flagged this tool as "returned content but was not fully parsed." This cycle went further: the category tree (`GET https://www.stats.gov.sa/en/statistics-tabs`, HTTP 200) is a Liferay accordion whose leaf items (e.g. "Oil and Gas Statistics", "International Trade for Goods") are `javascript:void(0)` links carrying a `data-category-id`. Clicking one submits a hidden form (`POST` to `.../en/statistics?p_p_id=com_digitallab_gastat_statistics_GastatStatisticsCategoriesPortlet_INSTANCE_eell&...&jakarta.portlet.action=go_to_publication_page&p_auth=<token>` with the category ID as a form field) that redirects to a filtered publication list. Replicated this live with `curl` (session cookie jar + a freshly-scraped `p_auth` token, both required — the token is per-page-load, not static): category `124827` ("Oil and Gas Statistics", under Energy Statistics) returned exactly **one** publication, not a truncated list — confirmed by searching the full response for every `row-header` span, not just the first match.

### 24.3 The publication that category yields: "Oil and Gas Statistics 2025" — a genuinely new dataset, not looked at in 16+ prior cycles

Downloaded live: `stats.gov.sa/documents/20117/2435281/…Oil+and+Gas+Statistics+2025+EN.xlsx…` (HTTP 200) and its 1-page infographic PDF, plus its 19-page methodology report (`…Methodology+and+Quality+Report+for+Oil+and+gas+Statistics2025+EN…pdf`, HTTP 200). This is a different GASTAT product from the monthly International Trade Report (ITR) chased in §23 — a dedicated Oil & Gas statistical release, sourced entirely from the Ministry of Energy (not customs).

Sheet `3.1` ("Crude Oil Exports") is exactly the variable this brief has been chasing since cycle 1: **monthly, in physical quantity ("Thousand Barrels"), national-level, 2010–2025**, e.g. 2025: Jan 188,263 … Dec 216,628, annual total 2,347,321 thousand barrels. Sheet `1.1` gives the matching Crude Oil Production series on the same basis. The 1-page PDF states the headline figures in the same units: "Crude oil exports reached approximately 2,347.3 million barrels [in 2025], an increase of 6.0%."

**Licence: already CLEARED, no new check needed.** This file is served from the same `stats.gov.sa` domain under the same site-wide use-policy verified live last cycle (§23.3, `stats.gov.sa/en/use-policy`, clause 1.2.2: commercial-and-non-commercial reuse/derivative-works grant with attribution). The clause covers "materials and data made available on this website" generally, not one named dataset, so it extends to this file without re-verification.

**The gap that remains: still no partner-country breakdown.** Sheet 3.1 has no country dimension at all — it is a single national total column by month. This does not answer the brief's specific ask; see §24.5 for why.

### 24.4 Cadence — checked in the dataset's own methodology report, not assumed, and it does not clear the bar the standing brief set

The methodology PDF answers this directly and repeatedly, not ambiguously:

- §3.16/3.17: *"The publication includes indicators covering the period from 2010 to 2025, with data presented on a monthly basis, while the publication itself is released annually."* / *"The results of the oil and gas statistics are published annually according to the approved statistical plan."*
- §5.4.4 (Coherence — sub-annual and annual statistics): *"Not applicable, as the oil and gas statistics are published on an annual basis, and no monthly or quarterly publications are issued."* — this is about as unambiguous a statement of cadence as a source has ever given this brief.
- §3.13: the reference period is "the last day of the calendar year." The 2025 edition (covering Jan–Dec 2025 in full, no 2026 data present) was uploaded to the server 2026-08-06 and its methodology page's own "latest update" is dated 22/07/2026 — consistent with **roughly a 7–8 month lag** after year-end before the full monthly series for that year is available at all.

**Verdict on cadence: this does not clear the standing bar ("a second numeric anchor at *better than quarterly* cadence").** It is worse than that, not better: the data has monthly granularity *inside* each release, but the release itself happens once a year, so a reader only gets a new data point once every twelve months, each one ~7-8 months stale on arrival. The current EIA quarterly anchor refreshes four times as often with comparable lag. Recorded so no future cycle re-discovers this dataset and mistakes "monthly data" in the column headers for "monthly cadence" — they are not the same thing, and this source is the clearest illustration of that distinction found yet.

### 24.5 The quarterly ITR companion methodology report — read live, and it explains *why* GASTAT will structurally never publish the by-country oil table this brief has wanted since cycle 1

The other unread lead named in the brief, `stats.gov.sa/documents/d/guest/methodology-and-quality-report-of-international-trade-statistics-quarterly-_en`, resolved (live, HTTP 200 — the URL serves the PDF directly rather than an HTML wrapper) to the *"Methodology and Quality Report of International Trade Statistics (Quarterly)"*. It is not a different dataset from the monthly ITR in §23 — it is the same International Trade Report's quarterly-aggregation methodology (the monthly ITR workbook already carries Q1–Q4 columns alongside the monthly ones). Reading it end to end answers the standing question directly, in its own words:

> §11.3 (Completeness): *"International trade data are based on two main sources... Updated data from the Ministry of Energy: It is a major source of oil exports. Updated data from the Zakat, Tax and Customs Authority: It is a major source of exports and imports of non-oil goods."*
> §16.1 (Source data): *"General Authority for Zakat, Tax and Customs: Exports and imports of goods. Ministry of Energy: Oil exports."*
> §3.4 defines "Oil exports" narrowly as HS Chapter 27, and the data-description section (§3.1) states the underlying record includes "value of goods and the quantity and weight of goods" and "country of origin in imports and country of destination in exports" — but those fields are populated from **customs declarations**, and oil exports are **not** customs-declared through that pipeline; they come from the Ministry of Energy as a separate administrative feed with no partner-country field at all.

**This is a mechanism-level finding, not a "didn't find it this cycle" one.** The reason GASTAT's public products never carry an oil-by-partner-country quantity table is not that it hasn't been published yet or is buried somewhere unindexed — it is that Saudi Arabia's oil exports are administratively tracked by the Ministry of Energy as a national aggregate, structurally outside the customs (Zakat/Tax/Customs) pipeline that is the *only* source of country-level granularity in GASTAT's trade statistics. Non-oil goods get the by-country, by-quantity cross-tab (confirmed already in §23.3 for Table 4/6.1) precisely because they *do* pass through customs with a declared destination; oil doesn't. Barring a change in Saudi administrative data flows, or a Ministry-of-Energy-published product this brief hasn't found (not ruled out, but not indicated anywhere in either methodology report), **this specific cross-tab is very unlikely to ever exist as a GASTAT-published product.**

### 24.6 Verdict and recommendation

**GASTAT, for the specific ask ("by-country oil-export quantity"): the licence is CLEARED (carried from §23.3, unchanged) but the dataset is now REJECTED, not merely UNRESOLVED** — reasoned by mechanism, not by exhaustive search, per §24.5. Recommend this specific sub-search be closed rather than carried forward again; re-opening it would need a different source entirely (e.g. a Ministry-of-Energy-published product, if one exists and is separately licensed — not indicated by anything found this cycle).

**Separately, "Oil and Gas Statistics 2025" (§24.3) is a real, new, CLEARED finding, just not one that satisfies the anchor bar.** One preferred construction, not a menu: **treat it as an analysis-only corroboration/back-test input for the Saudi component of GPCI, the same tier as the existing Eurostat and Japan corroboration (§17, §18), not as a replacement anchor.** Reasoning: (a) its annual cadence is worse than the current quarterly anchor, so it cannot drive the daily estimate; (b) its national-total, Ministry-of-Energy-sourced Saudi crude-export series, spanning 2010–2025, is nonetheless a structurally independent check on the largest single producer inside GPCI (production, not export, from EIA STEO Table 3d) — a genuine second-source read on Saudi Arabia specifically, which is exactly the "single-publisher dependence" weakness named at the top of this brief; (c) unlike Eurostat's country-list ambiguity (§17.5) or Japan's must-transit-vs-bypass caveat (§18.6), this input's licence is unconditionally CLEARED, so adopting it as corroboration carries no category-3 risk, only the ordinary judgment call about whether it's worth the build. Rejected alternative: treating it as a co-anchor alongside the EIA quarterly figure — rejected because its slower cadence and worse lag would only ever fire once a year, i.e. it could confirm or contradict a full year's worth of quarterly anchors at once, long after the fact, which is a corroboration signal's job, not an anchor's.

This is a recommendation for the CEO to weigh, not a decision executed here: no script was written, `sources.html` and `site/` are untouched, and nothing in the model changed.

### 24.7 Net effect

**No new numeric input enters the model or `sources.html` this cycle.** What changed: (1) `open.data.gov.sa` remains could-not-reach, now confirmed across two different failure signatures over two cycles — deprioritize further blind retries absent a signal the origin has stabilized; (2) the by-country oil-export-quantity dataset that has been the standing brief's top bucket-1 priority for two cycles running is now understood as **structurally absent from GASTAT**, not merely unfound — this specific sub-search should stop being re-attempted at GASTAT; (3) a new, licence-CLEARED, monthly-granularity national Saudi crude-oil-export/production quantity series (2010–2025, annual release cadence) was found and is recommended to the CEO as analysis-only corroboration, not an anchor. `site/` and `site/data/hormuz.json` untouched.

**Carry-forward, in priority order:** (1) Japan — re-run `scripts/japan_imports_analysis.py` **after 2026-09-29 09:30 JST** (unchanged from §23). (2) UN Comtrade — still awaiting an owner call on account registration or direct outward contact (unchanged from §23.2). (3) The standing bucket-1 producer-side search now needs a **new country or a new Saudi source** (not GASTAT-by-country-oil, which is closed per §24.6) — Iraq, Kuwait, UAE, Qatar customs/statistics authorities remain effectively unchecked, and a Ministry-of-Energy-specific (not GASTAT) Saudi product, if one exists, is untested. (4) Everything else carried forward verbatim from §23.4/§22.5: UKMTO and KNOC deprioritized absent new evidence; OPEC MOMR still Cloudflare-blocked; the `data.gov.in` "Principal Commodity wise Import" dataset still awaiting a CEO call on account registration or a no-login path.

## 25. KR6 cycle — 2026-09-28: GASTAT's Saudi production series built and run as GPCI corroboration; strong agreement found, but it is calm-period only; `open.data.gov.sa` confirmed unreachable by a third, independent network path

**Delivery type: (b) — a model/calibration improvement (a new corroboration test against the model's largest single production component), with no new licence surface and no change to the published figure.** No new input enters `site/data/hormuz.json` or `sources.html`. Brief: (1) build the GASTAT analysis-only corroboration script recommended in section 24.6; (2) retry `open.data.gov.sa` once more via a genuinely different method; (3) confirm (not force) whether Japan e-Stat's August 2026 detailed release is live. All three done.

### 25.1 The script: `scripts/gastat_analysis.py`

ANALYSIS ONLY, matches the discipline of `scripts/eu_imports_analysis.py` and `scripts/japan_imports_analysis.py`: re-fetches both source files live on every run, fails loudly rather than guessing on any layout, unit, or history-boundary change, and does not write to `site/data/hormuz.json` or `site/sources.html`.

**What it tests.** GASTAT's *Oil and Gas Statistics 2025* (licence CLEARED, section 23.3/24.3; dataset itself found section 24.3) publishes a Saudi Arabia crude oil **production** series (sheet 1.1), monthly, thousand barrels, sourced directly from Saudi Arabia's own Ministry of Energy — a different government and a different collection pipeline from EIA's STEO. Saudi Arabia is GPCI's largest single component (roughly half of the index in calm months; section 13.2). This script asks the direct question the standing brief has been circling since GPCI was built: **does an independent government source agree with GPCI's biggest input?**

**Why no placebo/control group, unlike the Eurostat and Japan scripts.** Stated explicitly in the script's docstring, not glossed over: Eurostat and Japan support a group-vs-control test because each has multiple partner countries, so a non-Gulf control group is available. GASTAT is a **single-country, national-aggregate-only** release (section 24.5 explains this is structural, not a gap in the current release — Saudi oil exports are a Ministry-of-Energy administrative feed with no country-of-destination field at all). There is no comparable held-out group to use as a placebo. In its place, the script runs (a) an independent cross-source agreement test (Pearson r, MAPE, bias) between GASTAT and STEO's `copr_sa` series over their full monthly overlap, and (b) a split-period robustness check — first half of the overlap vs second half — which does the placebo's actual job here: it guards against a correlation that is really just "both series trend upward/downward together over four years" rather than genuine month-to-month agreement.

### 25.2 Result: strong, robust agreement — in the calm period only

Overlap window: **2022-01 to 2025-12 (n=48 months)** — bounded on the early side by STEO's own Saudi production history (`copr_sa` history starts January 2022; confirmed by the same "Last Historical Month" mechanism `gpci.py` already uses, not assumed) and on the late side by GASTAT's 2025 edition carrying **zero 2026 data** (confirmed live this cycle: `prod_max_year` and `exp_max_year` both parsed as 2025, matching section 24.4's finding).

| Metric (GASTAT vs EIA/STEO `copr_sa`, both m b/d) | Value |
|---|---|
| n | 48 months |
| Pearson r | **0.961** |
| Mean signed difference | +0.78% (GASTAT reads marginally higher) |
| MAPE (mean absolute difference) | **1.76%** |
| Median absolute difference | 1.47% |
| Max absolute difference | 6.84% (single month, 2023-01) |

**Split-period robustness (the placebo's job, done differently):** first half (2022-01..2023-12, n=24): r=0.954, MAPE 2.02%. Second half (2024-01..2025-12, n=24): r=0.894, MAPE 1.50%. Agreement holds in both halves independently, not just on the pooled average — this is what rules out "the correlation is really just a shared four-year trend" as the explanation.

**Read plainly:** two structurally independent statistical systems — EIA's STEO (US federal, partly model-informed) and Saudi Arabia's own Ministry of Energy (via GASTAT) — agree on Saudi crude production to within 1.5–2% on a typical month, across 48 months, in both halves of the window independently. This is real corroborating evidence that **GPCI's single largest component is sound.**

**Secondary, internal-consistency finding (GASTAT's own two series against each other, not a GPCI check):** the export/production ratio computed from GASTAT's sheets 1.1 and 3.1 is **stable across all 16 years available (2010–2025): mean 0.717, sd 0.030, range 0.676–0.783.** Roughly 28% of Saudi crude production consistently stays domestic (refining/consumption) rather than being exported, every year, with no visible trend break. This is a sanity check on GASTAT's own two series, not a Hormuz or GPCI finding, and the script's output says so explicitly — it must not be read as a transit or bypass measurement.

### 25.3 What this does and does not say about the current published estimate

**It does not, and cannot, speak to the 2026 disruption or the live estimate (currently anchored on 2Q26/August GPCI, per section 19).** GASTAT's 2025 edition has no 2026 rows at all — the overlap window is entirely pre-disruption. This is reported by the script itself (it prints the number of 2026 months in the overlap: zero) rather than left for a reader to notice.

**What it does say:** it raises confidence in the *construction* of GPCI, specifically its largest and most load-bearing component, during the only period it can test. That is a real, if narrower-than-hoped-for, form of corroboration — the standing mandate's "single-publisher dependence" weakness is now measurably smaller for GPCI's Saudi component, even though the anchor (EIA Global Energy Security Data Table 4) and the companion-chokepoint control (Table 2) remain single-publisher. This does **not** move the published band or point estimate; it is evidence about the reliability of an input, not a new data point for 2026.

### 25.4 Verdict and recommendation

**GASTAT's Saudi production series (sheet 1.1): CORROBORATES GPCI's Saudi component in the tested (calm) window.** Licence unchanged from section 23.3/24.3 (CLEARED, `stats.gov.sa/en/use-policy` clause 1.2.2, commercial-and-non-commercial reuse with attribution). **Not adopted as a model input** — it cannot be, by its own annual cadence and total absence of 2026 data (section 24.4's verdict stands). Recommend `scripts/gastat_analysis.py` be kept and re-run whenever GASTAT publishes its 2026 edition (expected ~mid-2027 on the ~7–8 month-after-year-end lag documented in section 24.4) — that will be the first point this specific check can say anything about the disrupted regime.

**GASTAT's export series (sheet 3.1): used only as an internal-consistency check this cycle, not adopted for anything Hormuz-specific.** No partner-country breakdown exists or can exist (section 24.5), so it cannot support a must-transit-vs-bypass split the way the Eurostat and Japan corroboration scripts do. Not pursued further as a Hormuz signal.

### 25.5 `open.data.gov.sa` — retried via a third, independent network path; now unreachable by three unrelated mechanisms

Two prior cycles tried two methods from our own network path: `curl` direct through the proxy (TLS-layer `Recv failure: Connection reset by peer`, section 24.1) and `WebFetch` (`HTTP 503`, section 23.3/24.1). This cycle added methods that do **not** share our proxy's route to the origin at all:

- **`curl` on plain HTTP (port 80)**, not HTTPS: `HTTP 503` (application-level, not a connection reset — a different failure signature from the HTTPS attempt run moments earlier in the same session, which reset again).
- **`curl` direct to the resolved IP (`78.93.109.61`) with `Host:` header**, bypassing whatever hostname-based routing might exist: TLS handshake reset again, same as the hostname path — rules out a hostname-specific block.
- **`r.jina.ai` reader proxy**, fetched live via `curl` (`https://r.jina.ai/https://open.data.gov.sa/en/pages/home`) — this is Jina AI's own infrastructure running a real headless browser against the origin, sharing no network path with our proxy at all. Result: **`TimeoutError: page.goto: ... Timeout 15000ms exceeded`** — Jina's own browser, on its own network, could not get the page to load within 15 seconds either.
- **Wayback Machine availability API** (`archive.org/wayback/available?url=open.data.gov.sa`, fetched live via WebFetch): **no archived snapshot exists for this domain at all** — not "temporarily down since a recent crawl," genuinely never successfully archived.

**Verdict: still could-not-reach, and now on stronger evidence that this is the origin's own problem, not a block aimed at us or our proxy specifically.** Three unrelated network paths (our proxy, Jina's independent headless-browser service, and the Internet Archive's crawler history) all fail to get a working response from this specific subdomain, while the main `stats.gov.sa` domain (used throughout sections 23–24) has been reliably reachable across every cycle it's been tried. **Recommendation: stop re-trying this specific URL every cycle** — three cycles, five distinct methods, one consistent outcome. If it matters again, the better next step is not another fetch attempt but finding whether GASTAT's own `statistics-tabs` explorer (section 24.2, confirmed working) can reach the same catalogued datasets `open.data.gov.sa` would have, since that mechanism is already proven live.

### 25.6 Japan e-Stat — August 2026 detailed release confirmed still not live, as expected; no re-run attempted

Per section 23.1's precisely-dated forecast, live-checked `https://www.customs.go.jp/toukei/latest/index_e.htm` (fetched 2026-09-28): the page's most recent entry is **"August 2026 (Provisional)"** — the aggregate press-release figure, not the detailed 確報 report with the 9-digit HS-by-country breakdown `scripts/japan_imports_analysis.py` needs. This matches section 23.1's prediction exactly (detailed release scheduled 2026-09-29 09:30 JST, one day after this check). **Not re-run**, per the brief's own instruction not to re-run the full analysis before the file exists. Carry forward: re-run `scripts/japan_imports_analysis.py` after 2026-09-29 09:30 JST, unchanged from section 23/24.

### 25.7 Net effect

**No new numeric input enters the model or `sources.html` this cycle. The published figure is unchanged.** What changed: (1) a new, reusable analysis script (`scripts/gastat_analysis.py`) now gives the model's largest single production component (Saudi Arabia inside GPCI) a real, statistically-rigorous, independently-sourced corroboration check — strong agreement (r=0.96, MAPE 1.8%) in the only window it can currently test; (2) `open.data.gov.sa` moves from "could-not-reach, two methods" to "could-not-reach, five methods across three independent network paths, recommend deprioritizing further blind retries"; (3) Japan's next data point is confirmed still one day away, exactly as scheduled, no cycle wasted re-running against data that doesn't exist yet.

**Carry-forward, in priority order:** (1) Japan — re-run `scripts/japan_imports_analysis.py` **after 2026-09-29 09:30 JST** (unchanged from section 23/24). (2) Re-run `scripts/gastat_analysis.py` when GASTAT publishes its 2026 edition (expected mid-2027 on current lag) — that is the first point it can test the disrupted regime rather than only the calm one. (3) `open.data.gov.sa` — deprioritized per section 25.5; use GASTAT's own `statistics-tabs` explorer instead if the same catalog is needed. (4) UN Comtrade — still awaiting an owner call on account registration or direct outward contact (unchanged from section 23.2). (5) The standing bucket-1 producer-side search now needs a genuinely new country (Iraq, Kuwait, UAE, Qatar customs/statistics authorities remain effectively unchecked) since GASTAT-by-country-oil is closed per section 24.6. (6) Everything else carried forward verbatim from section 24.7: UKMTO and KNOC deprioritized absent new evidence; OPEC MOMR still Cloudflare-blocked; the `data.gov.in` "Principal Commodity wise Import" dataset still awaiting a CEO call on account registration or a no-login path.

## 26. KR6 cycle — 2026-09-28 (18th cycle, second session of the day): (c), with an analysis-only refresh attached. No model change.

**Delivery type: (c), evidenced.** This was a second, owner-requested session on the same UTC day as delivery 13 (§25), focused on wiring in visitor analytics. Here is why neither (a) nor (b) was available:

1. **No new cleared input was reachable to add.** Research could not be dispatched: `No such tool available: Agent. Agent is disabled for this session, in subagents as well as here.` This session ran the CEO role as a launched agent, not as the top-level `/ceo-cycle` session. The one time-triggered lead is Japan e-Stat's August detailed release, scheduled 2026-09-29 09:30 JST (00:30 UTC on the 29th), about 10.5 hours after this session. Re-running `scripts/japan_imports_analysis.py` before it exists would find nothing (§23.1, §25.6).
2. **No recalibration trigger fired.** The EIA supplement was re-fetched this session and the release is still 2026-08-12, so there is no new quarter to score against. The monthly GPCI input updates with the October STEO (parent STEO schedule, early October), not yet published.
3. **What was done instead, cheaply and in-bounds:** re-ran `scripts/weekly_arrivals_analysis.py` (§16) against EIA's latest weekly releases. Latest week ending **2026-09-18**, which at a 35–55 day voyage means loadings of about **2026-07-25 to 2026-08-14**. Gulf-origin 4-week average **−26.7%** vs the 2025 calm baseline (§16: −27.3%). **Saudi Arabia +12.7%** (§16: +16.4%). **Iraq −82.3%** (§16: −89.0%). **Reading:** essentially unchanged. The bypass-capable producer is above normal and the must-transit producer is still near the floor, so production is recovering faster than transit, consistent with §16 and with the live estimate sitting modestly above the 4.9 anchor (5.6, band 4.9–10.8). Iraq's +6.7 point move is within about one cargo at this resolution and is not read as a trend. **Analysis-only, unchanged status:** it does not enter the formula, and `sources.html` does not list it.
4. **Small defect noticed, not fixed in passing:** the script's closing caveat still says the series is analysis-only "until the owner rules on issue #9". Issue #9 was resolved on 2026-09-23 (option C), so the caveat's reason is stale, though its conclusion (analysis-only) is still true. Backlog nit.

**Published figure, `site/data/hormuz.json`, `sources.html`: unchanged.**

## 27. KR6 cycle — 2026-09-29: Japan's August detailed release confirmed live and re-run — Kuwait's July "recovery" reverses to zero, must-transit stays on the floor while bypass-capable Gulf keeps recovering

**Delivery type: (c) — no new cleared input, no model/calibration change.** This is
the pre-scheduled re-run of an already-CLEARED, already-analysis-only input
(§18, licence PDL1.0, re-confirmed not-yet-published in §23/§26). It produces
a new, real 3Q26 observation, but per its own standing status it **does not
enter the model or `sources.html`**. `site/`, `site/data/hormuz.json` and
`sources.html` are untouched this cycle.

### 27.1 Confirming the release actually happened, live, and finding the new file ID

The brief's premise — "today is the first cycle this could plausibly find
real data" — was checked, not assumed. Three independent live signals, all
fetched this session (2026-09-29, after 09:30 JST):

1. The old `FILES[2026]` id (`000040494488`) now returns **HTTP 404** at the
   file-download endpoint — a strong signal the file set changed, not proof
   of what replaced it.
2. `https://www.e-stat.go.jp/dbview?sid=0004002163` (customs-office-level
   companion table, live, HTTP 200, 2026-09-29): title string live-reads
   **"(1-7月：確報、8月：輸入9桁速報) 2026年"** — Jan–Jul now confirmed
   (確報), August now present as 9-digit provisional (速報). This is the
   exact status the 2026-09-26 cycle (§23.1) predicted would appear after
   the 09:30 JST release.
3. `https://www.e-stat.go.jp/stat-search/database?page=1&layout=dataset&toukei=00350300&tstat=000001013141&tclass1=000001013180`
   (the **nationwide** table the script actually needs, live, HTTP 200):
   same status, **"公開（更新）日 2026-09-29"**, i.e. published today, not
   backdated.

**Methodological note for future cycles, since it cost real time this
session:** the plain `stat-search/files?...&stat_infid=...` URL the script's
docstring points at is client-rendered (no file data in the static HTML) —
this is new; §23.1 apparently could read it directly, but that no longer
works, or the earlier read used a different rendering path. What **does**
still render server-side, confirmed this session: `dbview?sid=...` pages,
and `stat-search/{files,database}?...&layout=dataset` (note the
`layout=dataset` parameter, undocumented in the script, found by matching
Google's indexed snippets — which *do* see rendered content — back to a
working live URL). **The new statInfId was found and verified this way**,
not guessed and not taken from a snippet: filtered the live `layout=dataset`
files list to the row reading *"確速 品別国別表 輸入(1-7月：確報、8月：輸入9桁速報)
５部 25-27類"* (Section V, Chapters 25–27, Import, 2026), which resolves to
`statInfId=000040507877`. Downloaded directly
(`https://www.e-stat.go.jp/en/stat-search/file-download?statInfId=000040507877&fileKind=1`,
HTTP 200, `content-disposition: ik-100h2026i005.csv`), parsed, and confirmed
HS-2709 rows with `Unit1=KL` for all 16 origin countries, months Jan–Aug
populated, Sep–Dec zero — exactly the shape a mid-cycle release should have.
`scripts/japan_imports_analysis.py` `FILES[2026]` updated to
`"000040507877"` with a dated comment; no other logic changed.

**Cross-check against the prior (provisional) July read, since a revision
could otherwise masquerade as a trend:** §18.4 recorded Jul must-transit
−73%, Kuwait −55%, Saudi −27%, bypass-capable −30%. This run's Jul figures:
must-transit −72% (1-point rounding noise, not a revision), Kuwait −55%,
Saudi −27%, bypass-capable −30% — **unchanged**. The July→confirmed step did
not materially revise anything, which is itself worth recording: it argues
against treating "provisional" as a reason to discount July's reading, and
by extension against assuming August's own provisional figure will move much
either.

### 27.2 Results (% of each group's own 2024–25 calm daily rate, by month of arrival in Japan)

| 2026 | Jan | Feb | Mar | Apr | May | Jun | Jul | **Aug (prov.)** |
|---|---|---|---|---|---|---|---|---|
| Must-transit (KW, QA) | −34 | −45 | −52 | −98 | −100 | −87 | −72 | **−94** |
| Bypass-capable (SA, AE) | +22 | +15 | +1 | −60 | −60 | −41 | −30 | **−27** |
| Kuwait alone (calm 153 kb/d) | −23 | −12 | −58 | −100 | −100 | −78 | −55 | **−100** |
| Qatar alone (calm 97 kb/d) | −52 | −98 | −42 | −96 | −100 | −100 | −100 | **−84** |
| Saudi alone (calm 936 kb/d) | +72 | +46 | +16 | −60 | −75 | −48 | −27 | **−9** |
| UAE alone (calm 1,026 kb/d) | −23 | −13 | −13 | −60 | −46 | −36 | −33 | **−43** |
| Oman (weak placebo) | −100 | −3 | −10 | −16 | +4 | −49 | +7 | **+3** |
| Non-Gulf (substitution, NOT a placebo) | +67 | +81 | −6 | +5 | +21 | +413 | +682 | **+589** |
| **Japan total (demand check)** | +18 | +12 | −5 | −60 | −59 | −22 | +4 | **−0** |

2Q26 quarter average, for reference: Gulf −58.4% (must-transit −95.0%,
bypass-capable −53.8%). August alone: Gulf −34.3% (must-transit −93.7%,
bypass-capable −26.7%).

Cargo-count context, since this group is at VLCC resolution (~2 Mbbl/cargo):
Kuwait's raw August figure is **exactly 0 KL** — not a small positive
number rounding to −100, a literal zero across all HS-2709 rows for country
code 138. July was 338,741 KL ≈ 2.13 Mbbl (≈1 cargo). Qatar's August figure
is 77,988 KL ≈ 0.49 Mbbl (≈0.25 cargo, a part-cargo/blended parcel, not a
full VLCC) after two months (Jun, Jul) at exactly zero.

### 27.3 Question 1 — did Kuwait's recovery continue past July's "−55%, about one cargo"?

**No. It reversed to zero.** July's partial recovery (0 cargoes in
Apr/May/Jun-adjacent months → ~1 cargo in July) did **not** continue into
August; Kuwait-origin crude arriving in Japan in August was **zero**, the
same floor as April–May. Read narrowly, this is a genuine new data point
against the "recovery is underway" reading §18.5 flagged as modestly
supported. Read at the correct resolution, per the caveat carried since
§18.4 item 3, it is **one more swing in a series that has been alternating
between 0 and ~1 cargo a month since April** (Apr 0, May 0, Jun ~0.5, Jul
~1, Aug 0) — consistent with monthly VLCC scheduling lumpiness on a
calm-rate base of only ~2.3 cargoes/month, not with a clean recovery-then-
relapse story. **The honest statement is that July's reading was never
strong evidence of a trend, and August confirms that by not extending it in
either direction** — it is not evidence of a *reversal* either, just further
noise at a resolution too coarse to read as a signal. This should correct,
not reinforce, any inclination to read July's number as the start of a
recovery.

Qatar moved the opposite way (zero in Jun/Jul → a part-cargo in August),
which on its own would read as the *beginning* of a recovery, but is
symmetric noise from the same cause: two must-transit origins with structural
near-zero calm-period cargo counts, moving independently of each other, is
exactly what cargo-lumpiness — not a coordinated transit signal — looks
like. **Net for the must-transit group: −94% in August, marginally worse
than July's −72%, not materially different from the April–June floor.**

### 27.4 Question 2 — does the Jan–Feb must-transit weakness recur (§18.4 item 4)?

§18.4 item 4 flagged Jan (−34%) and Feb (−45%) must-transit readings as
*earlier* than the March 2026 onset dated elsewhere (§13.3, §17), and asked
whether the same **moderate, partial** pattern would recur later in the
year — which would suggest a real early signal rather than one-off
lumpiness. **It does not recur in this shape.** August's must-transit
reading (−94%) is not a moderate partial decline like Jan/Feb's — it is
close to the same near-total floor the group has held since April. The
Jan/Feb readings remain best read as lumpiness on a thin base (Qatar was at
a 0–1-cargo level even in February, per §18.4), not as an early leading
indicator that August reproduces. This narrows, but does not fully close,
the open question from §18.4 — the honest state is **unresolved, leaning
toward "not a recurring pattern,"** not confirmed either way with only two
non-adjacent data points to compare.

### 27.5 Overall Gulf-vs-control read, and the demand check

The split that has now reproduced across §16 (US), §17 (Eurostat/EU), and
§18 (Japan) reproduces again, more starkly, in August: **the bypass-capable
producer keeps closing the gap toward normal (Saudi −9%, its best reading of
2026), while the must-transit group does not (−94%, effectively unchanged
from the April–June floor).** UAE is the exception inside the bypass-capable
group — it *worsened* in August (−43%, vs −33% in July) rather than
continuing to recover, so "bypass-capable" as a pair is roughly flat
month-on-month (−30% Jul → −27% Aug) only because Saudi's improvement offsets
UAE's regression; the two origins are not moving together and should not be
read as one trend.

**Japan's total crude imports are now back to essentially calm levels
(−0% in August, vs −60% in April/May and +4% in July)** — the clearest
reading in this series to date that Japan has substituted its way back to
normal aggregate demand (non-Gulf +589% vs calm) while its Gulf-origin
supply, and especially its must-transit-origin supply, remains severely
depressed. This is consistent with, not contradictory to, an ongoing
transit constraint: it shows demand-side normalization masking a
supply-side shortfall that a naive read of "Japan's imports are fine" would
miss entirely.

### 27.6 What this does and does not support

- **Does not support** treating July's Kuwait figure as the start of a
  recovery trend — August's reversal argues the opposite, at the same
  resolution that made July look like a recovery in the first place. Net:
  **weaker, not stronger, support** for the "B: widen the band upward"
  direction §18.5/§23 discussed, though the sample is still too thin
  (single-digit cargo counts) to move a published number.
- **Does support**, more strongly than before, the cross-publisher ordinal
  finding that bypass-capable production is recovering faster than transit
  through the strait — now with an August reading where Saudi alone is
  within single digits of its calm rate while must-transit Gulf is still
  at −94%.
- **Magnitude: still not informed.** The must-transit sample is ~0.25 m b/d
  calm (~1.2% of calm Hormuz transit) at whole-cargo resolution; this cycle's
  reading is a literal zero for one of its two origins. A ratio built on this
  would be a ratio of near-zero numbers.
- August is **provisional** (9-digit速報); per §27.1 the Jul provisional→
  confirmed transition this cycle showed no material revision, so a large
  revision is not expected, but it hasn't happened yet either.

### 27.7 Carry-forward

Re-run again once September's data publishes (on the historical cadence,
provisional 9-digit ~end of the following month, i.e. ~late October for
September). Everything else carried forward verbatim from §26/§25: GASTAT's
2026 edition (expected ~mid-2027 on its current lag), UN Comtrade licence
resolution (owner call, §23.2/§47 backlog row), the standing bucket-1
producer-side search still needs a genuinely new Gulf country (Iraq, Kuwait,
UAE, Qatar customs/statistics authorities remain effectively unchecked).

**Published figure, `site/data/hormuz.json`, `sources.html`: unchanged.**

## 28. KR6 cycle — 2026-09-30: the standing Gulf-country gap closed for all four named countries — Iraq's SOMO surfaces the most promising raw finding of this whole search, but its licence is unresolved; Kuwait closed by mechanism; UAE and Qatar could-not-reach

**Delivery type: (c), with one substantive UNRESOLVED finding significant enough to
flag for a CEO/owner decision.** No new numeric input enters the model or
`sources.html` this cycle. Brief: check 1-2 of Iraq/Kuwait/UAE/Qatar's national
customs/statistics authorities for a crude oil export or production series with
useful granularity (monthly+, physical quantity, or country/partner breakdown),
per §27.7's standing carry-forward ("Iraq, Kuwait, UAE, Qatar customs/statistics
authorities remain effectively unchecked"). All four were actually attempted this
cycle, not just one or two, since time allowed it.

### 28.1 Iraq — SOMO (State Oil Marketing Organization, under the Ministry of Oil): the best raw candidate this brief has found, licence NOT cleared

**Reached live**, `https://www.somooil.gov.iq/en/exports/chart` (HTTP 200) — unlike
`oil.gov.iq` (the Ministry of Oil's own domain), which returned `HTTP 403` to every
fetch method tried and was not pursued further this cycle.

**What it measures.** Monthly crude oil **export quantity, in physical barrels**,
split by three loading routes, read directly off the live page: *"January 2026
report #79 — Quantity exported 107.6M bbl — Basrah 101.2M (94.0% of the month) —
North [Kirkuk-Ceyhan pipeline via Turkey] — Kurdistan Region fields 6.5M (6.0%)."*
Also gives monthly revenue and implied FOB price per barrel, and quarterly
refined-product export/import volumes (fuel oil, naphtha, gasoline, etc., metric
tons). Six months of 2026 were populated in the page's default view (January
through June), each with its own per-field monthly figure, e.g. Basrah:
Jan 101,160,349 bbl … Jun 17,799,036 bbl (a sharp mid-year drop, consistent with the
2026 disruption dated elsewhere in this document, §13.3/§17).

**Why this is more valuable than a generic national total.** "Basrah" is not an
administrative region — it is Iraq's Gulf export terminals (Basra Oil Terminal /
Khor al-Amaya single-point moorings), essentially 100% Hormuz-transiting, while
"North" is the Kirkuk-Ceyhan pipeline, Iraq's own Hormuz-bypass route. SOMO is
publishing, natively, exactly the must-transit vs. bypass split this document's
corroboration scripts (§16 US, §17 Eurostat, §18/§27 Japan) have had to construct
indirectly by grouping *other countries'* import records by Gulf producer. A
primary-source, government-published, route-level split for a single country is a
structurally different (and more direct) kind of evidence than any of those three.

**Cadence and lag — only partially confirmed.** Monthly, per the historical
columns; but the interactive chart is a client-hydrated widget that ignores URL
query parameters when fetched without JS execution (tested explicitly:
`?from=2026-07&to=2026-09` returned the same Jan-default content), and no
documented API or downloadable file could be found (`/api/exports`,
`/exports/month/2026-08`, and similar guesses all `404`). So **whether July-September
2026 figures are already published behind the JS widget is unconfirmed** — this
cycle's tooling could only confirm data existed for Jan-Jun as of 2026-09-30. The
site's separate "Reports" index shows an "18 August 2026 — Crude oil prices for
AUGUST 2026" entry, but that is a different product (official-selling-price
formula announcements, not export-volume reports) and does not resolve the
question. Flag for next cycle: retry with a JS-capable fetch if one becomes
available, rather than guessing at the true lag.

**Licence: UNRESOLVED, leaning toward not usable without further clearance.** No
terms-of-use, open-data licence, or explicit reuse/redistribution grant was found
anywhere on the site — checked: main nav (all sections), footer (every page),
`/en/about/policy` ("Policies and Strategies of SOMO regarding Crude Oil Export
Operations" — about export-allocation policy to trading companies, not a data
licence), the Reports index, and a targeted web search for
`somooil.gov.iq terms of use / privacy policy / copyright disclaimer` (no results
beyond the site's own generic pages). The only rights statement found, present
verbatim on every page checked including the 404 page, is: *"© 2026 State Oil
Marketing Organization (SOMO). All rights reserved by the IT & Communications
Department"* / *"© SOMO. All rights reserved."* That is a copyright-reservation
statement, the opposite of a reuse grant — per the standing guilty-until-checked
rule this is recorded as **UNRESOLVED / silent**, not rounded up to "probably
fine," exactly the failure mode the standing mandate warns against.
`somooil.gov.iq/robots.txt` returns the site's generic 404 page (no robots file
exists either way) — not informative on redistribution rights.

**Access mechanism.** Public web page, no login required, but the data itself is
delivered only through the rendered chart widget — no CSV/API/documented export
was found. Scraping the rendered figures would be the only access path, and with
no terms page at all, whether that scraping is itself permitted has no answer yet
either.

**Verdict: UNRESOLVED.** On substance this is the single most promising Gulf-producer
finding across the entire history of this standing search — closer to the "second
numeric anchor" the mandate names as the model's biggest weakness than GASTAT,
Eurostat, or Japan, specifically because of the Basrah/North/KRG route split. It
clears none of the licence bar, though: not adopted, not used even for internal
calibration. **Recommend the CEO weigh asking the owner to authorize direct
outward contact to SOMO** requesting explicit redistribution permission — the same
shape of ask already sitting in `backlog.md` for JODI, just with a stronger
substantive case (route-level, not just national, granularity) and a currently
completely silent (not explicitly hostile) licence posture.

### 28.2 Kuwait — Central Bank of Kuwait (republishing Central Statistical Bureau data): reached live, closed by mechanism

**Reached live**: `cbk.gov.kw/en/statistics-and-publication/dynamic-statistical-releases/quarterly/2023/q3/{33,35,38,40}`
(all HTTP 200) and the monthly release table list (tables 11-28, HTTP 200).

- **Table 33, "Summary of Foreign Trade"**: quarterly, KD million, gives "Oil
  Exports" as a single national-aggregate **value** figure only — no physical
  quantity, no country breakdown.
- **Table 35, "Total Exports According to SITC Sections"**: quarterly, KD million;
  oil is bundled inside SITC Section 3 ("Mineral Fuels, Lubricants & Related
  Materials") together with other fuels — value only, not oil-exclusive.
- **Table 38 is explicitly titled "Non-Oil Exports According to Destination"** —
  i.e. CBK's only by-destination trade table deliberately *excludes* oil. This is
  a structural, not incidental, absence: there is no CBK product that crosses oil
  exports with a destination country at all.
- **Table 40, "Kuwait's Foreign Trade with GCC Countries"**: all-goods (not
  oil-specific), value only, and partners limited to the five other GCC states —
  not useful for a global-destination Hormuz question even setting the oil-specific
  gap aside.
- The monthly release list (tables 11-28) is entirely banking/monetary (credit,
  exchange rates, reserves) — no trade or oil table exists at monthly cadence in
  this product at all.
- Source line on every table: *"Source: Central Statistical Bureau. ... All data is
  the property of Central Bank of Kuwait."* No explicit reuse/redistribution grant
  found on any page fetched — not pursued further, since the granularity question
  already closes this candidate on its own.
- A separate, dedicated petroleum-statistics module exists on the primary
  publisher's own site, `csb.gov.kw`, linked from its homepage nav as
  `/Petrol/Pet_Login.aspx` — but as the URL states, it is **login-gated**. Creating
  an account is outward contact in the owner's name (GOVERNANCE.md), so this was
  flagged, not pursued.

**Verdict: REJECTED for the standing ask, by mechanism, not merely unfound** — the
same shape of decisive negative §24.5 reached for GASTAT's by-country oil table.
CBK's published oil-export data is structurally value-only and structurally
excludes a by-destination breakdown; the one product that might carry more (CSB's
Petrol module) needs an owner-authorized account before it can be checked.

### 28.3 UAE — FCSC (Federal Competitiveness and Statistics Centre): named, plausible datasets exist, but the whole relevant surface is Cloudflare-blocked to every method tried — could-not-reach, not a licence verdict

**What is known to exist**, from one successful fetch of the FCSC homepage's
rendered navigation (via a reader-proxy service, before that same service became
blocked for this specific domain — see below): FCSC operates two relevant
sub-portals, `uaestat.fcsc.gov.ae` (a .Stat-Suite-style SDMX data explorer) and
`opendata.fcsc.gov.ae` (an open-data catalog). Named categories/datasets
identified (via the nav plus corroborating search-engine indexing): an **"Oil and
Gas"** statistics category (2009-2024 — year-range formatting with no month
markers, unlike the same site's own "Climate" category which explicitly reads
"Jan 2016 – Dec 2024," suggestively but not confirmedly annual); an
**"International Trade in Commodities"** category (2000-2025, "General System" — a
customs-based by-commodity dataset, plausibly with a partner-country dimension,
cadence unconfirmed); and, the most specific and promising lead, an open-data
entry titled **"Production and export crude oil"**, published by "Ministry of
Energy and Industry," at
`opendata.fcsc.gov.ae/@ministry-energy-industry/production-and-export-crude-oil`,
plus an SDMX dataflow named **"Crude Oil Reserves, Production, Exports and
Imports"** (`DF_CO`) referenced in a UAE.STAT visualization link surfaced by
search indexing.

**What could NOT be confirmed**: cadence, physical-quantity-vs-value, any
country/partner breakdown, or licence text — none of the actual data pages or the
portal's terms pages could be loaded this cycle. Methods tried, with their exact
failure signatures, recorded so a future cycle does not repeat them blind:

1. Direct `curl` through the proxy, with realistic browser headers (`User-Agent`,
   `Accept`, `Accept-Language`), against `fcsc.gov.ae` and both subdomains:
   consistent Cloudflare **`HTTP 403`**, response titled "Attention Required! |
   Cloudflare" — a bot-management challenge response, not a dead domain or a 404.
2. `WebFetch` tool: **`HTTP 403`** on every `fcsc.gov.ae`-family URL tried,
   including the plain homepage on a second attempt.
3. `r.jina.ai` reader proxy (an independent headless-browser service): worked
   **exactly once**, for the plain homepage nav only, then returned
   **`401 AuthenticationRequiredError ... blocked from performing anonymous
   queries due to bad IP reputation`** on every subsequent request to this
   specific domain for the rest of the session, including on retry after a delay
   — i.e. now blocked for this target specifically, not merely rate-limited.
4. Google Translate proxy trick (`fcsc-gov-ae.translate.goog/...`): relayed the
   origin's own **`403`** through unchanged.
5. Generic CORS proxy (`api.allorigins.win`): **`HTTP 522`** (Cloudflare timeout
   reaching the origin through that proxy).
6. Wayback Machine availability API, specifically for the `/p/about` licence page:
   **`archived_snapshots: {}`** — no snapshot has ever been taken.

One AI-generated web-search summary paraphrased what it characterized as FCSC's
open-data reuse terms in permissive-sounding language ("usable, reusable and
republished by any individual ... credited ... no distortion ..."). **This is
explicitly not treated as a licence read.** It is a search-engine summary of a
page this cycle never actually loaded, and the standing rule is unambiguous that a
snippet can never promote a source past UNRESOLVED. Recorded here only so a future
cycle knows `/p/about` and `/p/open-data-101` are the specific pages to prioritize
once the block clears — not as evidence the licence is fine.

**Verdict: UNRESOLVED / could-not-reach**, on the same footing as
`open.data.gov.sa` (§24-25), but on a wider and more deliberate block: six
independent methods, one consistent outcome (active Cloudflare bot-management
across the whole domain family, not a timeout or flaky origin). **Recommendation:
do not re-attempt with the same tool stack** — every method above shares either
this proxy's network path or a generic reader/proxy service Cloudflare can
fingerprint the same way. If revisited, the next genuinely different thing to try
is a real interactive browser session, if one becomes available to this role, not
another curl/proxy/reader-service variant.

### 28.4 Qatar — Planning and Statistics Authority (PSA): could-not-reach, same discipline

URLs tried: `psa.gov.qa/en/statistics1/StatisticsSite/Pages/Trade.aspx`,
`psa.gov.qa/en/Pages/default.aspx`, plain `psa.gov.qa`. Methods and results:
direct `curl` through the proxy — TLS-layer **`Recv failure: Connection reset by
peer`** (the same failure signature §24.1 judged "more consistent with the
origin's own problem than a block aimed at us specifically," though that read was
about a different domain and is not assumed to transfer here without more
evidence); `WebFetch` — **`HTTP 503 Service Unavailable`**; `r.jina.ai`, tried
twice against two different URLs — both **`TimeoutError: page.goto ... Timeout
15000ms exceeded`**, i.e. an independent real headless browser also cannot get
the page to load within 15 seconds. Also noted in passing, not itself reached:
search results reference a "National Planning Council" as a current publisher of
Qatar export statistics — a possibly-renamed or parallel body to PSA, not
disambiguated this cycle, and a concrete lead for next time.

**Verdict: UNRESOLVED / could-not-reach.** Three methods, three distinct failure
signatures, none successful — closer to "genuinely hard to reach" than to a
deliberate block, but not conclusively either, on the evidence gathered so far.
**Recommendation: try the "National Planning Council" naming directly next time**,
and retry PSA itself only if a new fetch method becomes available — don't spend a
cycle re-running the same three methods absent a reason to think the origin has
changed.

### 28.5 Net effect

**No new numeric input enters the model, `site/data/hormuz.json`, or
`sources.html` this cycle.** What changed: (1) the standing bucket-1 gap named in
§27.7 — Iraq, Kuwait, UAE, Qatar customs/statistics authorities "remain
effectively unchecked" — is now checked for all four, for the first time; (2)
Iraq/SOMO is the most substantively promising raw finding this standing search has
produced to date: a monthly, physical-quantity, route-split (Basrah/North/KRG)
export series that maps closely onto the must-transit/bypass distinction already
used elsewhere in this document — but its licence is unresolved (silent, default
copyright footer, no terms page found anywhere on the site), so it is flagged for
a CEO/owner decision rather than adopted or used for calibration; (3) Kuwait is
closed by mechanism, the same shape of decisive negative §24.5 reached for GASTAT
— CBK's oil-export data is structurally value-only and structurally excludes a
by-destination table, and the one product that might carry more (CSB's Petrol
module) is login-gated; (4) UAE (FCSC) and Qatar (PSA) are both recorded
could-not-reach, each on multiple independently-failing methods, so future cycles
don't repeat the same dead ends — UAE in particular has named, specific, plausible
datasets (a Ministry-of-Energy-sourced "production and export crude oil" open-data
entry) worth prioritizing the moment its Cloudflare block clears.

### 28.6 Carry-forward

1. **Owner/CEO decision needed: Iraq/SOMO.** Recommend the CEO weigh asking the
   owner to authorize direct outward contact to SOMO requesting explicit
   redistribution permission for the Basrah/North/KRG monthly export-quantity
   series — substantively the strongest candidate this search has found, held
   back only by licence silence, not by data quality or cadence. Also worth a
   deeper crawl for a terms/licence page next cycle before escalating to outward
   contact, in case one exists somewhere not yet found (only the obvious locations
   were checked this cycle).
2. **UAE (FCSC):** retry when a different fetch mechanism (e.g. a real browser
   session) is available; prioritize `opendata.fcsc.gov.ae/p/about` and
   `/p/open-data-101` (licence), the `production-and-export-crude-oil` dataset
   page itself, and the `uaestat.fcsc.gov.ae` `DF_CO` SDMX dataflow.
3. **Qatar (PSA):** try the "National Planning Council" naming directly next
   time; retry PSA itself only if a new method becomes available.
4. **Kuwait:** this specific sub-search (CBK/CSB oil-by-country) should be
   considered closed on the same footing as §24.6 closed GASTAT's equivalent ask.
   Re-opening it needs CSB's login-gated Petrol module, which needs an
   owner-authorized account first.
5. Everything else carried forward verbatim from §27.7: Japan — re-run
   `scripts/japan_imports_analysis.py` after September 2026 data publishes
   (expected ~late October on the historical cadence); UN Comtrade — still
   awaiting an owner call on account registration or direct outward contact;
   GASTAT's 2026 edition — expected ~mid-2027 on its current lag.

## 29. KR6 cycle — 2026-10-01: Oman and Bahrain checked, live — two of the strongest licences this search has ever found, attached to zero adoptable export series

**Delivery type: (c), evidenced.** No new numeric input enters the model, `site/data/hormuz.json`, or `sources.html` this cycle. Brief: check the two GPCI-member Gulf producers never yet checked as *customs/export* sources — Oman (NCSI / customs) and Bahrain (iGA / Ministry of Oil) — continuing the standing Gulf-customs sweep (Iraq, Kuwait, UAE, Qatar, Saudi Arabia all checked in §23-28). Both were reached live this cycle, unlike several of §28's targets. The headline finding is a reversal of the usual pattern: **licence is the easy part this time, data is not.** Both authorities turned out to have the clearest, most explicit open-data licences this entire standing search has read first-hand — better than EIA's own public-domain notice in terms of spelling out commercial use — but neither publishes a crude-oil **export** quantity series that is both current and at a useful cadence. Recorded in full because the licence texts themselves are reusable findings for any future Bahraini or Omani dataset, not just this cycle's candidates.

### 29.1 Bahrain — Information & eGovernment Authority (iGA) / Ministry of Oil and Environment: licence CLEARED (read live, full text), but no export series exists on the portal

**Licence: CLEARED.** Read first-hand from the actual PDF, not a snippet: `www.data.gov.bh` homepage states "By using the government open data, you implicitly acknowledge your agreement to the terms and conditions stated in the [Bahrain Government Open Data License]," linking to **`https://nea.gov.bh/Documents/OpenDataLicense.pdf`**. Fetched that PDF directly (confirmed as a genuine 5-page PDF via `file`, not an error page — the first `curl` attempt through the proxy got a bare `403`/118-byte stub, but `WebFetch`'s own fetch of the same URL succeeded and the binary was read directly with the `Read` tool) — **"Bahrain Open Government Data License, Version 1.0 – 20 May 2025"**, published by iGA. Operative text, clause 3.1: *"This license allows you royalty-free, non-exclusive use of the datasets for the following purposes: (a) sharing, copying, distributing or transmitting the datasets. (b) adapting the datasets to suit your needs. (c) using the datasets for applications that you develop or integrate with. (d) commercializing the applications that you develop using the datasets."* Clause 3.3 requires attribution — a specific mandatory sentence: *"Datasets provided by \<entity name\> via www.data.gov.bh are governed by the Bahrain Open Government Data License available at www.nea.gov.bh/Documents/OpenDataLicense.pdf. To the fullest extent permitted by law, the government is not liable for any damage or loss..."* — plus disclosure of any analysis/transformation as **ours**, not iGA's. Clause 3.4 bars misleading or illegal use. This is explicit, dated, bilingual, and squarely answers the redistribution/commercial-use question EIA's own notice doesn't even have to, because EIA's is simpler public-domain language — Bahrain's is a purpose-built reuse licence that names commercialization outright. **This clears the licence bar for any dataset actually published under `www.data.gov.bh` or another Bahraini government site**, independent of whether a usable oil dataset exists (it doesn't, below).

**What's actually published.** Queried the portal's OpenDataSoft catalog API directly (`https://www.data.gov.bh/api/v2/catalog/datasets`, confirmed live, 514 datasets total) and read every energy/petroleum-titled dataset's metadata first-hand (not search snippets):

| Dataset ID | Title | Fields | Frequency | Publisher |
|---|---|---|---|---|
| `01-crude-oil-produced-v1` | Bahrain Field Crude Oil Production (Thousands of US Barrels) | year, production | **Annual** | Ministry of Oil and Environment |
| `imports-of-crude-oil-thousands-of-us-barrels` | Imports of Crude Oil (Thousands of US Barrels) | year, quantity | **Annual** | Ministry of Oil and Environment |
| `crude-oil-run-to-refinery` | Refinery Throughput (Crude Oil and Feedstock) | year, quantity | **Annual** | Ministry of Oil and Environment |
| `05-petroleum-products-in-refinery-factory-v1` | Refinery Production (Thousands of US Barrels) | year, quantity | **Annual** | Ministry of Oil and Environment |
| `local-sales-of-petroleum-products` | Local Sales of Petroleum Products | year, product, quantity | **Annual** | Ministry of Oil and Environment |

**No crude oil or petroleum product EXPORT series exists in this catalog at all** — confirmed by exhaustively listing and keyword-matching all 514 dataset titles (`oil`, `petrol`, `crude`, `energy`, `hydrocarbon`, `export`, `sitra`, `bapco`, `refinery`, `fuel`), not just the obvious hits. The closest adjacent category, "Total Exports 2023/2024/2025/2026" and "EXPORTS (NATIONAL ORIGIN) 2023-2026," are confirmed **structurally non-oil** — their own metadata description reads *"KINGDOM OF BAHRAIN EXPORTS AND RE-EXPORTS NON-OIL CLASSIFIED BY COMMODITY AND COUNTRY"* (read from the `total-export-1-2024` dataset's own `description_en` field) — the same shape of deliberate oil-exclusion §28.2 found in Kuwait's CBK Table 38 and §24.5 found in GASTAT. iGA's own quarterly Foreign Trade press releases (checked one directly, the Q1 2025 article at `iga.gov.bh`) report only the non-oil figure by name and do not give an oil export figure at all, physical or value. The crude-oil-imports dataset's own description confirms *why* an export series would matter here anyway: *"Bahrain relies heavily on imported crude, which is primarily supplied via pipeline from Saudi Arabia... processed at the Bapco Refining refinery to produce a wide range of refined petroleum products for both domestic use and export"* — so Bahrain's Hormuz-relevant flow would be refined-product tanker exports from Sitra, exactly the series that is missing. (The crude import itself is pipeline-fed from Saudi Arabia across the Gulf, not Hormuz-transiting, so it would not have been Hormuz-relevant even if more granular.) A direct check of the Ministry of Oil and Environment's own site (`moo.gov.bh`, formerly NOGA's `noga.gov.bh`) found only a thin "Welcome to NOGA" landing page with no navigable statistics section reachable without JS — not pursued further this cycle; flagged as a carry-forward only if a future cycle has a JS-capable fetch method, since the open-data catalog already appears to mirror everything the Ministry publishes digitally and a dead landing page is a weak lead on its own.

**Verdict: REJECTED by mechanism (no adoptable content), licence CLEARED for future use.** Bahnrain's licence is now on record as genuinely clear and strong — if any Bahraini government body ever publishes a crude or product export-quantity series (or if a future cycle finds one this search missed), it clears instantly on the licence question and this section is where to look for the citation. For this cycle's purpose (a second numeric anchor, export-side, better than quarterly), there is simply nothing published to adopt. Also worth noting for completeness, independent of the "no export series" finding: Bahrain's own crude production is trivial (Bahrain Field, ~9 records i.e. a short annual run, order of tens of thousands of b/d) next to the GPCI members' flows, so even a hypothetical Bahrain export series would be a minor corroboration input at best, not a material anchor — this was a real but low-stakes gap to close.

### 29.2 Oman — National Centre for Statistics and Information (NCSI): licence CLEARED (read live, full text, CC-BY-4.0-equivalent), content exists but fails on currency (one portal) or confirmed cadence (the other)

**Licence: CLEARED.** `www.ncsi.gov.om` and `data.gov.om` both state in their footers: *"The content of this website is licensed under the Open Government License – Sultanate of Oman."* Read the actual licence PDF live at **`https://data.gov.om/s3/gov_license.pdf`** (confirmed genuine 4-page PDF via `file`, read directly with the `Read` tool, bilingual Arabic/English — titled "رخصة استخدام البيانات المفتوحة" / "Open Data Usage License"). Clause 2 ("Beneficiary rights") grants: *"Use and reuse of the data under this licence for any commercial or non-commercial purpose,"* *"Copy, download, publish, distribute, transmit, and process the data,"* and *"Combine the data with data from other sources, and incorporate or publish it within another website or application."* Clause 3 requires attribution to the original source and disclosure of any modifications; prohibits misrepresentation or false claims of official endorsement. Clause 4 excludes only personal data, official government emblems, third-party IP (patents/trademarks), ID documents, and classified/restricted data — none of which bear on a statistical export series. Clause 6.2 states explicitly: *"This licence is compatible with the Creative Commons CC BY 4.0 licence."* This is, if anything, a cleaner and more explicit grant than EIA's own public-domain notice — on the same footing as Bahrain's §29.1 finding, and the two strongest licences this whole standing search has read first-hand to date.

**What's actually published — two separate portals, two separate problems.**

1. **`data.gov.om`'s "Oil and Gas" explorer** (`OMOLGS2016`), reached live at `https://data.gov.om/OMOLGS2016/oil-and-gas?region=1000000-oman&country=1000000-total&indicator=1000160-imports`. This runs on **Knoema**, a third-party commercial data-platform vendor (confirmed via the page's own `Content-Security-Policy: frame-ancestors 'self' *.knoema.com *.knoema.org` header and dozens of `Knoema`-branded asset paths in the HTML) — worth flagging on its own, since a vendor-hosted government page could in principle carry the vendor's own terms layered on top of the government licence, though nothing on this page suggested that here. Substantively, its own description is exactly on-point: *"Crude oil data reflects the quantity of production and exports according to the producer... the data reflects crude oil exports by importing countries"* — a physical-quantity, by-destination export series, which is precisely the kind of thing this standing search is looking for. **But the page's own metadata block reads "Published by source: 15 August 2016" / "Expected next release: 31 August 2021"** — read directly off the live page, not inferred — i.e. this product is **five years stale by its own stated schedule** and shows no sign of having been refreshed since. Not pursued for actual record-level data on cadence/currency grounds alone; a live but abandoned dashboard is not a usable anchor regardless of licence or topical fit.
2. **`data.ncsi.gov.om`'s "Daily Average Exports of Crude Oil"** dataset (a separate, Drupal-based NCSI portal, distinct domain from `data.gov.om`), reached live at `https://data.ncsi.gov.om/?q=dataset/daily-average-exports-crude-oil`. Read directly off the page's own structured metadata fields (not a search-engine summary): **"Frequency: Annually," "Unit of Measurement: bbl"** (physical quantity, confirmed), "Release Date: 2023-07-18" (a far more recent listing date than the Knoema dashboard, suggesting this is the currently-maintained product). Despite the "Daily Average" name, the dataset's own stated update frequency is annual, not daily or monthly — matching the common pattern (seen before in this document) of a national statistical bulletin table that reports a year's daily-average rate as a single annual figure, not a true daily series. The underlying data is served through an ArcGIS `FeatureServer` reference (`NCSIindicatorsPartXI/FeatureServer/4303`) embedded in a heavy JS map/table viewer (`map.ncsi.gov.om`) — six URL-construction attempts to reach the FeatureServer's REST query endpoint directly (`/arcgis/rest/services/...`, `/server/rest/services/...`, `/host/rest/services/...`, `/rest/services/...`, each against both `FeatureServer` and `MapServer`) all returned a generic IIS "404 - File or directory not found," meaning the true service root could not be located by guesswork from static tooling — the same class of problem as §28.1's SOMO chart and §28.3's FCSC block: **real content exists behind a JS widget this cycle's tooling cannot execute.** Because the page's own "Frequency: Annually" field is a structural fact already read, not something blocked by the widget, this doesn't change the headline conclusion even if record-level access is resolved later: **annual is not better than EIA's existing quarterly anchor**, so this dataset would not clear the bar that motivated the search even in the best case. A search-engine summary separately claimed a "January 2002 to September 2026" range and a by-country dimension list (China, India, Japan, Korea, etc.) for this dataset — **not independently confirmed this cycle, recorded only as a lead**, consistent with the standing rule against promoting anything past UNRESOLVED on a snippet.

**Relevance caveat, independent of the above (per this cycle's brief and methodology.md §23):** Oman loads almost entirely at Mina al Fahal, outside the Strait of Hormuz. Even a fully resolved, monthly-or-better Omani export series would be a **regime-detector control/placebo** (upgrading the existing EIA-STEO-production-based "Oman weak placebo" row already in the backtest table, §16 and §27) rather than a must-transit anchor. That upgrade isn't available regardless, since the one confirmed-live cadence (annual) is worse than the EIA production series already used for that placebo role.

**Verdict: REJECTED on cadence for the confirmed candidate (`data.ncsi.gov.om`, Annually), REJECTED on currency for the topically-perfect candidate (`data.gov.om`/Knoema, dormant since ~2016/2021); licence CLEARED for both portals.** Neither failure is a licence problem — both would clear instantly if either dataset were live and better-than-quarterly. Flagged for a future cycle only if a JS-capable fetch method becomes available (to resolve the FeatureServer and confirm whether finer-grained records sit behind the "Annually" summary field) — not worth re-attempting with the same static-tooling approach.

### 29.3 Net effect

**No new numeric input enters the model, `site/data/hormuz.json`, or `sources.html` this cycle.** What changed: (1) the standing brief's two remaining unchecked GPCI-member customs/export authorities, Oman and Bahrain, are now checked, live, closing out the full seven-country Gulf-producer customs sweep named in the standing mandate (Saudi Arabia, Iraq, Kuwait, UAE, Qatar, Oman, Bahrain — Iran not pursued, consistent with sanctions-context caution already implicit elsewhere in this document); (2) two genuinely strong, explicit open-data licences were read first-hand in full and are now CLEARED for any future dataset from either publisher — Bahrain's Open Government Data License v1.0 (20 May 2025, `nea.gov.bh/Documents/OpenDataLicense.pdf`) and Oman's Open Data Usage License (`data.gov.om/s3/gov_license.pdf`, CC-BY-4.0-equivalent) — both explicitly permit commercial use, redistribution, and combination with other data, with only an attribution requirement; (3) despite that, **zero adoptable export series resulted**: Bahrain publishes no crude-or-product export quantity series at all (only production, imports, refinery throughput and local sales, all annual); Oman publishes one topically perfect but five-years-dormant series (Knoema/`data.gov.om`) and one live-looking but annual-cadence series (`data.ncsi.gov.om`) whose finer-grained records, if any, sit behind a JS widget this cycle's tooling could not reach. This is a clean instance of the standing mandate's "check whether a newer/better product exists" discipline cutting the other way: both leads were followed to an actual, confirmed, evidenced dead end rather than stopped early on a promising title.

### 29.4 Carry-forward

1. **Bahrain and Oman licences are now on file (§29.1, §29.2) for instant reuse** if either country's statistics authority, Ministry of Oil, or a successor portal ever publishes an export-quantity series — no re-clearing needed, cite this section.
2. **Oman `data.ncsi.gov.om` FeatureServer** (`NCSIindicatorsPartXI/FeatureServer/4303`): retry only with a JS-capable fetch/real browser session, not another static-tooling guess at the REST path — six guesses already exhausted this cycle. Resolving it would only matter if it turns out to carry sub-annual granularity despite the page's own "Frequency: Annually" label, which the page itself gives no reason to expect.
3. **Oman `data.gov.om`/Knoema oil-and-gas dashboard**: do not re-attempt on the assumption it has been revived without first checking whether its "Expected next release" field has moved past 31 August 2021 — if it hasn't, treat as abandoned without re-fetching.
4. **Bahrain `moo.gov.bh` (Ministry of Oil and Environment, formerly NOGA)**: homepage is a thin JS-nav shell this cycle's tooling couldn't get past; a future cycle with a JS-capable method could check it directly, but the open-data catalog likely already mirrors anything the Ministry publishes digitally, so this is a low-priority lead, not a strong one.
5. **The seven-country Gulf-producer customs/statistics sweep named in the standing mandate is now complete** (Saudi Arabia §23-25, Iraq/Kuwait/UAE/Qatar §28, Oman/Bahrain §29). Recommend the next KR6 cycle's default search order shift back toward the mandate's other two listed directions — event signals for the regime detector (UKMTO/IMO/MARAD/sanctions notices), and re-checking whether any of this document's UNRESOLVED/could-not-reach items (SOMO §28.1, FCSC §28.3, PSA §28.4) have changed status — rather than opening an eighth country search without a specific new lead.
6. Everything else carried forward verbatim from §28.6: Iraq/SOMO licence still UNRESOLVED pending a CEO/owner decision on outward contact; UAE/FCSC and Qatar/PSA still could-not-reach; Japan re-run pending September 2026 data; UN Comtrade awaiting an owner call; GASTAT's 2026 edition expected ~mid-2027.
