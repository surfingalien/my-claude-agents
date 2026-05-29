---
name: make-plan
description: >-
  Turn a feature request, task, or multi-session objective into a phased,
  LLM-friendly implementation plan. Each phase is independently executable by
  a fresh agent with zero re-explanation. TRIGGER when: user asks to plan,
  blueprint, or roadmap anything non-trivial. Pair with do to execute.
  DO NOT TRIGGER when the task fits in a single PR or fewer than 3 tool calls.
origin: claude-mem
owner: surfingalien
---

# make-plan

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

You are an **ORCHESTRATOR**. Create an LLM-friendly plan in phases that can be executed consecutively in new chat contexts. Do not implement — plan with precision and hand off to `do`.

## When to Use

- Planning a feature, refactor, or migration before executing
- Breaking complex multi-session work into independently deliverable chunks
- Any task where context loss between sessions would cause rework or re-discovery
- Pre-flight before running `do`

**Do not use** for tasks completable in a single PR, fewer than 3 tool calls, or when user says "just do it."

## Delegation Model

Use subagents for **fact gathering** (docs, examples, API signatures, grep results). Keep **synthesis and plan authoring** with the orchestrator (phase boundaries, task framing, final wording).

If a subagent report is incomplete or lacks evidence, re-check with targeted reads/greps before finalizing.

### Subagent Reporting Contract (MANDATORY)

Each subagent response must include:
1. Sources consulted (files/URLs) and what was read
2. Concrete findings (exact API names/signatures; exact file paths/locations)
3. Copy-ready snippet locations (example files/sections to copy)
4. "Confidence" note + known gaps (what might still be missing)

## Planning Workflow

### Phase 1: Reconnaissance

Before writing a single plan step, deploy a subagent to:

```
1. Read project structure — CLAUDE.md, README, package.json / pyproject.toml
2. Identify existing patterns — file naming, test strategy, API conventions
3. Grep for related code — functions, schemas, routes relevant to the objective
4. Check for prior plans — plans/, docs/, CHANGELOG for related history
```

Return: exact file paths, function signatures, existing patterns to follow.

### Phase 2: Design

Break the objective into **one-PR-sized phases** (3–12 typical). For each phase:

- Assign dependency edges (what must complete before this starts)
- Detect parallel/serial ordering
- Assign model tier: Opus for architecture decisions, Sonnet for implementation, Haiku for boilerplate
- Define rollback strategy per phase

### Phase 3: Draft

Write the plan to `plans/NN-<slug>.md`. Every phase must include:

```markdown
### Phase N: [Name]

**Goal:** One sentence
**Model:** sonnet / opus / haiku
**Depends on:** Phase X, Phase Y
**Parallel:** Yes / No

**Steps:**
1. **[Action]** (File: `path/to/file.ts`)
   - Action: Specific thing to do
   - Why: Reason
   - Risk: Low / Medium / High

**Verification:**
- Command to verify this phase is complete
- Expected output

**Exit Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
```

### Phase 4: Adversarial Review

Before finalizing, run a review subagent (Opus) against:

**Anti-pattern checklist:**
- [ ] No phase requires all prior phases to run for anything to work
- [ ] No step has "update tests" as its only test strategy
- [ ] No step hardcodes values that will drift
- [ ] No phase mixes implementation + schema migration in one PR
- [ ] No step leaves the repo in a broken state mid-phase

Fix all critical findings. Warn on non-critical.

### Phase 5: Register

Save to `plans/`, update any memory index or CLAUDE.md plan list, present phase count + parallelism summary.

## Plan Format

```markdown
# Plan: [Objective]

## Overview
[2-3 sentences. What ships, what doesn't, why this sequence.]

## Context
- **Repo:** [name]
- **Stack:** [language, framework, DB]
- **Existing patterns:** [key conventions to follow]
- **Prior related work:** [links to existing plans or PRs if any]

## Phases

### Phase 1: [Name]
...

## Parallelism Map
Phase 1 → Phase 2 → Phase 3
                 ↘ Phase 4 (parallel with Phase 3)

## Risk Register
| Phase | Risk | Mitigation |
|-------|------|------------|
| 2 | Schema migration irreversible | Test in staging first |

## Success Criteria
- [ ] All phases merged
- [ ] All tests green
- [ ] Feature verified in production
```

## FinSurfing Context

When planning work for FinSurfing (React + Vite + Express + PostgreSQL + Anthropic API on Railway):

- Always check `src/` structure before proposing file locations
- Prefer extending existing Express routes over new files when adding endpoints
- Anthropic API calls go through the server — never expose keys client-side
- Railway env vars: confirm names match before referencing in plans
- For AI-Trader integration phases: sequence data pipeline before UI

## Best Practices

1. **Be specific** — Exact file paths, function names, schema column names
2. **One concern per phase** — Never mix DB migration + feature implementation
3. **Enable incremental delivery** — Each phase must be independently mergeable
4. **Name your risks** — Explicit beats optimistic
5. **Measure done** — Every phase has verification commands, not just vibes
6. **Think AI-first** — Route model tiers by complexity, not habit

## Related Skills

- `do` — Execute a plan produced by make-plan
- `blueprint` — Alternative planner for multi-PR construction plans
- `babysit` — Monitor PR through CI and review after executing a phase
- `agents-orchestrator` — Full pipeline orchestration
