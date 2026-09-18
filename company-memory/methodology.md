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
