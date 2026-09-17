# Metrics

Updated by the CEO at the end of each weekly cycle (or by Build, for
uptime/data-freshness, as it observes them). Keep every week's row — this is
the trend line the CEO uses to judge Phase 1 before proposing graduation.

| Week of | Site uptime | Data freshness (max staleness observed) | Visits | Spend ($) | Ceiling ($) | Notes |
|---|---|---|---|---|---|---|
| 2026-09-14 (2nd mid-week snapshot, 2026-09-17 — week not yet closed) | **DEGRADED** — content up, HTTPS broken | N/A — no data feed wired (and none will be until the re-scope decision lands) | UNMEASURED | $0 agent-committed | ~$0 | Uptime is now *measured*, not inferred: egress returned, so the CEO fetched the site directly. Content serves correctly on `http://oilthroughhormuz.com/` and `https://wp-tszabo.github.io/oil-through-hormuz/` (both HTTP 200, byte-identical to the repo). But `https://` on the custom domain fails TLS (`*.github.io` cert), and `www` 301s into that broken URL — so the primary domain is unusable for normal visitors. Recorded as DEGRADED rather than up. Critical issue #3, needs owner action in Settings → Pages. Data freshness still N/A: PortWatch rejected on licence, EIA clear but ~14 months stale on its latest Hormuz figure. Spend $0, within ceiling. Still no analytics, so visits unmeasured by design. |
| 2026-09-14 (mid-week snapshot, 2026-09-17 — week not yet closed) | UNMEASURED | N/A — no data feed wired | UNMEASURED | $0 agent-committed (+ owner-paid domain, amount not reported to CEO) | ~$0 | Uptime is UNMEASURED, not 100%: the CEO's egress policy blocks its own site, so it has no way to observe uptime (critical issue #1). Indirect signal only — DNS correct, last Pages deploy `3fd9200` succeeded 2026-09-16. Data freshness is N/A rather than good: nothing is published, because no source has been ToS-cleared. No analytics installed, so visits are unmeasured by design. Agent-committed spend $0, within ceiling. |
