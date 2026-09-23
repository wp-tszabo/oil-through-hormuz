# oil-through-hormuz

This repository is the home base for an autonomous "AI company": a CEO agent
and three specialist subagents (Research, Build, Monetization) that run a
Strait of Hormuz oil-flow tracker site on a weekly cadence. As of
2026-09-23 the CEO has standing authority to publish site content and to
decide the estimation methodology on its own — the owner sets phase, spend
ceiling and the two standing goals (accuracy, visitor growth), and reviews
after the fact rather than approving each publish. See GOVERNANCE.md →
"Publishing authority", "Methodology authority" and "Standing goals".

**Read [GOVERNANCE.md](GOVERNANCE.md) first.** It's the binding constitution
for every agent operating in this repo, not optional background reading.

## Layout

- `GOVERNANCE.md` — roles, weekly cadence, spend ceiling, standing
  checkpoints, critical-issue categories, self-check rubric, rollout phases.
- `company-memory/` — shared persistent state: OKRs, backlog, decisions log,
  metrics, self-check log, critical-issues log, weekly plans. Source of
  truth across sessions — read it before acting, update it after.
- `.claude/agents/` — `ceo.md`, `research.md`, `build.md`, `monetization.md`
  subagent definitions.
- `.claude/commands/ceo-cycle.md` — the `/ceo-cycle` command a scheduled
  cloud Routine calls to run one cycle.
- `site/` — the actual website (static, deployed via GitHub Pages).

## For a human editing this repo directly

- `company-memory/weekly-plans/<date>.md` — this is where you approve or
  amend a plan (check the box under "Owner decision", change `Status` to
  `APPROVED`, add notes). This is the primary way you steer the company
  week to week.
- `company-memory/pending-copy/` (created on demand by the CEO) — historical
  record of drafts the CEO held for review before 2026-09-23. Since then the
  CEO publishes site content on its own authority via `ceo-published` PRs
  (see GOVERNANCE.md → "Publishing authority"), so this folder is no longer
  a waiting-for-you queue — check merged PRs and `decisions-log.md` instead
  to see what's shipped and why.
- Everything else in `company-memory/` is written by the agents; feel free
  to read it, but treat it as their working record rather than rewriting it
  out from under them mid-cycle.

## For an agent operating in this repo

Start every session by reading `GOVERNANCE.md` and the relevant
`company-memory/` files — do not rely on conversation memory, since cycles
run on a schedule in fresh sessions. See `.claude/agents/ceo.md` for the
full cycle procedure.
