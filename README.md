# LLM Preference Evaluation & Rubric Pipeline

A Python pipeline for producing auditable pairwise preference data from LLM response pairs. It defines a versioned five-dimension rubric, scores both responses per criterion, assigns A/B/tie labels, writes concise rationales, routes low-confidence cases to review, validates dataset quality, and exports JSONL/CSV plus a summary report.

## Rubric
- Correctness: 35%
- Instruction adherence: 25%
- Completeness: 15%
- Relevance: 15%
- Clarity: 10%

## Pipeline features
- Versioned rubric definitions and schema validation
- Pairwise preference labels with per-criterion 1-5 scores
- Written rationales and confidence scores
- Low-confidence / tie review queue
- Dataset QA for duplicate IDs, missing fields, and identical responses
- Parallel batch evaluation and checkpoint support
- JSONL and CSV export for downstream training/evaluation workflows
- Markdown summaries with preference agreement, review rate, and category coverage

## Run
```bash
python -m pip install -e .
python data/generate_benchmark.py
python -m preference_eval.cli data/preference_benchmark.jsonl
pytest -q
```

The benchmark generator creates 144 response pairs, including ambiguous calibration cases, across coding, reasoning, instruction following, technical writing, factual QA, and data analysis. It is a deterministic local benchmark for testing the evaluation pipeline, not a claim about production model quality.
