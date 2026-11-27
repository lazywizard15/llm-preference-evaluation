from __future__ import annotations
from collections import Counter, defaultdict
from .models import EvaluationRecord, PreferenceExample

def summarize(records: list[EvaluationRecord], examples: list[PreferenceExample]) -> dict:
    expected = {e.example_id: e.expected_winner for e in examples}
    labeled = [r for r in records if expected.get(r.example_id) is not None]
    correct = sum(r.winner == expected[r.example_id] for r in labeled)
    counts = Counter(r.winner for r in records)
    reviews = sum(r.review_required for r in records)
    by_category: dict[str, list[EvaluationRecord]] = defaultdict(list)
    for r in records:
        by_category[r.category].append(r)
    return {
        "records": len(records),
        "preference_accuracy": round(correct / max(1, len(labeled)), 4),
        "winner_counts": dict(counts),
        "review_queue": reviews,
        "review_rate": round(reviews / max(1, len(records)), 4),
        "category_counts": {k: len(v) for k, v in sorted(by_category.items())},
        "mean_confidence": round(sum(r.confidence for r in records) / max(1, len(records)), 4),
    }

def markdown_report(summary: dict) -> str:
    lines = [
        "# Preference Evaluation Report", "",
        f"- Records evaluated: {summary['records']}",
        f"- Agreement with labeled preference set: {summary['preference_accuracy']:.1%}",
        f"- Review queue: {summary['review_queue']} ({summary['review_rate']:.1%})",
        f"- Mean confidence: {summary['mean_confidence']:.3f}",
        f"- Winner distribution: {summary['winner_counts']}",
        f"- Category coverage: {summary['category_counts']}",
    ]
    return "\n".join(lines) + "\n"
