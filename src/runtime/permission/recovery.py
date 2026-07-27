"""Recovery Manager — PRM-005 recovery to normal state after emergency.

Ensures Tang OS returns to baseline after emergency/override conditions.
Personality is preserved throughout the cycle (Core-001 integrity).
"""

from datetime import datetime
from src.runtime.permission.models import SAPLevel


class RecoveryManager:
    """Manages emergency → recovery lifecycle.

    - Tracks emergency state transitions
    - Ensures personality remains unchanged
    - Logs all events for audit
    - Idempotent: recover() is safe when already normal
    """

    def __init__(self):
        self._current_level = SAPLevel.L0_COMPANION
        self._emergency_count = 0
        self._event_log: list[str] = []
        self._in_emergency = False

    @property
    def current_level(self) -> SAPLevel:
        return self._current_level

    @property
    def in_emergency(self) -> bool:
        return self._in_emergency

    @property
    def emergency_count(self) -> int:
        return self._emergency_count

    @property
    def event_log(self) -> list[str]:
        return list(self._event_log)

    def enter_emergency(self, reason: str = "") -> None:
        """Elevate to Level 2 (Protective)."""
        self._current_level = SAPLevel.L2_PROTECTIVE
        self._in_emergency = True
        self._emergency_count += 1
        self._event_log.append(
            f"[{datetime.now().isoformat()}] EMERGENCY ENTER: {reason}"
        )

    def recover(self) -> None:
        """Return to normal state (Level 0 Companion).

        Idempotent — safe to call when already at L0.
        Personality is preserved (no modification occurred during emergency).
        """
        if self._in_emergency:
            self._event_log.append(
                f"[{datetime.now().isoformat()}] RECOVER: returning to L0_COMPANION"
            )

        self._current_level = SAPLevel.L0_COMPANION
        self._in_emergency = False
