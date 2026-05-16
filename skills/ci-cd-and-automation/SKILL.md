---name: ci-cd-and-automation
description: Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines. Use when you need to automate quality gates, configure test runners in CI, or establish deployment strategies.---

# Ci Cd And Automation Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# CI/CD and Automation

## Overview

Automate quality gates so that no change reaches production without passing tests, lint, type checking, and build. CI/CD is the enforcement mechanism for every other skill — it catches what humans and agents miss, consistently on every change.

**Shift Left:** Catch problems as early as possible. A bug caught in linting costs minutes; the same bug in production costs hours.

**Faster is Safer:** Smaller batches and more frequent releases reduce risk. A deployment with 3 changes is easier to debug than one with 30.

## The Quality Gate Pipeline

```
Pull Request Opened
    │
    ▼
LINT CHECK → TYPE CHECK → UNIT TESTS → BUILD → INTEGRATION → E2E (optional) → SECURITY AUDIT → BUNDLE SIZE
    │
    ▼
  Ready for review
```

No gate can be skipped. If lint fails, fix lint — don't disable the rule.

## GitHub Actions Configuration

### Basic CI Pipeline

```yaml
name: CI
on:
  pull_request: { branches: [main] }
  push: { branches: [main] }

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npx tsc --noEmit
      - run: npm test -- --coverage
      - run: npm run build
      - run: npm audit --audit-level=high
```

### With Database Integration Tests

```yaml
  integration:
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: ci_user
          POSTGRES_PASSWORD: ${{ secrets.CI_DB_PASSWORD }}
        options: --health-cmd pg_isready --health-interval 10s --health-retries 5
```

> Use GitHub Secrets for credentials — even for CI-only test databases.

### E2E Tests

```yaml
  e2e:
    steps:
      - run: npx playwright install --with-deps chromium
      - run: npx playwright test
      - uses: actions/upload-artifact@v4
        if: failure()
        with: { name: playwright-report, path: playwright-report/ }
```

## Feeding CI Failures Back to Agents

```
CI fails → Copy failure output → Feed to agent:
"The CI pipeline failed with this error: [paste specific error]
Fix the issue and verify locally before pushing again."
```

## Deployment Strategies

### Feature Flags

Decouple deployment from release. Deploy incomplete features behind flags:

```typescript
if (featureFlags.isEnabled('new-checkout-flow', { userId })) {
  return renderNewCheckout();
}
return renderLegacyCheckout();
```

**Flag lifecycle:** Create → Enable for testing → Canary → Full rollout → Remove flag and dead code.

### Staged Rollout

```
PR merged → Staging (auto) → Manual verification → Production → Monitor 15 min → Done | Rollback
```

### Rollback Plan

```yaml
name: Rollback
on:
  workflow_dispatch:
    inputs:
      version: { description: 'Version to rollback to', required: true }
jobs:
  rollback:
    steps:
      - run: npx vercel rollback ${{ inputs.version }}
```

## Environment Management

```
.env.example  → Committed (template)
.env          → NOT committed (local)
.env.test     → Committed (no real secrets)
CI secrets    → GitHub Secrets / vault
```

## CI Optimization

```
Slow CI? →
  Cache dependencies (actions/cache or setup-node cache)
  Run jobs in parallel (split lint, typecheck, test, build)
  Only run what changed (path filters)
  Shard test suites across runners
  Use larger runners for CPU-heavy builds
```

## Verification

- [ ] All quality gates present (lint, types, tests, build, audit)
- [ ] Pipeline runs on every PR and push to main
- [ ] Failures block merge (branch protection configured)
- [ ] Secrets in secrets manager, not in code
- [ ] Deployment has a rollback mechanism
- [ ] Pipeline runs in under 10 minutes