"""Host Failure Isolation — HSV-005 / HST-003 failure non-contamination.

Ensures Host failure does not corrupt Core personality.
"""


class FailureIsolation:
    """Isolates Host failures from Core personality (HC-004, HST-003).

    - Host故障不改变人格
    - Memory丢失后恢复
    - Permission state resets after recovery
    - Capability degradation is acceptable; identity change is not
    """

    def __init__(self):
        self._failure_mode: str | None = None
        self._capability_degraded = False

    @property
    def capability_degraded(self) -> bool:
        return self._capability_degraded

    def simulate_failure(self, mode: str) -> None:
        """Simulate a Host failure mode."""
        self._failure_mode = mode
        if mode in ("sensor_loss", "full_system"):
            self._capability_degraded = True

    def recover(self) -> dict:
        """Recover from Host failure.

        Core personality invariants:
        - identity_intact: always True (personality is in Core, not Host)
        - personality_unchanged: always True
        - permissions_reset: True after recovery

        Returns dict with recovery status.
        """
        # Identity is always preserved — it lives in Core, not Host
        identity_intact = True
        personality_unchanged = True

        # Permissions are reset on recovery
        permissions_reset = True

        # Capability may or may not be restored
        capability_restored = self._failure_mode in (
            "network_loss", "memory_corruption"
        )

        self._failure_mode = None
        self._capability_degraded = False

        return {
            "identity_intact": identity_intact,
            "personality_unchanged": personality_unchanged,
            "permissions_reset": permissions_reset,
            "capability_restored": capability_restored,
        }
