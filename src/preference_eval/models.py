from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal

Winner = Literal["A", "B", "tie"]

@dataclass(frozen=True)
class Criterion:
    name: str
    weight: float
    description: str

@dataclass(frozen=True)
class Rubric:
    name: str
    version: str
    criteria: tuple[Criterion, ...]
    def validate(self) -> None:
        total = sum(c.weight for c in self.criteria)
        if abs(total - 1.0) > 1e-9: raise ValueError(f"rubric weights must sum to 1.0, got {total}")
        if len({c.name for c in self.criteria}) != len(self.criteria): raise ValueError("criterion names must be unique")

@dataclass(frozen=True)
class PreferenceExample:
    example_id: str
    prompt: str
    response_a: str
    response_b: str
    expected_winner: Winner | None = None
    category: str = "general"

@dataclass(frozen=True)
class CriterionScore:
    criterion: str
    score_a: int
    score_b: int
    rationale: str

@dataclass(frozen=True)
class EvaluationRecord:
    example_id: str
    rubric_name: str
    rubric_version: str
    winner: Winner
    total_a: float
    total_b: float
    confidence: float
    criterion_scores: tuple[CriterionScore, ...]
    rationale: str
    review_required: bool
    category: str
    def to_dict(self) -> dict: return asdict(self)
