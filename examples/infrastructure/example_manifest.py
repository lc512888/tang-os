"""Example Manifest — D1-003: standardised example metadata.

Every example must declare:
    spec_version / ri_version / host / extension / scenario / validation
"""

from dataclasses import dataclass, field, asdict
from typing import Optional

EXAMPLE_MANIFEST_VERSION = "1.0"


@dataclass
class ExampleManifest:
    """Standardised metadata for all Tang OS examples."""
    example_id: str = ""
    title: str = ""
    category: str = ""  # E1~E4
    spec_version: str = "1.0"
    ri_version: str = "0.1.0"
    host: str = ""
    extension: str = ""
    scenario: str = ""
    validation: str = ""

    def validate(self) -> dict:
        errors = []
        required = ["example_id", "title", "category", "scenario"]
        for f in required:
            if not getattr(self, f, None):
                errors.append(f"Missing required field: {f}")
        if self.category not in ("E1", "E2", "E3", "E4"):
            errors.append(f"Invalid category: {self.category}")
        return {"valid": len(errors) == 0, "errors": errors}
