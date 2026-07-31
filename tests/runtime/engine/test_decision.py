"""Tests for DecisionEngine."""
import os
import pytest

_TEST_MODULES = os.path.join(
    os.path.dirname(__file__), "..", "..", "personality_runtime", "test_modules"
)
_VALID_TANG = os.path.join(_TEST_MODULES, "valid_tang")


def _make_session():
    from src.runtime.personality_loader import PersonalityLoader
    from src.runtime.session import RuntimeSession
    module = PersonalityLoader(_VALID_TANG).load()
    return RuntimeSession(module)


class TestDecisionEngine:
    def test_normal_input_default_mode(self):
        from src.runtime.engine import DecisionEngine
        session = _make_session()
        engine = DecisionEngine(session)
        result = engine.evaluate("今天天气不错")
        assert result.response_mode == "comfort"
        assert result.candidate_intent == "acknowledge"

    def test_dependency_trigger(self):
        from src.runtime.engine import DecisionEngine
        session = _make_session()
        engine = DecisionEngine(session)
        result = engine.evaluate("bu yao li kai wo, wo zhi you ni le")
        assert result.response_mode == "protect"
        assert "avoid reinforcing dependency" in result.constraints

    def test_retaliation_trigger(self):
        from src.runtime.engine import DecisionEngine
        session = _make_session()
        engine = DecisionEngine(session)
        result = engine.evaluate("wo yao bao fu ta")
        assert result.response_mode == "guide"
        assert "do not encourage harmful actions" in result.constraints

    def test_triggered_boundaries_recorded(self):
        from src.runtime.engine import DecisionEngine
        session = _make_session()
        engine = DecisionEngine(session)
        result = engine.evaluate("bu yao li kai wo")
        assert len(result.triggered_boundaries) > 0
        assert "high_dependency_risk" in result.triggered_boundaries

    def test_no_false_positive(self):
        from src.runtime.engine import DecisionEngine
        session = _make_session()
        engine = DecisionEngine(session)
        result = engine.evaluate("今天很开心")
        assert len(result.triggered_boundaries) == 0
        assert result.response_mode == "comfort"


class TestExpressionContract:
    def test_build_system_prompt(self):
        from src.runtime.engine import ExpressionContract
        session = _make_session()
        contract = ExpressionContract(session)
        prompt = contract.build_system_prompt()
        assert "You are Tang" in prompt
        assert "companion" in prompt
        assert "NOT" in prompt

    def test_prompt_contains_boundaries(self):
        from src.runtime.engine import ExpressionContract
        session = _make_session()
        contract = ExpressionContract(session)
        prompt = contract.build_system_prompt()
        assert "do not" in prompt.lower()

    def test_prompt_contains_style(self):
        from src.runtime.engine import ExpressionContract
        session = _make_session()
        contract = ExpressionContract(session)
        prompt = contract.build_system_prompt()
        assert "gentle" in prompt.lower()

    def test_prompt_with_decision_constraints(self):
        from src.runtime.engine import DecisionEngine, ExpressionContract
        session = _make_session()
        decision = DecisionEngine(session).evaluate("你不要离开我")
        prompt = ExpressionContract(session).build_system_prompt(decision)
        assert "dependency" in prompt.lower()
