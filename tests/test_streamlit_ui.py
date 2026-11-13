"""Streamlit AppTest smoke checks: no browser is needed for these interactions.

AppTest does not verify pixel layout, screen readers, zoom or touch hit targets.
"""
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


def _run():
    at = AppTest.from_file(str(APP), default_timeout=25).run()
    assert not at.exception
    return at


def test_public_first_use_is_a_simple_decision_flow():
    at = _run()
    assert any("Naija MenuShift" in title.value for title in at.title)
    assert any("Current restaurant menu item" in sel.label for sel in at.selectbox)
    assert any("Maximum cost per serving" in num.label for num in at.number_input)
    assert any("Minimum estimated protein" in num.label for num in at.number_input)
    assert at.warning  # synthetic-data disclaimer cannot be hidden


def test_no_feasible_budget_abstains_without_beef_recommendation():
    at = _run()
    at.number_input(key="budget").set_value(1.0).run()
    assert not at.exception
    assert any("No plant-based option" in err.message for err in at.error)


def test_allergen_selection_prevents_unreviewed_and_soy_options():
    at = _run()
    at.multiselect(key="avoid").set_value(["soy"]).run()
    assert not at.exception
    assert any("No plant-based option" in err.message for err in at.error)


def test_research_mode_has_no_synthetic_fallback():
    at = _run()
    at.sidebar.radio[0].set_value("Research data (requires evidence)").run()
    assert not at.exception
    assert any("Research data unavailable" in err.message for err in at.error)
