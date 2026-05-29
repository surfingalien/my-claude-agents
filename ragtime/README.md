# ragtime

Batch Document Intelligence Processor for claude-mem.

Processes a corpus of documents through isolated Claude Code sessions. Each file gets a fresh session — claude-mem's context injection hook carries observations forward, not the conversation. Observations compound across the entire corpus without ballooning a single context window.

**Original:** [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) (Apache 2.0)
**Adapted for:** financial filings, earnings transcripts, market news batches, trading research corpora

---

## Requirements

- [Bun](https://bun.sh) runtime
- claude-mem installed and worker running (`npx claude-mem worker:start`)
- `@anthropic-ai/claude-agent-sdk` package

```bash
# Install Bun
curl -fsSL https://bun.sh/install | bash

# Install claude-mem (if not already)
npx claude-mem install

# Install dependencies
cd ragtime
bun install
```

---

## Quick Start

```bash
# Create a corpus directory and drop in .md files
mkdir -p ragtime/datasets/earnings-q2
cp ~/downloads/aapl-10q-q2.md ragtime/datasets/earnings-q2/
cp ~/downloads/msft-10q-q2.md ragtime/datasets/earnings-q2/

# Run the batch
RAGTIME_CORPUS_PATH=ragtime/datasets/earnings-q2 \
RAGTIME_MODE=financial-filing \
RAGTIME_PROJECT_NAME=earnings-q2-2026 \
bun ragtime/ragtime.ts

# Query the results
npx claude-mem search "guidance revenue"
npx claude-mem search "risk factors"
```

---

## Configuration

All settings via environment variables:

| Variable | Default | Description |
|---|---|---|
| `RAGTIME_CORPUS_PATH` | `./ragtime/datasets/corpus` | Folder containing `.md` or `.txt` files to process |
| `RAGTIME_MODE` | `email-investigation` | claude-mem observation mode (see Modes below) |
| `RAGTIME_PROJECT_NAME` | `ragtime-batch` | Project name for grouping observations |
| `CLAUDE_MEM_WORKER_PORT` | `37777` | claude-mem worker port |
| `RAGTIME_TRANSCRIPT_MAX_AGE` | `24` | Max age of transcripts to keep (hours) |
| `RAGTIME_FILE_LIMIT` | `0` | Limit files processed (0 = all) — use for testing |
| `RAGTIME_SESSION_DELAY` | `2000` | Delay between sessions in ms |
| `RAGTIME_PROMPT` | _(mode default)_ | Override analysis prompt. Use `{file}` as placeholder. |

---

## Modes

### Built-in claude-mem modes

| `RAGTIME_MODE` | Best For | Observation Types |
|---|---|---|
| `email-investigation` | Email corpora, communication analysis | entity, relationship, timeline-event, evidence, anomaly, conclusion |
| `code` | Code repository batch analysis | bugfix, feature, refactor, change, discovery, decision |
| `code--chill` | Large code repos (selective recording only) | Same as code, less noise |
| `meme-tokens` | Token activity log analysis | pump-detected, dump-detected, signal-change, token-profile, market-condition |

### FinSurfing financial modes (custom prompts built-in)

| `RAGTIME_MODE` | Best For |
|---|---|
| `financial-filing` | SEC 10-K/10-Q filings, annual reports |
| `market-news` | Financial news articles, analyst reports |
| `earnings-call` | Earnings call transcripts |

These use custom analysis prompts built into ragtime — no additional config needed.

---

## Corpus Format

Put `.md` or `.txt` files in a directory. Files are processed in numeric order (if numbered) or alphabetical order.

```
ragtime/datasets/
  earnings-q2/
    0001-aapl-10q.md
    0002-msft-10q.md
    0003-googl-10q.md
    ...
  market-news/
    2026-05-01-fed-rate.md
    2026-05-02-cpi-data.md
    ...
```

Each file should contain one document. For large documents, consider splitting by section.

---

## FinSurfing Use Cases

### 1. Batch process SEC filings

```bash
# Organize filings
mkdir -p ragtime/datasets/10q-q1-2026
# Drop in converted .md files from SEC EDGAR

RAGTIME_CORPUS_PATH=ragtime/datasets/10q-q1-2026 \
RAGTIME_MODE=financial-filing \
RAGTIME_PROJECT_NAME=10q-q1-2026 \
bun ragtime/ragtime.ts

# Query for guidance patterns
npx claude-mem search "full year guidance raised"
npx claude-mem search "supply chain risk"
```

### 2. Batch process earnings transcripts

```bash
mkdir -p ragtime/datasets/earnings-q1-2026
# Drop in earnings call transcripts as .md

RAGTIME_CORPUS_PATH=ragtime/datasets/earnings-q1-2026 \
RAGTIME_MODE=earnings-call \
RAGTIME_PROJECT_NAME=earnings-q1-2026 \
bun ragtime/ragtime.ts

# Query for management tone signals
npx claude-mem search "cautious tone macro"
npx claude-mem search "beat estimates guidance"
```

### 3. Batch process market news

```bash
mkdir -p ragtime/datasets/news-may-2026

RAGTIME_CORPUS_PATH=ragtime/datasets/news-may-2026 \
RAGTIME_MODE=market-news \
RAGTIME_PROJECT_NAME=news-may-2026 \
bun ragtime/ragtime.ts

# Query for sector themes
npx claude-mem search "AI infrastructure spending"
npx claude-mem search "rate cut expectations"
```

### 4. Test with a small batch first

```bash
RAGTIME_FILE_LIMIT=3 \
RAGTIME_CORPUS_PATH=ragtime/datasets/earnings-q1-2026 \
RAGTIME_MODE=earnings-call \
bun ragtime/ragtime.ts
```

---

## How It Works

1. **Preflight** — verifies claude-mem worker is running, sets `CLAUDE_MEM_MODE`
2. **For each file:**
   - Starts a fresh Claude Code session (no cross-file conversation continuation)
   - Claude reads the file and analyzes it using the mode-specific prompt
   - claude-mem's context injection hook injects relevant past observations from prior files
   - Worker compresses and stores new observations to `~/.claude-mem/`
3. **Between files** — waits for worker queue to drain before starting next session
4. **Periodic cleanup** — removes old transcripts every 10 files and at completion

Observations accumulate in `~/.claude-mem/claude-mem.db` and are searchable with `npx claude-mem search`.

---

## Querying Results After a Batch

```bash
# Search observations
npx claude-mem search "revenue beat"
npx claude-mem search "management guidance"
npx claude-mem search "risk factor new"

# Get a summary of recent work
npx claude-mem summary --since "7 days ago"

# Build a knowledge agent brain from the batch
npx claude-mem corpus build \
  --name "q1-earnings" \
  --filter "guidance OR beat OR miss OR revenue" \
  --output ~/.claude-mem/corpora/q1-earnings.json

# Export full observation set
npx claude-mem export \
  --project ragtime-batch \
  --output ragtime-results.json
```

---

## package.json

```json
{
  "name": "@surfingalien/ragtime",
  "version": "1.0.0",
  "description": "Batch document intelligence processor for claude-mem",
  "scripts": {
    "start": "bun ragtime.ts",
    "financial": "RAGTIME_MODE=financial-filing bun ragtime.ts",
    "earnings": "RAGTIME_MODE=earnings-call bun ragtime.ts",
    "news": "RAGTIME_MODE=market-news bun ragtime.ts",
    "test": "RAGTIME_FILE_LIMIT=2 bun ragtime.ts"
  },
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "latest"
  }
}
```

---

## License

Apache License 2.0 — same as upstream claude-mem/ragtime.
