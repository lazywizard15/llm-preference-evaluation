from __future__ import annotations
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from .judge import RubricJudge
from .models import EvaluationRecord, PreferenceExample, Rubric
from .validator import validate_examples, DatasetValidationError

class EvaluationPipeline:
    def __init__(self, rubric: Rubric, workers: int = 4):
        self.rubric = rubric; self.workers = workers; self.judge = RubricJudge(rubric)

    def run(self, examples: list[PreferenceExample], checkpoint: str | Path | None = None) -> list[EvaluationRecord]:
        issues = validate_examples(examples)
        if issues: raise DatasetValidationError("; ".join(issues))
        completed: dict[str, EvaluationRecord] = {}
        checkpoint_path = Path(checkpoint) if checkpoint else None
        if checkpoint_path and checkpoint_path.exists():
            for line in checkpoint_path.read_text().splitlines():
                if not line.strip(): continue
                raw = json.loads(line); completed[raw["example_id"]] = None  # type: ignore[assignment]
        pending = [ex for ex in examples if ex.example_id not in completed]
        with ThreadPoolExecutor(max_workers=self.workers) as pool: records = list(pool.map(self.judge.evaluate, pending))
        if checkpoint_path:
            checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
            with checkpoint_path.open("a", encoding="utf-8") as f:
                for record in records: f.write(json.dumps(record.to_dict()) + "\n")
        return records
