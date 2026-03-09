from __future__ import annotations


def run(trend_score: float) -> dict:
    if trend_score >= 60:
        trend = "Bullish"
    elif trend_score <= 40:
        trend = "Bearish"
    else:
        trend = "Sideways"
    return {"trend_score": trend_score, "trend_status": trend}
