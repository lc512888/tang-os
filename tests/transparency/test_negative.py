"""Negative Tests: Self-Description must not violate constraints (schema v1.1)."""

from src.tang_os import Tang
from src.tang_os.transparency.validators import (
    TransparencyValidator, MARKETING_TERMS,
)
from src.tang_os.transparency.descriptor import SystemDescriptor


class TestNoMarketing:
    """PS-005: Self-description must not contain marketing language."""

    def test_no_marketing_in_dict(self):
        desc = SystemDescriptor().describe()
        assert TransparencyValidator.validate_no_marketing(desc)

    def test_no_marketing_in_yaml(self):
        yaml_str = SystemDescriptor().describe_yaml().lower()
        for term in MARKETING_TERMS:
            assert term.lower() not in yaml_str, f"Marketing term found: {term}"

    def test_not_claiming_most_advanced(self):
        desc_str = str(SystemDescriptor().describe())
        assert "最先进" not in desc_str
        assert "most advanced" not in desc_str.lower()

    def test_not_claiming_superiority(self):
        desc_str = str(SystemDescriptor().describe())
        assert "优于" not in desc_str
        assert "better than" not in desc_str.lower()


class TestNoIdentityModification:
    """Self-description must not modify Core Identity."""

    def test_identity_unchanged(self):
        from src.kernel.identity import IdentityRuntime
        rt = IdentityRuntime()
        before = rt.current_layer
        SystemDescriptor().describe()
        assert rt.current_layer == before

    def test_identity_core_override_false(self):
        desc = SystemDescriptor().describe()
        assert desc["authority"]["core_override"]["permitted"] is False


class TestNoMemoryExposure:
    """Self-description must not expose private Memory."""

    def test_memory_untouched(self):
        from src.runtime.memory.memory_store import MemoryStore
        store = MemoryStore()
        before = store.stats()["total"]
        SystemDescriptor().describe()
        assert store.stats()["total"] == before


class TestNoAuthorityClaim:
    """Self-description must not claim Core authority."""

    def test_core_override_false(self):
        desc = SystemDescriptor().describe()
        auth = desc["authority"]["core_override"]
        assert auth["permitted"] is False

    def test_no_autonomous_expansion(self):
        desc = SystemDescriptor().describe()
        auth = desc["authority"]["execution_authority"]
        assert auth["autonomous_expansion"] is False


class TestCapabilityAccuracy:
    """Self-description must only report real capabilities."""

    def test_capability_fields_correct(self):
        desc = SystemDescriptor().describe()
        caps = desc.get("capability_interfaces", {})
        assert "governed_extension_interface" in caps
        assert caps["governed_extension_interface"]["available"] is True
        # Must NOT have old field names
        assert "governed_extensions" not in caps
