from __future__ import annotations

import csv
from datetime import date
from pathlib import Path


def build_cycle_report(macro_regime: str, macro_score: float) -> dict:
    return {
        "module": "Cycle Report (Dalio)",
        "macro_regime": macro_regime,
        "macro_score": macro_score,
    }


def build_liquidity_dashboard(liquidity_status: str, liquidity_score: float) -> dict:
    return {
        "module": "Liquidity & Sentiment Dashboard (Druckenmiller)",
        "liquidity_status": liquidity_status,
        "liquidity_score": liquidity_score,
    }


def build_game_theory_matrix() -> list[dict]:
    return [
        {"player": "Federal Reserve", "incentive": "Control inflation, sustain growth", "likely_move": "Data-dependent policy"},
        {"player": "Global Funds", "incentive": "Seek real returns", "likely_move": "Rotate by liquidity and trend"},
        {"player": "Governments", "incentive": "Social stability and growth", "likely_move": "Targeted stimulus"},
    ]


def write_daily_report(payload: dict, report_dir: str = "data/daily_report") -> Path:
    folder = Path(report_dir)
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / f"report_{date.today().isoformat()}.md"
    out.write_text(payload["markdown"], encoding="utf-8")
    return out


def append_decision_log(row: dict, log_path: str) -> None:
    with Path(log_path).open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "date",
                "macro_regime",
                "liquidity_status",
                "trend_status",
                "opportunity_score",
                "allocation",
                "risk_alert",
                "notes",
            ],
        )
        writer.writerow(row)
