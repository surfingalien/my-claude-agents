---
name: mem-search
description: >-
  Search claude-mem's persistent cross-session memory database for past
  decisions, solutions, and patterns. TRIGGER when: user asks "did we already
  solve this?", "how did we do X last time?", "what did we decide about Y?",
  or needs context from previous sessions. Requires claude-mem installed.
origin: claude-mem
owner: surfingalien
---

# mem-search

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Search past work across all sessions. Find decisions, solutions, and patterns from previous Claude Code sessions before starting new work on the same problem.

**Never redo what's already been done. Never re-discover what's already been decided.**

## When to Use

Use when questions are about **previous sessions** — not the current conversation:

- "Did we already fix this?"
- "How did we solve X last time?"
- "What happened last week on the trading pipeline?"
- "What's our current approach to Anthropic API error handling?"
- "Did we ever try streaming for stock analysis?"

**Do not use** for questions answerable from the current context window. Search is for inter-session memory, not in-conversation retrieval.

## 3-Layer Workflow (Always Follow)

**Never fetch full details without filtering first. 10x token savings.**

### Layer 1: Broad Search

```bash
# Keyword search across all observations
claude-mem search "anthropic retry"
claude-mem search "railway deployment"
claude-mem search "stock agent streaming"
```

Returns: observation IDs, timestamps, session IDs, one-line summaries.

### Layer 2: Filter to Relevant

From Layer 1 results, identify the 3–5 most relevant observation IDs. Filter by:

- Recency (more recent = more likely to reflect current decisions)
- Session context (what project was active?)
- Observation type (code change vs discussion vs decision)

```bash
# Filter by session
claude-mem search "anthropic retry" --session <session-id>

# Filter by time range
claude-mem search "anthropic retry" --since "2026-04-01" --until "2026-05-01"

# Filter by observation type
claude-mem search "anthropic retry" --type code_change
```

### Layer 3: Fetch Details

Only for the filtered high-relevance observations:

```bash
# Fetch one observation in full
claude-mem observation get <observation-id>

# Fetch a session summary
claude-mem session summary <session-id>
```

## Search Patterns for Your Stack

### "How did we handle X before?"

```bash
claude-mem search "error handling anthropic"
claude-mem search "rate limit handling"
claude-mem search "retry backoff"
```

### "What's the current pattern for Y?"

```bash
claude-mem search "express middleware auth"
claude-mem search "postgresql connection pool"
claude-mem search "react state management"
```

### "Did we ever try Z?"

```bash
claude-mem search "streaming response"
claude-mem search "websocket trading"
claude-mem search "ai-trader integration"
```

### "What did we decide about W?"

```bash
claude-mem search "decided architecture"
claude-mem search "chose postgres over"
claude-mem search "switched from"
```

## Query Construction Tips

- Use **2–4 keywords** — too broad returns noise, too specific misses variants
- Include **both the thing and the context**: `"anthropic streaming finsurfing"` vs just `"streaming"`
- Try **past-tense verbs** for decisions: `"decided"`, `"switched"`, `"chose"`, `"fixed"`
- Try **present-tense** for current patterns: `"using"`, `"pattern"`, `"approach"`

## When Nothing is Found

If search returns empty or irrelevant results:

1. Broaden the query — fewer, more general keywords
2. Try synonyms — `"model call"` if `"anthropic api"` is empty
3. Try by file path — `"src/agents/stockAgent"`
4. Try by time range — `"since 2026-04-01"`
5. If still empty: the work hasn't been done in a recorded session — proceed from scratch

**Never block on an empty search.** Missing observations just mean "start fresh."

## Output Format

When reporting search results to the user:

```markdown
## Memory Search: "[query]"

### Found (N observations)

**[Date] — [Session summary]**
> [One-paragraph summary of what was done/decided]
> Key decision: [if applicable]
> Files involved: [if applicable]

**[Date] — [Session summary]**
> ...

### Recommendation
[Based on past work: re-use X, avoid Y, pick up from Z]
```

## Related Skills

- `knowledge-agent` — Build queryable AI brains from observation corpora (more powerful, more setup)
- `timeline-report` — Full chronological narrative of a project's history
- `weekly-digests` — Week-by-week narrative digest for longer project histories
