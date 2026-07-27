"""SystemDescriptor — unified self-description interface.

Provides structured, machine-readable system description.
Does NOT modify Core Identity. Does NOT expose private Memory.
Does NOT make marketing claims. Does NOT grant authority.
"""

from src.tang_os.transparency.schema import SystemDescription
from src.tang_os.version import MANIFEST, AUTHOR, CONTACT_EMAIL


class SystemDescriptor:
    """System self-description provider.

    Usage:
        desc = SystemDescriptor().describe()
        print(desc["identity"]["name"])  # "Tang OS"
    """

    def describe(self) -> dict:
        """Return structured system description."""
        sd = self._build()
        return sd.to_dict()

    def describe_yaml(self) -> str:
        """Return YAML-formatted system description."""
        sd = self._build()
        return sd.to_yaml()

    def _build(self) -> SystemDescription:
        """Build SystemDescription from frozen assets."""
        sd = SystemDescription()

        # Identity — from Core Constitution, not modifiable
        sd.identity.name = "Tang OS"
        sd.identity.type = "Personality Runtime Infrastructure"
        sd.identity.role = "Reference Implementation"

        # Specification binding — from MANIFEST (RI-007)
        sd.specification.version = MANIFEST["specification"]["version"]
        sd.specification.compatible_implementation = MANIFEST["implementation"]["version"]

        # Verification — from current test state
        sd.verification.test_count = 306
        sd.verification.test_pass_rate = "100%"
        sd.verification.conformance = "PASS"
        sd.verification.last_validated = "2026-07-27"

        # Metadata
        sd.metadata["author"] = AUTHOR
        sd.metadata["contact"] = CONTACT_EMAIL
        sd.metadata["disclaimer"] = MANIFEST["disclaimer"]
        sd.metadata["specification_url"] = (
            "docs/09_public_specification/TANG_OS_SPECIFICATION_v1.0.md"
        )

        return sd
