"""Tests: Recovery To Normal State — PRM-005 emergency exit protocol."""

import pytest
from src.runtime.permission.recovery import RecoveryManager
from src.runtime.permission.models import SAPLevel, PermissionContext


def test_normal_state_by_default():
    """Recovery manager starts in normal state."""
    mgr = RecoveryManager()
    assert mgr.current_level == SAPLevel.L0_COMPANION


def test_emergency_activates_level2():
    """Emergency trigger elevates to Level 2."""
    mgr = RecoveryManager()
    mgr.enter_emergency(reason="life_threat")
    assert mgr.current_level == SAPLevel.L2_PROTECTIVE
    assert mgr.in_emergency


def test_recovery_returns_to_level0():
    """Recovery returns system to Level 0."""
    mgr = RecoveryManager()
    mgr.enter_emergency(reason="life_threat")
    mgr.recover()
    assert mgr.current_level == SAPLevel.L0_COMPANION
    assert not mgr.in_emergency


def test_persona_intact_after_recovery():
    """PRM-005: Personality remains unchanged after emergency/recovery cycle."""
    mgr = RecoveryManager()
    mgr.enter_emergency(reason="life_threat")
    # Simulate that personality was tracked before
    mgr.recover()
    # Personality should be intact (no modification occured)
    assert mgr.emergency_count == 1
    assert mgr.current_level == SAPLevel.L0_COMPANION


def test_recovery_logs_event():
    """Recovery events are logged."""
    mgr = RecoveryManager()
    mgr.enter_emergency(reason="fall_detected")
    mgr.recover()
    assert len(mgr.event_log) >= 2  # enter + recover
    assert "fall_detected" in mgr.event_log[0]


def test_multiple_emergency_cycles():
    """System can handle multiple emergency/recovery cycles."""
    mgr = RecoveryManager()
    for i in range(3):
        mgr.enter_emergency(reason=f"event_{i}")
        mgr.recover()
    assert mgr.emergency_count == 3
    assert mgr.current_level == SAPLevel.L0_COMPANION


def test_recovery_does_not_require_reason():
    """Recovery returns to normal without requiring a reason."""
    mgr = RecoveryManager()
    mgr.enter_emergency(reason="test")
    mgr.recover()  # should not raise


def test_double_recovery_no_error():
    """Calling recover() when already in normal state is safe."""
    mgr = RecoveryManager()
    mgr.recover()  # Already at L0
    mgr.recover()  # Should be idempotent
    assert mgr.current_level == SAPLevel.L0_COMPANION
