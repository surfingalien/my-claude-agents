---
name: timeline-report
description: >-
  Generate a "Journey Into [Project]" narrative report analyzing a project's
  full development history from claude-mem's timeline. TRIGGER when: user asks
  for a timeline report, project history analysis, development journey,
  full project report, or "what's the story of this project?".
  Requires claude-mem installed with session history.
origin: claude-mem
owner: surfingalien
---

# timeline-report

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Generate a comprehensive narrative report of a project's complete development history using claude-mem's persistent memory timeline. Tell the story of how the project was built — decisions made, problems solved, patterns evolved.

## When to Use

- "Write a timeline report for [project]"
- "Journey into [project name]"
- "What's the story of this project?"
- "Analyze my project history"
- "Full development report"
- "Summarize the entire development history"
- Retrospectives and post-mortems
- Onboarding new collaborators to a project's history

**Requires:** claude-mem installed, multiple sessions of observations recorded for the project.

## Workflow

### Step 1: Fetch the Full Timeline

```bash
# Get all observations for the project
claude-mem timeline --project <project-path> --format json > timeline.json

# Check the span
cat timeline.json | jq '[.[] | .timestamp] | min, max'

# Count observations
cat timeline.json | jq 'length'
```

### Step 2: Identify Major Phases

Scan the timeline and cluster observations into **narrative phases** — not arbitrary time windows, but meaningful development stages:

Common phases for software projects:
- **Foundation** — initial setup, architecture decisions, tooling
- **Core Build** — primary feature implementation
- **Integration** — connecting services, APIs, external dependencies
- **Stabilization** — bug fixes, refactors, test coverage
- **Evolution** — new features, direction changes, scale-up work

For FinSurfing specifically, look for:
- Initial Express/React setup
- Anthropic API integration point
- PostgreSQL schema evolution
- Railway deployment milestones
- AI-Trader integration phases
- my-claude-agents skill development sessions

### Step 3: Extract Key Moments

For each phase, identify:
- **Pivots**: direction changes and why they happened
- **Breakthroughs**: when something hard finally worked
- **Decisions**: architectural choices with lasting impact
- **Lessons**: patterns that emerged from struggle

### Step 4: Write the Narrative

Write in chronological order, phase by phase. Style: analytical narrative — like a technical post-mortem mixed with a project retrospective.

```markdown
# Journey Into [Project Name]
*A development history — [date range]*

## Overview

[3–4 sentence summary: what was built, how long it took, what makes this project notable]

---

## Phase 1: [Phase Name]
*[Date range] — [N observations]*

[2–4 paragraphs narrating what happened, key decisions, why things were done the way they were]

**Key decisions:**
- [Decision]: [Rationale]

**Patterns established:**
- [Pattern that persisted throughout the project]

---

## Phase 2: [Phase Name]
...

---

## Patterns & Themes

[Cross-cutting observations across all phases]
- What recurred?
- What was consistently hard?
- What accelerated work?

## Technical Debt Accumulated

[Honest accounting of shortcuts taken and why]

## What Worked

[Specific practices, tools, or decisions that paid off]

## What Would Be Done Differently

[Specific changes in hindsight — not generic advice]

---

*Generated from [N] observations across [M] sessions*
*Report date: [date]*
```

### Step 5: Save the Report

```bash
# Save to docs/ for persistent reference
mkdir -p docs/history
claude-mem timeline-report --project <path> --output docs/history/journey-$(date +%Y-%m).md
```

## Output Variants

### Short (executive summary)

For a 1-page version:

```
claude-mem timeline --project <path> --format summary
```

### By Component

Narrow to a specific subsystem:

```
claude-mem timeline --project <path> --filter "anthropic OR claude-api"
```

### Comparative (before/after a decision)

```
claude-mem timeline --project <path> --until "2026-03-01" # before
claude-mem timeline --project <path> --since "2026-03-01" # after
```

## FinSurfing Context

Suggested timeline reports to generate:

- **Full FinSurfing journey** — the whole arc from initial setup to current state
- **Anthropic integration history** — how the AI layer evolved
- **Trading intelligence roadmap history** — decisions made about AI-Trader integration
- **my-claude-agents development story** — the meta-history of building the agent repo itself

These reports serve as onboarding docs, retrospective inputs, and foundation for future planning.

## Related Skills

- `weekly-digests` — Same concept but split by week (better for long projects)
- `mem-search` — Quick targeted queries without a full narrative (faster, less comprehensive)
- `knowledge-agent` — Topic-focused brains (more interactive, less narrative)
