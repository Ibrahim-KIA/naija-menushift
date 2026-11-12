"""Naija MenuShift decision workspace. Research only; synthetic data by default."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from menushift.engine import baselines, evaluate, load_dataset, sensitivity
from menushift.quality import audit_dataset

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Naija MenuShift · Research Studio", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

st.markdown(
    """
<style>
:root { --ink: #153428; --mint: #eaf5ee; --forest: #18664a; }
.block-container { max-width: 1320px; padding-top: 1.2rem; padding-bottom: 3rem; }
[data-testid="stAppViewContainer"] { background: #f6f8f6; }
[data-testid="stSidebar"] { background: #eaf2ed; }
h1,h2,h3 { letter-spacing: -.035em; color: var(--ink); }
h1 { font-size: clamp(2.1rem, 4vw, 3.5rem) !important; }
[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e0e9e3; border-radius: 17px; padding: 14px 18px; }
[data-testid="stMetricLabel"] { font-weight: 600; }
[data-testid="stAlert"] { border-radius: 14px; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 17px; }
.stButton button[kind="primary"] { background: #18664a; border-radius: 11px; }
</style>
""", unsafe_allow_html=True)

head_l, head_r = st.columns([5, 1.35], vertical_alignment="center")
with head_l:
    st.caption("HACK THE FORK NIGERIA 2026  /  CHALLENGE 02")
    st.title("Naija MenuShift 🌱")
    st.markdown("**Explore plant-based menu alternatives with transparent evidence and constraints.**")
with head_r:
    st.info("**RESEARCH PROTOTYPE**\n\nHuman review required")

st.warning("**DEMONSTRATION DATA:** All prices, nutrients, yields, energy costs, and rankings are fictional until sourced input data are supplied. These are not real food or purchasing recommendations.", icon="⚠️")

with st.sidebar:
    st.header("Decision settings")
    mode = st.radio("Data source", ["Synthetic demonstration", "Research data (requires evidence)"], index=0,
                    help="No fallback: missing or incomplete research files stop the app.")
    demo = mode == "Synthetic demonstration"
    folder = ROOT / "data" / ("demo" if demo else "verified")
    try:
        data = load_dataset(folder, demo=demo)
    except (ValueError, OSError) as exc:
        st.error(f"Research data unavailable: {exc}")
        st.info("Amina: complete all four data/verified/*.csv templates with dated sources and checked recipe quantities.")
        st.stop()
    available = {r["dish_id"]: r["name"] for r in data.dishes if any(o["dish_id"] == r["dish_id"] for o in data.options)}
    if not available:
        st.error("No dish has a complete set of candidate options yet.")
        st.stop()
    dish = st.selectbox("Existing menu item", list(available), format_func=lambda x: available[x])
    budget = st.number_input("Maximum total cost per serving (₦)", min_value=1.0, max_value=100000.0, value=1500.0, step=50.0)
    target = st.number_input("Minimum estimated protein (g)", min_value=0.0, max_value=150.0, value=10.0, step=1.0)
    prep = st.number_input("Maximum preparation time (minutes)", min_value=1.0, max_value=1440.0, value=120.0, step=5.0)
    preference = st.text_input("Preparation preference (experimental text matching)", value="chewy smoky grilled", max_chars=200,
                               help="A small text-retrieval signal, NOT a model of flavor or customer acceptance.")
    avoid = st.multiselect("Exclude declared allergens", ["soy", "peanut", "wheat", "milk", "egg", "sesame", "tree nut", "fish", "shellfish"],
                           help="Only recorded labels are filtered. This cannot establish cross-contact safety.")
    shock = st.slider("Ingredient price scenario", -20, 20, 0, step=5) / 100
    st.caption("The selection changes only purchased-ingredient costs, not energy or labour.")

try:
    outputs = evaluate(data, dish, budget_ngn=budget, protein_target_g=target, price_shock=shock,
                       max_prep_minutes=prep, preference=preference, avoid_allergens=avoid)
except (ValueError, RuntimeError) as exc:
    st.error(f"Unable to calculate a trustworthy recommendation: {exc}")
    st.stop()

base = baselines(outputs)
feasible = [r for r in outputs if r.feasible]
references = [r for r in outputs if not r.plant_only]

summary, evidence, stress, methodology = st.tabs(["🌿 Recommendations", "🔬 Ingredient evidence", "📉 Price resilience", "📘 How it works"])
with summary:
    if feasible:
        choice = feasible[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Best eligible option", choice.name)
        c2.metric("Full cost / serving", f"₦{choice.cost_ngn:,.0f}")
        c3.metric("Est. protein / serving", f"{choice.protein_g:.1f} g")
        c4.metric("Preparation", f"{choice.prep_minutes:.0f} min")
        st.success("This option satisfies the selected **numerical and declared-ingredient** constraints in the supplied dataset. It has not been taste-tested or food-safety certified.")
    else:
        st.error("**No valid plant option meets the chosen conditions.** Adjust a constraint or add better evidence. Beef will never be substituted into the plant-based results.")

    st.subheader("Decision comparison")
    frame = pd.DataFrame([{
        "Option": r.name, "Type": "Plant alternative" if r.plant_only else "Beef reference",
        "Total cost (₦)": r.cost_ngn, "Ingredients (₦)": r.ingredient_cost_ngn,
        "Processing (₦)": r.processing_cost_ngn, "Protein (g)": r.protein_g,
        "Iron (mg)": r.iron_mg, "Zinc (mg)": r.zinc_mg,
        "Finished serving (g)": r.finished_g, "Prep (min)": r.prep_minutes,
        "Eligible": "Yes" if r.feasible else "No", "Score": r.score,
    } for r in outputs])
    st.dataframe(frame, use_container_width=True, hide_index=True)
    st.caption("Finished serving weight is a research input, not a measured yield. Nutrient quantities are estimated from input ingredients and retention assumptions.")
    if not frame.empty:
        st.bar_chart(frame.set_index("Option")[["Total cost (₦)"]], color="#29946c")
    bc1, bc2 = st.columns(2)
    bc1.info(f"**Cheapest plant alternative (ignores constraints):** `{base['cheapest_plant_unconstrained'] or 'none'}`")
    bc2.info(f"**Cheapest feasible alternative:** `{base['cheapest_feasible_plant'] or 'none'}`")
    if references:
        st.caption("Beef is displayed solely as a comparison reference; it is never a plant-based recommendation.")

    st.subheader("Why the tool ranked each option")
    for r in outputs:
        prefix = "✅" if r.feasible else "○"
        with st.expander(f"{prefix} {r.name}  ·  ₦{r.cost_ngn:,.0f}  ·  {r.protein_g:.1f}g protein"):
            for reason in r.reasons:
                st.write("• " + reason)
            if r.score_breakdown:
                st.caption("Weighted score contributions (heuristic, not a learned effectiveness guarantee):")
                st.json(dict(r.score_breakdown), expanded=False)
            st.write(f"Recorded allergen labels: {', '.join(r.allergens) if r.allergens else 'Not recorded — do not assume safe'}")
            st.write("**Source trace**")
            for src in r.sources:
                st.caption(src)

with evidence:
    st.subheader("Evidence register")
    st.write("Every ingredient requires a region, price observation date, nutrition source, and food state.")
    ingredients = pd.DataFrame(data.ingredients)
    columns = [c for c in ["name", "price_ngn_per_kg", "price_date", "price_region", "price_source", "protein_g_per_100g", "iron_mg_per_100g", "zinc_mg_per_100g", "nutrition_source", "nutrition_state", "allergens"] if c in ingredients.columns]
    st.dataframe(ingredients[columns], use_container_width=True, hide_index=True)
    st.subheader("Dataset audit")
    issues = audit_dataset(data)
    st.dataframe(pd.DataFrame([issue.to_dict() for issue in issues]), use_container_width=True, hide_index=True)
    st.caption("Checks flag missing allergen review, stale prices and unvalidated sensory assumptions. They do not constitute a scientific or regulatory assessment.")

with stress:
    st.subheader("±20% ingredient price sensitivity")
    st.write("A scenario analysis, not a forecast. The displayed recommendation can change when ingredient costs change.")
    scenarios = sensitivity(data, dish, budget_ngn=budget, protein_target_g=target, max_prep_minutes=prep,
                            preference=preference, avoid_allergens=avoid)
    records = [{"Scenario": label, "Option": r.name, "Cost (₦)": r.cost_ngn,
                "Eligible": "Yes" if r.feasible else "No", "Rank score": r.score}
               for label, collection in scenarios.items() for r in collection]
    st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)
    st.caption("This varies **all** ingredient prices together. Future research can test ingredient-specific risk and quote ranges.")

with methodology:
    st.subheader("Methods & safeguards")
    st.markdown("""
**1. Structured data:** A dish maps to alternative formulations; each formulation lists purchased ingredient weights, sources, nutrient assumptions, processing cost, time, and finished weight.

**2. Hard filters:** Plant-only eligibility, total price budget, minimum estimated protein, preparation time, and recorded allergens.

**3. Explanation:** Feasible options receive a provisional weighted score for cost margin (45%), protein target (25%), prep time (15%), and experimental TF-IDF preference matching (15%). This is **not** a learned or clinically validated food suitability model.

**4. Baseline:** Compare the ranked selection against cheapest-only choices. An improvement claim requires actual benchmark cases and independent testing.

**5. Research obligations:** Verify ingredient food states, prices, serving quantities, retention, cooking yield, peanut/soy/wheat safety, and food acceptance with qualified human reviewers.

**6. Expansion:** Add dish, option, and ingredient rows; the calculation engine has no suya-specific branch. Future model upgrades should be evaluated offline before use.
""")
    st.caption("No personal information is collected or sent by this demo. It runs calculations against local CSV files.")

st.divider()
st.caption("Naija MenuShift · Built as a research demonstration for Hack the Fork Nigeria 2026 · Not a food safety, nutrition, purchasing, or dietary advice service")
