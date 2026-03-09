from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from urllib import request


@dataclass
class MarketSnapshot:
    as_of: date
    spy_change_pct: float
    csi300_change_pct: float
    us10y_change_bps: float
    dxy_change_pct: float
    gold_change_pct: float
    oil_change_pct: float
    fed_balance_trend: float
    m2_growth: float
    hy_spread: float


class DataMonitor:
    """Fetches market indexes from internet with safe fallbacks."""

    def __init__(self, timeout_s: int = 12) -> None:
        self.timeout_s = timeout_s

    def _fetch_stooq_change(self, symbol: str) -> float:
        url = f"https://stooq.com/q/l/?s={symbol}&f=sd2t2ohlcv&h&e=csv"
        with request.urlopen(url, timeout=self.timeout_s) as resp:
            text = resp.read().decode("utf-8")
        lines = [x.strip() for x in text.splitlines() if x.strip()]
        if len(lines) < 2:
            raise ValueError(f"No data for {symbol}")
        parts = lines[1].split(",")
        open_px = float(parts[3])
        close_px = float(parts[6])
        if open_px <= 0:
            return 0.0
        return round((close_px - open_px) / open_px * 100, 2)

    def fetch_snapshot(self) -> MarketSnapshot:
        defaults = MarketSnapshot(
            as_of=date.today(),
            spy_change_pct=0.35,
            csi300_change_pct=0.18,
            us10y_change_bps=-2.0,
            dxy_change_pct=-0.12,
            gold_change_pct=0.25,
            oil_change_pct=-0.31,
            fed_balance_trend=0.2,
            m2_growth=4.1,
            hy_spread=3.9,
        )

        try:
            return MarketSnapshot(
                as_of=date.today(),
                spy_change_pct=self._fetch_stooq_change("spy.us"),
                csi300_change_pct=self._fetch_stooq_change("2822.hk"),
                us10y_change_bps=self._fetch_stooq_change("10usy.b"),
                dxy_change_pct=self._fetch_stooq_change("dx.f"),
                gold_change_pct=self._fetch_stooq_change("xauusd"),
                oil_change_pct=self._fetch_stooq_change("cl.f"),
                fed_balance_trend=0.2,
                m2_growth=4.1,
                hy_spread=3.9,
            )
        except Exception:
            return defaults
