from __future__ import annotations


def classify_environment(macro_regime: str, liquidity_status: str, trend_status: str) -> str:
    if macro_regime == "Contraction" and liquidity_status == "Tightening":
        return "Risk-Off"
    if macro_regime == "Expansion" and liquidity_status == "Easing" and trend_status == "Bullish":
        return "Risk-On"
    return "Neutral"
