# Pending copy — one sentence on the homepage, for the suppressed state

**Status**: HELD, awaiting owner review. Nothing changed on the live site.
**Raised**: 2026-09-19 (8th cycle), immediately after PR #8 merged.
**Wanted by**: 2026-09-30 — that is when it starts being visible.
**Size**: one sentence. It is here because it is user-facing prose, not because
it is large.

## The problem

PR #8 (now merged, on the owner's approval of the one-quarter horizon) makes the
homepage suppress the headline number once the day being estimated is more than
about one quarter past the anchor. From roughly 1 October 2026 the top of the
page will read:

> **No current estimate — awaiting the next published quarter**
> —
> million barrels per day
> Our anchor covers 2Q26 and our method is only tested one quarter ahead. We are
> now N days past that, so we have stopped publishing a daily number rather than
> extrapolate beyond what we have tested.

The automation only ever writes inside the generated block. The very next
sentence on the page is fixed prose, and it currently reads:

> The range is this wide because the strait is anything but steady right now
> — see how we get to a number.

So a reader arriving in October is told there is no number and no range, and
then immediately told why "the range is this wide". It is not false — there is
no claim about the data's authority here — it is just incoherent, and it reads
like a page that has broken rather than a page that is being careful. The whole
point of the suppression is to look deliberate.

## Proposed fix

Make that one sentence conditional on the same state as the block above it, so
it is written by the refresh script into its own small generated region:

- **Normal state (unchanged, word for word):**
  "The range is this wide because the strait is anything but steady right now
  — see how we get to a number."

- **Suppressed state (new):**
  "This is deliberate, not a fault — see how we get to a number."

Nothing else on the page changes. No figure, no band, no methodology text, no
`sources.html` copy (the "When we stop answering" section there already explains
the behaviour in full, and the owner has approved it).

## What happens if you do nothing

The page still tells the truth and the suppression still works; it just reads
badly for the weeks between the horizon expiring and EIA publishing 3Q26. The
CEO will not change it without approval either way.

## Owner decision

- [ ] Approve the conditional sentence as drafted
- [ ] Approve with different wording (write it here)
- [ ] Leave it alone — the mismatch is acceptable
