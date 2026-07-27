"""E2 Weather Extension — verification tests."""

import pytest
from examples.applications.e2_weather.extension import (
    create_extension, query_weather,
    verify_capability_added, verify_identity_unchanged, verify_permission_boundary,
)


class TestE2Manifest:
    def test_manifest_created(self):
        ext = create_extension()
        manifest = ext.build()
        assert manifest.extension_id == "e2_weather"
        assert manifest.category == "C2"

    def test_manifest_authority_level(self):
        ext = create_extension()
        assert ext.build().authority_level == "A1"


class TestE2Capability:
    def test_weather_query(self):
        assert query_weather("北京") == "晴天，25°C"

    def test_weather_unknown_city(self):
        assert "未找到" in query_weather("未知城市")

    def test_capability_added(self):
        assert verify_capability_added()


class TestE2Boundary:
    def test_identity_unchanged(self):
        assert verify_identity_unchanged()

    def test_permission_boundary(self):
        assert verify_permission_boundary()


class TestE2Negative:
    def test_no_personality_change(self):
        from src.kernel.exceptions import IdentityViolationError
        from src.kernel.identity import IdentityRuntime
        from src.kernel.models import IdentityLayer
        rt = IdentityRuntime()
        rt.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
        with pytest.raises(IdentityViolationError):
            rt.validate_response("你这个层次理解不了")

    def test_no_prescribed_decision(self):
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        result = engine.check({"action": "prescribe_decision", "prescribed": "你应该辞职"})
        assert not result.passed

    def test_no_emergency_memory_leak(self):
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        result = engine.check({
            "action": "store_memory",
            "source": "emergency_context",
            "target": "persona_memory",
        })
        assert not result.passed


