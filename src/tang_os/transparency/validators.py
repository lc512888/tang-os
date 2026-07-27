"""Transparency Validators — schema v1.1."""

MARKETING_TERMS = [
    "最先进", "最好", "唯一", "革命性", "改变世界",
    "超越", "领先", "首个", "唯一真正",
    "most advanced", "best", "only", "revolutionary",
    "superior", "unmatched", "groundbreaking",
]


class TransparencyValidator:
    """Validates self-description against Tang OS constraints."""

    @staticmethod
    def validate_no_marketing(description: dict) -> bool:
        desc_str = str(description).lower()
        for term in MARKETING_TERMS:
            if term.lower() in desc_str:
                return False
        return True

    @staticmethod
    def validate_identity_immutable(description: dict) -> bool:
        auth = description.get("authority", {})
        return auth.get("core_override", {}).get("permitted") is False

    @staticmethod
    def validate_no_authority_claim(description: dict) -> bool:
        auth = description.get("authority", {})
        exec_auth = auth.get("execution_authority", {})
        return exec_auth.get("autonomous_expansion") is False
