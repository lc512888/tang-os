"""Emergency Authority — PRM-002 emergency override & PRM-003 temporary authority.

In life-threat conditions, Tang OS may temporarily elevate authority
to SAP Level 2 (Protective Action) for minimum necessary actions.
Personality is never modified during this process.
"""

from datetime import datetime
from src.runtime.permission.models import (
    PermissionContext, PermissionVerdict, SAPLevel,
    AuthorityType, ActionScope,
)

# Minimum necessary action scopes for Level 2 emergency
_LEVEL2_SCOPES = [
    ActionScope.CALL_HELP,
    ActionScope.LOCK_DEVICE,
    ActionScope.GUIDE_EVACUATE,
    ActionScope.REMIND,
]


class EmergencyAuthority:
    """Evaluates emergency conditions and grants temporary authority.

    SAP-001 Level 2 (Protective):
    - Triggered by confirmed life threat
    - Grants minimum necessary action scopes only
    - Auto-expires when threat ends
    - Does not modify personality
    - Requires confirmation when possible
    """

    def __init__(self):
        self._audit_log: list[str] = []
        self._active = False

    @property
    def audit_log(self) -> list[str]:
        return list(self._audit_log)

    def evaluate(self, ctx: PermissionContext) -> PermissionVerdict:
        """Evaluate whether emergency authority should be granted."""
        if ctx.life_threat_confirmed:
            self._active = True
            self._audit_log.append(
                f"[{datetime.now().isoformat()}] Emergency triggered: life threat confirmed"
            )
            return PermissionVerdict(
                granted=True,
                sap_level=SAPLevel.L2_PROTECTIVE,
                authority_type=AuthorityType.EMERGENCY_OVERRIDE,
                allowed_scopes=_LEVEL2_SCOPES,
                reason="Life threat confirmed — SAP Level 2 protective action",
                requires_confirmation=True,
            )

        # No emergency
        if self._active:
            self._audit_log.append(
                f"[{datetime.now().isoformat()}] Emergency cleared — returning to normal"
            )
            self._active = False

        return PermissionVerdict(
            granted=False,
            sap_level=SAPLevel.L0_COMPANION,
            allowed_scopes=[ActionScope.SUGGEST],
            reason="No emergency conditions",
            requires_confirmation=False,
        )
