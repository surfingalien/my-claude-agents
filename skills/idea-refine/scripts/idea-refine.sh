#!/usr/bin/env bash
# Initialize an idea refinement session

set -euo pipefail

IDEAS_DIR="${IDEAS_DIR:-docs/ideas}"
IDEA_NAME="${1:-}"

usage() {
  echo "Usage: idea-refine.sh <idea-name>"
  echo ""
  echo "Creates a new idea refinement document in $IDEAS_DIR/"
  echo ""
  echo "Example:"
  echo "  idea-refine.sh better-onboarding"
  echo "  idea-refine.sh mobile-app-v2"
  exit 1
}

if [[ -z "$IDEA_NAME" ]]; then
  usage
fi

mkdir -p "$IDEAS_DIR"

IDEA_FILE="$IDEAS_DIR/${IDEA_NAME}.md"
DATE=$(date +%Y-%m-%d)

if [[ -f "$IDEA_FILE" ]]; then
  echo "File already exists: $IDEA_FILE"
  echo "Edit it directly or choose a different name."
  exit 1
fi

cat > "$IDEA_FILE" << EOF
# Idea: ${IDEA_NAME//-/ }

**Date:** $DATE
**Status:** Drafting

---

## Phase 1: Understand & Expand

### Problem Statement
[What problem are we solving? Who has this problem?]

### HMW Questions
- HMW ...?
- HMW ...?
- HMW ...?

### Wild Ideas (no filtering yet)
- 
- 
- 
- 

---

## Phase 2: Evaluate & Converge

### Idea Scoring

| Idea | User Value (1-5) | Feasibility (1-5) | Differentiation (1-5) | Total |
|------|-----------------|-------------------|----------------------|-------|
| | | | | |

### Assumptions to Validate

| Assumption | Confidence | Risk if Wrong | How to Validate |
|-----------|-----------|---------------|-----------------|
| | | | |

### Selected Direction
[Which idea(s) move forward and why]

---

## Phase 3: Sharpen & Ship

### Concept
[One paragraph: what this is, who it's for, why it's better]

### MVP Scope
**Must have:**
- 

**Out of scope:**
- 

### Success Criteria
We will consider this successful if:
- [ ] [Metric]: [Target]
- [ ] [Qualitative signal]: [Description]

We will run this for [timeframe] before deciding.
EOF

echo "Created: $IDEA_FILE"
echo ""
echo "Next steps:"
echo "  1. Fill in Phase 1 (understand the problem, generate ideas)"
echo "  2. Score ideas in Phase 2 and select a direction"
echo "  3. Define MVP scope in Phase 3"
echo "  4. Review with skill: skills/idea-refine/SKILL.md"
