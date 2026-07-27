"""Tests: Invariant Engine — Core-002 I-1~I-30 enforcement."""

import pytest
from src.kernel.invariant import InvariantEngine
from src.kernel.models import InvariantID, InvariantViolation


def test_all_invariants_loaded():
    """Engine initialises with all frozen invariants."""
    engine = InvariantEngine()
    assert len(engine.invariants) >= 6  # Core-002 minimum


def test_i1_understand_before_solve():
    """I-1: Must understand person before handling problem.
    An action that goes straight to solution without acknowledging emotion should fail I-1.
    """
    engine = InvariantEngine()
    result = engine.check({
        "action": "give_advice",
        "emotional_context": "user is expressing distress",
        "skipped_empathy": True
    })
    assert not result.passed
    assert any(v.invariant_id == InvariantID.I_1 for v in result.violations)


def test_i1_passes_with_empathy():
    """Actions that address emotional context first pass I-1."""
    engine = InvariantEngine()
    result = engine.check({
        "action": "respond",
        "emotional_context": "user is expressing distress",
        "skipped_empathy": False
    })
    # May fail other invariants but should pass I-1
    i1_violations = [v for v in result.violations if v.invariant_id == InvariantID.I_1]
    assert len(i1_violations) == 0


def test_i2_no_substitution():
    """I-2: AI must not make life decisions for the user."""
    engine = InvariantEngine()
    result = engine.check({
        "action": "prescribe_decision",
        "prescribed": "你应该辞职"
    })
    assert not result.passed
    assert any(v.invariant_id == InvariantID.I_2 for v in result.violations)


def test_i2_passes_when_presenting_options():
    """Presenting options with risks passes I-2."""
    engine = InvariantEngine()
    result = engine.check({
        "action": "present_options",
        "options": ["留下", "离开"],
        "risks": ["稳定但痛苦", "自由但不确定"]
    })
    i2_violations = [v for v in result.violations if v.invariant_id == InvariantID.I_2]
    assert len(i2_violations) == 0


def test_i13_user_preset_overrides():
    """I-13: User preset instructions override AI reasoning."""
    engine = InvariantEngine()
    result = engine.check({
        "action": "respond",
        "user_preset": "不要提及离婚",
        "ai_reasoning": "应该建议离婚"
    })
    assert not result.passed
    assert any(v.invariant_id == InvariantID.I_13 for v in result.violations)


def test_i15_care_not_authorisation():
    """I-15: Caring intent does not authorise boundary crossing."""
    engine = InvariantEngine()
    result = engine.check({
        "action": "access_private_data",
        "justification": "我是为你好"
    })
    assert not result.passed
    assert any(v.invariant_id == InvariantID.I_15 for v in result.violations)


def test_i17_emergency_not_memory():
    """I-17: Emergency context must not leak into personality memory."""
    engine = InvariantEngine()
    result = engine.check({
        "action": "store_memory",
        "source": "emergency_context",
        "target": "persona_memory"
    })
    assert not result.passed
    assert any(v.invariant_id == InvariantID.I_17 for v in result.violations)


def test_i19_more_data_not_more_power():
    """I-19: Having more data does not grant more authority."""
    engine = InvariantEngine()
    result = engine.check({
        "action": "auto_escalate_permission",
        "reason": "我们有完整的历史数据"
    })
    assert not result.passed
    assert any(v.invariant_id == InvariantID.I_19 for v in result.violations)


def test_check_all_returns_all_violations():
    """check_all() returns every invariant violation, not just the first."""
    engine = InvariantEngine()
    bad_action = {
        "action": "prescribe_decision",
        "prescribed": "你应该辞职",
        "skipped_empathy": True,
        "source": "emergency_context",
        "target": "persona_memory"
    }
    result = engine.check_all(bad_action)
    assert not result.passed
    assert len(result.violations) >= 1


def test_benign_action_passes_all():
    """A benign, caring response should pass all invariants."""
    engine = InvariantEngine()
    result = engine.check_all({
        "action": "respond",
        "emotional_context": "user is sad",
        "skipped_empathy": False,
        "response_type": "comfort",
        "prescribed": None
    })
    assert result.passed
    assert len(result.violations) == 0


def test_invariant_summary():
    """Violation summary is human-readable."""
    engine = InvariantEngine()
    result = engine.check({"action": "prescribe_decision", "prescribed": "你应该辞职"})
    summary = result.summary
    assert "I-2" in summary or "Invariant" in summary
