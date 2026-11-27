from __future__ import annotations
import json
from pathlib import Path

CATEGORIES = ["coding", "reasoning", "instruction_following", "technical_writing", "factual_qa", "data_analysis"]
GOOD = [
    "Here are the steps. First, identify the requirement. Second, verify the relevant constraint. Finally, test the result and summarize the reason because this makes the answer actionable and easy to verify.",
    "The correct approach is specific: verify the input, apply the requested rule, and report the result with evidence. This follows the instruction directly and avoids unsupported assumptions.",
    "Recommendation: use the requested method, validate the output, and explain the tradeoff. For example, test the edge case before shipping so the conclusion is supported by evidence.",
]
BAD = [
    "Maybe this is probably right, but I would guess and ignore some of the requirements. The answer could be wrong and the details are omitted.",
    "I cannot really verify this. It is probably fine. Some parts may be incorrect or irrelevant and I will skip the requested format.",
    "The result is maybe correct, though I am guessing. Important constraints are omitted and there could be an error or contradiction.",
]
TIE_A = "First, verify the requested constraint. Then test the result and explain the reason clearly. This keeps the answer focused, supported by evidence, and easy to act on."
TIE_B = "Start by checking the requested constraint. Next, validate the result and give the reason clearly. This keeps the response focused, evidence based, and actionable."

def main():
    rows=[]
    for i in range(120):
        cat=CATEGORIES[i % len(CATEGORIES)]
        prompt=f"{cat.replace('_',' ').title()} task {i}: provide a concise, correct answer that follows all instructions and explains the reasoning clearly."
        good=GOOD[i%len(GOOD)] + f" Task reference {i}."
        bad=BAD[i%len(BAD)] + f" Task reference {i}."
        if i % 2 == 0:
            a,b,w=good,bad,"A"
        else:
            a,b,w=bad,good,"B"
        rows.append({"example_id":f"pref-{i:03d}","prompt":prompt,"response_a":a,"response_b":b,"expected_winner":w,"category":cat})
    for j in range(24):
        cat=CATEGORIES[j % len(CATEGORIES)]
        prompt=f"Calibration task {j}: answer clearly, follow the instruction, and support the conclusion."
        rows.append({"example_id":f"tie-{j:03d}","prompt":prompt,"response_a":TIE_A+f" Case {j}.","response_b":TIE_B+f" Case {j}.","expected_winner":"tie","category":cat})
    out=Path(__file__).with_name("preference_benchmark.jsonl")
    out.write_text("\n".join(json.dumps(r) for r in rows)+"\n")
    print(out)
if __name__ == "__main__": main()
