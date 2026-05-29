---
name: smart-explore
description: >-
  Token-optimized structural code search using tree-sitter AST parsing.
  Replaces the Glob → Grep → Read discovery cycle with smart_search,
  smart_outline, smart_unfold. TRIGGER when: exploring an unfamiliar module,
  finding where a function is defined, understanding file structure before
  editing. Requires smart_search MCP tool to be available.
origin: claude-mem
owner: surfingalien
---

# smart-explore

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Token-optimized structural code exploration using AST parsing.

**While this skill is active, use `smart_search` / `smart_outline` / `smart_unfold` as primary tools instead of Read, Grep, and Glob.**

**Core principle:** Index first, fetch on demand. Get a structural map before loading implementation details.

Before every file read, ask: "Do I need to see all of this, or can I get a structural overview first?" The answer is almost always: **get the map first.**

## When to Use

- Exploring an unfamiliar module or service before editing
- Finding where a function, class, or type is defined
- Understanding a file's structure without reading the full implementation
- Tracing a call graph across files
- Pre-flight for `pathfinder` on a large codebase

**Requires:** `smart_search` MCP tool configured and available in your session.

## Tool Reference

### `smart_search` — Discover files and symbols

```
smart_search(query="<topic>", path="./src")
```

- Walks directories, parses all code files, returns ranked symbols
- **Use this first** — replaces Glob + Grep + initial Read
- Returns: file paths, symbol names, line numbers, relevance scores

```
# Find anything related to Anthropic API calls
smart_search(query="anthropic client", path="./src")

# Find all route handlers
smart_search(query="express router", path="./src/routes")

# Find database query patterns
smart_search(query="postgres query", path="./src/db")
```

### `smart_outline` — Structural skeleton of one file

```
smart_outline(file_path="<file>")
```

- Returns: function signatures, class definitions, exports, imports
- **No implementation details** — just the structural shape
- Use before deciding whether to read the full file

```
# Get the shape of a service file before reading it
smart_outline(file_path="src/services/stockAnalysis.ts")

# Understand a large agent file without reading 400 lines
smart_outline(file_path="src/agents/stockAgent.ts")
```

### `smart_unfold` — Full source of one symbol

```
smart_unfold(file_path="<file>", symbol_name="<name>")
```

- Returns: full implementation of one function, class, or export
- **Only fetch what you need** — not the whole file
- Use after `smart_outline` identifies which symbol to read

```
# Read just the retry logic function
smart_unfold(file_path="src/lib/apiClient.ts", symbol_name="withRetry")

# Read just the stock analysis handler
smart_unfold(file_path="src/routes/stocks.ts", symbol_name="analyzeStock")
```

## Exploration Patterns

### Pattern 1: "What handles X?"

```
1. smart_search(query="<topic>", path="./src")
2. smart_outline(file_path=<top result>)
3. smart_unfold(file_path=<file>, symbol_name=<relevant symbol>)
```

### Pattern 2: "How does Y work?"

```
1. smart_search(query="<feature name>", path="./src")
2. smart_outline for each candidate file
3. smart_unfold the relevant entry point
4. Follow the call graph with targeted smart_unfold calls
```

### Pattern 3: "Where is Z defined?"

```
1. smart_search(query="<symbol name>", path="./")
2. Filter to definition site (vs import/usage sites)
3. smart_unfold the definition
```

### Pattern 4: Before editing a file

```
1. smart_outline(file_path=<target file>)  -- understand structure
2. smart_unfold for the specific function being changed
3. Read full file only if the change requires understanding all context
```

## Do NOT Use

- **Glob to discover files** — use `smart_search` instead
- **Grep to find symbols** — use `smart_search` instead
- **Read entire files over ~100 lines** — use `smart_outline` + `smart_unfold` instead
- **Run find commands for source discovery** — use `smart_search` instead

## FinSurfing Quick Reference

Useful queries for FinSurfing exploration:

```
# Find all Anthropic API integration points
smart_search(query="anthropic model messages", path="./src")

# Map the Express route surface
smart_search(query="router.get router.post", path="./src/routes")

# Find PostgreSQL query patterns
smart_search(query="pool.query db.query", path="./src")

# Locate React data-fetching hooks
smart_search(query="useEffect fetch axios", path="./client/src")

# Find AI-Trader integration hooks
smart_search(query="trading signal portfolio", path="./src")
```

## Fallback

If `smart_search` is not available (MCP tool not configured):

1. Use `learn-codebase` for full priming
2. Use standard `Grep` + `Read` with explicit file paths
3. Add smart_search MCP server to your Claude Code config — see `mcp-builder` skill

## Related Skills

- `learn-codebase` — Full file-by-file priming (more thorough, more tokens)
- `pathfinder` — Architecture mapping (uses smart-explore for discovery phase)
- `mcp-builder` — Set up the smart_search MCP server if not yet configured
