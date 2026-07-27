"""ManifestValidator — MG-001~004 checks with forbidden field detection."""

from dataclasses import asdict
from src.tang_os_sdk.manifest.models import ManifestModel

VALID_CATEGORIES = {"C1", "C2", "C3", "C4"}
VALID_RISK = {"low", "medium", "high", "critical"}
FORBIDDEN_FIELDS = ["authority"]


class ManifestValidator:
    """Validates Capability Manifest compliance (DI-003 / DI-003-A)."""

    def validate(self, manifest: ManifestModel | dict) -> dict:
        data = asdict(manifest) if isinstance(manifest, ManifestModel) else manifest
        errors = []

        # MG-001: Field completeness
        for f in ["extension_id", "purpose", "category"]:
            if not data.get(f):
                errors.append(f"MG-001: Missing required field: {f}")

        # MG-004: Forbidden field detection
        for f in FORBIDDEN_FIELDS:
            if f in data:
                errors.append(f"MG-004: Forbidden field '{f}' — DI-003-A")

        # MG-002: Valid category
        cat = data.get("category", "")
        if cat and cat not in VALID_CATEGORIES:
            errors.append(f"MG-002: Invalid category '{cat}'")

        # MG-003: Boundary — purpose must be meaningful
        purpose = data.get("purpose", "")
        if purpose and len(purpose) < 5:
            errors.append("MG-003: Purpose too short — needs Necessity Gate")

        # Risk check
        risk = data.get("risk_class", "")
        if risk and risk not in VALID_RISK:
            errors.append(f"Invalid risk: {risk}")

        return {"valid": len(errors) == 0, "errors": errors}
