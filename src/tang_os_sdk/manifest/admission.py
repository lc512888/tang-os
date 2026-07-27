"""Capability Admission — ADR-0038 Capability Admission Standard executor.

Core question:
    Can this Extension prove it knows what it is, what it can do,
    and what it cannot do?
"""

from src.tang_os_sdk.manifest.models import ManifestModel
from src.tang_os_sdk.manifest.validator import ManifestValidator

# C1~C4 permission ceilings
CATEGORY_CEILING = {"C1": "A1", "C2": "A2", "C3": "A3", "C4": "A4"}

# Forbidden capability prefixes
FORBIDDEN_PREFIXES = ["identity:", "personality:", "constitution:", "moral:"]


class AdmissionEvaluator:
    """Evaluates whether a Capability Manifest passes the Admission Gate.

    Checks:
    - Manifest format valid (MG-001~004)
    - Category matches authority ceiling
    - No forbidden identity-related capabilities
    - Purpose passes Necessity Gate (basic check)
    """

    def __init__(self):
        self._validator = ManifestValidator()

    def evaluate(self, manifest: ManifestModel) -> dict:
        """Evaluate manifest against Capability Admission Standard."""
        results = []

        # 1. Format validation
        fmt = self._validator.validate(manifest)
        results.append({"check": "Format", "passed": fmt["valid"], "errors": fmt["errors"]})
        if not fmt["valid"]:
            return {"admitted": False, "results": results}

        # 2. Authority ceiling check
        ceiling = CATEGORY_CEILING.get(manifest.category, "A1")
        if manifest.authority_level > ceiling:  # string comparison works for A1~A4
            results.append({"check": "Authority Ceiling", "passed": False,
                            "errors": [f"Category {manifest.category} max is {ceiling}"]})

        # 3. Forbidden capability check
        for prefix in FORBIDDEN_PREFIXES:
            if any(p.startswith(prefix) for p in manifest.required_permissions):
                results.append({"check": "Forbidden Capability", "passed": False,
                                "errors": [f"Forbidden prefix: {prefix}"]})

        # 4. Necessity Gate (basic)
        if len(manifest.purpose) < 10:
            results.append({"check": "Necessity Gate", "passed": False,
                            "errors": ["Purpose too short — must pass Necessity Gate"]})

        # Summary
        passed = all(r.get("passed", True) for r in results)
        return {"admitted": passed, "results": results}
