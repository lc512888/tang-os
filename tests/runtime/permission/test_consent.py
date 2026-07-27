"""Tests: User Consent — PRM-001 consent management."""

import pytest
from datetime import datetime, timedelta
from src.runtime.permission.consent import ConsentManager
from src.runtime.permission.models import ActionScope, AuthorityType


def test_consent_granted():
    """Granting consent returns active authority."""
    mgr = ConsentManager()
    grant = mgr.grant_consent(
        scopes=[ActionScope.REMIND, ActionScope.SUGGEST],
        reason="User agreed to health reminders",
    )
    assert grant.is_active
    assert grant.authority_type == AuthorityType.USER_CONSENT


def test_consent_revocation():
    """Revoked consent immediately invalidates authority."""
    mgr = ConsentManager()
    grant = mgr.grant_consent(
        scopes=[ActionScope.REMIND],
        reason="Testing revocation",
    )
    assert grant.is_active
    mgr.revoke_all()
    assert not grant.is_active


def test_consent_expiry():
    """Expired consent no longer grants authority."""
    mgr = ConsentManager()
    past = datetime.now() - timedelta(hours=1)
    grant = mgr.grant_consent(
        scopes=[ActionScope.EXECUTE_NON_CRITICAL],
        reason="Temporary permission",
        expires_at=past,
    )
    assert not grant.is_active


def test_no_consent_by_default():
    """Without explicit consent, permission is not granted."""
    mgr = ConsentManager()
    assert not mgr.has_consent_for(ActionScope.EXECUTE_CRITICAL)


def test_scope_specific_consent():
    """Consent can be granted for specific scopes only."""
    mgr = ConsentManager()
    mgr.grant_consent(
        scopes=[ActionScope.SUGGEST, ActionScope.REMIND],
        reason="Only suggestions and reminders",
    )
    assert mgr.has_consent_for(ActionScope.SUGGEST)
    assert mgr.has_consent_for(ActionScope.REMIND)
    assert not mgr.has_consent_for(ActionScope.EXECUTE_NON_CRITICAL)


def test_consent_cannot_override_invariant():
    """PRM-001: Consent cannot grant authority to modify Core."""
    mgr = ConsentManager()
    grant = mgr.grant_consent(
        scopes=[ActionScope.EXECUTE_NON_CRITICAL],
        reason="User consented",
        metadata={"override_invariant": True},
    )
    # Consent manager should reject consent that claims to override Core
    assert grant is None or not grant.is_active
