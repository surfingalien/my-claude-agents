---
name: babysit
description: >-
  Monitor a pull request through CI and review cycles until it is merge-ready.
  Polls checks, reads review comments, fixes real issues, resolves threads.
  TRIGGER when: user says "babysit this PR", "watch it until it merges",
  "monitor the PR", or "keep checking". Do not stop after one pass.
origin: claude-mem
owner: surfingalien
---

# babysit

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Stay with the PR until it is **actually clean**. One pass is not babysitting — it's a glance. Do not stop after checking once if comments or review threads remain.

## When to Use

- After executing a plan with `do` and a PR is open
- When CI is flaky and needs persistent monitoring
- When waiting for review comments and ready to fix-and-recheck
- When a PR has accumulated review threads that need systematic resolution

## Workflow

### Step 1: Identify the PR

```bash
gh pr list --state open
gh pr view <number> --json number,title,headRefName,baseRefName,mergeable,reviewDecision,statusCheckRollup
```

Confirm: not draft, has a base branch, is in a reviewable state.

### Step 2: Snapshot Current State

Capture the full picture before doing anything:

```bash
# CI check status
gh pr checks <number>

# Review decision
gh pr view <number> --json reviewDecision,reviews

# All comments and threads
gh pr view <number> --json comments,reviewThreads
```

Classify each item:
- **Actionable**: fix required (code, test, doc)
- **Bot summary**: context only, verify before acting
- **Pending CI**: wait and re-check
- **Stale thread**: resolvable if code already addresses it

### Step 3: Watch Pending CI

If checks are pending/running:
- Poll at 30–60 second intervals (or as user specifies)
- Re-snapshot on first state change
- Do not make code changes while CI is still running

```bash
# Watch loop
while gh pr checks <number> | grep -q "pending\|in_progress"; do
  sleep 45
  gh pr checks <number>
done
```

### Step 4: Fix Actionable Items

For each actionable comment or failing check:

1. Read the actual code being discussed (do not trust the comment summary alone)
2. Determine if the concern is real or already addressed
3. Fix in a focused commit — one fix per commit, clear message
4. Run relevant tests/builds before pushing
5. Push and return to Step 2

```bash
# After fixes
git add -p   # stage selectively
git commit -m "fix: <specific thing from review>"
git push origin <branch>
```

### Step 5: Resolve Stale Threads

Only resolve a thread **after** verifying the code now addresses it:

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "<thread_id>"}) {
    thread { isResolved }
  }
}'
```

Never resolve threads speculatively. If in doubt, leave open with a comment explaining what was done.

### Step 6: Re-check and Loop

After every round of fixes:

1. Return to Step 2
2. Re-snapshot the full state
3. Continue until ALL conditions below are met

## Stop Conditions

Only stop when ALL of the following are true:

- [ ] All CI checks are passing (or intentionally skipped with documented reason)
- [ ] Review decision is `APPROVED` or no blocking reviews remain
- [ ] No actionable comments in PR body or review threads
- [ ] No unresolved review threads
- [ ] PR is not in draft state

## Common Fixes

### Failing lint

```bash
npm run lint -- --fix
git add -A && git commit -m "fix: lint"
```

### Failing types

```bash
npx tsc --noEmit 2>&1 | head -30
# Fix each error, then
npx tsc --noEmit
```

### Failing tests

```bash
npm test -- --testPathPattern=<failing-file>
# Fix, then run full suite
npm test
```

### Conflicting branch

```bash
git fetch origin
git rebase origin/<base-branch>
# Resolve conflicts, then
git push --force-with-lease origin <branch>
```

## FinSurfing Context

For PRs in the FinSurfing repo:

- Railway preview deploys: check deploy logs if CI passes but preview fails
- Anthropic API integration tests: may need `ANTHROPIC_API_KEY` in CI secrets — confirm before chasing test failures
- PostgreSQL migration PRs: verify `db:migrate` step in CI ran successfully
- React/Vite build: check for bundle size warnings if build passes but reviewer flags size

## Related Skills

- `do` — What creates the PR this skill monitors
- `make-plan` — What created the plan that do executed
- `oh-my-issues` — If review surfaces architectural issues worth clustering
