---
name: how-it-works
description: >-
  Explains how claude-mem captures observations, when memory injection kicks
  in, where data lives, and how to verify it's running. TRIGGER when: user asks
  "how does claude-mem work?", "what is this thing doing?", "is claude-mem
  running?", "where does it store data?", or "explain the memory system".
origin: claude-mem
owner: surfingalien
---

# how-it-works

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## What claude-mem Does

Every Read, Edit, and Bash that Claude makes turns into a compressed **observation**. Observations are summarized at session end. Relevant ones are auto-injected into future prompts so the next session starts with context from the last one.

**No re-explaining the codebase. No re-discovering decisions. No starting cold.**

## When Memory Kicks In

- **Session 1** in a project: seeds memory. No injection yet.
- **Session 2+**: auto-injects relevant past observations at session start.
- **Cross-project**: memory is project-scoped. FinSurfing sessions don't bleed into my-claude-agents sessions.

Run `/learn-codebase` if you want to front-load the entire repo into memory in a single session (~5 minutes, optional but powerful for large repos).

## What Gets Captured

Every tool call generates an observation:

| Tool | What's Captured |
|------|----------------|
| Read | File path, key content summary |
| Edit / Write | File path, change summary, before/after |
| Bash | Command, output summary, exit code |
| grep / glob | Search query, result count |

Observations are compressed by Claude — not raw tool output. They're semantic summaries, not logs.

## Where Data Lives

Everything stays local:

```
~/.claude-mem/
├── claude-mem.db          # SQLite — all observations
├── chroma/                # Vector store — semantic search index
└── sessions/              # Per-session metadata
```

**No cloud sync. No external API calls for storage.** Your project history stays on your machine.

## How to Verify It's Running

```bash
# Check worker status
npm run worker:status --prefix ~/.claude/plugins/marketplaces/thedotmack

# Or via npx
npx claude-mem worker:status

# Check observation count
npx claude-mem stats

# Search for recent observations
npx claude-mem search "recent" --limit 5
```

If the worker isn't running, start it:

```bash
npx claude-mem worker:start
```

## How Memory Injection Works

At session start (SessionStart hook), the worker:

1. Loads the current project path
2. Queries the vector store for observations semantically related to the session context
3. Injects a compressed summary block into the Claude context window
4. You see this as a `<memory>` block at the start of the session (if verbose mode is on)

The injection is **additive** — it doesn't replace your CLAUDE.md or project context, it prepends it.

## Modes

claude-mem supports workflow modes via the `CLAUDE_MEM_MODE` environment variable:

```bash
# Standard coding mode (default)
CLAUDE_MEM_MODE=code claude

# Relaxed / chill mode
CLAUDE_MEM_MODE=code--chill claude

# Language-specific (e.g., for code comments in Spanish)
CLAUDE_MEM_MODE=code--es claude

# Email investigation mode (for ragtime)
CLAUDE_MEM_MODE=email-investigation claude
```

Modes are defined in `~/.claude/plugins/marketplaces/thedotmack/plugin/modes/`.

## Server Beta (v13+)

claude-mem v13 ships a **Server Beta** mode with PostgreSQL + Redis backing:

```bash
# Start the server
claude-mem server start

# Check status
claude-mem server status

# Stop
claude-mem server stop
```

Server Beta adds a `/v1` REST API for observations, sessions, memories, and search — useful for integrating claude-mem data into external tools (e.g., FinSurfing dashboard showing your own coding history).

**Default install still uses SQLite worker** — Server Beta is opt-in.

## Useful Commands

```bash
# Search past observations
npx claude-mem search "anthropic api"

# Generate a summary of recent work
npx claude-mem summary --since "7 days ago"

# Export observations for a project
npx claude-mem export --project /path/to/project --output history.json

# Clean old observations (> 90 days)
npx claude-mem clean --older-than 90d

# Check version
npx claude-mem --version

# Repair if something's broken
npx claude-mem repair
```

## Installation / Update

```bash
# Install
npx claude-mem install

# Update to latest
npx claude-mem install --update

# Repair broken installation
npx claude-mem repair
```

## Related Skills

- `mem-search` — Search observation history
- `knowledge-agent` — Build queryable brains from observation corpora
- `timeline-report` — Narrative project history from observations
- `weekly-digests` — Week-by-week chapter digest
