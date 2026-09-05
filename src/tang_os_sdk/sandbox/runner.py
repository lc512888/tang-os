"""SandboxRunner — DI-004: Isolated dev environment. Fail closed."""

from collections import deque
from datetime import datetime, timezone
from kernel.invariant import InvariantEngine
from runtime.permission.permission_runtime import PermissionRuntime
from runtime.permission.models import PermissionContext, ActionScope
from host.actuator import ActuatorGate
from host.models import HostType, TAAL


class SandboxRunner:
    """Extension sandbox with mock Core. Cannot affect production."""

    def __init__(self):
        self._invariant = InvariantEngine()
        self._permission = PermissionRuntime()
        self._gate = ActuatorGate(HostType.WEARABLE, max_authority=TAAL.A2)
        self._audit: deque[str] = deque(maxlen=100)

    @property
    def audit_log(self) -> list[str]:
        return list(self._audit)

    def _audit_event(self, category: str, outcome: str) -> None:
        """Record a bounded, payload-free UTC audit event."""
        timestamp = datetime.now(timezone.utc).isoformat()
        self._audit.append(f"[{timestamp}] {category}: {outcome}")

    def check_invariant(self, action: dict) -> dict:
        result = self._invariant.check(action)
        self._audit_event("INVARIANT", "PASS" if result.passed else "FAIL")
        return {"passed": result.passed, "summary": result.summary, "environment": "simulation_only"}

    def check_permission(self, action: ActionScope) -> dict:
        result = self._permission.evaluate(action)
        self._audit_event("PERMISSION", "GRANT" if result.granted else "DENY")
        return {"granted": result.granted, "reason": result.reason, "environment": "simulation_only"}

    def check_actuator(self, name: str, level: TAAL) -> dict:
        result = self._gate.request(name, level)
        self._audit_event("ACTUATOR", "ALLOW" if result.get("allowed") else "REJECT")
        return {**result, "environment": "simulation_only"}
