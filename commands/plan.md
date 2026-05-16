---
name: plan
description: Break the current task into an ordered, dependency-aware task list before writing code.
---

Apply the planning-and-task-breakdown skill to create an execution plan.

Steps:

1. **State the goal** — Write one sentence: "This feature lets [user] do [action] so that [outcome]."
2. **Identify layers** — What does this touch? (DB, API, frontend, external services, tests, docs)
3. **Draw dependencies** — What must be built before other things can start?
4. **Write tasks** — Each task needs:
   - Short imperative title
   - Acceptance criteria (testable conditions)
   - Dependencies (task IDs or "none")
   - Size estimate (Small <2h | Medium 2-4h | Large 4-8h)
5. **Identify parallelism** — Which tasks can run simultaneously?
6. **Flag risks** — What's uncertain? What needs a spike first?

**Do not write any code yet.** The plan is the deliverable.

Reference: `skills/planning-and-task-breakdown/SKILL.md`
