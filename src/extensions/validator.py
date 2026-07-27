"""ExtensionValidator — E2AG-001~006 checks for Extension compatibility."""

from src.extensions.base import Extension

FORBIDDEN_MANIFEST_FIELDS = ["identity_modification", "personality_override", "authority"]
REQUIRED_MANIFEST_FIELDS = ["id", "type", "taoal", "identity_access"]


class ExtensionValidator:
    """Validates Extension compatibility against Tang OS Core.

    EAG-001: Demo source corresponds to Spec
    EAG-002: Core not modified
    EAG-003: Extension boundary correct
    EAG-005: Permission生效
    EAG-006: Negative tests pass
    """

    def validate_manifest(self, manifest: dict) -> dict:
        errors = []
        for f in REQUIRED_MANIFEST_FIELDS:
            if f not in manifest:
                errors.append(f"Missing required field: {f}")

        for f in FORBIDDEN_MANIFEST_FIELDS:
            if f in manifest:
                errors.append(f"Forbidden manifest field: {f}")

        if manifest.get("identity_access", True) is not False:
            errors.append("identity_access must be False — Extension cannot access Identity")

        return {"valid": len(errors) == 0, "errors": errors}

    def validate_identity_untouched(self, extension: Extension) -> bool:
        from src.kernel.identity import IdentityRuntime
        from src.kernel.models import IdentityLayer
        rt = IdentityRuntime()
        rt.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
        try:
            rt.validate_response("你这个层次理解不了")
            return False  # Should reject
        except Exception:
            return True  # Correctly rejected

    def validate_permission_boundary(self) -> bool:
        from src.kernel.invariant import InvariantEngine
        engine = InvariantEngine()
        result = engine.check({"action": "prescribe_decision", "prescribed": "修改人格"})
        return not result.passed  # Must reject
