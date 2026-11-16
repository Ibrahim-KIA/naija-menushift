"""Hack the Fork Challenge 3: independent market opportunity research page.

Not a production demand estimator. Synthetic outputs are segregated from research.
"""
from __future__ import annotations

import csv
from io import StringIO
from pathlib import Path

import pandas as pd
import streamlit as st

from menushift.market3 import (
    WEIGHT_SCENARIOS,
    evaluate_markets,
    evidence_coverage,
    read_opportunities,
    synthetic_demonstration,
)
from menushift.market_segments import (
    read_survey,
    segment_consumers,
    synthetic_survey,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "challenge3"

st.set_page_config(
    page_title="Market Opportunity | Naija MenuShift",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.caption("HACK THE FORK NIGERIA 2026 · CHALLENGE 3")
st.title("Where should alternative proteins launch?")
st.write(
    "Compare **tofu suya** and **Kafi soy yoghurt** by city, consumer segment, "
    "affordability, retail access, sourcing and competition."
)
st.info(
    "Research tool, not an automatic forecast. State soybean output measures "
    "agricultural production, **not** city demand or guaranteed local supplier access."
)

try:
    candidates = read_opportunities(DATA / "opportunities.csv")
    survey = read_survey(DATA / "survey_responses.csv")
except (OSError, ValueError) as error:
    st.error(f"Market datasets cannot be loaded: {error}")
    st.stop()

mode = st.radio(
    "Evidence mode",
    ("Research evidence (no invented scores)", "SYNTHETIC ranking demonstration"),
    horizontal=True,
    help="The demonstration uses deliberately fabricated 1–5 scores, not Nigerian market measurements.",
)
is_demo = mode.startswith("SYNTHETIC")
considered = synthetic_demonstration(candidates) if is_demo else candidates
results = evaluate_markets(considered, synthetic=is_demo)
coverage = evidence_coverage(results)

st.warning(
    "SYNTHETIC DEMONSTRATION: all displayed rankings and criterion scores are invented, "
    "for testing scoring logic only. Not a recommended location."
    if is_demo
    else "REAL-EVIDENCE MODE: Missing product-specific demand and observed price data "
    "mean the tool must abstain from ranking."
)
k1, k2, k3 = st.columns(3)
k1.metric("Candidate opportunities", coverage["opportunities"])
k2.metric("Rankable opportunities", coverage["rankable"])
k3.metric("Require more evidence", coverage["not_rankable"])

market, segments, methods = st.tabs(
    ["Market opportunities", "Buyer segmentation (experimental AI)", "Sources & methods"]
)
with market:
    st.subheader("Product × city × customer segment")
    c1, c2 = st.columns(2)
    with c1:
        chosen_product = st.selectbox("Product", ["Both", "Tofu suya", "Kafi soy yoghurt"])
    with c2:
        chosen_city = st.selectbox(
            "City", ["All cities", "Kano", "Kaduna", "Jos", "Abuja", "Lagos", "Ibadan"]
        )
    rows = [
        r.as_dict() for r in results
        if (chosen_product == "Both" or r.product == chosen_product)
        and (chosen_city == "All cities" or r.city == chosen_city)
    ]
    st.dataframe(
        pd.DataFrame(rows), hide_index=True, use_container_width=True,
    )
    if not coverage["rankable"]:
        st.error(
            "No defensible winning market can be named yet. The 48 research rows contain "
            "no measured product-specific demand or completed criterion scores."
        )
        st.write(
            "Collect comparable pack/portion prices, dated survey observations, "
            "retailer counts and supplier/cold-chain evidence before scoring."
        )
        st.caption(
            "Provisional fieldwork: Kano/Kaduna for northern soy-food sourcing and "
            "vendor interviews; Lagos/Abuja for channel and competitor comparisons; "
            "Jos/Ibadan as additional comparison markets. These are research priorities, "
            "NOT opportunity rankings."
        )
    else:
        st.subheader("Highest-scoring eligible opportunities")
        top = [r for r in results if r.ready][:3]
        for row in top:
            st.write(
                f"**{row.product}, {row.city}, {row.customer_segment}** — "
                f"{row.score:.1f}/100 · {row.evidence_confidence}"
            )
        with st.expander("Check sensitivity to scoring weights"):
            for label, weights in WEIGHT_SCENARIOS.items():
                scenario = evaluate_markets(considered, weights=weights, synthetic=is_demo)
                winner = next((r for r in scenario if r.ready), None)
                if winner:
                    st.write(f"{label}: {winner.product} in {winner.city} ({winner.score:.1f}/100)")
    if not is_demo:
        st.subheader("Evidence required to unlock rankings")
        missing = coverage["missing_field_counts"]
        st.dataframe(
            pd.DataFrame(
                [{"Evidence field": name, "Rows missing / invalid": count}
                 for name, count in sorted(missing.items(), key=lambda x: -x[1])]
            ),
            hide_index=True, use_container_width=True,
        )
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["Opportunity", "Product", "City", "Missing fields"])
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row[name] for name in writer.fieldnames})
        st.download_button(
            "Download current evidence-gap checklist",
            output.getvalue(), "challenge3_evidence_gaps.csv", "text/csv",
        )
    else:
        with st.expander("How sensitive are synthetic rankings to criterion weights?"):
            for label, weights in WEIGHT_SCENARIOS.items():
                scenario = evaluate_markets(considered, weights=weights, synthetic=True)
                winner = scenario[0]
                st.write(f"{label} → {winner.product}, {winner.city} ({winner.score:.1f})")
        st.caption("Changing a synthetic score does not reveal real customer preferences.")

with segments:
    st.subheader("Exploratory market segmentation")
    st.write(
        "The AI component uses K-means on consented, product-specific responses to group "
        "similar stated purchase behaviours. It requires at least 24 complete responses "
        "per product. Clusters do **not** represent market shares, sales forecasts or "
        "proven willingness to pay."
    )
    segment_product = st.selectbox("Segment product", ["Tofu suya", "Kafi soy yoghurt"])
    demo_clusters = st.checkbox(
        "Show SYNTHETIC 36-person clustering test", value=False,
        help="Synthetic responses are fabricated and are never written to the research dataset.",
    )
    try:
        source = synthetic_survey(segment_product) if demo_clusters else survey
        report = segment_consumers(source, segment_product, synthetic=demo_clusters)
    except ValueError as error:
        st.info(str(error))
    else:
        if report.synthetic:
            st.warning("SIMULATION ONLY: 36 invented responses. Not Nigerian consumer research.")
        st.metric("Responses clustered", report.n_respondents)
        st.write(f"Within-sample silhouette: {report.silhouette} (descriptive only)")
        st.dataframe(
            pd.DataFrame([x.as_dict() for x in report.segments]),
            hide_index=True, use_container_width=True,
        )
        st.caption("The clustering is not used to fabricate a 48-market opportunity score.")

with methods:
    st.subheader("How the evidence gate works")
    st.write(
        "Five criteria are scored from 1–5, with weights: demand 30%, "
        "affordability 25%, channel access 20%, supply/distribution 15%, "
        "competition gap 10%. The score is the weighted sum divided by five, "
        "yielding a value from 20 to 100."
    )
    st.write(
        "A row is ranked only if all five scores AND supporting observations exist: "
        "dated demand data and sample size, comparable prices and serving/pack sizes, "
        "retailer count, supplier/distribution constraints, competitor evidence, "
        "source IDs and an evidence-confidence label."
    )
    st.write(
        "High soybean production is not a consumer-demand score. A yoghurt consumer "
        "survey is not direct evidence of demand for Kafi. A public tofu-suya menu "
        "is a competitor observation, not a measure of its sales."
    )
    st.markdown(
        "**Market references**\n"
        "- [NAERLS 2024 soybean production](https://naerls.gov.ng/wp-content/uploads/2025/04/Agricultural-Performance-Survey-of-2024-Wet-Season-in-Nigeria.pdf)\n"
        "- [Euromonitor 2025 Nigeria dairy category](https://www.euromonitor.com/dairy-products-and-alternatives-in-nigeria/report)\n"
        "- [VeggieVictory Lagos tofu-suya menu](https://veggievictory.com/menu/)\n"
        "- [Nigerian soy-yoghurt sensory study (Bukar et al.)](https://www.nsmjournal.org.ng/uploads/articles/nutritional_and_sensory_evaluation_of_soy-yoghurt_produced_with__lactobacillus_plantarum_isolated_from_locally_fermented_milk__nono__7.pdf)"
    )
    st.caption(
        "Original data: Amina's 15 Nov 2026 workbook. "
        "No real consumer survey responses were supplied. "
        "The model uses only local data and no paid LLM or external customer tracking."
    )
st.divider()
st.caption(
    "Naija MenuShift · Challenge 3 exploration · No unmeasured sales, "
    "price or preference is treated as ground truth."
)
