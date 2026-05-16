---name: documentation-and-adrs
description: Records decisions and documentation. Use when making architectural decisions, changing public APIs, shipping features, or when you need to record context that future engineers and agents will need.---

# Documentation And Adrs Agent

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

# Documentation And Adrs Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# Documentation and ADRs

## Overview

Document decisions, not just code. The most valuable documentation captures the *why* — the context, constraints, and trade-offs that led to a decision. Code shows *what* was built; documentation explains *why it was built this way* and *what alternatives were considered*.

## Architecture Decision Records (ADRs)

### When to Write an ADR

- Choosing a framework, library, or major dependency
- Designing a data model or database schema
- Selecting an authentication strategy
- Choosing between REST, GraphQL, or tRPC
- Any decision that would be expensive to reverse

### ADR Template

Store in `docs/decisions/` with sequential numbering:

```markdown
# ADR-001: Use PostgreSQL for primary database

## Status
Accepted

## Date
2025-01-15

## Context
We need a primary database. Requirements: relational data model, ACID transactions,
full-text search, managed hosting.

## Decision
Use PostgreSQL with Prisma ORM.

## Alternatives Considered

### MongoDB
- Pros: Flexible schema
- Cons: Our data is relational; rejected

### SQLite
- Cons: Limited concurrent writes, no managed hosting; rejected

## Consequences
- Type-safe DB access via Prisma
- Can use PostgreSQL's built-in full-text search
```

### ADR Lifecycle

```
PROPOSED → ACCEPTED → (SUPERSEDED or DEPRECATED)
```

Don't delete old ADRs. When a decision changes, write a new ADR that supersedes the old one.

## Inline Documentation

### When to Comment

Comment the *why*, not the *what*:

```typescript
// BAD: Restates the code
// Increment counter by 1
counter += 1;

// GOOD: Explains non-obvious intent
// Rate limit uses a sliding window — reset at window boundary, not fixed schedule,
// to prevent burst attacks at window edges
if (now - windowStart > WINDOW_SIZE_MS) { counter = 0; windowStart = now; }
```

### When NOT to Comment

- Self-explanatory code
- TODO comments for things you should just do now
- Commented-out code (delete it — git has history)

## README Structure

```markdown
# Project Name
One-paragraph description.

## Quick Start
1. Clone, install, copy .env.example, run dev server

## Commands
| Command | Description |
| `npm run dev` | Start development server |
| `npm test` | Run tests |

## Architecture
Brief overview. Link to ADRs.
```

## Documentation for Agents

- **CLAUDE.md / rules files** — Document project conventions so agents follow them
- **Spec files** — Keep specs updated so agents build the right thing
- **ADRs** — Help agents understand why past decisions were made
- **Inline gotchas** — Prevent agents from falling into known traps

## Verification

- [ ] ADRs exist for all significant architectural decisions
- [ ] README covers quick start, commands, and architecture overview
- [ ] API functions have parameter and return type documentation
- [ ] Known gotchas are documented inline
- [ ] No commented-out code remains
- [ ] Rules files (CLAUDE.md etc.) are current and accurate