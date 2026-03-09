import pytest
from urllib.error import URLError

from src.main import run_pipeline
from src.models.decision_tree import classify_environment


def test_decision_tree_states():
    assert classify_environment("Contraction", "Tightening", "Bearish") == "Risk-Off"
    assert classify_environment("Expansion", "Easing", "Bullish") == "Risk-On"
    assert classify_environment("Transition", "Neutral", "Sideways") == "Neutral"


def test_pipeline_runs_and_generates_report():
    try:
        result = run_pipeline()
    except URLError as exc:
        pytest.skip(f"Live data endpoints are unreachable in this environment: {exc}")

    assert "Environment=" in result["summary"]
    assert result["report_path"].endswith(".md")
