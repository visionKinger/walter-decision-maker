from __future__ import annotations

from src.data.data_monitor import MarketSnapshot


def _clip(value: float) -> float:
    return max(0.0, min(100.0, round(value, 1)))


def macro_score(snapshot: MarketSnapshot) -> float:
    score = 50 + snapshot.spy_change_pct * 8 - snapshot.us10y_change_bps * 1.5 - snapshot.dxy_change_pct * 10
    return _clip(score)


def liquidity_score(snapshot: MarketSnapshot) -> float:
    score = 45 + snapshot.fed_balance_trend * 20 + snapshot.m2_growth * 2 - snapshot.hy_spread * 4
    return _clip(score)


def expectation_gap_score(snapshot: MarketSnapshot) -> float:
    score = 50 + snapshot.csi300_change_pct * 12 + snapshot.oil_change_pct * 2 - snapshot.dxy_change_pct * 4
    return _clip(score)


def trend_score(snapshot: MarketSnapshot) -> float:
    score = 50 + snapshot.spy_change_pct * 10 + snapshot.gold_change_pct * 5 + snapshot.csi300_change_pct * 8
    return _clip(score)
