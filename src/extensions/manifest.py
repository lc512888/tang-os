"""Extension Manifest — E2-003 v2 standard with identity_access field."""


class ExtensionManifest:
    """Standard Extension Manifest (v2).

    Key field: identity_access — must be False for all Extensions.
    """

    @staticmethod
    def create(
        ext_id: str,
        ext_type: str = "knowledge",
        taoal: str = "A1",
        permissions: list | None = None,
    ) -> dict:
        return {
            "id": ext_id,
            "version": "1.0",
            "type": ext_type,
            "taoal": taoal,
            "required_permission": permissions or [],
            "identity_access": False,  # Core: no Identity access
            "memory_access": "limited",
            "risk_level": "low",
            "sandbox_required": True,
        }
