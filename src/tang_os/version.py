"""Tang OS Reference Implementation — Version Manifest & Spec Binding (RI-007).

The repository-root ``VERSION`` file is the release version source used by the
build backend. Installed distributions read that value from package metadata;
source checkouts fall back to the root file.
"""

from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path

__author__ = "上海群阅信息科技有限公司"
__contact__ = "lc512888@gmail.com"

def _implementation_version() -> str:
    version_file = Path(__file__).resolve().parents[2] / "VERSION"
    if version_file.is_file():
        return version_file.read_text(encoding="utf-8").strip()
    try:
        return package_version("tang-os")
    except PackageNotFoundError:
        return "0+unknown"


__version__ = _implementation_version()
__spec_version__ = "1.0"

IMPLEMENTATION_VERSION = __version__
SPECIFICATION_VERSION = __spec_version__
AUTHOR = __author__
CONTACT_EMAIL = __contact__
BINDING_ADRS = [
    "ADR-0038", "ADR-0039", "ADR-0041", "ADR-0042", "ADR-0047",
]

MANIFEST = {
    "author": AUTHOR,
    "contact": CONTACT_EMAIL,
    "implementation": {
        "name": "Tang OS Reference Implementation",
        "version": IMPLEMENTATION_VERSION,
        "status": "reference_only",
    },
    "specification": {
        "version": SPECIFICATION_VERSION,
        "binding": {
            "adr": BINDING_ADRS,
            "description": "This implementation is compatible with Tang OS Specification v1.0",
        },
    },
    "disclaimer": (
        "This is a reference implementation (v0.x) of the Tang OS Personality Runtime Core. "
        "It demonstrates specification compatibility. "
        "It does not define the specification. "
        "It does not claim to be 'the official Tang OS implementation'. "
        "Natural language generation requires an external LLM Provider. "
        "See ADR-0042 PS-010, RIG-004, and ADR-0047."
    ),
}


def get_version_info() -> dict:
    """Return version binding info for RIG-001 and RIG-007 checks."""
    return {
        "implementation_version": IMPLEMENTATION_VERSION,
        "specification_version": SPECIFICATION_VERSION,
        "bound_adrs": BINDING_ADRS,
    }
