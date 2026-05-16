# Studio Operations Skill

## Overview

Provides day-to-day studio efficiency management: SOP (Standard Operating Procedure) generation, process documentation, operational efficiency reporting, and workflow optimization. Helps studio operations teams codify institutional knowledge and systematically improve recurring processes.

## Capabilities

### SOP Template Structure

```
SOP: [Process Name]
===================
Document ID:  SOP-[DEPT]-[NUMBER]
Version:      [X.Y]
Owner:        [Name/Role]
Last Updated: [YYYY-MM-DD]
Review Date:  [YYYY-MM-DD + 6 months]

PURPOSE
-------
[1-2 sentences explaining why this process exists and what outcome it achieves]

SCOPE
-----
Applies to: [Who performs this process]
Excludes:   [What is explicitly out of scope]

PREREQUISITES
-------------
- [ ] [Required tool/access/permission]
- [ ] [Required knowledge/training]
- [ ] [Required materials/assets]

PROCEDURE
---------
Step 1: [Action verb] + [Clear description]
  - Detail or sub-step if needed
  - Expected result: [What should happen]
  - ⚠️ Warning: [If applicable]

Step 2: [Action verb] + [Clear description]
  - Detail or sub-step if needed
  - Expected result: [What should happen]

Step 3: [Continue pattern...]

QUALITY CHECKS
--------------
After completing this procedure, verify:
- [ ] [Quality checkpoint 1]
- [ ] [Quality checkpoint 2]
- [ ] [Quality checkpoint 3]

ESCALATION PATH
---------------
If [condition]: Contact [Role] via [Channel]
If [condition]: Escalate to [Senior Role] via [Channel]
Emergency: [Emergency contact/procedure]

RELATED DOCUMENTS
-----------------
- [Related SOP ID]: [Title]
- [Template/Asset name]: [Location]

REVISION HISTORY
----------------
Version  Date        Author    Changes
-------  ----------  --------  -------
1.0      YYYY-MM-DD  [Name]    Initial version
```

### Process Efficiency Metrics

```python
EFFICIENCY_METRICS = {
    "cycle_time": {
        "description": "Time from process start to completion",
        "unit": "hours",
        "target": None,  # Set per process
    },
    "error_rate": {
        "description": "Percentage of process runs requiring rework",
        "unit": "percent",
        "target": 2.0,  # <2% errors
    },
    "completion_rate": {
        "description": "Percentage of runs completed without escalation",
        "unit": "percent",
        "target": 95.0,
    },
    "automation_coverage": {
        "description": "Percentage of steps that are automated",
        "unit": "percent",
        "target": None,  # Aspirational metric
    },
}

def efficiency_score(cycle_time: float, target_cycle_time: float,
                     error_rate: float, completion_rate: float) -> float:
    """Composite efficiency score 0-100."""
    time_score = min(100, (target_cycle_time / max(cycle_time, 0.1)) * 100)
    error_score = max(0, 100 - (error_rate * 10))
    completion_score = completion_rate
    return round((time_score + error_score + completion_score) / 3, 1)
```

### Process Inventory

```
PROCESS INVENTORY — [Studio Name]
===================================
ID          Name                          Owner       Frequency   Automated   Score
----------  ----------------------------  ----------  ----------  ----------  -----
SOP-OPS-001 Daily standup facilitation    Ops Lead    Daily       No          85
SOP-OPS-002 Client onboarding             PM          Per project Partial     72
SOP-OPS-003 Asset delivery checklist      Prod        Per project No          68
SOP-OPS-004 Invoice processing            Finance     Weekly      Yes         91
SOP-OPS-005 Equipment checkout            Ops         Ad hoc      No          60

Automation opportunities (score <70, frequency = daily/weekly):
  → SOP-OPS-005 Equipment checkout: consider digital sign-out form
  → SOP-OPS-003 Asset delivery: Automate folder structure creation
```

## Scripts

### `scripts/sop_generator.py`

Generates SOP documents from structured process descriptions, with version tracking and efficiency scoring.

```
Usage: python sop_generator.py --name "Client Onboarding" --dept OPS --owner "Alice"
       python sop_generator.py --inventory processes.json
       python sop_generator.py --efficiency process.json --actual-time 4.5 --target-time 3.0
       python sop_generator.py --format json
Output:
  - Complete SOP document with all standard sections
  - Process inventory table
  - Efficiency score and improvement recommendations
  - Automation opportunity analysis
```

## References

### `references/sop_writing_guide.md`
SOP authoring best practices: active voice, numbered steps, avoiding ambiguity, when to use warnings vs notes, screenshot guidelines, review cadence, and change management process for SOP updates.

### `references/process_optimization.md`
Lean process improvement: value stream mapping basics, waste identification (TIMWOOD), Kaizen event facilitation, before/after measurement, and sustaining improvements through visual management.

## Assets

### `assets/sop_template.md`
Full SOP template with all standard sections, guidance text, and formatting conventions.

### `assets/process_inventory_template.csv`
Spreadsheet template for maintaining a complete studio process inventory with scoring columns.

## Quality Standards

- Every recurring process documented as SOP before sixth repetition
- SOPs reviewed every 6 months or after any process failure
- Version history maintained; old versions archived not deleted
- All SOPs tested by someone other than the author before publication
- Process inventory updated quarterly with efficiency scores
- Automation ROI calculated for all manual daily/weekly processes
