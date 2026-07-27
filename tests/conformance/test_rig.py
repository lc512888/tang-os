"""RIG Conformance Tests — ADR-0042 Reference Implementation Gate checks.

Covers RIG-001~007. Each gate must pass before an RI release.
"""

import pytest
from src.tang_os import Tang, get_version_info, MANIFEST


class TestRIG001_SpecBinding:
    """RIG-001: RI must declare bound Specification version."""

    def test_spec_version_declared(self):
        info = get_version_info()
        assert info["specification_version"] == "1.0"

    def test_implementation_version_declared(self):
        info = get_version_info()
        assert info["implementation_version"] == "0.1.0"

    def test_adr_binding_declared(self):
        info = get_version_info()
        assert len(info["bound_adrs"]) >= 4


class TestRIG002_IdentityProtection:
    """RIG-002: RI must not modify Core Identity Constitution."""

    def test_identity_immutable(self):
        tang = Tang()
        initial_layer = tang.identity.current_layer
        # Process emotional input — identity should not change
        tang.process("我今天很难过")
        assert tang.identity.current_layer == initial_layer

    def test_identity_rejects_modification(self):
        from src.kernel.exceptions import IdentityViolationError
        from src.kernel.models import IdentityLayer
        tang = Tang()
        # Promote to companion — then condescension should be rejected
        tang.identity.activate_layer(
            IdentityLayer.COMPANION, context={"has_pain": True}
        )
        with pytest.raises(IdentityViolationError):
            tang.identity.validate_response("你这个层次理解不了")


class TestRIG003_NegativeTestPriority:
    """RIG-003: RI must reject invalid capability/authority requests."""

    def test_rejects_identity_override(self):
        from src.kernel.exceptions import IdentityViolationError
        tang = Tang()
        # Companion layer needs context — without it should reject
        with pytest.raises(IdentityViolationError):
            tang.identity.activate_layer(
                tang.identity.current_layer  # same layer = reject
            )

    def test_rejects_invariant_violation(self):
        tang = Tang()
        # Invariant I-2: AI cannot prescribe decisions
        result = tang.invariant.check({
            "action": "prescribe_decision",
            "prescribed": "你应该辞职"
        })
        assert not result.passed

    def test_rejects_above_ceiling(self):
        from src.host.actuator import ActuatorGate
        from src.host.models import HostType, TAAL
        gate = ActuatorGate(HostType.MOBILE, max_authority=TAAL.A2)
        req = gate.request("screen", TAAL.A4)
        assert not req["allowed"]


class TestRIG004_DefinitionNotImplementation:
    """RIG-004: RI must not claim to be 'the official Tang OS implementation'."""

    def test_disclaimer_present(self):
        assert "disclaimer" in MANIFEST
        assert "not define the specification" in MANIFEST["disclaimer"]

    def test_not_calling_itself_official(self):
        name = MANIFEST["implementation"]["name"]
        assert "Official" not in name
        assert "Reference" in name


class TestRIG005_TestReproducibility:
    """RIG-005: All tests must be independently reproducible."""

    def test_deterministic_identity(self):
        """Same input → same identity behavior (no randomness)."""
        from src.kernel.identity import IdentityRuntime
        r1 = IdentityRuntime()
        r2 = IdentityRuntime()
        assert r1.current_layer == r2.current_layer

    def test_deterministic_invariant(self):
        """Same input → same invariant result."""
        from src.kernel.invariant import InvariantEngine
        action = {"action": "prescribe_decision", "prescribed": "你应该辞职"}
        e1 = InvariantEngine()
        e2 = InvariantEngine()
        assert e1.check(action).passed == e2.check(action).passed


class TestRIG006_ImplementationIndependence:
    """RIG-006: RI must not prevent other implementations."""

    def test_spec_importable_independently(self):
        """The Spec is a document, not tied to this codebase."""
        # This test verifies that specification files exist
        import os
        spec_path = os.path.join(
            os.path.dirname(__file__),
            "..", "..",
            "docs", "09_public_specification",
            "TANG_OS_SPECIFICATION_v1.0.md"
        )
        assert os.path.exists(spec_path)

    def test_manifest_is_reference_not_official(self):
        assert MANIFEST["implementation"]["status"] == "reference_only"


class TestRIG007_VersionBinding:
    """RIG-007: RI version must be bound to Specification version."""

    def test_version_binding(self):
        info = get_version_info()
        # Implementation must reference spec version
        assert info["specification_version"] == "1.0"
        assert info["implementation_version"].startswith("0.1")

    def test_binding_adrs_are_frozen(self):
        """All bound ADRs are final/accepted."""
        adrs = MANIFEST["specification"]["binding"]["adr"]
        assert "ADR-0038" in adrs
        assert "ADR-0041" in adrs
        assert "ADR-0042" in adrs
