from __future__ import annotations


def run(roe: float, debt_ratio: float, fcf_margin: float) -> dict:
    quality = (roe * 0.4) + ((1 - debt_ratio) * 0.3) + (fcf_margin * 0.3)
    score = max(0.0, min(100.0, quality * 100))
    return {"quality_score": round(score, 2), "passed": score >= 55}
