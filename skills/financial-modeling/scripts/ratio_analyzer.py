#!/usr/bin/env python3
"""
Financial Ratio Analyzer — calculates profitability, leverage, efficiency, and growth ratios.

Usage:
    python ratio_analyzer.py financials.csv
    python ratio_analyzer.py financials.csv --benchmark industry.csv
    python ratio_analyzer.py financials.csv --format json

Input CSV columns (required):
    year, revenue, cogs, gross_profit, ebitda, ebit, net_income,
    total_assets, total_debt, cash, equity, capex, working_capital,
    interest_expense (optional)
"""

import argparse
import csv
import json
import sys


def safe_div(numerator, denominator):
    if denominator == 0 or denominator is None:
        return None
    return numerator / denominator


def calculate_ratios(row, prior_row=None):
    try:
        revenue = float(row.get("revenue", 0))
        cogs = float(row.get("cogs", 0))
        gross_profit = float(row.get("gross_profit", revenue - cogs))
        ebitda = float(row.get("ebitda", 0))
        ebit = float(row.get("ebit", 0))
        net_income = float(row.get("net_income", 0))
        total_assets = float(row.get("total_assets", 0))
        total_debt = float(row.get("total_debt", 0))
        cash = float(row.get("cash", 0))
        equity = float(row.get("equity", 0))
        capex = float(row.get("capex", 0))
        working_capital = float(row.get("working_capital", 0))
        interest_expense = float(row.get("interest_expense", 0))
        net_debt = total_debt - cash
    except (ValueError, TypeError) as e:
        print(f"Error parsing row: {e}", file=sys.stderr)
        return {}

    ratios = {
        "year": row.get("year"),
        "profitability": {
            "gross_margin_pct": round(safe_div(gross_profit, revenue) * 100, 1) if safe_div(gross_profit, revenue) else None,
            "ebitda_margin_pct": round(safe_div(ebitda, revenue) * 100, 1) if safe_div(ebitda, revenue) else None,
            "ebit_margin_pct": round(safe_div(ebit, revenue) * 100, 1) if safe_div(ebit, revenue) else None,
            "net_margin_pct": round(safe_div(net_income, revenue) * 100, 1) if safe_div(net_income, revenue) else None,
            "roe_pct": round(safe_div(net_income, equity) * 100, 1) if safe_div(net_income, equity) else None,
            "roa_pct": round(safe_div(net_income, total_assets) * 100, 1) if safe_div(net_income, total_assets) else None,
        },
        "leverage": {
            "net_debt_ebitda": round(safe_div(net_debt, ebitda), 2) if safe_div(net_debt, ebitda) is not None else None,
            "debt_equity": round(safe_div(total_debt, equity), 2) if safe_div(total_debt, equity) is not None else None,
            "interest_coverage": round(safe_div(ebit, interest_expense), 1) if interest_expense and safe_div(ebit, interest_expense) is not None else "N/A",
        },
        "efficiency": {
            "asset_turnover": round(safe_div(revenue, total_assets), 2) if safe_div(revenue, total_assets) else None,
            "capex_pct_revenue": round(safe_div(capex, revenue) * 100, 1) if safe_div(capex, revenue) else None,
            "wc_pct_revenue": round(safe_div(working_capital, revenue) * 100, 1) if safe_div(working_capital, revenue) else None,
        },
    }

    if prior_row:
        try:
            prior_revenue = float(prior_row.get("revenue", 0))
            prior_ebitda = float(prior_row.get("ebitda", 0))
            prior_net_income = float(prior_row.get("net_income", 0))
            ratios["growth"] = {
                "revenue_growth_pct": round(safe_div(revenue - prior_revenue, prior_revenue) * 100, 1) if safe_div(revenue - prior_revenue, prior_revenue) is not None else None,
                "ebitda_growth_pct": round(safe_div(ebitda - prior_ebitda, abs(prior_ebitda)) * 100, 1) if prior_ebitda and safe_div(ebitda - prior_ebitda, abs(prior_ebitda)) is not None else None,
                "net_income_growth_pct": round(safe_div(net_income - prior_net_income, abs(prior_net_income)) * 100, 1) if prior_net_income and safe_div(net_income - prior_net_income, abs(prior_net_income)) is not None else None,
            }
        except (ValueError, TypeError):
            pass

    return ratios


def print_ratios_table(all_ratios):
    years = [r.get("year", "N/A") for r in all_ratios]
    header = f"{'Metric':<35}" + "".join(f"{str(y):<14}" for y in years)
    print(f"\n{'='*80}")
    print("  Financial Ratio Analysis")
    print(f"{'='*80}")

    sections = [
        ("Profitability", "profitability", [
            ("Gross Margin %", "gross_margin_pct"),
            ("EBITDA Margin %", "ebitda_margin_pct"),
            ("EBIT Margin %", "ebit_margin_pct"),
            ("Net Margin %", "net_margin_pct"),
            ("ROE %", "roe_pct"),
            ("ROA %", "roa_pct"),
        ]),
        ("Leverage", "leverage", [
            ("Net Debt / EBITDA", "net_debt_ebitda"),
            ("Debt / Equity", "debt_equity"),
            ("Interest Coverage (x)", "interest_coverage"),
        ]),
        ("Efficiency", "efficiency", [
            ("Asset Turnover", "asset_turnover"),
            ("CapEx % Revenue", "capex_pct_revenue"),
            ("Working Capital % Revenue", "wc_pct_revenue"),
        ]),
        ("Growth", "growth", [
            ("Revenue Growth %", "revenue_growth_pct"),
            ("EBITDA Growth %", "ebitda_growth_pct"),
            ("Net Income Growth %", "net_income_growth_pct"),
        ]),
    ]

    print(f"\n{header}")
    print("-" * (35 + 14 * len(years)))

    for section_name, section_key, metrics in sections:
        print(f"\n  {section_name.upper()}")
        for label, key in metrics:
            row = f"  {label:<33}"
            for r in all_ratios:
                val = r.get(section_key, {}).get(key)
                if val is None:
                    row += f"{'—':<14}"
                elif isinstance(val, str):
                    row += f"{val:<14}"
                else:
                    row += f"{val:<14.1f}"
            print(row)


def main():
    parser = argparse.ArgumentParser(description="Financial Ratio Analyzer")
    parser.add_argument("financials", help="CSV file with financial data")
    parser.add_argument("--benchmark", help="Industry benchmark CSV for comparison")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    try:
        with open(args.financials, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: File '{args.financials}' not found.", file=sys.stderr)
        sys.exit(1)

    all_ratios = []
    for i, row in enumerate(rows):
        prior = rows[i - 1] if i > 0 else None
        all_ratios.append(calculate_ratios(row, prior))

    if args.format == "json":
        print(json.dumps(all_ratios, indent=2))
    else:
        print_ratios_table(all_ratios)


if __name__ == "__main__":
    main()
