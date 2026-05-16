# Experiment Tracker Skill

## Overview

Provides A/B testing, statistical analysis, and experiment lifecycle management capabilities. Covers experiment design with proper sample size calculation, statistical significance testing, multi-armed bandit optimization, Bayesian analysis, and portfolio-level experiment coordination to maximize learning velocity.

## Capabilities

### Experiment Design

**Sample Size Calculator**
```python
import math

def calculate_sample_size(baseline_rate: float, mde: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """
    Calculate required sample size per variant.
    baseline_rate: current conversion rate (e.g. 0.10 for 10%)
    mde: minimum detectable effect as relative change (e.g. 0.10 for 10% lift)
    alpha: significance level (default 0.05 for 95% confidence)
    power: statistical power (default 0.80 for 80% power)
    """
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    
    # Z-scores
    z_alpha = 1.96  # for alpha=0.05 two-tailed
    z_power = 0.84  # for power=0.80
    
    p_bar = (p1 + p2) / 2
    
    n = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) + 
         z_power * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
    
    return math.ceil(n)
```

**Experiment Brief Template**
```
EXPERIMENT BRIEF
================
Title: [Short descriptive name]
Hypothesis: If we [change], then [metric] will [direction] by [amount] because [rationale]
Primary metric: [Single north-star metric]
Guardrail metrics: [Metrics that must not regress]

Baseline rate: X%
MDE (minimum detectable effect): X%
Required sample size per variant: N
Estimated duration: X days at current traffic

Variants:
  Control: [Current state]
  Treatment A: [Change description]
  Treatment B: [Optional second treatment]

Allocation: 50/50 (or 34/33/33 for 3 variants)
Start date: YYYY-MM-DD
Stop date: YYYY-MM-DD
Owner: [Name]
```

### Statistical Analysis

**Frequentist Significance Test**
```python
from scipy import stats

def analyze_ab_test(control_conversions, control_visitors, 
                    treatment_conversions, treatment_visitors):
    control_rate = control_conversions / control_visitors
    treatment_rate = treatment_conversions / treatment_visitors
    
    # Two-proportion z-test
    p_pool = (control_conversions + treatment_conversions) / (control_visitors + treatment_visitors)
    se = math.sqrt(p_pool * (1 - p_pool) * (1/control_visitors + 1/treatment_visitors))
    z_score = (treatment_rate - control_rate) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))
    
    lift = (treatment_rate - control_rate) / control_rate
    
    return {
        "control_rate": control_rate,
        "treatment_rate": treatment_rate,
        "lift": lift,
        "z_score": z_score,
        "p_value": p_value,
        "significant": p_value < 0.05
    }
```

**Bayesian Analysis**
```python
import numpy as np

def bayesian_ab_test(control_conversions, control_visitors,
                     treatment_conversions, treatment_visitors, simulations=100000):
    """Beta-Binomial Bayesian analysis with uninformative prior."""
    # Beta distribution parameters (prior: Beta(1,1) = uniform)
    alpha_control = 1 + control_conversions
    beta_control = 1 + (control_visitors - control_conversions)
    alpha_treatment = 1 + treatment_conversions
    beta_treatment = 1 + (treatment_visitors - treatment_conversions)
    
    control_samples = np.random.beta(alpha_control, beta_control, simulations)
    treatment_samples = np.random.beta(alpha_treatment, beta_treatment, simulations)
    
    prob_treatment_better = np.mean(treatment_samples > control_samples)
    expected_lift = np.mean((treatment_samples - control_samples) / control_samples)
    
    return {
        "prob_treatment_better": prob_treatment_better,
        "expected_lift": expected_lift,
        "credible_interval_95": np.percentile(treatment_samples - control_samples, [2.5, 97.5]).tolist()
    }
```

### Multi-Armed Bandit

**Epsilon-Greedy Bandit**
```python
class EpsilonGreedyBandit:
    def __init__(self, variants: list, epsilon: float = 0.1):
        self.variants = variants
        self.epsilon = epsilon
        self.counts = {v: 0 for v in variants}
        self.rewards = {v: 0.0 for v in variants}
    
    def select_variant(self) -> str:
        if random.random() < self.epsilon:
            return random.choice(self.variants)  # Explore
        return max(self.rewards, key=lambda v: self.rewards[v] / max(self.counts[v], 1))  # Exploit
    
    def update(self, variant: str, reward: float):
        self.counts[variant] += 1
        n = self.counts[variant]
        self.rewards[variant] = ((n - 1) / n) * self.rewards[variant] + (1 / n) * reward
    
    def allocations(self) -> dict:
        total = sum(self.counts.values())
        if total == 0:
            return {v: 1/len(self.variants) for v in self.variants}
        return {v: self.counts[v] / total for v in self.variants}
```

### Experiment Portfolio Management

**Portfolio Status Template**
```
EXPERIMENT PORTFOLIO — [Month Year]
=====================================
Running experiments: N
Completed this quarter: N
Significant wins: N | Losses: N | Inconclusive: N
Win rate: X%

ACTIVE EXPERIMENTS
------------------
[ID]  [Name]                    [Day X/Y]  [Status]   [Owner]
EXP-001  Checkout button color     Day 5/14   On track   Alice
EXP-002  Email subject line test   Day 12/21  On track   Bob
EXP-003  Pricing page layout       Day 2/14   On track   Carol

COMPLETED THIS QUARTER
----------------------
[ID]  [Name]           [Result]   [Lift]   [Shipped]
EXP-010  Hero copy test   WIN        +8.3%    Yes
EXP-011  CTA placement    LOSS       -2.1%    No
EXP-012  Font size test   NULL       +0.4%    No

INSIGHTS & LEARNINGS
--------------------
1. [Key learning from winning experiments]
2. [Key learning from losing experiments]
3. [Patterns observed across portfolio]

NEXT UP (QUEUE)
---------------
1. [Experiment name] — [Hypothesis summary] — Owner: [Name]
2. [Experiment name] — [Hypothesis summary] — Owner: [Name]
```

## Scripts

### `scripts/experiment_designer.py`

Calculates sample sizes, generates experiment briefs, and analyzes A/B test results.

```
Usage: python experiment_designer.py --baseline 0.10 --mde 0.10
       python experiment_designer.py --analyze --control 450,5000 --treatment 495,5000
       python experiment_designer.py --portfolio experiments.json
       python experiment_designer.py --format json
Output:
  - Required sample size per variant
  - Estimated test duration
  - Statistical analysis (frequentist + Bayesian)
  - Experiment brief document
  - Portfolio status report
```

## References

### `references/statistical_testing_guide.md`
Statistical significance testing: Type I/II errors, p-values, confidence intervals, multiple testing correction (Bonferroni, FDR), sequential testing pitfalls, peeking problem, and when to use Bayesian vs frequentist approaches.

### `references/experiment_lifecycle.md`
End-to-end experiment process: ideation scoring (ICE/PIE frameworks), pre-experiment checklist, instrumentation requirements, monitoring during experiment, decision framework, shipping process, and retrospective template.

## Assets

### `assets/experiment_brief_template.md`
Fillable experiment brief: hypothesis, metrics, sample size calculation, variant descriptions, timeline, success criteria, and stakeholder sign-off.

### `assets/results_readout_template.md`
Experiment results presentation: executive summary, statistical results, qualitative insights, recommendation, next steps, and learnings for the knowledge base.

## Quality Standards

- Every experiment starts with a written brief reviewed by a statistician
- Sample size calculated before experiment starts (no peeking adjustments)
- Guardrail metrics monitored daily during experiment runtime
- Results documented in shared knowledge base within 48 hours of completion
- Win rate tracked quarterly; target ≥35% significant wins
- No experiment runs longer than 30 days without checkpoint review
