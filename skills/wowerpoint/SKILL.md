---
name: wowerpoint
description: >-
  Turn one document into a shareable narrative slide deck PDF using NotebookLM.
  One doc in, one PDF out. TRIGGER when: user says "wowerpoint this",
  "make a deck about [file]", "turn this report into slides",
  "make slides from this", or "deck this". Requires notebooklm CLI installed.
origin: claude-mem
owner: surfingalien
---

# wowerpoint

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

One doc in, one PDF out. Turn any document — report, analysis, README, research note — into a presentation-ready slide deck PDF via NotebookLM's slide generation engine.

Slide decks only. For videos or podcasts from the same source, use the `notebooklm` CLI directly.

## When to Use

- "Wowerpoint this [file]"
- "Make a slide deck about [file]"
- "Turn this report into slides"
- "Deck this"
- "Make this presentable"

**Requires:** `notebooklm` CLI installed and authenticated.

## Setup (One-Time Per Machine)

```bash
# Check if ready
notebooklm auth check && command -v jq && echo "✅ Ready"

# If not authenticated
notebooklm auth login

# If notebooklm not installed
npm install -g @google/notebooklm-cli
# or
pip install notebooklm-cli
```

## Workflow

### Step 1: Identify the Source Document

Accept any of:
- Markdown file: `.md`
- Text file: `.txt`
- PDF: `.pdf`
- URL: `https://...`
- Plain text pasted directly

If the user gives a URL or file path, use it directly. If they pasted text, write it to a temp file first:

```bash
echo "<pasted content>" > /tmp/wowerpoint-source.md
```

### Step 2: Generate the Deck

```bash
notebooklm slides \
  --source "<file-or-url>" \
  --output "<output-name>.pdf" \
  --format pdf
```

For local files:
```bash
notebooklm slides \
  --source ./docs/finsurfing-architecture.md \
  --output finsurfing-architecture-deck.pdf \
  --format pdf
```

For URLs:
```bash
notebooklm slides \
  --source "https://github.com/surfingalien/my-claude-agents/blob/main/README.md" \
  --output my-claude-agents-overview.pdf \
  --format pdf
```

### Step 3: Verify and Deliver

```bash
# Verify the PDF was created
ls -lh "<output-name>.pdf"

# Report to user
echo "✅ Deck ready: <output-name>.pdf ([N] slides, [size])"
```

## Use Cases for Your Stack

### FinSurfing Architecture Deck

```bash
notebooklm slides \
  --source ./README.md \
  --output finsurfing-overview.pdf
```

Good for: investor overviews, collaborator onboarding, demo prep.

### Skill/Agent Documentation Deck

```bash
notebooklm slides \
  --source ./skills/make-plan/SKILL.md \
  --output make-plan-overview.pdf
```

Good for: sharing a skill with team or community, ClawHub publishing.

### Sprint/Release Report Deck

```bash
# First generate the report, then deck it
cat > /tmp/sprint-report.md << 'EOF'
# Sprint N Report
...
EOF

notebooklm slides \
  --source /tmp/sprint-report.md \
  --output sprint-N-report.pdf
```

### AI-Trader Integration Proposal Deck

```bash
notebooklm slides \
  --source ./plans/04-trading-intelligence.md \
  --output ai-trader-proposal.pdf
```

Good for: pitching the integration approach before building.

## Output Customization

```bash
# Specify number of slides (approximate)
notebooklm slides --source <file> --output <file>.pdf --slides 10

# Specify tone
notebooklm slides --source <file> --output <file>.pdf --tone professional

# Specify language
notebooklm slides --source <file> --output <file>.pdf --language en
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Auth error | `notebooklm auth login` |
| Empty PDF | Source file may be too short — add more content or try a longer doc |
| CLI not found | `npm install -g @google/notebooklm-cli` |
| Timeout | Large files take longer — wait or split the source doc |

## Anti-Patterns

❌ Using this for video/podcast generation (use `notebooklm` CLI directly)
❌ Feeding a one-paragraph source — needs enough content for multiple slides
❌ Expecting design customization — NotebookLM controls the visual style

## Related Skills

- `timeline-report` — Generate the narrative report that you then wowerpoint
- `make-plan` — Generate the plan doc that you then deck for presentation
- `pptx` — If you need full control over slide design and layout (heavier but more customizable)
