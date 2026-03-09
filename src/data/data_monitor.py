from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from urllib import parse, request
import csv
import io
import json


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


@dataclass
class QualitySnapshot:
    as_of: date
    roe: float
    debt_ratio: float
    fcf_margin: float
    symbol: str


class DataMonitor:
    """Fetches market and quality inputs from live public data endpoints."""

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
            raise ValueError(f"Invalid open price for {symbol}: {open_px}")
        return round((close_px - open_px) / open_px * 100, 2)

    def _fetch_fred_latest(self, series_id: str) -> float:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        with request.urlopen(url, timeout=self.timeout_s) as resp:
            text = resp.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        rows = [r for r in reader if r.get(series_id) and r[series_id] != "."]
        if not rows:
            raise ValueError(f"No FRED data for {series_id}")
        return float(rows[-1][series_id])

    def _fetch_fred_prev(self, series_id: str) -> float:
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
        with request.urlopen(url, timeout=self.timeout_s) as resp:
            text = resp.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))
        values = [float(r[series_id]) for r in reader if r.get(series_id) and r[series_id] != "."]
        if len(values) < 2:
            raise ValueError(f"Insufficient FRED history for {series_id}")
        return values[-2]

    def _fetch_fmp_quality(self, symbol: str, api_key: str | None = None) -> QualitySnapshot:
        key = api_key or "demo"
        q_symbol = parse.quote(symbol.upper())
        url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{q_symbol}?apikey={parse.quote(key)}"
        with request.urlopen(url, timeout=self.timeout_s) as resp:
            payload = json.loads(resp.read().decode("utf-8"))

        if not payload or not isinstance(payload, list):
            raise ValueError(f"No quality metrics returned for {symbol}")

        latest = payload[0]
        roe = float(latest["roeTTM"])
        debt_to_equity = float(latest["debtToEquityTTM"])
        fcf_per_share = float(latest["freeCashFlowPerShareTTM"])
        net_income_per_share = float(latest["netIncomePerShareTTM"])
        if net_income_per_share == 0:
            raise ValueError("Invalid netIncomePerShareTTM=0 while deriving FCF margin proxy")

        debt_ratio = debt_to_equity / (1.0 + debt_to_equity) if debt_to_equity >= 0 else 1.0
        fcf_margin_proxy = fcf_per_share / abs(net_income_per_share)

        return QualitySnapshot(
            as_of=date.today(),
            roe=max(0.0, roe),
            debt_ratio=min(max(debt_ratio, 0.0), 1.0),
            fcf_margin=min(max(fcf_margin_proxy, 0.0), 1.0),
            symbol=symbol.upper(),
        )

    def fetch_snapshot(self) -> MarketSnapshot:
        fed_now = self._fetch_fred_latest("WALCL")
        fed_prev = self._fetch_fred_prev("WALCL")
        m2_now = self._fetch_fred_latest("M2SL")
        m2_prev = self._fetch_fred_prev("M2SL")
        hy_spread = self._fetch_fred_latest("BAMLH0A0HYM2")

        return MarketSnapshot(
            as_of=date.today(),
            spy_change_pct=self._fetch_stooq_change("spy.us"),
            csi300_change_pct=self._fetch_stooq_change("2822.hk"),
            us10y_change_bps=self._fetch_stooq_change("10usy.b"),
            dxy_change_pct=self._fetch_stooq_change("dx.f"),
            gold_change_pct=self._fetch_stooq_change("xauusd"),
            oil_change_pct=self._fetch_stooq_change("cl.f"),
            fed_balance_trend=round(((fed_now - fed_prev) / fed_prev) * 100, 4),
            m2_growth=round(((m2_now - m2_prev) / m2_prev) * 100, 4),
            hy_spread=hy_spread,
        )

    def fetch_quality_snapshot(self, symbol: str = "AAPL", api_key: str | None = None) -> QualitySnapshot:
        return self._fetch_fmp_quality(symbol=symbol, api_key=api_key)
