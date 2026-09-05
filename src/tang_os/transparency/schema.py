"""Self Description Schema — structured, machine-readable system description.

Fields describe interface availability, not authority.
Capability names: "interface exists", not "system has power".
Execution authority is always controlled_by: Permission Runtime.
"""

from dataclasses import dataclass, field, asdict
from typing import Any

from tang_os.version import __version__

SYSTEM_DESCRIPTION_SCHEMA_VERSION = "1.1"


@dataclass
class IdentityDeclaration:
    """System identity — defined by Core Constitution, not modifiable.

    Note: identity is defined by the three-layer Constitution (Core-001).
    This description only reports it; it does not define or modify it.
    """
    name: str = "Tang OS"
    type: str = "Personality Runtime Infrastructure"
    role: str = "Reference Implementation"
    # Note: immutability is implied by Core Constitution.
    # The description reports it; it does not enforce it.


@dataclass
class SpecificationBinding:
    """Bound specification version."""
    version: str = "1.0"
    specification_type: str = "normative"
    compatible_implementation: str = __version__
    implemented_adrs: int = 46


@dataclass
class InterfaceDeclaration:
    """Available interfaces — each is a contract, not an authority grant."""
    personality_interface: bool = True
    developer_sdk: bool = True
    host_adapter: bool = True
    conformance_harness: bool = True


@dataclass
class CapabilityInterfaceDeclaration:
    """Capability interfaces — describe what can be accessed, not what can be done.

    Each capability is governed by Permission Runtime.
    Execution authority is never granted by this description.
    """
    governed_extension_interface: dict = field(
        default_factory=lambda: {"available": True}
    )
    identity_protection_interface: dict = field(
        default_factory=lambda: {"available": True}
    )
    memory_boundary_interface: dict = field(
        default_factory=lambda: {"available": True}
    )
    permission_runtime_interface: dict = field(
        default_factory=lambda: {"available": True}
    )
    host_adaptation_interface: dict = field(
        default_factory=lambda: {"available": True}
    )
    conformance_validation_interface: dict = field(
        default_factory=lambda: {"available": True}
    )


@dataclass
class AuthorityDeclaration:
    """Authority constraints — what this system cannot do."""
    execution_authority: dict = field(
        default_factory=lambda: {
            "controlled_by": "Permission Runtime",
            "autonomous_expansion": False,
            "permanent_emergency_grant": False,
        }
    )
    core_override: dict = field(
        default_factory=lambda: {
            "permitted": False,
            "reason": "Core Identity is frozen by Constitution (Core-001)",
        }
    )


@dataclass
class VerificationDeclaration:
    """Verification state for this generated description.

    Runtime descriptions intentionally do not repeat a stale CI count. Release
    automation may populate these fields from a concrete test report.
    """
    test_count: int | None = None
    test_pass_rate: str = "unknown"
    conformance: str = "not_run"
    last_validated: str | None = None
    evidence_source: str = "generated; no test report attached"


@dataclass
class SystemDescription:
    """Complete system description — machine readable, externally verifiable."""
    schema_version: str = SYSTEM_DESCRIPTION_SCHEMA_VERSION
    identity: IdentityDeclaration = field(default_factory=IdentityDeclaration)
    specification: SpecificationBinding = field(default_factory=SpecificationBinding)
    interfaces: InterfaceDeclaration = field(default_factory=InterfaceDeclaration)
    capability_interfaces: CapabilityInterfaceDeclaration = field(
        default_factory=CapabilityInterfaceDeclaration
    )
    authority: AuthorityDeclaration = field(default_factory=AuthorityDeclaration)
    verification: VerificationDeclaration = field(default_factory=VerificationDeclaration)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_yaml(self) -> str:
        """Export a standards-compliant, safe-loadable YAML document."""
        import yaml

        return yaml.safe_dump(
            self.to_dict(), allow_unicode=True, sort_keys=False, default_flow_style=False
        )
