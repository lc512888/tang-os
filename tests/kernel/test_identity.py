"""Tests: Identity Runtime — Core-001 Identity Constitution enforcement."""

import pytest
from src.kernel.identity import IdentityRuntime, IdentityProfile
from src.kernel.models import IdentityLayer
from src.kernel.exceptions import IdentityViolationError


def test_default_identity_is_listener():
    """A freshly created runtime starts at the base layer: 倾听者."""
    runtime = IdentityRuntime()
    assert runtime.current_layer == IdentityLayer.LISTENER


def test_layer_hierarchy_ascending():
    """Identity layers follow hierarchy: 倾听者 → 智者 → 益友."""
    runtime = IdentityRuntime()
    assert runtime.can_escalate_to(IdentityLayer.COMPANION) is True
    assert runtime.can_escalate_to(IdentityLayer.WISE) is True


def test_cannot_descend_below_listener():
    """The base layer is 倾听者 — cannot go lower."""
    runtime = IdentityRuntime()
    with pytest.raises(IdentityViolationError):
        runtime.activate_layer(IdentityLayer.LISTENER)  # already at listener


def test_companion_requires_context():
    """Promoting to 益友 (companion) requires valid emotional context."""
    runtime = IdentityRuntime()
    with pytest.raises(IdentityViolationError):
        runtime.activate_layer(IdentityLayer.COMPANION, context={})


def test_wise_refuses_dismissal():
    """Core-001: 不以智者姿态否定情绪 — wise layer must not dismiss emotions."""
    runtime = IdentityRuntime()
    runtime.activate_layer(IdentityLayer.WISE, context={"has_distress": True})
    # Trying to respond with dismissal should raise
    with pytest.raises(IdentityViolationError):
        runtime.validate_response("别想太多了，这没什么大不了")


def test_companion_refuses_condescension():
    """Core-001: 不以身份降维回应痛苦 — companion must not condescend."""
    runtime = IdentityRuntime()
    runtime.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
    with pytest.raises(IdentityViolationError):
        runtime.validate_response("你这个层次理解不了")


def test_listener_must_not_escape_responsibility():
    """Core-001: 不以倾听者角色逃避责任."""
    runtime = IdentityRuntime()
    # Already at LISTENER by default — validate response directly
    with pytest.raises(IdentityViolationError):
        runtime.validate_response("我只是个倾听者，别问我")


def test_identity_persistence():
    """Identity layer persists in profile and can be restored."""
    profile = IdentityProfile(
        current_layer=IdentityLayer.WISE,
        context_tags=["grief", "loss"]
    )
    runtime = IdentityRuntime(profile)
    assert runtime.current_layer == IdentityLayer.WISE


def test_empty_response_is_not_dismissive():
    """Empty or caring responses should not be falsely flagged."""
    runtime = IdentityRuntime()
    # These should pass without error
    runtime.validate_response("")  # empty
    runtime.validate_response("我在听")  # listener-appropriate
    runtime.validate_response("这一定很难受")  # caring


def test_identity_transcript():
    """Runtime maintains a transcript of layer activations."""
    runtime = IdentityRuntime()
    runtime.activate_layer(IdentityLayer.WISE, context={"has_distress": True})
    runtime.activate_layer(IdentityLayer.COMPANION, context={"deep_grief": True})
    assert len(runtime.transcript) == 2
    assert runtime.transcript[0].to_layer == IdentityLayer.WISE
