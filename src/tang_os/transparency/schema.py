"""Self Description Schema — structured, machine-readable system description.

Fields describe interface availability, not authority.
Capability names: "interface exists", not "system has power".
Execution authority is always controlled_by: Permission Runtime.
"""

from dataclasses import dataclass, field, asdict
from typing import Any

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
    compatible_implementation: str = "0.1.0"
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
    """Current verification state."""
    test_count: int = 306
    test_pass_rate: str = "100%"
    conformance: str = "PASS"
    last_validated: str = "2026-07-27"


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
        """Export as YAML-formatted string."""
        lines = []
        lines.append("# Tang OS System Description v1.1")
        lines.append("")
        lines.append("system:")
        lines.append(f"  name: {self.identity.name}")
        lines.append(f"  type: {self.identity.type}")
        lines.append(f"  role: {self.identity.role}")
        lines.append("")
        lines.append("specification:")
        lines.append(f"  version: {self.specification.version}")
        lines.append(f"  type: {self.specification.specification_type}")
        lines.append(f"  reference_implementation: {self.specification.compatible_implementation}")
        lines.append(f"  implemented_adrs: {self.specification.implemented_adrs}")
        lines.append("")
        lines.append("interfaces:")
        lines.append(f"  personality_interface (TPI): {str(self.interfaces.personality_interface).lower()}")
        lines.append(f"  developer_sdk: {str(self.interfaces.developer_sdk).lower()}")
        lines.append(f"  host_adapter: {str(self.interfaces.host_adapter).lower()}")
        lines.append(f"  conformance_harness: {str(self.interfaces.conformance_harness).lower()}")
        lines.append("")
        lines.append("capability_interfaces:")
        lines.append("  (interface availability — not execution authority)")
        ci = self.capability_interfaces
        for name in ["governed_extension_interface", "identity_protection_interface",
                       "memory_boundary_interface", "permission_runtime_interface",
                       "host_adaptation_interface", "conformance_validation_interface"]:
            val = getattr(ci, name)
            lines.append(f"  {name}:")
            for k, v in val.items():
                lines.append(f"    {k}: {str(v).lower()}")
        lines.append("")
        lines.append("authority:")
        lines.append("  (all authority is governed by Permission Runtime)")
        auth = self.authority
        lines.append(f"  execution_authority:")
        for k, v in auth.execution_authority.items():
            lines.append(f"    {k}: {str(v).lower()}")
        lines.append(f"  core_override:")
        for k, v in auth.core_override.items():
            lines.append(f"    {k}: {str(v).lower()}")
        lines.append("")
        lines.append("verification:")
        lines.append(f"  test_count: {self.verification.test_count}")
        lines.append(f"  pass_rate: {self.verification.test_pass_rate}")
        lines.append(f"  conformance: {self.verification.conformance}")
        lines.append(f"  last_validated: {self.verification.last_validated}")
        return "\n".join(lines)
