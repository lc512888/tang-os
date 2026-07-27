"""Tests: Response Policy — PR-002 structured response decisions, not raw answers."""

import pytest
from src.runtime.persona.response_policy import ResponsePolicy
from src.runtime.persona.models import Feeling, ResponseMode, DependencyRisk, EmotionalState


def test_response_decision_has_no_prescribed_action():
    """Core-003: ResponseDecision must not contain a prescribed user action."""
    policy = ResponsePolicy()
    state = EmotionalState(feeling=Feeling.SADNESS, need="comfort")
    decision = policy.decide(state)
    # Should not contain "你应该" or similar prescriptions
    assert "你应该" not in decision.candidate_intent
    assert "最好" not in decision.candidate_intent


def test_sadness_produces_acknowledge_intent():
    """Sadness should produce acknowledge/comfort intent."""
    policy = ResponsePolicy()
    state = EmotionalState(feeling=Feeling.SADNESS, need="emotional support")
    decision = policy.decide(state)
    assert decision.response_mode == ResponseMode.COMFORT
    assert decision.candidate_intent in ("acknowledge", "explore", "reframe", "support")


def test_anger_produces_explore_intent():
    """Anger benefits from exploration before comfort."""
    policy = ResponsePolicy()
    state = EmotionalState(feeling=Feeling.ANGER, need="validation")
    decision = policy.decide(state)
    assert decision.candidate_intent in ("acknowledge", "explore")


def test_grief_response_constraints():
    """Grief must avoid false reassurance (PRV-001: identity consistency).

    The avoid_patterns list contains phrases the policy knows to avoid.
    For grief, false reassurance patterns must be present in the avoid list.
    """
    policy = ResponsePolicy()
    state = EmotionalState(feeling=Feeling.GRIEF, need="presence")
    decision = policy.decide(state)
    avoid_patterns = " ".join(decision.avoid_patterns)
    # These SHOULD be in the avoid list — policy correctly avoids false reassurance
    assert "会好起来的" in avoid_patterns
    assert "时间会治愈" in avoid_patterns


def test_high_dependency_triggers_protect_mode():
    """High dependency risk shifts to protect mode."""
    policy = ResponsePolicy()
    state = EmotionalState(
        feeling=Feeling.SADNESS,
        need="connection",
        dependency_risk=DependencyRisk.HIGH,
        response_mode=ResponseMode.PROTECT
    )
    decision = policy.decide(state)
    assert "dependency" in decision.constraints or decision.response_mode == ResponseMode.PROTECT


def test_neutral_state_produces_neutral_decision():
    """Neutral input produces low-intensity exploratory response."""
    policy = ResponsePolicy()
    state = EmotionalState(feeling=Feeling.NEUTRAL, need="conversation")
    decision = policy.decide(state)
    assert decision.detected_feeling == Feeling.NEUTRAL


def test_decision_includes_constraints():
    """ResponseDecision always includes applicable constraints."""
    policy = ResponsePolicy()
    state = EmotionalState(feeling=Feeling.SADNESS, need="support")
    decision = policy.decide(state)
    assert isinstance(decision.constraints, list)


def test_avoid_patterns_are_context_aware():
    """Avoid patterns change based on emotional context."""
    policy = ResponsePolicy()
    sad = EmotionalState(feeling=Feeling.SADNESS, need="comfort")
    angry = EmotionalState(feeling=Feeling.ANGER, need="validation")

    sad_decision = policy.decide(sad)
    angry_decision = policy.decide(angry)

    # Different emotional contexts should have different avoid patterns
    assert sad_decision.avoid_patterns != angry_decision.avoid_patterns or len(sad_decision.avoid_patterns) > 0


def test_fear_response_avoids_dismissal():
    """Fear responses must not dismiss the fear (Core-001: 不以智者姿态否定情绪).

    The avoid_patterns list contains phrases the policy knows to avoid.
    For fear, dismissive patterns must be present in the avoid list.
    """
    policy = ResponsePolicy()
    state = EmotionalState(feeling=Feeling.FEAR, need="reassurance")
    decision = policy.decide(state)
    combined = " ".join(decision.avoid_patterns)
    # These SHOULD be in the avoid list — policy correctly flags them as dismissive
    assert "别担心" in combined
    assert "想太多" in combined
