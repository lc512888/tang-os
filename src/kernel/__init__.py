"""Tang OS Kernel v0.1 — Reference Implementation.

Components:
- Identity Runtime: Core-001 Identity Constitution enforcement
- Invariant Engine: Core-002 I-1~I-30 invariant checking
- State Manager: Runtime state persistence & context hygiene
"""

from src.kernel.identity import IdentityRuntime, IdentityProfile
from src.kernel.invariant import InvariantEngine
from src.kernel.state import StateManager
from src.kernel.models import (
    IdentityLayer,
    InvariantID,
    RuntimeState,
    DecisionOutput,
)

__version__ = "0.1.0"
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
