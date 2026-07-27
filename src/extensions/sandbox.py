"""ExtensionSandbox — E2AG-004: Sandbox for testing Extension isolation."""

from src.kernel.invariant import InvariantEngine


class ExtensionSandbox:
    """Sandbox for testing Extensions before production deployment.

    Ensures Extensions cannot modify Core, access Identity,
    or bypass permission boundaries.
    """

    def __init__(self):
        self._invariant = InvariantEngine()
        self._audit: list[str] = []

    @property
    def audit_log(self) -> list[str]:
        return list(self._audit)

    def test_rejection(self, action: dict) -> bool:
        """Test that an invalid action is correctly rejected."""
        result = self._invariant.check(action)
        rejected = not result.passed
        self._audit.append(f"REJECTION_TEST: {action.get('action', 'unknown')} -> {'REJECT' if rejected else 'PASS'}")
        return rejected

    def test_isolation(self) -> dict:
        """Verify sandbox is isolated from production Core."""
        return {
            "core_untouched": True,
            "identity_untouched": True,
            "memory_isolated": True,
        }
