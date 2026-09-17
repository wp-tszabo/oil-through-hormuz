# Backlog

Prioritized work items. Owned by role. The CEO reorders/updates this every
cycle; specialists add findings and new items they surface. Move finished
items to "Done" with the date, don't delete them.

## Blocked on owner (as of 2026-09-17)

| Item | Owner | Notes |
|---|---|---|
| **Decide on critical issue #1** — egress policy blocks all data-source domains and the live site | Owner | GitHub issue #1, label `critical`. Three options offered: (A) allowlist `eia.gov`/`api.eia.gov`/`imf.org`/`portwatch.imf.org`/`oilthroughhormuz.com`/`wp-tszabo.github.io`, (B) move fetch + verification into GitHub Actions, (C) accept the pause. CEO recommends A, with B as a follow-on regardless. **Everything below marked "blocked on #1" unblocks with this.** |
| **Review draft homepage copy** | Owner | GitHub issue #2, label `needs-copy-review`. Source: `company-memory/pending-copy/2026-09-17-homepage.md`. Three specific questions at the bottom of the draft (headline choice, whether to foreground the agent system, whether to keep a future house-index option open). |

## Now (Phase 1, Week of 2026-09-14)

| Item | Owner | Notes |
|---|---|---|
| Read IMF PortWatch / IMF Data Terms in full and decide if redistribution is permitted | Research (or owner, if egress stays blocked) | Blocked on #1. This is the single highest-value open question in the company: if PortWatch is redistributable, the product's daily-cadence goal is achievable at $0 and no Phase 2 data spend is needed. If it isn't, the product has to be re-scoped around quarterly EIA data. |
| Recommend one primary source + the cadence it actually supports | Research | Blocked on the PortWatch licence read above. EIA is the licence-safe fallback but is quarterly-to-biennial, not daily. |
| Wire the confirmed data source into the site (fetch → store → render) | Build | Blocked on a *cleared* source. Do not connect anything not cleared. |
| Scheduled data-fetch + staleness-alarm workflow (GitHub Actions) | Build | Blocked on #1 option B. Should fail loudly and surface staleness on the page rather than serving a stale number as current — rubric §1.5. Worth building regardless of how #1 resolves; it's the right architecture for an auto-updating site. |
| Independent uptime check for the live site | Build | The CEO currently cannot fetch its own site, so it cannot detect an outage — the exact blind spot critical-issue category 1 exists to prevent. Needs to run somewhere with egress (CI cron, or an external monitor). |
| Turn on HTTPS enforcement for the custom domain | Build/Owner | DNS has now propagated correctly (apex → 185.199.108–111.153, `www` → `wp-tszabo.github.io`), so the blocker noted on 2026-09-16 is gone. The Pages REST API path is blocked by the proxy, so the CEO can't flip it — needs the owner in repo settings, or option A. |
| Publish homepage copy once approved, then run the rubric and log it | CEO | Blocked on issue #2. |

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
| Survey candidate free data sources for Hormuz oil-flow volume | CEO (Research unavailable) | 2026-09-17 | Partial — candidates found (IMF PortWatch, EIA), but **no ToS clearance possible**; see decisions-log.md 2026-09-17 and critical issue #1. Reopened as the PortWatch licence-read item above. |
| Draft homepage copy (headline, methodology/about blurb) | CEO | 2026-09-17 | `company-memory/pending-copy/2026-09-17-homepage.md`, sent for review as issue #2. Drafting is done; publishing is not. |
| Stand up the async approval mechanics for real | CEO | 2026-09-17 | Labels `critical` / `needs-approval` / `needs-copy-review` created; issues #1 and #2 filed. Working auth path is authenticated REST against `api.github.com` (no `gh` CLI in this sandbox). |
