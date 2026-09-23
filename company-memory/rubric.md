# Self-Check Rubric

The CEO runs this checklist against any work item before it's approved for
publishing (or immediately after, if that's unavoidable — see
[GOVERNANCE.md](../GOVERNANCE.md)), and logs the result to
`self-check-log.md`. Since 2026-09-23 the owner no longer pre-approves copy,
so this rubric is the main pre-publish gate and is never skipped. Every item
must be `PASS` to publish. Any `FAIL` blocks
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

- [ ] The change serves the OKRs, in particular the two standing goals
      (reasonable accuracy, visitor growth). No scope creep into work the
      owner has not authorised (e.g. monetization before Phase 2 approval).
- [ ] The site does not misrepresent the data's authority (e.g. doesn't
      imply an official government feed when it's a derived/aggregated
      estimate).
- [ ] **Headline test (added 2026-09-23 with the traffic goal):** every
      title, headline, meta description, share card and teaser passes this
      on its own. A reader who sees *only that line* would not come away
      believing something the band and the methodology page do not support.
      The estimate is called an estimate and its range is shown wherever the
      point is. There is no sensational or alarmist framing, no implied
      real-time/official/tracking data, and no unevidenced superlatives
      (GOVERNANCE.md → "Standing goals"). A failure here is also
      critical-issue category 4.
- [ ] Nothing published exceeds the approved spend ceiling to produce.
- [ ] Published under GOVERNANCE.md → "Publishing authority": through a PR
      (not a direct push to `site/`), with a plain-language what-and-why in
      the PR body, and no unresolved category-3/4 doubt. *(Until 2026-09-23
      this item was "Copy has gone through the standing owner-review
      checkpoint". The owner retired that checkpoint.)*

## Logging format

Each row in `self-check-log.md`:

`date | item checked | accuracy | no-copied-text | on-purpose | overall | notes/evidence`
