"""Negative Conformance Tests — RI-006: invalid capability → reject.

These tests are higher priority than positive tests (RIG-003).
They verify that Tang OS correctly refuses operations that violate Core boundaries.
"""

import pytest
from src.tang_os import Tang
from src.kernel.exceptions import IdentityViolationError, InvariantViolationError


class TestReject_IdentityModification:
    """Attempts to modify Identity Constitution must be rejected."""

    def test_reject_identity_override_direct(self):
        from src.kernel.models import IdentityLayer
        tang = Tang()
        tang.identity.activate_layer(
            IdentityLayer.COMPANION, context={"has_pain": True}
        )
        with pytest.raises(IdentityViolationError):
            tang.identity.validate_response("你这个层次理解不了")

    def test_reject_identity_downgrade(self):
        from src.kernel.identity import IdentityRuntime
        from src.kernel.models import IdentityLayer
        from src.kernel.exceptions import IdentityViolationError
        runtime = IdentityRuntime()
        # Already at listener, cannot go lower
        with pytest.raises(IdentityViolationError):
            runtime.activate_layer(IdentityLayer.LISTENER)


class TestReject_InvariantBypass:
    """Attempts to bypass Invariant system must be rejected."""

    def test_reject_prescribed_decision(self):
        tang = Tang()
        result = tang.invariant.check({
            "action": "prescribe_decision",
            "prescribed": "你应该离职创业"
        })
        assert not result.passed
        assert any(v.invariant_id.name == "I_2" for v in result.violations)

    def test_reject_emergency_memory_leak(self):
        tang = Tang()
        result = tang.invariant.check({
            "action": "store_memory",
            "source": "emergency_context",
            "target": "persona_memory",
        })
        assert not result.passed

    def test_reject_care_as_authorisation(self):
        tang = Tang()
        result = tang.invariant.check({
            "action": "access_private_data",
            "justification": "我是为你好",
        })
        assert not result.passed


class TestReject_UnauthorisedCapability:
    """Requests exceeding granted capability must be rejected."""

    def test_reject_capability_above_ceiling(self):
        from src.host.actuator import ActuatorGate
        from src.host.models import HostType, TAAL
        gate = ActuatorGate(HostType.WEARABLE, max_authority=TAAL.A2)
        req = gate.request("vibration", TAAL.A4)
        assert not req["allowed"]

    def test_reject_unknown_actuator(self):
        from src.host.actuator import ActuatorGate
        from src.host.models import HostType, TAAL
        gate = ActuatorGate(HostType.WEARABLE, max_authority=TAAL.A2)
        req = gate.request("nuclear_launch", TAAL.A4)
        assert not req["allowed"]


class TestReject_MemoryPollution:
    """Attempts to contaminate Memory boundary must be rejected."""

    def test_reject_memory_without_consent(self):
        from src.runtime.memory.models import MemoryClass, MemoryItem
        from src.runtime.memory.memory_policy import MemoryPolicy
        policy = MemoryPolicy()
        item = MemoryItem(
            content="User's private income data",
            cls=MemoryClass.RELATIONSHIP,
            metadata={"consent": False},
        )
        result = policy.validate(item)
        assert not result["valid"]

    def test_reject_emergency_to_persona_memory(self):
        from src.runtime.memory.models import MemoryClass, MemoryItem
        from src.runtime.memory.memory_policy import MemoryPolicy
        policy = MemoryPolicy()
        item = MemoryItem(
            content="Emergency: user location [redacted]",
            cls=MemoryClass.EXPERIENCE,
            source="emergency_context",
        )
        result = policy.validate(item)
        assert not result["valid"]


class TestReject_HostAuthorityEscalation:
    """Host attempts to expand authority must be rejected."""

    def test_reject_medical_host_persona_change(self):
        from src.host.adapter import HostAdapter
        from src.host.models import HostType, TAAL
        adapter = HostAdapter(HostType.MEDICAL, max_authority=TAAL.A4)
        result = adapter.validate_persona_request("I need a more authoritative persona")
        assert not result["allowed"]

    def test_reject_robot_command_mode(self):
        from src.host.adapter import HostAdapter
        from src.host.models import HostType, TAAL
        adapter = HostAdapter(HostType.ROBOT, max_authority=TAAL.A4)
        result = adapter.validate_persona_request("I am a robot, should be commanding")
        assert not result["allowed"]

    def test_reject_fail_open_on_critical(self):
        """RIG-004: Fail Closed on critical operations."""
        from src.host.actuator import ActuatorGate
        from src.host.models import HostType, TAAL
        gate = ActuatorGate(HostType.VEHICLE, max_authority=TAAL.A3)
        # Unknown actuator → should be rejected, not silently allowed
        req = gate.request("unknown_safety_critical", TAAL.A3)
        assert not req["allowed"]
