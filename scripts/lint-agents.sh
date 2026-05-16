#!/usr/bin/env bash
#
# lint-agents.sh — Validate agent markdown files.
#
#   1. YAML frontmatter must exist with name, description, domain (ERROR)
#   2. Recommended sections checked but only warned (WARN)
#   3. File must have meaningful content (WARN if < 50 words)
#
# Usage: ./scripts/lint-agents.sh [file ...]
#   If no files given, scans all agent directories.

set -euo pipefail

# Agent directories — keep in sync with convert.sh / install.sh
AGENT_DIRS=(
  agents
  business-growth
  c-level
  engineering
  engineering-team
  finance
  marketing
  product
  project-management
  ra-qm-team
)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Required YAML frontmatter fields for cs-* agents
REQUIRED_FRONTMATTER=("name" "description" "domain")

# Recommended markdown sections (warns if absent)
RECOMMENDED_SECTIONS=("Purpose" "Skill Integration" "Workflows")

errors=0
warnings=0

lint_file() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    echo "ERROR $file: not a file or does not exist"
    (( errors++ )) || true
    return
  fi

  # 1. Check frontmatter delimiters
  local first_line
  first_line=$(head -1 "$file")
  if [[ "$first_line" != "---" ]]; then
    echo "ERROR $file: missing frontmatter opening ---"
    (( errors++ )) || true
    return
  fi

  # Extract frontmatter (between first and second ---)
  local frontmatter
  frontmatter=$(awk 'NR==1{next} /^---$/{exit} {print}' "$file")

  if [[ -z "$frontmatter" ]]; then
    echo "ERROR $file: empty or malformed frontmatter"
    (( errors++ )) || true
    return
  fi

  # 2. Check required frontmatter fields
  for field in "${REQUIRED_FRONTMATTER[@]}"; do
    if ! echo "$frontmatter" | grep -qE "^${field}:"; then
      echo "ERROR $file: missing frontmatter field '${field}'"
      (( errors++ )) || true
    fi
  done

  # 3. Check recommended sections (warn only)
  local body
  body=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2{print}' "$file")

  for section in "${RECOMMENDED_SECTIONS[@]}"; do
    if ! echo "$body" | grep -qi "$section"; then
      echo "WARN  $file: missing recommended section '${section}'"
      (( warnings++ )) || true
    fi
  done

  # 4. Check file has meaningful content
  local word_count
  word_count=$(echo "$body" | wc -w | awk '{print $1}')
  if [[ "${word_count:-0}" -lt 50 ]]; then
    echo "WARN  $file: body seems very short (< 50 words)"
    (( warnings++ )) || true
  fi

  # 5. Check that at least 3 workflow sections are documented
  local workflow_count
  workflow_count=$(echo "$body" | grep -ciE "^### Workflow [0-9]" || true)
  if [[ "${workflow_count:-0}" -lt 3 ]]; then
    echo "WARN  $file: fewer than 3 documented workflows (found ${workflow_count:-0})"
    (( warnings++ )) || true
  fi
}

# Collect files to lint
files=()
if [[ $# -gt 0 ]]; then
  files=("$@")
else
  for dir in "${AGENT_DIRS[@]}"; do
    local_dir="$REPO_ROOT/$dir"
    if [[ -d "$local_dir" ]]; then
      while IFS= read -r f; do
        files+=("$f")
      done < <(find "$local_dir" -name "*.md" -type f | sort)
    fi
  done
fi

if [[ ${#files[@]} -eq 0 ]]; then
  echo "No agent files found."
  exit 1
fi

echo "Linting ${#files[@]} agent files..."
echo ""

for file in "${files[@]}"; do
  lint_file "$file"
done

echo ""
echo "Results: ${errors} error(s), ${warnings} warning(s) in ${#files[@]} files."

if [[ $errors -gt 0 ]]; then
  echo "FAILED: fix the errors above before merging."
  exit 1
else
  echo "PASSED"
  exit 0
fi
