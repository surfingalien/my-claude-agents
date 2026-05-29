---
name: weekly-digests
description: >-
  Generate serial week-by-week narrative digests of a project's full claude-mem
  timeline. One chapter per ISO week, each subagent receiving prior week's
  carry-forward for narrative coherence. TRIGGER when: user asks for
  "weekly digests", "week-by-week story", "serial timeline", "narrative chapters",
  or a project with many weeks of history that would be too long for one report.
origin: claude-mem
owner: surfingalien
---

# weekly-digests

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## Your Role

Produce a serial, multi-chapter narrative digest of a project's complete claude-mem history. One digest per ISO week. Each chapter receives the prior week's carry-forward so the story stays coherent across sessions.

**Differs from `timeline-report`**: that tool produces one long document. This produces N chapter files, one per ISO week, suitable for week-by-week reading or team distribution.

## When to Use

- Project has 4+ weeks of claude-mem observation history
- User wants a "story" of the project that can be read chapter by chapter
- Team retrospectives: distribute this week's chapter at the end of the sprint
- Long-running projects where a single report would be overwhelming
- "Show me what we did each week"

**For shorter projects (< 4 weeks):** Use `timeline-report` instead — one document is cleaner.

## Workflow

### Step 1: Count the Weeks

```bash
# Fetch full timeline
claude-mem timeline --project <path> --format json > full-timeline.json

# Find the ISO week range
cat full-timeline.json | jq '[.[] | .timestamp] | min, max'

# Count ISO weeks covered
cat full-timeline.json | jq '[.[] | (.timestamp | strptime("%Y-%m-%dT%H:%M:%SZ") | strftime("%Y-W%V"))] | unique | length'
```

**The chapter count equals the number of ISO weeks covered.** A project with 8 weeks of data produces 8 chapters. Do not artificially limit.

### Step 2: Split by ISO Week

```bash
# Split timeline into per-week files
claude-mem timeline --project <path> --split-by week --output-dir /tmp/weekly-splits/

# Verify splits
ls /tmp/weekly-splits/  # should show: 2026-W18.json, 2026-W19.json, etc.
```

### Step 3: Run Serial Subagents

Deploy one subagent per week, in chronological order. Each subagent receives:
1. That week's observation file
2. The prior week's carry-forward block (2–3 paragraphs summary)

**Subagent brief template:**

```markdown
## Your Task: Write Chapter for ISO Week [YYYY-WXX]

**Observations file:** /tmp/weekly-splits/[YYYY-WXX].json

**Carry-forward from prior week:**
[2–3 paragraph summary from previous chapter's carry-forward block]

**Write:**
1. A chapter titled "Week [N]: [Evocative Chapter Title]"
2. Narrative: what was built, what was struggled with, what was decided
3. Key events bullet list (3–7 items)
4. A "Carry-forward" block at the end (2–3 paragraphs: what's unresolved, what matters next week)

**Tone:** Analytical but readable. Like a dev blog post, not a commit log.

**Length:** 300–600 words for the narrative, 3–7 bullet points for key events.
```

### Step 4: Assemble the Digest

After all subagents complete, assemble into the final output:

```markdown
# [Project Name] — Weekly Development Digest

*[N] chapters covering [start date] to [end date]*
*Generated from [M] observations across [K] sessions*

---

## Chapter 1: Week of [Date]
### [Evocative Title]

[Narrative]

**Key Events:**
- ...

---

## Chapter 2: Week of [Date]
...
```

### Step 5: Save and Distribute

```bash
# Save to docs/
mkdir -p docs/weekly-digests
cp assembled-digest.md docs/weekly-digests/digest-$(date +%Y-%m-%d).md

# Or save individual chapters
mkdir -p docs/weekly-digests/chapters/
# [copy per-week chapter files]
```

## Chapter Format

Each chapter must include:

```markdown
## Chapter [N]: [ISO Week Range]
### [Evocative Chapter Title — e.g., "The Great Schema Migration" or "Shipping the Trading Pipeline"]

[300–600 word narrative]

**Key Events This Week:**
- [Event with specific detail — files changed, decisions made, problems solved]
- [Event]
- ...

**Carry-forward:**
[2–3 paragraphs: what's still in progress, what context the next week needs, any open questions]
```

## FinSurfing Digest Suggestions

For a FinSurfing weekly digest series, watch for these narrative beats:

- **The Railway Deploy chapter** — when the first successful production deploy happened
- **The Anthropic Integration chapter** — when Claude API was first wired in
- **The Trading Signal chapter** — when AI-Trader integration was attempted/shipped
- **The Schema Evolution chapters** — each major migration and what forced it
- **The my-claude-agents parallel track** — weeks where skill/agent development happened alongside FinSurfing work

These naturally cluster into a compelling story about building a solo trading intelligence platform.

## Related Skills

- `timeline-report` — Single narrative document (better for short projects or executive summaries)
- `mem-search` — Quick targeted search without narrative overhead
- `knowledge-agent` — Topic-focused interactive brains (complementary, not a substitute)
