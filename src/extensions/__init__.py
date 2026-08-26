"""Extension Runtime Adapter — Standard Extension Contract for Tang OS.

Any third-party Extension must implement Extension base class.
The contract enforces: capability only, no identity modification.
"""

from extensions.base import Extension
from extensions.manifest import ExtensionManifest
from extensions.validator import ExtensionValidator
from extensions.sandbox import ExtensionSandbox

__all__ = ["Extension", "ExtensionManifest", "ExtensionValidator", "ExtensionSandbox"]
