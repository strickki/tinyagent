"""Chapter 3 — reasoning through prompting (exercises, not agent code)."""

from collections import Counter

import pytest

from my_agent.exercises.ch03 import (
    COT_TRIGGER,
    best_of_n,
    extract_answer,
    few_shot_messages,
    self_consistency,
    verify,
    zero_shot_cot,
)

pytestmark = pytest.mark.chapter(3)


# ── Few-shot and zero-shot chain-of-thought ──────────────────────────────────


def test_few_shot_alternates_user_and_assistant_then_asks():
    messages = few_shot_messages([("6 - 2 - 1?", "3"), ("1 + 1?", "2")], "9 - 2 + 4?")
    assert messages == [
        {"role": "user", "content": "6 - 2 - 1?"},
        {"role": "assistant", "content": "3"},
        {"role": "user", "content": "1 + 1?"},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "9 - 2 + 4?"},
    ]


def test_few_shot_with_no_examples_is_just_the_query():
    assert few_shot_messages([], "q") == [{"role": "user", "content": "q"}]


def test_zero_shot_cot_appends_the_trigger():
    assert zero_shot_cot("How many?") == "How many? Let's think step by step."
    assert COT_TRIGGER == " Let's think step by step."


# ── Self-consistency ─────────────────────────────────────────────────────────


def test_extract_answer_takes_text_after_the_last_marker():
    text = "Answer: maybe 1?\nWait, recheck.\nAnswer:\n Seat 5\n"
    assert extract_answer(text) == "Seat 5"


def test_extract_answer_without_marker_returns_cleaned_text():
    assert extract_answer("  just 5\n") == "just 5"


def test_extract_answer_custom_marker():
    assert extract_answer("so... Final: 42", marker="Final:") == "42"


def test_self_consistency_counts_answers(make_llm):
    llm = make_llm("...Answer: 5", "...Answer: 1", "...Answer: 5")
    votes = self_consistency(llm, "Where is Maarten?", n=3)
    assert votes == Counter({"5": 2, "1": 1})
    assert votes.most_common(1)[0][0] == "5"


def test_self_consistency_sends_the_query_each_time(make_llm):
    llm = make_llm("Answer: a", "Answer: b")
    self_consistency(llm, "puzzle", n=2)
    assert [c["messages"] for c in llm.calls] == [[{"role": "user", "content": "puzzle"}]] * 2


# ── Verifier + Best-of-N ─────────────────────────────────────────────────────

CASES = [("III", 3), ("IV", 4), ("", 0)]

GOOD = """
def roman_to_int(s):
    return {"III": 3, "IV": 4}.get(s, 0)
"""
HALF = """
def roman_to_int(s):
    return 3 if s == "III" else -1
"""


def test_verify_scores_fraction_passed():
    assert verify(GOOD, CASES) == 1.0
    assert verify(HALF, CASES) == pytest.approx(1 / 3)


def test_verify_scores_broken_code_zero():
    assert verify("def roman_to_int(s) return", CASES) == 0.0


def test_verify_scores_missing_function_zero():
    assert verify("def something_else(s): return 0", CASES) == 0.0


def test_verify_scores_crashing_function_zero():
    assert verify("def roman_to_int(s): raise ValueError", CASES) == 0.0


def test_verify_respects_fn_name():
    assert verify("def f(x): return x * 2", [(2, 4)], fn_name="f") == 1.0


def test_best_of_n_keeps_the_highest_scoring_candidate(make_llm):
    llm = make_llm("bad", "best", "ok")
    scores = {"bad": 0.1, "best": 0.9, "ok": 0.5}
    best, score, all_scores = best_of_n(llm, "write it", scores.get, n=3)
    assert (best, score) == ("best", 0.9)
    assert all_scores == [0.1, 0.9, 0.5]
    assert len(llm.calls) == 3
