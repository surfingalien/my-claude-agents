---
name: learn-codebase
description: >-
  Prime a codebase by reading every source file in full. Builds deep structural
  understanding before starting work on unfamiliar repos. TRIGGER when: user
  says "learn the codebase", "read the codebase", "prime", "get up to speed",
  "onboard me", or when joining a new project for the first time.
origin: claude-mem
owner: surfingalien
---

# learn-codebase

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Systematically read **every source file in full** to build a comprehensive understanding of the codebase before starting any implementation work.

This is an upfront token investment that pays back across the entire session and future sessions (via claude-mem memory injection if installed).

## When to Use

- First time opening a new project with Claude Code
- Joining a new repo or team
- Before running `pathfinder` on a large codebase
- When context was lost and re-priming is faster than re-discovering
- User says: "learn the codebase", "prime", "get up to speed", "read everything"

**Do not use** when you already have the codebase in context or when the task is a clearly scoped single-file change.

## Execution

### Step 1: Inventory

Before reading anything, map the terrain:

```bash
# Project structure
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.py" \
  -o -name "*.go" -o -name "*.rs" -o -name "*.md" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" ! -path "*/build/*" \
  | sort > source-inventory.txt

wc -l source-inventory.txt  # total files
```

Categorize before reading:
- **Config**: `package.json`, `tsconfig.json`, `.env.example`, `railway.toml`
- **Entry points**: `main.ts`, `index.ts`, `app.ts`, `server.ts`
- **Routes/Handlers**: `src/routes/`, `src/api/`, `src/handlers/`
- **Business logic**: `src/services/`, `src/agents/`, `src/lib/`
- **Data layer**: `src/models/`, `migrations/`, `src/db/`
- **Tests**: `**/*.test.ts`, `**/*.spec.ts`
- **Docs**: `README.md`, `CLAUDE.md`, `docs/`

### Step 2: Read in Priority Order

Read in this sequence — highest signal to lowest:

1. **CLAUDE.md** — project-specific instructions for Claude
2. **README.md** — overview and setup
3. **package.json / pyproject.toml** — dependencies, scripts, entry points
4. **Entry point files** — where execution starts
5. **Route/API files** — what the system exposes
6. **Service/agent files** — business logic
7. **Data/model files** — schemas and DB patterns
8. **Config files** — environment, build, deployment
9. **Tests** — what behavior is already verified
10. **Remaining source files** — in directory order

### Step 3: Chunk Large Files

For files over ~100 lines, page through with offset/limit:

```
Read(file, offset=1, limit=500)
Read(file, offset=501, limit=500)
...
```

Never skip a file because it's large. Large files are often the most important.

### Step 4: Build a Mental Map

While reading, maintain a running summary:

```markdown
## Codebase Map (running)

### Architecture
- [Pattern: REST API / tRPC / GraphQL / etc.]
- [Auth: JWT / session / API key]
- [DB: PostgreSQL / SQLite / etc., ORM or raw]

### Key Files
- `src/server.ts` — Express app setup, middleware registration
- `src/routes/stocks.ts` — Stock intelligence endpoints
- `src/agents/stockAgent.ts` — Anthropic API integration
- `src/db/index.ts` — Database connection, query helpers

### Patterns to Follow
- [Naming conventions]
- [Error handling pattern]
- [Import style]
- [Test patterns]

### Red Flags / Technical Debt
- [Anything worth noting for make-plan or pathfinder]
```

### Step 5: Deliver the Summary

After reading everything, produce:

```markdown
# Codebase Summary: [Project Name]

## Architecture Overview
[2-3 paragraphs: what it is, how it's structured, tech choices]

## Entry Points
[List with one-line purpose each]

## Key Systems
[Each major subsystem with responsible files]

## Data Model
[Key entities and relationships]

## External Integrations
[APIs, services, MCP servers the project connects to]

## Development Patterns
[Conventions Claude should follow when coding here]

## Open Questions / Technical Debt
[Things worth addressing — link to pathfinder or oh-my-issues if relevant]

## Suggested Next Steps
[What to do now: implement feature X, run pathfinder, fix issue Y]
```

## FinSurfing Context

When priming FinSurfing (React + Vite + Express + PostgreSQL + Anthropic API on Railway):

Priority read order:
1. `CLAUDE.md` → `README.md`
2. `server/src/server.ts` or `src/app.ts` — Express setup
3. `client/src/main.tsx` or `src/App.tsx` — React entry
4. All route files — understand the API surface
5. Anthropic integration files — how Claude API is called
6. DB migration files — understand the data model evolution
7. `railway.toml` or `.env.example` — deployment config

Watch for:
- How API keys are injected (Railway env vars vs hardcoded)
- Whether AI-Trader integration is present and how it's wired
- PostgreSQL connection pooling setup
- React state management pattern (Zustand, Context, or none)

## Related Skills

- `pathfinder` — Use after learn-codebase to map architecture and find duplication
- `codebase-onboarding` — Alternative that generates a structured CLAUDE.md
- `smart-explore` — Faster AST-based exploration for targeted discovery (use instead of learn-codebase when you only need specific areas)
- `make-plan` — Use after priming to plan work on the codebase
