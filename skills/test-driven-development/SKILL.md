---name: test-driven-development
description: Drives implementation with tests. Use when building any new feature or fixing any bug to ensure correctness through the Red-Green-Refactor cycle. Tests are the specification, not the afterthought.---

# Test Driven Development Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# Test-Driven Development

## Overview

Write the test first. The test defines the expected behavior — the implementation is just the code that makes the test pass. TDD produces code that's provably correct, easier to change, and naturally testable by design.

**The Cycle:** RED → GREEN → REFACTOR

```
RED:      Write a failing test that defines the desired behavior
GREEN:    Write the minimum code to make the test pass
REFACTOR: Improve the code without changing behavior (all tests still pass)
```

## The RED Phase

Write a test that:
1. Fails for the right reason (the behavior doesn't exist yet)
2. Describes intent in its name
3. Tests one thing only

```typescript
// Good: specific, failing, describes intent
describe('TaskService.createTask', () => {
  it('rejects titles longer than 200 characters', async () => {
    const input = { title: 'x'.repeat(201) };
    await expect(taskService.createTask(input)).rejects.toThrow('Title must be 200 characters or fewer');
  });
});
```

Run the test. Confirm it fails. If it passes, the behavior already exists or the test is wrong.

## The GREEN Phase

Write the minimum code to make the test pass — nothing more:

```typescript
async createTask(input: { title: string }): Promise<Task> {
  if (input.title.length > 200) {
    throw new Error('Title must be 200 characters or fewer');
  }
  return this.repository.create(input);
}
```

Resist the urge to generalize, abstract, or extend during the Green phase. Just pass the test.

## The REFACTOR Phase

With all tests green, improve the code:
- Extract repeated logic
- Rename for clarity
- Remove duplication
- Improve error messages

Run tests after every change. If any test fails, undo and try again.

## The Prove-It Pattern (Bug Fixes)

When fixing a bug:

```
1. REPRODUCE → Write a test that reproduces the bug (it must fail)
2. VERIFY    → Confirm the test fails for the right reason
3. FIX       → Fix the bug
4. CONFIRM   → Confirm the test now passes
5. CHECK     → Run all tests to ensure no regression
```

The bug-reproducing test becomes permanent regression protection.

```typescript
// Bug: tasks with empty titles were saved
it('rejects empty titles', async () => {
  // This test MUST FAIL before the fix
  await expect(taskService.createTask({ title: '' })).rejects.toThrow('Title is required');
});

// Now fix the bug
if (!input.title || input.title.trim().length === 0) {
  throw new Error('Title is required');
}

// Test now passes — regression is protected
```

## Test Pyramid

```
         /\
        /  \      E2E Tests (few, slow, high confidence)
       /----\
      /      \    Integration Tests (moderate, real DB)
     /--------\
    /          \  Unit Tests (many, fast, isolated)
   /____________\
```

Write mostly unit tests. Add integration tests for DB queries and API endpoints. Add a handful of E2E tests for critical user flows only.

## DAMP Over DRY

Tests should be **D**escriptive **A**nd **M**eaningful **P**hrases, not DRY (Don't Repeat Yourself).

```typescript
// BAD: DRY but unreadable test
it('works', async () => {
  const result = await createAndValidate(defaults);
  assertCommonProps(result);
});

// GOOD: DAMP — more verbose, but readable in isolation
it('creates a task with the provided title and due date', async () => {
  const result = await taskService.createTask({
    title: 'Write tests',
    dueDate: '2026-06-01',
  });

  expect(result.title).toBe('Write tests');
  expect(result.dueDate).toBe('2026-06-01');
  expect(result.id).toBeDefined();
  expect(result.createdAt).toBeDefined();
});
```

Repeated setup code in tests is fine. Each test should be understandable without reading other tests.

## Prefer Real Over Mocks

Use real implementations where practical:

```typescript
// Prefer real test database over mocked repository
beforeAll(async () => {
  db = await createTestDatabase(); // real SQLite or test Postgres
  repository = new TaskRepository(db);
});

// Only mock at true system boundaries (external APIs, email, payment)
const emailService = { send: jest.fn() };
```

Mocks that mirror real behavior exactly give false confidence. Test against the real thing where the cost is acceptable.

## Arrange-Act-Assert

Structure every test clearly:

```typescript
it('marks a task as complete', async () => {
  // Arrange
  const task = await createTask({ title: 'Test task' });

  // Act
  const result = await taskService.completeTask(task.id);

  // Assert
  expect(result.completedAt).toBeDefined();
  expect(result.status).toBe('completed');
});
```

One assertion per concept (not literally one `expect()` call, but one logical thing being verified).

## Verification

- [ ] Tests written before implementation (RED phase confirmed)
- [ ] Every bug fix has a reproducing test committed with the fix
- [ ] Test names describe behavior ("rejects empty titles"), not implementation ("calls validator")
- [ ] Tests are DAMP — readable in isolation without context
- [ ] No mocks for internal code — only at system boundaries
- [ ] Unit → Integration → E2E pyramid maintained
- [ ] All tests pass before committing