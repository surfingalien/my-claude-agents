# my-claude-agents

> Production-ready Claude Code agents, skills, commands, rules & hooks.

## What's inside

| Component | Count | Description |
|-----------|-------|-------------|
| **Agents** | 56 | Specialized subagents for delegation |
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
| `cs-brand-guardian` | Brand identity development and consistency protection |
| `cs-image-prompt-engineer` | AI photography prompt engineering for all major platforms |
| `cs-inclusive-visuals-specialist` | Counter-bias prompt engineering for authentic representation |
| `cs-ui-designer` | Design systems, component libraries, and WCAG AA accessibility |
| `cs-ux-architect` | CSS architecture foundations, layout systems, and theme infrastructure |
| `cs-ux-researcher` | User research studies, personas, usability testing, and behavioral insights |
| `cs-visual-storyteller` | Visual narratives, storyboards, multimedia content, and cross-platform visual strategy |
| `cs-whimsy-injector` | Micro-interactions, playful microcopy, Easter eggs, and accessible gamification |
| `cs-bookkeeper-controller` | Month-end close, account reconciliations, GAAP compliance, and internal controls |
| `cs-financial-analyst` | DCF valuation, three-statement models, comparable analysis, and scenario planning |
| `cs-fpa-analyst` | Annual operating plans, rolling forecasts, variance analysis, and monthly business reviews |
| `cs-investment-researcher` | Investment thesis construction, due diligence, valuation, and portfolio monitoring |
| `cs-tax-strategist` | Tax optimization, entity structuring, equity comp planning, and multi-jurisdictional compliance |
| `cs-anthropologist` | Culturally coherent society design — kinship systems, rituals, exchange mechanisms, cosmologies |
| `cs-geographer` | Physically coherent world geography — climate systems, hydrology, biomes, settlement patterns |
| `cs-historian` | Historical authenticity, anachronism detection, material culture, and period-accurate enrichment |
| `cs-narratologist` | Story structure analysis, character arc assessment, genre conventions, and narrative debt tracking |
| `cs-psychologist` | Psychological profiles, interpersonal dynamics, trauma response modeling, and character credibility |
| `cs-macos-metal-engineer` | Metal rendering pipelines for macOS and Vision Pro — instanced drawing, GPU compute, 90fps spatial rendering |
| `cs-terminal-specialist` | SwiftTerm terminal emulation, SSH I/O bridging, ANSI rendering, and iOS/macOS terminal app development |
| `cs-visionos-spatial-engineer` | Native visionOS 26 spatial computing — Liquid Glass design, volumetric SwiftUI, and RealityKit integration |
| `cs-xr-cockpit-specialist` | Immersive cockpit environments for XR — A-Frame/Three.js seated interfaces with ergonomic control design |
| `cs-xr-immersive-developer` | Browser-based WebXR AR/VR across Meta Quest, Vision Pro, HoloLens, and mobile with graceful fallback |

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
