from __future__ import annotations

from pathlib import Path

import json

from src.data.data_monitor import DataMonitor
from src.data.indicators import expectation_gap_score, liquidity_score, macro_score, trend_score
from src.models.decision_tree import classify_environment
from src.models.scoring import weighted_opportunity_score
from src.reports.report_generator import (
    append_decision_log,
    build_cycle_report,
    build_game_theory_matrix,
    build_liquidity_dashboard,
    write_daily_report,
)
from src.stages import (
    stage0_quality_filter,
    stage1_macro_cycle,
    stage2_liquidity,
    stage3_expectation_gap,
    stage4_trend_confirm,
    stage5_position_decision,
    stage6_daily_review,
)


def load_settings(path: str = "config/settings.json") -> dict:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def run_pipeline() -> dict:
    settings = load_settings()
    monitor = DataMonitor()
    snapshot = monitor.fetch_snapshot()

    stage0 = stage0_quality_filter.run(roe=0.18, debt_ratio=0.35, fcf_margin=0.12)
    m_score = macro_score(snapshot)
    l_score = liquidity_score(snapshot)
    e_score = expectation_gap_score(snapshot)
    t_score = trend_score(snapshot)

    stage1 = stage1_macro_cycle.run(m_score)
    stage2 = stage2_liquidity.run(l_score)
    stage3 = stage3_expectation_gap.run(e_score)
    stage4 = stage4_trend_confirm.run(t_score)

    overall = weighted_opportunity_score(
        {
            "macro": m_score,
            "liquidity": l_score,
            "trend": t_score,
            "expectation_gap": e_score,
            "quality": stage0["quality_score"],
        },
        settings["weights"],
    )

    env = classify_environment(stage1["macro_regime"], stage2["liquidity_status"], stage4["trend_status"])
    stage5 = stage5_position_decision.run(stage1["macro_regime"], stage2["liquidity_status"], stage4["trend_status"], overall)

    cycle = build_cycle_report(stage1["macro_regime"], m_score)
    liquidity_dash = build_liquidity_dashboard(stage2["liquidity_status"], l_score)
    game_theory = build_game_theory_matrix()

    summary = (
        f"Environment={env}, Macro={stage1['macro_regime']}, Liquidity={stage2['liquidity_status']}, "
        f"Trend={stage4['trend_status']}, Score={overall}, Allocation={stage5['allocation']}"
    )
    stage6 = stage6_daily_review.run(summary)

    markdown = "\n".join(
        [
            "# Walter Daily Decision Report",
            f"- Macro Regime: {stage1['macro_regime']} ({m_score})",
            f"- Liquidity Status: {stage2['liquidity_status']} ({l_score})",
            f"- Trend Status: {stage4['trend_status']} ({t_score})",
            f"- Opportunity Score: {overall}",
            f"- Portfolio Allocation: {stage5['allocation']}",
            f"- Risk Alert: {stage5['risk_alert']}",
            "",
            "## Module 1: Cycle Report",
            str(cycle),
            "",
            "## Module 2: Liquidity & Sentiment Dashboard",
            str(liquidity_dash),
            "",
            "## Module 3: Game Theory Matrix",
            *[str(x) for x in game_theory],
            "",
            f"## Daily Review\n{stage6}",
            f"## Expectation Signal\n{stage3}",
        ]
    )

    out = write_daily_report({"markdown": markdown}, settings["paths"]["report_dir"])

    append_decision_log(
        {
            "date": str(snapshot.as_of),
            "macro_regime": stage1["macro_regime"],
            "liquidity_status": stage2["liquidity_status"],
            "trend_status": stage4["trend_status"],
            "opportunity_score": overall,
            "allocation": stage5["allocation"],
            "risk_alert": stage5["risk_alert"],
            "notes": env,
        },
        settings["paths"]["decision_log"],
    )

    return {"summary": summary, "report_path": str(out)}


if __name__ == "__main__":
    result = run_pipeline()
    print(result["summary"])
    print(f"Report written to: {result['report_path']}")
