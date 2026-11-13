"""Naija MenuShift decision workspace. Research only; synthetic data by default."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from menushift.engine import baselines, compare_rankers, evaluate, load_dataset, sensitivity
from menushift.quality import audit_dataset
from menushift.scenarios import SYNTHETIC_SCENARIOS
from menushift.sources import collected_quote_gaps, load_market_prices, load_nutrition_quotes

ROOT = Path(__file__).resolve().parent
ALLERGEN_CHOICES = ["soy", "peanut", "wheat", "milk", "egg", "sesame", "tree nut", "fish", "shellfish"]

st.set_page_config(
    page_title="Naija MenuShift · Research Studio",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
:root { --ink: #153428; }
.block-container { max-width: 1100px; padding-top: 1.2rem; padding-bottom: 3rem; }
[data-testid="stAppViewContainer"] { background: #f6f8f6; }
[data-testid="stSidebar"] { background: #eaf2ed; }
h1,h2,h3 { letter-spacing: -.035em; color: var(--ink); }
h1 { font-size: clamp(1.8rem, 4vw, 3rem) !important; }
[data-testid="stMetric"] { background: #ffffff; border: 1px solid #d5e3da; border-radius: 17px; padding: 14px 18px; }
[data-testid="stMetricLabel"] { font-weight: 600; }
[data-testid="stAlert"] { border-radius: 14px; }
</style>
""",
    unsafe_allow_html=True,
)

st.caption("HACK THE FORK NIGERIA 2026  /  CHALLENGE 02")
st.title("Naija MenuShift")
st.write("Explore plant-based menu alternatives with transparent evidence and constraints.")
st.info("Research prototype. A person still has to review any menu change.")


def _apply_scenario(scenario) -> None:
    st.session_state.budget = float(scenario.budget_ngn)
    st.session_state.protein = float(scenario.protein_target_g)
    st.session_state.prep = float(scenario.max_prep_minutes)
    st.session_state.preference = scenario.preference
    st.session_state.avoid = list(scenario.avoid_allergens)


def _settings_ready() -> bool:
    return all(key in st.session_state for key in ("budget", "protein", "prep", "preference", "avoid"))


def _option_label(option_id: str | None, names: dict[str, str]) -> str:
    if not option_id:
        return "none (abstained)"
    return f"{names.get(option_id, option_id)} [{option_id}]"


load_error: Exception | None = None
data = None
with st.sidebar:
    st.header("Decision settings")
    mode = st.radio(
        "Data source",
        ["Synthetic demonstration", "Research data (requires evidence)"],
        index=0,
        help="Missing or incomplete research files stop the app. Demonstration numbers are never substituted.",
    )
    demo = mode == "Synthetic demonstration"
    folder = ROOT / "data" / ("demo" if demo else "verified")
    try:
        data = load_dataset(folder, demo=demo)
    except (ValueError, OSError) as exc:
        load_error = exc
    if data is not None:
        available = {
            row["dish_id"]: row["name"]
            for row in data.dishes
            if any(option["dish_id"] == row["dish_id"] for option in data.options)
        }
        if not available:
            load_error = ValueError("No dish has a complete set of candidate options yet.")
            data = None
    # Keep these widgets mounted in both modes. If they disappear, Streamlit recreates them at the minimum.
    if not _settings_ready():
        _apply_scenario(SYNTHETIC_SCENARIOS[0])
    if data is not None and demo:
        st.subheader("Reproducible cases")
        st.caption("Synthetic presets. The naira amounts are fictional.")
        for scenario in SYNTHETIC_SCENARIOS:
            if st.button(scenario.label, key=f"preset-{scenario.scenario_id}", use_container_width=True):
                _apply_scenario(scenario)
                st.rerun()
    recorded = set()
    if data is not None:
        recorded = {
            token.strip().lower()
            for ingredient in data.ingredients
            for token in ingredient.get("allergens", "").split(";")
            if token.strip()
        }
    allergen_options = sorted(recorded | set(ALLERGEN_CHOICES))
    if data is not None:
        dish = st.selectbox("Existing menu item", list(available), format_func=lambda item: available[item])
    budget = st.number_input(
        "Maximum total cost per serving (naira)",
        min_value=1.0,
        max_value=100000.0,
        step=50.0,
        key="budget",
    )
    target = st.number_input(
        "Minimum estimated protein (g)",
        min_value=0.0,
        max_value=150.0,
        step=1.0,
        key="protein",
    )
    prep = st.number_input(
        "Maximum preparation time (minutes)",
        min_value=1.0,
        max_value=1440.0,
        step=5.0,
        key="prep",
    )
    preference = st.text_input(
        "Preparation preference (experimental text matching)",
        max_chars=200,
        key="preference",
        help="Compared with keyword overlap and TF-IDF. Neither score is a flavour or acceptance model.",
    )
    avoid = st.multiselect(
        "Exclude declared allergens",
        allergen_options,
        key="avoid",
        help="Only recorded labels are filtered. This cannot establish cross-contact safety.",
    )
    shock = st.slider("Ingredient price scenario", -20, 20, 0, step=5) / 100
    st.caption("The slider changes purchased-ingredient cost only. It is a scenario, not a forecast.")

if load_error is not None or data is None:
    st.error(f"Research data unavailable: {load_error}")
    st.info(
        "Research mode needs all four data/verified CSV files, with dates, regions, nutrients, "
        "and per-serving recipe weights. Demonstration data is not copied in to fill the gap."
    )
    st.subheader("Collected quotes do not close that gap")
    for gap in collected_quote_gaps():
        st.write("- " + gap)
    st.stop()

if data.demo:
    st.warning(
        "Demonstration data: prices, nutrients, yields, energy costs, and rankings on this screen "
        "are fictional. They are not Nigerian market prices or restaurant recommendations.",
        icon="⚠️",
    )
else:
    st.warning(
        "Research files are loaded. Check every source, date, food state, and serving weight. "
        "A completed file is not a food-safety or nutrition certification.",
    )

try:
    outputs = evaluate(
        data,
        dish,
        budget_ngn=budget,
        protein_target_g=target,
        price_shock=shock,
        max_prep_minutes=prep,
        preference=preference,
        avoid_allergens=avoid,
    )
    comparison = compare_rankers(
        data,
        dish,
        budget_ngn=budget,
        protein_target_g=target,
        price_shock=shock,
        max_prep_minutes=prep,
        preference=preference,
        avoid_allergens=avoid,
    )
except (ValueError, RuntimeError) as exc:
    st.error(f"Unable to calculate a trustworthy recommendation: {exc}")
    st.stop()

base = baselines(outputs)
feasible = [row for row in outputs if row.feasible]
references = [row for row in outputs if not row.plant_only]
names = {row.option_id: row.name for row in outputs}
active = next(
    (
        scenario
        for scenario in SYNTHETIC_SCENARIOS
        if data.demo
        and scenario.budget_ngn == budget
        and scenario.protein_target_g == target
        and scenario.max_prep_minutes == prep
        and scenario.preference == preference
        and set(scenario.avoid_allergens) == set(avoid)
        and shock == 0
    ),
    None,
)

summary, evidence, stress, methodology = st.tabs(
    ["Recommendations", "Ingredient evidence", "Price resilience", "How it works"]
)
with summary:
    if active is not None:
        st.caption(active.note)
    if feasible:
        choice = feasible[0]
        top_l, top_r = st.columns(2)
        top_l.metric("Eligible plant option (TF-IDF hybrid)", choice.name)
        top_r.metric("Status", "Eligible")
        cost_l, cost_r = st.columns(2)
        cost_l.metric("Ingredients / serving", f"{choice.ingredient_cost_ngn:,.0f} naira")
        cost_r.metric("Processing / serving", f"{choice.processing_cost_ngn:,.0f} naira")
        nut_l, nut_r = st.columns(2)
        nut_l.metric("Estimated protein / serving", f"{choice.protein_g:.1f} g")
        nut_r.metric("Preparation", f"{choice.prep_minutes:.0f} min")
        st.success(
            "This option passes the selected budget, estimated protein, preparation time, "
            "and declared-allergen checks in the loaded file. It has not been taste-tested "
            "or food-safety certified."
        )
        st.caption(f"Full serving cost: {choice.cost_ngn:,.0f} naira (ingredients plus processing).")
        if not choice.allergen_review_complete:
            st.warning(
                "Some ingredient allergen labels have not been reviewed. The option may meet numeric constraints, "
                "but it is not cleared for dietary restrictions or food service."
            )
    else:
        st.error(
            "No plant option meets the chosen conditions. Adjust a constraint or add sourced "
            "recipe weights. Beef is not moved into the plant results."
        )
        st.caption("Status: no feasible plant option.")

    if references:
        st.subheader("Beef reference")
        st.caption("Comparison only. This row is excluded from every plant ranking.")
        beef = references[0]
        beef_l, beef_r = st.columns(2)
        beef_l.metric("Reference cost / serving", f"{beef.cost_ngn:,.0f} naira")
        beef_r.metric("Reference estimated protein / serving", f"{beef.protein_g:.1f} g")
        st.write(f"Reference name: {beef.name}. Status: Excluded from plant recommendations.")

    st.subheader("Ranker comparison")
    st.write("Cheapest plant, constraints ignored: " + _option_label(comparison["cheapest_plant_unconstrained"], names))
    st.write("Cheapest feasible plant: " + _option_label(comparison["cheapest_feasible_plant"], names))
    st.write("Keyword hybrid: " + _option_label(comparison["keyword_hybrid"], names))
    st.write("TF-IDF hybrid: " + _option_label(comparison["tfidf_hybrid"], names))
    if comparison["abstained"]:
        st.error("Every ranker abstains. No plant option is eligible, so there is no recommendation.")
    elif comparison["methods_disagree"]:
        st.warning(
            "Keyword overlap and TF-IDF name different options. That is a score difference "
            "on this dataset, not evidence that one option tastes better."
        )
    elif comparison["text_changes_winner"]:
        st.info(
            "Both text methods name a different option than the cheapest feasible serving. "
            "The weights are provisional and were not fitted on restaurant reviews."
        )
    else:
        st.info("The text methods agree with the cheapest feasible option. The text term did not change the decision.")
    st.caption(
        f"Cheapest plant ignoring constraints: {base['cheapest_plant_unconstrained'] or 'none'}. "
        f"Cheapest feasible: {base['cheapest_feasible_plant'] or 'none'}."
    )

    st.subheader("Decision comparison")
    frame = pd.DataFrame(
        [
            {
                "Option": row.name,
                "Type": "Plant alternative" if row.plant_only else "Beef reference",
                "Ingredients (naira)": row.ingredient_cost_ngn,
                "Processing (naira)": row.processing_cost_ngn,
                "Total cost (naira)": row.cost_ngn,
                "Protein (g)": row.protein_g,
                "Iron (mg)": row.iron_mg,
                "Zinc (mg)": row.zinc_mg,
                "Finished serving (g)": row.finished_g,
                "Prep (min)": row.prep_minutes,
                "Status": "Eligible" if row.feasible else "Excluded",
                "Score": row.score,
            }
            for row in outputs
        ]
    )
    st.dataframe(frame, use_container_width=True, hide_index=True)
    st.caption(
        "Finished serving weight is an input, not a measured yield. "
        "Nutrient totals use purchase weight and a single retention fraction. "
        "Pressing or drying does not create protein."
    )
    if not frame.empty:
        chart_l, chart_r = st.columns(2)
        with chart_l:
            st.caption("Cost split per serving")
            st.bar_chart(frame.set_index("Option")[["Ingredients (naira)", "Processing (naira)"]])
        with chart_r:
            st.caption("Estimated protein per serving (g)")
            st.bar_chart(frame.set_index("Option")[["Protein (g)"]])

    st.subheader("Why each option is eligible or excluded")
    for row in outputs:
        status = "Eligible" if row.feasible else "Excluded"
        with st.expander(f"{status}: {row.name} · {row.cost_ngn:,.0f} naira · {row.protein_g:.1f} g protein"):
            for reason in row.reasons:
                st.write("- " + reason)
            if row.score_breakdown:
                st.caption("Weighted score parts for the TF-IDF hybrid. This is a heuristic, not a learned guarantee.")
                st.json(dict(row.score_breakdown), expanded=False)
            allergen_text = ", ".join(row.allergens) if row.allergens else "Not recorded. Do not assume this is safe."
            st.write("Recorded allergen labels: " + allergen_text)
            st.caption(
                "Allergen label review: "
                + ("Recorded (not cross-contact certified)" if row.allergen_review_complete else "Incomplete")
            )
            st.write("Source trace")
            for src in row.sources:
                st.caption(src)

with evidence:
    st.subheader("Evidence register")
    st.write("Every ingredient used in a calculation needs a region, price date, nutrition source, and food state.")
    ingredients = pd.DataFrame(data.ingredients)
    columns = [
        column
        for column in [
            "name",
            "price_ngn_per_kg",
            "price_date",
            "price_region",
            "price_source",
            "protein_g_per_100g",
            "iron_mg_per_100g",
            "zinc_mg_per_100g",
            "nutrition_source",
            "nutrition_state",
            "allergens",
        ]
        if column in ingredients.columns
    ]
    st.dataframe(ingredients[columns], use_container_width=True, hide_index=True)
    st.subheader("Dataset audit")
    issues = audit_dataset(data)
    st.dataframe(pd.DataFrame([issue.to_dict() for issue in issues]), use_container_width=True, hide_index=True)
    st.caption("Checks flag missing allergen review, stale prices, and unvalidated texture notes. They are not a regulatory assessment.")

    st.subheader("Collected market and nutrition quotes")
    st.write(
        "These tables are a local copy of the team workbook. They are not the rows used to rank "
        "demonstration options, and they do not open research mode."
    )
    try:
        prices = load_market_prices(ROOT / "data" / "sources")
        nutrients = load_nutrition_quotes(ROOT / "data" / "sources")
    except (OSError, ValueError) as exc:
        st.error(f"Collected quotes could not be read: {exc}")
    else:
        st.dataframe(pd.DataFrame(prices), use_container_width=True, hide_index=True)
        st.dataframe(pd.DataFrame(nutrients), use_container_width=True, hide_index=True)
    st.subheader("Gaps that keep research mode closed")
    for gap in collected_quote_gaps():
        st.write("- " + gap)

with stress:
    st.subheader("Ingredient price scenarios: minus 20%, base, plus 20%")
    st.write("A scenario check, not a forecast. The eligible option can change when ingredient costs change.")
    scenarios = sensitivity(
        data,
        dish,
        budget_ngn=budget,
        protein_target_g=target,
        max_prep_minutes=prep,
        preference=preference,
        avoid_allergens=avoid,
    )
    records = [
        {
            "Scenario": label,
            "Option": row.name,
            "Cost (naira)": row.cost_ngn,
            "Status": "Eligible" if row.feasible else "Excluded",
            "Rank score": row.score,
        }
        for label, collection in scenarios.items()
        for row in collection
    ]
    st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
    st.caption("All ingredient prices move together. Energy and labour stay fixed. This is not an ingredient-specific risk model.")

with methodology:
    st.subheader("Methods and safeguards")
    st.write("1. A dish has candidate formulations. Each formulation lists purchased ingredient weights, sources, a retention assumption, processing cost, time, and finished weight.")
    st.write("2. Hard filters run first: plant-only, total budget, minimum estimated protein, preparation time, and recorded allergens. If an allergen exclusion is selected, unknown labels make that option ineligible. Beef never becomes eligible.")
    st.write("3. Eligible options receive a provisional score: 45% cost margin, 25% diminishing-returns protein utility, 15% preparation time, and 15% text match. The minimum protein target is still a hard filter; the protein utility is a preference, not nutritional adequacy. The text term uses keyword overlap or experimental TF-IDF.")
    st.write("4. The same constraints are scored both ways and compared with the cheapest plant option and the cheapest feasible plant option. A difference is a score difference, not a taste result.")
    st.write("5. On the frozen synthetic cases, 'chewy smoky grilled' leads both text methods to pressed tofu instead of cheaper plain tofu. 'crispy fried' leads the keyword method to fried tofu, while TF-IDF still picks plain tofu. Weights were not changed to hide that disagreement.")
    st.write("6. Research mode stays closed until dated prices, food states, serving weights, and allergen review are entered. Moisture-adjusted nutrient notes are not treated as protein created by pressing.")
    st.caption("This demo does not collect personal information. Calculations use local CSV files.")

st.divider()
st.caption(
    "Naija MenuShift · Research demonstration for Hack the Fork Nigeria 2026 · "
    "Not a food safety, nutrition, purchasing, or dietary advice service"
)
