from __future__ import annotations

from datetime import date


def run(summary: str) -> dict:
    return {
        "date": str(date.today()),
        "decision_made": summary,
        "review_questions": [
            "What was the decision made today?",
            "What was the rationale behind it?",
            "What were the implications?",
            "Were there unexpected outcomes?",
            "What can we learn for the future?",
        ],
    }
