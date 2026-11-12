# Project brief and problem statement

**Challenge:** Hack the Fork Nigeria 2026, Challenge 2 — AI for Plant-Based Menu Innovation.

**Who:** Nigerian restaurant owners, chefs and menu planners assessing a new plant-based option.

**Problem:** Restaurant teams seeking to add plant-based alternatives face uncertainty about local ingredient substitutions, serving cost, nutritional suitability, preparation effort and culinary fit. This is an **unvalidated problem hypothesis** until user interviews are completed.

**Solution hypothesis:** A reusable, evidence-aware recommendation and optimisation tool can narrow a set of ingredient/preparation options to realistic candidates for a specified restaurant dish and the chef's constraints, explain trade-offs, and reveal where direct food testing is required.

**First demonstration:** Beef suya vs four plant-based preparations using tofu (plain marinated, pressed, frozen then thawed, pressed/fried/grilled). Beef is context/reference only. This is a **pilot**, not a permanent restriction to tofu or suya.

**Next research cases:** Meat pie, egusi soup, jollof/chicken, pepper soup. Additional plant protein candidates: cowpea, soy-derived products, Bambara groundnut, groundnut and other evaluated options. Do not promise that these are functional or nutritionally equivalent without testing.

## Proposed measurable success criteria (not achieved)

- Four tofu methods plus one beef reference represented with source-backed cost, iron, zinc and protein values for a **defined portion and state**.
- 100% of displayed feasible plant recommendations pass budget/protein/preparation checks in documented test cases.
- Every displayed ingredient price has amount/unit, source, collection date and location; nutrition source documents measurement/food-state.
- The system says **no feasible option** rather than quietly relaxing hard constraints.
- Baseline and ±20% ingredient-price scenarios both work and are explained.
- At least five normal/edge test cases and one food practitioner review are documented.
- A measurable comparison with cheapest-only and generic recipe-generation approaches demonstrates whether the NLP/ranking layer adds any value.

## Out of scope for the hackathon

Clinical nutrition advice, proven protein-quality equivalence, safety certification, regulatory approvals, consumer taste guarantees, large-scale recipe coverage, full production deployment or a proven commercial business model.

## Decisions to confirm

- What counts as one serving and what cooking loss will be measured?
- Is the budget purchase cost only or fully loaded price including energy/labour? (Current engine includes all.)
- Which Nigerian supplier/locality is the initial price reference?
- Is the AI experiment meaningful relative to a deterministic baseline?
- Are pre-hackathon code/build activities permitted? Verify with organisers.
