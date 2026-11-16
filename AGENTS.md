# Naija MenuShift — agent instructions (Codex, Claude, GitHub Copilot)

This repo contains distinct research prototypes for Hack the Fork Nigeria 2026: Challenge 2 (menu adaptation) and Challenge 3 (food market opportunity). Challenge 3 does not change the commercial target of the Challenge 2 software. Its product scope is **many Nigerian dishes**; **suya is only the first use case**. Never hardcode the architecture to tofu or suya.

## Invariants
- `data/demo/` is SYNTHETIC. Do not describe demo numbers as real prices, measured nutrients, verified taste, or evidence of affordability.
- `data/verified/` has to remain fail-closed until actual source/date/region and recipe observations are supplied. Never silently replace missing evidence with synthetic values.
- Beef/reference options are never eligible plant-based recommendations. Plant recipes must contain no declared animal ingredients.
- A spreadsheet label is not an allergy or cross-contact certification. Explicitly report incomplete labeling.
- Avoid unsupported assertions about protein equivalence, cooking yield, texture, nutritional adequacy or local acceptance.
- All substantive changes need unit tests and clear limitations. Keep the app usable with only local CSVs; no paid model APIs or secret keys required.
- Keep personal contact information and credentials out of git.

- **Challenge 3:** `data/challenge3/opportunities.csv` contains 48 sparse market candidates, not 48 sales observations. The survey is empty. Never infer a real market winner from soybean production or from the synthetic market/segmentation demos. Use consented survey responses only and cite product-specific interview and retail evidence.

## Workflows / skills
- For research CSV changes, invoke `.agents/skills/menushift-data-evidence/SKILL.md`.
- For ranking, AI, cost and testing, invoke `.agents/skills/menushift-recommendations/SKILL.md`.
- For Streamlit UI or charts, invoke `.agents/skills/menushift-streamlit-ui/SKILL.md`.
- If Streamlit's CLI has `streamlit skills`, run `streamlit skills --yes` locally for official current Streamlit agent guidance; it is an optional developer setup step and not required to run CI.

## Commands
```bash
python -m pip install -e '.[dev]'
python -m pytest -q
ruff check src tests app.py
menushift --dish suya --budget 1500 --protein 10 --sensitivity
streamlit run app.py
```

Review design changes on narrow screens, with a no-feasible-option case and with research data unavailable. Never treat code-only inspection as proof of visual QA.
