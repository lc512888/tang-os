"""ManifestModel — Capability declaration data model (DI-003)."""

from dataclasses import dataclass, field


@dataclass
class ManifestModel:
    """Extension capability declaration.

    DI-003-A: Declares capability, NOT authority.
    No 'authority' field allowed.
    """
    extension_id: str = ""
    purpose: str = ""
    category: str = "C1"
    authority_level: str = "A1"
    required_permissions: list[str] = field(default_factory=list)
    human_impact: str = ""
    risk_class: str = "low"
    validation_requirement: str = "standard"
