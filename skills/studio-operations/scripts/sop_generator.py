#!/usr/bin/env python3
"""Generates SOP documents and process efficiency reports."""

import sys
import json
import argparse
from datetime import date, timedelta


DEPT_PREFIXES = {
    "ops": "OPS",
    "prod": "PROD",
    "eng": "ENG",
    "finance": "FIN",
    "hr": "HR",
    "comms": "COMMS",
    "qa": "QA",
}

FREQUENCY_SCORES = {
    "daily": 5,
    "weekly": 4,
    "monthly": 3,
    "per_project": 2,
    "ad_hoc": 1,
}


def next_sop_id(dept: str, existing_sops: list) -> str:
    prefix = f"SOP-{dept.upper()}-"
    existing_nums = [
        int(s.get("id", "SOP-X-000").split("-")[-1])
        for s in existing_sops
        if s.get("id", "").startswith(prefix)
    ]
    next_num = max(existing_nums, default=0) + 1
    return f"{prefix}{next_num:03d}"


def generate_sop(name: str, dept: str, owner: str,
                 purpose: str, steps: list, sop_id: str = None) -> dict:
    dept_code = DEPT_PREFIXES.get(dept.lower(), dept.upper())
    sop_id = sop_id or f"SOP-{dept_code}-001"
    today = date.today()
    review = today + timedelta(days=180)

    return {
        "id": sop_id,
        "name": name,
        "version": "1.0",
        "owner": owner,
        "department": dept_code,
        "created": str(today),
        "review_date": str(review),
        "purpose": purpose or f"Define the standard procedure for {name.lower()}.",
        "scope": {
            "applies_to": f"All {owner} role team members",
            "excludes": "One-off exceptions requiring manager approval",
        },
        "prerequisites": [
            "Required tool access and permissions",
            "Completion of onboarding training",
        ],
        "steps": steps or [
            {"number": 1, "action": "Start process", "detail": "Describe first action", "expected_result": "Process initiated"},
            {"number": 2, "action": "Execute main task", "detail": "Describe core action", "expected_result": "Task completed"},
            {"number": 3, "action": "Verify and close", "detail": "Quality check", "expected_result": "Process complete and verified"},
        ],
        "quality_checks": [
            "Output matches expected format",
            "No errors or warnings logged",
            "Stakeholder notified of completion",
        ],
        "escalation": {
            "level_1": f"Contact {owner} via Slack",
            "level_2": f"Escalate to department head",
            "emergency": "Page on-call via PagerDuty",
        },
        "revision_history": [
            {"version": "1.0", "date": str(today), "author": owner, "changes": "Initial version"}
        ],
    }


def efficiency_score(cycle_time: float, target_time: float,
                     error_rate: float, completion_rate: float) -> dict:
    time_score = min(100.0, (target_time / max(cycle_time, 0.01)) * 100)
    error_score = max(0.0, 100.0 - (error_rate * 10.0))
    completion_score = completion_rate
    composite = round((time_score + error_score + completion_score) / 3, 1)
    return {
        "time_score": round(time_score, 1),
        "error_score": round(error_score, 1),
        "completion_score": round(completion_score, 1),
        "composite_score": composite,
        "rating": "Excellent" if composite >= 85 else "Good" if composite >= 70 else "Needs Improvement",
    }


def process_inventory(processes: list) -> list:
    scored = []
    for p in processes:
        freq = p.get("frequency", "ad_hoc")
        freq_score = FREQUENCY_SCORES.get(freq, 1)
        automated = p.get("automated", False)
        eff = p.get("efficiency_score", 75)
        # Automation opportunity: high frequency + low efficiency + not automated
        automation_opportunity = freq_score >= 3 and eff < 75 and not automated
        scored.append({**p, "automation_opportunity": automation_opportunity})
    return sorted(scored, key=lambda x: x.get("efficiency_score", 0))


def print_sop(sop: dict):
    print(f"\nSOP: {sop['name']}")
    print("=" * 60)
    print(f"Document ID:  {sop['id']}")
    print(f"Version:      {sop['version']}")
    print(f"Owner:        {sop['owner']}")
    print(f"Last Updated: {sop['created']}")
    print(f"Review Date:  {sop['review_date']}")
    print(f"\nPURPOSE")
    print(f"  {sop['purpose']}")
    print(f"\nPROCEDURE")
    for step in sop["steps"]:
        print(f"\n  Step {step['number']}: {step['action']}")
        print(f"    {step['detail']}")
        print(f"    Expected: {step['expected_result']}")
    print(f"\nQUALITY CHECKS")
    for check in sop["quality_checks"]:
        print(f"  ☐ {check}")
    print(f"\nESCALATION")
    for level, action in sop["escalation"].items():
        print(f"  {level.replace('_', ' ').title()}: {action}")


def print_inventory(processes: list):
    print(f"\nPROCESS INVENTORY")
    print(f"{'ID':<15} {'Name':<35} {'Owner':<15} {'Freq':<12} {'Auto':<6} {'Score':<6} {'Opportunity'}")
    print("-" * 100)
    for p in processes:
        opp = "✓ AUTOMATE" if p.get("automation_opportunity") else ""
        print(f"{p.get('id',''):<15} {p.get('name',''):<35} {p.get('owner',''):<15} "
              f"{p.get('frequency',''):<12} {'Yes' if p.get('automated') else 'No':<6} "
              f"{p.get('efficiency_score', '-'):<6} {opp}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate SOP documents and process efficiency reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python sop_generator.py --name 'Client Onboarding' --dept OPS --owner 'Alice'\n"
            "  python sop_generator.py --inventory processes.json\n"
            "  python sop_generator.py --efficiency --actual-time 4.5 --target-time 3.0 --error-rate 3 --completion 92"
        )
    )
    parser.add_argument("--name", help="SOP process name")
    parser.add_argument("--dept", default="OPS", help="Department code")
    parser.add_argument("--owner", default="Operations", help="Process owner")
    parser.add_argument("--purpose", help="Process purpose statement")
    parser.add_argument("--steps", help="Path to steps JSON file")
    parser.add_argument("--inventory", help="Path to processes JSON file for inventory report")
    parser.add_argument("--efficiency", action="store_true", help="Calculate efficiency score")
    parser.add_argument("--actual-time", type=float, help="Actual cycle time in hours")
    parser.add_argument("--target-time", type=float, help="Target cycle time in hours")
    parser.add_argument("--error-rate", type=float, default=2.0, help="Error rate percent")
    parser.add_argument("--completion", type=float, default=95.0, help="Completion rate percent")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    if args.efficiency and args.actual_time and args.target_time:
        score = efficiency_score(args.actual_time, args.target_time,
                                 args.error_rate, args.completion)
        if args.format == "json":
            print(json.dumps(score, indent=2))
        else:
            print(f"\nEFFICIENCY SCORE")
            print("=" * 40)
            for k, v in score.items():
                print(f"  {k.replace('_', ' ').title():<25} {v}")

    elif args.inventory:
        try:
            with open(args.inventory) as f:
                processes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading inventory file: {e}", file=sys.stderr)
            sys.exit(1)
        scored = process_inventory(processes)
        if args.format == "json":
            print(json.dumps(scored, indent=2))
        else:
            print_inventory(scored)

    elif args.name:
        steps = []
        if args.steps:
            try:
                with open(args.steps) as f:
                    steps = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading steps file: {e}", file=sys.stderr)
                sys.exit(1)
        sop = generate_sop(args.name, args.dept, args.owner, args.purpose, steps)
        if args.format == "json":
            print(json.dumps(sop, indent=2))
        else:
            print_sop(sop)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
