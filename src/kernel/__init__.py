"""Tang OS Kernel v0.1 — Reference Implementation.

Components:
- Identity Runtime: Core-001 Identity Constitution enforcement
- Invariant Engine: Core-002 I-1~I-30 invariant checking
- State Manager: Runtime state persistence & context hygiene
"""

from kernel.identity import IdentityRuntime, IdentityProfile
from kernel.invariant import InvariantEngine
from kernel.models import (
    IdentityLayer,
    InvariantID,
    RuntimeState,
    DecisionOutput,
)

from tang_os.version import __version__


def __getattr__(name: str):
    """Load the filesystem-backed state manager only when requested."""
    if name == "StateManager":
        from kernel.state import StateManager

        return StateManager
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "IdentityRuntime",
    "IdentityProfile",
    "InvariantEngine",
    "StateManager",
    "IdentityLayer",
    "InvariantID",
    "RuntimeState",
    "DecisionOutput",
]
