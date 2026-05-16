#!/usr/bin/env python3
"""Converts site specifications into actionable development task lists."""

import sys
import json
import argparse
import re
from pathlib import Path


def read_specification(spec_path: str) -> str:
    """Read specification file."""
    try:
        with open(spec_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Specification file not found: {spec_path}", file=sys.stderr)
        sys.exit(1)


def extract_requirements(spec: str) -> dict:
    """Extract key requirements from specification."""
    # Basic extraction of common sections
    requirements = {
        "title": "",
        "description": "",
        "pages": [],
        "features": [],
        "components": [],
        "stack": {},
    }

    # Try to find title
    lines = spec.split('\n')
    for line in lines:
        if line.startswith('#') and not line.startswith('##'):
            requirements["title"] = line.replace('#', '').strip()
            break

    # Extract stack section
    if 'stack' in spec.lower() or 'technology' in spec.lower():
        requirements["stack"]["framework"] = "Laravel"
        requirements["stack"]["frontend"] = "Livewire + Alpine.js"
        requirements["stack"]["components"] = "FluxUI"
        requirements["stack"]["css"] = "Tailwind CSS"

    return requirements


def generate_basic_tasks(requirements: dict) -> list:
    """Generate basic task structure."""
    tasks = []

    # Task 1: Setup and project structure
    tasks.append({
        "number": 1,
        "name": "Project Setup and Configuration",
        "description": "Initialize Laravel project, install dependencies, configure Livewire and FluxUI",
        "acceptance_criteria": [
            "Laravel project runs without errors",
            "Livewire components load",
            "FluxUI components available",
            "Tailwind CSS configured"
        ],
        "files": [
            "composer.json",
            "config/app.php",
            "tailwind.config.js"
        ],
        "components": "Livewire, FluxUI",
        "time_estimate_minutes": 45
    })

    # Task 2: Database and models
    tasks.append({
        "number": 2,
        "name": "Database Schema and Models",
        "description": "Create database tables and Eloquent models based on specification",
        "acceptance_criteria": [
            "All required tables exist",
            "Models have correct relationships",
            "Migrations run without errors"
        ],
        "files": [
            "database/migrations/*.php",
            "app/Models/*.php"
        ],
        "components": "Laravel Eloquent",
        "time_estimate_minutes": 60
    })

    # Task 3: Authentication
    tasks.append({
        "number": 3,
        "name": "Authentication and Authorization",
        "description": "Setup user authentication and authorization",
        "acceptance_criteria": [
            "User registration works",
            "Login/logout functional",
            "Protected routes enforce authentication"
        ],
        "files": [
            "app/Models/User.php",
            "routes/web.php",
            "app/Http/Middleware/Authenticate.php"
        ],
        "components": "Laravel Auth, Livewire",
        "time_estimate_minutes": 60
    })

    return tasks


def generate_quality_checklist() -> list:
    """Generate quality checklist."""
    return [
        "All FluxUI components use supported props only",
        "No background processes in any commands",
        "No server startup commands in scripts",
        "Mobile responsive design verified",
        "Form functionality tested",
        "Images from approved sources (Unsplash, picsum.photos)",
        "No Pexels images (causes 403 errors)",
        "Playwright screenshot testing configured"
    ]


def generate_task_list(spec: str, title: str = "Development Task List") -> dict:
    """Generate complete task list from specification."""
    requirements = extract_requirements(spec)
    tasks = generate_basic_tasks(requirements)

    return {
        "project_title": requirements.get("title", title),
        "specification_summary": spec[:200] + "..." if len(spec) > 200 else spec,
        "technical_stack": {
            "framework": "Laravel 11+",
            "frontend": "Livewire v3 + Alpine.js",
            "components": "FluxUI",
            "css": "Tailwind CSS",
            "images": "Unsplash, https://picsum.photos/",
            "testing": "Playwright"
        },
        "tasks": tasks,
        "quality_checklist": generate_quality_checklist(),
        "estimated_total_hours": sum(
            t.get("time_estimate_minutes", 45) / 60 for t in tasks
        ),
        "notes": [
            "Each task should be completable in 30-60 minutes",
            "Most features will require 2-3 revision cycles",
            "Basic implementations are acceptable in first pass",
            "Focus on functional requirements before polish"
        ]
    }


def print_task_list(task_list: dict):
    """Print task list in readable format."""
    print(f"\n# {task_list['project_title']}")
    print("=" * 60)

    print(f"\n## Technical Stack")
    for key, value in task_list['technical_stack'].items():
        print(f"- **{key.title().replace('_', ' ')}**: {value}")

    print(f"\n## Development Tasks")
    print(f"\nEstimated Total: {task_list['estimated_total_hours']:.1f} hours\n")

    for task in task_list['tasks']:
        print(f"### [ ] Task {task['number']}: {task['name']}")
        print(f"**Description**: {task['description']}")
        print(f"**Time Estimate**: {task['time_estimate_minutes']} minutes")
        print(f"\n**Acceptance Criteria**:")
        for criterion in task['acceptance_criteria']:
            print(f"- {criterion}")
        print(f"\n**Files to Create/Edit**:")
        for file in task['files']:
            print(f"- {file}")
        print(f"\n**Components**: {task['components']}")
        print()

    print(f"## Quality Checklist")
    for item in task_list['quality_checklist']:
        print(f"- [ ] {item}")

    print(f"\n## Notes")
    for note in task_list['notes']:
        print(f"- {note}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert site specification to development task list",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python task_list_generator.py --spec specification.md\n"
            "  python task_list_generator.py --spec spec.md --format json\n"
            "  python task_list_generator.py --spec spec.md --format markdown"
        )
    )
    parser.add_argument("--spec", required=True, help="Path to specification file")
    parser.add_argument("--format", choices=["table", "json", "markdown"],
                        default="markdown", help="Output format")
    args = parser.parse_args()

    # Read specification
    spec = read_specification(args.spec)

    # Generate task list
    task_list = generate_task_list(spec)

    # Output
    if args.format == "json":
        print(json.dumps(task_list, indent=2))
    else:
        print_task_list(task_list)


if __name__ == "__main__":
    main()
