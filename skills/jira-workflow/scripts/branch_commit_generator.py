#!/usr/bin/env python3
"""Generates valid branch names and commit messages from Jira IDs and descriptions."""

import sys
import json
import re
import argparse

BRANCH_TYPES = ["feature", "bugfix", "hotfix", "chore", "release"]

GITMOJI_MAP = {
    "feature": ("✨", "add"),
    "bugfix": ("🐛", "fix"),
    "hotfix": ("🐛", "fix"),
    "chore": ("🔧", "update"),
    "refactor": ("♻️", "refactor"),
    "docs": ("📚", "document"),
    "test": ("🧪", "test"),
    "style": ("💄", "style"),
    "perf": ("⚡", "improve"),
    "security": ("🔒", "secure"),
    "deps": ("📦", "upgrade"),
    "release": ("🚀", "release"),
}

JIRA_PATTERN = re.compile(r'^[A-Z]+-[0-9]+$')
BRANCH_PATTERN = re.compile(
    r'^(feature|bugfix|hotfix|chore)/[A-Z]+-[0-9]+-[a-z0-9-]+$|^release/[0-9]+\.[0-9]+\.[0-9]+$'
)
COMMIT_PATTERN = re.compile(
    r'^(🚀|✨|🐛|♻️|📚|🧪|💄|🔧|📦|🔒|⚡|🗑️) [A-Z]+-[0-9]+: .+'
)


def slugify(text: str) -> str:
    """Convert description to branch-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text).strip('-')
    return text[:40]


def generate_branch(jira_id: str, branch_type: str, description: str) -> str:
    if not JIRA_PATTERN.match(jira_id):
        raise ValueError(f"Invalid Jira ID format: {jira_id}. Expected: PROJECT-123")
    if branch_type not in BRANCH_TYPES:
        raise ValueError(f"Invalid branch type: {branch_type}. Choose: {', '.join(BRANCH_TYPES)}")
    slug = slugify(description)
    return f"{branch_type}/{jira_id}-{slug}"


def generate_commit(jira_id: str, branch_type: str, description: str) -> str:
    if not JIRA_PATTERN.match(jira_id):
        raise ValueError(f"Invalid Jira ID format: {jira_id}")
    emoji, verb = GITMOJI_MAP.get(branch_type, ("✨", "add"))
    # Ensure description starts with imperative verb
    desc = description.strip().rstrip('.')
    if not any(desc.lower().startswith(v) for v in [verb, "add", "fix", "update", "remove", "refactor"]):
        desc = f"{verb} {desc}"
    return f"{emoji} {jira_id}: {desc}"


def generate_pr_template(jira_id: str, jira_base_url: str = "https://yourorg.atlassian.net") -> str:
    return f"""## What does this PR do?

Closes [{jira_id}]({jira_base_url}/browse/{jira_id})

### Summary
<!-- 2-3 sentences describing the change -->

### Changes
- [ ]
- [ ]
- [ ]

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass locally
- [ ] Manual testing completed

### Screenshots (if UI change)
<!-- Before / After -->

### Checklist
- [ ] Code follows project style guide
- [ ] Self-review completed
- [ ] No sensitive data in code/logs
- [ ] Documentation updated if needed
"""


def validate_branch(branch: str) -> dict:
    valid = bool(BRANCH_PATTERN.match(branch))
    issues = []
    if not valid:
        if '/' not in branch:
            issues.append("Missing type prefix (feature/, bugfix/, hotfix/, chore/, release/)")
        elif not re.search(r'[A-Z]+-[0-9]+', branch) and not branch.startswith('release/'):
            issues.append("Missing Jira ID (e.g. PROJ-123)")
        elif re.search(r'[A-Z]', branch.split('/')[-1]):
            issues.append("Description must be lowercase")
        else:
            issues.append("Does not match pattern: type/PROJ-123-description")
    return {"branch": branch, "valid": valid, "issues": issues}


def validate_commit(subject: str) -> dict:
    valid = bool(COMMIT_PATTERN.match(subject))
    issues = []
    if not valid:
        if not re.match(r'^(🚀|✨|🐛|♻️|📚|🧪|💄|🔧|📦|🔒|⚡|🗑️)', subject):
            issues.append("Must start with a Gitmoji")
        if not re.search(r'[A-Z]+-[0-9]+:', subject):
            issues.append("Must include Jira ID followed by colon (e.g. PROJ-123:)")
    return {"commit": subject, "valid": valid, "issues": issues}


def main():
    parser = argparse.ArgumentParser(
        description="Generate Jira-linked Git branch names and commit messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python branch_commit_generator.py --jira AUTH-214 --type feature --desc 'add SSO login'\n"
            "  python branch_commit_generator.py --validate --branch 'feature/AUTH-214-add-sso'\n"
            "  python branch_commit_generator.py --pr-template --jira AUTH-214 --format json"
        )
    )
    parser.add_argument("--jira", help="Jira ticket ID (e.g. AUTH-214)")
    parser.add_argument("--type", dest="branch_type", default="feature",
                        choices=BRANCH_TYPES, help="Branch type")
    parser.add_argument("--desc", help="Short description of the change")
    parser.add_argument("--validate", action="store_true", help="Validate existing branch/commit")
    parser.add_argument("--branch", help="Branch name to validate")
    parser.add_argument("--commit", help="Commit subject to validate")
    parser.add_argument("--pr-template", action="store_true", help="Generate PR description template")
    parser.add_argument("--jira-url", default="https://yourorg.atlassian.net",
                        help="Jira base URL for PR links")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    if args.validate:
        results = {}
        if args.branch:
            results["branch_validation"] = validate_branch(args.branch)
        if args.commit:
            results["commit_validation"] = validate_commit(args.commit)
        if not results:
            print("Error: --validate requires --branch and/or --commit", file=sys.stderr)
            sys.exit(1)
        if args.format == "json":
            print(json.dumps(results, indent=2))
        else:
            for key, r in results.items():
                label = "Branch" if "branch" in key else "Commit"
                status = "✓ VALID" if r["valid"] else "✗ INVALID"
                print(f"{label}: {list(r.values())[0]}")
                print(f"Status: {status}")
                for issue in r.get("issues", []):
                    print(f"  Issue: {issue}")

    elif args.pr_template and args.jira:
        tmpl = generate_pr_template(args.jira, args.jira_url)
        if args.format == "json":
            print(json.dumps({"pr_template": tmpl}, indent=2))
        else:
            print(tmpl)

    elif args.jira and args.desc:
        try:
            branch = generate_branch(args.jira, args.branch_type, args.desc)
            commit = generate_commit(args.jira, args.branch_type, args.desc)
            result = {
                "branch_name": branch,
                "commit_message": commit,
                "git_commands": [
                    f"git checkout -b {branch}",
                    f'git commit -m "{commit}"',
                ]
            }
            if args.format == "json":
                print(json.dumps(result, indent=2))
            else:
                print(f"\nBranch name:     {branch}")
                print(f"Commit message:  {commit}")
                print("\nGit commands:")
                for cmd in result["git_commands"]:
                    print(f"  {cmd}")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
