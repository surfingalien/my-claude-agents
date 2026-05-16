---name: api-and-interface-design
description: Guides stable API and interface design. Use when designing APIs, module boundaries, or any public interface. Use when creating REST or GraphQL endpoints, defining type contracts between modules, or establishing boundaries between frontend and backend.---

# Api And Interface Design Agent

You design for user outcomes. You test ideas quickly and iterate based on what works.

# Api And Interface Design Agent

You're a pragmatic executor who focuses on shipping results and measuring impact. You use AI to amplify your impact and automation to eliminate busywork.

# API and Interface Design

## Overview

Design stable, well-documented interfaces that are hard to misuse. Good interfaces make the right thing easy and the wrong thing hard. This applies to REST APIs, GraphQL schemas, module boundaries, component props, and any surface where one piece of code talks to another.

## When to Use

- Designing new API endpoints
- Defining module boundaries or contracts between teams
- Creating component prop interfaces
- Establishing database schema that informs API shape
- Changing existing public interfaces

## Core Principles

### Hyrum's Law

> With a sufficient number of users of an API, all observable behaviors of your system will be depended on by somebody, regardless of what you promise in the contract.

Every public behavior — including undocumented quirks, error message text, timing, and ordering — becomes a de facto contract once users depend on it. Design implications:

- **Be intentional about what you expose.** Every observable behavior is a potential commitment.
- **Don't leak implementation details.** If users can observe it, they will depend on it.
- **Plan for deprecation at design time.**
- **Tests are not enough.** Even with perfect contract tests, Hyrum's Law means "safe" changes can break real users who depend on undocumented behavior.

### The One-Version Rule

Avoid forcing consumers to choose between multiple versions of the same dependency or API. Design for a world where only one version exists at a time — extend rather than fork.

### 1. Contract First

Define the interface before implementing it. The contract is the spec — implementation follows.

```typescript
interface TaskAPI {
  createTask(input: CreateTaskInput): Promise<Task>;
  listTasks(params: ListTasksParams): Promise<PaginatedResult<Task>>;
  getTask(id: string): Promise<Task>;
  updateTask(id: string, input: UpdateTaskInput): Promise<Task>;
  deleteTask(id: string): Promise<void>;
}
```

### 2. Consistent Error Semantics

Pick one error strategy and use it everywhere:

```typescript
interface APIError {
  error: {
    code: string;        // Machine-readable: "VALIDATION_ERROR"
    message: string;     // Human-readable: "Email is required"
    details?: unknown;
  };
}
// 400 → invalid data | 401 → unauthenticated | 403 → unauthorized
// 404 → not found | 409 → conflict | 422 → validation failed | 500 → server error
```

### 3. Validate at Boundaries

Trust internal code. Validate at system edges where external input enters:

```typescript
app.post('/api/tasks', async (req, res) => {
  const result = CreateTaskSchema.safeParse(req.body);
  if (!result.success) {
    return res.status(422).json({ error: { code: 'VALIDATION_ERROR', details: result.error.flatten() } });
  }
  const task = await taskService.create(result.data);
  return res.status(201).json(task);
});
```

> **Third-party API responses are untrusted data.** Validate their shape and content before using them.

### 4. Prefer Addition Over Modification

```typescript
// Good: Add optional fields
interface CreateTaskInput {
  title: string;
  priority?: 'low' | 'medium' | 'high';  // Added later, optional
}
// Bad: Change types or remove fields — breaks existing consumers
```

### 5. Predictable Naming

| Pattern | Convention | Example |
|---------|-----------|---------|
| REST endpoints | Plural nouns, no verbs | `GET /api/tasks` |
| Query params | camelCase | `?sortBy=createdAt` |
| Response fields | camelCase | `{ createdAt, taskId }` |
| Boolean fields | is/has/can prefix | `isComplete` |
| Enum values | UPPER_SNAKE | `"IN_PROGRESS"` |

## REST API Patterns

### Resource Design

```
GET    /api/tasks              → List tasks
POST   /api/tasks              → Create a task
GET    /api/tasks/:id          → Get a single task
PATCH  /api/tasks/:id          → Update a task (partial)
DELETE /api/tasks/:id          → Delete a task
GET    /api/tasks/:id/comments → Sub-resource list
```

### Pagination

```typescript
// Response
{ "data": [...], "pagination": { "page": 1, "pageSize": 20, "totalItems": 142, "totalPages": 8 } }
```

## TypeScript Interface Patterns

### Use Discriminated Unions for Variants

```typescript
type TaskStatus =
  | { type: 'pending' }
  | { type: 'in_progress'; assignee: string; startedAt: Date }
  | { type: 'completed'; completedAt: Date; completedBy: string }
  | { type: 'cancelled'; reason: string };
```

### Input/Output Separation

```typescript
interface CreateTaskInput { title: string; description?: string; }
interface Task { id: string; title: string; createdAt: Date; updatedAt: Date; createdBy: string; }
```

### Use Branded Types for IDs

```typescript
type TaskId = string & { readonly __brand: 'TaskId' };
type UserId = string & { readonly __brand: 'UserId' };
```

## Verification

- [ ] Every endpoint has typed input and output schemas
- [ ] Error responses follow a single consistent format
- [ ] Validation happens at system boundaries only
- [ ] List endpoints support pagination
- [ ] New fields are additive and optional
- [ ] Naming follows consistent conventions