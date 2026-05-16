---name: doubt-driven-development
description: Subjects every non-trivial decision to a fresh-context adversarial review before it stands. Use when correctness matters more than speed, when working in unfamiliar code, or when stakes are high.---

# Doubt Driven Development Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# Doubt-Driven Development

## Overview

A confident answer is not a correct one. Long sessions accumulate context that quietly turns assumptions into "facts." Doubt-driven development is the discipline of materializing a fresh-context reviewer — biased to **disprove**, not approve — before any non-trivial output stands.

## When to Use

A decision is **non-trivial** when at least one of these is true:

- It introduces or modifies branching logic
- It crosses a module or service boundary
- It asserts a property the type system cannot verify (thread safety, idempotence, ordering)
- Its blast radius is irreversible (production deploy, data migration, public API change)

**When NOT to use:**

- Mechanical operations (renaming, formatting, file moves)
- Following a clear, unambiguous user instruction
- Reading or summarizing existing code
- One-line changes with obvious correctness
- The user has explicitly asked for speed over verification

## The Process

```
Doubt cycle:
- [ ] Step 1: CLAIM — wrote the claim + why-it-matters
- [ ] Step 2: EXTRACT — isolated artifact + contract, stripped reasoning
- [ ] Step 3: DOUBT — invoked fresh-context reviewer with adversarial prompt
- [ ] Step 4: RECONCILE — classified every finding against the artifact text
- [ ] Step 5: STOP — met stop condition
```

### Step 1: CLAIM

```
CLAIM: "The new caching layer is thread-safe under the read-heavy workload."
WHY THIS MATTERS: a race here corrupts user data and is hard to detect in QA.
```

### Step 2: EXTRACT

Provide the **artifact** and the **contract**, not the journey. Strip your reasoning. Pass conclusions and the reviewer will validate conclusions.

### Step 3: DOUBT — Adversarial Reviewer Prompt

```
Adversarial review. Find what is wrong with this artifact.
Assume the author is overconfident. Look for:
- Unstated assumptions
- Edge cases not handled
- Hidden coupling or shared state
- Ways the contract could be violated
- Existing conventions this might break
- Failure modes under unexpected input

Do NOT validate. Do NOT summarize. Find issues, or state
explicitly that you cannot find any after thorough examination.

ARTIFACT: <paste artifact>
CONTRACT: <paste contract>
```

**Pass ARTIFACT + CONTRACT only. Do NOT pass the CLAIM.**

### Step 4: RECONCILE

For each finding, classify in precedence order:

1. **Contract misread** — reviewer flagged something because the CONTRACT was unclear. Fix the contract, re-classify.
2. **Valid + actionable** — real issue requiring a change. Change it, re-loop.
3. **Valid trade-off** — real but cost of fixing exceeds cost of accepting. Document explicitly.
4. **Noise** — actually correct under context the reviewer didn't have. Note it, move on.

### Step 5: STOP

Stop when:
- Next iteration returns only trivial or already-considered findings, **or**
- 3 cycles completed (escalate to user), **or**
- User explicitly says "ship it"

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'm confident, skip the doubt step" | Moments of certainty are exactly when blind spots hide. |
| "Spawning a reviewer is expensive" | Debugging a wrong commit in production is more expensive. |
| "I'll do doubt at the end with /review" | /review is a final gate. Doubt-driven catches wrong directions while course-correction is still cheap. |
| "If I doubt every step I'll never ship" | The skill applies to non-trivial decisions, not every keystroke. |

## Verification

- [ ] Every non-trivial decision was named explicitly as a CLAIM before standing
- [ ] At least one fresh-context review per non-trivial artifact
- [ ] The reviewer received ARTIFACT + CONTRACT — NOT the CLAIM
- [ ] The reviewer's prompt was adversarial ("find issues"), not validating
- [ ] Findings were classified against the artifact text
- [ ] A stop condition was met