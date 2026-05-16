# 🏆 SDE Practices: Production-Grade Engineering Skills

This guide covers **23 production-grade software development practices** from the world's top engineering teams, integrated into your Claude agents workflow.

These aren't generic tips — they're **proven workflows** that senior engineers at Google, Anthropic, Vercel, and other tier-1 companies use daily. Each practice encodes a phase of the software development lifecycle with concrete steps, verification points, and anti-patterns to avoid.

## Overview

### The 7 Phases of Production Software

```
Define → Plan → Build → Verify → Review → Ship → Learn
```

Every skill maps to one of these phases. Together, they form your **complete engineering playbook**.

## Quick Start

### 1. Load the Essentials (3 Skills)

Always keep these active when using Claude for engineering:

```bash
# In your .claude/agents/ or .cursor/rules/
test-driven-development.md
code-review-and-quality.md
incremental-implementation.md
```

Why these three?
- **TDD** ensures proof (tests before code)
- **Code Review** ensures quality (multi-axis evaluation)
- **Incremental** ensures safety (small, reviewable changes)

### 2. Use Phase-Specific Skills On Demand

| Phase | Skills | Use When |
|-------|--------|----------|
| **Define** | spec-driven-development, idea-refine | Starting a feature or exploring ideas |
| **Plan** | planning-and-task-breakdown | Breaking work into implementable chunks |
| **Build** | context-engineering, frontend-ui-engineering, api-and-interface-design, code-simplification | Writing code for any domain |
| **Verify** | browser-testing-with-devtools, debugging-and-error-recovery, doubt-driven-development, source-driven-development | Tests fail or behavior breaks |
| **Review** | security-and-hardening, performance-optimization, deprecation-and-migration | Before merging any change |
| **Ship** | git-workflow-and-versioning, ci-cd-and-automation, documentation-and-adrs, shipping-and-launch | Deploying to production |

### 3. Run Linting & Validation

```bash
./scripts/lint-agents.sh
./scripts/install.sh --tool cursor
```

## 23 Skills Reference

### Define Phase: 2 Skills

#### idea-refine
**When**: You have a rough idea but need to explore options

Refine ideas through structured divergent and convergent thinking. Move from vague concepts to concrete proposals.

- Divergent thinking (explore options)
- Convergent thinking (narrow to best)
- Validate with stakeholders
- Document the decision

#### spec-driven-development
**When**: Starting a new project or major feature

Write structured specifications before writing code.

- High-level vision
- PRD with six core sections (commands, testing, project structure, code style, git workflow, boundaries)
- Gated workflow: Specify → Plan → Tasks → Implement
- Living document maintenance

### Plan Phase: 1 Skill

#### planning-and-task-breakdown
**When**: You have a spec and need to split work into tasks

Decompose work into small, verifiable tasks with explicit acceptance criteria.

- Plan-mode-first workflow
- Task sizing (break until atomic)
- Dependency ordering
- Checkpoint design
- Acceptance criteria clarity

### Build Phase: 5 Skills

#### incremental-implementation
**When**: Implementing any feature touching > 1 file

Build in thin vertical slices — implement one piece, test, verify, expand.

- Feature flags
- Safe defaults
- Rollback-friendly changes
- Land small, complete increments
- Test each slice before expanding

#### context-engineering
**When**: Agent output quality degrades

Feed agents the right information at the right time.

- Rules files (CLAUDE.md, .cursorrules)
- Context packing strategies
- Selective inclusion
- Hierarchical summaries
- MCP integrations
- Avoid context starvation and overload

#### frontend-ui-engineering
**When**: Building production-quality UIs

Production-grade user interface design and implementation.

- Component architecture
- Design system adherence
- State management patterns
- Responsive design
- Accessibility (WCAG 2.1 AA)
- Avoid "AI-generated UI" aesthetic

#### api-and-interface-design
**When**: Designing APIs, module boundaries, or public interfaces

Design stable, well-documented interfaces.

- REST and GraphQL patterns
- Error semantics
- Versioning strategy
- Boundary design
- Input validation at edges
- Backward compatibility

#### code-simplification
**When**: Code is becoming complex

Reduce complexity while maintaining functionality.

- Identify complexity hotspots
- Extract reusable abstractions
- Remove duplication
- Clarify intent through naming
- Decompose large functions
- Test during refactoring

### Verify Phase: 5 Skills

#### test-driven-development
**When**: Implementing any logic or fixing any bug (i.e., always)

Write tests before code.

- Prove-It pattern (reproduce bugs with failing tests)
- Test hierarchy: unit → integration → e2e
- Test sizing
- When to use each level
- Never ship without verification

#### browser-testing-with-devtools
**When**: Building or debugging browser applications

Use Chrome DevTools to give your agent eyes.

- DOM inspection
- Console log analysis
- Network trace review
- Performance profiling
- Screenshot comparison
- Automated UI testing

#### debugging-and-error-recovery
**When**: Tests fail or behavior breaks

Systematic debugging with structured triage.

- Stop-the-line rule
- Five-step triage: reproduce → localize → reduce → fix → guard
- Safe fallbacks
- Rollback strategies
- When to instrument vs. remove debug code

#### doubt-driven-development
**When**: You're unsure about an implementation

Test your assumptions rigorously.

- Identify points of doubt
- Write tests that expose the doubt
- Prove the happy path AND edge cases
- Document assumptions
- Verify with integration tests

#### source-driven-development
**When**: Understanding existing code

Navigate and comprehend codebases systematically.

- Start with high-level architecture
- Trace key execution paths
- Identify critical sections
- Extract mental models
- Document what you learned

### Review Phase: 4 Skills

#### code-review-and-quality
**When**: Before merging any change (i.e., always)

Multi-dimensional code review with quality gates.

- Five-axis review: correctness, readability, architecture, security, performance
- Dependency discipline
- Multi-model review patterns
- "Would a staff engineer approve this?" standard
- Concrete examples of what to look for

#### security-and-hardening
**When**: Handling user input, authentication, data, or external integrations

Security-first development practices.

- OWASP Top 10 prevention
- Input validation
- Output encoding
- Authentication/authorization patterns
- Secrets management
- Dependency auditing
- Three-tier boundary system (Always/Ask First/Never)

#### performance-optimization
**When**: Performance requirements exist or you suspect regressions

Measure before optimizing.

- Core Web Vitals
- Performance budgets
- Profiling workflow
- Common anti-patterns: N+1 queries, unbounded loops, layout thrashing
- Bundle analysis
- Optimize only what measurements prove matters

#### deprecation-and-migration
**When**: Removing or changing old code

Safe, tracked removal of deprecated features.

- Deprecation lifecycle
- Migration planning
- Gradual rollout
- Monitoring deprecated usage
- Timeline for removal
- Impact communication

### Ship Phase: 5 Skills

#### git-workflow-and-versioning
**When**: Making any code change (i.e., always)

Git as your safety net.

- Atomic commits
- Descriptive messages
- Branch strategy
- Worktrees for parallel work
- "Commit as save point" pattern
- Never mix formatting with behavior changes

#### ci-cd-and-automation
**When**: Setting up or modifying build pipelines

Automate quality gates.

- Pipeline design
- Test/lint/typecheck/build enforcement
- Failure feedback loops
- Deployment strategies
- Environment management

#### documentation-and-adrs
**When**: Making architectural decisions or shipping features

Document decisions, not just code.

- Architecture Decision Records (ADRs)
- API documentation
- Inline documentation standards
- README patterns
- Changelog maintenance
- Document the **why** (context future engineers need)

#### shipping-and-launch
**When**: Preparing to deploy to production

Ship with confidence.

- Pre-launch checklists
- Feature flag management
- Monitoring setup
- Rollback procedures
- Staged rollouts
- Post-launch verification

#### interview-me
**When**: Preparing for technical interviews

Interview preparation and mock interview guidance.

- System design interview patterns
- Coding problem approaches
- Behavioral questions
- Storytelling frameworks
- Technical communication
- Practice strategies

### Meta: 1 Skill

#### using-agent-skills
**When**: Learning how to use this entire skill pack effectively

How to use the SDE practices pack.

- Skill selection strategy
- Context management
- Verification patterns
- When to load/unload skills
- Common mistakes and solutions

## Installation & Setup

### For Cursor

```bash
# Copy all skills to your project
cp -r skills/sde-practices/* .cursor/rules/

# Or copy just the essentials first
cp skills/sde-practices/test-driven-development/.cursor/rules/test-driven-development.md .cursor/rules/
cp skills/sde-practices/code-review-and-quality/.cursor/rules/code-review-and-quality.md .cursor/rules/
cp skills/sde-practices/incremental-implementation/.cursor/rules/incremental-implementation.md .cursor/rules/
```

### For Claude Code

```bash
# Reference in your CLAUDE.md
Import skills from skills/sde-practices/
```

### For Copilot / GitHub

```bash
./scripts/install.sh --tool copilot
```

### For Windsurf, Aider, QWen, etc.

```bash
./scripts/install.sh --tool <tool-name>
```

## Skill Categories by Use Case

### New Product MVP

1. **Define**: spec-driven-development
2. **Plan**: planning-and-task-breakdown
3. **Build**: incremental-implementation, context-engineering, frontend-ui-engineering (if UI), api-and-interface-design
4. **Verify**: test-driven-development, browser-testing-with-devtools
5. **Review**: code-review-and-quality, security-and-hardening
6. **Ship**: git-workflow-and-versioning, documentation-and-adrs, shipping-and-launch

### Bug Fix

1. **Verify**: debugging-and-error-recovery, test-driven-development (write test first)
2. **Build**: incremental-implementation
3. **Review**: code-review-and-quality
4. **Ship**: git-workflow-and-versioning

### Performance Crisis

1. **Verify**: performance-optimization, browser-testing-with-devtools
2. **Build**: code-simplification, incremental-implementation
3. **Review**: code-review-and-quality
4. **Ship**: git-workflow-and-versioning, shipping-and-launch

### Security Audit

1. **Review**: security-and-hardening
2. **Verify**: test-driven-development (test security assumptions)
3. **Ship**: documentation-and-adrs (ADRs for security decisions)

### Legacy Code Maintenance

1. **Verify**: source-driven-development (understand existing code), doubt-driven-development
2. **Build**: code-simplification, incremental-implementation
3. **Review**: code-review-and-quality
4. **Ship**: git-workflow-and-versioning, documentation-and-adrs

## Best Practices

### ✅ Do

- **Load 2-3 core skills** to start, add others as needed
- **Reference skills explicitly** in your prompts: "Follow the TDD rules for this"
- **Read the SKILL.md files** before using them
- **Use skills iteratively** — return to them as context shifts
- **Remove skills when done** to keep context tight
- **Test all assumptions** — never assume something works

### ❌ Don't

- **Load all 23 skills at once** — you'll lose context focus
- **Skip verification steps** — skills enforce "Prove It"
- **Treat skills as optional** — they're workflows, not suggestions
- **Modify SKILL.md files in place** — copy and customize
- **Use skills you don't understand** — read the file first

## Integration with My Agents

These SDE practices **complement your existing agents**:

- **Agents** define *who* is working (code-reviewer, test-engineer, security-auditor)
- **Skills** define *how* work gets done (TDD, code review, security)

Load both:

```
@code-reviewer Review this PR using code-review-and-quality
@test-engineer Plan tests using test-driven-development
@security-auditor Audit using security-and-hardening
```

## Validation & Quality

### Lint Your Skills

```bash
./scripts/lint-agents.sh
```

Checks:
- YAML frontmatter (name, description, color)
- Recommended sections present
- Meaningful content (50+ words)
- Proper structure

### Install Validated Skills

```bash
./scripts/install.sh --tool cursor --parallel
```

## Further Reading

- **README.md** — Overview and quick start
- **AGENTS.md** — Agent personas and how to use them
- **the-longform-guide.md** — Deep dive into practices
- **the-security-guide.md** — Security-specific practices
- **CHANGELOG.md** — What's new in each version

## Contributing

To add a new SDE practice skill:

1. Create a directory in `skills/sde-practices/YOUR-SKILL-NAME/`
2. Write `SKILL.md` with YAML frontmatter (name, description, color)
3. Include sections: Identity, Core Mission, Critical Rules, Workflows, Verification
4. Run `./scripts/lint-agents.sh YOUR-SKILL-NAME/SKILL.md`
5. Run `./scripts/install.sh --tool cursor` to test locally
6. Submit PR with your skill

## License

MIT — use these practices in your projects, teams, and tools.

---

**Remember**: These skills are tools, not dogma. Use what works for your context, question what doesn't, and always prioritize shipping valuable code safely.

**Start with TDD**: If you only use one skill, make it `test-driven-development`. Everything else builds from proof.
