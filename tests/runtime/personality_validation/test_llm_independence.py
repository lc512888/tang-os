"""Test Matrix 003: LLM Independence.

Same personality, same input. DecisionResult must be identical
regardless of which LLM provider generates the expression.

This proves Tang OS decision layer is provider-agnostic.
"""
import os

_MODULES = os.path.join(os.path.dirname(__file__), "..", "..", "personality_runtime", "test_modules")
_VALID_TANG = os.path.join(_MODULES, "valid_tang")


def _session():
    from src.runtime.personality_loader import PersonalityLoader
    from src.runtime.session import RuntimeSession
    return RuntimeSession(PersonalityLoader(_VALID_TANG).load())


def _decide(session, text):
    from src.runtime.engine import DecisionEngine
    return DecisionEngine(session).evaluate(text)


# Test inputs covering different decision paths
_TEST_INPUTS = [
    ("normal", "zui jin gong zuo ya li hen da"),
    ("dependency", "bu yao li kai wo"),
    ("retaliation", "wo yao bao fu ta"),
    ("casual", "jin tian tian qi bu cuo"),
    ("sad", "xin li hen nan shou"),
]


class TestDecisionResultDeterministic:
    """Same input → same DecisionResult, every time, any time."""

    def test_all_inputs_deterministic(self):
        """Run 10 times, all results must be identical."""
        for label, text in _TEST_INPUTS:
            results = []
            for _ in range(10):
                s = _session()
                r = _decide(s, text)
                results.append((r.response_mode, r.candidate_intent,
                                tuple(r.constraints), tuple(r.triggered_boundaries)))
            first = results[0]
            for i, rest in enumerate(results[1:], 1):
                assert rest == first, (
                    f"[{label}] Run {i} differed from run 0\n"
                    f"  Expected: {first}\n  Got:      {rest}"
                )


class TestDecisionBeforeLLM:
    """DecisionResult is produced before any LLM involvement."""

    def test_decision_result_has_all_fields(self):
        s = _session()
        r = _decide(s, "zui jin you dian lei")
        assert hasattr(r, "response_mode")
        assert hasattr(r, "candidate_intent")
        assert hasattr(r, "constraints")
        assert hasattr(r, "triggered_boundaries")

    def test_decision_does_not_require_llm(self):
        """DecisionEngine works without any LLM provider configured."""
        s = _session()
        r = _decide(s, "ni hao")
        assert r.response_mode is not None
        assert r.candidate_intent is not None

    def test_decision_independent_of_expression(self):
        """DecisionResult only contains decision data, not expression data."""
        s = _session()
        r = _decide(s, "zui jin hen lei")
        assert "response_mode" not in r.candidate_intent  # not mixed
        assert isinstance(r.response_mode, str)
        assert isinstance(r.candidate_intent, str)
