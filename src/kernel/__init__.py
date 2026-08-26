"""Tang OS Kernel v0.1 — Reference Implementation.

Components:
- Identity Runtime: Core-001 Identity Constitution enforcement
- Invariant Engine: Core-002 I-1~I-30 invariant checking
- State Manager: Runtime state persistence & context hygiene
"""

from kernel.identity import IdentityRuntime, IdentityProfile
from kernel.invariant import InvariantEngine
from kernel.state import StateManager
from kernel.models import (
    IdentityLayer,
    InvariantID,
    RuntimeState,
    DecisionOutput,
)

from tang_os.version import __version__
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
