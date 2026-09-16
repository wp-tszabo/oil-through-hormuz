---
description: Run one CEO cycle for the Hormuz Oil Tracker company (called by the scheduled cloud Routine, or manually to check/advance status).
---

Run one CEO cycle now. Invoke the `ceo` agent (via the Agent tool) with this
brief:

> Run a full cycle per your instructions in `.claude/agents/ceo.md` and
> `GOVERNANCE.md`. Check for critical issues first. Then check the current
> weekly plan's status in `company-memory/weekly-plans/` and act
> accordingly: propose, execute, or close out, exactly as your agent
> instructions describe. Enforce the copy-review and self-check checkpoints.
> Update company memory. End with a short status report: what happened,
> what's blocked or needs an owner decision, and what's next.

Do not skip the "check for critical issues first" step even if it seems
obviously fine — that check is what makes it safe to run this unattended on
a schedule.

After the CEO agent returns its report, relay that report back verbatim (or
lightly formatted) as your own final output — this is what the owner will
see when they check the Routine's run history, and what may reach them via
notification. Don't summarize it away.
