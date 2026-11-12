# Model and business-evidence evaluation protocol

**Status: design only. There is no measured model uplift or Nigerian restaurant acceptance yet.**

## Research questions
1. Can every recommended plant alternative pass hard budget, estimated protein, preparation-time and declared-allergen checks?
2. Does NLP-assisted scoring yield more useful rankings than cheapest feasible alone on a small **independently labeled** set of chef/restaurant scenarios?
3. How stable are recommendations at −20%, baseline and +20% ingredient price scenarios?

## Proposed benchmark (do not report as achieved)
- Record at least 10 varied scenarios: tight/wide budget; high/low protein target; peanut exclusion; soy exclusion; short prep time; conflicting constraints; and a no-feasible case.
- Have a reviewer score candidate substitutions on relevance and practical feasibility **without seeing the model rank**.
- Report hard-constraint pass rate, ranking relevance at top 1 and top 3, number of abstentions and cost differences. Include confidence limitations and failed scenarios.
- Compare `cheapest unconstrained`, `cheapest feasible`, `keyword preference`, and `TF-IDF hybrid ranking` on the same cases. Do not claim statistically significant advantages from a tiny, hand-picked dataset.
- Freeze one evaluation set before tuning the weights; document changes openly.

## Nutrition and processing
- Confirm edible serving mass, source nutrient state, and recipe mass conservation. A water-loss concentration effect must not be represented as creating total protein.
- Protein, iron and zinc sums are provisional, not a nutrient quality or absorption guarantee.
- Verify pressing, freezing, frying and grilling protocols (energy, oil, loss, storage). Collect sensory feedback in separate records, not fabricated numeric scores.

## Go / no-go
If data are insufficient or all options violate constraints, show no feasible option. If restaurant reviews reject a treatment, label it experimental and revisit the pilot dish/ingredient rather than forcing a winner.
