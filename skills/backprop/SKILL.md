---
name: backprop
description: |
  Bug → spec protocol. When a bug is found or a test fails, trace the cause,
  decide whether a new §V invariant would catch recurrence, append to §B.
  This is the one non-obvious thing SDD does that plan-then-execute doesn't.
  Triggers on test failure, bug report, post-mortem, or explicit user ask.
origin: JuliusBrussee/cavekit
owner: surfingalien
license: MIT
---

You're a pragmatic executor focused on shipping results and measuring impact. You use AI to amplify your effect and automation to eliminate busywork.

## FinSurfing Context

**Backprop is the highest-value habit to build in FinSurfing development.** Every bug that hits Railway production should generate a §B entry + §V invariant so it can never silently recur.

**Example FinSurfing backprop flow**:
```
Bug: portfolio value shows NaN when Finnhub returns null for a delisted stock

§B row: B4|2026-05-31|Finnhub null on delisted → NaN in portfolio|V8
§V new: V8: ∀ Finnhub quote response → null coalesce before arithmetic
Test:   TestV8_NullQuoteCoalesces → passes 0 not NaN for null price
Fix:    src/api/portfolio.js:142 → price ?? 0
Commit: backprop §B.4 + §V.8: Finnhub null → NaN in portfolio value
```

**When to always backprop in FinSurfing**:
- Any Railway deploy that caused a visible error
- Any Finnhub API edge case (rate limit, delisted stock, missing field)
- Any PostgreSQL race condition or transaction gap
- Any Claude API timeout or malformed response

## Related Skills

- `cavekit-spec` → sole SPEC.md mutator; backprop calls it internally
- `cavekit-build` → resumes build after backprop updates the spec
- `caveman-review` → catches bug classes before they hit production

# backprop — bug → spec

Plan-then-execute fixes the code & forgets.
SDD fixes the code AND edits spec so recurrence is impossible.
That edit is backprop.

## WHEN TO BACKPROP

- Test failed at `/build` verification.
- User reports bug.
- Post-mortem after production incident.
- `/check` flags VIOLATE with root cause found.

## SIX STEPS

### 1. TRACE
Read failure output / bug report.
Find exact file:line of wrong behavior.
Name root cause in one caveman sentence.

### 2. ANALYZE
Ask three questions:
- Would a new §V invariant catch this class of bug? (most common: yes)
- Is §I wrong — did spec claim shape the code cannot deliver? (sometimes)
- Is §T wrong — did we build the wrong thing? (rare but real)

### 3. PROPOSE
Draft the spec change. Never skip §B; §V/§I/§T are case-by-case.

Template:
```
§B row: B<next>|<date>|<root cause>|V<N>
§V line: V<next>: <testable rule that would have caught it>
```

Example:
```
§B row: B3|2026-04-20|refund job ran twice on retry|V7
§V line: V7: ∀ refund → idempotency key check before charge reversal
```

### 4. GENERATE TEST
New invariant without test = lie. Add failing test first.
Name test so it cites the invariant: `TestV7_RefundIdempotent`.

### 5. VERIFY
Fix code. Run test. Must pass. Run full suite. Must not regress.

### 6. LOG
Commit spec edit + test + code fix together.
Commit msg: `backprop §B.<n> + §V.<N>: <one-line cause>`.

## WHAT MAKES A GOOD INVARIANT

- Testable in code (grep-able or assert-able).
- Scoped to a behavior, not a file.
- Stated positively when possible (`! hold` over `⊥ forbid`).
- References §I surface where it applies.

**Bad**: V8: code should be correct.
**Good**: V8: ∀ pg_query ! params interpolated via driver, ⊥ string concat.

## WHEN NOT TO ADD §V

- Bug was purely mechanical typo with no class (`i++` vs `i--` in throwaway).
- Fix is a one-time migration.
- Root cause is external dep (upgrade deps instead, note in §C).

Still append §B entry — record that this failure mode was considered. Future bug with same smell → §B search shows precedent.

## OUTPUT SHAPE

Every backprop run produces:
1. §B entry (always).
2. §V entry (usually).
3. Test file (when §V added).
4. Code fix.
5. One commit.

No dashboards. No log files. SPEC.md + git is the full history.