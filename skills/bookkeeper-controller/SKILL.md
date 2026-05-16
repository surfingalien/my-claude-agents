# Bookkeeper & Controller Skill

## Overview

Provides accounting operations methodology, month-end close frameworks, internal control templates, and GAAP compliance guidance. Covers day-to-day bookkeeping through controller-level financial statement preparation and audit readiness.

## Capabilities

### Core Accounting Operations

**Accounts Payable**
- Invoice processing and three-way matching (PO → receipt → invoice)
- Payment scheduling and vendor management
- 1099 preparation and vendor master maintenance

**Accounts Receivable**
- Invoice generation and cash application workflows
- Collections management and aging analysis
- Bad debt assessment and reserve calculations

**Payroll Accounting**
- Payroll journal entry templates
- Benefit accruals and PTO liability tracking
- Payroll tax reconciliation to returns

**Cash Management**
- Daily cash position reporting
- Bank reconciliation methodology
- Cash forecasting (weekly rolling 13-week)

**Fixed Assets**
- Capitalization policy enforcement
- Depreciation schedule maintenance (straight-line, declining balance, MACRS)
- Impairment testing triggers and disposal tracking

**Revenue Recognition**
- ASC 606 five-step model: identify contract → identify obligations → determine price → allocate price → recognize revenue
- Deferred revenue roll-forward schedule
- Variable consideration constraint analysis

### Month-End Close Process

**Close Calendar Structure**
```
Pre-Close (Day 1-2):   Bank feed sync, AP cut-off, payroll posting, expense reports
Core Close (Day 3-5):  Recurring JEs, accruals, deferred revenue, FX revaluation
Reconciliations (Day 3-6): All balance sheet accounts
Financial Statements (Day 6-7): Trial balance review, IS/BS/CF preparation, flux analysis
Review & Finalize (Day 7-8): Controller review, period lock, distribution, archive
```

**Month-End Close Checklist Template**
```markdown
# Month-End Close — [Month Year]
**Close Deadline**: [Business Day X]  **Controller**: [Name]
**Status**: In Progress / Complete

## Pre-Close (Day 1-2)
- [ ] Confirm all bank feeds synced through cut-off date
- [ ] Verify all AP invoices received and entered
- [ ] Confirm payroll JEs posted for all pay periods
- [ ] Review and post employee expense reports
- [ ] Verify AR invoices issued for all delivered goods/services
- [ ] Confirm intercompany transactions reconciled with counterparties

## Core Close (Day 3-5)
- [ ] Post standard recurring JEs (depreciation, amortization, rent, insurance)
- [ ] Calculate and post expense accruals (utilities, professional services, commissions)
- [ ] Calculate and post revenue accruals / deferred revenue adjustments
- [ ] Post payroll tax and benefit accruals
- [ ] Record credit card transactions and reconcile statements
- [ ] Post foreign currency revaluation entries
- [ ] Post intercompany elimination entries (if consolidated)

## Reconciliations (Day 3-6)
- [ ] Bank account reconciliations (all accounts)
- [ ] Credit card reconciliations (all cards)
- [ ] AR aging reconciliation to GL
- [ ] AP aging reconciliation to GL
- [ ] Prepaids & deposits reconciliation with amortization schedules
- [ ] Fixed assets — additions, disposals, depreciation
- [ ] Accrued liabilities — detail support for all balances
- [ ] Deferred revenue — roll-forward schedule
- [ ] Intercompany — zero net balance confirmation
- [ ] Equity — stock comp, dividends, treasury stock
- [ ] Payroll tax liability to returns

## Financial Statements (Day 6-7)
- [ ] Generate trial balance, review for unusual balances
- [ ] Prepare income statement with MoM and BvA variance analysis
- [ ] Prepare balance sheet with reconciliation tie-out
- [ ] Prepare cash flow statement
- [ ] Prepare supporting schedules (debt, equity, deferred revenue)
- [ ] Flux analysis — investigate variances >$[X] or >[X]%

## Review & Finalize (Day 7-8)
- [ ] Controller review of all reconciliations and JEs
- [ ] Final review of financial statements
- [ ] Lock period in accounting system
- [ ] Distribute financial package to management
- [ ] Archive supporting documentation
- [ ] Hold close retrospective
```

### Account Reconciliation Template

```markdown
# Account Reconciliation — [Account Name] ([Account #])
**Period**: [Month Year]  **Preparer**: [Name]  **Reviewer**: [Name]
**Date Prepared**: [Date]  **Date Reviewed**: [Date]

## Balance Summary
| Source | Amount |
|--------|--------|
| GL Balance (per trial balance) | $[X] |
| Reconciliation Balance (per supporting detail) | $[X] |
| **Difference** | **$[X]** |

## Reconciling Items
| # | Date | Description | Amount | Status | Resolution Date |
|---|------|-------------|--------|--------|-----------------|
| 1 | [Date] | [Description] | $[X] | Open/Resolved | [Date] |

## Adjusted Balance
| GL Balance | $[X] |
| + Reconciling Items | $[X] |
| **Reconciled Balance** | **$[X]** |
| Subledger Balance | **$[X]** |
| **Variance** | **$0** |

## Roll-Forward
| Component | Amount |
|-----------|--------|
| Beginning balance | $[X] |
| + Additions | $[X] |
| - Reductions | $(X) |
| **Ending balance** | **$[X]** |
```

### Internal Controls Framework

**Segregation of Duties Matrix**
```
Function          | Initiate | Approve | Record | Reconcile
AP Invoices       | AP Clerk | Manager | Controller | Controller
Payroll           | HR       | CFO     | Controller | Controller
Cash Disbursements| AP Clerk | CFO     | Controller | Controller
Revenue           | Sales    | Sales Mgr| Controller| Controller
```

**Journal Entry Controls**
- Every manual JE requires: description (not "adjusting entry"), support documentation, preparer + approver
- Recurring JEs auto-post; manual JEs require secondary approval above $[threshold]
- All JEs visible in audit trail; no backdating without CFO approval + disclosure

**Audit Readiness Standards**
- Support for any balance sheet account available within 24 hours
- Reconciliation workpapers retained for 7 years minimum
- All policy exceptions documented with approvals

### Technical Accounting Standards

**ASC 606 — Revenue Recognition**
Five-step model checklist for each contract:
1. Is there an enforceable contract? (written/oral, commercial substance)
2. What are the distinct performance obligations?
3. What is the transaction price (fixed + variable consideration)?
4. How is price allocated to each obligation (SSP)?
5. When is each obligation satisfied (point-in-time vs. over time)?

**ASC 842 — Lease Accounting**
- Lease classification test: operating vs. finance (5 criteria)
- Right-of-use asset = PV of lease payments + initial direct costs
- Remeasurement triggers: lease modification, reassessment events
- Practical expedients: short-term lease (<12 months), non-lease component separation

**ASC 718 — Stock-Based Compensation**
- Measurement date: grant date (employees) / performance date (non-employees)
- FV methods: Black-Scholes (options), Monte Carlo (market conditions), intrinsic (liability awards)
- 83(b) election window: 30 days from grant, file with IRS + employer copy
- Expense recognition: straight-line (cliff vesting) / accelerated (graded vesting)

**ASC 805 — Business Combinations**
- Acquisition method: measure net assets at fair value at acquisition date
- Goodwill = consideration paid + NCI + fair value of prior equity − net assets at FV
- Contingent consideration: fair value at acquisition date, remeasure each period
- Measurement period: up to 1 year to adjust provisional amounts

## Scripts

### `scripts/reconciliation_tracker.py`

Tracks account reconciliation status across all balance sheet accounts for a given close period.

```
Usage: python reconciliation_tracker.py accounts.csv [--period "Jan 2026"] [--format json|table]
Input: CSV with columns: account_number, account_name, gl_balance, subledger_balance, preparer, status
Output: Reconciliation status report with open items highlighted
```

### `scripts/close_calendar_generator.py`

Generates a month-end close calendar with task assignments and sequential dependencies.

```
Usage: python close_calendar_generator.py --month 2026-01 --close-target 8 [--team team.csv]
Input: Target close day, team member assignments
Output: Day-by-day task calendar with dependencies and ownership
```

### `scripts/flux_analyzer.py`

Automates month-over-month and budget-vs-actual flux analysis with materiality thresholds.

```
Usage: python flux_analyzer.py actuals.csv budget.csv prior_month.csv [--threshold 5000] [--pct 10]
Input: Current actuals, budget, and prior period CSV files
Output: Flux report flagging variances above dollar or percentage threshold
```

## References

### `references/gaap_quick_reference.md`
Key GAAP standards with effective dates, scope, and practical application notes for ASC 606, 842, 718, 805, 350 (goodwill), 360 (impairment), and 230 (cash flows).

### `references/chart_of_accounts_template.md`
Standard chart of accounts structure for a SaaS/tech company with account numbering convention (1000s assets, 2000s liabilities, 3000s equity, 4000s revenue, 5000s COGS, 6000s OpEx).

### `references/close_benchmarks.md`
Industry benchmarks for close cycle times by company size, reconciliation accuracy rates, and audit adjustment norms.

## Assets

### `assets/close_checklist_template.xlsx`
Pre-built Excel close checklist with conditional formatting, task ownership dropdowns, and automated status tracking.

### `assets/reconciliation_workpaper_template.xlsx`
Standardized reconciliation workpaper format accepted by Big Four auditors with built-in roll-forward and variance calculations.

### `assets/journal_entry_template.xlsx`
Journal entry template with required fields, approval routing, and audit trail log.

## Integration Points

- **ERP Systems**: QuickBooks, Xero, NetSuite, Sage Intacct — standard GL export formats
- **Close Management**: FloQast, BlackLine, Trintech — task assignment and sign-off tracking
- **AP Automation**: Bill.com, Tipalti — invoice processing and approval workflows
- **Expense Management**: Expensify, Concur, Brex — expense report coding and GL posting

## Quality Standards

- Zero material audit adjustments (< 1% of total assets)
- 100% of balance sheet accounts reconciled monthly
- All financial statements delivered by published close deadline
- Zero restatements of previously reported results
- Internal control exceptions < 3% of controls tested
- AR aging: < 5% of receivables past 90 days
