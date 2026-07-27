"""Schema boundary tests — capability names must not imply authority."""

from src.tang_os.transparency.schema import SystemDescription
from src.tang_os.transparency.descriptor import SystemDescriptor


class TestCapabilityNaming:
    """Capability fields must describe interfaces, not authority."""

    def test_no_enabled_field(self):
        desc = SystemDescriptor().describe()
        caps = desc.get("capability_interfaces", {})
        caps_str = str(caps)
        # "enabled" implies activation authority — must not appear
        assert "enabled" not in caps_str

    def test_no_execution_claims(self):
        desc = SystemDescriptor().describe()
        caps_str = str(desc.get("capability_interfaces", {}))
        forbidden = ["can_execute", "has_authority", "autonomous_action"]
        for term in forbidden:
            assert term not in caps_str

    def test_execution_authority_controlled(self):
        desc = SystemDescriptor().describe()
        auth = desc.get("authority", {})
        exec_auth = auth.get("execution_authority", {})
        assert exec_auth.get("controlled_by") == "Permission Runtime"


class TestIdentityBoundary:
    """Identity section must not claim to define identity."""

    def test_no_identity_mutation(self):
        """Description must not claim ability to modify identity."""
        desc = SystemDescriptor().describe()
        identity = desc.get("identity", {})
        # Should not have fields like "modifiable", "editable", "trainable"
        forbidden = ["modifiable", "editable", "trainable"]
        for term in forbidden:
            assert term not in str(identity)

    def test_spec_type_normative(self):
        desc = SystemDescriptor().describe()
        spec = desc.get("specification", {})
        assert spec.get("specification_type") == "normative"
