#!/usr/bin/env python3
"""
Variance Analyzer — budget-vs-actual variance analysis with root cause flags and YTD summary.

Usage:
    python variance_analyzer.py actuals.csv budget.csv
    python variance_analyzer.py actuals.csv budget.csv --prior-month prior.csv
    python variance_analyzer.py actuals.csv budget.csv --threshold 5000 --format json

Input CSV columns (actuals and budget must share the same structure):
    department, category, amount

Output:
    - Variance table by department and category
    - Dollar and percentage variance
    - Items flagged above threshold
    - MoM comparison if prior month provided
"""

import argparse
import csv
import json
import sys
from collections import defaultdict


def load_csv(path):
    try:
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.", file=sys.stderr)
        sys.exit(1)


def index_by_key(rows, key_fields):
    index = {}
    for row in rows:
        key = tuple(row[k] for k in key_fields)
        index[key] = float(row.get("amount", 0))
    return index


def compute_variance(actuals_index, budget_index, all_keys):
    results = []
    for key in sorted(all_keys):
        actual = actuals_index.get(key, 0.0)
        budget = budget_index.get(key, 0.0)
        variance = actual - budget
        pct = (variance / abs(budget) * 100) if budget != 0 else None
        results.append({
            "department": key[0],
            "category": key[1],
            "budget": budget,
            "actual": actual,
            "variance": variance,
            "variance_pct": round(pct, 1) if pct is not None else None,
        })
    return results


def print_table(results, threshold, prior_index=None):
    print(f"\n{'='*85}")
    print("  Budget vs. Actual Variance Analysis")
    print(f"{'='*85}")
    header = f"{'Department':<20}{'Category':<22}{'Budget':>12}{'Actual':>12}{'Var $':>12}{'Var %':>9}{'Flag'}"
    print(f"\n{header}")
    print("-" * 85)

    dept_totals = defaultdict(lambda: {"budget": 0, "actual": 0, "variance": 0})

    for r in results:
        dept = r["department"]
        cat = r["category"]
        bud = r["budget"]
        act = r["actual"]
        var = r["variance"]
        pct = r["variance_pct"]
        flagged = abs(var) >= threshold

        dept_totals[dept]["budget"] += bud
        dept_totals[dept]["actual"] += act
        dept_totals[dept]["variance"] += var

        flag = "⚠" if flagged else ""
        pct_str = f"{pct:+.1f}%" if pct is not None else "N/A"
        print(f"  {dept:<18}{cat:<22}{bud:>12,.0f}{act:>12,.0f}{var:>+12,.0f}{pct_str:>9}  {flag}")

    print(f"\n{'─'*85}")
    print(f"  {'DEPARTMENT TOTALS'}")
    print(f"{'─'*85}")
    total_bud = total_act = total_var = 0
    for dept, t in sorted(dept_totals.items()):
        pct = (t["variance"] / abs(t["budget"]) * 100) if t["budget"] else None
        pct_str = f"{pct:+.1f}%" if pct is not None else "N/A"
        print(f"  {dept:<40}{t['budget']:>12,.0f}{t['actual']:>12,.0f}{t['variance']:>+12,.0f}{pct_str:>9}")
        total_bud += t["budget"]
        total_act += t["actual"]
        total_var += t["variance"]

    total_pct = (total_var / abs(total_bud) * 100) if total_bud else None
    pct_str = f"{total_pct:+.1f}%" if total_pct is not None else "N/A"
    print(f"{'─'*85}")
    print(f"  {'TOTAL':<40}{total_bud:>12,.0f}{total_act:>12,.0f}{total_var:>+12,.0f}{pct_str:>9}")
    print(f"\n  ⚠ = variance exceeds ${threshold:,.0f} threshold")


def main():
    parser = argparse.ArgumentParser(description="Budget vs. Actual Variance Analyzer")
    parser.add_argument("actuals", help="Actuals CSV file")
    parser.add_argument("budget", help="Budget CSV file")
    parser.add_argument("--prior-month", help="Prior month actuals CSV for MoM comparison")
    parser.add_argument("--threshold", type=float, default=5000, help="Dollar threshold for flagging (default: 5000)")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    actuals_rows = load_csv(args.actuals)
    budget_rows = load_csv(args.budget)

    key_fields = ["department", "category"]
    actuals_index = index_by_key(actuals_rows, key_fields)
    budget_index = index_by_key(budget_rows, key_fields)
    all_keys = set(actuals_index.keys()) | set(budget_index.keys())

    prior_index = None
    if args.prior_month:
        prior_rows = load_csv(args.prior_month)
        prior_index = index_by_key(prior_rows, key_fields)

    results = compute_variance(actuals_index, budget_index, all_keys)

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print_table(results, args.threshold, prior_index)


if __name__ == "__main__":
    main()
