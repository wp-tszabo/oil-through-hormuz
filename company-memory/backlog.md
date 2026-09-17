# Backlog

Prioritized work items. Owned by role. The CEO reorders/updates this every
cycle; specialists add findings and new items they surface. Move finished
items to "Done" with the date, don't delete them.

## Blocked on owner (as of 2026-09-17, 3rd cycle)

| Item | Owner | Notes |
|---|---|---|
| **Decide the headline: measured quarter, honest range, or daily number** | Owner | **PR #4 (`needs-copy-review`) + critical issue #5.** The single decision that unblocks publishing. The owner's spec asks for "the amount of oil passed through the Strait of Hormuz on {yesterday}" + a number; no source we may republish measures this daily, so a daily point figure would present a quarterly-anchored model output as a measurement (category 4, rubric §1.4/§3.2 FAIL). Three options are laid out in PR #4. CEO recommends option 1 (headline the latest measured quarter). |
| **Approve homepage v2 copy** | Owner | Same PR #4. Also needs: the name for the copyright line, and confirmation that "Strait" (not "Straight") is wanted. Everything else in the draft is ready to ship the moment the headline question is settled. |
| **Send (or don't) the IMF permission request** | Owner | Issue #1 was closed with "network access resolved", which answered the egress question and **not** this one — closure is not authorisation, so nothing has been sent. **CEO recommendation has now reversed to "don't bother"**: EIA turned out to be quarterly (not annual), so the gap is much narrower, and PortWatch is raw-AIS-derived at a time when EIA says Hormuz AIS is especially unreliable. Keeping the item open because outward contact is the owner's call either way. |

## Now (Phase 1, Week of 2026-09-14)

| Item | Owner | Notes |
|---|---|---|
| Publish homepage v2 once approved, then run the rubric against the **live** page and log it | CEO | Blocked on PR #4. Merge to `main` is what triggers the deploy, so merging *is* publishing — do not merge to tidy up the branch. |
| **Automate the EIA fetch + staleness alarm (GitHub Actions)** | Build | **Now the highest-value unblocked build item, and now concrete**: parse Table 4 from `eia.gov/outlooks/steo/report/energysecurity/article.php` into `site/data/hormuz.json` (schema already exists in PR #4), fail loudly on parse failure, and surface staleness on the page rather than serving an old number as current. Must derive staleness from the supplement's own release date and the coverage end of the latest row — **not** from the parent STEO's next-release date; those are different schedules and conflating them was a real error caught by the rubric this cycle. |
| **Independent uptime + certificate check (CI cron or external monitor)** | Build | Sharpened again by issue #3: it must assert **certificate validity**, not just HTTP 200. An HTTP-only check would have called the 16-hour TLS outage green. Must not depend on the CEO sandbox's egress, which has flipped between fully blocked and fully open within a single day. |
| **Standing end-of-cycle check: memory commit is on `main` AND `origin/main`** | CEO | New, after this cycle found two cycles of memory stranded on an unpushed detached HEAD. The cycle report must quote the pushed commit SHA. |
| Recalibrate the model on each new EIA release and append the error to the back-test | CEO/Build | `methodology.md` §3. The next release will be the first real test of the regime detector; if it shows flows recovering, the daily-estimate option reopens on its own. |
| Register a free EIA API key (`api.eia.gov`) | Owner (or CEO with permission) | $0 but requires an account in the owner's name, so not the CEO's to do. **Lower priority than previously recorded** — the quarterly table parses fine from the public page, so this is an optimisation, not a dependency. |

## Later (Phase 2, blocked until owner approves graduation)

| Item | Owner | Notes |
|---|---|---|
| Competitive scan (e.g. `straits.live`, which already publishes Hormuz CSV/JSON time series) | Research | Surfaced incidentally this cycle. Informs positioning; also a reminder not to redistribute another tracker's derived data. Not urgent, not Phase 1 scope. |
| Evaluate paid tanker-tracking / AIS data providers | Research | Do not start until Phase 1 evaluation is done and owner approves graduation |
| Monetization strategy (ads/affiliate/subscription) | Monetization | Dormant — do not start in Phase 1 |
| Budget proposal for paid data | CEO | Must be justified against a specific free-tier gap, not proposed by default |

## Done

| Item | Owner | Completed | Notes |
|---|---|---|---|
| **Fix broken HTTPS on the custom domain** | Owner (fix) / CEO (verify) | 2026-09-17 (3rd cycle) | **Done and verified.** Owner re-saved the custom domain to unstick cert issuance; CEO verified a valid Let's Encrypt cert and all four entry routes landing on the valid-TLS apex before closing issue #3. Closed on evidence, not on report. |
| **Design the daily best-guess estimation methodology** | CEO (Research unavailable, 3rd cycle) | 2026-09-17 (3rd cycle) | **Done** — `company-memory/methodology.md`: cleared/rejected input inventory, model structure, a real back-test on six quarters, a regime detector, and an explicit finding that the output is not publishable as a daily point figure in the current disrupted regime. Escalated to the owner rather than resolved by the CEO. |
| **Find a fresher cleared source than the annual EIA chokepoints table** | CEO (Research unavailable) | 2026-09-17 (3rd cycle) | **Done, and it overturned a prior finding** — EIA's Global Energy Security Data supplement publishes Hormuz flows **quarterly** (latest 2026-08-12, through 2Q26 = 4.9 m b/d). The "~14 months stale" conclusion from the 2nd cycle was wrong. |
| **Draft homepage copy to the owner's simplified spec** | CEO | 2026-09-17 (3rd cycle) | Built as a real page, not just prose: `site/index.html` + `site/data/hormuz.json` on branch `copy-review/homepage-v2`, opened as PR #4 with label `needs-copy-review`. Held, not published. |
| Draft homepage copy v1 (long-form drafts A–E) | CEO | 2026-09-17 | Retired unpublished — superseded by the owner's simplified spec in issue #2. Kept at `pending-copy/2026-09-17-homepage.md` for the record. |
| Scaffold static site structure + GitHub Pages deploy | Build | 2026-09-16 | Skeleton at `site/`, repo public, Pages enabled (Actions build, auto-deploys on push to `site/**`). Custom domain `oilthroughhormuz.com` configured; DNS confirmed correct 2026-09-17. Placeholder content only. |
| Survey candidate free data sources for Hormuz oil-flow volume | CEO (Research unavailable) | 2026-09-17 | Partial — candidates found (IMF PortWatch, EIA), but **no ToS clearance possible**; see decisions-log.md 2026-09-17 and critical issue #1. Reopened as the PortWatch licence-read item, now completed below. |
| **Read the IMF/PortWatch licence in full and decide on redistribution** | CEO (Research unavailable) | 2026-09-17 (2nd cycle) | **Done — answer is NO.** All PortWatch datasets are `license: custom` → IMF terms prohibiting systematic downloading, redistribution, compilation and derivative works. PortWatch REJECTED; nothing was ever ingested. See decisions-log.md. This was the company's highest-value open question. |
| **Confirm EIA's licence and true cadence** | CEO (Research unavailable) | 2026-09-17 (2nd cycle) | **Done.** EIA CLEAR (US public domain, free to use and distribute, attribution with publication date requested). Cadence worse than assumed: chokepoints table is annual 2020–2024 + 1H25, Hormuz 19.2/19.7/21.9/21.8/20.7/**20.9** m b/d, last updated 2026-03-03. Vortexa provenance caveat recorded. |
| **Verify the live site against the rubric for real** | CEO | 2026-09-17 (2nd cycle) | **Done.** Egress returned; fetched both live URLs, diffed byte-identical against `site/index.html`, confirmed zero data figures are live. Upgraded the earlier INCONCLUSIVE self-check to a genuine PASS on content — and caught the broken-HTTPS defect in the process. |
| Draft homepage copy (headline, methodology/about blurb) | CEO | 2026-09-17 | `company-memory/pending-copy/2026-09-17-homepage.md`, sent for review as issue #2. Drafting is done; publishing is not. |
| Stand up the async approval mechanics for real | CEO | 2026-09-17 | Labels `critical` / `needs-approval` / `needs-copy-review` created; issues #1 and #2 filed. Working auth path is authenticated REST against `api.github.com` (no `gh` CLI in this sandbox). |
