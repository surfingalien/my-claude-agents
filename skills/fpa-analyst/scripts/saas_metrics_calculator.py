#!/usr/bin/env python3
"""
SaaS Metrics Calculator — ARR waterfall, NRR, GRR, CAC payback, LTV/CAC, Rule of 40.

Usage:
    python saas_metrics_calculator.py arr_data.csv
    python saas_metrics_calculator.py arr_data.csv --format json

Input CSV columns:
    period, beginning_arr, new_bookings, expansion, contraction, churn,
    sales_marketing_spend, new_customers, acv, gross_margin_pct

Output:
    - ARR waterfall per period
    - NRR and GRR
    - CAC payback (months)
    - LTV/CAC ratio
    - Rule of 40 (requires revenue_growth and fcf_margin_pct columns if available)
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
        return float(val) if val not in (None, "", "N/A") else default
    except (ValueError, TypeError):
        return default


def calculate_metrics(row, prior_row=None):
    beg_arr = safe_float(row.get("beginning_arr"))
    new_bkgs = safe_float(row.get("new_bookings"))
    expansion = safe_float(row.get("expansion"))
    contraction = safe_float(row.get("contraction"))
    churn = safe_float(row.get("churn"))
    end_arr = beg_arr + new_bkgs + expansion - contraction - churn

    sm_spend = safe_float(row.get("sales_marketing_spend"))
    new_customers = safe_float(row.get("new_customers"))
    acv = safe_float(row.get("acv"))
    gm_pct = safe_float(row.get("gross_margin_pct"), default=0.70)

    nrr = ((beg_arr + expansion - contraction - churn) / beg_arr * 100) if beg_arr else None
    grr = ((beg_arr - contraction - churn) / beg_arr * 100) if beg_arr else None

    cac = (sm_spend / new_customers) if new_customers else None
    cac_payback_months = (cac / (acv * gm_pct / 12)) if (cac and acv and gm_pct) else None

    ltv = (acv * gm_pct / (1 - (nrr / 100))) if (acv and gm_pct and nrr and nrr < 100) else None
    ltv_cac = (ltv / cac) if (ltv and cac) else None

    revenue_growth = safe_float(row.get("revenue_growth_pct"))
    fcf_margin = safe_float(row.get("fcf_margin_pct"))
    rule_of_40 = (revenue_growth + fcf_margin) if (revenue_growth or fcf_margin) else None

    return {
        "period": row.get("period"),
        "arr_waterfall": {
            "beginning_arr": round(beg_arr, 1),
            "new_bookings": round(new_bkgs, 1),
            "expansion": round(expansion, 1),
            "contraction": round(-contraction, 1),
            "churn": round(-churn, 1),
            "ending_arr": round(end_arr, 1),
        },
        "retention": {
            "nrr_pct": round(nrr, 1) if nrr is not None else None,
            "grr_pct": round(grr, 1) if grr is not None else None,
        },
        "unit_economics": {
            "cac": round(cac, 0) if cac else None,
            "cac_payback_months": round(cac_payback_months, 1) if cac_payback_months else None,
            "ltv": round(ltv, 0) if ltv else None,
            "ltv_cac_ratio": round(ltv_cac, 1) if ltv_cac else None,
        },
        "rule_of_40": round(rule_of_40, 1) if rule_of_40 is not None else None,
    }


def print_table(all_metrics):
    print(f"\n{'='*70}")
    print("  SaaS Metrics Dashboard")
    print(f"{'='*70}")

    for m in all_metrics:
        period = m.get("period", "N/A")
        wf = m.get("arr_waterfall", {})
        ret = m.get("retention", {})
        ue = m.get("unit_economics", {})
        r40 = m.get("rule_of_40")

        print(f"\n  Period: {period}")
        print(f"  {'─'*50}")
        print(f"  ARR Waterfall")
        print(f"    Beginning ARR:    ${wf.get('beginning_arr', 0):>10,.1f}K")
        print(f"    + New Bookings:   ${wf.get('new_bookings', 0):>10,.1f}K")
        print(f"    + Expansion:      ${wf.get('expansion', 0):>10,.1f}K")
        print(f"    - Contraction:    ${abs(wf.get('contraction', 0)):>10,.1f}K")
        print(f"    - Churn:          ${abs(wf.get('churn', 0)):>10,.1f}K")
        print(f"    {'─'*36}")
        print(f"    Ending ARR:       ${wf.get('ending_arr', 0):>10,.1f}K")

        print(f"\n  Retention")
        nrr = ret.get("nrr_pct")
        grr = ret.get("grr_pct")
        print(f"    NRR: {nrr}%   GRR: {grr}%")

        print(f"\n  Unit Economics")
        cac = ue.get("cac")
        payback = ue.get("cac_payback_months")
        ltv_cac = ue.get("ltv_cac_ratio")
        if cac:
            print(f"    CAC: ${cac:,.0f}   Payback: {payback} months   LTV/CAC: {ltv_cac}x")

        if r40 is not None:
            status = "✓ Passing" if r40 >= 40 else "✗ Below target"
            print(f"\n  Rule of 40: {r40:.1f}  {status}")


def main():
    parser = argparse.ArgumentParser(description="SaaS Metrics Calculator")
    parser.add_argument("arr_data", help="CSV file with ARR and metrics data")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    rows = load_csv(args.arr_data)
    all_metrics = []
    for i, row in enumerate(rows):
        prior = rows[i - 1] if i > 0 else None
        all_metrics.append(calculate_metrics(row, prior))

    if args.format == "json":
        print(json.dumps(all_metrics, indent=2))
    else:
        print_table(all_metrics)


if __name__ == "__main__":
    main()
