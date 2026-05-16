#!/usr/bin/env python3
"""
Reconciliation Tracker — tracks month-end account reconciliation status across all balance sheet accounts.

Usage:
    python reconciliation_tracker.py accounts.csv
    python reconciliation_tracker.py accounts.csv --period "Jan 2026" --format json

Input CSV columns:
    account_number, account_name, gl_balance, subledger_balance, preparer, reviewer, status
    status: Complete | In Progress | Not Started

Output:
    - Reconciliation status summary
    - Open items requiring attention
    - Unreconciled difference report
"""

import argparse
import csv
import json
import sys


def load_csv(path):
    try:
        with open(path, newline="") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.", file=sys.stderr)
        sys.exit(1)


def safe_float(val, default=0.0):
    try:
        return float(val) if val not in (None, "") else default
    except (ValueError, TypeError):
        return default


def analyze_reconciliations(rows):
    results = []
    totals = {"complete": 0, "in_progress": 0, "not_started": 0, "unreconciled": 0}

    for row in rows:
        gl = safe_float(row.get("gl_balance"))
        sub = safe_float(row.get("subledger_balance"))
        diff = gl - sub
        status = row.get("status", "Not Started").strip()

        status_norm = status.lower().replace(" ", "_")
        if "complete" in status_norm:
            totals["complete"] += 1
        elif "progress" in status_norm:
            totals["in_progress"] += 1
        else:
            totals["not_started"] += 1

        if abs(diff) > 0.01:
            totals["unreconciled"] += 1

        results.append({
            "account_number": row.get("account_number", ""),
            "account_name": row.get("account_name", ""),
            "gl_balance": round(gl, 2),
            "subledger_balance": round(sub, 2),
            "difference": round(diff, 2),
            "reconciled": abs(diff) <= 0.01,
            "preparer": row.get("preparer", "—"),
            "reviewer": row.get("reviewer", "—"),
            "status": status,
        })

    total_accounts = len(results)
    completion_pct = (totals["complete"] / total_accounts * 100) if total_accounts else 0

    return results, totals, round(completion_pct, 1)


def print_table(results, totals, completion_pct, period):
    print(f"\n{'='*90}")
    print(f"  Reconciliation Status Report — {period}")
    print(f"{'='*90}")

    print(f"\n  Summary: {totals['complete']}/{len(results)} complete ({completion_pct}%)")
    print(f"  In Progress: {totals['in_progress']}  |  Not Started: {totals['not_started']}  |  Unreconciled Differences: {totals['unreconciled']}")

    header = f"\n  {'Acct #':<10}{'Account Name':<30}{'GL Balance':>14}{'Subledger':>14}{'Difference':>14}{'Status':<18}{'Preparer'}"
    print(header)
    print(f"  {'-'*9}{'-'*30}{'-'*14}{'-'*14}{'-'*14}{'-'*18}{'-'*15}")

    needs_attention = []
    for r in results:
        diff = r["difference"]
        status = r["status"]
        flag = " ⚠" if abs(diff) > 0.01 or "Not Started" in status else ""
        if flag:
            needs_attention.append(r)
        print(f"  {r['account_number']:<10}{r['account_name']:<30}{r['gl_balance']:>14,.2f}{r['subledger_balance']:>14,.2f}{diff:>+14,.2f}  {status:<16}{r['preparer']}{flag}")

    if needs_attention:
        print(f"\n{'─'*90}")
        print(f"  ITEMS REQUIRING ATTENTION ({len(needs_attention)})")
        print(f"{'─'*90}")
        for r in needs_attention:
            diff_str = f"  Difference: ${r['difference']:+,.2f}" if abs(r["difference"]) > 0.01 else ""
            print(f"  {r['account_number']} {r['account_name']:<28} Status: {r['status']}{diff_str}")


def main():
    parser = argparse.ArgumentParser(description="Account Reconciliation Tracker")
    parser.add_argument("accounts", help="CSV file with account reconciliation data")
    parser.add_argument("--period", default="Current Period", help='Period label (e.g., "Jan 2026")')
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    rows = load_csv(args.accounts)
    results, totals, completion_pct = analyze_reconciliations(rows)

    if args.format == "json":
        output = {
            "period": args.period,
            "summary": {**totals, "total_accounts": len(results), "completion_pct": completion_pct},
            "accounts": results,
        }
        print(json.dumps(output, indent=2))
    else:
        print_table(results, totals, completion_pct, args.period)


if __name__ == "__main__":
    main()
