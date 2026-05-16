---
name: ship
description: Run the pre-launch checklist before deploying to production.
---

Apply the shipping-and-launch skill to verify readiness for production.

Work through the pre-launch checklist:

### Code Quality
- [ ] All tests pass
- [ ] No TypeScript errors
- [ ] No lint warnings
- [ ] Code reviewed and approved
- [ ] Migrations tested against production data volume

### Security
- [ ] `npm audit --audit-level=high` passes
- [ ] No secrets committed
- [ ] Auth checks on all new endpoints
- [ ] Input validation on all new API boundaries

### Performance
- [ ] LCP ≤ 2.5s on mobile (Lighthouse)
- [ ] No N+1 queries
- [ ] Database queries have appropriate indexes

### Accessibility
- [ ] axe-core scan: zero critical/serious violations
- [ ] Keyboard navigable

### Infrastructure
- [ ] Environment variables set in production
- [ ] Database migrations applied or ready
- [ ] Feature flags configured
- [ ] Rollback procedure documented

Report: which items pass, which need action, and whether it's safe to deploy.

Reference: `skills/shipping-and-launch/SKILL.md`
