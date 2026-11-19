"""Premium restaurant-first, source-aware Kitchen Intelligence experience."""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from menushift.kitchen_optimizer import INVENTORY_ITEMS, explore
from menushift.recipe_trial import build_trial

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "data" / "sources"

st.set_page_config(
    page_title="Kitchen Intelligence | Naija MenuShift",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
:root{--forest:#173b2d;--forest-deep:#102c22;--cream:#fbfaf5;--gold:#bc8948;--line:#d8e2d9;}
[data-testid="stAppViewContainer"] {background:var(--cream);color:#183329;}
[data-testid="stHeader"]{background:rgba(251,250,245,.94);}
.block-container{max-width:1180px;padding-top:1rem;padding-bottom:4rem;}
.stMarkdown h1,.stMarkdown h2,.stMarkdown h3{color:var(--forest);letter-spacing:-.03em;}
[data-testid="stMetric"] {background:white;border:1px solid var(--line);border-radius:16px;padding:18px;}
[data-testid="stMetricLabel"] p{font-weight:650;}
[data-testid="stAlert"]{border-radius:14px;}
[data-testid="stForm"]{background:#fff;border:1px solid var(--line);border-radius:20px;padding:20px;}
div.stButton>button[kind="primary"],div.stFormSubmitButton>button[kind="primary"]{
  background:#1b5940;color:white;border:1px solid #1b5940;border-radius:11px;font-weight:650;
}
div.stButton>button[kind="primary"]:hover,div.stFormSubmitButton>button[kind="primary"]:hover{
  background:#143f2f;color:white;border-color:#143f2f;
}
button:focus-visible,input:focus-visible,[role="tab"]:focus-visible{
  outline:3px solid #c18a40!important;outline-offset:2px!important;
}
.ms-hero{
  background:radial-gradient(circle at 84% 20%,#34644a 0%,transparent 34%),
             linear-gradient(125deg,#102d23 0%,#24533d 100%);
  color:#fff;padding:40px 44px;border-radius:23px;margin:4px 0 22px;
  box-shadow:0 16px 30px rgba(16,45,35,.10);
}
.ms-eyebrow{font-size:.8rem;letter-spacing:.15em;text-transform:uppercase;color:#e2bd7b;font-weight:750}
.ms-hero h1{font-size:clamp(2rem,5vw,3.7rem);line-height:1.05;color:#fff!important;margin:14px 0;}
.ms-hero p{color:#e0eee5;max-width:750px;font-size:1.07rem;line-height:1.62;}
.ms-hero-tags{display:flex;gap:8px;flex-wrap:wrap;margin-top:18px}
.ms-hero-tags span{padding:6px 12px;border:1px solid #70947d;border-radius:999px;font-size:.82rem;color:#f0eadc}
.ms-steps{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0 20px}
.ms-steps span{background:#e7ede6;padding:9px 13px;border-radius:9px;color:#274436;font-size:.88rem;font-weight:600}
.ms-section{font-size:.8rem;letter-spacing:.1em;font-weight:800;color:#517a60;text-transform:uppercase;margin:18px 0 8px}
.ms-warning{padding:12px 16px;background:#fff3da;border-left:4px solid #af7930;border-radius:8px;color:#684817;margin:14px 0}
.ms-card-intro{color:#557366;font-size:.86rem;font-weight:650;letter-spacing:.06em;text-transform:uppercase;}
.ms-card-name{font-size:1.25rem;font-weight:800;color:#183a2a;line-height:1.25;margin-top:6px;}
.ms-research{color:#50665a;font-size:.87rem}
@media(max-width:640px){
 .ms-hero{padding:24px 22px;border-radius:18px;}
 .ms-steps span{font-size:.78rem;padding:7px 9px;}
 .block-container{padding-left:1rem;padding-right:1rem}
 [data-testid="stForm"]{padding:12px}
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<section class="ms-hero" aria-label="Kitchen Intelligence Studio introduction">
  <div class="ms-eyebrow">Naija MenuShift · Hack the Fork Nigeria · Challenge 2</div>
  <h1>Better food ideas.<br>Real kitchen decisions.</h1>
  <p>Explore plant-based formulations for familiar Nigerian meals with clear
  ingredient estimates, budget checks, practical equipment constraints and
  honest evidence trails.</p>
  <div class="ms-hero-tags"><span>Recipe exploration</span>
  <span>Cost & protein trade-offs</span><span>Source transparency</span></div>
</section>
<div class="ms-steps" aria-label="Four-step workflow">
<span>01 · Choose a dish</span><span>02 · Set the brief</span>
<span>03 · Explore options</span><span>04 · Understand why</span>
</div>
""",
    unsafe_allow_html=True,
)

st.warning(
    "Research prototype: ingredient prices and published nutrient references are sourced, "
    "but cooked-serving yields, coagulant, labour, energy, oil retention, taste and safety "
    "are NOT yet verified. Listed costs are incomplete and not commercial serving prices.",
    icon="⚠️",
)

st.markdown('<div class="ms-section">01 · Restaurant brief</div>', unsafe_allow_html=True)
st.subheader("What would you like to reinvent?")
st.selectbox(
    "Existing menu dish",
    ["suya"],
    format_func=lambda _: "Nigerian suya — plant-based adaptation",
    help="Suya is the evaluated pilot. Other Nigerian dishes require additional recipe evidence.",
)
st.caption("Starting with one properly tested dish. More meals can be added through the existing recipe schema.")

with st.container(border=True):
    st.markdown("### 02 · Your constraints")
    st.caption("Live simulation — results update when you change a requirement. All price and time feasibility is provisional.")
    b, p, t = st.columns(3)
    budget = b.number_input(
        "Maximum budget for listed costs (₦)",
        min_value=1.0, max_value=100000.0, value=750.0, step=50.0,
    )
    protein = p.number_input(
        "Minimum estimated protein (g)",
        min_value=0.0, max_value=150.0, value=12.0, step=1.0,
    )
    max_time = t.number_input(
        "Maximum preparation time (minutes)",
        min_value=1.0, max_value=1440.0, value=120.0, step=5.0,
    )
    preference = st.text_input(
        "What matters about the dish?",
        placeholder="For example: chewy and smoky, soft and mild, crisp exterior",
        max_chars=200,
        help="Experimental text similarity — no validated prediction of taste.",
    )
    labels = {
        "grill": "Grill / charcoal setup",
        "press": "Press or weights",
        "freezer": "Freezer",
        "frying_pan": "Frying pan & heat source",
    }
    equipment = st.multiselect(
        "What equipment is available?",
        list(labels),
        default=["grill", "press", "frying_pan"],
        format_func=lambda code: labels[code],
        help="Options needing absent equipment are not recommended.",
    )
    stock = st.multiselect(
        "Which ingredients do you currently have?",
        options=list(INVENTORY_ITEMS),
        default=list(INVENTORY_ITEMS),
        format_func=lambda key: INVENTORY_ITEMS[key],
        help="Reported stock is a hard constraint. Selecting an item does not verify its label or supplier.",
    )
    with st.expander("Advanced assumptions, allergens and scenarios"):
        size_min, size_max = st.select_slider(
            "Illustrative finished serving sizes (grams)",
            options=list(range(60, 221, 20)), value=(80, 200),
        )
        avoid = st.multiselect(
            "Exclude these declared allergens",
            ["soy", "peanut", "wheat", "sesame", "milk", "egg", "tree nut", "fish", "shellfish"],
            help="Unknown ingredient labels cause exclusion, not a claim of allergen safety.",
        )
        st.caption("Optional, unmeasured seasoning amounts for a trial only; no validated yaji recipe exists.")
        season_a, season_b = st.columns(2)
        onion_g = season_a.number_input(
            "Onions (purchased g; assumption)", min_value=0.0, max_value=100.0, value=0.0, step=1.0,
        )
        pepper_g = season_b.number_input(
            "Pepper (purchased g; assumption)", min_value=0.0, max_value=100.0, value=0.0, step=1.0,
        )
        season_c, season_d = st.columns(2)
        salt_g = season_c.number_input(
            "Salt (purchased g; assumption)", min_value=0.0, max_value=20.0, value=0.0, step=0.5,
        )
        seasoning_g = season_d.number_input(
            "Seasoning cube (purchased g; unreviewed label)",
            min_value=0.0, max_value=20.0, value=0.0, step=1.0,
        )
        oil_cl = st.number_input(
            "Oil for fried method (centilitres, assumption)",
            min_value=0.0, max_value=30.0, value=1.0, step=0.5,
        )
        shock = st.slider("Ingredient-price scenario (%)", -20, 20, 0, step=5)
        yield_ratio = st.slider(
            "Wet curd per kg dry soy (research assumption, kg)",
            1.5, 2.0, 1.75, 0.05,
        )
        st.caption(
            "Default method times are illustrative, from the synthetic research template. "
            "They must be replaced with actual timed batches before claiming kitchen practicality."
        )
        a, c, d, e = st.columns(4)
        firm_t = a.number_input("Firm minutes (assumed)", min_value=1, max_value=600, value=35)
        pressed_t = c.number_input("Pressed minutes (assumed)", min_value=1, max_value=600, value=48)
        frozen_t = d.number_input("Freeze/thaw minutes (assumed)", min_value=1, max_value=1440, value=110)
        fried_t = e.number_input("Fried minutes (assumed)", min_value=1, max_value=600, value=65)

# Streamlit controls are rerunnable; one bounded, deterministic analysis per brief.
try:
    search = explore(
        SOURCES,
        budget_ngn=budget,
        protein_target_g=protein,
        max_prep_minutes=max_time,
        equipment=frozenset(equipment),
        available_ingredients=frozenset(stock),
        onion_g=onion_g, pepper_g=pepper_g, salt_g=salt_g, seasoning_g=seasoning_g,
        portions_g=tuple(range(int(size_min), int(size_max) + 1, 20)),
        preference=preference,
        avoid_allergens=tuple(avoid),
        wet_yield_kg_per_kg_dry=yield_ratio,
        oil_cl=oil_cl,
        price_shock=shock / 100,
        prep_minutes={"firm": firm_t, "pressed": pressed_t,
                      "frozen": frozen_t, "fried": fried_t},
    )
except (ValueError, OSError, RuntimeError) as exc:
    st.error(f"Cannot calculate this scenario: {exc}")
    st.stop()

st.markdown('<div class="ms-section">03 · Formulation exploration</div>', unsafe_allow_html=True)
st.subheader("Find a formulation that fits your kitchen")
a, b, c = st.columns(3)
a.metric("Candidates evaluated", f"{search.inspected}")
b.metric("Within hard limits", f"{len(search.eligible)}")
c.metric("Pareto alternatives", f"{len(search.frontier)}")
if search.skipped_equipment:
    st.caption(f"{search.skipped_equipment} configurations excluded for unavailable equipment.")
if search.skipped_ingredients:
    st.caption(f"{search.skipped_ingredients} configurations excluded for unavailable ingredients.")
if search.skipped_unverified_yaji:
    st.warning(
        "Peanut exclusion selected: traditional suya yaji often contains groundnut, "
        "and a reviewed peanut-free yaji formulation is not yet in this dataset. "
        "No suya-style recommendation can be certified for this restriction."
    )
st.caption(
    "Eligibility is against *listed* costs, approximate nutrients and assumed durations; "
    "it does not guarantee affordability when unmeasured overheads are added."
)

if not search.eligible:
    st.error("No plant-based formulation meets all of your requirements.")
    st.write(
        "Try increasing the budget or time, adjusting the protein target, or supplying "
        "the required equipment. Dietary exclusions cannot be bypassed."
    )
    st.info("We don't invent a recommendation when your constraints cannot be satisfied.")
else:
    cards = (
        ("Budget-first", "budget", "Lowest modelled ingredient/known cost within your limits"),
        ("Protein-first", "protein", "Highest source-referenced estimated protein within limits"),
        ("Kitchen-first", "kitchen", "Shortest assumed preparation within your limits"),
    )
    cols = st.columns(3)
    for col, (heading, objective, description) in zip(cols, cards):
        candidate = search.best(objective)
        if candidate is None:
            continue
        with col, st.container(border=True):
            st.markdown(f'<div class="ms-card-intro">{heading}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="ms-card-name">{candidate.method}</div>',
                unsafe_allow_html=True,
            )
            st.caption(description)
            st.metric("Listed cost (incomplete)", f"₦{candidate.evaluation.cost_ngn:,.0f}")
            st.write(
                f"**{candidate.portion_g:.0f} g** finished assumption · "
                f"**{candidate.evaluation.protein_g:.1f} g** estimated protein"
            )
            st.caption("Unvalidated serving and preparation assumptions")

    st.markdown('<div class="ms-section">04 · Understand the recommendation</div>', unsafe_allow_html=True)
    st.subheader("Inspect a formulation")
    indexed = {c.identifier: c for c in search.eligible}
    chosen_id = st.selectbox(
        "Choose a feasible formulation to inspect",
        list(indexed),
        format_func=lambda k: (
            f"{indexed[k].method} · {indexed[k].portion_g:.0f} g · "
            f"₦{indexed[k].evaluation.cost_ngn:,.0f}"
        ),
        index=list(indexed).index(search.best("balanced").identifier),
    )
    selected = indexed[chosen_id]
    info, recipe = st.columns([1, 1], gap="large")
    with info:
        st.markdown("#### Why this candidate is eligible")
        st.write(
            f"Estimated ingredients: ₦{selected.evaluation.ingredient_cost_ngn:,.0f} · "
            f"Other listed preparation: ₦{selected.evaluation.processing_cost_ngn:,.0f}"
        )
        st.write(
            f"Estimated protein: {selected.evaluation.protein_g:.1f} g · "
            f"Assumed preparation time: {selected.evaluation.prep_minutes:.0f} minutes"
        )
        st.write("Required equipment:", ", ".join(labels[x] for x in sorted(selected.required_equipment)))
        for reason in selected.evaluation.reasons:
            st.write("• " + reason)
        if not selected.evaluation.allergen_review_complete:
            st.warning(
                "At least one ingredient label has not been reviewed. This is NOT "
                "certified allergen-safe or ready to serve."
            )
        st.caption(
            "A score or calculated feasibility does not establish flavour, texture, "
            "nutritional equivalence, ingredient safety or restaurant approval."
        )
    with recipe:
        st.markdown("#### Ingredient and quantity worksheet")
        st.caption("The model currently has NO verified complete suya seasoning/yaji formula.")
        st.dataframe(
            pd.DataFrame([
                {
                    "Ingredient": line.name,
                    "Purchased grams (estimated)": line.purchase_g,
                    "Listed cost (₦)": line.estimated_cost_ngn,
                    "Estimated protein (g)": line.estimated_protein_g,
                    "Declared label": line.allergen_labels or "Unreviewed",
                }
                for line in selected.ingredient_lines
            ]),
            hide_index=True, width="stretch",
        )
        st.caption(
            "Quantities are model assumptions. They are not tested recipes or final "
            "purchase instructions. Energy and labour are not yet measured."
        )
        with st.expander("Show price sources and food-state limitations"):
            for line in selected.ingredient_lines:
                st.write(f"**{line.name}** — {line.source}")
            st.caption(
                "Published nutrient references may not represent local awara or the "
                "exact finished food state; production yields are unmeasured."
            )
        trial = build_trial(selected)
        st.markdown("#### " + trial.cookbook_title)
        st.caption(
            "Cookbook-style research recipe • 1 assumed serving • "
            f"{selected.evaluation.prep_minutes:.0f} min unmeasured • soy allergen"
        )
        st.markdown("**Ingredients**")
        for ingredient in selected.ingredient_lines:
            st.markdown(f"- {ingredient.purchase_g:.1f} g {ingredient.name}")
        if selected.oil_cl:
            st.markdown(
                f"- {selected.oil_cl:g} cl vegetable oil allowance (retention unmeasured)"
            )
        st.warning(
            "Complete reviewed suya yaji is not in this dataset. "
            "This is a kitchen trial, not a ready-to-serve recipe."
        )
        st.markdown("**Step-by-step trial method**")
        for i, step in enumerate(trial.steps, 1):
            st.markdown(f"**{i}. {step.heading}.** {step.instruction}")
        st.download_button(
            "Download source-traceable kitchen trial worksheet",
            data=trial.to_markdown(selected),
            file_name="naija-menushift-kitchen-trial.md",
            mime="text/markdown",
            use_container_width=True,
        )
        with st.expander("What must be measured before serving?"):
            for gap in trial.evidence_gaps:
                st.write("- " + gap)
    st.subheader("Trade-offs across eligible formulations")
    chart = pd.DataFrame([
        {
            "Recipe": f"{c.method} · {c.portion_g:.0f}g",
            "Cost (₦)": c.evaluation.cost_ngn,
            "Estimated protein (g)": c.evaluation.protein_g,
            "Time (min, assumed)": c.evaluation.prep_minutes,
        }
        for c in search.eligible
    ])
    st.scatter_chart(chart, x="Cost (₦)", y="Estimated protein (g)")
    with st.expander("Inspect Pareto-efficient options and method benchmark"):
        st.caption(
            "Pareto-efficient means no other eligible candidate has lower/equal "
            "cost and time plus greater/equal protein, with at least one improvement."
        )
        st.dataframe(
            pd.DataFrame([
                {
                    "Alternative": c.method,
                    "Portion (g)": c.portion_g,
                    "Estimated cost (₦)": c.evaluation.cost_ngn,
                    "Estimated protein (g)": c.evaluation.protein_g,
                    "Assumed prep (min)": c.evaluation.prep_minutes,
                }
                for c in search.frontier
            ]),
            hide_index=True, width="stretch",
        )
        cheap = search.best("budget")
        balanced = search.best("balanced")
        st.write("Cheapest feasible baseline:", cheap.identifier)
        st.write("Balanced experimental ranking:", balanced.identifier)
        st.caption(
            "Any difference here is not proof of superiority. Independent kitchen "
            "review and out-of-sample benchmark scenarios remain necessary."
        )

with st.expander("What this system can and cannot conclude"):
    st.markdown(
        """
**What is calculated:** ingredient-priced alternatives, portion-size exploration,
budget/protein/time/allergen/equipment checks, Pareto trade-offs and
a transparent experimental ranking.

**What is not established:** a measured soy-to-tofu manufacturing yield, a
complete kitchen cost (electricity, labour and overhead can be absent),
real preparation duration, tested flavour or texture, confirmed food safety,
nutritional equivalence to beef, or model accuracy against chefs.

**AI scope:** this deterministic constrained search is an optimisation approach,
not a trained culinary or sensory model. Bedrock could suggest or explain
candidates, but generated content must be checked through this engine and
rejected if unsupported. No AWS keys or temporary endpoints are used here.
"""
    )

st.caption(
    "Naija MenuShift · Kitchen Intelligence Studio · "
    "Provisional research exploration only. Built for honest testing at Hack the Fork Nigeria."
)
