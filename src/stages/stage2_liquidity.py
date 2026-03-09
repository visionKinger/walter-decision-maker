from __future__ import annotations


def run(liquidity_score: float) -> dict:
    if liquidity_score >= 60:
        status = "Easing"
    elif liquidity_score <= 40:
        status = "Tightening"
    else:
        status = "Neutral"
    return {"liquidity_score": liquidity_score, "liquidity_status": status}
