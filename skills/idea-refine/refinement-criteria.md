# Idea Refinement Criteria

## Scoring an Idea

Rate each dimension 1–5. Total score out of 25.

### 1. User Value (1–5)

Does this create genuine value for the target user?

| Score | Description |
|-------|-------------|
| 1 | Solves a problem no one has |
| 2 | Marginally better than alternatives |
| 3 | Meaningfully better for some users |
| 4 | Significantly better for a clear segment |
| 5 | Dramatically better; users would pay for it |

### 2. Feasibility (1–5)

Can this be built with available resources?

| Score | Description |
|-------|-------------|
| 1 | Requires technology that doesn't exist |
| 2 | Possible but requires significant R&D |
| 3 | Buildable but complex; 6+ months |
| 4 | Buildable in 1–3 months with current stack |
| 5 | Can prototype in days; clear path to production |

### 3. Differentiation (1–5)

Does this stand out from existing solutions?

| Score | Description |
|-------|-------------|
| 1 | Identical to existing products |
| 2 | Minor variation on existing approach |
| 3 | Meaningful difference in one dimension |
| 4 | Clearly distinct approach or positioning |
| 5 | Category-defining; no direct comparison |

---

## Assumption Audit

Before committing to an idea, list every assumption and challenge each:

```markdown
## Assumptions

| Assumption | Confidence | Risk if Wrong | How to Validate |
|-----------|-----------|---------------|-----------------|
| Users want X | Medium | High | 5 user interviews |
| We can build Y in Z weeks | Low | Medium | Technical spike |
| Market is large enough | Medium | High | Market sizing research |
| Users will pay $N | Low | High | Pre-sell before building |
```

**Confidence levels:**
- **High:** We have evidence (user research, data, prior work)
- **Medium:** We have indirect evidence or strong intuition
- **Low:** We're guessing

Assumptions with Low confidence + High risk = validate first before building.

---

## Decision Framework

When choosing between ideas:

### 1. Eliminate Non-Starters
Remove any idea that:
- Scores < 2 on Feasibility
- Scores < 2 on User Value
- Has an unvalidatable critical assumption

### 2. Score Remaining Ideas

Use the 3-dimension scorecard. Sort by total score.

### 3. Apply Qualitative Filters

High-scoring ideas still need a gut check:
- Does the team actually want to build this?
- Does it align with the product's strategic direction?
- Is the timing right, or should this wait?

### 4. Select and Commit

Pick the idea. Write the assumptions. Set a validation plan. Commit.

---

## MVP Scoping

Once an idea is selected, scope the minimum viable version:

**The MVP Test:** "What is the smallest thing we could build that would let us learn whether this idea works?"

### The Scoping Questions

1. **What job does this solve for the user?** (JTBD)
2. **What's the one metric that would prove it's working?**
3. **What features are required vs. desired?**
4. **What could we cut and still validate the hypothesis?**

### Feature Categorization

```
MUST HAVE (without this, the MVP doesn't prove anything):
- [Feature]

SHOULD HAVE (adds significant signal, low cost):
- [Feature]

NICE TO HAVE (save for v2):
- [Feature]

OUT OF SCOPE (would distract from the hypothesis):
- [Feature]
```

### MVP Success Criteria

Write the success criteria before building:

```
"We will consider this MVP successful if:
  - [Metric 1]: [Target value]
  - [Metric 2]: [Target value]
  - [Qualitative signal]: [Description]

We will run this for [time period] before making a go/no-go decision."
```
