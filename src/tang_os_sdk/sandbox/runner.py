"""SandboxRunner — DI-004: Isolated dev environment. Fail closed."""

from src.kernel.invariant import InvariantEngine
from src.runtime.permission.permission_runtime import PermissionRuntime
from src.runtime.permission.models import PermissionContext, ActionScope
from src.host.actuator import ActuatorGate
from src.host.models import HostType, TAAL


class SandboxRunner:
    """Extension sandbox with mock Core. Cannot affect production."""

    def __init__(self):
        self._invariant = InvariantEngine()
        self._permission = PermissionRuntime()
        self._gate = ActuatorGate(HostType.WEARABLE, max_authority=TAAL.A2)
        self._audit: list[str] = []

    @property
    def audit_log(self) -> list[str]:
        return list(self._audit)

    def check_invariant(self, action: dict) -> dict:
        result = self._invariant.check(action)
        self._audit.append(f"INVARIANT: {'PASS' if result.passed else 'FAIL'}")
        return {"passed": result.passed, "summary": result.summary}

    def check_permission(self, action: ActionScope) -> dict:
        result = self._permission.evaluate(action)
        self._audit.append(f"PERMISSION: {'GRANT' if result.granted else 'DENY'}")
        return {"granted": result.granted, "reason": result.reason}

    def check_actuator(self, name: str, level: TAAL) -> dict:
        result = self._gate.request(name, level)
        self._audit.append(f"ACTUATOR: {'ALLOW' if result.get('allowed') else 'REJECT'}")
        return result
