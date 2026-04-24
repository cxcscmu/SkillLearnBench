import json
import os
from numbers import Number

import pytest

ANSWER_PATH = "/root/answer.json"

DATA_PATH = "/root/DATA"
QUESTION_PATH = "/root/question.txt"

EXPECTED_ANSWER_Q1 = [
    "eid_3bd7cd36",
    "eid_48346442",
    "eid_52681a26",
    "eid_62db8640",
    "eid_7f69c513",
    "eid_82e9fcef",
    "eid_9d32990b",
    "eid_4a8d1f7b",
]

EXPECTED_ANSWER_Q3 = [
    "https://www.insightguru.com/demo",
    "https://www.knowledgenavigator.com/demo",
    "https://www.wisdomai.com/demo",
]

EXPECTED_ANSWERS = {
    "q1": EXPECTED_ANSWER_Q1,
    "q3": EXPECTED_ANSWER_Q3,
}


def load_answer():
    assert os.path.exists(ANSWER_PATH), f"Missing output file: {ANSWER_PATH}"
    with open(ANSWER_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def coerce_numeric_token(value):
    if isinstance(value, Number):
        return float(value)
    if isinstance(value, str):
        stripped = value.strip()
        try:
            return float(stripped)
        except ValueError as exc:
            raise AssertionError(f"Token field is not numeric/coercible. Got {value}") from exc
    raise AssertionError(f"Token field is not numeric/coercible. Got {value}")


class TestOutputs:
    def test_inputs_exist(self):
        """Check required input files exist."""
        assert os.path.exists(DATA_PATH), f"Missing input file: {DATA_PATH}"
        assert os.path.exists(QUESTION_PATH), f"Missing input file: {QUESTION_PATH}"

    def test_answer_structure_and_values(self):
        """Check answer structure and correctness for all questions."""
        actual = load_answer()
        assert isinstance(actual, dict), f"Answer is not a dict. Got {type(actual)}"
        missing = [k for k in EXPECTED_ANSWERS.keys() if k not in actual]
        assert not missing, f"Answer missing keys: {missing}. Got keys: {list(actual.keys())}"

        for q_key, expected in EXPECTED_ANSWERS.items():
            assert "answer" in actual[q_key], f"Missing 'answer' in {q_key}. Got {actual[q_key]}"
            got = actual[q_key]["answer"]
            assert isinstance(got, list), f"{q_key} answer is not a list. Got {type(got)}"
            missing_expected = sorted(set(expected) - set(got))
            assert not missing_expected, (
                f"{q_key} missing required items. Expected to cover {expected}, got {got}"
            )

    @pytest.mark.parametrize("q_key", ["q1", "q3"])
    def test_tokens_efficient(self, q_key):
        """Check token field exists and is numeric/coercible."""
        actual = load_answer()
        assert q_key in actual, f"Answer does not contain {q_key}. Got {actual}"
        assert "tokens" in actual[q_key], f"Missing 'tokens' in {q_key}. Got {actual[q_key]}"
        coerce_numeric_token(actual[q_key]["tokens"])
