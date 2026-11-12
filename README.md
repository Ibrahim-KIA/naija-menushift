# Naija MenuShift 🌿

**Hack the Fork Nigeria 2026 · Challenge 2 · Team research prototype**

A reusable, evidence-aware decision-support tool for Nigerian restaurant teams exploring plant-based alternatives to familiar menu items. **Suya is the first demonstration, not the product's permanent scope.** The data model already lists future candidate dishes (meat pie, egusi, jollof with chicken, pepper soup); their formulas and verified data have **not** yet been developed.

> **IMPORTANT: The default dataset is completely SYNTHETIC.** Every demonstration price, nutrient value, recipe weight, energy charge, preparation time and resulting ranking is fictional. Never quote these values as actual Nigerian prices, measured nutritional content, or tested restaurant recommendations. The empty `data/verified/` templates intentionally refuse to run until the team fills and sources them.

## What it does now

- Select a Nigerian dish and compare its candidate preparation/ingredient options.
- Use a maximum ingredient-and-preparation cost per serving, a minimum estimated protein target, a maximum preparation time, a free-text preparation preference and exclusion of **recorded** allergen labels (not cross-contact certification).
- Compute option costs from purchased ingredient quantities and price per kg, plus recorded energy, labour and other costs.
- Estimate protein, iron and zinc from sourced ingredient composition *with explicit, simplified nutrient-retention assumptions*. Report amounts per finished serving; **do not infer protein gains simply from pressing or drying tofu**.
- Filter plant options against hard numeric constraints and explain exclusions. Beef stays a **comparison reference**, never a valid plant-based recommendation.
- Rank feasible options with a transparent weighted scoring formula and an experimental TF-IDF text-similarity component. Compare against cheapest-only baselines.
- Test sensitivity to **−20%, 0%, +20% ingredient price changes**.
- Fail clearly when no option satisfies the constraints, when data is incomplete, or when a plant recipe contains an animal ingredient.
- Provide a Streamlit decision studio with cost breakdowns, evidence register, scenario comparisons and a machine-readable command-line output.

**Not yet done:** credible local price collection, verified nutrient inputs, measured cooking yields, taste/texture evaluation, food-safety review, multi-dish recipes, and assessment showing statistical or practical value beyond a transparent rule-based baseline. The TF-IDF component is an *experimental NLP similarity signal*, not a taste model or validation of AI performance.

## Quick start (Python 3.11+)

```bash
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -e '.[dev]'
streamlit run app.py
```

The web UI opens with **Synthetic demonstration** mode. A verified mode exists but fails closed until Amina and team have supplied the required sourced data.

Run calculations without a browser:

```bash
menushift --dish suya --budget 1500 --protein 10 --sensitivity
pytest -q
ruff check src tests app.py
```

## Team workstreams

| Person | Scope | File locations |
|---|---|---|
| Ibrahim (`@Ibrahim-KIA`) | repository, data schema, serving-cost engine, beef comparison, cheapest baseline, sensitivity, tests | `src/menushift/`, `tests/`, `docs/` |
| Muhammad Inuwa (`@devinuwa`) | ranking/recommendation refinement, Streamlit experience, charts, explanations and experiments | `app.py`, `src/menushift/` |
| Amina | research framing, dated price ranges, nutrition figures, actual recipe and cost evidence, validation/limitations | `data/verified/`, `docs/RESEARCH_AND_VALIDATION.md` |

See [CONTRIBUTORS.md](CONTRIBUTORS.md), [TASKS.md](docs/TASKS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## Directory map

```text
app.py                    Streamlit demonstration
src/menushift/            Generic domain engine and CLI
data/demo/                SYNTHETIC illustrative test rows
data/verified/            Empty templates for sourced research
tests/                    Automated guardrails
.github/workflows/ci.yml  Tests and lint on push/PR
docs/                     Scope, methods, data, evidence and work plan
scripts/                  Repo publishing helper
```

## What the judges should see

1. A clearly defined restaurant decision and an unambiguous suya starting point.
2. A visibly **plant-only** recommendation, constrained by cost, nutrition and preparation.
3. A priced, sourced, explainable comparison with beef plus cheaper-only baselines.
4. At least one documented benchmark where structured ranking changes the outcome compared with choosing solely on cost; include failures/edge cases.
5. Honest data provenance, limitations and an expansion path to other dishes.

The [official participant guide](https://drive.google.com/drive/folders/18NG81Tng8uTgh-oHvWAYKd2WAKUS6GOr) should be checked against the final team work. Challenge 2 expects a demonstrable alternative to an existing menu item, **meaningful AI use**, evidence and a description of limitations. Confirm whether pre-event code construction is permitted before submitting this repository as hackathon work.

## Collaboration and GitHub workflow

The private repository was created by the owner and collaboration invitations have been sent. **Confirm acceptance and permissions inside GitHub; a CODEOWNERS line alone does not provide access.** Work through feature branches and pull requests, with CI tests before merging. Follow [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`docs/TEAM_HANDOFF.md`](docs/TEAM_HANDOFF.md).

### Design and agent workflow

- **Foundation:** data-driven domain engine; source-required research mode; safe synthetic presentation mode; price/protein/time/allergen constraints; beef reference; pricing scenarios and audit traces.
- **Experience:** Streamlit decision workspace with ranked results, evidence, scenarios, empty-state messaging and disclosures.
- **Automation:** SHA-pinned GitHub Actions quality gate, Python 3.11/3.12 matrix, Dependabot and repository CODEOWNERS.
- **Codex/agent use:** [`AGENTS.md`](AGENTS.md) + three targeted repository-local skills in `.agents/skills/`. See [`docs/TOOLING.md`](docs/TOOLING.md) for optional official Streamlit agent skills.
- **No unsupported AI claim:** TF-IDF preference matching is experimental; no taste or customer-acceptance model is trained or validated. Use [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md) to test evidence of benefit.

## Source of truth and related materials

- [Challenge 2 Research Brief (Google Doc)](https://docs.google.com/document/d/1J4o7CuT9_P1rRm1UE5uMUTkGoTejSHQPaN_ECUKUYME/edit)
- [Challenge 2 Meeting Presentation (Google Slides)](https://docs.google.com/presentation/d/1vdc8KmijvfRY0up1j2Ysf8Gq9DrPvyfiMyftqqGKqmg/edit)
- [Hack the Fork project Drive folder](https://drive.google.com/drive/folders/18NG81Tng8uTgh-oHvWAYKd2WAKUS6GOr)

Older presentation material lists five dishes as research candidates, not finished app features. Team WhatsApp discussions narrow the first technical pilot to four tofu preparations plus beef reference; that does **not** replace the broader product goal.
