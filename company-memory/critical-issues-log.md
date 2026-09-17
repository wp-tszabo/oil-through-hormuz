# Critical Issues Log

Append-only. Log every critical issue the moment it's raised — even if it's
resolved within the same cycle. See GOVERNANCE.md for the four categories
(outage/stale data, overspend, legal/compliance exposure, hard-to-reverse
action) and the escalation mechanism (GitHub issue, label `critical`).

| Date raised | Category | Description | Immediate action taken | Status | Resolved date |
|---|---|---|---|---|---|
| 2026-09-17 | 3 (legal/compliance) + 1 (data verification) | Sandbox egress proxy returns a hard policy denial for every data-source and live-site domain the CEO needs: `eia.gov`, `api.eia.gov`, `imf.org`, `portwatch.imf.org`, `oilthroughhormuz.com`, `wp-tszabo.github.io`, and the GitHub Pages API path. Consequence: (a) no data source's ToS can be read in full, so none can be cleared — search snippets indicate IMF PortWatch is under the IMF's bespoke Data Terms (2024-10-11), explicitly not Creative Commons; (b) rubric §1's spot re-fetch is impossible, so the CEO cannot verify a published figure or detect a stale feed. No confirmed outage: DNS for the apex resolves to the four GitHub Pages IPs, `www` CNAMEs to `wp-tszabo.github.io`, and the last Pages deploy (`3fd9200`) succeeded 2026-09-16. | Paused all data wiring; cleared no source; published nothing (no commit touches `site/`, so no deploy fired). Candidate sources recorded as UNVERIFIED in `decisions-log.md`. Continued only the in-bounds part of the approved plan (copy drafting, held for review). Opened GitHub issue #1, label `critical`, with three options for the owner (allowlist / CI-side fetch+verify / accept the pause). | OPEN — awaiting owner decision | — |
