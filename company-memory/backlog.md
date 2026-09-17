# Backlog

Prioritized work items. Owned by role. The CEO reorders/updates this every
cycle; specialists add findings and new items they surface. Move finished
items to "Done" with the date, don't delete them.

## Blocked on owner (as of 2026-09-17, 2nd cycle)

| Item | Owner | Notes |
|---|---|---|
| **Fix broken HTTPS on the custom domain** | Owner | **GitHub issue #3, `critical`.** `https://oilthroughhormuz.com` and both `www` forms fail TLS — Pages is serving a `*.github.io` cert because the Let's Encrypt cert for the custom domain was never provisioned. Every normal visitor route ends in a browser security warning. Fix: Settings → Pages → clear Custom domain, Save, re-enter `oilthroughhormuz.com`, Save, wait for the cert, then tick Enforce HTTPS. CEO cannot do this — the Pages REST API is blocked by the sandbox proxy, and DNS/domain changes are hard-to-reverse and out of its authority. |
| **Decide the product re-scope** — PortWatch rejected, EIA clear but ~14 months stale | Owner | **GitHub issue #1** (updated with the full licence verdict). (A) ask `copyright@imf.org` for written redistribution permission — $0, restores the daily-cadence product if granted; (B) re-scope honestly around EIA's real vintage and ship that now; (C) open the Phase 2 paid-data conversation. **CEO recommends A now, B in parallel as what ships, C only if A fails.** No email has been sent — outward contact on the company's behalf is the owner's call. Everything under "Now" that involves data is blocked on this. |
| **Review draft homepage copy** | Owner | GitHub issue #2, label `needs-copy-review`. Source: `company-memory/pending-copy/2026-09-17-homepage.md`. Three questions at the bottom of the draft (headline choice, whether to foreground the agent system, whether to keep a future house-index option open) — **plus a fourth added this cycle**: Draft C's "a figure here can legitimately be weeks old" is now too generous given EIA's true vintage, and the CEO has proposed replacement wording in an issue comment. Reasonable to hold the whole draft until the re-scope in #1 is decided. |

## Now (Phase 1, Week of 2026-09-14)

| Item | Owner | Notes |
|---|---|---|
| Re-verify HTTPS once the owner has re-saved the custom domain, and log the result | CEO | Blocked on #3. Close the critical issue only after a successful `https://oilthroughhormuz.com` fetch, not on the owner's say-so alone. |
| Wire the confirmed data source into the site (fetch → store → render) | Build | Blocked on the re-scope decision (#1), not on clearance — EIA *is* cleared. The open question is whether an EIA-only page is the product we want to ship. **Do not ingest PortWatch under any circumstances** unless the IMF grants written permission. |
| Scheduled data-fetch + staleness-alarm workflow (GitHub Actions) | Build | **Now the highest-value unblocked build item.** Should fail loudly and surface staleness on the page rather than serving a stale number as current (rubric §1.5) — and with EIA's real vintage, staleness display isn't a nice-to-have, it's the core honesty feature. Worth building regardless of how #1 resolves. |
| Independent uptime + HTTPS check for the live site | Build | Sharpened by this cycle: the CEO's sandbox egress flipped from fully blocked to fully open within a single day, so *nothing* that matters may depend on it. Needs to run in CI cron or an external monitor. Must check HTTPS specifically — #3 is precisely the failure an HTTP-only check would have called green. |
| Record the EIA attribution string and the Vortexa provenance caveat wherever figures get rendered | Build/CEO | EIA asks for "Source: U.S. Energy Information Administration" with publication date. Chokepoint figures are EIA analysis *based on Vortexa tanker tracking* — attribute EIA's analysis, never imply we hold or license Vortexa data. |
| Publish homepage copy once approved, then run the rubric and log it | CEO | Blocked on issue #2. |
| Register a free EIA API key (`api.eia.gov`) | Owner (or CEO with permission) | $0 but requires creating an account with the owner's email. The CEO has **not** registered one — signing the owner up to a third-party service unasked isn't its call. Only needed if we go the programmatic-EIA route; the chokepoints table can also be parsed from the public page. |

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
| Scaffold static site structure + GitHub Pages deploy | Build | 2026-09-16 | Skeleton at `site/`, repo public, Pages enabled (Actions build, auto-deploys on push to `site/**`). Custom domain `oilthroughhormuz.com` configured; DNS confirmed correct 2026-09-17. Placeholder content only. |
| Survey candidate free data sources for Hormuz oil-flow volume | CEO (Research unavailable) | 2026-09-17 | Partial — candidates found (IMF PortWatch, EIA), but **no ToS clearance possible**; see decisions-log.md 2026-09-17 and critical issue #1. Reopened as the PortWatch licence-read item, now completed below. |
| **Read the IMF/PortWatch licence in full and decide on redistribution** | CEO (Research unavailable) | 2026-09-17 (2nd cycle) | **Done — answer is NO.** All PortWatch datasets are `license: custom` → IMF terms prohibiting systematic downloading, redistribution, compilation and derivative works. PortWatch REJECTED; nothing was ever ingested. See decisions-log.md. This was the company's highest-value open question. |
| **Confirm EIA's licence and true cadence** | CEO (Research unavailable) | 2026-09-17 (2nd cycle) | **Done.** EIA CLEAR (US public domain, free to use and distribute, attribution with publication date requested). Cadence worse than assumed: chokepoints table is annual 2020–2024 + 1H25, Hormuz 19.2/19.7/21.9/21.8/20.7/**20.9** m b/d, last updated 2026-03-03. Vortexa provenance caveat recorded. |
| **Verify the live site against the rubric for real** | CEO | 2026-09-17 (2nd cycle) | **Done.** Egress returned; fetched both live URLs, diffed byte-identical against `site/index.html`, confirmed zero data figures are live. Upgraded the earlier INCONCLUSIVE self-check to a genuine PASS on content — and caught the broken-HTTPS defect in the process. |
| Draft homepage copy (headline, methodology/about blurb) | CEO | 2026-09-17 | `company-memory/pending-copy/2026-09-17-homepage.md`, sent for review as issue #2. Drafting is done; publishing is not. |
| Stand up the async approval mechanics for real | CEO | 2026-09-17 | Labels `critical` / `needs-approval` / `needs-copy-review` created; issues #1 and #2 filed. Working auth path is authenticated REST against `api.github.com` (no `gh` CLI in this sandbox). |
