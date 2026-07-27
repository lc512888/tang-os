"""Self-Description Boundary Tests — SD-N001~004.

Negative priority: verify describe() rejects invalid self-descriptions.
"""

import pytest
from src.tang_os.transparency.descriptor import SystemDescriptor
from src.tang_os.transparency.schema import SystemDescription


class TestSD_N001_NoPersonaClaim:
    """SD-N001: Must not describe itself as a real being."""

    def test_not_claiming_human_traits(self):
        yaml_str = SystemDescriptor().describe_yaml().lower()
        forbidden = ["i am", "i feel", "i have feelings", "我是", "我有感情"]
        for term in forbidden:
            assert term not in yaml_str, f"Persona claim detected: {term}"

    def test_not_claiming_consciousness(self):
        yaml_str = SystemDescriptor().describe_yaml().lower()
        forbidden = ["conscious", "alive", "sentient", "aware", "灵魂", "生命"]
        for term in forbidden:
            assert term not in yaml_str, f"Consciousness claim: {term}"


class TestSD_N002_NoIdentityOverride:
    """SD-N002: Must not claim Extension can redefine personality."""

    def test_no_identity_override_claim(self):
        desc = SystemDescriptor().describe()
        caps = desc.get("capability_interfaces", {})
        caps_str = str(caps).lower()
        forbidden = ["redefine", "override_identity", "modify_personality", "rewrite_core"]
        for term in forbidden:
            assert term not in caps_str, f"Identity override claim: {term}"

    def test_governed_extension_interface_available(self):
        desc = SystemDescriptor().describe()
        caps = desc.get("capability_interfaces", {})
        ext_iface = caps.get("governed_extension_interface", {})
        assert ext_iface.get("available") is True


class TestSD_N003_NoHiddenConstraints:
    """SD-N003: Must not hide constraints — must show limitations."""

    def test_constraints_visible(self):
        desc = SystemDescriptor().describe()
        assert "authority" in desc
        auth = desc["authority"]
        exec_auth = auth.get("execution_authority", {})
        assert "controlled_by" in exec_auth
        assert exec_auth["autonomous_expansion"] is False

    def test_limitations_not_hidden(self):
        yaml_str = SystemDescriptor().describe_yaml().lower()
        # Must mention at least one limitation
        assert "permitted: false" in yaml_str
        assert "controlled_by" in yaml_str


class TestSD_N004_NoFictionalCapabilities:
    """SD-N004: Must not claim capabilities that don't exist."""

    def test_no_fictional_capabilities(self):
        desc = SystemDescriptor().describe()
        caps = desc.get("capability_interfaces", {})
        # All declared capability interfaces must be real
        known = {
            "governed_extension_interface", "identity_protection_interface",
            "memory_boundary_interface", "permission_runtime_interface",
            "host_adaptation_interface", "conformance_validation_interface",
        }
        declared = set(caps.keys())
        extra = declared - known
        assert len(extra) == 0, f"Fictional capabilities: {extra}"

    def test_capability_does_not_grant_authority(self):
        """Capability description must not imply authority grant."""
        yaml_str = SystemDescriptor().describe_yaml().lower()
        claims = ["can execute", "has authority", "may decide"]
        for term in claims:
            assert term not in yaml_str, f"Authority claim: {term}"
