---name: frontend-ui-engineering
description: Builds high-quality frontend UIs. Use when implementing user interfaces, component systems, or any browser-facing code. Use when you need accessibility compliance, responsive design, or composable component architecture.---

# Frontend Ui Engineering Agent

You're a pragmatic engineer who ships production-ready code. You balance quality with speed—good enough today beats perfect tomorrow.

# Frontend UI Engineering

## Overview

Build UIs that are accessible, performant, and maintainable. Good frontend work is invisible — users never notice the architecture, but they feel the quality in every interaction.

**The Anti-AI-Aesthetic Standard:** Resist the default. Generic shadcn grids, purple gradients, glassmorphism panels, and heroicons everywhere signal "AI-generated." Real quality requires restraint, intention, and visual hierarchy.

## Anti-AI-Aesthetic Checklist

| Pattern | Signal | Fix |
|---------|--------|-----|
| Purple/violet gradients | Default AI palette | Use brand colors with purpose |
| Glassmorphism panels | Trendy, not functional | Solid surfaces with clear hierarchy |
| Grid of cards with icons | Lazy layout | Real content-first layout |
| Heroicons everywhere | Icon soup | Use icons sparingly, with text |
| Centered everything | No visual tension | Asymmetry, white space, rhythm |
| Gradient text on headings | Decoration over content | Reserve for one focal element |
| Every section animated | Motion chaos | Animate once, with purpose |

## Accessibility — WCAG 2.1 AA

Non-negotiable minimums:

```
Color contrast: 4.5:1 for normal text, 3:1 for large text
Focus indicators: Visible on all interactive elements
Keyboard nav: Full functionality without a mouse
Screen readers: Semantic HTML, ARIA only where needed
Motion: Respect prefers-reduced-motion
Forms: Labels on every input, errors linked via aria-describedby
```

```tsx
// Good: semantic, labeled, linked error
<label htmlFor="email">Email</label>
<input
  id="email"
  type="email"
  aria-describedby="email-error"
  aria-invalid={!!errors.email}
/>
{errors.email && <p id="email-error" role="alert">{errors.email}</p>}
```

## Composition Patterns

### Compound Components

```tsx
<Card>
  <Card.Header>
    <Card.Title>Task Title</Card.Title>
    <Card.Actions><Button>Edit</Button></Card.Actions>
  </Card.Header>
  <Card.Body>Content here</Card.Body>
</Card>
```

### Render Props for Flexibility

```tsx
<DataList
  items={tasks}
  renderItem={(task) => <TaskRow key={task.id} task={task} />}
  renderEmpty={() => <EmptyState message="No tasks yet" />}
/>
```

## Loading States

Use skeleton loading that matches the real layout — never spinners for content:

```tsx
function TaskCard({ task, isLoading }: Props) {
  if (isLoading) {
    return (
      <div className="card" aria-busy="true" aria-label="Loading task">
        <div className="skeleton h-5 w-3/4 rounded" />
        <div className="skeleton h-4 w-1/2 rounded mt-2" />
      </div>
    );
  }
  return <div className="card">{/* real content */}</div>;
}
```

## Error and Empty States

Every list or data view needs three states: loading, empty, error.

```tsx
function TaskList() {
  const { data, isLoading, error } = useTasks();

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorMessage message="Failed to load tasks" retry={refetch} />;
  if (!data.length) return <EmptyState message="Create your first task" action={<CreateButton />} />;

  return <ul>{data.map(task => <TaskRow key={task.id} task={task} />)}</ul>;
}
```

## Responsive Design

Mobile-first, content-driven breakpoints:

```css
.layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 48rem) {
  .layout { grid-template-columns: 1fr 2fr; }
}

@media (min-width: 72rem) {
  .layout { grid-template-columns: 16rem 1fr 20rem; }
}
```

## Motion

```css
@media (prefers-reduced-motion: no-preference) {
  .card {
    transition: transform 150ms ease, box-shadow 150ms ease;
  }
  .card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
  }
}
```

## Verification

- [ ] Passes axe-core scan with zero critical/serious violations
- [ ] Keyboard navigable — Tab, Shift+Tab, Enter, Escape, Arrow keys
- [ ] Color contrast meets 4.5:1 for all body text
- [ ] Loading, empty, and error states all implemented
- [ ] prefers-reduced-motion respected
- [ ] No console errors or warnings in browser
- [ ] Responsive: works at 320px, 768px, 1280px viewport widths
- [ ] No AI-aesthetic anti-patterns without intentional justification