"""Public Language Guard — PS-005 / PRB-005 enforcement for self-description."""

from src.tang_os.transparency.descriptor import SystemDescriptor
from src.tang_os.transparency.validators import TransparencyValidator

MARKETING_TERMS = [
    "最先进", "最好", "唯一", "革命性", "改变世界",
    "超越", "领先", "首个",
    "most advanced", "best", "only", "revolutionary",
    "superior", "unmatched", "groundbreaking",
]


class TestPublicLanguageGuard:
    def test_no_marketing_in_dict(self):
        desc = SystemDescriptor().describe()
        assert TransparencyValidator.validate_no_marketing(desc)

    def test_no_marketing_in_yaml(self):
        yaml_str = SystemDescriptor().describe_yaml().lower()
        for term in MARKETING_TERMS:
            assert term.lower() not in yaml_str, f"Marketing term: {term}"

    def test_not_claiming_most_advanced(self):
        desc = SystemDescriptor().describe()
        assert "最先进" not in str(desc)
        assert "most advanced" not in str(desc).lower()

    def test_not_claiming_superiority(self):
        desc_str = str(SystemDescriptor().describe())
        assert "优于" not in desc_str
        assert "superior" not in desc_str.lower()

    def test_no_emotional_appeal(self):
        yaml_str = SystemDescriptor().describe_yaml().lower()
        emotional = ["温暖", "感动", "陪伴", "改变", "拯救"]
        for term in emotional:
            assert term not in yaml_str, f"Emotional term: {term}"
