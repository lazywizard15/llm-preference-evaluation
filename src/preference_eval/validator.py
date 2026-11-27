from __future__ import annotations
from .models import PreferenceExample

class DatasetValidationError(ValueError): pass

def validate_examples(examples: list[PreferenceExample]) -> list[str]:
    issues=[]; seen=set()
    for ex in examples:
        if not ex.example_id.strip(): issues.append("missing example_id")
        if ex.example_id in seen: issues.append(f"duplicate example_id:{ex.example_id}")
        seen.add(ex.example_id)
        if not ex.prompt.strip(): issues.append(f"{ex.example_id}:empty_prompt")
        if not ex.response_a.strip() or not ex.response_b.strip(): issues.append(f"{ex.example_id}:empty_response")
        if ex.response_a.strip() == ex.response_b.strip(): issues.append(f"{ex.example_id}:identical_responses")
        if ex.expected_winner not in (None,"A","B","tie"): issues.append(f"{ex.example_id}:invalid_expected_winner")
    return issues
