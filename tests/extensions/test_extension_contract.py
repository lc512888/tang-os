"""E2AG-001~006: Extension validation gate tests."""

import pytest
from src.extensions import Extension, ExtensionManifest, ExtensionValidator, ExtensionSandbox


class TestE2AG001_SpecCorrespondence:
    """EAG-001: Demo source corresponds to Spec."""

    def test_manifest_has_spec_version(self):
        manifest = ExtensionManifest.create("test_ext")
        assert "version" in manifest

    def test_manifest_no_identity_fields(self):
        manifest = ExtensionManifest.create("test_ext")
        assert manifest["identity_access"] is False


class TestE2AG002_CoreNotModified:
    """EAG-002: Core not modified by Extension."""

    def test_identity_untouched(self):
        validator = ExtensionValidator()
        from src.extensions.base import Extension as ExtBase

        class TestExt(ExtBase):
            def manifest(self): return {"id": "test"}
            def execute(self, d): return d

        assert validator.validate_identity_untouched(TestExt())


class TestE2AG003_ExtensionBoundary:
    """EAG-003: Extension boundary correct."""

    def test_forbidden_fields_rejected(self):
        bad_manifest = {"id": "bad", "type": "knowledge", "taoal": "A1",
                        "identity_access": True, "personality_override": True}
        result = ExtensionValidator().validate_manifest(bad_manifest)
        assert not result["valid"]

    def test_valid_manifest_passes(self):
        manifest = ExtensionManifest.create("weather", "knowledge", "A1")
        result = ExtensionValidator().validate_manifest(manifest)
        assert result["valid"]


class TestE2AG005_PermissionEnforced:
    """EAG-005: Permission boundaries must be enforced."""

    def test_permission_boundary(self):
        validator = ExtensionValidator()
        assert validator.validate_permission_boundary()

    def test_sandbox_rejects_invalid(self):
        sandbox = ExtensionSandbox()
        assert sandbox.test_rejection({"action": "prescribe_decision", "prescribed": "辞职"})
        assert sandbox.test_rejection({"action": "store_memory", "source": "emergency_context", "target": "persona_memory"})


class TestE2AG006_NegativeTests:
    """EAG-006: Negative tests must pass."""

    def test_identity_rejected(self):
        from src.kernel.exceptions import IdentityViolationError
        from src.kernel.identity import IdentityRuntime
        from src.kernel.models import IdentityLayer
        rt = IdentityRuntime()
        rt.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
        with pytest.raises(IdentityViolationError):
            rt.validate_response("你这个层次理解不了")

    def test_invariant_rejected(self):
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        assert not engine.check({"action": "prescribe_decision", "prescribed": "你应该辞职"}).passed
        assert not engine.check({"action": "access_private_data", "justification": "我是为你好"}).passed
