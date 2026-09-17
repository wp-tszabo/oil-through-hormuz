# OKRs

Updated by the CEO at the start/end of each weekly cycle. Keep history —
don't delete past quarters/phases, mark them closed instead.

## Phase 1 — Prove the free-tier core product (current)

**Objective**: Ship a small, honest, reliably-updating Strait of Hormuz
oil-flow tracker on free/public data, before spending money or building
monetization.

| Key Result | Target | Status |
|---|---|---|
| KR1: Identify and validate a free, ToS-clear daily/periodic Hormuz flow data source | 1 primary source documented, with a licensing check logged in `decisions-log.md` | **MET, on the "periodic" half — and the bar moved in our favour.** Primary source: **EIA Global Energy Security Data** (`eia.gov/outlooks/steo/report/energysecurity/article.php`), licence-cleared (US federal public domain), **quarterly**, latest release 2026-08-12 covering through 2Q26. This supersedes the 2nd cycle's finding that EIA was annual and ~14 months stale — that was the wrong EIA product. Real staleness is ~11 weeks. The **daily** half is not met and cannot be met free: every daily source found is licence-closed (PortWatch rejected 2nd cycle; WTO/AXSMarine rejected this cycle). The owner-directed estimation model (`methodology.md`) is designed and back-tested, but its output is not honest to publish as a daily point figure in the current disrupted regime — escalated, not decided. |
| KR2: Publish a working site on GitHub Pages showing that data | Live URL, auto-updating, uptime tracked in `metrics.md` | **Infrastructure now healthy; content still not published.** HTTPS is fixed and verified (critical issue #3 closed) — valid Let's Encrypt cert, enforcement on, all four entry routes landing on the valid-TLS apex. Uptime **UP**. But the live page is still the placeholder: the page carrying real figures is held in PR #4 awaiting owner copy approval. Not auto-updating yet — the EIA fetch workflow is the top unblocked Build item. |
| KR3: Zero unreviewed copy reaches the live site | 100% of published copy has an owner-approval record | **On track, and stress-tested this cycle.** 0 published. The v1 drafts were retired unpublished when the owner changed the spec; v2 is held in PR #4. The checkpoint did real work here rather than being a formality: it is the mechanism by which a disagreement with the owner's own instruction (the daily-headline question) reached the owner instead of being resolved unilaterally in either direction. |
| KR4: Run the self-check rubric on every publish | 100% of publishes have a `self-check-log.md` entry | **On track, and it caught something real.** 0 publishes, 4 rubric runs logged. This cycle's pre-publish run found a genuine factual error before the owner ever saw the draft — the page had claimed a next-release date that belonged to the parent STEO, not to the Hormuz dataset. Fixed in the page, the JSON and the methodology doc. First time the rubric has caught an error rather than confirming a clean draft. |
| KR5: First weekly spend ceiling stays at ~$0 | Actual spend = $0 unless owner explicitly raises the ceiling | **On track** — $0 agent-committed across three cycles. The owner-purchased domain remains the one logged exception (2026-09-16), not agent spend. Notably the CEO's spend-related recommendation moved *downward* this cycle: the IMF licence ask and the Phase 2 paid-data conversation both became less justified once EIA turned out to be quarterly. |

### Phase 1 evaluation — running notes (for the graduation decision)

GOVERNANCE.md asks three questions before Phase 2 is proposed. Partial answers so far, to be finalised at week close:

1. **Did the research approach hold up?** Mixed, and honestly: the guilty-until-checked licence rule worked twice (PortWatch, WTO/AXSMarine — both rejected before any code depended on them). But the *search* was weak — two cycles asserted a 14-month staleness that was simply wrong because nobody asked whether EIA had a newer product. The rule caught legal risk; it did not catch incuriosity.
2. **Did the checkpoints fire when they should have?** Yes, and twice for real: the copy checkpoint carried a disagreement with the owner's instruction upward instead of resolving it silently, and the rubric caught a factual error pre-publish. A third fired late — broken HTTPS sat in the backlog as routine for a day before being re-classified critical.
3. **Is free-tier data good enough?** Better than believed, and still not sufficient for the product as specified. Quarterly at ~11 weeks is genuinely publishable; daily is unavailable at any free price because the constraint is licensing, not cost. **A paid feed would close the daily gap — which is exactly why the case for it must wait until the owner has decided whether the honest quarterly product is the product.** Not proposing graduation.

## Phase 2 — Graduation (not started)

Gated on the Phase 1 evaluation described in GOVERNANCE.md. No OKRs defined
yet — the CEO drafts these as part of the graduation proposal, justified
against specific Phase 1 findings (not proposed by default).
