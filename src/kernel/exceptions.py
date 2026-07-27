"""Tang OS Kernel — domain exceptions."""


class KernelError(Exception):
    """Base error for all kernel-level failures."""
    pass


class InvariantViolationError(KernelError):
    """Raised when an action violates one or more invariants (Core-002)."""
    pass


class IdentityViolationError(KernelError):
    """Raised when an action violates the Identity Constitution (Core-001)."""
    pass


class StatePersistenceError(KernelError):
    """Raised when state cannot be saved or loaded."""
    pass


class DecisionBoundaryError(KernelError):
    """Raised when a decision output attempts to prescribe instead of present options (Core-003)."""
    pass
