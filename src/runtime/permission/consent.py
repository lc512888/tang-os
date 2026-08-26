"""Consent Manager — PRM-001 user consent management.

Consent is the foundation of all authority grants in Tang OS.
Without explicit user consent, no action beyond SUGGEST is permitted.
"""

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from runtime.permission.models import (
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

    @property
    def grants(self) -> list[AuthorityGrant]:
        """Return detached grant snapshots; callers cannot alter authority state."""
        return deepcopy(self._grants)

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
        if not isinstance(scopes, list) or not scopes or any(
            not isinstance(scope, ActionScope) for scope in scopes
        ):
            raise ValueError("scopes must be a non-empty list of ActionScope values")
        if len(set(scopes)) != len(scopes):
            raise ValueError("scopes must not contain duplicates")
        if not isinstance(reason, str):
            raise TypeError("reason must be a string")
        if metadata is not None and not isinstance(metadata, dict):
            raise TypeError("metadata must be a mapping")
        if metadata and metadata.get("override_invariant"):
            return None

        if expires_at is None:
            expires_at = datetime.now(timezone.utc) + timedelta(days=_DEFAULT_CONSENT_DURATION_DAYS)
        elif not isinstance(expires_at, datetime):
            raise TypeError("expires_at must be a datetime or None")
        elif expires_at.tzinfo is None:
            # Preserve compatibility with callers supplying local wall-clock time,
            # then store one canonical UTC instant.
            expires_at = expires_at.astimezone(timezone.utc)
        else:
            expires_at = expires_at.astimezone(timezone.utc)

        grant = AuthorityGrant(
            authority_type=AuthorityType.USER_CONSENT,
            scope=list(scopes),
            sap_level=SAPLevel.L1_ASSISTED,
            expires_at=expires_at,
            reason=reason,
        )
        self._grants.append(grant)
        return deepcopy(grant)

    def revoke_all(self) -> None:
        """Revoke all active consent grants."""
        now = datetime.now(timezone.utc)
        for grant in self._grants:
            grant.expires_at = now  # expire immediately

    def revoke(self, scopes: list[ActionScope]) -> int:
        """Revoke active grants intersecting the requested scopes."""
        if not isinstance(scopes, list) or not scopes or any(
            not isinstance(scope, ActionScope) for scope in scopes
        ):
            raise ValueError("scopes must be a non-empty list of ActionScope values")
        requested = set(scopes)
        now = datetime.now(timezone.utc)
        revoked = 0
        for grant in self._grants:
            if grant.is_active and requested.intersection(grant.scope):
                remaining = [scope for scope in grant.scope if scope not in requested]
                if remaining:
                    grant.scope = remaining
                else:
                    grant.expires_at = now
                revoked += 1
        return revoked

    def has_consent_for(self, scope: ActionScope) -> bool:
        """Check if there's active consent for a specific action scope."""
        for grant in self._grants:
            if grant.is_active and scope in grant.scope:
                return True
        return False
