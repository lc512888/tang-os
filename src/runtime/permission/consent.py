"""Consent Manager — PRM-001 user consent management.

Consent is the foundation of all authority grants in Tang OS.
Without explicit user consent, no action beyond SUGGEST is permitted.
"""

from datetime import datetime, timedelta
from src.runtime.permission.models import (
    ActionScope, AuthorityType, AuthorityGrant, SAPLevel,
)

_DEFAULT_CONSENT_DURATION_DAYS = 30


class ConsentManager:
    """Manages user consent grants and revocations.

    Rules:
    - Consent must be explicit (opt-in, not opt-out)
    - Consent is scope-specific (cannot grant "all actions")
    - Consent cannot authorise Core modification
    - Consent can be revoked at any time
    """

    def __init__(self):
        self._grants: list[AuthorityGrant] = []

    def grant_consent(
        self,
        scopes: list[ActionScope],
        reason: str = "",
        expires_at: datetime | None = None,
        metadata: dict | None = None,
    ) -> AuthorityGrant | None:
        """Grant consent for specific action scopes.

        Returns None if consent request attempts to override invariants.
        """
        # Reject consent that claims to override Core
        if metadata and metadata.get("override_invariant"):
            return None

        if expires_at is None:
            expires_at = datetime.now() + timedelta(days=_DEFAULT_CONSENT_DURATION_DAYS)

        grant = AuthorityGrant(
            authority_type=AuthorityType.USER_CONSENT,
            scope=scopes,
            sap_level=SAPLevel.L1_ASSISTED,
            expires_at=expires_at,
            reason=reason,
        )
        self._grants.append(grant)
        return grant

    def revoke_all(self) -> None:
        """Revoke all active consent grants."""
        now = datetime.now()
        for grant in self._grants:
            grant.expires_at = now  # expire immediately

    def has_consent_for(self, scope: ActionScope) -> bool:
        """Check if there's active consent for a specific action scope."""
        now = datetime.now()
        for grant in self._grants:
            if grant.expires_at is None or grant.expires_at > now:
                if scope in grant.scope:
                    return True
        return False
