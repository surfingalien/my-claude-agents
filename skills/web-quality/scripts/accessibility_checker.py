#!/usr/bin/env python3
"""
Parse axe-core or Lighthouse accessibility JSON and group violations by impact.
Usage: python accessibility_checker.py <results.json> [--source axe|lighthouse] [--min-impact LEVEL] [--json]

Generate input:
  axe-core:   npx axe https://example.com --save axe-results.json
  lighthouse: npx lighthouse https://example.com --output json --output-path report.json
"""
import argparse
import json
import sys


IMPACT_ORDER = ["critical", "serious", "moderate", "minor"]


def parse_axe(data: dict, min_impact: str) -> list[dict]:
    min_idx = IMPACT_ORDER.index(min_impact) if min_impact in IMPACT_ORDER else len(IMPACT_ORDER)
    violations = []
    for v in data.get("violations", []):
        impact = v.get("impact", "minor")
        if IMPACT_ORDER.index(impact) > min_idx:
            continue
        violations.append({
            "id": v.get("id"),
            "impact": impact,
            "description": v.get("description", ""),
            "help": v.get("help", ""),
            "help_url": v.get("helpUrl", ""),
            "nodes": len(v.get("nodes", [])),
            "wcag": [tag for tag in v.get("tags", []) if tag.startswith("wcag")],
        })
    return violations


def parse_lighthouse(data: dict, min_impact: str) -> list[dict]:
    # Lighthouse maps score 0 → fail, 1 → pass, null → not applicable
    audits = data.get("audits", {})
    cat_a11y = data.get("categories", {}).get("accessibility", {})
    audit_refs = [r["id"] for r in cat_a11y.get("auditRefs", [])]

    violations = []
    for audit_id in audit_refs:
        audit = audits.get(audit_id, {})
        if audit.get("score") in (1, None) or audit.get("scoreDisplayMode") in ("notApplicable", "manual"):
            continue
        score = audit.get("score", 0)
        # Map score to impact level
        if score == 0:
            impact = "critical"
        elif score < 0.5:
            impact = "serious"
        elif score < 0.9:
            impact = "moderate"
        else:
            impact = "minor"

        min_idx = IMPACT_ORDER.index(min_impact) if min_impact in IMPACT_ORDER else len(IMPACT_ORDER)
        if IMPACT_ORDER.index(impact) > min_idx:
            continue

        items = audit.get("details", {}).get("items", [])
        violations.append({
            "id": audit_id,
            "impact": impact,
            "description": audit.get("description", ""),
            "help": audit.get("title", ""),
            "help_url": f"https://dequeuniversity.com/rules/axe/4.9/{audit_id}",
            "nodes": len(items),
            "wcag": [],
        })
    return violations


def run(path: str, source: str, min_impact: str, as_json: bool) -> None:
    try:
        with open(path) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if source == "lighthouse":
        violations = parse_lighthouse(data, min_impact)
    else:
        violations = parse_axe(data, min_impact)

    violations.sort(key=lambda v: IMPACT_ORDER.index(v["impact"]) if v["impact"] in IMPACT_ORDER else 99)

    if as_json:
        print(json.dumps({"source": source, "min_impact": min_impact,
                          "total": len(violations), "violations": violations}, indent=2))
        return

    url = data.get("finalUrl") or data.get("url") or path
    print(f"\n{'='*60}")
    print(f"Accessibility Audit ({source}): {url}")
    print(f"{'='*60}\n")

    if not violations:
        print(f"  No violations at or above '{min_impact}' impact level.\n")
        return

    by_impact: dict[str, list] = {level: [] for level in IMPACT_ORDER}
    for v in violations:
        by_impact.setdefault(v["impact"], []).append(v)

    for level in IMPACT_ORDER:
        group = by_impact.get(level, [])
        if not group:
            continue
        print(f"{level.upper()} ({len(group)})")
        print("-" * 50)
        for v in group:
            nodes = f" [{v['nodes']} element(s)]" if v["nodes"] else ""
            print(f"  {v['id']}{nodes}")
            print(f"    {v['help']}")
            if v["wcag"]:
                print(f"    WCAG: {', '.join(v['wcag'])}")
            if v["help_url"]:
                print(f"    Ref:  {v['help_url']}")
        print()

    print(f"Total violations: {len(violations)}")
    critical = len(by_impact.get("critical", []))
    serious = len(by_impact.get("serious", []))
    if critical + serious > 0:
        print(f"  {critical} critical + {serious} serious — fix these first (WCAG 2.1 AA)")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse accessibility audit results")
    parser.add_argument("results", help="Path to axe-core or Lighthouse JSON")
    parser.add_argument("--source", choices=["axe", "lighthouse"], default="axe")
    parser.add_argument("--min-impact", choices=IMPACT_ORDER, default="minor",
                        dest="min_impact", help="Minimum impact level to report")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    run(args.results, args.source, args.min_impact, args.json)


if __name__ == "__main__":
    main()
