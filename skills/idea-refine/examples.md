# Idea Refinement — Examples

## Example 1: "Build a better to-do app"

### Phase 1: Understand & Expand

**Problem space:** Personal productivity tools are abundant; most fail due to friction, not features.

**HMW Questions:**
- HMW make task capture so fast users do it reflexively?
- HMW reduce the cognitive load of prioritizing?
- HMW make the app useful even when the user is overwhelmed?

**Wild ideas:**
- Voice capture with AI transcription and auto-tagging
- Tasks that expire if not acted on (urgency by design)
- A "brain dump" mode that captures anything without organizing
- Context-aware task surfacing based on location/time

### Phase 2: Evaluate & Converge

| Idea | User Value | Feasibility | Differentiation | Score |
|------|-----------|-------------|-----------------|-------|
| Voice capture | High (reduces friction) | Medium | Medium | 7 |
| Task expiry | Medium (controversial) | High | High | 6 |
| Brain dump mode | High (solves overwhelm) | High | Medium | 7.5 |
| Context-aware surfacing | High (reduces choices) | Low | High | 5 |

**Selected direction:** Brain dump mode + smart daily review

### Phase 3: Sharpen & Ship

**Concept:** A to-do app with two modes — capture mode (no friction, zero organization) and review mode (once daily, AI surfaces what matters today).

**MVP:** Voice/text input → instant list → daily 5-minute review with AI priority suggestions.

**Assumptions to test:**
- Users will use daily review consistently
- AI priority suggestions will be accurate enough to trust

---

## Example 2: "Improve our onboarding"

### Phase 1: Understand & Expand

**Problem:** Users drop off during onboarding. Current flow has 8 steps before first value.

**HMW Questions:**
- HMW get users to their first "aha moment" in under 60 seconds?
- HMW make setup feel like progress, not work?
- HMW onboard different user types without one-size-fits-all friction?

**Wild ideas:**
- Skip setup entirely — generate sample data so users see a working product immediately
- Role-based onboarding paths (manager vs. individual contributor)
- Video demo that runs before signup
- "Import from" options (Notion, Asana) as first step

### Phase 2: Evaluate & Converge

**Selected direction:** Sample data generation + role fork at step 1

### Phase 3: Sharpen & Ship

**MVP:** Auto-populate with sample tasks on signup. Role selection on first screen routes to different feature highlights.

**Success metric:** Time to first task created < 2 minutes for 80% of signups.
