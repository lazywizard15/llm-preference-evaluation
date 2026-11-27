from __future__ import annotations
import argparse, json
from pathlib import Path
from .analysis import summarize, markdown_report
from .io import load_examples, export_jsonl, export_csv
from .pipeline import EvaluationPipeline
from .rubrics import DEFAULT_RUBRIC

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out", default="reports/evaluations.jsonl")
    ap.add_argument("--csv", default="reports/evaluations.csv")
    ap.add_argument("--report", default="reports/summary.md")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    examples = load_examples(args.input)
    records = EvaluationPipeline(DEFAULT_RUBRIC, args.workers).run(examples)
    export_jsonl(records, args.out); export_csv(records, args.csv)
    summary = summarize(records, examples)
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(markdown_report(summary))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__": main()
