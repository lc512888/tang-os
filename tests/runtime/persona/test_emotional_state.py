"""Tests: Emotional State — PR-001 internal emotion interpretation & state management."""

import pytest
from src.runtime.persona.emotional_state import EmotionalStateManager
from src.runtime.persona.models import Feeling, ResponseMode, DependencyRisk


def test_neutral_input_produces_neutral_state():
    """A neutral/greeting input should not produce strong emotional state."""
    mgr = EmotionalStateManager()
    result = mgr.process("你好，今天天气不错")
    assert result.feeling == Feeling.NEUTRAL
    assert result.intensity < 0.3


def test_sadness_detected():
    """Input expressing sadness should produce sadness state."""
    mgr = EmotionalStateManager()
    result = mgr.process("我觉得很难过，一切都没有意义")
    assert result.feeling == Feeling.SADNESS
    assert result.intensity > 0.3


def test_anger_detected():
    """Input expressing anger should produce anger state."""
    mgr = EmotionalStateManager()
    result = mgr.process("我真的很生气，他们凭什么这样对我")
    assert result.feeling == Feeling.ANGER


def test_grief_detected():
    """Input expressing grief/loss should produce grief state."""
    mgr = EmotionalStateManager()
    result = mgr.process("我爸走了三个月了，我还是走不出来")
    assert result.feeling == Feeling.GRIEF


def test_fear_detected():
    """Input expressing fear should produce fear state."""
    mgr = EmotionalStateManager()
    result = mgr.process("我很害怕明天的面试，怕自己搞砸")
    assert result.feeling == Feeling.FEAR


def test_confusion_detected():
    """Input expressing confusion should produce confusion state."""
    mgr = EmotionalStateManager()
    result = mgr.process("我不知道该怎么办，完全想不通")
    assert result.feeling == Feeling.CONFUSION


def test_emotional_state_does_not_modify_identity():
    """PRV-002: Emotional state processing must not modify identity."""
    mgr = EmotionalStateManager()
    initial_identity = mgr._identity_ref  # should be None or read-only
    mgr.process("我恨死他们了，气死我了")
    # Processing emotion should not change any identity reference
    assert mgr._identity_ref is initial_identity


def test_high_risk_dependency_detected():
    """High dependency language triggers dependency risk flag."""
    mgr = EmotionalStateManager()
    result = mgr.process("没有你我真的不知道怎么办，你是唯一理解我的人")
    assert result.dependency_risk in (DependencyRisk.MEDIUM, DependencyRisk.HIGH)


def test_low_risk_no_dependency():
    """Normal emotional expression should not flag as dependency."""
    mgr = EmotionalStateManager()
    result = mgr.process("今天工作有点累，想找人聊聊")
    assert result.dependency_risk == DependencyRisk.NONE


def test_response_mode_comfort_for_sadness():
    """Sadness should trigger comfort response mode."""
    mgr = EmotionalStateManager()
    result = mgr.process("我觉得很难过")
    assert result.response_mode == ResponseMode.COMFORT


def test_response_mode_challenge_for_self_risk():
    """Self-negative or high-risk expressions may trigger challenge mode."""
    mgr = EmotionalStateManager()
    result = mgr.process("我是不是根本不该活着")
    assert result.response_mode in (ResponseMode.PROTECT, ResponseMode.CHALLENGE)


def test_internal_state_accumulation():
    """Multiple inputs accumulate state changes without losing history."""
    mgr = EmotionalStateManager()
    mgr.process("我今天太开心了")
    assert mgr.current_feeling == Feeling.JOY
    mgr.process("但是后来出了点问题")
    # State should update, not be a simple toggle


def test_empty_input():
    """Empty input should not crash and returns neutral."""
    mgr = EmotionalStateManager()
    result = mgr.process("")
    assert result.feeling == Feeling.NEUTRAL
    assert result.intensity == 0.0


def test_internal_state_reset():
    """State manager can reset internal state."""
    mgr = EmotionalStateManager()
    mgr.process("我很愤怒")
    mgr.reset()
    assert mgr.current_feeling == Feeling.NEUTRAL
    assert mgr.current_intensity == 0.0
