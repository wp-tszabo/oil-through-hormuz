# OKRs

Updated by the CEO at the start/end of each weekly cycle. Keep history —
don't delete past quarters/phases, mark them closed instead.

## Phase 1 — Prove the free-tier core product (current)

**Objective**: Ship a small, honest, reliably-updating Strait of Hormuz
oil-flow tracker on free/public data, before spending money or building
monetization.

| Key Result | Target | Status |
|---|---|---|
| KR1: Identify and validate a free, ToS-clear daily/periodic Hormuz flow data source | 1 primary source documented in `backlog.md` research findings, with a licensing check logged in `decisions-log.md` | **Met on "ToS-clear", missed on "daily"** (2026-09-17, 2nd cycle). Licence question is now *answered*, not blocked: **IMF PortWatch REJECTED** (`license: custom` → IMF terms forbidding systematic download, redistribution, compilation, derivative works). **EIA CONFIRMED CLEAR** (US public domain, attribution requested) and is the documented primary. But EIA's Hormuz release is annual/half-yearly — freshest figure (20.9 m b/d, 1H25) covers a period that ended ~14 months ago. So we have a source we may legally publish and no source that updates often enough for the product as conceived. Re-scope options with the owner on issue #1. |
| KR2: Publish a working site on GitHub Pages showing that data | Live URL, auto-updating, uptime tracked in `metrics.md` | **Partial / degraded** — content is live and verified this cycle (fetched and diffed byte-identical against the repo), but **HTTPS on the custom domain is broken** (critical issue #3): `https://oilthroughhormuz.com` and both `www` forms fail TLS. Only apex-over-HTTP and the `github.io` URL serve. Still no data shown, now because the only clear source is too stale to headline rather than because nothing is cleared. |
| KR3: Zero unreviewed copy reaches the live site | 100% of published copy has an owner-approval record | **On track** — 1 draft produced, still held (issue #2, unanswered), 0 published. Verified rather than assumed this cycle: fetched the live page and confirmed it contains only the original placeholder prose and zero data figures. |
| KR4: Run the self-check rubric on every publish | 100% of publishes have a `self-check-log.md` entry | **On track, and now meaningful again** — 0 publishes, 3 rubric runs logged. The live-site check that was INCONCLUSIVE on 2026-09-17 was re-run properly once egress returned and is now a genuine **PASS** on content (with the HTTPS degradation tracked separately, since the rubric has no availability column). |
| KR5: First weekly spend ceiling stays at ~$0 | Actual spend = $0 unless owner explicitly raises the ceiling | **On track** — $0 agent-committed. Separately, the owner bought `oilthroughhormuz.com` directly; logged 2026-09-16 as an explicit owner-approved exception, not agent spend. |

## Phase 2 — Graduation (not started)

Gated on the Phase 1 evaluation described in GOVERNANCE.md. No OKRs defined
yet — the CEO drafts these as part of the graduation proposal, justified
against specific Phase 1 findings (not proposed by default).
