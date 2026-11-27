from pathlib import Path
from preference_eval.models import PreferenceExample
from preference_eval.pipeline import EvaluationPipeline
from preference_eval.rubrics import DEFAULT_RUBRIC
from preference_eval.io import export_jsonl, export_csv

def test_exports_jsonl_and_csv(tmp_path: Path):
    ex=[PreferenceExample("1","Explain retries","First verify the error, then retry and test the result because evidence matters.","Maybe retry forever; this could be wrong.","A","coding")]
    recs=EvaluationPipeline(DEFAULT_RUBRIC).run(ex)
    jp=tmp_path/"out.jsonl"; cp=tmp_path/"out.csv"
    export_jsonl(recs,jp); export_csv(recs,cp)
    assert jp.read_text().strip()
    assert "example_id,winner" in cp.read_text()
