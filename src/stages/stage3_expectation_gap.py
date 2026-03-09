from __future__ import annotations


def run(expectation_gap_score: float) -> dict:
    signal = "Positive Surprise" if expectation_gap_score >= 55 else "Negative/Flat"
    return {"expectation_gap_score": expectation_gap_score, "expectation_signal": signal}
