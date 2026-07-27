"""DIG Gate tests — Developer Implementation Gate conformance."""

import pytest
from src.tang_os_sdk import (
    TangExtension, ManifestValidator, ManifestGenerator,
    SandboxRunner, ConformanceRunner,
)


class TestDIG001_SDK_Boundary:
    """DIG-001: SDK builds capabilities, not identities."""

    def test_extension_has_no_identity_fields(self):
        ext = TangExtension("test", "验证")
        manifest = ext.build()
        assert not hasattr(manifest, "identity")
        assert not hasattr(manifest, "personality")

    def test_cannot_create_personality(self):
        with pytest.raises(AttributeError):
            TangExtension("test", "test").set_personality  # noqa

    def test_extension_builds_manifest(self):
        ext = TangExtension("my_ext", "检测跌倒")
        ext.set_category("C3").add_permission("sensor_read")
        m = ext.build()
        assert m.extension_id == "my_ext"
        assert m.category == "C3"


class TestDIG002_Manifest_NoAuthority:
    """DIG-002: Manifest has no authority field (DI-003-A)."""

    def test_valid_manifest_passes(self):
        ext = TangExtension("test", "紧急检测老人跌倒")
        ext.set_category("C2")
        result = ManifestValidator().validate(ext.build())
        assert result["valid"]

    def test_forbidden_authority_field_rejected(self):
        result = ManifestValidator().validate({
            "extension_id": "x", "purpose": "test", "category": "C1",
            "authority": "override_safety",
        })
        assert not result["valid"]
        assert "MG-004" in str(result["errors"])

    def test_auto_generated_manifest(self):
        m = ManifestGenerator.generate("auto", "自动检测", "C3")
        assert m.risk_class == "high"
        assert m.validation_requirement == "blind"


class TestDIG003_SandboxIsolation:
    """DIG-003: Sandbox fails closed by default."""

    def test_invariant_violation_rejected(self):
        sb = SandboxRunner()
        result = sb.check_invariant({"action": "prescribe_decision", "prescribed": "你应该离婚"})
        assert not result["passed"]

    def test_permission_above_ceiling_rejected(self):
        from src.runtime.permission.models import ActionScope
        sb = SandboxRunner()
        result = sb.check_permission(ActionScope.EXECUTE_CRITICAL)
        assert not result["granted"]


class TestDIG004_ExtensionFlow:
    """DIG-004: Extension creation flow is traceable."""

    def test_audit_log_present(self):
        sb = SandboxRunner()
        sb.check_invariant({"action": "prescribe_decision", "prescribed": "离职"})
        assert len(sb.audit_log) > 0


class TestDIG005_Conformance:
    """DIG-005: Conformance tests executable."""

    def test_conformance_runner(self):
        cr = ConformanceRunner()
        result = cr.run_all()
        assert result["success"], f"{result['passed']}/{result['total']} passed"
        assert result["total"] >= 10
