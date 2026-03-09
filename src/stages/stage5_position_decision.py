from __future__ import annotations


def run(regime: str, liquidity: str, trend: str, overall_score: float) -> dict:
    if regime == "Contraction" or liquidity == "Tightening" or trend == "Bearish":
        allocation = "Defensive 20-40%"
        risk = "High"
    elif regime == "Expansion" and liquidity == "Easing" and trend == "Bullish" and overall_score >= 70:
        allocation = "Aggressive 70-90%"
        risk = "Medium"
    else:
        allocation = "Balanced 40-70%"
        risk = "Medium"
    return {"allocation": allocation, "risk_alert": risk}
