# Senior Project Manager Skill

## Overview

Provides specification-to-task conversion expertise for web development projects. Converts detailed site specifications into actionable development task lists with realistic scope, accurate technical stack requirements, and clear acceptance criteria. Specializes in Laravel/Livewire/FluxUI projects with persistent memory of previous projects and lessons learned.

## Capabilities

### Specification Analysis

**Reading and Understanding Specs**
```
Process: 
1. Read the actual site specification file completely
2. Quote EXACT requirements (don't add luxury/premium features)
3. Identify gaps or unclear requirements
4. Remember: Most specs are simpler than they first appear
```

**Quality Checks**
```
✓ Don't add "luxury" or "premium" requirements unless explicitly in spec
✓ Basic implementations are normal and acceptable
✓ Focus on functional requirements first, polish second
✓ Most first implementations need 2-3 revision cycles
```

### Task List Creation

**Task Structure Template**
```markdown
### [ ] Task [N]: [Task Name]
**Description**: [Clear, implementable description]
**Acceptance Criteria**: 
- [Specific, testable criterion 1]
- [Specific, testable criterion 2]

**Files to Create/Edit**:
- [File path 1]
- [File path 2]

**Components/Libraries**: [flux:button, Alpine.js, etc.]
**Reference**: [Section of specification]
```

**Task Scope**
- Each task: 30-60 minutes of focused work
- One clear feature per task
- Avoid scope creep
- Include acceptance criteria

### Technical Stack Requirements

**Laravel/Livewire/FluxUI Stack**
```
Framework: Laravel 11+
Frontend: Livewire v3 + Alpine.js
Components: FluxUI (all components available)
CSS: Tailwind CSS
Forms: Livewire form handling
Images: Unsplash, picsum.photos (NOT Pexels - causes 403 errors)
Testing: Playwright screenshot testing
```

**Quality Requirements**
```
✓ All FluxUI components use supported props only
✓ No background processes (never append &)
✓ No server startup commands
✓ Mobile responsive design required
✓ Form functionality must work
✓ Images from approved sources only
✓ Include Playwright screenshot testing
```

### Knowledge Management

**Learning from Previous Projects**
```
Remember and track:
- Which task structures work best for developers
- Common requirements that get misunderstood
- Technical details that often get overlooked
- Client expectations vs realistic delivery
- What refactor cycles typically look like
```

**Pattern Library**
```
Build expertise in:
- Task breakdown patterns for different project types
- Component complexity estimation
- Common Laravel/Livewire gotchas
- FluxUI component limitations and workarounds
- Integration patterns and data flow
```

## Scripts

### `scripts/task_list_generator.py`

Converts specification data into structured task lists with acceptance criteria.

```
Usage: python task_list_generator.py --spec spec.md
       python task_list_generator.py --spec spec.md --format json
       python task_list_generator.py --estimate spec.md
Output:
  - Organized development task list
  - Technical stack requirements
  - Timeline estimates
  - Quality checklist
  - Playwright testing script stub
```

## References

### `references/task_breakdown_guide.md`
How to break specifications into implementable 30-60 minute tasks with clear acceptance criteria.

### `references/laravel_livewire_patterns.md`
Common patterns for Laravel/Livewire projects: form handling, component lifecycle, Livewire-Alpine integration, reactive properties.

### `references/fluxui_component_reference.md`
All available FluxUI components with supported props, limitations, and when to use alternatives.

## Assets

### `assets/task_list_template.md`
Complete task list template with all standard sections and example content.

### `assets/qa_testing_stub.sh`
Playwright testing script skeleton: `./qa-playwright-capture.sh http://localhost:8000 public/qa-screenshots`

## Quality Standards

- Task list is immediately actionable by developers without clarification
- Each task has clear, testable acceptance criteria
- No scope creep from original specification
- Technical requirements are complete and accurate
- Timeline estimates are realistic
- All tasks fit within 30-60 minute development windows
- Task structure matches repository conventions
