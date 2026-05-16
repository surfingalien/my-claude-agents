---
name: planning-and-task-breakdown
description: Breaks complex work into executable tasks. Use at the start of any feature or project to decompose requirements into ordered, parallelizable tasks with clear acceptance criteria.
---

# Planning and Task Breakdown

## Overview

Good planning prevents wasted work. Break complex requirements into tasks small enough to complete in a single focused session, sequenced by dependencies, and specific enough that "done" is unambiguous.

**The Goal:** A task list where every item has: a clear action, an acceptance criterion, and a known dependency chain.

## The Dependency Graph

Before writing tasks, map what depends on what:

```
Database schema
    ↓
Repository layer
    ↓           ↘
Service layer    Migration script
    ↓
API endpoints
    ↓           ↘
Frontend forms   API documentation
```

Tasks must follow the dependency graph. Work that can run in parallel should be identified explicitly.

## Vertical Slicing

Slice features vertically (through all layers), not horizontally (all of one layer):

```
HORIZONTAL (bad — nothing is usable until all done):
  Task 1: All database tables
  Task 2: All API endpoints
  Task 3: All UI components

VERTICAL (good — each task delivers usable functionality):
  Task 1: Create task with title only (DB + API + UI)
  Task 2: Add due date to tasks (DB migration + API + UI)
  Task 3: Add task assignee (DB + API + UI)
```

## Task Template

```markdown
## Task: [Short imperative title]

**Goal:** One sentence describing what this achieves.

**Acceptance criteria:**
- [ ] [Specific, testable condition 1]
- [ ] [Specific, testable condition 2]
- [ ] [Specific, testable condition 3]

**Dependencies:** [Task IDs this depends on, or "None"]
**Can run in parallel with:** [Task IDs that don't block this]
**Estimated size:** Small (< 2h) | Medium (2-4h) | Large (4-8h)
```

## Parallelization Guide

```
SEQUENTIAL (must run in order):
  Schema migration → Model definition → Repository → Service → API → UI

PARALLEL (can run simultaneously):
  Unit tests ↔ Integration tests
  Frontend component ↔ API endpoint (if interface agreed)
  Documentation ↔ Implementation
  Multiple independent features on separate branches
```

Agent parallelization: assign independent tracks to separate agents with separate git worktrees.

## Planning Session Structure

### Step 1: Understand the Goal

Write one sentence: "This feature lets [user] do [action] so that [outcome]."

If you can't write this sentence, interview the user before planning.

### Step 2: Identify the Layers

What does this feature touch?
- [ ] Database schema changes
- [ ] Backend service logic
- [ ] API endpoints
- [ ] Frontend components
- [ ] External service integrations
- [ ] Configuration/environment changes
- [ ] Tests
- [ ] Documentation/migration guide

### Step 3: Draw the Dependency Graph

Identify what must be built before other things can start.

### Step 4: Write Tasks

One task per unit of work. Tasks should be completable in 1-4 hours.

### Step 5: Sequence and Parallelize

Order tasks by dependency. Mark which tasks can run in parallel.

### Step 6: Identify Risks

For each large/complex task:
- What could go wrong?
- Is there a proof-of-concept needed first?
- What assumptions are we making?

## Example: Task Management Feature

```markdown
## Plan: Task Creation Feature

**Goal:** Let users create tasks with a title, due date, and optional assignee.

### Tasks (in order)

**[T1] Database: tasks table** (depends on: nothing)
- [ ] Create migration: id, title, due_date (nullable), assignee_id (nullable), created_at
- [ ] Run migration in dev
- [ ] Write rollback migration
- Size: Small

**[T2] Repository: TaskRepository** (depends on: T1)
- [ ] create(data): Task
- [ ] findById(id): Task | null
- [ ] findAll(filters): Task[]
- Size: Small

**[T3] Service: TaskService** (depends on: T2, parallel with T4)
- [ ] createTask(input): validates, calls repository, returns Task
- [ ] Unit tests for validation logic
- Size: Small

**[T4] API: POST /tasks endpoint** (depends on: T2, parallel with T3)
- [ ] Accept {title, dueDate?, assigneeId?}
- [ ] Return 201 + created task
- [ ] Return 422 for validation errors
- [ ] Integration test with test DB
- Size: Medium

**[T5] UI: Task creation form** (depends on: T4)
- [ ] Form with title (required), due date picker, assignee select
- [ ] Submit calls POST /tasks
- [ ] Success: show created task
- [ ] Error: show field errors
- Size: Medium
```

## Estimation Guidelines

| Size | Time | Characteristics |
|------|------|-----------------|
| Small | < 2h | Single file, clear scope, existing patterns |
| Medium | 2–4h | Multiple files, some unknowns, some new patterns |
| Large | 4–8h | Cross-cutting concerns, significant new code |
| Epic | > 8h | **Split further before starting** |

Tasks estimated as "Large" should be split before any work begins.

## Verification

- [ ] One-sentence goal statement written
- [ ] Dependency graph drawn (even informally)
- [ ] All tasks have acceptance criteria
- [ ] No task is estimated > 8 hours (split if so)
- [ ] Parallel work identified
- [ ] Risks and unknowns surfaced
- [ ] Tasks ordered by dependency
