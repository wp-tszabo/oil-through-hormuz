# Backlog

Prioritized work items. Owned by role. The CEO reorders/updates this every
cycle; specialists add findings and new items they surface. Move finished
items to "Done" with the date, don't delete them.

## Now (Phase 1, Week of 2026-09-14)

| Item | Owner | Notes |
|---|---|---|
| Identify candidate free data sources for Hormuz oil-flow volume (EIA, and any other public/free options) | Research | Must include a ToS/licensing check for each candidate — see GOVERNANCE.md critical-issue #3 |
| Recommend one primary source + update cadence it actually supports | Research | Daily is the goal; document what's realistically achievable free-tier |
| Scaffold static site structure + GitHub Pages deploy | Build | Done for the skeleton (see `site/`), but **Pages hosting is blocked**: the repo is private and Pages needs a paid plan for private repos on this account. Owner chose to stay private for now (see decisions-log.md, 2026-09-16). The `deploy-pages.yml` workflow exists but is manual-dispatch-only until a hosting decision is made (go public / upgrade plan / different host). Raise this as a decision the CEO needs from the owner before the site can actually go live, not something to route around quietly. |
| Wire the confirmed data source into the site (fetch → store → render) | Build | Blocked on Research's recommendation |
| Draft homepage copy (headline, methodology/about blurb) | CEO | Must go to owner review before publishing — never skip this checkpoint |
| Write Week 1 self-check log entry once site is live | CEO | Use `rubric.md` |

## Later (Phase 2, blocked until owner approves graduation)

| Item | Owner | Notes |
|---|---|---|
| Evaluate paid tanker-tracking / AIS data providers | Research | Do not start until Phase 1 evaluation is done and owner approves graduation |
| Monetization strategy (ads/affiliate/subscription) | Monetization | Dormant — do not start in Phase 1 |
| Budget proposal for paid data | CEO | Must be justified against a specific free-tier gap, not proposed by default |

## Done

_(none yet)_
