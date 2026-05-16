# Jira Workflow Skill

## Overview

Provides Jira-linked Git workflow management: branch naming conventions, Gitmoji commit formatting, PR template generation, and Git hook validation. Ensures every code change traces back to a Jira ticket, maintaining full traceability from requirement to deployment.

## Capabilities

### Branch Naming Convention

**Format:** `<type>/<JIRA-ID>-<short-description>`

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/PROJ-123-short-description` | `feature/AUTH-214-add-sso-login` |
| Bug fix | `bugfix/PROJ-456-short-description` | `bugfix/AUTH-315-fix-token-refresh` |
| Hotfix | `hotfix/PROJ-789-short-description` | `hotfix/AUTH-411-patch-auth-bypass` |
| Release | `release/X.Y.Z` | `release/2.4.0` |
| Chore | `chore/PROJ-012-short-description` | `chore/INFRA-012-upgrade-node` |

**Rules:**
- Jira ID required for all non-release branches
- Description: lowercase, hyphens only, ≤40 characters
- No spaces, no special characters, no uppercase after prefix

### Gitmoji Commit Format

**Format:** `<emoji> <JIRA-ID>: <imperative description>`

| Gitmoji | Code | When to Use |
|---------|------|-------------|
| 🚀 | `:rocket:` | Deployments and releases |
| ✨ | `:sparkles:` | New features |
| 🐛 | `:bug:` | Bug fixes |
| ♻️ | `:recycle:` | Refactoring |
| 📚 | `:books:` | Documentation |
| 🧪 | `:test_tube:` | Tests |
| 💄 | `:lipstick:` | UI/styling |
| 🔧 | `:wrench:` | Config/tooling |
| 📦 | `:package:` | Dependencies |
| 🔒 | `:lock:` | Security fixes |
| ⚡ | `:zap:` | Performance |
| 🗑️ | `:wastebasket:` | Removing code |

**Examples:**
```
✨ AUTH-214: add SSO login flow with OAuth 2.0
🐛 AUTH-315: fix token refresh race condition
♻️ INFRA-042: extract auth middleware to shared module
🧪 AUTH-214: add integration tests for SSO callback
📦 INFRA-099: upgrade express to 4.19.0
```

### PR Template

```markdown
## What does this PR do?

Closes [JIRA-ID](https://yourorg.atlassian.net/browse/JIRA-ID)

### Summary


### Changes
- [ ] 
- [ ] 
- [ ] 

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

### Screenshots (if UI change)


### Checklist
- [ ] Code follows project style guide
- [ ] Self-review completed
- [ ] No sensitive data in code/logs
- [ ] Documentation updated
```

### Git Hook Validation

**commit-msg hook:**
```bash
#!/usr/bin/env bash
set -euo pipefail
message_file="${1:?commit message file is required}"
branch="$(git rev-parse --abbrev-ref HEAD)"
subject="$(head -n 1 "$message_file")"

branch_regex='^(feature|bugfix|hotfix|chore)/[A-Z]+-[0-9]+-[a-z0-9-]+$|^release/[0-9]+\.[0-9]+\.[0-9]+$'
commit_regex='^(🚀|✨|🐛|♻️|📚|🧪|💄|🔧|📦|🔒|⚡|🗑️) [A-Z]+-[0-9]+: .+'

if [[ ! "$branch" =~ $branch_regex ]]; then
  echo "ERROR: Invalid branch name: $branch" >&2
  echo "Expected: feature/PROJ-123-description or release/X.Y.Z" >&2
  exit 1
fi

if [[ "$branch" != release/* && ! "$subject" =~ $commit_regex ]]; then
  echo "ERROR: Invalid commit subject: $subject" >&2
  echo "Expected: ✨ PROJ-123: imperative description" >&2
  exit 1
fi
```

## Scripts

### `scripts/branch_commit_generator.py`

Generates valid branch names and commit messages from Jira ID and description inputs.

```
Usage: python branch_commit_generator.py --jira AUTH-214 --type feature --desc "add SSO login"
       python branch_commit_generator.py --jira AUTH-315 --type bugfix --desc "fix token refresh"
       python branch_commit_generator.py --validate --branch "feature/AUTH-214-add-sso" --commit "✨ AUTH-214: add SSO"
       python branch_commit_generator.py --pr-template --jira AUTH-214
Output:
  - Valid branch name following naming convention
  - Gitmoji commit message suggestion
  - Validation result for existing branch/commit
  - PR description template pre-filled with Jira ID
```

## References

### `references/git_workflow_guide.md`
Branch strategy overview, merge vs rebase policy, squash commits on PR merge, protected branch rules (main, release/*), hotfix process for production incidents, and version tagging convention.

### `references/jira_field_mapping.md`
Jira issue type to Git branch type mapping, Jira status transitions triggered by branch events (In Review when PR opened, Done when merged), required custom fields, sprint ceremony workflow integration.

## Assets

### `assets/pr_template.md`
Ready-to-copy PR description template with Jira link, summary, changes checklist, testing checklist, and screenshots section.

### `assets/commit_msg_hook`
Drop-in `commit-msg` Git hook for enforcing branch naming and commit message format locally.

## Quality Standards

- Every branch name includes valid Jira ticket ID (except release branches)
- Every commit subject includes Gitmoji + Jira ID + imperative verb
- PR descriptions link to Jira ticket within first 3 lines
- No direct commits to main or release/* branches
- PR requires at least 1 approving review before merge
- Squash merge on all PRs to keep main history linear
