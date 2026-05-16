#!/usr/bin/env python3
"""
DCF Calculator — builds multi-scenario discounted cash flow valuation.

Usage:
    python dcf_calculator.py --revenue 100 --growth 0.25 --margin 0.20 --wacc 0.10
    python dcf_calculator.py --revenue 100 --growth 0.25 --margin 0.20 --wacc 0.10 --scenarios
    python dcf_calculator.py --revenue 100 --growth 0.25 --margin 0.20 --wacc 0.10 --format json
"""

import argparse
import json
import sys


def project_fcf(base_revenue, growth_rate, ebitda_margin, capex_pct, wc_pct, years):
    """Project free cash flows over the forecast period."""
    flows = []
    revenue = base_revenue
    for year in range(1, years + 1):
        revenue = revenue * (1 + growth_rate)
        ebitda = revenue * ebitda_margin
        da = revenue * 0.03  # assume 3% D&A
        ebit = ebitda - da
        nopat = ebit * 0.79  # 21% tax rate
        capex = revenue * capex_pct
        delta_wc = revenue * wc_pct * growth_rate
        fcf = nopat + da - capex - delta_wc
        flows.append({
            "year": year,
            "revenue": round(revenue, 1),
            "ebitda": round(ebitda, 1),
            "fcf": round(fcf, 1),
        })
    return flows


def terminal_value_gordon(fcf_terminal, terminal_growth, wacc):
    """Terminal value using Gordon Growth Model."""
    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth rate")
    return fcf_terminal * (1 + terminal_growth) / (wacc - terminal_growth)


def terminal_value_multiple(ebitda_terminal, exit_multiple):
    """Terminal value using exit multiple."""
    return ebitda_terminal * exit_multiple


def present_value(cash_flows, wacc):
    """Discount a list of (year, amount) tuples to present value."""
    return sum(cf / (1 + wacc) ** yr for yr, cf in cash_flows)


def run_dcf(revenue, growth, margin, wacc, terminal_growth, capex_pct, wc_pct, years, debt, cash, shares):
    flows = project_fcf(revenue, growth, margin, capex_pct, wc_pct, years)
    pv_fcfs = present_value([(f["year"], f["fcf"]) for f in flows], wacc)

    last = flows[-1]
    tv = terminal_value_gordon(last["fcf"], terminal_growth, wacc)
    pv_tv = tv / (1 + wacc) ** years

    enterprise_value = pv_fcfs + pv_tv
    equity_value = enterprise_value - debt + cash
    price_per_share = equity_value / shares if shares > 0 else None

    return {
        "projections": flows,
        "pv_fcfs": round(pv_fcfs, 1),
        "terminal_value": round(tv, 1),
        "pv_terminal_value": round(pv_tv, 1),
        "enterprise_value": round(enterprise_value, 1),
        "equity_value": round(equity_value, 1),
        "price_per_share": round(price_per_share, 2) if price_per_share else None,
        "tv_pct_of_ev": round(pv_tv / enterprise_value * 100, 1),
    }


def print_table(result, scenario_name="Base"):
    print(f"\n{'='*60}")
    print(f"  DCF Valuation — {scenario_name} Case")
    print(f"{'='*60}")
    print(f"\n{'Year':<8}{'Revenue ($M)':<18}{'EBITDA ($M)':<16}{'FCF ($M)'}")
    print(f"{'-'*8}{'-'*18}{'-'*16}{'-'*12}")
    for f in result["projections"]:
        print(f"{f['year']:<8}{f['revenue']:<18.1f}{f['ebitda']:<16.1f}{f['fcf']:.1f}")

    print(f"\n{'PV of FCFs':<35} ${result['pv_fcfs']:>10.1f}M")
    print(f"{'Terminal Value (Gordon Growth)':<35} ${result['terminal_value']:>10.1f}M")
    print(f"{'PV of Terminal Value':<35} ${result['pv_terminal_value']:>10.1f}M")
    print(f"{'Terminal Value % of EV':<35} {result['tv_pct_of_ev']:>10.1f}%")
    print(f"{'─'*47}")
    print(f"{'Enterprise Value':<35} ${result['enterprise_value']:>10.1f}M")
    print(f"{'Equity Value':<35} ${result['equity_value']:>10.1f}M")
    if result["price_per_share"]:
        print(f"{'Implied Price per Share':<35} ${result['price_per_share']:>10.2f}")


def run_scenarios(base_revenue, wacc, capex_pct, wc_pct, years, debt, cash, shares):
    scenarios = [
        ("Bull",  0.35, 0.25, 0.03),
        ("Base",  0.25, 0.20, 0.03),
        ("Bear",  0.15, 0.15, 0.025),
    ]
    weights = {"Bull": 0.25, "Base": 0.50, "Bear": 0.25}

    print(f"\n{'Scenario':<10}{'Revenue CAGR':<16}{'EBITDA Margin':<18}{'EV ($M)':<14}{'Price':<12}{'Weight'}")
    print(f"{'-'*10}{'-'*16}{'-'*18}{'-'*14}{'-'*12}{'-'*8}")

    weighted_price = 0.0
    for name, growth, margin, tg in scenarios:
        r = run_dcf(base_revenue, growth, margin, wacc, tg, capex_pct, wc_pct, years, debt, cash, shares)
        price = r["price_per_share"] or 0
        w = weights[name]
        weighted_price += price * w
        print(f"{name:<10}{growth*100:<16.0f}%{margin*100:<18.0f}%${r['enterprise_value']:<13.1f}${price:<12.2f}{w*100:.0f}%")

    print(f"{'─'*78}")
    print(f"{'Weighted Price Target':<56}${weighted_price:<12.2f}")


def main():
    parser = argparse.ArgumentParser(description="DCF Valuation Calculator")
    parser.add_argument("--revenue", type=float, required=True, help="Base year revenue ($M)")
    parser.add_argument("--growth", type=float, default=0.20, help="Annual revenue growth rate (decimal)")
    parser.add_argument("--margin", type=float, default=0.20, help="EBITDA margin (decimal)")
    parser.add_argument("--wacc", type=float, default=0.10, help="WACC (decimal)")
    parser.add_argument("--terminal-growth", type=float, default=0.03, help="Terminal growth rate")
    parser.add_argument("--capex-pct", type=float, default=0.05, help="CapEx as % of revenue")
    parser.add_argument("--wc-pct", type=float, default=0.10, help="Working capital as % of revenue")
    parser.add_argument("--years", type=int, default=5, help="Forecast years")
    parser.add_argument("--debt", type=float, default=0, help="Net debt ($M)")
    parser.add_argument("--cash", type=float, default=0, help="Cash ($M)")
    parser.add_argument("--shares", type=float, default=0, help="Diluted shares outstanding (M)")
    parser.add_argument("--scenarios", action="store_true", help="Run bull/base/bear scenario table")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    if args.scenarios:
        run_scenarios(args.revenue, args.wacc, args.capex_pct, args.wc_pct,
                      args.years, args.debt, args.cash, args.shares)
        return

    result = run_dcf(args.revenue, args.growth, args.margin, args.wacc,
                     args.terminal_growth, args.capex_pct, args.wc_pct,
                     args.years, args.debt, args.cash, args.shares)

    if args.format == "json":
        print(json.dumps(result, indent=2))
    else:
        print_table(result)


if __name__ == "__main__":
    main()
