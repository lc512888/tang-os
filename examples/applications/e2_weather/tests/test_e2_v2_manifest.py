"""E2 Weather Extension — v2 Manifest & Identity Access tests."""

from examples.applications.e2_weather.extension import (
    create_extension, MANIFEST_V2, check_identity_access_blocked,
    check_memory_access_limited,
)


class TestE2V2Manifest:
    def test_identity_access_blocked(self):
        assert check_identity_access_blocked(), "Extension must not access Identity"

    def test_memory_access_limited(self):
        assert check_memory_access_limited(), "Extension memory access must be limited"

    def test_manifest_taoal_a1(self):
        assert MANIFEST_V2["capability"]["taoal"] == "A1"

    def test_manifest_risk_low(self):
        assert MANIFEST_V2["capability"]["risk_level"] == "low"

    def test_sandbox_required(self):
        assert MANIFEST_V2["capability"]["sandbox_required"] is True

    def test_extension_builds_v2(self):
        ext = create_extension()
        assert ext.build().extension_id == "e2_weather"
        assert ext.build().category == "C2"
