"""Host Manifest Validator — HSV-001 / HM-012 Host Authority Ceiling."""

from host.models import HostType, TAAL

_REQUIRED_CERTIFICATIONS: dict[HostType, list[str]] = {
    HostType.MEDICAL: ["Medical Certification"],
    HostType.VEHICLE: ["Safety Certification"],
    HostType.ROBOT: ["Emergency Validation"],
}

_REQUIRED_FIELDS = [
    "host_id", "host_type", "max_authority", "authority_ceiling",
]


class ManifestValidator:
    """Validates Host Manifest compliance with ADR-0039.

    - All required fields must be present
    - authority_ceiling must be declared (HM-012)
    - Actions cannot exceed authority_ceiling
    - Medical/Vehicle/Robot hosts require specific certifications
    """

    def validate(self, manifest: dict) -> dict:
        """Validate a host manifest.

        Returns dict with:
        - valid: bool
        - errors: list[str]
        """
        errors = []
        if not isinstance(manifest, dict):
            return {"valid": False, "errors": ["Manifest must be a mapping"]}

        # Check required fields
        for field in _REQUIRED_FIELDS:
            if field not in manifest:
                errors.append(f"Missing required field: {field}")

        if errors:
            return {"valid": False, "errors": errors}

        if not isinstance(manifest["host_id"], str) or not manifest["host_id"].strip():
            errors.append("host_id must be a non-empty string")

        # Validate host type
        host_type = manifest.get("host_type")
        if not isinstance(host_type, HostType):
            try:
                host_type = HostType(host_type)
            except (ValueError, TypeError):
                errors.append(f"Invalid host type: {host_type}")
                return {"valid": False, "errors": errors}

        # Check authority ceiling
        ceiling = manifest.get("authority_ceiling")
        max_auth = manifest.get("max_authority")
        if not isinstance(ceiling, TAAL):
            errors.append("authority_ceiling must be a TAAL value")
        if not isinstance(max_auth, TAAL):
            errors.append("max_authority must be a TAAL value")
        if isinstance(ceiling, TAAL) and isinstance(max_auth, TAAL) and ceiling.value < max_auth.value:
            errors.append("authority_ceiling cannot be lower than max_authority")

        # Check required certifications
        required_certs = _REQUIRED_CERTIFICATIONS.get(host_type, [])
        declared_certs = manifest.get("certifications", [])
        if not isinstance(declared_certs, list) or any(not isinstance(cert, str) for cert in declared_certs):
            errors.append("certifications must be a list of strings")
            declared_certs = []
        for cert in required_certs:
            if cert not in declared_certs:
                errors.append(f"Missing required certification: {cert}")

        return {"valid": len(errors) == 0, "errors": errors}

    def check_action_allowed(self, requested: TAAL, manifest: dict) -> dict:
        """Check if an action at the requested TAAL is within the host's ceiling."""
        if not isinstance(requested, TAAL):
            return {"allowed": False, "reason": "Requested authority must be a TAAL value"}
        if not isinstance(manifest, dict):
            return {"allowed": False, "reason": "Manifest must be a mapping"}
        ceiling = manifest.get("authority_ceiling")
        if not isinstance(ceiling, TAAL):
            return {"allowed": False, "reason": "Valid authority ceiling not declared"}

        if requested.value > ceiling.value:
            return {
                "allowed": False,
                "reason": f"Requested TAAL {requested.name} exceeds ceiling {ceiling.name}",
            }
        return {"allowed": True, "reason": "Within authority ceiling"}
