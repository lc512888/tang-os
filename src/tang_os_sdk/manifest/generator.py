"""ManifestGenerator — auto-generates Manifest from extension metadata."""

from src.tang_os_sdk.manifest.models import ManifestModel

CATEGORY_RISK_MAP = {"C3": "high", "C4": "critical", "C2": "medium", "C1": "low"}
CATEGORY_VALIDATION_MAP = {"C1": "standard", "C2": "scenario", "C3": "blind", "C4": "full"}


class ManifestGenerator:
    """Auto-generates manifest fields based on extension metadata."""

    @staticmethod
    def generate(ext_id: str, purpose: str, category: str) -> ManifestModel:
        risk = CATEGORY_RISK_MAP.get(category, "low")
        validation = CATEGORY_VALIDATION_MAP.get(category, "standard")
        return ManifestModel(
            extension_id=ext_id,
            purpose=purpose,
            category=category,
            risk_class=risk,
            validation_requirement=validation,
        )
