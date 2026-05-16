#!/usr/bin/env python3
"""Generates portfolio plans, ROI calculations, and executive review reports for studio producers."""

import sys
import json
import argparse
from datetime import date

TIER_MARGIN_TARGETS = {"tier1": 45, "tier2": 35, "tier3": 25}
STATUS_ICONS = {"on_track": "🟢", "at_risk": "🟡", "blocked": "🔴"}


def calculate_roi(revenue: float, direct_costs: float, overhead: float) -> dict:
    total_cost = direct_costs + overhead
    gross_profit = revenue - direct_costs
    net_profit = revenue - total_cost
    gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
    roi = (net_profit / total_cost * 100) if total_cost > 0 else 0
    return {
        "revenue": revenue,
        "direct_costs": direct_costs,
        "overhead": overhead,
        "total_cost": total_cost,
        "gross_profit": round(gross_profit, 2),
        "net_profit": round(net_profit, 2),
        "gross_margin_pct": round(gross_margin, 1),
        "roi_pct": round(roi, 1),
    }


def tier_health(project: dict) -> str:
    tier = project.get("tier", "tier2")
    margin = project.get("gross_margin_pct", 0)
    target = TIER_MARGIN_TARGETS.get(tier, 35)
    status = project.get("status", "on_track")
    if status == "blocked" or margin < target - 10:
        return "blocked"
    if status == "at_risk" or margin < target:
        return "at_risk"
    return "on_track"


def portfolio_summary(projects: list) -> dict:
    tier_counts = {"tier1": 0, "tier2": 0, "tier3": 0}
    total_revenue = 0
    total_costs = 0
    for p in projects:
        tier = p.get("tier", "tier2")
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        total_revenue += p.get("revenue", 0)
        total_costs += p.get("direct_costs", 0) + p.get("overhead", 0)

    gross_margin = ((total_revenue - total_costs) / total_revenue * 100) if total_revenue > 0 else 0
    return {
        "total_projects": len(projects),
        "tier_breakdown": tier_counts,
        "total_revenue": total_revenue,
        "total_costs": total_costs,
        "portfolio_margin_pct": round(gross_margin, 1),
        "projects_at_risk": sum(1 for p in projects if tier_health(p) in ["at_risk", "blocked"]),
    }


def generate_portfolio_plan(projects: list, quarter: str, year: int, producer: str) -> dict:
    by_tier = {"tier1": [], "tier2": [], "tier3": []}
    for p in projects:
        tier = p.get("tier", "tier2")
        by_tier.setdefault(tier, []).append(p)

    summary = portfolio_summary(projects)
    return {
        "quarter": quarter,
        "year": year,
        "producer": producer,
        "generated": str(date.today()),
        "summary": summary,
        "tier1_projects": by_tier["tier1"],
        "tier2_projects": by_tier["tier2"],
        "tier3_projects": by_tier["tier3"],
    }


def generate_review(projects: list, month: str, presenter: str) -> dict:
    summary = portfolio_summary(projects)
    health_dashboard = []
    for p in projects:
        health = tier_health(p)
        health_dashboard.append({
            "name": p.get("name", "Project"),
            "tier": p.get("tier", "tier2"),
            "health": health,
            "health_icon": STATUS_ICONS.get(health, "🟢"),
            "revenue": p.get("revenue", 0),
            "gross_margin_pct": p.get("gross_margin_pct", 0),
            "lead": p.get("lead", "TBD"),
        })
    return {
        "month": month,
        "presenter": presenter,
        "generated": str(date.today()),
        "headline_metrics": summary,
        "health_dashboard": health_dashboard,
    }


def print_portfolio_plan(plan: dict):
    s = plan["summary"]
    print("\nSTRATEGIC PORTFOLIO PLAN — {} {}".format(plan['quarter'], plan['year']))
    print("=" * 60)
    print(f"Producer: {plan['producer']} | Generated: {plan['generated']}")
    print("\nOVERVIEW")
    print("  Active projects:   {}  ".format(s['total_projects']) +
          "(T1: {} | ".format(s['tier_breakdown'].get('tier1', 0)) +
          "T2: {} | ".format(s['tier_breakdown'].get('tier2', 0)) +
          "T3: {})".format(s['tier_breakdown'].get('tier3', 0)))
    print(f"  Total revenue:     ${s['total_revenue']:,.0f}")
    print(f"  Portfolio margin:  {s['portfolio_margin_pct']}%")
    print(f"  Projects at risk:  {s['projects_at_risk']}")

    for tier_label, tier_key in [("TIER 1 — FLAGSHIP", "tier1_projects"),
                                 ("TIER 2 — CORE", "tier2_projects"),
                                 ("TIER 3 — PIPELINE", "tier3_projects")]:
        projects = plan.get(tier_key, [])
        if projects:
            print(f"\n{tier_label}")
            print("-" * 50)
            for p in projects:
                health = tier_health(p)
                icon = STATUS_ICONS.get(health, "🟢")
                print(f"  {icon} {p.get('name','Project')}")
                print(f"     Revenue: ${p.get('revenue',0):,.0f} | "
                      f"Margin: {p.get('gross_margin_pct',0)}% | "
                      f"Lead: {p.get('lead','TBD')}")


def print_review(review: dict):
    s = review["headline_metrics"]
    print("\nPORTFOLIO REVIEW — {}".format(review['month']))
    print("=" * 60)
    print(f"Presenter: {review['presenter']}")
    print("\nHEADLINE METRICS")
    print("  Total revenue:     ${:,.0f}".format(s['total_revenue']))
    print("  Portfolio margin:  {}%".format(s['portfolio_margin_pct']))
    print("  Projects at risk:  {}".format(s['projects_at_risk']))
    print("\nPROJECT HEALTH DASHBOARD")
    print(f"  {'Name':<30} {'Tier':<8} {'Health':<6} {'Revenue':>12} {'Margin':>8} {'Lead'}")
    print(f"  {'-'*80}")
    for p in review["health_dashboard"]:
        print(f"  {p['name']:<30} {p['tier']:<8} {p['health_icon']:<6} "
              f"${p['revenue']:>10,.0f} {p['gross_margin_pct']:>7.1f}% {p['lead']}")


def print_roi(roi: dict):
    print("\nROI ANALYSIS")
    print("=" * 40)
    print(f"  Revenue:         ${roi['revenue']:>12,.2f}")
    print(f"  Direct costs:    ${roi['direct_costs']:>12,.2f}")
    print(f"  Overhead:        ${roi['overhead']:>12,.2f}")
    print(f"  Total cost:      ${roi['total_cost']:>12,.2f}")
    print(f"  Gross profit:    ${roi['gross_profit']:>12,.2f}")
    print(f"  Net profit:      ${roi['net_profit']:>12,.2f}")
    print(f"  Gross margin:    {roi['gross_margin_pct']:>11.1f}%")
    print(f"  ROI:             {roi['roi_pct']:>11.1f}%")


def main():
    parser = argparse.ArgumentParser(
        description="Generate studio portfolio plans and ROI reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python portfolio_planner.py --projects projects.json --quarter Q2 --year 2026\n"
            "  python portfolio_planner.py --roi --revenue 150000 --costs 80000 --overhead 20000\n"
            "  python portfolio_planner.py --review projects.json --month 'May 2026'"
        )
    )
    parser.add_argument("--projects", help="Path to projects JSON file")
    parser.add_argument("--quarter", default="Q1", help="Quarter (Q1/Q2/Q3/Q4)")
    parser.add_argument("--year", type=int, default=date.today().year, help="Year")
    parser.add_argument("--producer", default="Studio Producer", help="Producer name")
    parser.add_argument("--roi", action="store_true", help="Calculate ROI for a single project")
    parser.add_argument("--revenue", type=float, help="Project revenue")
    parser.add_argument("--costs", type=float, help="Direct project costs")
    parser.add_argument("--overhead", type=float, default=0, help="Overhead allocation")
    parser.add_argument("--review", help="Path to projects JSON for portfolio review")
    parser.add_argument("--month", default=str(date.today().strftime("%B %Y")), help="Review month")
    parser.add_argument("--presenter", default="Studio Producer", help="Review presenter name")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    if args.roi and args.revenue is not None and args.costs is not None:
        roi = calculate_roi(args.revenue, args.costs, args.overhead)
        if args.format == "json":
            print(json.dumps(roi, indent=2))
        else:
            print_roi(roi)

    elif args.review:
        try:
            with open(args.review) as f:
                projects = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading projects file: {e}", file=sys.stderr)
            sys.exit(1)
        review = generate_review(projects, args.month, args.presenter)
        if args.format == "json":
            print(json.dumps(review, indent=2))
        else:
            print_review(review)

    elif args.projects:
        try:
            with open(args.projects) as f:
                projects = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading projects file: {e}", file=sys.stderr)
            sys.exit(1)
        plan = generate_portfolio_plan(projects, args.quarter, args.year, args.producer)
        if args.format == "json":
            print(json.dumps(plan, indent=2))
        else:
            print_portfolio_plan(plan)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
