# Pending copy — say which time zone the date is in

**Status**: PUBLISHED 2026-09-23 by the CEO under its publishing authority (PR #12, `16def17`). *(Previously: HELD, awaiting owner review.)*
**Raised**: 2026-09-20 (9th cycle), from the opening critical-issue check.
**Urgency**: low. Not dated, not a correctness failure. **Batch it with
`2026-09-19-suppressed-state-note.md`** — they are both one-liners and there is
no reason to spend two separate decisions on them.
**Size**: one word on the page, one clause in the methodology paragraph.

## What the check found

At 02:20 UTC on Sunday 20 September the live page read:

> Our model's estimate for **Friday 18 September 2026**

Two calendar days back, where the design is one. The figure itself was correct
and the site was healthy (HTTP 200, valid TLS, bytes identical to `main`, source
re-fetched and unchanged).

This is **not** the frozen-date defect from 18 and 19 September. The refresh job
computes `for_date = today(UTC) − 1` and runs at **05:10 UTC**, so between 00:00
and 05:10 UTC every day the page carries the day *before* yesterday, then
corrects itself. It is a bounded, self-correcting window rather than a page
nobody is updating. Full reasoning is in `critical-issues-log.md` under
2026-09-20, including the trigger that would make it a real interrupt.

## Why it is still worth one sentence of copy

Two reasons, and the second is the real one.

1. The workflow's own comment says 05:10 UTC is *"after midnight everywhere that
   matters"*. For the Strait of Hormuz that is backwards. The Gulf is UTC+3/+4,
   so local midnight there is 20:00–21:00 UTC the previous day — a Gulf reader
   sees a two-days-back date for roughly **nine hours every night**. The place
   the story is happening is the place the date is most often wrong.

2. The page makes an explicit promise about this date. The methodology paragraph
   says our model *"carries it forward to the day you are reading"*. For a
   reader in Dubai at 04:00 local, that sentence is false — and it is the same
   sentence that made the September frozen-date defect a truth problem rather
   than a cosmetic one.

**There is no cron time that is right for every reader.** Moving the job earlier
fixes the Gulf and breaks the Americas, where the page would then name a day
that has not finished locally. A single global date label is inherently
ambiguous; the honest fix is to say which clock we are using.

## Proposed fix

**Change 1 — the estimate label** (written by the refresh script, inside the
generated block):

- Now: `Our model's estimate for Friday 18 September 2026`
- Proposed: `Our model's estimate for Friday 18 September 2026 (UTC)`

**Change 2 — one clause in the "How we get to a number" paragraph** (fixed
prose, currently reads "...calibrates against the quarterly record, and carries
it forward to the day you are reading"):

- Proposed: "...calibrates against the quarterly record, and carries it forward
  to the most recent completed day, UTC."

Nothing else changes. No figure, no band, no chart, no `sources.html` text.

## What is not in this draft, and needs a separate yes/no

Whether to move the refresh job from 05:10 UTC to shortly after 00:00 UTC. That
would shrink the stale window from ~5 hours to minutes for UTC and eastward
readers, at the cost of naming a date that is still in progress for readers in
the Americas. It is a code change to already-approved automation rather than
copy, so it is sitting in `backlog.md` for decision alongside next week's plan —
**the CEO recommends changing the copy and leaving the schedule alone**, because
the copy fix is honest for every reader and the schedule change is only ever a
trade between two groups of them.

## What happens if you do nothing

The page keeps telling the truth for most of each day and is ambiguously one day
behind for Gulf readers overnight. No number is affected. The CEO will not
change either the copy or the schedule without approval.

## Owner decision

- [ ] Approve both changes as drafted
- [ ] Approve change 1 only (the `(UTC)` label)
- [ ] Approve with different wording (write it here)
- [ ] Leave it alone
