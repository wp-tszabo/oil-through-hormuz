# Daily Best-Guess Estimation Methodology — design v1

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
