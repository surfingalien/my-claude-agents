# 🔗 Integration Guide: Agents, Skills & Management Scripts

This document explains how **agents**, **SDE practice skills**, and **management scripts** work together in your workflow.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│ Your Claude Environment (Cursor, Claude Code, GitHub Copilot)   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────┐    ┌──────────────────────────────┐   │
│  │   AGENTS (Who)      │    │   SKILLS (How)               │   │
│  ├─────────────────────┤    ├──────────────────────────────┤   │
│  │ • code-reviewer     │    │ • test-driven-development    │   │
│  │ • test-engineer     │    │ • code-review-and-quality    │   │
│  │ • security-auditor  │    │ • incremental-implementation │   │
│  │ • architect         │    │ • spec-driven-development    │   │
│  │ • product-manager   │    │ • frontend-ui-engineering    │   │
│  │ • ... (100+)        │    │ • security-and-hardening     │   │
│  │                     │    │ • performance-optimization    │   │
│  │                     │    │ • ... (23 SDE practices)     │   │
│  └─────────────────────┘    └──────────────────────────────┘   │
│         ^                              ^                        │
│         │                              │                        │
│         └──────────────────────────────┘                        │
│                    You tell Claude:                             │
│            "@agent-name Use skill-name for this task"           │
└─────────────────────────────────────────────────────────────────┘
                           │
                           │ ./scripts/install.sh
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│          Management Scripts (Installation & Validation)          │
├─────────────────────────────────────────────────────────────────┤
│ • install.sh        → Deploy agents/skills to tools             │
│ • convert.sh        → Convert formats (MD → tool-specific)      │
│ • lint-agents.sh    → Validate YAML, structure, content         │
│ • i18n/localize-*.ps1 → Translate to Chinese, etc.             │
└─────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
my-claude-agents/
│
├── agents/                          [AGENT DEFINITIONS]
│   ├── academic/
│   ├── design/
│   ├── engineering/
│   ├── finance/
│   ├── ... (15+ domains)
│
├── skills/                          [SKILL PACKS]
│   ├── sde-practices/               ← NEW: 23 SDE skills
│   │   ├── test-driven-development/
│   │   ├── code-review-and-quality/
│   │   ├── incremental-implementation/
│   │   └── ... (20 more)
│   │
│   ├── engineering/
│   ├── business-growth/
│   ├── ... (other skill packs)
│
├── scripts/                         [MANAGEMENT SCRIPTS]
│   ├── install.sh                   ← Install agents/skills
│   ├── convert.sh                   ← Format conversion
│   ├── lint-agents.sh               ← Validation
│   │
│   └── i18n/                        [LOCALIZATION]
│       ├── localize-agents-zh.ps1   ← Chinese localization
│       └── agent-names-zh.json      ← Chinese translations
│
├── rules/                           [CURSOR/CODE RULES]
├── personas/                        [SPECIALIZED ROLES]
├── contexts/                        [DOMAIN-SPECIFIC CONTEXT]
├── mcp-configs/                     [MCP SERVER CONFIGS]
├── commands/                        [CUSTOM COMMANDS]
├── hooks/                           [LIFECYCLE HOOKS]
│
├── AGENTS.md                        ← Agent directory
├── SDE-PRACTICES.md                 ← THIS GUIDE: SDE skills
├── README.md                        ← Main readme
├── CLAUDE.md                        ← Claude Code config
├── INTEGRATION.md                   ← THIS FILE
├── CHANGELOG.md                     ← Version history
└── VERSION                          ← Current version
```

## How to Use: Agent + Skill Combinations

### Example 1: TDD Feature Implementation

**Scenario**: Implementing a new user authentication feature

```
Step 1: Tell Claude which agent to use
├─ @test-engineer Design test cases for login feature

Step 2: Load the TDD skill
├─ "Use test-driven-development for this implementation:
│   1. Write failing tests
│   2. Implement to make them pass
│   3. Verify edge cases"

Step 3: Let the code-reviewer agent review
├─ @code-reviewer Review this implementation using code-review-and-quality

Step 4: Use the security-auditor agent
├─ @security-auditor Audit the login flow using security-and-hardening

Step 5: Ship with confidence
├─ "Use shipping-and-launch for production deployment"
```

### Example 2: Performance Optimization

**Scenario**: Your app is slow, need to fix it

```
Agent sequence:
1. @architect        - "Use performance-optimization to profile"
2. @code-reviewer    - "Review optimizations using code-review-and-quality"
3. @engineer         - "Implement incremental-implementation style"
4. @test-engineer    - "Test using browser-testing-with-devtools"
5. @deployer         - "Deploy using shipping-and-launch"
```

### Example 3: Security Audit

**Scenario**: Found a potential vulnerability

```
Agent + skill flow:
1. @security-auditor - "Audit using security-and-hardening"
2. @test-engineer    - "Write tests using test-driven-development"
3. @code-reviewer    - "Review using code-review-and-quality"
4. @architect        - "Document using documentation-and-adrs"
5. @deployer         - "Ship using shipping-and-launch"
```

## Installation & Setup

### Quick Start (5 minutes)

```bash
# 1. Navigate to your project
cd ~/your-project

# 2. Clone/pull this repo
git clone https://github.com/surfingalien/my-claude-agents.git

# 3. Install agents and skills for your tool
./scripts/install.sh --tool cursor        # Cursor
./scripts/install.sh --tool claude-code   # Claude Code
./scripts/install.sh --tool copilot       # GitHub Copilot

# 4. Validate installation
./scripts/lint-agents.sh
```

### For Different Tools

```bash
# Cursor
./scripts/install.sh --tool cursor

# Claude Code (embedded)
./scripts/install.sh --tool claude-code

# GitHub Copilot
./scripts/install.sh --tool copilot

# Windsurf
./scripts/install.sh --tool windsurf

# All available tools
./scripts/install.sh --tool all
```

### For Chinese Users

```bash
# After installation, localize agent names to Chinese
powershell -ExecutionPolicy Bypass -File scripts/i18n/localize-agents-zh.ps1
```

## Agent + Skill Mapping

### Core Development

| Task | Best Agent | Best Skill |
|------|-----------|-----------|
| Code review | code-reviewer | code-review-and-quality |
| Test strategy | test-engineer | test-driven-development |
| Security audit | security-auditor | security-and-hardening |
| Architecture | architect | api-and-interface-design |
| UI building | frontend-engineer | frontend-ui-engineering |
| Performance | performance-analyst | performance-optimization |
| Documentation | technical-writer | documentation-and-adrs |

### Product & Business

| Task | Best Agent | Best Skill |
|------|-----------|-----------|
| Feature spec | product-manager | spec-driven-development |
| Planning | project-manager | planning-and-task-breakdown |
| Launch | release-manager | shipping-and-launch |
| Data analysis | data-analyst | performance-optimization |

### Domain-Specific

| Domain | Key Agents | Key Skills |
|--------|-----------|-----------|
| Engineering | code-reviewer, test-engineer, architect | TDD, code-review, security |
| Design | design-systems-lead, product-designer | frontend-ui-engineering |
| Finance | financial-analyst, auditor | code-review, security |
| Marketing | content-strategist, growth-marketer | documentation, incremental-impl |

## Workflow: Full Feature Development

```
Phase 1: DEFINE
  Agent: product-manager
  Skill: spec-driven-development
  ├─ Write product specification
  ├─ Define acceptance criteria
  └─ Get alignment

Phase 2: PLAN
  Agent: project-manager
  Skill: planning-and-task-breakdown
  ├─ Break spec into tasks
  ├─ Order by dependencies
  └─ Create checkpoints

Phase 3: BUILD
  Agent: engineer
  Skill: incremental-implementation + context-engineering
  ├─ Implement task 1 (thin slice)
  ├─ Implement task 2
  └─ Land small, complete changes

Phase 4: VERIFY
  Agent: test-engineer
  Skill: test-driven-development + browser-testing-with-devtools
  ├─ Write tests first
  ├─ Test implementation
  └─ Run integration tests

Phase 5: REVIEW
  Agent: code-reviewer + security-auditor
  Skill: code-review-and-quality + security-and-hardening
  ├─ 5-axis code review
  ├─ Security analysis
  └─ Performance check

Phase 6: SHIP
  Agent: release-manager
  Skill: shipping-and-launch + git-workflow-and-versioning
  ├─ Pre-launch checklist
  ├─ Deploy to production
  └─ Monitor metrics

Phase 7: LEARN
  Agent: architect
  Skill: documentation-and-adrs
  ├─ Write decision record
  ├─ Update documentation
  └─ Share learnings
```

## Context Management

### Loading Skills Based on Phase

```bash
# Define phase
.cursor/rules/spec-driven-development.md
.cursor/rules/idea-refine.md

# Plan phase
.cursor/rules/planning-and-task-breakdown.md

# Build phase
.cursor/rules/incremental-implementation.md
.cursor/rules/context-engineering.md
.cursor/rules/frontend-ui-engineering.md

# Verify phase
.cursor/rules/test-driven-development.md
.cursor/rules/browser-testing-with-devtools.md
.cursor/rules/debugging-and-error-recovery.md

# Review phase
.cursor/rules/code-review-and-quality.md
.cursor/rules/security-and-hardening.md
.cursor/rules/performance-optimization.md

# Ship phase
.cursor/rules/git-workflow-and-versioning.md
.cursor/rules/ci-cd-and-automation.md
.cursor/rules/documentation-and-adrs.md
.cursor/rules/shipping-and-launch.md
```

### Smart Context Switching

1. **Load essentials always**:
   - test-driven-development.md
   - code-review-and-quality.md
   - incremental-implementation.md

2. **Add phase-specific** as you move through phases

3. **Remove when done** to keep context tight

4. **Reference explicitly**: "Follow the test-driven-development skill"

## Validation & Quality

### Lint Before Committing

```bash
./scripts/lint-agents.sh
```

Validates:
- ✓ YAML frontmatter (name, description, color)
- ✓ Required sections present
- ✓ Minimum content length (50+ words)
- ✓ Proper markdown structure

### Install & Test Locally

```bash
./scripts/install.sh --tool cursor
# Now in Cursor, test the agents and skills
```

## Advanced: Creating Custom Agent-Skill Combinations

### Example: Your Custom Workflow

```bash
# 1. Create a new agent
cat > agents/engineering/your-custom-agent.md << 'EOF'
---
name: Your Custom Agent
description: Specialized for your workflow
color: 0066FF
---

## Identity
[Your agent description]

## Core Mission
[What they do]

## Critical Rules
[Key constraints]
EOF

# 2. Create a new skill (or reference existing)
mkdir -p skills/your-custom-skills/your-custom-skill
cp skills/sde-practices/test-driven-development/SKILL.md \
   skills/your-custom-skills/your-custom-skill/SKILL.md

# 3. Validate
./scripts/lint-agents.sh agents/engineering/your-custom-agent.md

# 4. Install
./scripts/install.sh --tool cursor

# 5. Use in Claude
# @your-custom-agent Use your-custom-skill for this task
```

## Troubleshooting

### Issue: Skills not loading in Cursor

```bash
# Check installation
ls -la .cursor/rules/

# Re-install
./scripts/install.sh --tool cursor

# Restart Cursor (Cmd+Shift+P → Reload)
```

### Issue: Agent not found in chat

```bash
# Validate agent YAML
./scripts/lint-agents.sh agents/your-domain/agent-name.md

# Install agents
./scripts/install.sh --tool copilot

# Check agent format
cat agents/your-domain/agent-name.md | head -20
```

### Issue: Too many skills loaded (context exceeded)

```bash
# Remove non-essential skills from .cursor/rules/
ls .cursor/rules/*.md | wc -l  # How many loaded?

# Keep only 3-4 active
# Add more as you phase through your work
```

## Updating & Staying Current

### Pull Latest Changes

```bash
git pull origin main
./scripts/install.sh --tool cursor
./scripts/lint-agents.sh
```

### Contributing New Skills

1. Create `skills/your-category/your-skill/SKILL.md`
2. Include YAML frontmatter (name, description, color)
3. Write meaningful content (500+ words)
4. Run `./scripts/lint-agents.sh`
5. Submit PR

### Versioning

Check current version:
```bash
cat VERSION
```

See changelog:
```bash
cat CHANGELOG.md
```

## Best Practices

### ✅ Do

- **Tell Claude which agent to use**: "@code-reviewer Review this PR"
- **Tell Claude which skill to follow**: "Use test-driven-development for this"
- **Keep 3-4 skills active** in your editor at once
- **Add phase-specific skills** as you move through phases
- **Use validation**: `./scripts/lint-agents.sh` before committing
- **Install regularly**: `./scripts/install.sh --tool cursor` after updates

### ❌ Don't

- **Load all agents at once** — they're for switching roles
- **Load all 150+ skills at once** — you'll lose context focus
- **Treat skills as optional** — they encode proven practices
- **Modify SKILL.md files in place** — copy and customize
- **Skip validation** — lint before committing

## Quick Reference

### CLI Commands

```bash
# Install agents & skills
./scripts/install.sh --tool cursor

# Validate
./scripts/lint-agents.sh

# Localize to Chinese
powershell -File scripts/i18n/localize-agents-zh.ps1

# Convert formats (internal)
./scripts/convert.sh
```

### In Your Prompts

```
# Use an agent
@agent-name Task description

# Use a skill
Use skill-name for this implementation

# Use both
@code-reviewer Use code-review-and-quality to review this PR

# Phase-based workflow
@test-engineer Use test-driven-development to design tests
@engineer Use incremental-implementation to build
@code-reviewer Use code-review-and-quality to validate
```

## Resources

- **README.md** — Overview
- **AGENTS.md** — Full agent directory
- **SDE-PRACTICES.md** — SDE skills guide
- **the-longform-guide.md** — Deep engineering practices
- **the-security-guide.md** — Security-specific practices
- **CHANGELOG.md** — What's new

## Support

- Issues? Open an issue on GitHub
- Questions? Check the guides above
- Want to contribute? See CONTRIBUTING.md

---

**Remember**: Agents answer "who is working?" Skills answer "how do they work?" Use both for best results.

**Start simple**: Agent + 3 core skills (TDD, code-review, incremental-impl) covers 80% of workflows.
