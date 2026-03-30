# my-claude-agents

> Production-ready Claude Code agents, skills, commands, rules & hooks.
> Built from [everything-claude-code](https://github.com/affaan-m/everything-claude-code) v1.9.0.

## What's inside

| Component | Count | Description |
|-----------|-------|-------------|
| **Agents** | 30 | Specialized subagents for delegation |
| **Skills** | 135 | Workflow definitions & domain knowledge |
| **Commands** | 60 | Slash commands (`/tdd`, `/plan`, `/e2e`, ...) |
| **Rules** | 77 | Always-follow guidelines (13 languages) |
| **Hooks** | — | Session persistence & automation triggers |
| **MCP Configs** | 14 | External service integrations |

## Agents

| Agent | Purpose |
|-------|---------|
| `planner` | Implementation planning for complex features |
| `architect` | System design and scalability decisions |
| `tdd-guide` | Test-driven development workflow |
| `code-reviewer` | Code quality and maintainability |
| `security-reviewer` | Vulnerability detection |
| `build-error-resolver` | Fix build/type errors |
| `e2e-runner` | End-to-end Playwright testing |
| `refactor-cleaner` | Dead code cleanup |
| `typescript-reviewer` | TypeScript/JS code review |
| `python-reviewer` | Python code review |
| `rust-reviewer` | Rust code review |
| `go-reviewer` | Go code review |
| `java-reviewer` | Java/Spring Boot review |
| `kotlin-reviewer` | Kotlin/Android/KMP review |
| `cpp-reviewer` | C++ code review |
| `database-reviewer` | PostgreSQL/Supabase specialist |
| `performance-optimizer` | Performance analysis |
| `chief-of-staff` | Multi-channel communication triage |
| `loop-operator` | Autonomous loop execution |
| `healthcare-reviewer` | Healthcare/PHI compliance |

## Quick Start (Claude Code)

```bash
git clone https://github.com/surfingalien/my-claude-agents.git
cd my-claude-agents
node scripts/install-apply.js --profile full --target claude
```

Then inside any project with Claude Code, use slash commands:

```
/plan        # Plan a new feature
/tdd         # Test-driven development
/code-review # Review your code
/e2e         # Generate E2E tests
/build-fix   # Fix build errors
/learn       # Extract patterns from sessions
```

## Core Principles

1. **Agent-First** — Delegate to specialized agents for domain tasks
2. **Test-Driven** — Write tests before implementation, 80%+ coverage required
3. **Security-First** — Validate all inputs, never hardcode secrets
4. **Plan Before Execute** — Plan complex features before writing code

## Skills Highlights

- **Framework/Language**: Django, Kotlin, Rust, Go, Java/Spring, Laravel, React, Next.js
- **Testing**: TDD workflow, E2E, eval harness, verification loops
- **Security**: Security review, OWASP scanning, framework-specific hardening
- **Agentic**: Autonomous loops, LLM pipelines, agent harness construction
- **Database**: PostgreSQL patterns, migrations, JPA
- **DevOps**: Docker, deployment patterns
- **Apple**: SwiftUI, Swift concurrency, on-device models

## License

MIT — see [LICENSE](./LICENSE)

---

*Powered by [everything-claude-code](https://github.com/affaan-m/everything-claude-code)*
