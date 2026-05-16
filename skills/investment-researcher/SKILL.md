# Investment Researcher Skill

## Overview

Provides institutional-quality investment research frameworks for equity analysis, due diligence, thesis construction, and portfolio decision support. Covers fundamental and quantitative analysis across public equities, private markets, and alternative assets.

## Capabilities

### Investment Research Process

**5-Phase Research Workflow**

```
Phase 1 — Screening & Idea Generation
  - Run quantitative screens: value, quality, momentum, growth factors
  - Monitor industry themes, regulatory changes, structural shifts
  - Track insider activity, activist positions, institutional flow changes

Phase 2 — Initial Assessment
  - Review last 3 years of financial statements and earnings transcripts
  - Map competitive landscape and identify moat (or lack thereof)
  - Estimate rough valuation range to determine if research is warranted
  - Identify 3-5 key questions that will determine the investment outcome

Phase 3 — Deep Dive Research
  - Build detailed financial model with scenario analysis
  - Conduct primary research: customer calls, expert interviews, supplier checks
  - Analyze alternative data sources for real-time business momentum
  - Stress-test thesis against historical analogs and bear case scenarios

Phase 4 — Thesis Formulation & Recommendation
  - Write full research report with actionable recommendation
  - Define monitoring framework with thesis breakers and catalyst timelines
  - Set price targets for upside, base, and downside scenarios

Phase 5 — Ongoing Monitoring
  - Track quarterly earnings against model forecasts
  - Monitor thesis breaker triggers and catalyst progression
  - Update position sizing 
  - Publish update notes when material developments occur
```

### Investment Research Report Template

```markdown
# Investment Research: [Company / Asset Name]
**Ticker**: [Ticker]  **Sector**: [Sector]  **Market Cap**: $[X]B
**Rating**: Buy / Hold / Sell  **Price Target**: $[X] ([X]% upside/downside)
**Conviction Level**: High / Medium / Low
**Investment Horizon**: [6 months / 1-3 years / 5+ years]
**Analyst**: [Name]  **Date**: [Date]

---

## Executive Summary
[3-4 sentences: What is the thesis? Why now? What is the expected return?]

---

## Investment Thesis
### Core Arguments (Bull Case)
1. **[Driver 1]**: [Quantified argument with supporting data]
2. **[Driver 2]**: [Quantified argument with supporting data]
3. **[Driver 3]**: [Quantified argument with supporting data]

### Key Catalysts & Timeline
| Catalyst | Expected Date | Impact on Price | Probability |
|----------|--------------|----------------|-------------|
| [Catalyst 1] | [Date/Quarter] | +X% | High/Med/Low |
| [Catalyst 2] | [Date/Quarter] | +X% | High/Med/Low |

---

## Bear Case & Risk Factors
1. **[Risk 1]**: [Description with quantified impact] — **Mitigation**: [How addressed]
2. **[Risk 2]**: [Description with quantified impact] — **Mitigation**: [How addressed]
3. **[Risk 3]**: [Description with quantified impact] — **Mitigation**: [How addressed]

### Thesis Breakers (Exit Triggers)
- If [specific metric] falls below [threshold], thesis is invalidated
- If [specific event] occurs, reassess position immediately
- If [competitive development] materializes, downside case becomes base case

---

## Valuation
### DCF Analysis
| Scenario | Revenue CAGR | Terminal Multiple | Implied Price | Weight |
|----------|-------------|------------------|--------------|--------|
| Bull | X% | XXx | $[X] | 25% |
| Base | X% | XXx | $[X] | 50% |
| Bear | X% | XXx | $[X] | 25% |
| **Weighted Target** | | | **$[X]** | |

### Comparable Analysis
| Peer | EV/Revenue | EV/EBITDA | P/E | Growth |
|------|-----------|-----------|-----|--------|
| [Peer 1] | X.Xx | X.Xx | X.Xx | X% |
| [Peer 2] | X.Xx | X.Xx | X.Xx | X% |
| **[Target]** | **X.Xx** | **X.Xx** | **X.Xx** | **X%** |
| Peer Median | X.Xx | X.Xx | X.Xx | X% |

---

## Financial Summary
| Metric | FY-1 (A) | FY0 (A) | FY+1 (E) | FY+2 (E) | FY+3 (E) |
|--------|---------|---------|----------|----------|----------|
| Revenue ($M) | | | | | |
| Revenue Growth | | | | | |
| Gross Margin | | | | | |
| EBITDA Margin | | | | | |
| FCF Margin | | | | | |
| Net Debt/EBITDA | | | | | |
| ROIC | | | | | |

---

## Competitive Landscape
| Competitor | Market Share | Key Advantage | Key Weakness |
|-----------|-------------|---------------|-------------|
| [Comp 1] | X% | [Advantage] | [Weakness] |
| **[Target]** | **X%** | **[Advantage]** | **[Weakness]** |
```

### Due Diligence Framework

**Due Diligence Checklist**
```markdown
# Due Diligence Report: [Company Name]
**Stage**: Initial / Intermediate / Final  **Date**: [Date]

## Financial DD
- [ ] Revenue quality — recurring vs. one-time, customer concentration (top 10 customers = X% of revenue)
- [ ] Earnings quality — cash conversion, accrual analysis, non-GAAP adjustments
- [ ] Balance sheet — off-balance sheet items, contingent liabilities, debt covenants
- [ ] Working capital — DSO/DPO/DIO trends, seasonality
- [ ] Capital efficiency — ROIC trends, CapEx requirements (maintenance vs. growth)

## Operational DD
- [ ] Customer interviews (n=[X]) — satisfaction, switching likelihood, competitive alternatives
- [ ] Supplier analysis — concentration, contract terms, pricing power
- [ ] Technology assessment — architecture scalability, technical debt, competitive differentiation
- [ ] Management reference checks (n=[X]) — leadership quality, integrity, execution track record

## Market DD
- [ ] TAM/SAM/SOM validation with bottom-up analysis
- [ ] Competitive positioning — sustainable advantages vs. temporary leads
- [ ] Regulatory risk — compliance, pending legislation, enforcement trends
- [ ] Secular trend alignment — tailwinds and headwinds

## Legal DD
- [ ] IP portfolio — patents, trademarks, trade secrets
- [ ] Litigation review — pending cases, historical settlements, contingent liabilities
- [ ] Contract review — key customer/supplier agreements, change of control provisions
- [ ] Regulatory compliance — historical violations, pending investigations

## Red Flags
| Finding | Severity | Impact | Recommendation |
|---------|----------|--------|----------------|
| [Finding] | High/Med/Low | [Description] | [Action] |
```

### Competitive Moat Assessment

**Porter's Five Forces Application**
```
Threat of New Entrants:
  - Capital requirements to enter
  - Regulatory barriers
  - Existing brand equity and switching costs

Supplier Power:
  - Concentration of suppliers (HHI)
  - Switching costs to alternative suppliers
  - Forward integration threat

Buyer Power:
  - Customer concentration
  - Price sensitivity / elasticity
  - Backward integration threat

Threat of Substitutes:
  - Performance-price tradeoff of alternatives
  - Switching costs to substitutes

Competitive Rivalry:
  - Number and relative size of competitors
  - Industry growth rate
  - Exit barriers
```

**Moat Strength Rating**
| Moat Type | Definition | Evidence to Look For |
|-----------|-----------|---------------------|
| Network Effects | Value increases with each additional user | DAU/MAU growth, engagement density |
| Switching Costs | High cost or friction to change provider | Churn < 5%, NPS > 50, integration depth |
| Cost Advantages | Structural cost position below peers | Gross margin premium vs. peers |
| Intangible Assets | Patents, brands, regulatory licenses | Patent count, brand premium, license duration |
| Efficient Scale | Natural monopoly in niche market | Market share concentration |

### Risk Metrics

**Portfolio Risk Assessment**
```
Beta: sensitivity to market movements (
Value-at-Risk (VaR): maximum expected loss at 95% confidence over 1 day/1 month
Sharpe Ratio: (Return - Rf) / σ — risk-adjusted return
Sortino Ratio: (Return - Rf) / downside σ — penalizes only downside volatility
Maximum Drawdown: largest peak-to-trough decline in holding period
```

## Scripts

### `scripts/thesis_tracker.py`

Tracks investment thesis health against predefined triggers and catalysts over time.

```
Usage: python thesis_tracker.py thesis.json [--update-metrics metrics.csv] [--format json|table]
Input thesis.json fields: ticker, thesis_summary, bull_drivers, thesis_breakers (metric, threshold, current),
                          catalysts (event, expected_date, probability), price_target, conviction
Output:
  - Thesis scorecard: bull drivers status (intact/deteriorating/broken)
  - Thesis breaker monitoring table with current vs. threshold
  - Catalyst countdown by expected date
  - Overall thesis health: Green / Yellow / Red
```

### `scripts/comps_valuation.py`

Builds a comparable company analysis and implied valuation range for a target company.

```
Usage: python comps_valuation.py peers.csv target.json [--multiples ev_revenue,ev_ebitda,pe,ev_fcf]
Input: peers.csv with financial metrics, target.json with target company metrics and shares outstanding
Output:
  - Ranked comps table by metric
  - Implied value at 25th/median/75th percentile for each multiple
  - Football field chart data (valuation bridge across methodologies)
  - Premium/discount to peer median analysis
```

### `scripts/dd_checklist_generator.py`

Generates a customized due diligence checklist 

```
Usage: python dd_checklist_generator.py --stage [initial|intermediate|final] --sector [saas|hardware|services|marketplace] --type [public|private|ma]
Output: Markdown DD checklist with sector-specific items and priority ranking (must-have vs. nice-to-have)
```

## References

### `references/sector_specific_metrics.md`
Industry-specific KPIs and valuation approaches for SaaS (ARR, NRR, CAC payback, Rule of 40), healthcare (pipeline probability, FDA timelines), fintech (take rate, loss rate, unit economics), and industrials (backlog, book-to-bill, cycle positioning).

### `references/red_flags_library.md`
Catalog of documented due diligence red flags with historical context: revenue concentration risks, founder equity sale patterns, related-party transactions, non-GAAP manipulation tactics, and working capital deterioration signals.

### `references/primary_research_guide.md`
Guide to conducting primary research: expert network calls, customer reference interviews, supplier checks, and channel checks — with question frameworks and documentation templates.

## Assets

### `assets/investment_thesis_one_pager.md`
One-page investment thesis template for initial pitch to investment committee: thesis in 3 bullets, bull/bear case, valuation range, catalyst timeline, position sizing recommendation.

### `assets/dd_workbook_template.xlsx`
Excel due diligence workbook with tabs for financial analysis, red flag tracking, management assessment scorecard, and investment committee decision log.

## Quality Standards

- Investment recommendations generate risk-adjusted returns above benchmark over stated time horizon
- 80%+ of thesis breakers correctly identified before material price movements
- Due diligence process catches 90%+ of material risks before investment decision
- Forecast accuracy within ±10% for revenue, ±15% for earnings on covered names
- All recommendations have clearly documented catalysts with defined timelines and thesis breakers
