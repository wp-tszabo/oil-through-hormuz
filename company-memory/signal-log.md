# Signal log — tier-2 reported facts about the Strait of Hormuz

Started 2026-11-17 (70th cycle), per the owner's 2026-11-16 directive
(GOVERNANCE.md → "Prediction mandate and information sources") and the
amended weekly plan `weekly-plans/2026-11-15.md`.

**What this file is.** A dated, cited, reliability-graded record of discrete
facts — news reporting, maritime advisories, insurer/market commentary,
producer/port announcements — that may inform the prediction model as event,
regime or level signals **without needing a licence clearance**, because the
risk is in copying a source's content, not in using what happened.

**Rules this file follows (GOVERNANCE.md, binding):**
- Cite, never copy. Source link + date for every entry. No bulk re-hosting.
- Read, don't scrape. Every entry below was fetched and read directly
  (WebFetch on the specific URL), not bulk-scraped. Any lead that could only
  be reached by circumventing a paywall/login/CAPTCHA is logged as **NOT
  READ** and not used.
- Reliability graded per entry. A single unconfirmed post/claim is a lead,
  not a fact, and does not move the published figure.
- A fact moves the published figure only once confirmed by two independent
  sources, or by one primary/official source (here: UKMTO, JMIC, CENTCOM
  statements reported by a news outlet still count as primary once the
  primary body's own words are quoted directly and read directly — the
  outlet is the access path, not the source of the claim).
- "Entered the model" below means: did this fact change the published point,
  band, or regime classification? For this cycle, the answer for every entry
  is **no** — all are logged as regime/baseline *context* corroborating what
  the cleared EIA data already shows, not as inputs that moved a number. None
  of these change `site/data/hormuz.json`.

---

## 2026-11-17 (70th cycle) entries

| Date of fact | Fact | Source (read directly) | Reliability | Status | Entered model? |
|---|---|---|---|---|---|
| 2026-11-10 (reporting as of) | UKMTO's own latest weekly transit count: **170 outbound + 155 inbound** vessel transits through the strait, ~**65% below pre-conflict levels**. Most transponder-on traffic uses the Iranian-side route. UKMTO states it "cannot independently verify" the higher US Navy-reported counts. | [Gulf News, "Hormuz shipping 'below normal, but not stalled': UKMTO"](https://gulfnews.com/world/mena/hormuz-shipping-below-normal-but-not-stalled-ukmto-1.500741839) (fetched and read directly, page shows "Last updated: November 10, 2026") | **High** — UKMTO is a primary official maritime-security body; its own figures are quoted directly in the article, not paraphrased from an unnamed source. | Confirmed (one primary source, quoted directly) | No. This is a vessel-**count**, structurally different from EIA's volume (m b/d) figure. Converting one to the other needs an unvalidated per-vessel-cargo assumption. Logged as corroboration that the model's own "disrupted" regime classification is directionally right — not as an input. |
| 2026-11-01 to -03 | **JMIC Update 111 Advisory Note** (distributed via UKMTO): 4 attacks on commercial vessels in the strait within ~96 hours, up from 3 in the preceding reporting period, all off Oman's Musandam coast; threat level held at **"severe"**; Hormuz traffic described as "substantially reduced" vs. the 2025 baseline, single-digit to low-double-digit transits per day; ~31 US-facilitated transits/day (down slightly from ~34/day for Oct 24–30). Two further attacks recorded in the Arabian Gulf (total 8 since Oct 7, one north of Qatar, UKMTO ref 196-26). | [Gulf News, "Hormuz attacks rise as Iran steps up pressure on shipping, UKMTO warns"](https://gulfnews.com/business/energy/hormuz-attacks-rise-as-iran-steps-up-pressure-on-shipping-ukmto-warns-1.500737866) (fetched and read directly) | **High** — JMIC is a primary multinational naval-intelligence body; its own advisory text is quoted/paraphrased directly from the article's description of the note, dated and numbered (Update 111). | Confirmed (one primary source) | No. Qualitative incident/threat-level signal, no flow-volume magnitude. Logged as regime-detector/baseline context: the threat level stayed "severe" through early November, which is consistent with — not contradicted by — the EIA-measured 3Q26 partial volume recovery (§81), because recovery here is managed/escorted, not a return to calm. |
| 2026-11-07 | A tanker was struck by an unidentified projectile ~15 nautical miles north of Khasab, Oman; all crew reported safe. | Reported consistently in both Gulf News articles above (two independent reads of the same underlying UKMTO report, consistent on date, location and outcome) | **High** — primary source (UKMTO), consistent across two independently fetched articles | Confirmed (2 independent reads, same primary source) | No. Single-incident, no magnitude; logged as a dated regime-relevant event only. |
| Week ending 2026-11-06 | At least 11 ships attacked in and around the strait in the week ending Nov 6, three sank. UKMTO has recorded **88 projectile strikes since hostilities "resumed" in early July 2026** (implying a lull before July, then renewed escalation). | [Gulf News, "Hormuz attacks rise..."](https://gulfnews.com/business/energy/hormuz-attacks-rise-as-iran-steps-up-pressure-on-shipping-ukmto-warns-1.500737866) (fetched and read directly, AP figures relayed via Gulf News, UKMTO cumulative count quoted directly) | **High** — primary (UKMTO cumulative count) plus wire-service (AP) weekly toll | Confirmed | No. Important **timeline** fact for the baseline write-up (§81.6): the "hostilities resumed in early July" framing means the EIA-measured partial 3Q26 recovery (Jul–Sep, to 9.1 m b/d) happened *during*, not instead of, renewed attacks — i.e., the recovery is a managed/escorted-transit story, not a calm-return story. Used only as narrative context, not as a numeric input. |
| as of 2026-11-01 | CENTCOM blockade-enforcement figures (since enforcement began in July 2026): **144 commercial vessels redirected, 4 disabled, 2 boarded** for compliance checks. | [Gulf News, "Hormuz attacks rise..."](https://gulfnews.com/business/energy/hormuz-attacks-rise-as-iran-steps-up-pressure-on-shipping-ukmto-warns-1.500737866) (fetched and read directly; CENTCOM is the primary originator, Gulf News is the single read path this cycle — not independently cross-confirmed against a second outlet) | **Medium-High** — primary originator (CENTCOM), but read via only one citation chain this cycle | Confirmed-via-one-primary-source (CENTCOM), not independently cross-confirmed by a second outlet | No. Mechanism context only: explains *how* any transit continues at all alongside a "severe" JMIC threat level (an active US-enforced convoy/redirection system), supporting the baseline write-up's characterization of the recovery mechanism. |
| 2026-11-10/11 | **UNCONFIRMED, low reliability.** An IRGC statement (relayed by Bernama) claims a tanker struck a naval mine and exploded in the strait after using a route "not authorised" by Iran; UKMTO said separately it had received a report of "an incident" and advised caution. | Found via search snippet only; **NOT independently fetched and read this cycle** | **Low** — single source, the substantive causal claim (mine, unauthorised route) originates from a belligerent party's own statement (IRGC), not independently corroborated | **Unconfirmed** | No. Flagged only so a future cycle knows to look for independent confirmation (flag-state, insurer, or UKMTO's own causal assessment) before treating the cause as fact. The bare "an incident occurred, UKMTO advised caution" part is plausible given the pattern above, but is not elevated past "lead" here. |
| — | S&P Global Commodity Insights, "Hormuz Oct crossings at 3-month high despite attacks" | [spglobal.com link found via search](https://www.spglobal.com/energy/en/news-research/latest-news/shipping/110226-hormuz-oct-crossings-at-3-month-high-despite-attacks-red-sea-traffic-also-rises) — **fetch attempted, returned HTTP 403 (paywalled)** | n/a | **NOT READ — not cited, not used.** Logged only to record the lead was tried and is blocked, per the standing rule against circumventing paywalls. | No. |
| 2026-11-01 to -10 | United Against Nuclear Iran (UANI) "Iran Shipping Update" figures: ~31.5 US-facilitated transits/day, 126 recorded Nov 1–4. | Found via search summary only; **not independently fetched and read this cycle** | **Low-Medium** — UANI is an advocacy organization, not a neutral primary body; its figure is directionally consistent with JMIC's independently-confirmed ~31/day figure above but was not itself independently verified this cycle | **Unconfirmed** (redundant with the already-confirmed JMIC figure above, so not needed to establish the fact) | No. |

## Net reading from this cycle's signals

Every confirmed tier-2 signal this cycle is **consistent with, and does not
contradict**, the EIA-measured 3Q26 figures (§81 of `methodology.md`): the
strait is "well below normal but not stalled," the recovery since July is
managed/escorted rather than organic, and the threat level has stayed
"severe" throughout the quarter being measured. No signal this cycle rises to
the two-independent-sources-or-one-primary-source bar for anything that would
move a numeric input — everything here is corroboration of the regime
classification (`model.regime = "disrupted"`, kind `"local"`), not a new
input. Future cycles: keep reading UKMTO/JMIC-sourced reporting directly
(both cleared this cycle as readable via news coverage even though UKMTO's
own domain stays blocked) — it is the single most load-bearing tier-2 source
class found so far for the regime detector.

## 2026-11-18 (71st cycle) entries

| Date of fact | Fact | Source (read directly) | Reliability | Status | Entered model? |
|---|---|---|---|---|---|
| 2026-11-10/11 | Four UKMTO-attributed attacks: **Fujairah Energy** struck 2026-11-10 in the Arabian Gulf (multiple crew injured, taken ashore); an unidentified tanker struck 2026-11-10 ~19nm NE of Lima, Oman; **NCC Fajr** struck ~0200 UTC 2026-11-11 north of Khasab (UKMTO first reported it unconfirmed, then reclassified as an attack); **Dominica Prosperity** struck ~1800 UTC 2026-11-11 ~14nm NW of Ras Al Khaimah, UAE (22 crew evacuated, no casualties). Separately, JMIC's 2026-11-12 advisory update: **181 recorded maritime-security incidents since 2026-03-01**; **~211 commercial vessels stationary** at anchorages east of Hormuz (Fujairah, Khor Fakkan, Sohar, Musandam); threat held at "severe." NCAGS: **~34 US-facilitated transits/day** over the latest 96-hour period (Nov 8-11), flagged by the article itself as not directly comparable to independent tracking. | [gCaptain, "Vessels in the Strait of Hormuz, as seen from Musandam"](https://gcaptain.com/tanker-ablaze-off-uae-as-more-attacks-rattle-gulf-shipping/) (fetched and read directly, dated 2026-11-12) | **High** - UKMTO/JMIC primary bodies, their own advisory text/figures relayed directly, not paraphrased from an unnamed source. | Confirmed (one primary source each, quoted/relayed directly) | No. Four more named incidents and higher cumulative/anchorage-congestion counts, consistent with - not contradicting - the already-established "severe, managed-transit" baseline (methodology.md section 81.6). No m b/d magnitude; the 211-vessels-waiting and 181-incidents-since-March figures extend the picture but don't change a numeric input. |
| October 2026 (monthly total); 2026-11-07 (CENTCOM action) | Washington Institute for Near East Policy count: **37 ships attacked in October 2026**, described as "the highest monthly total since the war began." Separately, CENTCOM: a US military aircraft disabled a St Kitts-flagged cargo vessel on 2026-11-07 after it visited an Iranian port and tried to leave regional waters in violation of the US naval blockade. | [Baird Maritime, "Markets are betting on peace but Hormuz ship attacks persist"](https://www.bairdmaritime.com/amp/story/security/markets-are-betting-on-peace-but-hormuz-ship-attacks-persist) (fetched and read directly, dated 2026-11-11) | **Medium-High** for the October count - a single named think-tank's tally, and this cycle's own search surfaced two other October tallies for the same month (Gulf Times/Noam Raydan: 28; Seatrade Maritime: ~34), so "37" is one of at least three diverging counts, not a clean consensus figure - flagging the spread itself as a reliability caveat for any future cycle that wants to use an attack-count tally as regime corroboration. **High** for the CENTCOM action (primary military source, though read via only one citation chain this cycle). | Unconfirmed-as-a-precise-count (Washington Institute figure, given the 28/34/37 spread); Confirmed-via-one-primary-source (CENTCOM action) | No. Narrative/trend corroboration only - October being the worst month yet by every count, whichever exact number is right, is consistent with the EIA 3Q26 "partial recovery under active military enforcement" read (methodology.md section 81.6/81.8). No volume magnitude. |
| 2026-11-15 | **UKMTO** (relaying a report from Indian maritime authorities): one tanker came under attack while transiting the Arabian Gulf toward the Strait of Hormuz; crew safe; UKMTO did **not** attribute the cause to a mine. Separately and **unconfirmed**: Iran's **IRGC** claimed two tankers struck naval mines on an "unauthorized route," alleging one supertanker (2m+ barrels of crude) sank and a second caught fire; Iran's state agency **IRNA** separately claimed **five** tankers struck mines and caught fire over the preceding 48 hours (2 near Oman's coast, 3 in the central/eastern strait). No independent (non-Iranian-state) confirmation of any mine strike, sinking, or vessel count; the three sources (UKMTO/IRGC/IRNA) do not agree even on how many vessels were involved (1 vs. 2 vs. 5). | [Shafaq News, "Tanker hit in Gulf, Iran reports mine strikes"](https://shafaq.com/en/World/Tanker-hit-in-Gulf-Iran-reports-mine-strikes) (fetched and read directly, dated 2026-11-15) | **High** for the bare UKMTO incident report (quoted/relayed directly); **Low** for the mine-strike and sinking claims - single-party, belligerent-state-media origin, the same shape as the 2026-11-10/11 unconfirmed entry logged last cycle, now a second and larger-magnitude instance of the same unverified pattern. | Confirmed (UKMTO's bare incident report only); Unconfirmed (IRGC/IRNA mine/sinking claims) | No. Flagged for a future cycle to watch for independent confirmation of the claimed supertanker sinking specifically - if a non-Iranian source (flag state, insurer, classification society, or a second independent outlet) ever confirms a 2m+-barrel tanker sinking in the strait, that would be the single largest-magnitude incident of the conflict and would warrant an explicit regime-detector check ahead of the next EIA quarter. Not elevated past "lead" here. |
| - | Search this cycle surfaced multiple "Iran seizes tanker Talara" articles that read as current; independently checked and the event is dated **2026-11-14, but of 2025, not 2026** (a year-old story resurfacing in search results). | Multiple outlets (naharnet, CBS News, Washington Examiner, etc.), dates verified via each article's own byline/timestamp, not used as a 2026 signal | n/a | **Not used - dating error caught and discarded**, logged only as a caution for future cycles searching this exact phrase. | No. |

## Net reading from this cycle's signals (2026-11-18)

Every confirmed tier-2 signal this cycle continues to corroborate the
EIA-measured 3Q26 regime read (severe threat level, managed/escorted partial
recovery, not a return to calm) without contradicting it on the facts that
are actually confirmed. The one quantity that would be genuinely new if
confirmed - a claimed supertanker sinking on 2026-11-15 - rests entirely on
Iranian state media and is explicitly not elevated to "confirmed" here. The
October attack-count spread (28/34/37 across three trackers) is logged as a
standing reliability caveat, not resolved. No signal this cycle moves a
numeric input. See `methodology.md` section 83 for this cycle's tier-3
PortWatch validation finding, which is a materially different kind of result
(a measured divergence between two AIS-derived series, not a tier-2 news
signal) and is reported there, not here.
