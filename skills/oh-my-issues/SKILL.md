---
name: oh-my-issues
description: >-
  Cluster a GitHub issue backlog by root cause, create plan-master issues for
  each architectural defect, redirect child issues with standardized comments,
  and bundle fix PRs that close clusters atomically. TRIGGER when: issue tracker
  has 20+ open issues with duplicates, user says "triage", "consolidate",
  "cluster", "dedupe", or "make a roadmap from issues". Also routes new bugs
  into existing plans.
origin: claude-mem
owner: surfingalien
---

# oh-my-issues

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Core Principle

Stop closing issues one at a time. Issues are **symptom data** — the unit of work is the architectural defect that produces them.

Group symptoms that share a single root cause into a cluster. Give each cluster one canonical home (a plan-master issue + a `plans/NN-*.md` doc). Close every child with a standardized redirect. Ship one PR per cluster that closes all children atomically.

**End state: open issues == open plans. 1:1.**

## When to Use

- Repo has 20+ open issues and many feel like duplicates or platform-specific variants of the same bug
- User asks to "triage", "consolidate", "cluster", "dedupe", or "build a roadmap from issues"
- A new bug is filed and needs routing to an existing plan rather than a new tracked issue
- Post-incident: cluster all issues filed during an outage by root cause

## Workflow

### Phase 1: Ingest the Backlog

```bash
# Fetch all open issues with labels and body
gh issue list --state open --limit 200 --json number,title,body,labels,comments > issues.json

# Count and preview
cat issues.json | jq 'length'
cat issues.json | jq '.[].title'
```

### Phase 2: Cluster by Root Cause

Deploy a subagent to read all issues and group them by the **architectural defect** they symptomize — not by label, component, or feature area.

Clustering rules:
- Issues sharing the same root cause → one cluster, regardless of surface area
- Platform-specific symptoms of the same bug → same cluster
- Bot-filed variants of the same regression → same cluster
- Genuinely independent defects → separate clusters

Output format:

```markdown
## Cluster A: [Root Cause Name]
**Defect:** [One sentence describing the architectural defect]
**Issues:** #12, #34, #67, #89
**Evidence:** [What the issues have in common]

## Cluster B: [Root Cause Name]
...
```

### Phase 3: Create Plan-Master Issues

For each cluster, create one canonical issue:

```bash
gh issue create \
  --title "plan: [Root Cause Name]" \
  --body "$(cat plan-master-template.md)" \
  --label "plan-master"
```

Plan-master issue body template:

```markdown
## Root Cause

[One paragraph describing the architectural defect, not the symptoms]

## Symptoms (Child Issues)

| Issue | Title | Status |
|-------|-------|--------|
| #12 | ... | → redirected |
| #34 | ... | → redirected |

## Fix Strategy

[Proposed architectural fix — reference plans/NN-<slug>.md]

## Prevention

[What CI check, type constraint, or test would catch regressions]

## Rounds

**Round 1** — [date]: Issues #12, #34, #67, #89
```

### Phase 4: Redirect Children

For each child issue, post a standardized redirect comment:

```bash
gh issue comment <child-number> --body "$(cat redirect-comment.md)"
gh issue close <child-number>
```

Redirect comment template:

```markdown
**Redirected to plan-master → #<plan-master-number>**

This issue is a symptom of the architectural defect tracked in #<plan-master-number>.
Progress, discussion, and the fix will land there.

If this issue has a specific angle not covered, please add a comment to #<plan-master-number>.
```

### Phase 5: Create Plans

For each cluster, create `plans/NN-<cluster-slug>.md` using `make-plan` format:

```bash
# Reference make-plan skill for plan format
# Each plan closes its cluster atomically: PR body includes "Closes #12, #34, #67, #89"
```

### Phase 6: Routing New Bugs

When a new issue arrives during triage:

1. Search existing plan-masters for matching root cause
2. If match found: comment on new issue with plan-master link and close
3. If no match: open new cluster (go to Phase 3)
4. Never let "Round N" issues accumulate as new tracked issues

```bash
# Search plan-masters
gh issue list --label "plan-master" --json number,title,body | jq '.[] | select(.body | contains("<keyword>"))'
```

## Anti-Patterns to Avoid

❌ Creating a plan-master per symptom (defeats the purpose)
❌ Closing issues without a redirect comment
❌ Mixing architectural fixes with feature work in one cluster
❌ "Triage" that just re-labels without clustering
❌ Plans that require reading all prior plans to make sense

## Metrics

After triage, report:

```
📊 Backlog Summary
- Total open issues before: N
- Clusters identified: M
- Plan-masters created: M
- Issues redirected/closed: N-M
- Open issues after: M (1:1 with plans)
```

## FinSurfing Context

Common issue patterns to watch for:

- **Anthropic API timeout clusters** — may all trace to missing retry logic
- **Railway env var issues** — may cluster around missing `.env` sync pattern
- **PostgreSQL query performance** — may cluster around missing index strategy
- **React state sync bugs** — may cluster around a single shared state pattern
- **AI-Trader integration failures** — route to trading intelligence roadmap plan

## Related Skills

- `make-plan` — Creates the `plans/NN-*.md` file for each cluster
- `do` — Executes the fix plan
- `babysit` — Monitors the PR that closes the cluster
- `pathfinder` — Use before oh-my-issues if the codebase architecture itself needs mapping
