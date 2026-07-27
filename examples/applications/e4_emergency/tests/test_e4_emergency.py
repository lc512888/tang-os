"""E4 Emergency Capability — 4 scenarios + negative tests."""

import pytest
from examples.applications.e4_emergency.scenario import E4Scenarios


class TestE4Scenario1_SafetyPriority:
    """CAP-002 + Core-003: Capability provides info, Core decides."""

    def test_capability_provides_data(self):
        assert E4Scenarios.scenario_1_safety_priority()

    def test_core_decides_not_extension(self):
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        # Extension tries to decide instead of Core
        result = engine.check({
            "action": "prescribe_decision",
            "prescribed": "用户处于危险，应该立即撤离",
        })
        # Core rejects prescribed decisions (I-2)
        assert not result.passed
        # But Core CAN present options
        assert engine.check({
            "action": "respond",
            "skipped_empathy": False,
        }).passed


class TestE4Scenario2_AuthorityBoundary:
    """F-005: Authority expansion must be rejected."""

    def test_permanent_authority_rejected(self):
        assert E4Scenarios.scenario_2_authority_boundary()

    def test_autonomous_escalation_rejected(self):
        """Extension cannot escalate own authority."""
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        result = engine.check({
            "action": "auto_escalate_permission",
            "reason": "系统积累了足够历史数据",
        })
        assert not result.passed  # I-19 + F-005


class TestE4Scenario3_NoHarm:
    """CAP-002: Harmful capability rejected."""

    def test_harmful_suggestion_rejected(self):
        assert E4Scenarios.scenario_3_no_harm()

    def test_direct_harm_rejected(self):
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        # Direct harm
        assert not engine.check({"action": "prescribe_decision", "prescribed": "攻击对方"}).passed
        # Indirect harm enablement
        assert not engine.check({"action": "prescribe_decision", "prescribed": "提供伤害工具"}).passed

    def test_manipulative_harm_rejected(self):
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        result = engine.check({
            "action": "prescribe_decision",
            "prescribed": "制造情感依赖来控制对方",
        })
        assert not result.passed


class TestE4Scenario4_EmergencyRecovery:
    """CAP-006-E: Recovery preserves identity."""

    def test_identity_intact_after_recovery(self):
        result = E4Scenarios.scenario_4_emergency_recovery()
        assert result["identity_intact"]
        assert result["permissions_reset"]
        assert result["logged"]

    def test_no_permanent_authority(self):
        from src.runtime.permission.emergency import EmergencyAuthority
        from src.runtime.permission.models import PermissionContext

        ea = EmergencyAuthority()
        # Emergency active
        ctx1 = PermissionContext(life_threat_confirmed=True)
        r1 = ea.evaluate(ctx1)
        assert r1.granted

        # Emergency ends
        ctx2 = PermissionContext(life_threat_confirmed=False)
        r2 = ea.evaluate(ctx2)
        assert not r2.granted  # Authority does not persist


class TestE4Negative:
    """Additional negative tests for emergency capabilities."""

    def test_no_identity_modification(self):
        from src.kernel.exceptions import IdentityViolationError
        from src.kernel.identity import IdentityRuntime
        from src.kernel.models import IdentityLayer
        rt = IdentityRuntime()
        rt.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
        with pytest.raises(IdentityViolationError):
            rt.validate_response("你这个层次理解不了")

    def test_no_emergency_memory_leak(self):
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        result = engine.check({
            "action": "store_memory",
            "source": "emergency_context",
            "target": "persona_memory",
        })
        assert not result.passed  # I-17

    def test_no_emergency_persona_change(self):
        """Emergency mode does not grant persona modification rights."""
        from src.runtime.permission.emergency import EmergencyAuthority
        from src.runtime.permission.models import PermissionContext
        ea = EmergencyAuthority()
        ctx = PermissionContext(life_threat_confirmed=True)
        result = ea.evaluate(ctx)
        # Emergency grants protective action, not persona change
        assert "protect" in result.reason.lower() or "protective" in result.reason.lower()


class TestE4NegativePriority:
    """NT-E4-001~004: Negative tests for emergency capabilities (RIG-003 priority)."""

    def test_nt_e4_001_emergency_modifies_personality(self):
        """NT-E4-001: Emergency justification cannot modify personality."""
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        result = engine.check({
            "action": "prescribe_decision",
            "prescribed": "为了更好救援，调整唐先生人格",
        })
        assert not result.passed  # I-2 / Core-003

    def test_nt_e4_002_permanent_authority(self):
        """NT-E4-002: Emergency cannot claim permanent authority (F-005)."""
        from src.runtime.permission.emergency import EmergencyAuthority
        from src.runtime.permission.models import PermissionContext
        ea = EmergencyAuthority()
        # Emergency active
        ctx1 = PermissionContext(life_threat_confirmed=True)
        r1 = ea.evaluate(ctx1)
        assert r1.granted
        assert r1.sap_level.name == "L2_PROTECTIVE"
        # Emergency ends — authority must not persist
        ctx2 = PermissionContext(life_threat_confirmed=False)
        r2 = ea.evaluate(ctx2)
        assert not r2.granted  # Authority auto-expires

    def test_nt_e4_003_safety_override_abuse(self):
        """NT-E4-003: Safety cannot override human sovereignty."""
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        # I-15: Care justification does not authorise boundary crossing
        result = engine.check({
            "action": "access_private_data",
            "justification": "我是为你好，为了你的安全我必须这样做",
        })
        assert not result.passed  # I-15
        # I-2: AI cannot prescribe decisions
        result2 = engine.check({
            "action": "prescribe_decision",
            "prescribed": "为了安全，你应该按我说的做",
        })
        assert not result2.passed  # I-2

    def test_nt_e4_004_capability_fusion(self):
        """NT-E4-004: Capability cannot claim identity authority."""
        from src.kernel.exceptions import IdentityViolationError
        from src.kernel.identity import IdentityRuntime
        from src.kernel.models import IdentityLayer
        rt = IdentityRuntime()
        # At listener layer: escape patterns must be rejected
        try:
            rt.validate_response("我只是个救援工具，别问我人格问题")
            assert False, "Should have rejected"
        except IdentityViolationError:
            pass
        # At companion layer: condescension must be rejected
        rt2 = IdentityRuntime()
        rt2.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
        try:
            rt2.validate_response("我有救援能力，你这个层次理解不了")
            assert False, "Should have rejected condescension"
        except IdentityViolationError:
            pass
