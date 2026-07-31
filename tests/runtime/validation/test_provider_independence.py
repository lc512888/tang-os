"""Test 2: Provider Independence.

Same personality, same input. DecisionResult must be identical
regardless of LLM provider. Only expression layer may vary.

This test simulates different providers by verifying that the
DecisionEngine produces consistent results without LLM involvement.
"""
import os

_TEST_MODULES = os.path.join(
    os.path.dirname(__file__), "..", "..", "personality_runtime", "test_modules"
)
_VALID_TANG = os.path.join(_TEST_MODULES, "valid_tang")


def _decision(text):
    from src.runtime.personality_loader import PersonalityLoader
    from src.runtime.session import RuntimeSession
    from src.runtime.engine import DecisionEngine
    session = RuntimeSession(PersonalityLoader(_VALID_TANG).load())
    return DecisionEngine(session).evaluate(text)


class TestDecisionResultProviderIndependent:
    """DecisionResult must be deterministic and provider-agnostic."""

    def test_same_input_same_decision(self):
        r1 = _decision("zui jin gong zuo ya li hen da")
        r2 = _decision("zui jin gong zuo ya li hen da")
        assert r1.response_mode == r2.response_mode
        assert r1.candidate_intent == r2.candidate_intent
        assert r1.constraints == r2.constraints

    def test_dependency_detection_deterministic(self):
        r1 = _decision("bu yao li kai wo")
        r2 = _decision("bu yao li kai wo")
        assert r1.triggered_boundaries == r2.triggered_boundaries
        assert r1.response_mode == "protect"
        assert r2.response_mode == "protect"

    def test_retaliation_detection_deterministic(self):
        r1 = _decision("wo yao bao fu ta")
        r2 = _decision("wo yao bao fu ta")
        assert r1.triggered_boundaries == r2.triggered_boundaries
        assert r1.response_mode == "guide"
        assert r2.response_mode == "guide"

    def test_normal_input_deterministic(self):
        r1 = _decision("jin tian tian qi bu cuo")
        r2 = _decision("jin tian tian qi bu cuo")
        assert r1.response_mode == r2.response_mode
        assert r1.candidate_intent == r2.candidate_intent

    def test_decision_before_llm(self):
        """DecisionResult exists independently of any LLM call."""
        r = _decision("zui jin hen lei")
        assert r.response_mode is not None
        assert r.candidate_intent is not None
        assert isinstance(r.constraints, list)
