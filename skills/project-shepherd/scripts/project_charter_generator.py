#!/usr/bin/env python3
"""Generates project charter documents and status reports from structured input."""

import sys
import json
import argparse
from datetime import date, timedelta

RISK_SCORES = {"high": 3, "medium": 2, "low": 1}

STATUS_ICONS = {
    "on_track": "🟢 ON TRACK",
    "at_risk": "🟡 AT RISK",
    "blocked": "🔴 BLOCKED",
}


def risk_score(probability: str, impact: str) -> int:
    return RISK_SCORES.get(probability, 1) * RISK_SCORES.get(impact, 1)


def risk_priority(score: int) -> str:
    if score >= 6:
        return "Critical"
    if score >= 4:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def generate_charter(name: str, pm: str, sponsor: str,
                     objectives: list, start_date: str) -> dict:
    start = date.fromisoformat(start_date) if start_date else date.today()
    phases = [
        ("Discovery", 0, 14),
        ("Design", 14, 28),
        ("Build", 28, 70),
        ("Launch", 70, 84),
        ("Measure", 84, 98),
    ]
    timeline = [
        {
            "phase": name,
            "start": str(start + timedelta(days=s)),
            "end": str(start + timedelta(days=e)),
        }
        for name, s, e in phases
    ]
    return {
        "project_name": name,
        "project_manager": pm,
        "sponsor": sponsor,
        "date": str(date.today()),
        "objectives": objectives or [
            "Define measurable objective 1",
            "Define measurable objective 2",
            "Define measurable objective 3",
        ],
        "success_criteria": [
            "Specific measurable outcome 1",
            "Specific measurable outcome 2",
        ],
        "scope_in": ["List what is included"],
        "scope_out": ["List what is explicitly excluded"],
        "timeline": timeline,
        "stakeholders": [
            {"role": "Sponsor", "name": sponsor, "engagement": "Monthly approval"},
            {"role": "Project Manager", "name": pm, "engagement": "Daily driver"},
            {"role": "Tech Lead", "name": "TBD", "engagement": "Weekly sync"},
        ],
        "risks": [],
        "budget": {"estimated": 0, "approved": 0},
    }


def generate_status_report(project_name: str, pm: str, week: int,
                           status: str, accomplishments: list,
                           next_week: list, blockers: list) -> dict:
    return {
        "project": project_name,
        "pm": pm,
        "week": week,
        "date": str(date.today()),
        "status": status,
        "status_display": STATUS_ICONS.get(status, "🟢 ON TRACK"),
        "executive_summary": f"Week {week} update for {project_name}.",
        "accomplishments": accomplishments or ["Complete accomplishments list"],
        "next_week": next_week or ["Complete next week plan"],
        "blockers": blockers or [],
    }


def score_risks(risks: list) -> list:
    scored = []
    for r in risks:
        score = risk_score(r.get("probability", "low"), r.get("impact", "low"))
        scored.append({**r, "score": score, "priority": risk_priority(score)})
    return sorted(scored, key=lambda x: x["score"], reverse=True)


def print_charter(charter: dict):
    print("\nPROJECT CHARTER")
    print("=" * 60)
    print(f"Project:  {charter['project_name']}")
    print(f"PM:       {charter['project_manager']}")
    print(f"Sponsor:  {charter['sponsor']}")
    print(f"Date:     {charter['date']}")
    print("\nOBJECTIVES")
    for i, obj in enumerate(charter['objectives'], 1):
        print(f"  {i}. {obj}")
    print("\nTIMELINE")
    for phase in charter['timeline']:
        print(f"  {phase['phase']:<12} {phase['start']} → {phase['end']}")
    print("\nSTAKEHOLDERS")
    print(f"  {'Role':<20} {'Name':<20} {'Engagement'}")
    print(f"  {'-'*55}")
    for s in charter['stakeholders']:
        print(f"  {s['role']:<20} {s['name']:<20} {s['engagement']}")


def print_status_report(report: dict):
    print("\nPROJECT STATUS REPORT — Week {}, {}".format(report['week'], report['date']))
    print("=" * 60)
    print(f"Project: {report['project']} | PM: {report['pm']} | {report['status_display']}")
    print("\nEXECUTIVE SUMMARY")
    print(f"  {report['executive_summary']}")
    print("\nACCOMPLISHMENTS")
    for item in report['accomplishments']:
        print(f"  ✓ {item}")
    print("\nNEXT WEEK")
    for item in report['next_week']:
        print(f"  → {item}")
    if report['blockers']:
        print("\nBLOCKERS")
        for b in report['blockers']:
            print(f"  🔴 {b}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate project charters and status reports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python project_charter_generator.py --name 'Project Alpha' --pm 'Alice' --sponsor 'Bob'\n"
            "  python project_charter_generator.py --status --project project.json --week 5\n"
            "  python project_charter_generator.py --risks risks.json --format json"
        )
    )
    parser.add_argument("--name", help="Project name")
    parser.add_argument("--pm", help="Project manager name")
    parser.add_argument("--sponsor", help="Executive sponsor name")
    parser.add_argument("--start", help="Project start date YYYY-MM-DD", default=str(date.today()))
    parser.add_argument("--objectives", help="Comma-separated list of objectives")
    parser.add_argument("--status", action="store_true", help="Generate status report")
    parser.add_argument("--project", help="Path to project JSON file")
    parser.add_argument("--week", type=int, default=1, help="Week number for status report")
    parser.add_argument("--project-status", choices=["on_track", "at_risk", "blocked"],
                        default="on_track", help="Overall project status")
    parser.add_argument("--risks", help="Path to risks JSON file for scoring")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    if args.risks:
        try:
            with open(args.risks) as f:
                risks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading risks file: {e}", file=sys.stderr)
            sys.exit(1)
        scored = score_risks(risks)
        if args.format == "json":
            print(json.dumps(scored, indent=2))
        else:
            print("\nRISK REGISTER (sorted by priority)")
            print(f"{'ID':<10} {'Title':<30} {'Priority':<10} {'Score'}")
            print("-" * 60)
            for r in scored:
                print(f"{r.get('id', '-'):<10} {r.get('title', '-'):<30} {r['priority']:<10} {r['score']}")

    elif args.status:
        project_data = {}
        if args.project:
            try:
                with open(args.project) as f:
                    project_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading project file: {e}", file=sys.stderr)
                sys.exit(1)
        report = generate_status_report(
            project_name=project_data.get("project_name", args.name or "Project"),
            pm=project_data.get("project_manager", args.pm or "PM"),
            week=args.week,
            status=args.project_status,
            accomplishments=project_data.get("accomplishments", []),
            next_week=project_data.get("next_week", []),
            blockers=project_data.get("blockers", []),
        )
        if args.format == "json":
            print(json.dumps(report, indent=2))
        else:
            print_status_report(report)

    elif args.name:
        objectives = [o.strip() for o in args.objectives.split(",")] if args.objectives else []
        charter = generate_charter(args.name, args.pm or "TBD", args.sponsor or "TBD",
                                   objectives, args.start)
        if args.format == "json":
            print(json.dumps(charter, indent=2))
        else:
            print_charter(charter)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
