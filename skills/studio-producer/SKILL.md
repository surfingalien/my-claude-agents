# Studio Producer Skill

## Overview

Provides strategic portfolio management and executive-level creative orchestration for studio producers. Covers Tier 1/2 project prioritization, portfolio health monitoring, resource allocation optimization, ROI tracking, and stakeholder reporting for complex multi-project studio environments.

## Capabilities

### Portfolio Tier System

**Tier 1 — Flagship Projects**
- Highest strategic value; primary revenue drivers or brand-defining work
- Full resource allocation; senior talent assigned
- Weekly executive review; CEO/CCO visibility
- Success metrics: revenue contribution, brand impact, award potential

**Tier 2 — Core Projects**
- Standard commercial work; solid revenue with manageable risk
- Standard resource allocation; mid-senior talent
- Bi-weekly producer review
- Success metrics: margin, on-time delivery, client satisfaction

**Tier 3 — Pipeline Projects**
- Lower priority; exploratory or early-stage
- Minimal resource commitment until greenlit
- Monthly portfolio review

### Portfolio Plan Template

```
STRATEGIC PORTFOLIO PLAN — [Quarter] [Year]
============================================
Studio: [Name] | Producer: [Name] | Approved by: [Name]

PORTFOLIO OVERVIEW
------------------
Active projects:   [N]  (T1: [N] | T2: [N] | T3: [N])
Total budget:      $[Amount]
Projected revenue: $[Amount]
Target margin:     [X]%
Team capacity:     [N] FTE | [X]% allocated

TIER 1 — FLAGSHIP
-----------------
[Project Name]
  Client:    [Name]
  Budget:    $[Amount]
  Revenue:   $[Amount]
  Margin:    [X]%
  Timeline:  [Start] → [End]
  Team:      [Lead + N members]
  Status:    [On track / At risk / Blocked]
  Risk:      [Key risk]

TIER 2 — CORE
--------------
[Continue pattern...]

RESOURCE ALLOCATION
-------------------
Name           Role           T1 Projects  T2 Projects  Capacity
----------     ----------     -----------  -----------  --------
[Name]         Creative Lead  60%          30%          90% ✓
[Name]         Producer       80%          10%          90% ✓
[Name]         Designer       40%          50%          90% ✓

FINANCIAL SUMMARY
-----------------
              Q1      Q2      Q3      Q4      Total
Revenue:      $0      $0      $0      $0      $0
Direct costs: $0      $0      $0      $0      $0
Margin:        0%      0%      0%      0%       0%

STRATEGIC PRIORITIES
--------------------
1. [Priority focus area with rationale]
2. [Priority focus area with rationale]
3. [Priority focus area with rationale]
```

### ROI Tracking

```python
def calculate_project_roi(revenue: float, direct_costs: float,
                           overhead_allocation: float) -> dict:
    total_cost = direct_costs + overhead_allocation
    gross_profit = revenue - direct_costs
    net_profit = revenue - total_cost
    gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
    roi = (net_profit / total_cost * 100) if total_cost > 0 else 0
    return {
        "revenue": revenue,
        "direct_costs": direct_costs,
        "overhead": overhead_allocation,
        "total_cost": total_cost,
        "gross_profit": gross_profit,
        "net_profit": net_profit,
        "gross_margin_pct": round(gross_margin, 1),
        "roi_pct": round(roi, 1),
    }

TIER_MARGIN_TARGETS = {
    "tier1": 45,  # Flagship: 45%+ gross margin
    "tier2": 35,  # Core: 35%+ gross margin
    "tier3": 25,  # Pipeline: 25%+ or exploratory
}
```

### Portfolio Review Template

```
PORTFOLIO REVIEW — [Month Year]
================================
Presenter: [Name] | Audience: [Executive team]

HEADLINE METRICS
----------------
Portfolio revenue (MTD):  $[Amount]  vs target $[Amount]  ([+/-X%])
Portfolio margin (MTD):   [X]%       vs target [X]%       ([+/-X pts])
On-time delivery:         [X]%       vs target 90%
Client NPS:               [Score]    vs target 50

PROJECT HEALTH DASHBOARD
------------------------
[Project] T1  🟢  $[Rev]  [X]% margin  Day [N]/[Total]  [Lead]
[Project] T2  🟡  $[Rev]  [X]% margin  Day [N]/[Total]  [Lead]
[Project] T2  🔴  $[Rev]  [X]% margin  Day [N]/[Total]  [Lead]

KEY DECISIONS
-------------
1. [Decision needed] — Options: [A] vs [B] — Deadline: [Date]
2. [Decision needed] — Options: [A] vs [B] — Deadline: [Date]

PIPELINE UPDATE
---------------
[Prospect name] — $[Value] opportunity — Stage: [Discovery/Proposal/Negotiation]

RETROSPECTIVE HIGHLIGHTS
------------------------
Win:  [What went well this month]
Miss: [What didn't go as planned]
Fix:  [What we're changing]
```

## Scripts

### `scripts/portfolio_planner.py`

Generates portfolio plans, ROI calculations, and executive review reports for studio producers.

```
Usage: python portfolio_planner.py --projects projects.json --quarter Q1 --year 2026
       python portfolio_planner.py --roi --revenue 150000 --costs 80000 --overhead 20000
       python portfolio_planner.py --review projects.json --month "January 2026"
       python portfolio_planner.py --format json
Output:
  - Strategic portfolio plan document
  - Project ROI analysis
  - Portfolio health dashboard
  - Executive review report
  - Resource allocation table
```

## References

### `references/portfolio_management_guide.md`
Portfolio strategy: tier assignment criteria, rebalancing triggers, capacity planning formulas, pipeline-to-project conversion rates, and healthy portfolio composition ratios (T1/T2/T3 balance).

### `references/studio_financial_model.md`
Studio financial fundamentals: direct vs indirect costs, overhead allocation methods, utilization rate calculation, target margin by project type, and financial KPIs for studio health.

## Assets

### `assets/portfolio_plan_template.md`
Quarterly portfolio plan template with all sections pre-structured for studio context.

### `assets/executive_review_template.md`
Monthly executive portfolio review presentation template with headline metrics, project dashboard, and decisions section.

## Quality Standards

- Portfolio plan published at start of each quarter
- Project tier reviewed at each phase gate (no tier drift without approval)
- Monthly executive portfolio review with all Tier 1 leads present
- Margin variance >10pts triggers immediate producer review
- Resource allocation never exceeds 90% capacity (10% buffer for firefighting)
- All new projects require ROI projection before kickoff approval
