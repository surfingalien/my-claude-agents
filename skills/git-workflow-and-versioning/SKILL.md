---
name: git-workflow-and-versioning
description: Manages git workflow and versioning. Use when establishing branch strategy, writing commits, managing releases, or coordinating parallel development.
---

# Git Workflow and Versioning

## Overview

Clean git history is a communication tool. Every commit should tell a story — what changed, and why it mattered.

## Trunk-Based Development

One shared branch. Short-lived feature branches. Continuous integration.

**Rules:**
- Feature branches live ≤ 2 days before merging
- Branch from `main`, merge back to `main`
- Every merge triggers CI — no broken main
- Use feature flags for incomplete work, not long branches

## Atomic Commits

One commit = one logical change.

```
<type>(<scope>): <short summary>

<optional body — explain WHY, not WHAT>
```

**Types:** `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`

```bash
feat(auth): add OAuth2 login with GitHub provider
fix(api): return 404 instead of 500 for missing tasks
refactor(db): extract query builders into repository layer
test(users): add coverage for duplicate email registration
```

## Git Worktrees for Parallel Work

```bash
# Create isolated worktree for a feature
git worktree add ../project-feature-x feature/x
cd ../project-feature-x

# List active worktrees
git worktree list

# Remove when done
git worktree remove ../project-feature-x
```

Use worktrees when agents work in parallel — each agent gets its own worktree.

## Save-Point Pattern

Before risky refactoring:

```bash
# Create a save point
git tag save-point-$(date +%Y%m%d-%H%M)

# Do the risky work...

# Restore if needed
git reset --hard save-point-20260516-1430

# Delete if it worked
git tag -d save-point-20260516-1430
```

## Change Summaries

```bash
# Changes since branching from main
git log main..HEAD --oneline

# Full diff stat
git diff main...HEAD --stat
```

Template:
```
## Changes in this branch

**Goal:** [one sentence]

**Commits:**
- feat(auth): add session refresh endpoint
- fix(auth): prevent token reuse after logout

**Files changed:** 8 (4 source, 3 tests, 1 migration)
**Tests:** All passing
**Breaking changes:** None
```

## Releases and Tags

```bash
# Annotated release tag
git tag -a v1.2.0 -m "Release v1.2.0: add team collaboration features"
git push origin v1.2.0
```

Semantic versioning: MAJOR (breaking) · MINOR (new feature) · PATCH (bug fix)

## Verification

- [ ] Branch name describes the work (not `fix`, but `fix/session-expiry-extension`)
- [ ] Each commit is atomic — one logical change per commit
- [ ] Commit messages follow conventional commit format
- [ ] No merge commits from main into feature branch (rebase instead)
- [ ] All tests pass before pushing
- [ ] No secrets, credentials, or `.env` files committed
