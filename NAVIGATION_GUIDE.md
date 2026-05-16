# 📖 Navigation Guide: What to Read & When

Welcome! You've just completed a major upgrade of your Claude agents system. This guide shows you what to read in what order to get the most value.

## 🚀 TL;DR (30 seconds)

1. **Push to GitHub**: `git push origin main`
2. **Read**: SDE-PRACTICES.md (understand 23 skills)
3. **Install**: `./scripts/install.sh --tool cursor`
4. **Use**: Load 3 core skills + combine with agents

## 📚 Reading Path

### START HERE (Choose Your Path)

#### Path A: I Just Want It Working (5 min)
1. ✅ PROJECT_SUMMARY.md (quick overview)
2. ✅ DEPLOYMENT_GUIDE.md (push to GitHub)
3. Skip to: Quick Start section below

#### Path B: I Want to Understand Everything (30 min)
1. ✅ PROJECT_SUMMARY.md (overview)
2. ✅ SDE-PRACTICES.md (23 skills deep dive)
3. ✅ INTEGRATION.md (how agents + skills work)
4. ✅ DEPLOYMENT_GUIDE.md (push to GitHub)
5. Skip to: Workflow Examples below

#### Path C: I'm Building a Team Solution (1 hour)
1. ✅ PROJECT_SUMMARY.md (overview)
2. ✅ SDE-PRACTICES.md (understand all 23 skills)
3. ✅ INTEGRATION.md (architecture and patterns)
4. ✅ DEPLOYMENT_GUIDE.md (GitHub setup)
5. ✅ Read: your existing AGENTS.md (understand your agents)
6. ✅ Plan custom agent + skill combinations
7. Skip to: Customization section below

---

## 📋 Document Index

### v2.0.0 Release Documents

| Document | Purpose | Read If | Time |
|----------|---------|---------|------|
| **PROJECT_SUMMARY.md** | Overview of what was done | You just arrived | 5 min |
| **DEPLOYMENT_GUIDE.md** | How to push to GitHub | You need to deploy | 10 min |
| **SDE-PRACTICES.md** | Complete guide to 23 skills | You want to use the skills | 20 min |
| **INTEGRATION.md** | How agents + skills work | You want to combine them | 15 min |

### Previous Release Documents (For Reference)

| Document | Purpose | Read If | Time |
|----------|---------|---------|------|
| **AGENTS.md** | Agent directory | You want to see all agents | 10 min |
| **CLAUDE.md** | Claude Code config | You use Claude Code | 10 min |
| **README.md** | Main project overview | First time in repo | 5 min |
| **CHANGELOG.md** | Version history | You want to track changes | 5-10 min |

### From Agent-Skills (Previous Setup)

| Document | Purpose | Read If | Time |
|----------|---------|---------|------|
| **CURSOR_SETUP_GUIDE.md** | Cursor-specific setup | You use Cursor | 10 min |
| **QUICK_REFERENCE.md** | Command cheat sheet | You want quick commands | 2 min |

---

## 🎯 Quick Start (5 minutes)

### 1. Deploy to GitHub

```bash
cd /tmp/my-agents-setup/my-claude-agents

# Verify commit is ready
git log --oneline -1
# Output: 96d80b2 feat(v2.0): Integrate SDE practices + enhanced management tooling

# Push to GitHub
git push origin main

# Verify
git status
# Output: Your branch is up to date with 'origin/main'
```

### 2. Install Locally

```bash
./scripts/install.sh --tool cursor
# or your tool: claude-code, copilot, windsurf, etc.
```

### 3. Start Using

In Cursor (or your tool), try:

```
Follow test-driven-development rules for this implementation:
1. Write failing tests
2. Implement to make them pass
3. Verify edge cases
```

That's it! You're using the SDE practices.

---

## 🔄 Workflow Examples

### New Feature Development

```
1. Chat: "Help me plan this feature using spec-driven-development"
   → @product-manager writes spec
   
2. Chat: "Break this spec into tasks using planning-and-task-breakdown"
   → @project-manager creates task list
   
3. Chat: "Build task 1 using incremental-implementation"
   → Load: incremental-implementation.md
   → @engineer builds thin slice
   
4. Chat: "Write tests for this using test-driven-development"
   → Load: test-driven-development.md
   → @test-engineer writes tests first
   
5. Chat: "Review this code using code-review-and-quality"
   → @code-reviewer uses 5-axis review
   
6. Chat: "Deploy this using shipping-and-launch"
   → Load: shipping-and-launch.md
   → Go through pre-launch checklist
```

### Security Implementation

```
1. Chat: "Implement login using security-and-hardening"
   → @security-auditor checks for vulnerabilities
   
2. Chat: "Test this using test-driven-development"
   → Write tests for auth edge cases
   
3. Chat: "Review for security using security-hardening + code-review-and-quality"
   → @security-auditor and @code-reviewer validate
```

### Performance Optimization

```
1. Chat: "Profile using performance-optimization"
   → Load: performance-optimization.md
   → Measure before optimizing
   
2. Chat: "Optimize using incremental-implementation"
   → Build small, testable changes
   
3. Chat: "Review using code-review-and-quality + performance-optimization"
   → @code-reviewer validates quality
   
4. Chat: "Deploy using shipping-and-launch"
   → Staged rollout with monitoring
```

---

## 🛠️ Management Commands

### Installation

```bash
# Install to specific tool
./scripts/install.sh --tool cursor
./scripts/install.sh --tool claude-code
./scripts/install.sh --tool copilot
./scripts/install.sh --tool windsurf

# Install to all tools
./scripts/install.sh --tool all

# Interactive installer
./scripts/install.sh --interactive

# Parallel installation
./scripts/install.sh --tool all --parallel --jobs 4
```

### Validation

```bash
# Lint all agents and skills
./scripts/lint-agents.sh

# Lint specific agent/skill
./scripts/lint-agents.sh agents/engineering/my-agent.md
./scripts/lint-agents.sh skills/sde-practices/test-driven-development/SKILL.md
```

### Localization (Chinese)

```bash
# Localize agent names to Chinese
powershell -ExecutionPolicy Bypass -File scripts/i18n/localize-agents-zh.ps1

# Custom target directories
powershell -File scripts/i18n/localize-agents-zh.ps1 -TargetDirs @("C:\path\to\agents")
```

---

## 🎓 Learning Paths

### Path 1: Engineer Using TDD
**Goal**: Write better code with tests

1. Read: SDE-PRACTICES.md (sections: test-driven-development, test hierarchy)
2. Load skill: test-driven-development.md
3. Practice: Write tests first on next feature
4. Load skill: debugging-and-error-recovery.md (when tests fail)
5. Load skill: code-review-and-quality.md (before merge)

**Time**: 15 min reading + practice

### Path 2: Code Reviewer
**Goal**: Review code like a senior engineer

1. Read: SDE-PRACTICES.md (section: code-review-and-quality)
2. Read: INTEGRATION.md (agent + skill mapping)
3. Load agent: @code-reviewer
4. Load skill: code-review-and-quality.md
5. Practice: Review next PR using 5-axis framework

**Time**: 10 min reading + practice

### Path 3: Security Focus
**Goal**: Build secure applications

1. Read: SDE-PRACTICES.md (section: security-and-hardening)
2. Load agent: @security-auditor
3. Load skill: security-and-hardening.md
4. Practice: Review code for OWASP Top 10

**Time**: 10 min reading + practice

### Path 4: Full Lifecycle
**Goal**: Understand complete development flow

1. Read: SDE-PRACTICES.md (all 23 skills overview)
2. Read: INTEGRATION.md (full feature workflow)
3. Read each skill section as you move through phases
4. Practice: Build a feature using all phases

**Time**: 1 hour reading + building features

---

## 🚨 Important Notes

### Breaking Changes (v1.x → v2.0.0)

1. **Scripts moved to `scripts/` directory**
   - Was: `./install.sh`
   - Now: `./scripts/install.sh`

2. **New skill category: `skills/sde-practices/`**
   - Contains 23 new production-grade skills
   - Organized by development phase

3. **Version bumped to 2.0.0**
   - Signals major feature release
   - Check CHANGELOG.md for details

### Migration from v1.x

If you're upgrading:

```bash
# 1. Pull latest
git pull origin main

# 2. Update commands
./scripts/install.sh --tool cursor  # Not ./install.sh

# 3. Read new docs
# - SDE-PRACTICES.md (23 skills)
# - INTEGRATION.md (how to use them)

# 4. Validate
./scripts/lint-agents.sh
```

---

## ✅ Success Checklist

Before you start using this in production:

- [ ] Read PROJECT_SUMMARY.md (understand what was done)
- [ ] Read SDE-PRACTICES.md (understand the 23 skills)
- [ ] Read INTEGRATION.md (understand agent + skill patterns)
- [ ] Run `./scripts/lint-agents.sh` (verify structure)
- [ ] Run `./scripts/install.sh --tool cursor` (test installation)
- [ ] Load 3 core skills in your editor
- [ ] Try using a skill with an agent
- [ ] Push to GitHub (see DEPLOYMENT_GUIDE.md)
- [ ] Test fresh clone installation
- [ ] Create GitHub release (v2.0.0)

---

## 🆘 Troubleshooting

### "Where do I find [feature]?"

| Question | Answer |
|----------|--------|
| How do I install? | DEPLOYMENT_GUIDE.md |
| What skills are available? | SDE-PRACTICES.md |
| How do agents + skills work? | INTEGRATION.md |
| What's new in v2.0.0? | CHANGELOG.md + PROJECT_SUMMARY.md |
| How do I use Cursor? | CURSOR_SETUP_GUIDE.md |
| Quick command reference? | QUICK_REFERENCE.md |
| Who are all the agents? | AGENTS.md |
| What broke from v1? | CHANGELOG.md (Breaking Changes section) |

### "It's not working"

1. Check: `./scripts/lint-agents.sh`
2. Read: DEPLOYMENT_GUIDE.md (Troubleshooting section)
3. Check: INTEGRATION.md (Troubleshooting section)
4. Read: Relevant SKILL.md file

---

## 📞 Get Help

1. **For skill questions**: Read SDE-PRACTICES.md
2. **For workflow questions**: Read INTEGRATION.md
3. **For deployment**: Read DEPLOYMENT_GUIDE.md
4. **For agent questions**: Read AGENTS.md
5. **For version/changes**: Read CHANGELOG.md

---

## 🎯 Next Actions

### Right Now (5 min)

1. Push to GitHub: `git push origin main`
2. Read: PROJECT_SUMMARY.md

### Today (30 min)

1. Read: SDE-PRACTICES.md
2. Read: INTEGRATION.md
3. Run: `./scripts/install.sh --tool cursor`
4. Load 3 core skills in your editor

### This Week

1. Use TDD on your next feature
2. Try code-review-and-quality on a PR
3. Combine agent + skill in workflow

### This Month

1. Document custom workflows
2. Create custom agents/skills for your team
3. Set up GitHub release & documentation

---

## 📦 File Locations

All files are in `/mnt/user-data/outputs/`:
```
outputs/
├── DEPLOYMENT_GUIDE.md        ← How to push to GitHub
├── PROJECT_SUMMARY.md         ← What was done & next steps
├── SDE-PRACTICES.md           ← 23 skills complete guide
├── INTEGRATION.md             ← Architecture & patterns
├── AGENTS.md                  ← Agent directory
├── CHANGELOG.md               ← Version history
├── README.md                  ← Original project readme
├── CURSOR_SETUP_GUIDE.md      ← Cursor-specific setup
├── QUICK_REFERENCE.md         ← Command cheat sheet
├── code-reviewer.md           ← Agent persona
├── test-engineer.md           ← Agent persona
├── security-auditor.md        ← Agent persona
└── .cursor/rules/             ← All 23 skills + originals

Repository: /tmp/my-agents-setup/my-claude-agents/
```

---

## 🎉 You're Ready!

You have:
- ✅ 23 production-grade SDE practices
- ✅ Enhanced management scripts
- ✅ Comprehensive documentation
- ✅ Proven agent + skill combinations
- ✅ Clear deployment path
- ✅ Everything ready to ship

**Next step**: Read DEPLOYMENT_GUIDE.md and push to GitHub!

```bash
git push origin main
```

---

**Questions?** Check the appropriate guide above.  
**Ready to start?** Read SDE-PRACTICES.md next.  
**Need help deploying?** See DEPLOYMENT_GUIDE.md.

**Version 2.0.0 - Let's ship! 🚀**
