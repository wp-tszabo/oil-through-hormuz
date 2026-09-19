# Pending copy — `sources.html`, "What is in it today" (GPCI addition)

**Status: HELD. NOT PUBLISHED. CONDITIONAL — do not merge unless critical
issue #9 is resolved in favour of option B or C.**

Drafted 2026-09-19 by the CEO agent. Goes through the standing owner copy
checkpoint like everything else.

---

## Why this draft exists, and why it is deliberately not live

This cycle cleared a new input — **EIA Short-Term Energy Outlook, Table 3d,
monthly crude oil production** — and built GPCI (the Gulf Producer Crude Index)
and regime detector v3 on top of it. See `methodology.md` §13.

**That input is not in the published model today.** The live headline is still
4.9 with a 1.5–6.9 band, produced by persistence on the quarterly EIA Hormuz
anchor, exactly as before.

So `sources.html` must **not** mention it yet. That page makes a specific
promise — it says what is in the model *today* — and the CEO's standing mandate
says in terms that the site must "describe what is in the model today, never
what is aspired to", and that overstating input diversity is a category-4
critical issue. Listing a cleared-but-unused input under "What is in it today"
would do precisely that. A source we have analysed is not a source that is
feeding the number.

This draft is therefore held against a decision, not queued for publication.
**If the owner picks option A on issue #9 (change nothing), this draft should be
discarded, not banked.**

---

## Replacement text for the "What is in it today" section

> ### What is in it today
>
> Two cleared datasets, both from the **U.S. Energy Information
> Administration**, both works of the U.S. federal government and in the public
> domain.
>
> The **anchor** is EIA's [Global Energy Security
> Data](https://www.eia.gov/outlooks/steo/report/energysecurity/article.php),
> Table 4, released **12 August 2026**, covering quarters through April–June
> 2026. It is the only cleared series that measures the strait itself. EIA's
> volumes are based on Vortexa tanker tracking data with additional EIA
> analysis; we republish EIA's published analysis and do not hold or license
> Vortexa's underlying data.
>
> The **pacing signal** is EIA's [Short-Term Energy
> Outlook](https://www.eia.gov/outlooks/steo/), Table 3d, which publishes crude
> oil production by country every month — observed through **August 2026**, two
> months fresher than the anchor. We add up the Gulf producers that depend on
> the strait and watch how that total moves. It does not measure the strait, and
> we do not treat it as if it did: producers can lift oil into storage, into
> their own refineries, or into pipelines that bypass Hormuz entirely. What it
> gives us is timing — whether the producer side is falling, bottoming or
> recovering — weeks earlier than the quarterly record can tell us.

## Additional paragraph for "What is deliberately not in it"

> We also checked two maritime advisory services this month — the UK Maritime
> Trade Operations and the US Maritime Administration — and could not retrieve
> their terms at all. An unread licence is not a permissive one, so neither is
> used.

---

## Notes for the reviewer

- **"Two cleared datasets" is the ceiling of what may be claimed**, and only if
  option B or C is chosen. It must not drift into "multiple sources", "a range
  of feeds" or anything implying breadth we do not have.
- The second dataset is described as a **pacing signal**, not as a measurement
  of the strait, and the bypass caveat is in the visible copy rather than
  buried. Both are deliberate: the single most likely way this page becomes
  dishonest is by letting a production series read as a flow series.
- The Vortexa provenance caveat and the EIA AIS-reliability caveat stay exactly
  as they are.
- If PR #8 also merges, its Table 2 "control group" wording from
  `pending-copy/2026-09-18-sources-v2.md` needs reconciling with this — the two
  drafts touch the same section and have not been merged into one text.
- Nothing here changes `index.html`. If the owner picks option B or C on issue
  #9, the headline figure and/or band change, and that is a separate copy
  change requiring its own draft and its own rubric run.
