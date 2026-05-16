---
name: review
description: Review the current changes across five quality axes before merging.
---

Apply the code-review-and-quality skill to review all changes since branching from main.

Review across five axes:

### 1. Correctness
- Does it match the spec/task requirements?
- Are edge cases handled (null, empty, boundaries)?
- Any off-by-one errors, race conditions, or state issues?

### 2. Readability & Simplicity
- Can another engineer understand this without the author explaining?
- Are names descriptive and consistent?
- Could this be done in fewer lines without losing clarity?

### 3. Architecture
- Does it follow existing patterns?
- Clean module boundaries? No circular dependencies?

### 4. Security
- Input validated at boundaries?
- No secrets in code?
- Auth checks in place?
- SQL parameterized?

### 5. Performance
- Any N+1 query patterns?
- Any unbounded operations?
- Pagination on list endpoints?

Use comment severity labels in your output:
- **(no prefix)** — Required: must address before merge
- **Critical:** — Blocks merge
- **Nit:** — Optional style preference
- **Consider:** — Suggestion, not required
- **FYI** — No action needed

End with verdict: **APPROVE** or **REQUEST CHANGES**

Reference: `skills/code-review-and-quality/SKILL.md`
