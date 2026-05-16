# Project Shepherd Skill

## Overview

Provides cross-functional project coordination capabilities: project charter generation, timeline management, stakeholder alignment, risk mitigation, and status reporting. Designed for project managers and team leads shepherding complex initiatives across multiple teams and stakeholders.

## Capabilities

### Project Charter Template

```
PROJECT CHARTER
===============
Project Name: [Name]
Project ID: [ID]
Date: [YYYY-MM-DD]
Project Manager: [Name]
Sponsor: [Executive name]

PROBLEM STATEMENT
-----------------
[2-3 sentences describing the problem being solved]

OBJECTIVES
----------
1. [Measurable objective — OKR format preferred]
2. [Measurable objective]
3. [Measurable objective]

SUCCESS CRITERIA
----------------
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]
- [ ] [Specific measurable outcome]

SCOPE
-----
In scope:
- [What IS included]

Out of scope:
- [What is explicitly excluded]

TIMELINE
--------
Phase 1 — Discovery:  [Start] → [End]
Phase 2 — Design:     [Start] → [End]
Phase 3 — Build:      [Start] → [End]
Phase 4 — Launch:     [Start] → [End]
Phase 5 — Measure:    [Start] → [End]

STAKEHOLDERS
------------
Role              Name           Engagement
----------------------------------------------
Sponsor           [Name]         Final approval, monthly
Project Manager   [Name]         Daily driver
Tech Lead         [Name]         Weekly sync
Design Lead       [Name]         Weekly sync
Business Owner    [Name]         Bi-weekly review

RISKS
-----
Risk                  Probability  Impact  Mitigation
---------------------------------------------------
[Risk description]    High/Med/Low  H/M/L  [Mitigation plan]

BUDGET
------
Estimated total: $[Amount]
Approved budget: $[Amount]
```

### Status Report Template

```
PROJECT STATUS REPORT — Week [N], [Date]
==========================================
Project: [Name] | PM: [Name] | Status: 🟢 ON TRACK / 🟡 AT RISK / 🔴 BLOCKED

EXECUTIVE SUMMARY
-----------------
[2-3 sentences: progress this week, overall health, key decision needed]

THIS WEEK'S ACCOMPLISHMENTS
----------------------------
✓ [Completed item 1]
✓ [Completed item 2]
✓ [Completed item 3]

NEXT WEEK'S PLAN
----------------
→ [Planned item 1] — Owner: [Name]
→ [Planned item 2] — Owner: [Name]
→ [Planned item 3] — Owner: [Name]

RISKS & BLOCKERS
----------------
🔴 BLOCKED: [Description] — Action: [What's needed] — Owner: [Name] — Due: [Date]
🟡 AT RISK: [Description] — Mitigation: [Plan] — Owner: [Name]

METRICS
-------
[Metric name]:    [Current value] / [Target value]  ([Status])
Timeline:         [X% complete] | Budget: [$X spent / $Y approved]

DECISIONS NEEDED
----------------
1. [Decision needed] — Needed by: [Date] — Decision maker: [Name]
```

### Risk Register

```python
RISK_TEMPLATE = {
    "id": "RISK-001",
    "title": "Short risk title",
    "description": "Detailed risk description",
    "probability": "high|medium|low",
    "impact": "high|medium|low",
    "score": 0,  # probability_score * impact_score
    "mitigation": "Mitigation strategy",
    "contingency": "Contingency plan if risk materializes",
    "owner": "Name",
    "status": "open|monitoring|closed",
    "last_reviewed": "YYYY-MM-DD"
}

RISK_SCORES = {"high": 3, "medium": 2, "low": 1}

def risk_score(probability: str, impact: str) -> int:
    return RISK_SCORES[probability] * RISK_SCORES[impact]

def risk_priority(score: int) -> str:
    if score >= 6: return "Critical"
    if score >= 4: return "High"
    if score >= 2: return "Medium"
    return "Low"
```

### Stakeholder RACI Matrix

```
RACI MATRIX — [Project Name]
============================
            Sponsor  PM   TL   Design  QA   Comms
---------------------------------------------------
Charter       A      R    C     C      I    I
Architecture  I      C    R     I      C    I
Design        I      C    C     R      C    I
Development   I      C    R     C      I    I
Testing       I      C    C     I      R    I
Launch        A      R    C     C      C    R
Retrospective I      R    C     C      C    I

R=Responsible A=Accountable C=Consulted I=Informed
```

## Scripts

### `scripts/project_charter_generator.py`

Generates project charter documents and weekly status reports from structured input.

```
Usage: python project_charter_generator.py --name "Project Alpha" --pm "Alice" --sponsor "Bob"
       python project_charter_generator.py --status --project project.json --week 5
       python project_charter_generator.py --risks project.json
       python project_charter_generator.py --format json
Output:
  - Complete project charter document
  - Weekly status report
  - Risk register with priority scoring
  - RACI matrix
```

## References

### `references/project_management_guide.md`
Project lifecycle phases, gate criteria for phase transitions, escalation matrix, change control process, retrospective format, and lessons-learned documentation.

### `references/stakeholder_management.md`
Stakeholder mapping techniques, communication cadence recommendations, difficult conversation frameworks, alignment meeting facilitation guides.

## Assets

### `assets/project_charter_template.md`
Full project charter template with all standard sections pre-populated with guidance text.

### `assets/status_report_template.md`
Weekly status report template optimized for executive audiences and async stakeholders.

## Quality Standards

- Project charter signed off by sponsor before work begins
- Status reports published every Friday by 5pm
- Risk register reviewed weekly; critical risks reviewed daily
- All blockers escalated within 24 hours of identification
- Retrospective held within 1 week of project completion
- Lessons learned documented and shared across PM community
