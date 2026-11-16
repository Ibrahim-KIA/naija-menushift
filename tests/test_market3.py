"""Challenge 3 data and scoring checks: never rank missing real evidence."""
from pathlib import Path

import pytest

from menushift.market3 import (
    WEIGHTS,
    evidence_coverage,
    evidence_gaps,
    evaluate_markets,
    read_opportunities,
    score_opportunity,
    synthetic_demonstration,
)

DATA = Path(__file__).resolve().parents[1] / "data" / "challenge3"


def _sourced(row):
    new = dict(row)
    new.update({
        "Local_Product_Availability_Evidence": "Recorded retailer inventory 2026-11-16",
        "Consumer_Demand_Signal": "Buyer interview dataset OBS-001",
        "Demand_Sample_Size": "40",
        "Demand_Signal_Date": "2026-11-16",
        "Typical_Competing_Product": "Beef suya 100 g portion",
        "Competitor_Price_NGN": "2500",
        "Competitor_Pack_or_Serving_Size": "100 g",
        "Proposed_Product_Price_NGN": "2300",
        "Price_Comparison_Notes": "Same measured 100 g finished portion",
        "Affordability_Proxy_or_Source": "Buyer stated max pay OBS-001",
        "Relevant_Retail_or_Foodservice_Count": "3",
        "Channel_Access_Evidence": "Observed three outlets; two interviews",
        "Soybean_or_Tofu_Supplier_Evidence": "Dated local awara supplier quote",
        "Distribution_or_Storage_Constraints": "Observed insulated transport and chilled holding",
        "Competitor_Intensity_1to5": "2",
        "Demand_Score_1to5": "4",
        "Affordability_Score_1to5": "3",
        "Channel_Score_1to5": "5",
        "Supply_Distribution_Score_1to5": "2",
        "Market_Gap_Score_1to5": "4",
        "Evidence_Confidence": "Low",
        "Source_IDs": "OBS-001;OBS-002",
    })
    return new


def test_source_matrix_preserves_48_options_without_fake_rankings():
    rows = read_opportunities(DATA / "opportunities.csv")
    assert len(rows) == 48
    assert len({r["Opportunity_ID"] for r in rows}) == 48
    assert {r["Product"] for r in rows} == {"Tofu suya", "Kafi soy yoghurt"}
    assert {r["City"] for r in rows} == {"Kano", "Kaduna", "Jos", "Abuja", "Lagos", "Ibadan"}
    outcome = evaluate_markets(rows)
    assert all(not r.ready and r.score is None for r in outcome)
    report = evidence_coverage(outcome)
    assert report["rankable"] == 0
    assert report["not_rankable"] == 48


def test_source_matrix_has_zero_real_survey_rows():
    csv = (DATA / "survey_responses.csv").read_text(encoding="utf-8").strip().splitlines()
    assert len(csv) == 1  # header only; never invent respondents


def test_scoring_formula_matches_agreed_workbook_weights():
    row = _sourced(read_opportunities(DATA / "opportunities.csv")[0])
    r = score_opportunity(row)
    assert r.ready
    assert r.score == 73.0
    assert sum(WEIGHTS.values()) == 100


def test_missing_demand_abstains_instead_of_scoring_zero():
    row = _sourced(read_opportunities(DATA / "opportunities.csv")[0])
    row["Consumer_Demand_Signal"] = ""
    result = score_opportunity(row)
    assert result.score is None
    assert "Consumer_Demand_Signal" in result.gaps


def test_invalid_out_of_range_criteria_cannot_be_ranked():
    row = _sourced(read_opportunities(DATA / "opportunities.csv")[0])
    row["Demand_Score_1to5"] = "6"
    result = score_opportunity(row)
    assert not result.ready
    assert any("Demand_Score_1to5" in x for x in evidence_gaps(row))


def test_bad_weighting_is_rejected():
    row = _sourced(read_opportunities(DATA / "opportunities.csv")[0])
    with pytest.raises(ValueError, match="sum to 100"):
        score_opportunity(row, weights={k: 10 for k in WEIGHTS})


def test_complete_synthetic_scenarios_are_explicitly_synthetic_and_reproducible():
    rows = read_opportunities(DATA / "opportunities.csv")
    data = synthetic_demonstration(rows)
    assert len(data) == 12
    a = evaluate_markets(data, synthetic=True)
    b = evaluate_markets(data, synthetic=True)
    assert all(r.synthetic and r.score is not None for r in a)
    assert [(r.opportunity_id, r.score) for r in a] == [(r.opportunity_id, r.score) for r in b]
    assert max(r.score for r in a) <= 100
    assert min(r.score for r in a) >= 20


def test_duplicate_ids_rejected(tmp_path):
    src = DATA / "opportunities.csv"
    text = src.read_text(encoding="utf-8").splitlines()
    file = tmp_path / "duplicate.csv"
    file.write_text("\n".join([text[0], text[1], text[1]]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="unique"):
        read_opportunities(file)
