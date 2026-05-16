#!/usr/bin/env python3
"""Calculates sample sizes, generates experiment briefs, and analyzes A/B test results."""

import sys
import json
import math
import argparse
import random
from datetime import date, timedelta


def calculate_sample_size(baseline_rate: float, mde: float,
                          alpha: float = 0.05, power: float = 0.80) -> int:
    """Calculate required sample size per variant using two-proportion z-test."""
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)

    z_alpha = 1.96   # two-tailed, alpha=0.05
    z_power = 0.84   # power=0.80

    p_bar = (p1 + p2) / 2
    numerator = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) +
                 z_power * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    denominator = (p2 - p1) ** 2
    return math.ceil(numerator / denominator)


def estimate_duration(sample_size: int, daily_traffic: int, variants: int = 2) -> int:
    """Estimate test duration in days."""
    total_needed = sample_size * variants
    return math.ceil(total_needed / daily_traffic)


def analyze_frequentist(control_conv: int, control_vis: int,
                        treatment_conv: int, treatment_vis: int) -> dict:
    """Two-proportion z-test for A/B significance."""
    p1 = control_conv / control_vis
    p2 = treatment_conv / treatment_vis
    p_pool = (control_conv + treatment_conv) / (control_vis + treatment_vis)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / control_vis + 1 / treatment_vis))
    z = (p2 - p1) / se if se > 0 else 0

    # Two-tailed p-value approximation
    p_value = 2 * (1 - _norm_cdf(abs(z)))
    lift = (p2 - p1) / p1 if p1 > 0 else 0
    ci_margin = 1.96 * math.sqrt(p1 * (1 - p1) / control_vis + p2 * (1 - p2) / treatment_vis)

    return {
        "control_rate": round(p1, 4),
        "treatment_rate": round(p2, 4),
        "lift_pct": round(lift * 100, 2),
        "z_score": round(z, 3),
        "p_value": round(p_value, 4),
        "significant": p_value < 0.05,
        "confidence_interval_95": [round(lift - ci_margin / p1, 4), round(lift + ci_margin / p1, 4)],
    }


def analyze_bayesian(control_conv: int, control_vis: int,
                     treatment_conv: int, treatment_vis: int,
                     simulations: int = 50000) -> dict:
    """Beta-Binomial Bayesian analysis with uniform prior."""
    # Beta posterior parameters
    a_c = 1 + control_conv
    b_c = 1 + (control_vis - control_conv)
    a_t = 1 + treatment_conv
    b_t = 1 + (treatment_vis - treatment_conv)

    # Monte Carlo sampling
    control_samples = [_beta_sample(a_c, b_c) for _ in range(simulations)]
    treatment_samples = [_beta_sample(a_t, b_t) for _ in range(simulations)]

    prob_better = sum(t > c for t, c in zip(treatment_samples, control_samples)) / simulations
    lifts = [(t - c) / c for t, c in zip(treatment_samples, control_samples) if c > 0]
    expected_lift = sum(lifts) / len(lifts) if lifts else 0

    sorted_diff = sorted(t - c for t, c in zip(treatment_samples, control_samples))
    ci_lo = sorted_diff[int(0.025 * simulations)]
    ci_hi = sorted_diff[int(0.975 * simulations)]

    return {
        "prob_treatment_better": round(prob_better, 3),
        "expected_lift_pct": round(expected_lift * 100, 2),
        "credible_interval_95": [round(ci_lo, 4), round(ci_hi, 4)],
        "recommendation": "Ship treatment" if prob_better >= 0.95 else
                          "Continue testing" if prob_better >= 0.80 else
                          "Favor control",
    }


def _norm_cdf(x: float) -> float:
    """Approximation of standard normal CDF."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _beta_sample(alpha: float, beta: float) -> float:
    """Sample from Beta distribution using standard library."""
    return random.betavariate(alpha, beta)


def generate_brief(baseline: float, mde: float, daily_traffic: int,
                   title: str, hypothesis: str) -> dict:
    n = calculate_sample_size(baseline, mde)
    duration = estimate_duration(n, daily_traffic)
    start = date.today()
    end = start + timedelta(days=duration)
    return {
        "title": title,
        "hypothesis": hypothesis,
        "baseline_rate": baseline,
        "mde_relative": mde,
        "sample_size_per_variant": n,
        "total_sample_size": n * 2,
        "estimated_duration_days": duration,
        "start_date": str(start),
        "end_date": str(end),
        "alpha": 0.05,
        "power": 0.80,
    }


def portfolio_summary(experiments: list) -> dict:
    running = [e for e in experiments if e.get("status") == "running"]
    completed = [e for e in experiments if e.get("status") == "completed"]
    wins = [e for e in completed if e.get("result") == "win"]
    losses = [e for e in completed if e.get("result") == "loss"]
    nulls = [e for e in completed if e.get("result") == "null"]
    win_rate = len(wins) / len(completed) if completed else 0
    return {
        "running": len(running),
        "completed": len(completed),
        "wins": len(wins),
        "losses": len(losses),
        "inconclusive": len(nulls),
        "win_rate_pct": round(win_rate * 100, 1),
    }


def print_brief_table(brief: dict):
    print("\nEXPERIMENT BRIEF")
    print("=" * 50)
    print(f"Title:         {brief['title']}")
    print(f"Hypothesis:    {brief['hypothesis']}")
    print(f"Baseline rate: {brief['baseline_rate']:.1%}")
    print(f"MDE:           {brief['mde_relative']:.1%} relative")
    print(f"Sample/variant:{brief['sample_size_per_variant']:,}")
    print(f"Total sample:  {brief['total_sample_size']:,}")
    print(f"Duration:      {brief['estimated_duration_days']} days")
    print(f"Run dates:     {brief['start_date']} → {brief['end_date']}")
    print(f"Confidence:    {(1-brief['alpha']):.0%} | Power: {brief['power']:.0%}")


def print_analysis_table(freq: dict, bayes: dict):
    print("\nANALYSIS RESULTS")
    print("=" * 50)
    print(f"Control rate:       {freq['control_rate']:.2%}")
    print(f"Treatment rate:     {freq['treatment_rate']:.2%}")
    print(f"Lift:               {freq['lift_pct']:+.2f}%")
    print("\nFrequentist:")
    print(f"  Z-score:          {freq['z_score']:.3f}")
    print(f"  P-value:          {freq['p_value']:.4f}")
    print(f"  Significant:      {'✓ YES' if freq['significant'] else '✗ NO'}")
    print("\nBayesian:")
    print(f"  P(treatment wins):{bayes['prob_treatment_better']:.1%}")
    print(f"  Expected lift:    {bayes['expected_lift_pct']:+.2f}%")
    print(f"  Recommendation:   {bayes['recommendation']}")


def main():
    parser = argparse.ArgumentParser(
        description="A/B experiment designer and analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python experiment_designer.py --baseline 0.10 --mde 0.10\n"
            "  python experiment_designer.py --analyze --control 450,5000 --treatment 495,5000\n"
            "  python experiment_designer.py --portfolio experiments.json --format json"
        )
    )
    parser.add_argument("--baseline", type=float, help="Baseline conversion rate (e.g. 0.10)")
    parser.add_argument("--mde", type=float, help="Minimum detectable effect relative (e.g. 0.10 for 10%% lift)")
    parser.add_argument("--traffic", type=int, default=1000, help="Daily traffic per variant")
    parser.add_argument("--title", default="Experiment", help="Experiment title")
    parser.add_argument("--hypothesis", default="Treatment will improve primary metric", help="Hypothesis statement")
    parser.add_argument("--analyze", action="store_true", help="Run analysis on existing results")
    parser.add_argument("--control", help="Control results: conversions,visitors (e.g. 450,5000)")
    parser.add_argument("--treatment", help="Treatment results: conversions,visitors")
    parser.add_argument("--portfolio", help="Path to experiments JSON file for portfolio summary")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    if args.analyze and args.control and args.treatment:
        c_conv, c_vis = [int(x) for x in args.control.split(",")]
        t_conv, t_vis = [int(x) for x in args.treatment.split(",")]
        freq = analyze_frequentist(c_conv, c_vis, t_conv, t_vis)
        bayes = analyze_bayesian(c_conv, c_vis, t_conv, t_vis)
        if args.format == "json":
            print(json.dumps({"frequentist": freq, "bayesian": bayes}, indent=2))
        else:
            print_analysis_table(freq, bayes)

    elif args.portfolio:
        try:
            with open(args.portfolio) as f:
                experiments = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading portfolio file: {e}", file=sys.stderr)
            sys.exit(1)
        summary = portfolio_summary(experiments)
        if args.format == "json":
            print(json.dumps(summary, indent=2))
        else:
            print("\nEXPERIMENT PORTFOLIO SUMMARY")
            print("=" * 40)
            for k, v in summary.items():
                print(f"  {k.replace('_', ' ').title():<25} {v}")

    elif args.baseline and args.mde:
        brief = generate_brief(args.baseline, args.mde, args.traffic, args.title, args.hypothesis)
        if args.format == "json":
            print(json.dumps(brief, indent=2))
        else:
            print_brief_table(brief)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
