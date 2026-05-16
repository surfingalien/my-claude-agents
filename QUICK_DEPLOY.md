# ⚡ Quick Deploy Commands

Copy-paste these commands to deploy your v2.0.0 release.

## One-Liner Deploy (Copy & Paste)

```bash
cd /tmp/my-agents-setup/my-claude-agents && git push origin main && echo "✅ Pushed to GitHub!"
```

## Step-by-Step Deploy

### Verify Everything is Ready

```bash
# Navigate to repo
cd /tmp/my-agents-setup/my-claude-agents

# Check status
git status
# Expected: "working tree clean" and "ahead of 'origin/main' by 1 commit"

# Verify commit
git log --oneline -1
# Expected: 96d80b2 feat(v2.0): Integrate SDE practices + enhanced management tooling
```

### Option A: Deploy with GitHub CLI (Recommended)

```bash
# Authenticate (one-time)
gh auth login

# Push to GitHub
git push origin main

# View on GitHub
gh repo view --web
```

### Option B: Deploy with HTTPS (GitHub PAT)

```bash
# If not using credential storage yet:
git config --global credential.helper store

# Push (will prompt for token)
git push origin main

# When prompted:
# Username: surfingalien
# Password: [paste your GitHub Personal Access Token]

# To get a Personal Access Token:
# 1. Go to: https://github.com/settings/tokens/new
# 2. Scopes: repo, workflow
# 3. Copy token (only shown once!)
```

### Option C: Deploy with SSH

```bash
# If SSH keys are already configured:
git push origin main

# If not set up, first:
# 1. Generate key: ssh-keygen -t ed25519 -C "your-email@example.com"
# 2. Copy public key: cat ~/.ssh/id_ed25519.pub
# 3. Add to GitHub: https://github.com/settings/keys
# 4. Then: git push origin main
```

## Verify Deployment

### Check Local

```bash
git status
# Expected: "Your branch is up to date with 'origin/main'"

git log --oneline -1
# Expected: 96d80b2 feat(v2.0)...
```

### Check Remote

```bash
git fetch origin
git log origin/main --oneline -1
# Expected: 96d80b2 feat(v2.0)...

# Or visit:
https://github.com/surfingalien/my-claude-agents
```

## Test Installation After Push

```bash
# Test fresh clone
cd /tmp/fresh-test
git clone https://github.com/surfingalien/my-claude-agents.git
cd my-claude-agents

# Verify files
cat VERSION            # Should be: 2.0.0
ls scripts/            # Should show: convert.sh, install.sh, lint-agents.sh, i18n/
ls skills/sde-practices/ | wc -l  # Should be: 23

# Test scripts
./scripts/lint-agents.sh
# Expected: "PASSED"

# Cleanup
cd /tmp && rm -rf fresh-test
```

## Create Release on GitHub

### Option A: With GitHub CLI

```bash
cd /tmp/my-agents-setup/my-claude-agents

gh release create v2.0.0 \
  --title "v2.0.0: SDE Practices & Enhanced Tooling" \
  --notes "Production-grade SDE practices with 23 skills, enhanced management scripts, and comprehensive documentation. See CHANGELOG.md for full details."
```

### Option B: Web UI

```
1. Go to: https://github.com/surfingalien/my-claude-agents/releases/new
2. Tag: v2.0.0
3. Title: v2.0.0: SDE Practices & Enhanced Tooling
4. Description: Copy from CHANGELOG.md (v2.0.0 section)
5. Click "Publish release"
```

## All Together (Complete Workflow)

```bash
# 1. Navigate
cd /tmp/my-agents-setup/my-claude-agents

# 2. Verify
git log --oneline -1
git status

# 3. Deploy (choose one)
# GitHub CLI:
gh auth login && git push origin main && gh repo view --web

# HTTPS:
git push origin main  # Will prompt for token

# SSH:
git push origin main  # If already configured

# 4. Wait for GitHub to sync (1-2 seconds)

# 5. Create release
# Option A: Web UI at https://github.com/surfingalien/my-claude-agents/releases/new
# Option B: CLI (if you have `gh` installed)
# gh release create v2.0.0 --title "v2.0.0: SDE Practices & Enhanced Tooling" --notes "See CHANGELOG.md"

# 6. Done! 🎉
```

## Troubleshooting

### "fatal: 'origin' does not appear to be a git repository"

```bash
# Wrong directory
cd /tmp/my-agents-setup/my-claude-agents
pwd  # Should end in my-claude-agents
```

### "Permission denied (publickey)" or "401 Unauthorized"

```bash
# SSH issue - use HTTPS instead:
git config --global user.password ""
git push origin main

# Or create GitHub PAT and use that:
# https://github.com/settings/tokens/new
```

### "Your branch is ahead of 'origin/main' by 1 commit" (After push)

```bash
# Normal - wait 1-2 seconds for GitHub to sync
git fetch origin
git status
# Should now show: "Your branch is up to date with 'origin/main'"
```

### Can't find GitHub CLI

```bash
# Install it:
# macOS
brew install gh

# Linux
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update && sudo apt install gh

# Windows
choco install gh
```

## Recovery (If Needed)

### Undo Local Commit (Keep Changes)

```bash
git reset --soft HEAD~1
# Now you can edit and recommit
```

### Undo Local Commit (Delete Changes)

```bash
git reset --hard HEAD~1
# Reverts to previous commit
```

### Revert Pushed Commit (Create New Commit)

```bash
git revert 96d80b2
git push origin main
# Creates a new commit that undoes the changes
```

## Verification Checklist

- [ ] `git status` shows "working tree clean"
- [ ] `git log --oneline -1` shows the v2.0.0 commit
- [ ] `git push origin main` succeeds
- [ ] GitHub repo shows the new commit
- [ ] VERSION file shows 2.0.0
- [ ] SDE-PRACTICES.md is accessible
- [ ] INTEGRATION.md is accessible
- [ ] scripts/ directory with all 4 files is visible
- [ ] skills/sde-practices/ with 23 skills is visible
- [ ] CHANGELOG.md has v2.0.0 entry at top
- [ ] GitHub release created (optional but recommended)

## Common Questions

### How do I know if it worked?

```bash
git status
# Should show: "Your branch is up to date with 'origin/main'"

# And check GitHub:
https://github.com/surfingalien/my-claude-agents/commits/main
# Should show: 96d80b2 at top
```

### Can I undo if something goes wrong?

```bash
# Yes! Several options:
git reset --soft HEAD~1    # Keep changes, undo commit
git reset --hard HEAD~1    # Undo everything
git revert 96d80b2         # Undo but create new commit
```

### How do I add more to the commit?

```bash
git reset --soft HEAD~1
git add .
git commit -m "new message"
git push origin main
```

### What if I forget to push?

```bash
git log origin/main --oneline -1
# Compare with:
git log --oneline -1

# If different, just push:
git push origin main
```

## Time Estimates

| Task | Time | Command |
|------|------|---------|
| Verify | 10s | `git status && git log --oneline -1` |
| Push (GitHub CLI) | 5s | `git push origin main` |
| Push (HTTPS) | 10s | `git push origin main` (+ token entry) |
| Verify on GitHub | 5s | Visit repo or `gh repo view --web` |
| Create release | 30s | `gh release create v2.0.0 ...` |
| Test fresh clone | 30s | `git clone ... && ./scripts/lint-agents.sh` |
| **Total** | **~2 min** | **All of the above** |

---

## 🎯 Summary

1. **Navigate**: `cd /tmp/my-agents-setup/my-claude-agents`
2. **Verify**: `git status` and `git log --oneline -1`
3. **Push**: `git push origin main`
4. **Verify on GitHub**: Visit repo or `gh repo view --web`
5. **Create release**: (Optional) GitHub UI or `gh release create v2.0.0`
6. **Test**: (Optional) Fresh clone + lint-agents.sh
7. **Done!** 🎉

---

**Need help?** See DEPLOYMENT_GUIDE.md for detailed instructions.  
**Ready to deploy?** Copy the one-liner above and paste it!

```bash
cd /tmp/my-agents-setup/my-claude-agents && git push origin main && echo "✅ Pushed to GitHub!"
```

**Let's ship it! 🚀**
