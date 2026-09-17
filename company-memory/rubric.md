# Self-Check Rubric

The CEO runs this checklist against any work item before it's approved for
publishing (or immediately after, if that's unavoidable — see
[GOVERNANCE.md](../GOVERNANCE.md)), and logs the result to
`self-check-log.md`. Every item must be `PASS` to publish. Any `FAIL` blocks
publishing and, if the content is already live, triggers a rollback and a
critical-issue log entry.

## 1. Accuracy

- [ ] Every number displayed traces to a specific, cited source and
      retrieval timestamp.
- [ ] The displayed data matches the source at the time of the check (spot
      re-fetch, don't trust cache).
- [ ] Units, dates, and time zones are unambiguous and correct.
- [ ] Any estimate, derived figure, or extrapolation is clearly labeled as
      such (not presented as a direct measurement).
- [ ] Known data gaps or staleness are surfaced to the reader, not hidden.
- [ ] If the figure comes from the daily best-guess model (see
      `research.md`), its methodology is published and linked, its inputs
      are all independently cleared sources (never an uncleared source used
      "just for calibration"), and it carries a visible uncertainty range —
      not a falsely precise single number.

## 2. No copied text

- [ ] All prose (headlines, descriptions, methodology, about page) is
      original, not lifted from a source site or report.
- [ ] Any quoted material is in quotation marks with clear attribution.
- [ ] Charts/visuals are original renderings of the underlying data, not
      screenshots or re-hosted images from another site.

## 3. On-purpose

- [ ] The change actually serves the current week's approved plan/OKRs —
      no scope creep into unapproved work (e.g. monetization before Phase 2
      approval).
- [ ] The site does not misrepresent the data's authority (e.g. doesn't
      imply an official government feed when it's a derived/aggregated
      estimate).
- [ ] Nothing published exceeds the approved spend ceiling to produce.
- [ ] Copy has gone through the standing owner-review checkpoint before
      going live (this is never skipped, in any phase).

## Logging format

Each row in `self-check-log.md`:

`date | item checked | accuracy | no-copied-text | on-purpose | overall | notes/evidence`
