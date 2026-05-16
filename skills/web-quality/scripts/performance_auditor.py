#!/usr/bin/env python3
"""
Parse a Lighthouse JSON report and surface actionable performance findings.
Usage: python performance_auditor.py <report.json> [--category CATEGORY] [--json]
"""
import argparse
import json
import sys
from typing import Any


CATEGORIES = ["performance", "accessibility", "best-practices", "seo"]

CWV_AUDITS = {
    "largest-contentful-paint": ("LCP", 2500, 4000),
    "total-blocking-time": ("TBT proxy for INP", 200, 600),
    "cumulative-layout-shift": ("CLS", 0.1, 0.25),
    "first-contentful-paint": ("FCP", 1800, 3000),
    "speed-index": ("Speed Index", 3400, 5800),
    "interactive": ("TTI", 3800, 7300),
}


def score_label(score: float | None) -> str:
    if score is None:
        return "n/a"
    pct = round(score * 100)
    if pct >= 90:
        return f"GOOD  ({pct})"
    if pct >= 50:
        return f"FAIR  ({pct})"
    return f"POOR  ({pct})"


def format_value(audit: dict) -> str:
    display = audit.get("displayValue", "")
    if display:
        return display
    numeric = audit.get("numericValue")
    if numeric is not None:
        unit = audit.get("numericUnit", "")
        return f"{numeric:.0f} {unit}".strip()
    return "-"


def cwv_status(audit_id: str, numeric_value: float | None) -> str:
    if audit_id not in CWV_AUDITS or numeric_value is None:
        return ""
    _, good, poor = CWV_AUDITS[audit_id]
    if numeric_value <= good:
        return " ✓"
    if numeric_value <= poor:
        return " ~"
    return " ✗"


def audit_opportunities(audits: dict) -> list[dict]:
    opps = []
    for audit_id, audit in audits.items():
        if audit.get("scoreDisplayMode") in ("notApplicable", "manual", "informative"):
            continue
        score = audit.get("score")
        if score is not None and score < 0.9:
            opps.append({
                "id": audit_id,
                "title": audit.get("title", audit_id),
                "score": score,
                "value": format_value(audit),
                "description": audit.get("description", ""),
            })
    opps.sort(key=lambda x: x["score"] if x["score"] is not None else 1.0)
    return opps


def run(report_path: str, category_filter: str | None, as_json: bool) -> None:
    try:
        with open(report_path) as f:
            report = json.load(f)
    except FileNotFoundError:
        print(f"Error: file not found: {report_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    categories = report.get("categories", {})
    audits = report.get("audits", {})
    url = report.get("finalUrl", report.get("requestedUrl", "unknown"))

    if as_json:
        result: dict[str, Any] = {"url": url, "categories": {}, "opportunities": []}
        for cat_id, cat in categories.items():
            if category_filter and cat_id != category_filter:
                continue
            result["categories"][cat_id] = round((cat.get("score") or 0) * 100)
        result["opportunities"] = audit_opportunities(audits)[:10]
        print(json.dumps(result, indent=2))
        return

    print(f"\n{'='*60}")
    print(f"Lighthouse Report: {url}")
    print(f"{'='*60}\n")

    print("Category Scores")
    print("-" * 40)
    for cat_id, cat in categories.items():
        if category_filter and cat_id != category_filter:
            continue
        print(f"  {cat.get('title', cat_id):<30} {score_label(cat.get('score'))}")
    print()

    print("Core Web Vitals")
    print("-" * 40)
    for audit_id, (label, _, _) in CWV_AUDITS.items():
        audit = audits.get(audit_id, {})
        val = format_value(audit)
        status = cwv_status(audit_id, audit.get("numericValue"))
        print(f"  {label:<35} {val}{status}")
    print()

    opps = audit_opportunities(audits)
    if opps:
        print("Top Opportunities (lowest scoring)")
        print("-" * 40)
        for opp in opps[:8]:
            score_pct = round((opp["score"] or 0) * 100)
            print(f"  [{score_pct:>3}] {opp['title']}")
            if opp["value"] and opp["value"] != "-":
                print(f"        → {opp['value']}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a Lighthouse JSON report")
    parser.add_argument("report", help="Path to Lighthouse JSON report")
    parser.add_argument("--category", choices=CATEGORIES, help="Filter to one category")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    run(args.report, args.category, args.json)


if __name__ == "__main__":
    main()
