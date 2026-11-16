"""Experimental AI segmentation must not turn synthetic responses into Nigerian evidence."""
from pathlib import Path

import pytest

from menushift.market_segments import (
    read_survey,
    segment_consumers,
    synthetic_survey,
)

DATA = Path(__file__).resolve().parents[1] / "data" / "challenge3"


def test_real_survey_is_empty_and_model_refuses_to_fit():
    raw = read_survey(DATA / "survey_responses.csv")
    assert raw == []
    with pytest.raises(ValueError, match="at least 24"):
        segment_consumers(raw, "Tofu suya")


@pytest.mark.parametrize("product", ["Tofu suya", "Kafi soy yoghurt"])
def test_synthetic_segmentation_is_deterministic_and_labelled(product):
    invented = synthetic_survey(product)
    first = segment_consumers(invented, product, synthetic=True)
    second = segment_consumers(invented, product, synthetic=True)
    assert first.synthetic
    assert first.n_respondents == 36
    assert sum(s.respondents for s in first.segments) == 36
    assert first.segments == second.segments
    assert len(first.segments) == 3
    assert 0 <= first.silhouette <= 1


def test_unconsented_response_does_not_enter_model():
    invented = synthetic_survey("Tofu suya")
    invented[0]["Consent_Obtained"] = "no"
    result = segment_consumers(invented, "Tofu suya", synthetic=True)
    assert result.n_respondents == 35
    assert result.excluded_unconsented == 1


def test_small_and_homogeneous_samples_rejected():
    with pytest.raises(ValueError, match="at least 24"):
        segment_consumers(synthetic_survey("Tofu suya")[:10], "Tofu suya")
    entries = synthetic_survey("Tofu suya")
    for row in entries:
        row["Max_WTP_Tofu_Suya_NGN"] = "500"
        row["Willing_To_Buy_Tofu_Suya"] = "no"
        row["Willing_To_Try_Tofu_Suya"] = "no"
        row["Eats_Suya_How_Often"] = "rarely"
    with pytest.raises(ValueError, match="lack variation"):
        segment_consumers(entries, "Tofu suya")


def test_invalid_wtp_fails_explicitly():
    rows = synthetic_survey("Kafi soy yoghurt")
    rows[0]["Max_WTP_Kafi_NGN"] = "nan"
    with pytest.raises(ValueError, match="invalid"):
        segment_consumers(rows, "Kafi soy yoghurt")
