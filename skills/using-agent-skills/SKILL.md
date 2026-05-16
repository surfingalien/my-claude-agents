---name: using-agent-skills
description: Meta-skill for discovering and applying other skills. Use this skill to understand how to find, load, and combine skills effectively. Use when starting a new session, when unsure which skill applies, or when coordinating multiple skills.---

# Using Agent Skills Agent

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

# Using Agent Skills Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# Using Agent Skills

## Overview

This meta-skill explains how to navigate and use the skill library. Skills are modular, composable tools — each is self-contained with documentation, examples, and verification checklists. Knowing how to find the right skill and apply it correctly multiplies the effectiveness of every session.

## Skill Discovery Tree

```
What do I need to do?
│
├── Plan / Design
│   ├── Requirements unclear?       → interview-me
│   ├── Need a spec first?          → spec-driven-development
│   ├── Break into tasks?           → planning-and-task-breakdown
│   └── Refine an idea?             → idea-refine
│
├── Build / Implement
│   ├── Building incrementally?     → incremental-implementation
│   ├── Writing tests first?        → test-driven-development
│   ├── Designing an API?           → api-and-interface-design
│   ├── Building UI?                → frontend-ui-engineering
│   └── Using a library/API?        → source-driven-development
│
├── Review / Improve
│   ├── Reviewing code quality?     → code-review-and-quality
│   ├── Simplifying complex code?   → code-simplification
│   ├── Challenging assumptions?    → doubt-driven-development
│   └── Updating old patterns?      → deprecation-and-migration
│
├── Ship / Deploy
│   ├── Setting up CI/CD?           → ci-cd-and-automation
│   ├── Ready to launch?            → shipping-and-launch
│   ├── Investigating performance?  → performance-optimization
│   └── Hardening security?        → security-and-hardening
│
├── Debug / Fix
│   ├── Something is broken?        → debugging-and-error-recovery
│   ├── UI issue in browser?        → browser-testing-with-devtools
│   └── Performance regression?     → performance-optimization
│
└── Maintain / Document
    ├── Writing docs or ADRs?        → documentation-and-adrs
    ├── Managing context/sessions?   → context-engineering
    ├── Git workflow issues?         → git-workflow-and-versioning
    └── Web performance auditing?    → web-quality
```

## Core Operating Behaviors

### 1. Read Before Acting

Before using any skill, read its SKILL.md:
- Understand when to use and when NOT to use
- Note the verification checklist
- Identify the key principles and patterns

### 2. Start Simple

Default to the simplest skill that applies. Don't stack skills unnecessarily.

```
TASK: Fix a bug
WRONG: spec-driven-development → planning-and-task-breakdown → tdd
RIGHT: test-driven-development (Prove-It pattern is enough)
```

### 3. Compose Thoughtfully

Skills compose well when they address different concerns:

```
GOOD COMPOSITION:
  spec-driven-development (define what) +
  incremental-implementation (build how) +
  test-driven-development (verify correctness)

REDUNDANT COMPOSITION:
  code-review-and-quality + doubt-driven-development
  (both challenge the same thing — pick one per session)
```

### 4. Check Verification Checklists

Every skill ends with a verification checklist. Use it before declaring work done:

```
"Does this match what the skill says success looks like?"
```

## Full Lifecycle Sequence

For a complete feature from idea to production:

```
1. interview-me           → Understand what's actually needed
2. spec-driven-development → Write the specification
3. planning-and-task-breakdown → Break into ordered tasks
4. source-driven-development → Fetch authoritative docs
5. incremental-implementation + test-driven-development → Build
6. code-review-and-quality → Review the implementation
7. security-and-hardening → Harden the boundaries
8. performance-optimization → Verify performance
9. shipping-and-launch    → Ship safely
```

Not every feature needs all nine steps. A small bug fix needs step 5 (Prove-It pattern) and maybe step 6.

## Quick Reference Table

| Skill | When |
|-------|------|
| api-and-interface-design | Designing a new API or module boundary |
| browser-testing-with-devtools | Debugging UI or verifying browser behavior |
| ci-cd-and-automation | Setting up or fixing build/deploy pipelines |
| code-review-and-quality | Reviewing any code before merge |
| code-simplification | Refactoring for clarity after feature works |
| context-engineering | Starting a session, managing agent context |
| debugging-and-error-recovery | Something is broken and you need to find why |
| deprecation-and-migration | Replacing old patterns with new ones |
| documentation-and-adrs | Writing docs, ADRs, or decision records |
| doubt-driven-development | Adversarially reviewing your own reasoning |
| frontend-ui-engineering | Building or reviewing UI components |
| git-workflow-and-versioning | Commits, branches, releases, parallel work |
| idea-refine | Turning a vague idea into a concrete proposal |
| incremental-implementation | Building in safe, deployable slices |
| interview-me | Eliciting requirements before building |
| performance-optimization | Diagnosing and fixing slow code or UIs |
| planning-and-task-breakdown | Decomposing complex work into tasks |
| security-and-hardening | Hardening against vulnerabilities |
| shipping-and-launch | Safely deploying to production |
| source-driven-development | Verifying API behavior from official docs |
| spec-driven-development | Writing specs before coding |
| test-driven-development | Test-first development and bug fixes |
| web-quality | Auditing Core Web Vitals and accessibility |

## Failure Modes to Avoid

| Failure | Description | Correction |
|---------|-------------|------------|
| Skill overload | Using 5 skills for a 30-minute task | Match skill depth to task complexity |
| Checklist theater | Running checklists without thinking | Each item should prompt genuine verification |
| Wrong skill | Using code-review for a bug fix | Use the discovery tree to find the right fit |
| Skipping skills | Coding without spec when requirements are ambiguous | When in doubt, interview-me first |

## Verification

- [ ] Correct skill identified for the task
- [ ] SKILL.md read before applying the skill
- [ ] Verification checklist completed at the end
- [ ] Skills composed only when addressing different concerns
- [ ] Complexity matched to task (not over-engineered)