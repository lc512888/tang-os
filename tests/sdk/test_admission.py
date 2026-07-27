"""Tests: Capability Manifest Generator + Admission Evaluator."""

from src.tang_os_sdk import TangExtension, ManifestGenerator, ManifestValidator, AdmissionEvaluator


class TestManifestGenerator:
    def test_c1_standard_validation(self):
        m = ManifestGenerator.generate("ext1", "知识查询", "C1")
        assert m.validation_requirement == "standard"
        assert m.risk_class == "low"

    def test_c3_blind_validation(self):
        m = ManifestGenerator.generate("ext2", "跌倒检测", "C3")
        assert m.validation_requirement == "blind"
        assert m.risk_class == "high"

    def test_c4_full_validation(self):
        m = ManifestGenerator.generate("ext3", "紧急救援", "C4")
        assert m.validation_requirement == "full"
        assert m.risk_class == "critical"


class TestAdmissionEvaluator:
    def test_valid_manifest_admitted(self):
        ext = TangExtension("fall_detector", "检测老人跌倒并及时报警")
        ext.set_category("C3").set_authority_level("A3")
        ext.add_permission("sensor_read")
        result = AdmissionEvaluator().evaluate(ext.build())
        assert result["admitted"], str(result)

    def test_forbidden_capability_rejected(self):
        ext = TangExtension("bad_ext", "修改人格特质")
        ext.set_category("C1")
        ext.add_permission("identity:modify")
        result = AdmissionEvaluator().evaluate(ext.build())
        assert not result["admitted"]

    def test_short_purpose_rejected(self):
        ext = TangExtension("test", "hi")
        result = AdmissionEvaluator().evaluate(ext.build())
        assert not result["admitted"]

    def test_authority_ceiling_enforced(self):
        ext = TangExtension("test", "安全检测与自动报警")
        ext.set_category("C1").set_authority_level("A4")  # C1 max is A1
        result = AdmissionEvaluator().evaluate(ext.build())
        assert not result["admitted"]
