# Decisions Log

Append-only. Never edit or delete past entries — if a decision is reversed,
add a new entry that supersedes it and link back.

| Date | Decision | Rationale | Made by |
|---|---|---|---|
| 2026-09-16 | Company structure: CEO agent orchestrates Research, Build, and Monetization specialist subagents; all share persistent company-memory files. | Mirrors a small company so each function has a clear owner and the CEO has a single review point instead of doing everything itself. | Owner + Claude (setup) |
| 2026-09-16 | Weekly cadence: CEO proposes plan + $ spend ceiling → owner approves/amends → autonomous execution for the week → repeat. Approving a plan approves the approach, not every implementation detail. | Gives the owner control over direction and money without requiring them to review every step, which would defeat the point of autonomy. | Owner |
| 2026-09-16 | Website copy is a standing, permanent checkpoint — owner reviews all copy before publishing, in every phase. | Copy is the highest-visibility, hardest-to-silently-fix surface; worth a permanent human check even after trust is established elsewhere. | Owner |
| 2026-09-16 | Four critical-issue categories trigger an immediate interrupt outside the weekly cadence: site/data outage, overspend, legal/compliance exposure (esp. data ToS), hard-to-reverse actions. | Tanker-tracking/AIS-derived data specifically carries real redistribution-rights risk; outages and overspend need faster-than-weekly response. | Owner |
| 2026-09-16 | Phase 1 scope: free/public data only (e.g. EIA), build+publish the site, no monetization work, copy held for review, first spend ceiling ~$0. Graduation to Phase 2 (paid data/monetization) requires an explicit owner decision after 1-2 cycles, justified against a specific free-tier gap. | Start small and test the operating model itself before adding money or complexity. | Owner |
| 2026-09-16 | Scheduling platform: Claude Code cloud Routines (cron-based, min. 1hr interval), not Desktop scheduled tasks or session-scoped /loop. | Runs on Anthropic's infrastructure without requiring the owner's machine to be on, and without interactive permission prompts. | Owner |
| 2026-09-16 | Company home base: GitHub (wp-tszabo) for code + company-memory, with GitHub Pages as the eventual hosting target. | A cloud Routine isn't tied to a local folder, and a real hosted site needs somewhere like GitHub Pages regardless. | Owner |
| 2026-09-16 | Approval mechanics for an unattended, cron-scheduled CEO: async via GitHub Issues/PRs (`needs-approval`, `needs-copy-review`, `critical` labels) rather than a live prompt. If GitHub tooling isn't reachable, the CEO must mark items `NEEDS_OWNER_REVIEW` in company-memory and say so plainly — silence is never treated as approval. | The CEO has no synchronous human to ask; the mechanism must fail safe (blocking) rather than fail open. | Claude (setup), pending owner confirmation |
| 2026-09-16 | Repo scaffolded locally (agents, governance, company-memory, site skeleton) before GitHub push, because at setup time this machine had no `gh` CLI, no GitHub SSH key, and no git identity configured. Push to GitHub and cron Routine activation deferred pending owner input on auth method. | Earlier attempt (previous project, Cowork) got stuck on GitHub connector/local-folder issues; this time the local structure is built and verified before depending on any GitHub connectivity. | Claude (setup) |
| 2026-09-16 | `gh` CLI installed to `~/bin` (added to PATH via a new `~/.bash_profile`) and authenticated as wp-tszabo. Repo created as `wp-tszabo/oil-through-hormuz`, **private**, and pushed. | Machine had none of gh/SSH/git-identity configured; owner chose the gh-CLI login path (also needed for the async Issue/PR-based approval mechanics in GOVERNANCE.md). | Owner + Claude (setup) |
| 2026-09-16 | GitHub Pages deploy deferred — Pages isn't available for private repos on the free plan, and the owner chose to stay private and skip Pages for now rather than go public or upgrade. `deploy-pages.yml` trigger changed from `push` to `workflow_dispatch`-only so it doesn't fail on every push while hosting is undecided. | Avoid noisy, permanently-failing CI; revisit once a hosting decision (public repo, paid plan, or a different host) is made. | Owner |
| 2026-09-16 | Week of 2026-09-14 plan approved as-is (Phase 1, ~$0 ceiling). Owner approved directly in conversation rather than via a GitHub issue comment for this first week; the async GitHub-issue approval flow in GOVERNANCE.md remains the default mechanism for an unattended CEO going forward. | First-week bootstrapping; owner was present synchronously. | Owner |
| 2026-09-16 | Hosting decision resolved: made the repo **public** and enabled GitHub Pages (build via GitHub Actions), rather than staying private on a third-party free host (Cloudflare Pages/Netlify). `deploy-pages.yml` reverted to its `push`-triggered auto-deploy. No custom domain purchased — using the free `wp-tszabo.github.io/oil-through-hormuz` subdomain; a paid domain stays a deliberate future decision (and, per GOVERNANCE.md, domain changes are a hard-to-reverse action), not a default. | Nothing sensitive was in the repo (no secrets, just governance docs/placeholder site); staying public keeps everything on GitHub as already agreed, avoids a second service/account, and costs $0 — consistent with the Phase 1 ceiling. | Owner |
| 2026-09-16 | Owner purchased custom domain `oilthroughhormuz.com` (registrar: Name.com) and directed Claude to configure it as the site's custom domain, apex + `www`. This is real spend outside the Week 1 plan's ~$0 ceiling, and a domain change is explicitly named as a hard-to-reverse action in GOVERNANCE.md — logging it here as an explicit owner-approved exception rather than letting it pass as routine work. GitHub-side config (CNAME file, custom domain setting) done by Claude; DNS records at the registrar are the owner's to add (no registrar credentials shared, by design). HTTPS enforcement pending DNS propagation. | Owner wants a real domain now rather than deferring; approved directly and synchronously, same pattern as the Week 1 plan approval. | Owner |
| 2026-09-17 | **Owner directive: build a daily best-guess estimation methodology rather than waiting for a true daily source.** Given PortWatch is rejected and EIA alone is ~14 months stale, Research's mandate is extended (see `.claude/agents/research.md`) to design a model producing a daily estimated figure from licensed inputs only, recalibrated whenever a new real (EIA or equivalent) data point publishes, with a published methodology and a visible uncertainty range — never a falsely precise single number. Rubric §1 updated to require this explicitly for any modeled figure. This does not itself decide the separate IMF-permission-email question (issue #1, option A) — that remains open and unsent pending explicit owner go-ahead. | Neither "wait indefinitely for a licensable daily source" nor "publish a 14-month-stale number as the headline" serves the product; a transparently-labeled estimate, recalibrated on real anchors, can be honest and useful in a way a stale point figure can't. | Owner |
| 2026-09-17 | **No primary data source recommended or cleared this cycle.** Candidates surveyed and recorded as UNVERIFIED pending a full ToS read: (1) **IMF PortWatch** (portwatch.imf.org) — daily chokepoint transit calls + transit trade volume estimates for 28 chokepoints incl. Hormuz, AIS/satellite-derived, free, CSV/GeoJSON/API, refreshed weekly Tuesdays 09:00 ET. Best cadence match by a wide margin. **Licence blocker**: governed by the IMF's own bespoke Data Terms (effective 2024-10-11), explicitly *not* a Creative Commons licence; full text at imf.org/external/terms.htm is egress-blocked, so redistribution rights are UNKNOWN. (2) **EIA** — reuse is clear (US government work, public domain, acknowledgement with publication date requested), but cadence is poor: the World Oil Transit Chokepoints brief runs roughly biennial and the Hormuz figures in the Global Energy Security Data release appear quarterly. Reusable but not "daily". | Per GOVERNANCE.md critical-issue #3 and `research.md`, an unread licence is not a permissive one. PortWatch's terms could not be read, so it cannot be ingested; EIA can be ingested but cannot alone support the product's intended update cadence. Recording the finding rather than withholding it, and recording it as unresolved rather than rounding it up. | CEO (research done by CEO — subagent tooling unavailable this session) |
| 2026-09-17 | **Free-tier gap identified and recorded for a future Phase 2 justification** (not a proposal to graduate): no *licence-clear* free source is known to publish Hormuz oil-flow volume at daily cadence. The clear-licence source (EIA) is quarterly-to-biennial; the daily source (PortWatch) has an unresolved licence. If PortWatch's terms turn out to permit redistribution, the gap likely closes at $0 and no paid data is needed. | GOVERNANCE.md requires any future budget request to be justified against a specific free-tier shortfall rather than proposed by default. Logging the shortfall now, while explicitly noting the cheaper resolution must be ruled out first. | CEO |
| 2026-09-17 | Homepage copy drafted and **held** — written to `company-memory/pending-copy/2026-09-17-homepage.md` and opened for owner review as GitHub issue #2 (`needs-copy-review`). Deliberately contains no figures. Nothing in this cycle's commits touches `site/`, so no Pages deploy was triggered and nothing reached the public site. | Standing copy checkpoint; plus rubric §1 forbids publishing figures the CEO cannot spot-re-fetch, which is currently impossible (critical issue #1). | CEO |
| 2026-09-17 | Async approval mechanics activated for real: repo labels `critical`, `needs-approval`, `needs-copy-review` created; critical interrupt filed as issue #1, copy review as issue #2. Authenticated GitHub REST access confirmed working from the agent sandbox (as `wp-tszabo`); `gh` CLI is *not* installed in this environment, so the curl-against-`api.github.com` path is the working mechanism. | GOVERNANCE.md's approval mechanics assumed `gh`; that assumption was wrong for this session. Recording the working path so future cycles don't rediscover it. | CEO |
| 2026-09-17 (2nd cycle) | **IMF PortWatch REJECTED as a data source — licence does not permit redistribution.** Supersedes the "UNVERIFIED, pending ToS read" status recorded earlier the same day. Verified first-hand once egress was restored: every PortWatch dataset (`Daily_Chokepoints_Data`, `Chokepoints`, `Daily_Ports_Data`, `Ports`, `Disruptions`, spillover simulators) is `license: custom` with `licenseInfo: https://www.imf.org/external/terms.htm`. No CC licence, no open-data grant anywhere in the metadata. The IMF terms permit only "free non-systematic downloading … for personal, noncommercial usage only without any right to resell, redistribute, compile, or create derivative works", and require prior permission "to copy or download IMF Content in any systematic way", with Fair Use capped at 1,000 words of excerpt-for-commentary. | Our intended use — automated daily fetch, store, and re-publish on a public site — is systematic downloading, redistribution, compilation *and* derivative-work creation: four of the exact activities the terms prohibit, and nowhere near the Fair Use carve-out. It would also not survive the site becoming commercial in Phase 2. GOVERNANCE.md already treats an unclear licence as a no; this one is not unclear. Nothing was ever ingested, so there is no exposure to unwind — the guilty-until-checked rule did its job. | CEO |
| 2026-09-17 (2nd cycle) | **EIA CONFIRMED CLEAR as a source, with two caveats recorded.** Verified from EIA's reuse policy directly: US government publications are public domain, "may be freely used and distributed", with an acknowledgement including publication date ("Source: U.S. Energy Information Administration"). Caveat 1: EIA's chokepoint figures are "EIA analysis based on Vortexa tanker tracking" — we may republish EIA's published analysis with attribution, but must not imply we hold or license Vortexa's underlying data. Caveat 2: cadence is worse than previously assumed — the World Oil Transit Chokepoints table (last updated 2026-03-03) is annual 2020–2024 plus 1H25 only (Hormuz: 19.2 / 19.7 / 21.9 / 21.8 / 20.7 / 20.9 m b/d), i.e. the freshest published figure covers a period that ended ~14 months ago. | We need one source whose licence is beyond argument, and this is it. Recording the Vortexa caveat now so a future cycle doesn't overclaim provenance, and recording the true cadence because the previous cycle's "quarterly-to-biennial" estimate was optimistic — the copy draft's "weeks old" caveat is materially wrong against this and was flagged on issue #2. | CEO |
| 2026-09-17 (2nd cycle) | **Product re-scope escalated to the owner rather than decided by the CEO** (issue #1). With PortWatch rejected, no licence-clear free source publishes Hormuz oil-flow volume at anything like daily cadence, while real-world flows have reportedly fallen ~30% year-on-year in Q1 2026 amid regional conflict — so an EIA-only page would headline a 1H25 figure during a major disruption. Options put to the owner: (A) request written permission from `copyright@imf.org` — $0, reopens the daily-cadence product if granted; (B) re-scope honestly around EIA's real vintage and ship that; (C) open the Phase 2 paid-data conversation. CEO recommendation: **A now, B in parallel as what ships, C only if A fails.** | This changes the product's core promise, which GOVERNANCE.md puts outside the CEO's authority. Option C is deliberately not recommended: a budget request must be justified against a gap cheaper options couldn't close, and A is a free email that hasn't been sent. Asking for money before sending it would be precisely the lazy default that rule exists to prevent. **No email sent to the IMF** — outward-facing contact on the company's behalf is the owner's to authorise. | CEO |
| 2026-09-17 (2nd cycle) | **Broken HTTPS on the custom domain re-classified from a backlog task to a critical issue** (#3). `https://oilthroughhormuz.com/` and `https://www.oilthroughhormuz.com/` both fail TLS (edge serves `CN=*.github.io`); `http://www.…` redirects into the broken HTTPS URL. Only apex-over-HTTP and the `github.io` URL work. The CEO did **not** touch DNS or `site/CNAME`, and cannot reach the Pages API through the sandbox proxy, so the fix is the owner's in Settings → Pages. | The previous cycle logged this as "HTTPS enforcement pending DNS propagation" and parked it as routine. It isn't routine: it is the primary domain being unusable for every normal visitor, which is critical-issue category 1. Also recording the lesson — the earlier egress block was read as "can't verify our own site" when it was in fact partly masking a real outage, which is exactly the blind spot category 1 exists to prevent. Domain/DNS changes stay untouched because GOVERNANCE.md names them hard-to-reverse. | CEO |
| 2026-09-17 (2nd cycle) | Sandbox egress policy changed mid-day without notice or owner action — domains that hard-denied in the morning cycle (`eia.gov`, `portwatch.imf.org`, `imf.org`, `wp-tszabo.github.io`) all returned HTTP 200. Recording this as an environmental fact the company cannot rely on either way. | Two cycles on the same day saw opposite network conditions. Any capability that matters (data freshness checks, uptime monitoring, source re-fetch for the rubric's spot-check) must therefore not depend on the CEO sandbox's egress — which strengthens the standing recommendation to move fetch + verification into GitHub Actions regardless of how anything else resolves. | CEO |
| 2026-09-17 | Subagent delegation did not happen this cycle — the Agent/Task tool was unavailable, so Research and Build briefs could not be dispatched. CEO performed a reduced-depth research pass itself and did no Build work. Flagged to the owner in issue #1 and in the cycle report rather than silently absorbed. | The company's design assumes a CEO plus specialists; running as a single agent changes both capacity and the review model (no independent output for the CEO to review). That is a structural fact the owner should know about, not an implementation detail. | CEO |
| 2026-09-17 (2nd cycle) | Subagent delegation failed again — the Agent/Task tool was still unavailable this session, so the Research and Build briefs the approved plan assigns could not be dispatched for a second consecutive cycle. The CEO again did the research itself and did no Build work. Recording it a second time rather than treating it as already-known. | This is now a pattern, not a one-off glitch, and it should be weighed in the Phase 1 evaluation: the company has not yet once operated as designed. Every research finding so far — including the PortWatch rejection, which is a consequential call — has been made by the CEO with no independent specialist output to review it against. That removes one of the two layers this structure was built to provide. The owner should know the quality bar has been "one agent checking its own work", not "CEO reviewing a specialist". | CEO |
| 2026-09-17 (3rd cycle) | **EIA's Hormuz cadence finding from the 2nd cycle was WRONG and is hereby superseded: EIA publishes Hormuz chokepoint flows QUARTERLY, not annually.** The 2nd cycle concluded the only EIA Hormuz output was the World Oil Transit Chokepoints table (annual 2020–2024 + 1H25, freshest figure ~14 months stale) and built the whole re-scope argument on that. It missed that EIA launched a **Global Energy Security Data** supplement on 2026-05-13 expressly to publish chokepoint flows quarterly. Verified first-hand by fetching and parsing `eia.gov/outlooks/steo/report/energysecurity/article.php`: release date 2026-08-12, Hormuz total oil by quarter 1Q25 20.9 / 2Q25 21.0 / 3Q25 21.3 / 4Q25 21.6 / 1Q26 14.9 / **2Q26 4.9** m b/d, with crude+condensate, products and LNG broken out. Real lag is ~6–10 weeks, not 14 months. | The company spent two cycles reasoning from a pessimistic error, and the error pointed towards asking the IMF for a licence and towards a Phase 2 paid-data conversation — i.e. it pushed us towards spending. Correcting it in the opposite direction matters more, not less. Recorded as a superseding entry rather than an edit, per the append-only rule. Also a lesson about method: the 2nd cycle found *a* relevant EIA page and stopped; it did not ask whether EIA had a newer product. | CEO |
| 2026-09-17 (3rd cycle) | **WTO Strait of Hormuz Trade Tracker REJECTED on licence — new candidate, checked and closed the same cycle it was found.** `datalab.wto.org/Strait-of-Hormuz-Trade-Tracker` publishes daily AIS-derived crude, LNG and other volumes — exactly the cadence the product wants. Rejected because the underlying data is **AXSMarine (Signal Group)**, a commercial vendor, surfaced under "© WTO 2026" with no open-data grant and a "contact AXSMarine for data terms" pointer. Not ingested, not used for calibration, not used to sanity-check anything. | GOVERNANCE.md's guilty-until-checked rule: commercial vendor data behind an unstated licence is a no, and the fact that it is republished by an intergovernmental body does not launder the vendor's terms. Recording the rejection so a future cycle doesn't rediscover the tracker and assume a WTO URL means open data. | CEO |
| 2026-09-17 (3rd cycle) | **The daily best-guess model the owner directed is designed, back-tested, and judged NOT publishable as a daily point figure in the current regime** (`company-memory/methodology.md`). The model is anchored on EIA's quarterly figure with a persistence shape function, because no cleared higher-frequency input exists to justify anything more elaborate. Back-test against the cleared series: predicting each quarter from the prior one is accurate to **1.4%** through 4Q25, then errs **+45%** (1Q26) and **+204%** (2Q26). A band wide enough to have contained 2Q26 spans roughly **1.5–7 m b/d** on today's anchor — wider than the quantity being estimated — and EIA says the anchor itself is being revised frequently because Hormuz AIS data has been unreliable since end-February 2026. | The owner's directive was to build the model, and it is built; the question of whether its output is honest enough to headline is separate, and under GOVERNANCE.md is not the CEO's alone. Shipping a single daily number at that uncertainty would be rubric §1.4/§3.2 FAIL and critical-issue category 4. The model is not wasted: it becomes genuinely good (±3%) the moment flows are boring again, and a regime detector decides which state we are in from cleared data only. | CEO (decision on publication escalated to owner, PR #4 / issue #5) |
| 2026-09-17 (3rd cycle) | **Recommendation revised: the IMF permission email (issue #1 option A) is no longer worth sending, in the CEO's view — but the decision stays the owner's and the item stays open.** Two reasons it got less attractive this cycle: (1) EIA turned out to be quarterly rather than annual, so the gap the IMF licence was meant to close is much narrower than believed; (2) PortWatch is raw-AIS-derived, and EIA has documented that Hormuz AIS is *especially unreliable* precisely during the current disruption — so we would be negotiating a licence to obtain a daily number that is systematically understated exactly when it matters. | Recording a reversal of the CEO's own prior recommendation explicitly rather than letting it quietly lapse. The previous cycle recommended "A now, B in parallel"; the evidence changed, so the recommendation changes. Still not the CEO's call to send or not send outward contact on the company's behalf — the owner closed issue #1 with "network access resolved", which answers the egress question and not this one, and closure is not authorisation. | CEO |
| 2026-09-17 (3rd cycle) | **Two cycles of company memory were found on an unpushed detached HEAD and recovered onto `main`.** `main`/`origin/main` were still at the 1st cycle's commit; the 2nd cycle's three commits existed only locally, unreferenced by any branch. Verified they touch no `site/` files, fast-forwarded `main`, pushed. See `critical-issues-log.md` for the full entry. New standing rule adopted: **every cycle must end by verifying its memory commit is on `main` AND on `origin/main`**, and the cycle report must state the pushed commit SHA. | Company memory is defined by GOVERNANCE.md as the source of truth across sessions; memory that exists only in one sandbox's local git is not that. This was a near-miss on losing a legally consequential record (the PortWatch rejection) — the kind of loss that would have caused a future cycle to redo work and possibly re-approach a rejected source. | CEO |
| 2026-09-17 (3rd cycle) | Subagent delegation failed for a **third** consecutive cycle — the Agent/Task tool is still not present in this environment, so Research and Build received nothing again. The CEO did the research, wrote the methodology, and built the page itself. | Recording it a third time because the pattern is now the single largest unaddressed risk to output quality: the company has never once run as designed. Everything consequential this cycle — a source cleared, a source rejected on legal grounds, a model back-tested, a page built, and a judgement that the owner's own instruction shouldn't be followed literally — was done by one agent with no independent specialist to check it. The methodology doc says so in §8 rather than presenting itself as reviewed work. This belongs in the Phase 1 evaluation as a structural finding, not a footnote. | CEO |
| 2026-09-17 (4th cycle) | **OWNER DECISION — the daily model estimate becomes the headline figure, labelled as an estimate. This overrules the CEO's recommendation and closes the question raised as critical issue #5.** Owner on PR #4 (comment `5716791659`, 15:16:58Z): *"The daily figure is the estimate. That is the real value of the whole page thta we develop a model that make that estimate. So let's add 'estimated ' keyword to the title but let's keep the daily figure."* Implemented on branch `copy-review/homepage-v2`: title, H1, unit line and a standalone label all say "estimate"; headline figure is the model's point estimate for 2026-09-16 (4.9 m b/d); the band 1.5–6.9 m b/d sits immediately under it; the methodology section explains the persistence anchor, the back-tested band and the regime test in plain English; the measured EIA quarters remain as the chart, relabelled as the anchor rather than the headline. `methodology.md` §6 marked SUPERSEDED with a new §10 recording the decision; `hormuz.json` flips `daily_estimate_published` to true and records who authorised it. | The escalation worked as designed: the CEO refused to publish a dated point figure on its own authority because it touched critical-issue category 4, put the call to the owner with options, and the owner made it. **Deliberate interpretation, stated so it can be challenged**: the owner's instruction was "estimated in the title, keep the daily figure", and the CEO shipped that *plus* a visible band. The band was not the owner's ask, but `rubric.md` §1.6 requires one for any modelled figure, and the owner was never asked to waive a rubric clause — only to decide which number leads. The two are compatible; only "a bare number with no range" would have conflicted, and nobody asked for that. If the owner wants the band removed, that is a rubric amendment and needs saying explicitly. | Owner (decision) + CEO (implementation) |
| 2026-09-17 (4th cycle) | **New risk accepted and recorded rather than hidden: the page is now stale by construction.** A dated daily estimate that nothing refreshes will still be reading "16 September 2026" next week. Not raised as a critical issue today, because on the day of publication every word on the page is true and the date is visible to the reader; raised as the **top Build item** instead, and flagged to the owner on PR #4. Because `shape(d) = 1`, the daily job is genuinely small: re-date the estimate, widen the band with distance from the anchor, re-anchor when EIA publishes. | Honest labelling solves the "is it a measurement" problem but not the "is it current" problem, and the second one arrives automatically with the owner's decision. Better to name it at the moment it is created than to discover it as a category-1 incident in a week. | CEO |
| 2026-09-17 | **Owner confirmed "Strait" (not "Straight") is the correct spelling for the site.** Owner, live in conversation: *"Confirming 'Strait' (the page uses this; your original note said 'Straight')."* No site change needed — the page already uses "Strait" throughout; this closes the open confirmation item, leaving only the copyright-line name outstanding. | The original owner spec spelled it "Straight of Hormuz"; the CEO used the correct spelling ("Strait") on the page and flagged the discrepancy on PR #4 rather than silently deciding it was a typo. Owner has now confirmed. | Owner |
| 2026-09-17 (4th cycle) | Subagent delegation failed for a **fourth** consecutive cycle — the Agent/Task tool is still absent, so the Build brief that this page change would naturally have been (implement the owner's decision, re-run the numbers) went undispatched and the CEO implemented it itself. | Recorded again, briefly, because the pattern is unchanged and it is the Phase 1 evaluation's main structural finding. The specific cost this cycle: the judgement that "estimated in the title + a band" correctly honours both the owner's instruction and rubric §1.6 was made and reviewed by the same agent. | CEO |
| 2026-09-17 (5th cycle) | **OWNER DIRECTIVE, three parts, on the now-live homepage.** Verbatim: *"About the new copy: this is a customer facing site, so we need to change that explanation text to be more appealing. As for the trend breakdown we should not quote and exact source. The whole purpose of the site is to develop a proprietary method for calculating/estimating the flow by aggregating different data sources, news, reports, etc... It is the CEO's responsibility to keep improving this proprietary methodology. For the terms, copyright, etc... those should be put into the footer of the page behind links, and not have the text on the main page"*. Parsed as: (1) rewrite the explanatory copy as appealing customer-facing product copy; (2) do not name the provider in the visible trend/chart copy — the product is a proprietary aggregation method, not a pass-through; (3) move Terms/Copyright out of the main body into footer links. | Recorded verbatim because parts 2 and 3 change what the page *is*, not just how it reads, and part 2 sits adjacent to a critical-issue category. Implemented on `copy-review/homepage-v3`, held in **PR #6** (`needs-copy-review`) — a copy change to a live page is still a copy change, and the standing checkpoint does not lapse because v2 already shipped. | Owner (directive) + CEO (implementation) |
| 2026-09-17 (5th cycle) | **STANDING MANDATE ESTABLISHED: the CEO owns continuous improvement of the proprietary estimation methodology.** Per the owner's explicit words, expanding the model's input set over time — additional data sources, news, reports — as licence-clear ones are found is an ongoing CEO responsibility, not a one-off task. Written into `okrs.md` (new Phase 1 KR6), `methodology.md` (new §11), `.claude/agents/ceo.md` and `.claude/agents/research.md`. Every candidate input still has to clear the same unchanged bar: GOVERNANCE.md's guilty-until-checked licence rule, and no uncleared source may be used "just to calibrate". | This is the first time the company has a standing product mandate rather than a backlog of discrete tasks, and it needs to survive fresh sessions — hence writing it into the agent definitions and the OKRs, not just the decisions log. The licence bar is restated in the same breath deliberately: a mandate to add inputs is exactly the pressure under which the guilty-until-checked rule gets quietly relaxed. | Owner (mandate) + CEO (implementation) |
| 2026-09-17 (5th cycle) | **DESIGN DECISION on the source-attribution question, stated so the owner can overrule it.** The owner asked that the visible trend copy not name an exact source. Today the model has **exactly one** licence-clear numeric input (the EIA public-domain quarterly series), and GOVERNANCE.md category 4 / rubric §1.1/§3.2 forbid overstating the data's authority or originality. Two extremes were both rejected: (a) stripping attribution entirely, letting "our proprietary model" imply we observe the strait or already blend many feeds — a category-4 misrepresentation and a rubric FAIL, which the CEO would have raised as a critical issue rather than shipped; (b) refusing the directive and keeping the provider's name on the headline — unwarranted, since moving a citation off the headline is not dishonest and the owner's product logic is sound. **Shipped synthesis**: the visible primary copy speaks only of "our model"/"our method"; the full attribution (publisher, dataset, table, release date, licence, Vortexa provenance caveat, publisher's AIS-reliability warning, and the daily trackers checked and rejected) moves **intact** to a new linked `sources.html`, reachable from the chart caption, the methodology blurb and the footer. `index.html` now contains zero occurrences of "EIA", "Energy Information Administration", "Vortexa", "PortWatch", "AXSMarine" or "WTO" (grep-verified); `sources.html` carries all of them. The page also does **not** fabricate breadth: `sources.html` says outright "One cleared dataset, and we say so rather than implying a wider net", and the aggregation ambition appears as a "Where this is going" section describing ongoing work, not current capability. | The honest differentiator today is the *method* and the commitment to widen its inputs — both true — rather than a claimed input diversity that is not yet true. Rubric §1.1 ("every number traces to a specific, cited source") is judged satisfied by a citation reachable through an explicit in-context link from the chart it describes, the same way a footnote satisfies it; that judgement is recorded as a judgement, not assumed, and is stated on PR #6 so the owner can disagree. If the owner wants *no* visible pointer to the source at all, the CEO will raise that as a critical issue before implementing it rather than complying — that version is the one that crosses into misrepresenting the data's authority. | CEO (design), escalated for owner review on PR #6 |
| 2026-09-17 (5th cycle) | **The 1.5–6.9 band was again kept on the main page, deliberately, while everything else moved behind links.** The owner's directive was to move Terms/Copyright/Sources off the main body; the band is neither, and `rubric.md` §1.6 requires a *visible* uncertainty range for any modelled figure. A range behind a link is not a visible range. | Same call as PR #4, made again rather than treated as settled, because the v3 layout created fresh pressure to move it. Changing it is a rubric amendment and needs the owner to say so explicitly, not a layout decision the CEO makes while tidying a footer. | CEO |
| 2026-09-17 (5th cycle) | **Owner merged PR #6 directly on GitHub with no comment (merge commit `fff1efc`, 15:59 UTC).** Treated as approval of the v3 copy as drafted, including the source-attribution synthesis in the entry above (visible copy says "our model"; full attribution one click away via `sources.html`) — the PR explicitly asked for a yes/no on that judgement and offered to bring it back for discussion, and the owner merged rather than commenting to override it. Deploy workflow triggered on the merge; site now serves v3. | Same pattern as PR #4: the owner's mechanism for approving a copy-review PR is merging it. Recording the inference explicitly (silence-as-override is not assumed elsewhere in this log; here the merge action itself is the signal) so a future cycle doesn't need to re-derive whether "no comment" meant approval. | Owner |
| 2026-09-17 (5th cycle) | Subagent delegation failed for a **fifth** consecutive cycle — the Agent/Task tool returned "Task is disabled for this session, in subagents as well as here." Two fully-written briefs went undispatched: a Build brief to implement the v3 pages, and a Research brief to run the *first pass of the new standing mandate* (scout licence-clear producer-side export series, JODI-Oil, OPEC MOMR, UN Comtrade, Gulf customs/port authorities, and public-domain maritime advisories such as UKMTO/MARAD for the regime detector). The CEO implemented the pages itself; the research pass is carried into the backlog undone. | Recorded a fifth time, and the cost is now concrete rather than abstract: the owner has just made input-expansion a standing mandate, and the specialist whose entire job that is cannot be reached. The Research brief is preserved in the backlog so a future cycle can dispatch it verbatim rather than re-derive it. | CEO |
| 2026-09-18 (6th cycle) | **Treat the frozen 16-September estimate date as a fired category-1 critical issue, and fix it on live in the same cycle rather than wait for review.** | The page headlined "estimate for Wednesday 16 September 2026" on 18 September while separately promising the reader a figure "carried forward to the day you are reading" — so the page as a whole asserted something false, not merely something old. The 4th cycle had already ruled that this exact situation *would be* category 1, so treating it as routine maintenance would have quietly overruled a prior decision of the company. On fixing it live without waiting: the alternative was leaving a knowingly false sentence in front of readers for an unknown number of days. The fix changed **no prose and no figure** — persistence means the point is 4.9 for any day past the anchor and all three dates sit inside the same one-quarter band horizon — so it is a defect repair against the design the owner **already approved on PR #4**, not a new editorial choice. GOVERNANCE.md contemplates publish-then-verify where waiting is untenable; the rubric was re-run and logged, and issue #7 offers the owner a one-line revert. | CEO |
| 2026-09-18 (6th cycle) | **Do NOT self-approve the automation that makes the fix durable — hold `scripts/refresh_estimate.py` and its daily cron in PR #8.** | A one-off date correction and a standing mechanism that edits live site content on a schedule with no human in the loop are different kinds of act. The weekly plan approves an approach, not the creation of an unattended publisher. The line drawn: **repairing today's content is CEO work; installing something that will publish tomorrow's content unattended is an owner decision.** Recorded explicitly because the pressure to merge it was real — the automation is the actual remedy for the critical issue raised the same morning. | CEO |
| 2026-09-18 (6th cycle) | **KR6 cycle 1: adopt EIA Global Energy Security Data Table 2 (companion chokepoints + world supply) as a cleared model input; upgrade the regime detector to v2 (calm / disrupted-local / disrupted-systemic).** | Satisfies the standing mandate via options (1) and (2) together. Found by applying the company's own hard-won process lesson — *ask whether the publisher already has more than the obvious product* — to EIA itself: the supplement has ten tables, not one. Licence risk is **nil**: same publication, same release, same US federal public-domain status already cleared for Table 4. The gain is real — the detector can now distinguish a Hormuz-specific disruption from a global one, which the ±10% single-series rule could not do at all. 2Q26: Hormuz −67.1% while the control group (Danish + Turkish + Panama, which carry no Gulf barrels) **rose** 8.1% and world supply rose 3.7%. | CEO (Research unavailable, 6th consecutive cycle) |
| 2026-09-18 (6th cycle) | **State plainly that the published band does NOT change as a result, rather than manufacture a band movement.** | Both disrupted quarters classify as `local`, so there is no `systemic` history to calibrate a separate band against. The honest result of a better detector was a better *diagnosis*, not a different *number*, and the band stays 1.5–6.9. Written that way in `methodology.md` §12.3 and in PR #8 in those words. A mandate to keep improving the methodology is precisely the pressure under which a cosmetic change gets reported as progress; declining to do so is the decision being logged. | CEO |
| 2026-09-18 (6th cycle) | **Add a hard horizon guard (`MAX_HORIZON_DAYS = 92`): past the back-tested horizon the model suppresses the point estimate entirely instead of widening the range.** | The §4 back-test only measures one-quarter-ahead error. Beyond that the band is decoration, not evidence, and publishing it would imply a validation that was never done. Refusing to answer is a legitimate output for an honest model. **The consequence is dated and material**: the anchor covers through 2026-06-30, so the horizon expires **2026-09-30**, and EIA is not expected to publish 3Q26 until ~November — meaning the site's headline number most likely disappears at month end for several weeks. | CEO |
| 2026-09-18 (6th cycle) | **Escalate the horizon-guard consequence to the owner as a product decision rather than installing it as a silent safety mechanism.** | Merging PR #8 blanks the site's main number in twelve days. A safety constraint that removes the product's headline is not an implementation detail, even though its *motivation* is pure honesty and the CEO believes it is correct. Flagged at the top of PR #8, cross-linked from issue #7, and logged as a pre-emptive category-4 row in `critical-issues-log.md` with the owner decision needed **before 2026-09-30**. Alternatives offered: different threshold, or fall back to the measured quarter plus the chart. | CEO |
| 2026-09-18 (6th cycle) | **JODI-Oil REJECTED on licence.** | The most valuable candidate the mandate has produced — monthly producer-side Gulf export data, exactly the "second anchor at better than quarterly cadence" `methodology.md` §11 identified as the model's biggest gap. Terms read in full at `jodidata.org/terms-of-use.aspx`: *"The Intellectual Property rights in the JODI Website, and in the material published on it ... **All such rights are reserved.**"* The download page's "for free" refers to price, not to redistribution rights, and no open-data grant exists anywhere on the site. **Not ingested and not used "just to calibrate".** Logged prominently because this is the first time the standing input-expansion mandate and the guilty-until-checked licence rule pulled in opposite directions, and the licence rule won without argument — which is the outcome GOVERNANCE.md requires and the one §11 predicted would be hardest. | CEO |
| 2026-09-18 (6th cycle) | **EIA Table 1 (strategic inventories) not adopted — its freshness is illusory.** | Titled "as of August 2026", which reads like a monthly signal, but the table's own note says *"Data for 2Q26 are through June 2026 or the latest available"* and its columns are quarterly. Recorded so a future cycle that rediscovers the enticing title does not spend effort concluding the same thing twice — the same failure mode that cost this company two cycles on EIA's cadence. | CEO |
| 2026-09-19 (7th cycle) | **The recurring stale date was fixed on live by hand for the second consecutive day — and logged as a treadmill, not as a fix.** | Live page headlined "estimate for Thursday 17 September 2026" while served on Saturday 19 September, and the methodology copy promises a figure "carried forward to the day you are reading". Same defect as critical issue #7, one day later. Re-dated to Friday 18 September in `site/index.html` and `hormuz.json`; **no prose, no figure** — `shape(d)=1` so the point estimate is 4.9 for any day past the anchor, and 18 Sep is 80 days past the anchor end, inside the 92-day horizon, so the band is untouched. The decision worth recording is not the fix but the framing: hand-re-dating a page that claims to be dated daily **only works on days a cycle happens to run**, so it is not a control, and it was escalated on issue #7 in those terms rather than reported as resolved. | CEO |
| 2026-09-19 (7th cycle) | **EIA Short-Term Energy Outlook Table 3d adopted as a cleared input — monthly, and two months fresher than the anchor.** | Found by applying the company's own hard-won lesson one level higher than last cycle: cycle 1 asked whether the Hormuz *supplement* had more than one table (it has ten); this cycle asked whether **EIA** had a higher-cadence product than the quarterly supplement. It does — the supplement is a quarterly annex to a **monthly** STEO whose workbook carries per-country crude production. Licence CLEARED on a first-hand read of `eia.gov/about/copyrights_reuse.php` (US federal public domain, acknowledgement requested); **zero new licence surface**, same publisher and terms as the existing anchor. History runs through **2026-08**, verified from the workbook's own `Last Historical Month--- 202608` field rather than inferred from column headers — the load-bearing check, because STEO is a forecast product running to 2027 and reading the columns naively would have fed EIA's forecasts into our model as if they were observations. See `methodology.md` §13.1. | CEO |
| 2026-09-19 (7th cycle) | **GPCI built as an index on a single consistent variable, accepting incomplete coverage to avoid a silent unit error.** | GPCI = crude production of Iran + Iraq + Kuwait + Saudi Arabia + Bahrain, all `copr_` series. **UAE and Qatar excluded** even though they are material Hormuz producers: this workbook carries them only as `papr_` (petroleum *and other liquids*), a different variable, and summing the two would have produced a plausible-looking total that no downstream check would catch. This was a live near-miss — a first label match pulled UAE from Table 3b and was caught only by noticing the series code was `papr_tc`. Oman excluded because its export terminals lie outside the strait. Consistency over coverage, with the incompleteness recorded as a limitation in `methodology.md` §13.6 rather than hidden. | CEO |
| 2026-09-19 (7th cycle) | **Regime detector v3: monthly, and the 2026 disruption is now dated and diagnosed.** | v1 was a ±10% quarterly test; v2 added a chokepoint control group but was still quarterly and so could only notice a disruption a quarter late. v3 runs on GPCI monthly, with data landing ~2–3 weeks after month end instead of ~11 weeks. It dates onset to **March 2026** (−36.4% m/m), the trough to **May 2026**, and a recovery in June/July — then correctly drops back to `unstable` on August's −11.1% instead of declaring an all-clear. Separately, the flow/GPCI ratio is 1.070–1.085 across four calm quarters (sd 0.006) and collapses to 0.410 in 2026Q2, which establishes for the first time that **this is a transit constraint, not a production constraint** — a distinction the model previously had no way to draw. | CEO |
| 2026-09-19 (7th cycle) | **The new input contradicts the published figure, and the figure was NOT changed — escalated as critical issue #9 instead.** | 2026Q3 GPCI (Jul–Aug, history) is 14.42, up 20.6% on the Q2 trough. Applying every transit ratio ever observed gives implied Q3 flows of 5.9 / 11.8 / 15.5 — **all above the published point estimate of 4.9**, with the lowest sitting at the top of the published 1.5–6.9 band. So the bottom half of the range we tell readers to "treat as the answer" is now supported by nothing. The CEO did not re-fit the model: changing a published figure needs the owner, a fresh rubric run and the copy checkpoint, and the derivation is one cycle old with no specialist review. Four options put to the owner (leave; widen upward; re-anchor on GPCI; suppress now), recommending widen-now / re-anchor-after-review. The counter-argument was stated on the issue as prominently as the finding: the transit ratio is unstable, which is precisely why a low Q3 ratio could still put the truth inside the current band. | CEO |
| 2026-09-19 (7th cycle) | **`sources.html` deliberately NOT updated to mention the new input.** | The page promises to say what is in the model **today**, and GPCI is cleared and analysed but is **not feeding the published number** — the live headline is still persistence on the quarterly anchor. Listing a cleared-but-unused input under "What is in it today" would overstate input diversity, which the CEO's standing mandate names as a category-4 critical issue. Copy drafted and held at `pending-copy/2026-09-19-sources-v3-gpci.md`, explicitly **conditional** on issue #9 resolving in favour of adopting the input, with an instruction to discard rather than bank the draft if the owner declines. A source we have analysed is not a source that is feeding the number. | CEO |
| 2026-09-19 (7th cycle) | **UKMTO and US MARAD recorded UNRESOLVED (could not read terms), not rejected and not worked around.** | Both returned HTTP 403 at origin. Verified this was the origin and not our proxy — `eia.gov` and `msi.nga.mil` fetched fine in the same pass and the proxy reported no relay failures. No user-agent spoofing was attempted to get past the block: these are exactly the sources whose access terms would matter most if we later ingested them, so quietly evading a WAF to read a licence would be self-defeating. Recorded as UNRESOLVED because an unread licence is not a permissive licence. NGA Maritime Safety Information *was* reachable but was **not adopted for low signal** — its Gulf warnings are wrecks, survey operations and an inoperative beacon, which say nothing about oil flow; its licence was not pursued because an unusable input does not need clearing. Bucket (2) of the Research brief stays open. | CEO |
| 2026-09-19 (8th cycle) | **OWNER DECISION — the one-quarter horizon guard is approved exactly as designed in PR #8, including the consequence that the site's headline number most likely goes blank around 2026-09-30.** Owner, live in conversation: *"one quarter is fine for now, we should extend it later"*. Two separable instructions, and they are recorded separately on purpose. **(1) Now**: `MAX_HORIZON_DAYS` stays at **92**; past the back-tested horizon the point estimate is suppressed and the page reads "No current estimate — awaiting the next published quarter" rather than extrapolating. The threshold was **not** changed, no alternative (different threshold, or falling back to the last measured quarter) was adopted, and none was chosen by the CEO in passing. **(2) Later**: extending how far the model can be trusted is explicitly named as **future work**, not something to act on today — see the following entry. This closes the "DECIDE BEFORE 2026-09-30" item and the pre-emptive category-4 row in `critical-issues-log.md`. | The owner was asked to accept a known, dated product consequence knowingly rather than inherit it from a safety mechanism the CEO installed quietly, and did. Recording the exact words because the decision has two halves and only one of them authorises action. | Owner |
| 2026-09-19 (8th cycle) | **"Extend the tested horizon beyond one quarter" is adopted as ongoing future work under the standing KR6 methodology mandate — and deliberately NOT started this cycle.** The owner's "we should extend it later" is read as a direction of travel, not a work order, so nothing was built, no threshold was moved, and no back-test was stretched. Recorded as a KR6-linked backlog line and an OKR note. **Treated as a distinct concern from the existing "widen the inputs" line, not a duplicate of it**, because they can each happen without the other: widening inputs adds a *series*; extending the horizon requires *evidence about error at 2+ quarters out*, which can also come from back-testing further history of the input we already have, or from a higher-cadence input that produces measurable one-month-ahead errors more often. They are related — the most likely route to a longer trusted horizon is a higher-cadence cleared input, which is exactly the widen-inputs work — so the backlog line points at it rather than restating it. | Two reasons for the separation. First, honesty about what is tested: the horizon is a property of the *back-test*, not of the input set, and conflating them would let "we added a source" masquerade as "we can now see further". Second, the owner said "later" in plain words; a standing mandate to keep improving the methodology is precisely the pressure under which "later" quietly becomes "this cycle". | CEO (recording an owner directive) |
| 2026-09-19 (8th cycle) | **PR #8 merged to `main` by the CEO** (merge commit `160498a`), on the owner's explicit instruction above. Deploy workflow `35457474108` succeeded; live page re-fetched and byte-identical to `main`. This is the first time the CEO has merged a `needs-copy-review` PR itself rather than the owner merging it. **The authority is the owner's direct instruction in this session, not the weekly plan** — the week of 2026-09-14 is `DONE` and the week of 2026-09-21 is still `PROPOSED`, which under GOVERNANCE.md would otherwise make this cycle read-only. Written down explicitly so it is not mistaken for a precedent: a PROPOSED plan still blocks publishing; what unblocked it here was the owner speaking. | GOVERNANCE.md's plan mechanism is a proxy for owner approval when the owner is not present. When the owner is present and explicit, the proxy is not the binding constraint — but the distinction has to be on the record, because "the CEO merged its own copy PR" is exactly the sentence a future cycle could cite while the owner is silent. | CEO, on explicit owner instruction |
| 2026-09-19 (8th cycle) | **Two plumbing defects found in PR #8 during pre-merge re-verification and fixed before merging (`82d6e86`), rather than merged and patched afterwards.** (1) **The automation would have updated the repo without updating the site.** GitHub's documented rule: *"Events triggered by the GITHUB_TOKEN will not create a new workflow run, with the following exceptions: `workflow_dispatch` and `repository_dispatch`."* The refresh bot's push to `main` would therefore **not** have fired `deploy-pages.yml`. `main` would have looked fresh, the job would have gone green, the daily log would have said "refreshed" — and the live page would have stayed frozen. That is critical issue #7 all over again in a form that is *harder* to detect than the original, because the evidence would point the wrong way. The job now dispatches the Pages deploy explicitly and fails red if it cannot. (2) **The page write was not idempotent** — it appended a blank line to `site/index.html` on every run, so the "nothing changed, publish nothing" guard could never fire and the file would grow without bound. Markers and indentation are now rewritten verbatim; verified byte-identical over three consecutive runs. Also added a rebase before push so a concurrent company-memory commit is a retry, not a red build. **Both are implementation details inside an approved design: no figure, band, threshold, prose or copy changed.** | The owner approved a mechanism that keeps the *live page* current. A version that keeps only the repository current would have satisfied the letter of the PR and none of its purpose. Fixing it before the merge rather than after keeps the merged state the reviewed state. | CEO |
| 2026-09-19 (8th cycle) | **The automation was verified end-to-end on live infrastructure, not just in the sandbox.** After merging, the refresh workflow was dispatched manually: run `35457521885` succeeded, committed `3ecd690` as `hormuz-refresh-bot`, and its deploy-dispatch step created deploy run `35457530338`, which succeeded. The live page was then re-fetched and diffed byte-identical to `main`. **This also proves defect (1) above was real**: the deploy run that published the bot's commit was triggered by `workflow_dispatch`, not by the push. Live state after the run: estimate for Friday 18 September 2026, 4.9, band 1.5–6.9, horizon 80/92 days, regime `disrupted/local` — unchanged figures, as intended. | A mechanism that has only ever run on a developer's machine is not a control. The first unattended scheduled run is 05:10 UTC on 2026-09-20; it now has a green manual precedent rather than being its own first test. | CEO |
| 2026-09-19 (8th cycle) | **One residual copy defect in the suppressed state was found, deliberately NOT fixed in the merge, and held for owner review.** When the horizon guard fires, the sentence immediately below the generated block still reads *"The range is this wide because the strait is anything but steady right now"* — sitting directly under a block that says we have stopped publishing a number. It is incoherent rather than untrue, and it will become visible around 2026-10-01. It is user-facing prose, so it goes through the standing copy checkpoint: drafted to `pending-copy/2026-09-19-suppressed-state-note.md`, added to the backlog with the 30 September date on it, and flagged on PR #8. | The standing copy checkpoint has no "while I was in there" exception, and the merge of PR #8 was authorised on a specific question the owner answered — the horizon design — not as a general licence to edit the page. A one-sentence fix is exactly the size of change that erodes a checkpoint. | CEO |

## 2026-09-20 (9th cycle) — read-only cycle: bypass term measured, live figure untouched

**Context.** The week of 2026-09-14 closed `DONE` on 2026-09-19. The plan for
the week of 2026-09-21 is still `PROPOSED` (GitHub issue #10, opened
2026-09-19T02:21Z, **no owner comment**). Under GOVERNANCE.md that makes this a
read-only cycle: research and prep allowed, no spend, no publishing, no
hard-to-reverse action. Everything below was decided inside that boundary.

**Decision 1 — the live date lag was assessed as NOT a critical issue, and the
reasoning was written down rather than assumed.** The opening check found the
headline reading "Friday 18 September 2026" at 02:20 UTC on the 20th. The
previous two occurrences of a wrong date *were* category 1. This one differs in
the property that made those ones dangerous: the refresh job computes
`today(UTC) − 1` and runs at 05:10 UTC, so the 00:00–05:10 window carries the
day-before-yesterday and then self-corrects. Bounded, mechanical, ~2h50m from
correcting itself at the moment of the check. Logged in full in
`critical-issues-log.md` with an explicit trigger: if the live `for_date` is
still 2026-09-18 after 05:10 UTC today, it **is** category 1 and gets raised as
a new issue. Recording the trigger in advance is the point — it stops the next
cycle from re-litigating the judgement under time pressure.

**Decision 2 — the date was NOT hand-fixed, and the workflow was NOT manually
dispatched.** Three independent reasons, any one sufficient: read-only mode
forbids publishing; hand-re-dating was already proven not to be a control
(issue #7, second occurrence); and — the one that would have applied even
without the other two — **pre-writing the answer would have destroyed the
evidence.** Today's 05:10 UTC run is the first unattended cron fire in the
company's history. If the CEO sets the date first, the job finds nothing to
change, commits nothing, and the single test that matters returns a false green.
The same argument rules out a manual `workflow_dispatch`. Instead the date
*semantics* problem was written up as held copy
(`pending-copy/2026-09-20-date-semantics.md`), because the real defect is not
the lag, it is that a single global date label is wrong for Gulf readers
overnight while the page promises a figure "carried forward to the day you are
reading".

**Decision 3 — KR6 delivered as (b), and it argued against our own previous
work.** `methodology.md` §15: the bypass term that §13.6 listed as "real and
unmeasured" is now measured, using only already-cleared EIA tables and opening
**zero** new licence surface. Trend-residual method with a placebo control on
non-Gulf routes. Result: Bab el-Mandeb crude runs **+2.32 m b/d above its own
2025 trend** in 2Q26 (and **−0.05**, i.e. dead on trend, in 1Q26 — an
out-of-sample hit that is the main reason to believe the signal), Suez/SUMED
shows no bypass, and the bypass term explains **42%** of the collapse in the
transit ratio. Consequence: §13.3's headline finding that "2026 is a transit
constraint, not a production constraint" **survives but was overstated by
roughly a factor of two**, and is corrected in place rather than defended.

**Decision 4 — the recommendation on critical issue #9 was refined, not
reversed, and the live figure still did not move.** Carrying the bypass term
explicitly into 2026Q3 gives **6.5–10.2 m b/d** against a published 4.9 and a
band topping at 6.9 — a much tighter range than §13.5's 5.9 / 11.8 / 15.5, and
tighter because a mechanism is named rather than a ratio picked. Three
independent constructions now all land above 4.9. **Option C on issue #9 was
respecified as C′**: re-anchor on a *bypass-adjusted* GPCI estimator, not raw
GPCI — a raw-GPCI re-anchor would land near 15.5 and would be wrong for a reason
we can now name. Recommendation is **B now, C′ after review**. Posted as a
comment on issue #9; **nothing on the live site changed**, because changing a
published number needs the owner, a fresh rubric run and the copy checkpoint,
and none of that is available in a read-only cycle no matter how good the
evidence. That constraint working *against* our own best finding is the
checkpoint doing its job, not an obstacle to route around.

**Decision 5 — the week-of-21 plan was revised while staying `PROPOSED`.** It
was written at 02:21 UTC on 19 September; by that evening the owner had approved
the horizon and the CEO had merged PR #8, so two of its three "blocking owner
decisions" were already resolved before anyone read it. Asking the owner to
decide settled questions wastes the scarcest resource the company has. The file
now carries a revision note, the resolved items are listed as resolved, and
issue #10 was updated to point at the revised version. Objectives and the $0
ceiling are unchanged; **the status is unchanged and the plan is still not
executed.**

**Decision 6 — the derivation was written as a script, not as a table.**
`scripts/bypass_analysis.py` re-fetches both cleared sources and recomputes
everything, including rebuilding GPCI from the September workbook (which
reproduces §13.2 to two decimals). With the Agent tool unavailable for a **ninth**
consecutive cycle — re-tested this cycle, `No such tool available: Task` — the
designed control of "a specialist produces, the CEO reviews" still does not
exist. A reproducible script is a weak substitute, but it is a real one: a reader
can re-run the claim instead of trusting the agent that made it. The script
touches nothing under `site/`, so it cannot trigger a deploy.

**Not done, recorded so it is not silence**: no candidate-input scouting this
cycle. Bucket (2) (UKMTO/MARAD — 403 at origin, not licence-rejected), OPEC
MOMR, UN Comtrade, Eurostat, Gulf customs, and the "does EIA publish anything
weekly" question all carry forward verbatim in `backlog.md`. The cycle spent its
effort on the input we already had, which is the other legitimate half of the
standing mandate.

---

## 2026-09-21 (10th cycle) — a weekly input that argues against our own conclusion; the automation is verified unattended

**Cycle mode: read-only, for the second consecutive cycle.** The
week-of-2026-09-21 plan (issue #10) is still `PROPOSED` with no owner response
since it was posted on 19 September and revised on the 20th. Under
GOVERNANCE.md that permits research and prep and forbids spend, publishing and
hard-to-reverse action. Nothing under `site/` was touched. The published figure
is unchanged at **4.9, range 1.5–6.9**.

### Decision 1 — the first unattended cron run is verified, and the residual on KR2 is closed

Checked before anything else, from the Actions API rather than inferred from the
page: refresh run **`35503239041`** (`event=schedule`, `success`) → bot commit
**`9a1d712`** → Pages deploy **`35503243978`** (`success`, head `9a1d712`) →
live page re-fetched byte-identical to `main`. All three legs the plan demanded.
**KR2's "auto-updating" half is met unattended for the first time**, nine cycles
after it was first claimed.

### Decision 2 — the trigger we wrote last cycle was wrong, and it is corrected in the open

The scheduled run fired at **09:46 UTC against a 05:10 UTC cron** — a 4h36m
delay, because GitHub Actions schedules are best-effort. Three consequences were
recorded rather than quietly patched:

1. The "bounded, self-correcting ~5-hour window (00:00–05:10 UTC)" written down
   on 2026-09-20 **is not the real window**. On 20 September it was ~9h46m, and
   it has no guaranteed upper bound.
2. The category-1 trigger written last cycle — *"more than one day behind
   outside the 00:00–05:10 window"* — **would have misfired** on ordinary
   scheduler latency, declaring a critical issue where none existed. A
   false-positive interrupt is cheap by design, but a trigger that fires on
   normal behaviour is one that gets ignored, which is how a real one gets
   missed.
3. **A skipped cron is entirely silent.** `refresh_estimate.py` fails loudly
   only when it runs. GitHub can drop scheduled runs under load, and nothing
   anywhere would go red — the page would simply freeze, exactly as in critical
   issue #7, with the automation's green history as false reassurance.

**Decision**: not raised as an interrupt — the site is showing current, correct
data and was inside its documented tolerance at check time, so what is defective
is our monitoring and our own arithmetic, not a misstatement to a reader. The
trigger is **replaced** with: category 1 if a two-days-back date persists past
**~12:00 UTC**, or if **no `event=schedule` refresh run has succeeded in the
preceding 36 hours**. The second condition is the one that catches a silent
skip, which the old trigger could not express at all. The uptime-monitor backlog
item is widened from "HTTP 200 + certificate validity" to also assert data
freshness and that the job actually ran — it remains owner-gated on the plan.

### Decision 3 — KR6 cycle 5: adopt a weekly cleared input, analysis-only

The plan's cheapest open lead was *"does EIA publish anything **weekly** that is
Gulf-relevant?"*. It does: **Weekly Preliminary Crude Oil Imports by Country of
Origin** (release 2026-09-16, next release 2026-09-23, history to 2010), with
Saudi Arabia and Iraq reported weekly. Licence re-read **first-hand this cycle**
at `eia.gov/about/copyrights_reuse.php` rather than inherited from prior cycles
— including its "protected materials" carve-out for third-party content, which
was checked and does not bite, because these are EIA/Census survey statistics
rather than a vendor feed. **Zero new licence surface.** `ir.eia.gov` returned
403 on one probe and was left alone, not retried with a spoofed user-agent,
consistent with the UKMTO/MARAD precedent.

This is the **third** time the question "does this publisher have a
higher-cadence product?" has paid off — annual→quarterly→monthly→weekly — and
that single question has now produced **every input the model has**. It is
recorded here because it is the strongest standing argument against a Phase 2
paid-data proposal: OPEC MOMR, UN Comtrade, Eurostat and the Gulf customs
authorities have still never been checked once.

### Decision 4 — report the finding that undercuts our own recommendation, prominently

The new input was expected to strengthen critical issue #9. It partly does the
opposite, and that is written as the headline of `methodology.md` §16.4 rather
than buried in the limits.

What it confirms: the collapse was real and **Gulf-specific** — five consecutive
weeks of *zero* Gulf-origin arrivals ending 2026-07-31, against a non-Gulf
placebo control that ran **+6.6%** over the same window (a −106.6 point
divergence). And the arrivals trough (July) sits exactly one voyage after the
GPCI production trough (May), so three structurally unrelated inputs now agree
on this disruption's timing.

What it undercuts: the aggregate recovery (−27.3% of calm, for barrels loaded
18 Jul–7 Aug, i.e. *inside* the Q3 gap) **splits** into **Saudi Arabia +16.4%**
and **Iraq −89.0%**. A recovery visible only in the producer that owns a
non-Hormuz route, while Basrah crude that must transit the strait stays shut, is
the fingerprint of **production recovering while transit does not** — §15's
bypass mechanism showing up in an unrelated dataset.

**Decision**: the *direction* of issue #9 stands (Q3 loadings at −18/−27% of
calm are hard to reconcile with a published figure implying −77%, and the bottom
of the 1.5–6.9 band remains supported by nothing), but the CEO recommendation is
revised to be **more** conservative than last cycle's: **B now — widen the band
upward, keep 4.9 as the point estimate — and do NOT adopt C′ until a 3Q26
chokepoint observation exists (~November).** Last cycle said "C′ after review".
The implied Q3 figure this company has proposed has now shrunk on three
consecutive cycles (5.9/11.8/15.5 → 6.5–10.2 → evidence that even that is
top-heavy), which means a re-anchor adopted at any earlier point would already
have been wrong. That pattern is the argument for waiting, and it is worth more
than any single derivation.

### Decision 5 — no copy drafted for the new input, deliberately

`sources.html` was **not** updated and no new draft was written. The input is
analysis-only; listing an analysed-but-unused source would overstate the model's
input diversity, which is critical-issue category 4 — the same reason §13's GPCI
copy is still held and conditional. There are already two unreviewed one-line
drafts in the queue; adding a third speculative one for an input the owner has
not accepted would be noise rather than diligence.

### Standing conditions, unchanged

Agent tool unavailable for a **tenth** consecutive cycle (re-tested: `No such
tool available: Task. Task is disabled for this session, in subagents as well as
here.`). Every judgement above was made and reviewed by the same agent; the only
mitigation remains that the derivation is a script — `scripts/weekly_arrivals_analysis.py`
— which re-fetches all nine country series from source on every run, so a reader
can re-run the claim instead of trusting the agent that made it. It touches
nothing under `site/`. Spend **$0**, tenth consecutive cycle.

---

## 2026-09-22 (11th cycle) — the model is tested against a second publisher for the first time, and the input that does it is held out on licence

**Context.** Fourth consecutive read-only cycle. The week-of-21 plan (#10) is
still `PROPOSED` and critical issue #9 is still open; neither has had an owner
response since 2026-09-19/20. Under GOVERNANCE.md that means no spend, no
publishing, no hard-to-reverse action — only research and prep. That is how this
cycle ran, and the live figure is untouched at **4.9, band 1.5–6.9**.

**Decision 1 — the opening critical-issue check was run against the corrected
trigger, and found nothing.** Last cycle discovered that the previously written
category-1 trigger would have misfired on ordinary GitHub scheduler latency, and
that a *skipped* cron is completely silent. The corrected trigger — "no
successful `event=schedule` refresh run in 36 hours" — was checked against the
Actions API rather than inferred: run `35589882310` succeeded at
2026-09-21T10:39:14Z, 15h41m before the check. Live bytes byte-identical to
`origin/main`. EIA source spot re-fetched; release still 2026-08-12, Table 4
unchanged. No issue.

**Decision 2 — the estimate date was again NOT hand-fixed.** At 02:20 UTC the
page read 2026-09-20, two days back. That is the known 00:00–05:10 UTC design
window of the owner-approved automation, not a frozen date. Hand-fixing it would
return a false green on precisely the automation we are trying to observe. Third
consecutive cycle this call has been made the same way, and it is recorded again
because it *looks* like the kind of thing an unattended agent should tidy up.

**Decision 3 — a new fact about that window, which makes the pending copy draft
more justified, not less.** Scheduler latency now has three observations: the
cron asks for 05:10 UTC and actually fired at 09:46, 09:46 and 10:39 —
consistently ~4.6–5.5 hours late and never early. So the honest worst-case stale
window is **~10–11 hours, not the ~5 hours** recorded two cycles ago. This
strengthens the case for the held `pending-copy/2026-09-20-date-semantics.md`
draft, and it was **not** used as a reason to publish that draft unilaterally.

**Decision 4 (the substantive one) — aim the KR6 pass at independence rather than
cadence, and admit that a previous cycle overstated its result.** Five KR6 passes
had widened the model from quarterly to weekly, but **every input came from one
publisher, the EIA**. That is a correlated-error problem: EIA itself warns that
Hormuz AIS data has been unreliable since end-February 2026 and is being revised
frequently, so agreement among four EIA-derived series may be agreement about one
blind spot. §16 claimed "three structurally unrelated inputs now agree"; that is
**corrected in §17 as overstated** — three different series, one publisher.
Overstating *independence* is the same failure mode as overstating input
diversity, just quieter, and it is the kind of thing only the agent that wrote it
can catch.

**Decision 5 — the test, and what it found.** Eurostat `nrg_ti_oilm` (EU27 crude
imports by partner country, monthly) is a destination-side *customs declaration*
— methodologically about as far from Vortexa-derived AIS as a free source gets.
Derivation: `scripts/eu_imports_analysis.py`, which re-fetches every series on
each run.

- **Placebo passes decisively**: Gulf partners **−65.0%** against their own
  2024–25 calm mean in 2Q26; non-Gulf control (US, Norway, Nigeria, Brazil,
  Kazakhstan, Libya) **+4.5%**; divergence **−69.5 points**. Not an EU demand
  story.
- **Sensitivity recorded because the script's own cutoff is load-bearing**:
  Kuwait and Iran are structural zeros (calm means 5.2 and 0.2 kt/month) and were
  excluded rather than reported as fabricated −100% collapses; excluding the
  borderline UAE series too gives −47.5% and **−52.0 points**. The conclusion
  survives either choice, so the threshold is not doing the work — but a cutoff
  that could change a headline is a parameter and is written down as one.
- **The §15/§16 split reproduces**: **Saudi −16.7%, Iraq −78.2%** — the same
  *ordering* as the US weekly arrivals (+16.4% / −89.0%). Producer with a route
  around the strait holds up; producer whose barrels must transit it is on the
  floor. Agreement is ordinal, not numerical, and is described that way.
- **Onset independently recovered as March 2026**, matching §13.3's GPCI dating
  from a different publisher.

**Decision 6 — and the input is NOT adopted, on licence.** Eurostat's terms were
read first-hand including the Exceptions section. The general grant permits
commercial *and* non-commercial reuse with acknowledgement. But an exception makes
*"data for countries other than"* EU/EFTA/candidate states **non-commercial only**,
and Saudi Arabia and Iraq are outside that list. Their own Switzerland/Austria
clarification points to the **declarant** reading — which would make our use
commercial-safe — **but that is our inference from their text, not their grant,
and an inferred permission is not a permission.** Verdict: **CLEARED
non-commercial, AMBIGUOUS commercial.**

It therefore does not enter `site/data/hormuz.json`, does not touch the published
figure, and `sources.html` was **not** updated — listing an analysed-but-unused
source would overstate input diversity, category 4, the same discipline applied
to §13's GPCI and §16's weekly series. **The hazard being guarded against is a
silent flip**: adopt it now, approve monetization later, and the licence status
of a *live* input changes with no alert anywhere in the system. Logged as a
pre-emptive category-3 entry.

**Decision 7 — no third `critical` GitHub issue was opened, and the reasoning is
recorded so it can be audited and overruled.** No exposure has been incurred,
nothing is published, and the action is already paused by the read-only state.
Issues #9 and #10 have been open and unanswered since 19/20 September; a third
interrupt would dilute the channel rather than sharpen it. It is instead surfaced
as an explicit owner decision on the plan, in `backlog.md`, and as a comment on
#10. **If a future cycle is ever tempted to adopt this input, that temptation is
the moment this becomes a real interrupt.**

**Decision 8 — what this does to critical issue #9: almost nothing, stated
plainly.** The Eurostat Gulf series end at **2026-06**, exactly where the anchor
ends, so it corroborates the *mechanism* without adding forward information about
3Q26. Recommendation **unchanged** from last cycle: **B now** (widen the band
upward, keep 4.9 as the point estimate), **C′ not before a 3Q26 chokepoint
observation exists (~November)**. A cycle that produces striking new evidence and
does *not* move its recommendation is the honest outcome here.

**A Phase 2 finding that did not exist before this cycle.** Monetizing is not
free of data cost even if no subscription is bought: the best free corroboration
found so far is non-commercial-only-or-ambiguous. Any graduation proposal must now
state **which inputs are commercial-safe**, and the Phase 1 evaluation in
`okrs.md` has been updated to say so.

**Eleventh consecutive cycle with no specialist review.** The Agent tool returned
`No such tool available: Task. Task is disabled for this session, in subagents as
well as here.` The bucket-(2) scouting pass was therefore run by the CEO at
reduced depth, exactly as the week-of-21 plan authorises for that case: UKMTO,
MARAD MSCI and OPEC were all re-probed and all returned **403 at origin**. None
was worked around — no user-agent spoofing, on precisely the sources whose access
terms would matter most — and **none is licence-rejected; they are unread, which
is a weaker and more honest status.** UN Comtrade and Gulf customs/port
authorities remain unchecked and carry forward verbatim. Mitigation unchanged:
the derivation is a script that re-fetches from source, so a reader can re-run the
claim instead of trusting the agent that made it. Nothing under `site/` was
touched. Spend **$0**, eleventh consecutive cycle.

## 2026-09-23 (12th cycle) — read-only again; a commercial-safe, non-EIA input found and cleared, analysis-only

**Decision 1: fifth consecutive read-only cycle.** Issue #10 (week-of-21 plan) and
issue #9 have had no owner response. Every comment since 2026-09-21 is the CEO's
own progress note; they are posted through the owner's token, so they were
checked by content, not by login. The plan file is still `PROPOSED` and the
owner-decision boxes are unchecked. Nothing was published, spent, or merged.

**Decision 2: the opening health check is clean, but one of its instruments
degraded, so the check says so rather than reporting green.** This sandbox's
egress proxy re-signs TLS, so `ssl_verify_result=0` proved only the proxy chain.
Origin certificate state was confirmed from Certificate Transparency instead
(Let's Encrypt, valid to 2026-12-16). The Pages API is proxy-blocked. This is
logged in `critical-issues-log.md` as a further argument for the owner-gated
monitor running on GitHub infrastructure.

**Decision 3: KR6 cycle 7, type (a) analysis-only plus (b). Japan Ministry of
Finance trade statistics (HS 2709 by origin, via e-Stat).** Chosen to fill both
gaps §17 left: a *commercial-safe* non-EIA input, and cleared data reaching into
3Q26. The licence was read first-hand before any download: Customs notice (EN
and the authoritative JA page), PDL1.0, and e-Stat terms. **CLEARED, commercial
and non-commercial**, on condition of source citation plus an "edited by"
statement, and never presenting our output as government-produced. It is the
first non-EIA input that is commercial-safe.

**Decision 4: findings reported by weight, and two overclaims removed from our
own draft.** Robust: Japan's total crude imports fell ~60% in Apr–May (third
independent statistical system), and the no-bypass-falls-further ordering
(Kuwait vs Saudi) holds in all four disrupted months, matching §16 (US) and §17
(EU). Directional only: no-bypass Kuwait crude shows partial recovery in July
arrivals (−55% from −100%), but that is roughly one cargo. Removed: a "−716 pt
divergence" vs a non-Gulf "control" that is actually the substitution source.
Also corrected: a leap-year denominator.

**Decision 5: issue #9 recommendation unchanged, a second cycle running.** B now,
C′ not before ~November. The direction gains modest support; the magnitude is
not informed.

**Decision 6: not adopted into the published model, no copy drafted.** This is a
read-only cycle, the input cannot set a level, and `sources.html` describes only
what is in the model today. When a plan is approved, the candidate adoption
path is as a recovery/regime signal, not a level. It would need a rubric run and
owner-approved copy carrying the PDL1.0 citation and edit statement.

**Decision 7: no new GitHub issue opened.** Nothing is critical. The two open
threads get one short comment each rather than another long one. Five cycles of
long progress notes have drawn no response, so brevity is the remaining lever
on the channel.

Spend **$0**, twelfth consecutive cycle. No Agent tool (12th cycle); reduced-depth
CEO pass.
