---
name: source-driven-development
description: Grounds implementation in authoritative sources. Use when implementing any API, library feature, browser capability, or framework pattern. Always fetch from official docs before writing code.
---

# Source-Driven Development

## Overview

Don't code from memory. Code from documentation. The source is always more accurate than what you remember or what you were trained on — APIs change, behaviors get deprecated, and subtle details matter.

**The Principle:** Detect what you need → Fetch the authoritative source → Implement from that source → Cite the source in the PR.

## Source Hierarchy

When multiple sources exist, prefer in this order:

```
1. Official documentation (docs.example.com, MDN, spec)
2. Official changelog / migration guide
3. Official blog post from maintainers
4. MDN Web Docs (for web APIs)
5. Can I Use (for browser support)
6. GitHub source code / test suite
7. Community resources (Stack Overflow, blog posts)
```

Never rely solely on sources in positions 4–7 for any security-sensitive, performance-critical, or contract-defining implementation.

## The DETECT → FETCH → IMPLEMENT → CITE Process

### DETECT

Identify what needs authoritative source verification:

```
- New library or framework version
- Browser API you haven't used recently
- Third-party API endpoint behavior
- Security-relevant behavior (auth flows, crypto, headers)
- Performance-sensitive API (rendering, memory, I/O)
- Any assumption about default behavior
```

### FETCH

Retrieve the authoritative source before writing code:

```
For npm packages: check the package's README and CHANGELOG
For web APIs: fetch MDN documentation
For browser support: check Can I Use
For REST APIs: fetch the OpenAPI spec or reference docs
For framework patterns: check the framework's official docs
```

When implementing a feature using a third-party API, read the docs for:
- Request format and required fields
- Response structure (don't guess field names)
- Error codes and their meanings
- Rate limits and quotas
- Authentication requirements

### IMPLEMENT

Write code that matches what the documentation says, not what you expect:

```typescript
// BAD: Implementing from memory/assumption
const result = await stripe.charges.create({
  amount: 1000,
  currency: 'usd',
  source: tokenId,  // might be wrong — is it 'source' or 'payment_method'?
});

// GOOD: Implement from the fetched docs
// Per Stripe docs (fetched 2026-05-16): PaymentIntent API replaces Charges
// https://stripe.com/docs/payments/payment-intents
const paymentIntent = await stripe.paymentIntents.create({
  amount: 1000,
  currency: 'usd',
  payment_method: paymentMethodId,
  confirm: true,
});
```

### CITE

Record what source you used and when:

```typescript
// In PR description or commit message:
// "Implemented per Stripe PaymentIntents API docs (fetched 2026-05-16):
//  https://stripe.com/docs/api/payment_intents/create"
```

For security-critical implementations, always cite the source in the code comment too.

## When Source Is Unclear

When documentation contradicts itself, is ambiguous, or is missing:

1. Find the test suite — what the tests assert is ground truth
2. Check the GitHub issues for the official repo
3. Try it in isolation and test the behavior directly
4. Flag the ambiguity in your PR description

Never silently pick one interpretation. Surface the ambiguity.

## Source Staleness

Documentation can be outdated. Check:

```
- When was this page last updated?
- What version does it apply to?
- Is there a newer version with different behavior?
- Are there deprecation notices?
```

For packages: always check the CHANGELOG for the version you're using, not the latest docs.

## Red Flags That Signal "Fetch First"

```
"I think the API works like..."
"Wasn't this changed in v3?"
"IIRC the default is..."
"This should work similarly to..."
```

Each of these is a signal to stop and fetch the authoritative source before proceeding.

## Verification

- [ ] Official documentation consulted before implementation
- [ ] Source hierarchy followed (official > community)
- [ ] API response structure verified from docs, not assumed
- [ ] Version-specific behavior confirmed for the version in use
- [ ] Deprecation notices checked
- [ ] Security-sensitive behavior cited in PR description
- [ ] Ambiguous behaviors surfaced and resolved before merging
