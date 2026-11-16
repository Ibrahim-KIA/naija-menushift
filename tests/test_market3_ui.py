"""Streamlit AppTest: Challenge 3 market page fails closed, demo is segregated."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

PAGE = Path(__file__).resolve().parents[1] / "pages" / "3_Market_Opportunity.py"


def test_real_market_data_abstains_and_shows_missing_evidence():
    at = AppTest.from_file(str(PAGE), default_timeout=30).run()
    assert not at.exception
    assert any("Where should alternative proteins launch?" in x.value for x in at.title)
    assert any("No defensible winning market" in x.value for x in at.error)
    assert any("REAL-EVIDENCE MODE" in x.value for x in at.warning)
    assert any("48" in str(x.value) for x in at.metric)


def test_synthetic_rankings_are_explicitly_marked_as_synthetic():
    at = AppTest.from_file(str(PAGE), default_timeout=30).run()
    at.radio[0].set_value("SYNTHETIC ranking demonstration").run()
    assert not at.exception
    assert any("SYNTHETIC DEMONSTRATION" in x.value for x in at.warning)
    assert all("Missing evidence" not in str(x.value) for x in at.error)


def test_clustering_remains_inactive_until_requested():
    at = AppTest.from_file(str(PAGE), default_timeout=30).run()
    assert not at.exception
    assert any("Only 0 consented" in x.value for x in at.info)
