---
name: version-bump
description: >-
  Automated semantic versioning and release workflow for Claude Code plugins
  and npm packages. Handles version increments across all manifest files,
  npm publishing, git tagging, GitHub releases, and changelog generation.
  TRIGGER when: user says "release", "bump version", "publish", "cut a release",
  or "tag this version".
origin: claude-mem
owner: surfingalien
---

# version-bump

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Automate the full semantic versioning and release workflow. Bump every version string in every manifest, publish to npm, tag in git, create a GitHub release, and generate a changelog entry.

**CRITICAL:** Plan and write detailed release notes **before** starting. Commit EVERYTHING including build artifacts. At the end, `git status` must be clean.

## When to Use

- Releasing a new version of a Claude Code plugin or skill package
- Publishing an npm package update
- Cutting a tagged GitHub release
- Bumping version after a sprint or set of merged PRs

## Step 1: Classify the Change

Before touching any files, determine the version bump type:

| Type | When | Example |
|------|------|---------|
| **PATCH** | Bug fixes, docs, minor improvements | 1.2.3 → 1.2.4 |
| **MINOR** | New features, backward-compatible additions | 1.2.3 → 1.3.0 |
| **MAJOR** | Breaking changes, removed APIs, incompatible updates | 1.2.3 → 2.0.0 |

When in doubt: MINOR for new skills/agents, PATCH for fixes, MAJOR for breaking interface changes.

## Step 2: Identify All Version Strings

Every file that carries the version string must be updated atomically. Check for:

```bash
# Find all version references
grep -r "\"version\"" . \
  --include="*.json" \
  ! -path "*/node_modules/*" \
  ! -path "*/.git/*"

# Common locations
cat package.json | jq '.version'
cat plugin/package.json | jq '.version' 2>/dev/null
cat .claude-plugin/marketplace.json | jq '.plugins[0].version' 2>/dev/null
cat .claude-plugin/plugin.json | jq '.version' 2>/dev/null
```

For **my-claude-agents** repo:
```bash
cat VERSION
```

## Step 3: Write Release Notes

**Before changing any files**, draft the changelog entry:

```markdown
## [X.Y.Z] — YYYY-MM-DD

### Added
- [New skill/agent/feature with one-line description]

### Changed
- [What changed and why]

### Fixed
- [Bug fixed with context]

### Breaking (MAJOR only)
- [What breaks and migration path]
```

## Step 4: Bump Version in All Files

```bash
# Set new version
NEW_VERSION="X.Y.Z"

# package.json
npm version $NEW_VERSION --no-git-tag-version

# plugin/package.json (if exists)
cd plugin && npm version $NEW_VERSION --no-git-tag-version && cd ..

# marketplace.json (Claude Code plugin manifest)
jq ".plugins[0].version = \"$NEW_VERSION\"" .claude-plugin/marketplace.json > tmp.json \
  && mv tmp.json .claude-plugin/marketplace.json

# plugin.json
jq ".version = \"$NEW_VERSION\"" .claude-plugin/plugin.json > tmp.json \
  && mv tmp.json .claude-plugin/plugin.json

# VERSION file (if exists)
echo "$NEW_VERSION" > VERSION
```

Verify all version strings are consistent:

```bash
grep -r "\"version\"" . --include="*.json" ! -path "*/node_modules/*" | grep -v "$NEW_VERSION"
# Should return nothing
```

## Step 5: Build

```bash
# Run the project build
npm run build

# Verify build artifacts exist
ls -la dist/ plugin/dist/ 2>/dev/null
```

Commit build artifacts. Do not .gitignore them if they're part of the release.

## Step 6: Prepend Changelog

Add the release notes to `CHANGELOG.md`:

```bash
# Prepend to CHANGELOG.md
{
  echo "## [$NEW_VERSION] — $(date +%Y-%m-%d)"
  echo ""
  echo "[release notes content]"
  echo ""
  cat CHANGELOG.md
} > CHANGELOG.tmp && mv CHANGELOG.tmp CHANGELOG.md
```

## Step 7: Commit Everything

```bash
git add -A
git status  # verify — nothing should be untracked or modified after this
git commit -m "chore(release): v$NEW_VERSION

[First line of release notes]

[Full release notes]"
```

## Step 8: Tag and Push

```bash
# Create annotated tag
git tag -a "v$NEW_VERSION" -m "v$NEW_VERSION — [one-line release summary]"

# Push commits and tag
git push origin main
git push origin "v$NEW_VERSION"
```

## Step 9: GitHub Release

```bash
gh release create "v$NEW_VERSION" \
  --title "v$NEW_VERSION — [Release Title]" \
  --notes "$(cat release-notes.md)" \
  --latest
```

## Step 10: npm Publish (if applicable)

```bash
# Dry run first
npm publish --dry-run

# Confirm output looks correct, then publish
npm publish --access public
```

For scoped packages: `npm publish --access public --scope @surfingalien`

## Step 11: Final Verification

```bash
# Clean working tree
git status  # must show nothing

# Tag exists
git tag | grep "$NEW_VERSION"

# GitHub release visible
gh release view "v$NEW_VERSION"

# npm package live (if published)
npm view <package-name> version
```

## my-claude-agents Release Pattern

For the `surfingalien/my-claude-agents` repo:

```bash
# Version is in VERSION file
cat VERSION  # current
echo "X.Y.Z" > VERSION

# Update CHANGELOG.md with new skills added
# Commit, tag, push
git add VERSION CHANGELOG.md
git commit -m "chore(release): v$(cat VERSION) — add [skill list]"
git tag -a "v$(cat VERSION)" -m "Release v$(cat VERSION)"
git push origin main --tags
```

## Anti-Patterns

❌ Bumping version without building first
❌ Missing a manifest file (version strings go out of sync)
❌ Tagging before committing build artifacts
❌ Publishing to npm without a dry-run check
❌ No changelog entry

## Related Skills

- `do` — Use to execute multi-step releases via subagents
- `babysit` — If CI gates the release, use babysit to monitor
- `make-plan` — Pre-plan a major release with breaking changes
