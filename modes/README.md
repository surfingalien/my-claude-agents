# Claude-Mem Workflow Modes

Claude Code behavioral presets for claude-mem's `CLAUDE_MEM_MODE` environment variable. Each mode customizes how observations are captured, categorized, and compressed during sessions.

Source: [thedotmack/claude-mem](https://github.com/thedotmack/claude-mem) (Apache 2.0)

## Usage

```bash
# Set before starting a Claude Code session
CLAUDE_MEM_MODE=<mode-name> claude

# Or export in your shell profile
export CLAUDE_MEM_MODE=code--chill
```

Modes are installed to `~/.claude/plugins/marketplaces/thedotmack/plugin/modes/` by claude-mem. These files are kept here as reference and for re-deployment.

---

## Available Modes

### 🛠️ Code Modes

| Mode | File | Description |
|------|------|-------------|
| Standard | `code.json` | Default software development mode. Full observation taxonomy: bugfix, feature, refactor, change, discovery, decision. Records everything of durable signal. |
| Chill | `code--chill.json` | Selective recording — only captures what would be painful to rediscover. Skips obvious implementations and incremental steps. Best for exploratory sessions. |

### 🌍 Language-Localized Code Modes

Same as `code.json` but with observation prompts tuned for code written with non-English context. Use when working in codebases with comments, variable names, or docs in another language.

| Code | File | Language |
|------|------|----------|
| `ar` | `code--ar.json` | Arabic |
| `bn` | `code--bn.json` | Bengali |
| `cs` | `code--cs.json` | Czech |
| `da` | `code--da.json` | Danish |
| `de` | `code--de.json` | German |
| `el` | `code--el.json` | Greek |
| `es` | `code--es.json` | Spanish |
| `fi` | `code--fi.json` | Finnish |
| `fr` | `code--fr.json` | French |
| `he` | `code--he.json` | Hebrew |
| `hi` | `code--hi.json` | Hindi |
| `hu` | `code--hu.json` | Hungarian |
| `id` | `code--id.json` | Indonesian |
| `it` | `code--it.json` | Italian |
| `ja` | `code--ja.json` | Japanese |
| `ko` | `code--ko.json` | Korean |
| `nl` | `code--nl.json` | Dutch |
| `no` | `code--no.json` | Norwegian |
| `pl` | `code--pl.json` | Polish |
| `pt-br` | `code--pt-br.json` | Portuguese (Brazil) |
| `ro` | `code--ro.json` | Romanian |
| `ru` | `code--ru.json` | Russian |
| `sv` | `code--sv.json` | Swedish |
| `th` | `code--th.json` | Thai |
| `tr` | `code--tr.json` | Turkish |
| `uk` | `code--uk.json` | Ukrainian |
| `ur` | `code--ur.json` | Urdu |
| `vi` | `code--vi.json` | Vietnamese |
| `zh` | `code--zh.json` | Chinese (Simplified) — **built into claude-mem by default** |

### 🔍 Specialist Modes

| Mode | File | Description | Observation Types |
|------|------|-------------|-------------------|
| **Email Investigation** | `email-investigation.json` | RAGTIME-style entity/relationship/timeline extraction from email corpora. Used by the `ragtime` batch processor. | entity, relationship, timeline-event, evidence, anomaly, conclusion |
| **Law Study** | `law-study.json` | Legal study and exam prep. Captures case holdings, issue patterns, professor frameworks, doctrine rules, argument structures, cross-case connections. | case-holding, issue-pattern, prof-framework, doctrine-rule, argument-structure, cross-case-connection |
| **Law Study Chill** | `law-study--chill.json` | Selective law study mode — only records what you'd be frustrated to figure out again. |  |
| **Meme Tokens** | `meme-tokens.json` | Solana memecoin activity monitoring. Captures pump/dump detection, signal tier transitions, token profiles, market conditions, algorithm insights. Requires live DEX feed. | pump-detected, dump-detected, signal-change, token-profile, market-condition, algorithm-insight |

---

## Mode Structure

Each `.json` mode file defines:

```json
{
  "name": "Mode display name",
  "description": "What this mode is for",
  "version": "1.0.0",
  "observation_types": [...],   // What kinds of events get captured
  "observation_concepts": [...], // How observations are categorized
  "prompts": {                   // System prompt overrides for the observer agent
    "system_identity": "...",
    "recording_focus": "...",
    "skip_guidance": "...",
    "type_guidance": "...",
    "concept_guidance": "..."
  }
}
```

To create a custom mode: copy `code.json`, rename it, customize `observation_types`, `observation_concepts`, and the `prompts.recording_focus` and `prompts.skip_guidance` sections.

---

## FinSurfing Recommended Modes

| Session Type | Use Mode |
|---|---|
| Feature development | `code.json` |
| Exploratory / debugging | `code--chill.json` |
| Financial news/filing batch analysis | `email-investigation.json` → via ragtime |
| Trading signal research | `meme-tokens.json` (adapt observation types for equities) |

---

## Deploy Modes

To install a mode into a running claude-mem installation:

```bash
# Copy to claude-mem modes directory
cp modes/<mode>.json ~/.claude/plugins/marketplaces/thedotmack/plugin/modes/

# Verify
ls ~/.claude/plugins/marketplaces/thedotmack/plugin/modes/
```

Changes take effect on next Claude Code session start.
