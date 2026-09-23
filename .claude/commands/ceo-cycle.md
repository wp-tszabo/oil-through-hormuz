---
description: Run one CEO cycle for the Hormuz Oil Tracker company (called by the scheduled cloud Routine, or manually to check/advance status).
---

Run one CEO cycle now, **in this session directly — do not launch a `ceo`
subagent via the Agent tool.**

**Why, diagnosed 2026-09-23:** a subagent cannot itself launch further
subagents in this harness. If this top-level session delegates the whole
cycle to a `ceo` subagent, that subagent's own attempts to dispatch
`research`/`build`/`monetization` fail with `No such tool available: Agent.
Agent is disabled for this session, in subagents as well as here.` Thirteen
consecutive scheduled cycles hit exactly this, and the company never once
ran with real specialist delegation as a result. This session (the one
`/ceo-cycle` is invoked in) is the top-level session and *does* have the
Agent tool — so it must act as the CEO itself, not hand the role to a
subagent one level down.

So: read `.claude/agents/ceo.md` and `GOVERNANCE.md` yourself, right now, and
carry out a full cycle by following those instructions directly, exactly as
`ceo.md` describes:

> Check for critical issues first. Then check the current weekly plan's
> status in `company-memory/weekly-plans/` and act accordingly: propose,
> execute, or close out. Delegate concrete work items to the `research`,
> `build`, and `monetization` subagents via the Agent tool where `ceo.md`
> calls for it — you can do this now, because you are the top-level session.
> Enforce the publishing-authority and self-check checkpoints in
> `ceo.md`/`GOVERNANCE.md`. Update company memory. End with a short status
> report: what happened, what's blocked or needs an owner decision, and
> what's next.

Do not skip the "check for critical issues first" step even if it seems
obviously fine — that check is what makes it safe to run this unattended on
a schedule.

If dispatching a `research`/`build`/`monetization` subagent still fails from
here, that means the diagnosis above was incomplete (not just "subagents
can't nest") — capture the exact error text and say so plainly in the
report, rather than re-describing it as "Agent tool disabled" without
evidence, as earlier cycles did.

End with a short, plain-language status report — what happened, what's
blocked or needs an owner decision, and what's next — since this is what the
owner will see when they check the Routine's run history, and what may reach
them via notification. Don't summarize it away.
