"""Extension Runtime Adapter — Standard Extension Contract for Tang OS.

Any third-party Extension must implement Extension base class.
The contract enforces: capability only, no identity modification.
"""

from src.extensions.base import Extension
from src.extensions.manifest import ExtensionManifest
from src.extensions.validator import ExtensionValidator
from src.extensions.sandbox import ExtensionSandbox

__all__ = ["Extension", "ExtensionManifest", "ExtensionValidator", "ExtensionSandbox"]
