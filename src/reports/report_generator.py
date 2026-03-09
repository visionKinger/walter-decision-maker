from __future__ import annotations

import csv
import json
import os
from datetime import date
from pathlib import Path
from urllib import request


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


def generate_deepseek_report(context: str) -> str | None:
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("DEEKSEEK_API_KEY")
    if not api_key:
        return None

    body = json.dumps(
        {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are THE DECISION-MAKER'S DATA ENGINE. "
                        "Write a macro intelligence report in markdown with this exact high-level structure: "
                        "1) Title block using lines: THE DECISION-MAKER'S / DATA ENGINE / CHINA MACRO INTELLIGENCE REPORT / "
                        "Applying the Dalio · Druckenmiller · Jiang Framework. "
                        "2) Metadata line with Date, Classification, Region. "
                        "3) Executive Summary. "
                        "4) Module 1 — The Cycle Report (Dalio Framework). "
                        "5) Module 2 — Liquidity & Sentiment Dashboard (Druckenmiller Framework). "
                        "6) Module 3 — Game Theory Matrix (Jiang Framework). "
                        "7) Module 4 — Practical Data Engine Checklist using checkboxes and watchpoints. "
                        "8) Unified Framework Verdict. "
                        "Keep tone institutional and decision-oriented; infer cautiously and avoid fabricated statistics."
                    ),
                },
                {"role": "user", "content": context},
            ],
            "temperature": 0.2,
        }
    ).encode("utf-8")

    req = request.Request(
        "https://api.deepseek.com/chat/completions",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req, timeout=45) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload["choices"][0]["message"]["content"]


def build_llm_context(
    *,
    as_of: date,
    env: str,
    macro_regime: str,
    macro_score: float,
    liquidity_status: str,
    liquidity_score: float,
    trend_status: str,
    trend_score: float,
    opportunity_score: float,
    allocation: str,
    risk_alert: str,
    cycle: dict,
    liquidity_dash: dict,
    game_theory: list[dict],
    daily_review: str,
    expectation_signal: str,
) -> str:
    return "\n".join(
        [
            f"Date: {as_of.isoformat()}",
            "Classification: Decision-Maker Use Only",
            "Region: China / Asia-Pacific",
            f"Environment: {env}",
            f"Macro regime: {macro_regime} (score={macro_score})",
            f"Liquidity status: {liquidity_status} (score={liquidity_score})",
            f"Trend status: {trend_status} (score={trend_score})",
            f"Opportunity score: {opportunity_score}",
            f"Allocation: {allocation}",
            f"Risk alert: {risk_alert}",
            f"Cycle module snapshot: {cycle}",
            f"Liquidity dashboard snapshot: {liquidity_dash}",
            f"Game theory snapshot: {game_theory}",
            f"Daily review: {daily_review}",
            f"Expectation signal: {expectation_signal}",
        ]
    )


def build_fallback_report(context: str) -> str:
    return "\n".join(
        [
            "# THE DECISION-MAKER'S",
            "# DATA ENGINE",
            "# CHINA MACRO INTELLIGENCE REPORT",
            "### Applying the Dalio · Druckenmiller · Jiang Framework",
            "",
            "## Executive Summary",
            "LLM service unavailable. This report preserves the required structure and embeds the latest pipeline context.",
            "",
            "## Module 1 — The Cycle Report (Dalio Framework)",
            "Refer to context below.",
            "",
            "## Module 2 — Liquidity & Sentiment Dashboard (Druckenmiller Framework)",
            "Refer to context below.",
            "",
            "## Module 3 — Game Theory Matrix (Jiang Framework)",
            "Refer to context below.",
            "",
            "## Module 4 — Practical Data Engine Checklist",
            "- [x] CHECK THE CYCLE",
            "- [x] CHECK LIQUIDITY",
            "- [x] CHECK INCENTIVES",
            "- [x] CHECK THE NEWS",
            "",
            "## Unified Framework Verdict",
            "Use the context block to produce a discretionary decision.",
            "",
            "---",
            "### Context",
            context,
        ]
    )


def write_daily_report(payload: dict, report_dir: str = "data/daily_report") -> Path:
    folder = Path(report_dir)
    folder.mkdir(parents=True, exist_ok=True)
    out = folder / f"report_{date.today().isoformat()}.md"
    out.write_text(payload["markdown"], encoding="utf-8")
    return out


def append_decision_log(row: dict, log_path: str) -> None:
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as f:
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
