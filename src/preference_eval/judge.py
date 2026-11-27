from __future__ import annotations
import re
from dataclasses import dataclass
from .models import CriterionScore, EvaluationRecord, PreferenceExample, Rubric

_NEGATIVE = {"incorrect", "wrong", "fabricated", "irrelevant", "unsafe", "cannot", "guess", "maybe", "probably", "ignore", "omitted", "contradiction", "error", "hallucinated"}
_POSITIVE = {"because", "therefore", "example", "steps", "specifically", "verify", "test", "evidence", "result", "first", "second", "finally", "summary", "recommend", "reason"}

def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.lower())

def _quality_features(prompt: str, response: str) -> dict[str, float]:
    toks = _tokens(response)
    ptoks = set(_tokens(prompt)); rtoks = set(toks)
    overlap = len(ptoks & rtoks) / max(1, len(ptoks))
    neg = sum(t in _NEGATIVE for t in toks); pos = sum(t in _POSITIVE for t in toks)
    sentences = max(1, len(re.findall(r"[.!?](?:\s|$)", response)))
    avg_sentence = len(toks) / sentences
    structure = min(1.0, (response.count("\n") + response.count(":") + response.count(";") + 1) / 5)
    length_score = 1.0 - min(1.0, abs(len(toks) - 70) / 160)
    clarity = max(0.0, 1.0 - max(0.0, avg_sentence - 28) / 45)
    return {"overlap": overlap, "negative": min(1.0, neg / 4), "positive": min(1.0, pos / 5), "structure": structure, "length": max(0.0, length_score), "clarity": clarity}

def _score_dimension(name: str, f: dict[str, float]) -> int:
    if name == "correctness": raw = 3.0 + 1.2 * f["positive"] - 2.2 * f["negative"] + 0.4 * f["overlap"]
    elif name == "instruction_adherence": raw = 2.5 + 1.8 * f["overlap"] + 0.4 * f["structure"] - 1.5 * f["negative"]
    elif name == "completeness": raw = 2.2 + 1.4 * f["length"] + 0.8 * f["structure"] + 0.5 * f["positive"]
    elif name == "relevance": raw = 2.7 + 1.9 * f["overlap"] - 1.0 * f["negative"]
    else: raw = 2.5 + 1.6 * f["clarity"] + 0.7 * f["structure"] - 0.8 * f["negative"]
    return max(1, min(5, int(round(raw))))

@dataclass
class RubricJudge:
    rubric: Rubric
    tie_margin: float = 0.18
    review_threshold: float = 0.62

    def evaluate(self, ex: PreferenceExample) -> EvaluationRecord:
        fa = _quality_features(ex.prompt, ex.response_a); fb = _quality_features(ex.prompt, ex.response_b)
        criterion_scores = []; total_a = 0.0; total_b = 0.0
        for criterion in self.rubric.criteria:
            sa = _score_dimension(criterion.name, fa); sb = _score_dimension(criterion.name, fb)
            total_a += criterion.weight * sa; total_b += criterion.weight * sb
            if sa == sb: rationale = f"Both responses scored similarly on {criterion.name.replace('_', ' ')}."
            else:
                better = "A" if sa > sb else "B"
                rationale = f"Response {better} was stronger on {criterion.name.replace('_', ' ')} under rubric v{self.rubric.version}."
            criterion_scores.append(CriterionScore(criterion.name, sa, sb, rationale))
        delta = total_a - total_b
        winner = "tie" if abs(delta) < self.tie_margin else ("A" if delta > 0 else "B")
        confidence = min(0.99, 0.52 + abs(delta) / 3.0)
        review = confidence < self.review_threshold or winner == "tie"
        strongest = sorted(criterion_scores, key=lambda s: abs(s.score_a - s.score_b), reverse=True)[:2]
        rationale = " ".join(s.rationale for s in strongest)
        return EvaluationRecord(ex.example_id, self.rubric.name, self.rubric.version, winner, round(total_a,3), round(total_b,3), round(confidence,3), tuple(criterion_scores), rationale, review, ex.category)
