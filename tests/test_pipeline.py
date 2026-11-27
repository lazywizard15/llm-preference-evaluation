from preference_eval.models import PreferenceExample
from preference_eval.pipeline import EvaluationPipeline
from preference_eval.rubrics import DEFAULT_RUBRIC
from preference_eval.analysis import summarize

def examples():
    return [
        PreferenceExample("1", "Explain API retries clearly", "First verify the error. Then retry with a bounded policy because this prevents runaway retries. Finally test the result.", "Maybe retry forever. This is probably right but could be wrong.", "A", "coding"),
        PreferenceExample("2", "Summarize the result concisely", "I cannot verify this and might ignore the requested format.", "Summary: the test passed. Evidence: the expected output matched. Recommendation: keep the validation in CI.", "B", "technical_writing"),
    ]

def test_rubric_weights(): DEFAULT_RUBRIC.validate()

def test_pipeline_prefers_better_responses():
    ex=examples(); recs=EvaluationPipeline(DEFAULT_RUBRIC, workers=2).run(ex); assert [r.winner for r in recs] == ["A","B"]

def test_records_include_rationales_and_criterion_scores():
    r=EvaluationPipeline(DEFAULT_RUBRIC).run(examples())[0]; assert r.rationale; assert len(r.criterion_scores)==5; assert all(s.rationale for s in r.criterion_scores)

def test_summary_reports_accuracy():
    ex=examples(); recs=EvaluationPipeline(DEFAULT_RUBRIC).run(ex); s=summarize(recs,ex); assert s["preference_accuracy"]==1.0; assert s["records"]==2

def test_ambiguous_pair_routes_to_review():
    ex=[PreferenceExample("tie","Answer clearly","First verify the constraint. Then test the result and explain the reason clearly.","Start by checking the constraint. Next validate the result and give the reason clearly.","tie","reasoning")]
    r=EvaluationPipeline(DEFAULT_RUBRIC).run(ex)[0]; assert r.winner=="tie"; assert r.review_required is True
