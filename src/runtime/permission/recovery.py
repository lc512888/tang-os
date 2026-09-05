"""Recovery Manager — PRM-005 recovery to normal state after emergency.

Ensures Tang OS returns to baseline after emergency/override conditions.
Personality is preserved throughout the cycle (Core-001 integrity).
"""

from collections import deque
from datetime import datetime, timezone
from runtime.permission.models import SAPLevel


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
        self._event_log: deque[str] = deque(maxlen=100)
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

    def _audit_event(self, event: str) -> None:
        timestamp = datetime.now(timezone.utc).isoformat()
        self._event_log.append(f"[{timestamp}] {event}")

    def enter_emergency(self, reason: str = "") -> None:
        """Elevate to Level 2 (Protective)."""
        self._current_level = SAPLevel.L2_PROTECTIVE
        self._in_emergency = True
        self._emergency_count += 1
        # Never persist the free-form reason; it may contain sensitive context.
        self._audit_event(
            "EMERGENCY ENTER: reason supplied [REDACTED]" if reason else "EMERGENCY ENTER"
        )

    def recover(self) -> None:
        """Return to normal state (Level 0 Companion).

        Idempotent — safe to call when already at L0.
        Personality is preserved (no modification occurred during emergency).
        """
        if self._in_emergency:
            self._audit_event("RECOVER: returning to L0_COMPANION")

        self._current_level = SAPLevel.L0_COMPANION
        self._in_emergency = False
