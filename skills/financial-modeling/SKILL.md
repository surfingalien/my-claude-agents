# Financial Modeling Skill

## Overview

Provides institutional-quality financial modeling frameworks, valuation methodologies, and analytical templates. Covers three-statement models, DCF analysis, comparable company analysis, LBO modeling, M&A modeling, and scenario/sensitivity analysis.

## Capabilities

### Three-Statement Financial Model

Integrated income statement, balance sheet, and cash flow model with dynamic linking. All three statements balance automatically; changes in any assumption flow through the entire model.

**Model Architecture**
```
Layer 1: Assumptions (color-coded inputs — never hardcode in formulas)
Layer 2: Income Statement (revenue down to net income)
Layer 3: Balance Sheet (assets = liabilities + equity)
Layer 4: Cash Flow Statement (operating + investing + financing)
Layer 5: Scenario Switches (base/upside/downside toggle)
Layer 6: Outputs & Charts (summary page for stakeholders)
```

**Three-Statement Model Template**
```markdown
# Financial Model: [Company / Project Name]
**Version**: [X.X]  **Author**: [Name]  **Date**: [Date]
**Purpose**: [Investment decision / Budget planning / Strategic analysis]

## Key Assumptions
| Assumption | Base Case | Upside | Downside | Source |
|------------|-----------|--------|----------|--------|
| Revenue growth rate | X% | Y% | Z% | [Historical trend / Market data] |
| Gross margin | X% | Y% | Z% | [Historical avg / Industry benchmark] |
| OpEx as % of revenue | X% | Y% | Z% | [Management guidance / Peer analysis] |
| CapEx as % of revenue | X% | Y% | Z% | [Historical / Industry standard] |
| Working capital days | X days | Y days | Z days | [Historical trend] |

## Income Statement Summary ($ thousands)
| Line Item | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|-----------|--------|--------|--------|--------|--------|
| Revenue | | | | | |
| COGS | | | | | |
| Gross Profit | | | | | |
| Gross Margin % | | | | | |
| Operating Expenses | | | | | |
| EBITDA | | | | | |
| EBITDA Margin % | | | | | |
| D&A | | | | | |
| EBIT | | | | | |
| Net Income | | | | | |

## Cash Flow Summary ($ thousands)
| Line Item | Year 1 | Year 2 | Year 3 | Year 4 | Year 5 |
|-----------|--------|--------|--------|--------|--------|
| Net Income | | | | | |
| D&A (add back) | | | | | |
| Changes in Working Capital | | | | | |
| Operating Cash Flow | | | | | |
| CapEx | | | | | |
| Free Cash Flow | | | | | |
| Cumulative FCF | | | | | |

## Sensitivity Analysis (FCF Year 3)
|                    | Revenue Growth -5% | Base | Revenue Growth +5% |
|--------------------|-------------------|------|-------------------|
| **Margin -2%**     | [FCF]             | [FCF]| [FCF]             |
| **Base Margin**    | [FCF]             | [FCF]| [FCF]             |
| **Margin +2%**     | [FCF]             | [FCF]| [FCF]             |
```

### DCF Valuation

**WACC Calculation**
```
WACC = (E/V × Re) + (D/V × Rd × (1 - T))
Where:
  E = market value of equity
  D = market value of debt
  V = E + D
  Re = cost of equity (CAPM: Rf + β × ERP)
  Rd = cost of debt (yield on outstanding debt)
  T = marginal tax rate
```

**Terminal Value Methods**
- Gordon Growth Model: TV = FCF_n × (1 + g) / (WACC - g)
- Exit Multiple: TV = EBITDA_n × Exit Multiple (cross-check with comps)

**DCF Scenarios**
| Scenario | Revenue CAGR | Terminal Multiple | Implied Price | Weight |
|----------|-------------|------------------|--------------|--------|
| Bull | X% | XXx | $[X] | 25% |
| Base | X% | XXx | $[X] | 50% |
| Bear | X% | XXx | $[X] | 25% |
| **Weighted Target** | | | **$[X]** | |

### Comparable Company Analysis

**Peer Selection Criteria**
- Same sector and business model
- Similar revenue scale (±50%)
- Similar growth profile (±10pp)
- Comparable margins
- Publicly traded (for market-based multiples)

**Comps Table**
| Peer | EV | Revenue | EBITDA | EV/Revenue | EV/EBITDA | P/E | NTM Growth |
|------|----|---------|--------|-----------|-----------|-----|-----------|
| [Peer 1] | | | | X.Xx | X.Xx | X.Xx | X% |
| [Peer 2] | | | | X.Xx | X.Xx | X.Xx | X% |
| Peer Median | | | | X.Xx | X.Xx | X.Xx | X% |
| **[Target]** | | | | **X.Xx** | **X.Xx** | **X.Xx** | **X%** |

### Variance Analysis Report Template

```markdown
# Monthly Variance Analysis — [Month Year]

## Executive Summary
[2-3 sentences: Are we on track? Key variances and forward impact?]

## Revenue Variance
| Revenue Line | Budget | Actual | Variance ($) | Variance (%) | Root Cause |
|-------------|--------|--------|-------------|-------------|------------|
| [Product A] | $X | $Y | $(Z) | (X%) | [Explanation] |
| **Total Revenue** | **$X** | **$Y** | **$(Z)** | **(X%)** | |

## Cost Variance
| Cost Category | Budget | Actual | Variance ($) | Variance (%) | Root Cause |
|-------------|--------|--------|-------------|-------------|------------|
| COGS | $X | $Y | $(Z) | (X%) | [Explanation] |
| Sales & Marketing | $X | $Y | $Z | X% | [Explanation] |

## Key Actions Required
1. [Action with owner and deadline]
2. [Action with owner and deadline]

## Forecast Impact
[How do these variances change the full-year outlook?]
```

### LBO Model Framework

**Returns Analysis**
```
Entry: EV / EBITDA at entry multiple → total purchase price
Financing: Debt schedule (senior, subordinated, mezz) → annual interest + amortization
Operations: Revenue growth + margin expansion → EBITDA growth → FCF for debt paydown
Exit: EV / EBITDA at exit multiple → equity proceeds → IRR and MOIC calculation
```

**Credit Metrics to Monitor**
- Total Leverage: Total Debt / EBITDA (covenant trigger if > X.Xx)
- Interest Coverage: EBITDA / Interest Expense (covenant trigger if < X.Xx)
- Debt Service Coverage: (EBITDA - CapEx) / (Interest + Principal)

## Scripts

### `scripts/dcf_calculator.py`

Builds a multi-scenario DCF valuation from revenue and margin assumptions.

```
Usage: python dcf_calculator.py --revenue 100 --growth 0.25 --margin 0.20 --wacc 0.10 --terminal-growth 0.03
Options:
  --revenue     Base year revenue ($M)
  --growth      Annual revenue growth rate (decimal)
  --margin      EBITDA margin (decimal)
  --wacc        Weighted average cost of capital (decimal)
  --terminal-growth  Terminal growth rate for Gordon Growth Model
  --years       Forecast period in years (default: 5)
  --scenarios   Run bull/base/bear scenario table (flag)
  --format      Output format: table|json (default: table)
Output: Year-by-year FCF projection, terminal value, implied EV, equity value per share
```

### `scripts/ratio_analyzer.py`

Calculates comprehensive financial ratios from income statement and balance sheet inputs.

```
Usage: python ratio_analyzer.py financials.csv [--benchmark industry.csv] [--format json|table]
Input CSV columns: year, revenue, cogs, gross_profit, ebitda, ebit, net_income, total_assets,
                   total_debt, cash, equity, capex, working_capital
Output:
  Profitability: Gross margin, EBITDA margin, net margin, ROIC, ROE, ROA
  Leverage: Net debt/EBITDA, interest coverage, debt/equity
  Efficiency: Asset turnover, working capital days, cash conversion cycle
  Growth: YoY revenue growth, EBITDA growth, FCF growth
```

### `scripts/scenario_builder.py`

Generates three-scenario (bull/base/bear) financial projections with sensitivity tables.

```
Usage: python scenario_builder.py base_assumptions.json [--output scenarios.csv] [--sensitivity]
Input: JSON with base case assumptions (revenue, margins, growth rates, CapEx, working capital)
Output:
  - 5-year P&L for each scenario
  - Key metric comparison table
  - Sensitivity table (revenue growth × margin)
  - Scenario break-even analysis
```

### `scripts/comps_screener.py`

Builds a comparable company analysis table from a peer list with financial metrics.

```
Usage: python comps_screener.py peers.csv target.csv [--multiples ev_revenue,ev_ebitda,pe]
Input: CSV files with EV, revenue, EBITDA, net income, growth rates for peers and target
Output: Sorted comps table with median, 25th/75th percentile, and target positioning
```

## References

### `references/valuation_multiples_by_sector.md`
Sector-specific valuation multiple ranges for SaaS, fintech, healthcare tech, industrials, consumer, and financials — updated quarterly with market data context.

### `references/financial_modeling_best_practices.md`
Modeling standards: color conventions, error-check formulas, circular reference handling, audit trail documentation, version control protocols.

### `references/wacc_inputs_guide.md`
Step-by-step WACC calculation guide with beta sources (Bloomberg, Damodaran), equity risk premium data, and size premium adjustments.

## Assets

### `assets/three_statement_model_template.xlsx`
Fully linked IS/BS/CF model with scenario toggle, sensitivity tables, and chart outputs. Includes formula audit map and assumption documentation.

### `assets/dcf_template.xlsx`
DCF model with WACC calculator, Gordon Growth and exit multiple terminal value methods, football field chart, and scenario weighting.

### `assets/comps_table_template.xlsx`
Comparable company analysis template with automatic percentile calculations, premium/discount to median display, and implied price range output.

## Quality Standards

- Financial models audit-ready with zero formula errors and full assumption documentation
- Sensitivity analysis included on all recommendations with defined break-even thresholds
- Scenario analysis (bull/base/bear) required for all investment decisions
- Forecast accuracy within ±5% of actuals for 80%+ of line items
- All models usable by someone who didn't build them (documented, labeled, structured)
