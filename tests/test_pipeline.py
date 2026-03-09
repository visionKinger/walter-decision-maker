from src.main import run_pipeline
from src.models.decision_tree import classify_environment


def test_decision_tree_states():
    assert classify_environment("Contraction", "Tightening", "Bearish") == "Risk-Off"
    assert classify_environment("Expansion", "Easing", "Bullish") == "Risk-On"
    assert classify_environment("Transition", "Neutral", "Sideways") == "Neutral"


def test_pipeline_runs_and_generates_report():
    result = run_pipeline()
    assert "Environment=" in result["summary"]
    assert result["report_path"].endswith(".md")
