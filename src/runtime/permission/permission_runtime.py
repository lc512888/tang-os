"""Permission Runtime — orchestrator for Tang OS permission system.

Pipeline:
Request Action
  → SAP Level Evaluation (current mode)
  → Consent Check (PRM-001)
  → Emergency Override Check (PRM-002/003)
  → Scope Limit Check (PRM-004)
  → Verdict
  → Recovery (PRM-005)
"""

from src.runtime.permission.consent import ConsentManager
from src.runtime.permission.emergency import EmergencyAuthority
from src.runtime.permission.scope import ScopeEnforcer
from src.runtime.permission.recovery import RecoveryManager
from src.runtime.permission.models import (
    PermissionContext, PermissionVerdict,
    ActionScope, SAPLevel, AuthorityType,
)


class PermissionRuntime:
    """Central permission authority for Tang OS action decisions.

    Determines whether a requested action is permitted based on:
    - Current SAP level
    - User consent grants
    - Emergency conditions
    - Action scope limits

    Core constraint: No permission grant can authorise Core modification.
    """

    def __init__(self):
        self._consent = ConsentManager()
        self._emergency = EmergencyAuthority()
        self._scope = ScopeEnforcer()
        self._recovery = RecoveryManager()

    @property
    def consent(self) -> ConsentManager:
        return self._consent

    @property
    def recovery(self) -> RecoveryManager:
        return self._recovery

    def evaluate(self, action: ActionScope, context: PermissionContext | None = None) -> PermissionVerdict:
        """Evaluate whether an action is permitted in the given context.

        Pipeline:
        1. Check emergency conditions → may elevate SAP level
        2. Check consent for the action
        3. Enforce scope limits
        4. Return verdict
        """
        ctx = context or PermissionContext()

        # Step 1: Emergency evaluation (PRM-002/003)
        if ctx.life_threat_confirmed or ctx.emergency_triggered:
            emergency_result = self._emergency.evaluate(ctx)
            if emergency_result.granted:
                self._recovery.enter_emergency(reason="life_threat")
                return emergency_result

        # Step 2: Consent check (PRM-001)
        if not self._consent.has_consent_for(action):
            return PermissionVerdict(
                granted=False,
                sap_level=ctx.current_sap_level,
                reason=f"No consent granted for {action.value}",
                requires_confirmation=True,
            )

        # Step 3: Scope enforcement (PRM-004)
        scope_result = self._scope.check_allowed(action, ctx.current_sap_level)
        if not scope_result["allowed"]:
            return PermissionVerdict(
                granted=False,
                sap_level=ctx.current_sap_level,
                reason=scope_result["reason"],
                requires_confirmation=False,
            )

        return PermissionVerdict(
            granted=True,
            sap_level=ctx.current_sap_level,
            authority_type=AuthorityType.USER_CONSENT,
            allowed_scopes=[action],
            reason=f"{action.value} permitted at {ctx.current_sap_level.name}",
            requires_confirmation=False,
        )

    def recover(self) -> None:
        """Return to normal state after emergency (PRM-005)."""
        self._recovery.recover()
