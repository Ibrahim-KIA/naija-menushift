"""Streamlit AppTest smoke checks: no browser is needed for these interactions.

AppTest does not verify pixel layout, screen readers, zoom or touch hit targets.
"""

from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def _run():
    at = AppTest.from_file(str(APP), default_timeout=30).run()
    assert not at.exception
    return at


def test_public_first_use_compares_awara_under_a_budget():
    at = _run()
    assert any("Naija MenuShift" in title.value for title in at.title)
    assert any("Maximum cost per serving" in box.label for box in at.number_input)
    assert at.success
    titles = [header.value for header in at.subheader]
    assert any(title.startswith(("Firm", "Pressed", "Frozen")) for title in titles)
    assert not any(title.startswith("Beef") for title in titles)
    prices = " ".join(frame.value.to_csv() for frame in at.dataframe)
    assert "7171.41" in prices
    assert "2400" not in prices


def test_low_budget_abstains_without_recommending_beef():
    at = _run()
    at.number_input(key="budget").set_value(20.0).run()
    assert not at.exception
    assert any("No awara option" in err.value for err in at.error)
    assert not at.success


def test_soy_exclusion_removes_every_awara_option():
    at = _run()
    at.multiselect(key="avoid").set_value(["soy"]).run()
    assert not at.exception
    assert any("No awara option" in err.value for err in at.error)


def test_high_protein_target_drops_the_firm_option():
    at = _run()
    at.number_input(key="protein").set_value(20.0).run()
    assert not at.exception
    status = at.dataframe[0].value
    firm = status[status["Alternative"].astype(str).str.startswith("Firm")].iloc[0]
    pressed = status[status["Alternative"].astype(str).str.startswith("Pressed")].iloc[0]
    assert firm["Status"] == "Excluded"
    assert pressed["Status"] == "Eligible"
