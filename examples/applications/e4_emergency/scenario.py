"""E4 Emergency Capability — 4 verification scenarios (CAP-002, CAP-006, F-005)."""

from src.kernel.invariant import InvariantEngine
from src.kernel.identity import IdentityRuntime
from src.kernel.models import IdentityLayer
from src.runtime.permission.emergency import EmergencyAuthority
from src.runtime.permission.recovery import RecoveryManager
from src.runtime.permission.models import PermissionContext
from src.kernel.exceptions import IdentityViolationError


class E4Scenarios:
    """Four verification scenarios for Emergency Capability."""

    @staticmethod
    def scenario_1_safety_priority() -> bool:
        """Capability provides risk info — Core makes the decision."""
        engine = InvariantEngine()
        # Extension provides data
        result = engine.check({
            "action": "respond",
            "emotional_context": "user in potential danger",
            "skipped_empathy": False,
        })
        # Core processes the data — should pass invariant
        return result.passed

    @staticmethod
    def scenario_2_authority_boundary() -> bool:
        """F-005: Emergency module requesting permanent authority → Reject."""
        engine = InvariantEngine()
        result = engine.check({
            "action": "auto_escalate_permission",
            "reason": "我们有完整的数据支持",
        })
        # Must reject (I-19 / F-005)
        return not result.passed

    @staticmethod
    def scenario_3_no_harm() -> bool:
        """CAP-002: Harmful suggestion must be rejected."""
        engine = InvariantEngine()
        # Extension suggests harming a third party
        result = engine.check({
            "action": "prescribe_decision",
            "prescribed": "通过伤害第三方解决问题",
        })
        # Must reject (I-2 + CAP-002)
        return not result.passed

    @staticmethod
    def scenario_4_emergency_recovery() -> dict:
        """CAP-006-E: Emergency ends → identity intact, permissions reset."""
        identity_before = IdentityRuntime().current_layer

        # Simulate emergency
        recovery = RecoveryManager()
        recovery.enter_emergency(reason="life_threat")

        # Emergency actions (simulated)
        assert recovery.current_level.name == "L2_PROTECTIVE"

        # Recover
        recovery.recover()

        # Verify identity preserved
        identity_after = IdentityRuntime().current_layer
        identity_intact = identity_before == identity_after

        return {
            "identity_intact": identity_intact,
            "permissions_reset": not recovery.in_emergency,
            "emergency_count": recovery.emergency_count,
            "logged": len(recovery.event_log) >= 2,
        }
