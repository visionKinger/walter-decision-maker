from __future__ import annotations


def run(macro_score: float) -> dict:
    if macro_score >= 65:
        regime = "Expansion"
    elif macro_score <= 40:
        regime = "Contraction"
    else:
        regime = "Transition"
    return {"macro_score": macro_score, "macro_regime": regime}
