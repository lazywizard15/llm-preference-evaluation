from __future__ import annotations
import csv
import json
from pathlib import Path
from .models import EvaluationRecord, PreferenceExample

def load_examples(path: str | Path) -> list[PreferenceExample]:
    out = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            out.append(PreferenceExample(**json.loads(line)))
    return out

def export_jsonl(records: list[EvaluationRecord], path: str | Path) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record.to_dict()) + "\n")

def export_csv(records: list[EvaluationRecord], path: str | Path) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["example_id", "winner", "total_a", "total_b", "confidence", "review_required", "category", "rationale"])
        writer.writeheader()
        for r in records:
            writer.writerow({k: getattr(r, k) for k in writer.fieldnames})
