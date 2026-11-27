from preference_eval.models import PreferenceExample
from preference_eval.validator import validate_examples

def test_duplicate_ids_detected():
    ex=[PreferenceExample("x","p","a","b"), PreferenceExample("x","p2","a2","b2")]
    assert any("duplicate" in x for x in validate_examples(ex))

def test_identical_responses_detected():
    ex=[PreferenceExample("x","p","same","same")]
    assert any("identical" in x for x in validate_examples(ex))
