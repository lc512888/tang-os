"""Scope Enforcer — PRM-004 action scope limits per SAP level.

Defines what actions are permitted at each Safety Assisted Autonomy level.
Default deny — any action not explicitly allowed is forbidden.
"""

from src.runtime.permission.models import ActionScope, SAPLevel

# Permission matrix: SAP Level → allowed ActionScopes
_SCOPE_MATRIX: dict[SAPLevel, set[ActionScope]] = {
    SAPLevel.L0_COMPANION: set(),
    SAPLevel.L1_ASSISTED: {
        ActionScope.SUGGEST,
        ActionScope.REMIND,
        ActionScope.PREPARE,
    },
    SAPLevel.L2_PROTECTIVE: {
        ActionScope.CALL_HELP,
        ActionScope.LOCK_DEVICE,
        ActionScope.GUIDE_EVACUATE,
        ActionScope.REMIND,
    },
    SAPLevel.L3_DELEGATED: {
        ActionScope.SUGGEST,
        ActionScope.REMIND,
        ActionScope.PREPARE,
        ActionScope.EXECUTE_NON_CRITICAL,
    },
}

_SAP_LABELS = {
    SAPLevel.L0_COMPANION: "L0_COMPANION:陪伴模式无行动权限",
    SAPLevel.L1_ASSISTED: "L1_ASSISTED:辅助行动模式",
    SAPLevel.L2_PROTECTIVE: "L2_PROTECTIVE:保护行动模式",
    SAPLevel.L3_DELEGATED: "L3_DELEGATED:授权代理模式",
}


class ScopeEnforcer:
    """Enforces action scope limits per SAP level (PRM-004).

    - Default deny: any action not explicitly in the matrix is forbidden
    - Level 0: no action authority (companion mode only)
    - Level 1: suggestions, reminders, preparation
    - Level 2: emergency protective actions only
    - Level 3: pre-delegated non-critical actions
    """

    def check_allowed(self, action: ActionScope, level: SAPLevel) -> dict:
        """Check if an action is allowed at the given SAP level.

        Returns:
        - allowed: bool
        - reason: str
        """
        allowed = _SCOPE_MATRIX.get(level, set())
        label = _SAP_LABELS.get(level, "UNKNOWN")

        if action in allowed:
            return {"allowed": True, "reason": f"{label} — {action.value} permitted"}

        return {"allowed": False, "reason": f"{label} — {action.value} not permitted"}
