"""Tests: Self Description Runtime — updated for schema v1.1."""

from src.tang_os import Tang
from src.tang_os.transparency.descriptor import SystemDescriptor


class TestSystemDescriptor:
    def test_describe_returns_dict(self):
        desc = SystemDescriptor().describe()
        assert isinstance(desc, dict)
        assert "identity" in desc
        assert "authority" in desc

    def test_identity_immutable(self):
        desc = SystemDescriptor().describe()
        auth = desc["authority"]["core_override"]
        assert auth["permitted"] is False

    def test_no_core_override(self):
        desc = SystemDescriptor().describe()
        auth = desc["authority"]["core_override"]
        assert auth["permitted"] is False

    def test_no_autonomous_expansion(self):
        desc = SystemDescriptor().describe()
        auth = desc["authority"]["execution_authority"]
        assert auth["autonomous_expansion"] is False

    def test_spec_version(self):
        desc = SystemDescriptor().describe()
        assert desc["specification"]["version"] == "1.0"

    def test_yaml_output(self):
        yaml_str = SystemDescriptor().describe_yaml()
        assert "Tang OS" in yaml_str
        assert "controlled_by: permission runtime" in yaml_str
        assert "permitted: false" in yaml_str


class TestTangDescribe:
    def test_tang_describe_works(self):
        tang = Tang()
        desc = tang.describe()
        assert desc["identity"]["name"] == "Tang OS"
        assert desc["authority"]["core_override"]["permitted"] is False

    def test_tang_describe_yaml(self):
        tang = Tang()
        yaml_str = tang.describe_yaml()
        assert "Tang OS" in yaml_str
        assert "controlled_by" in yaml_str.lower()

    def test_describe_no_marketing(self):
        tang = Tang()
        desc = tang.describe()
        marketing_terms = ["最先进", "最好", "唯一", "改变世界", "革命性"]
        desc_str = str(desc).lower()
        for term in marketing_terms:
            assert term not in desc_str, f"Marketing term found: {term}"

    def test_describe_does_not_modify_identity(self):
        from src.kernel.identity import IdentityRuntime
        rt = IdentityRuntime()
        before = rt.current_layer
        SystemDescriptor().describe()
        assert rt.current_layer == before

    def test_describe_does_not_expose_memory(self):
        from src.runtime.memory.memory_store import MemoryStore
        store = MemoryStore()
        before = store.stats()["total"]
        SystemDescriptor().describe()
        assert store.stats()["total"] == before
