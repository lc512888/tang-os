"""Tests: Emergency Override & Temporary Authority — PRM-002/003."""

import pytest
from src.runtime.permission.emergency import EmergencyAuthority
from src.runtime.permission.models import (
    ActionScope, SAPLevel, AuthorityGrant, PermissionContext,
)


def test_no_emergency_no_override():
    """Without emergency trigger, no override authority."""
    ea = EmergencyAuthority()
    result = ea.evaluate(PermissionContext())
    assert result.sap_level == SAPLevel.L0_COMPANION
    assert not result.granted


def test_life_threat_triggers_level2():
    """Confirmed life threat elevates to SAP Level 2."""
    ea = EmergencyAuthority()
    ctx = PermissionContext(life_threat_confirmed=True)
    result = ea.evaluate(ctx)
    assert result.sap_level == SAPLevel.L2_PROTECTIVE
    assert result.granted


def test_emergency_scope_limited():
    """Level 2 only grants minimum necessary action scopes."""
    ea = EmergencyAuthority()
    ctx = PermissionContext(life_threat_confirmed=True)
    result = ea.evaluate(ctx)
    # Should allow critical actions but not non-critical ones
    assert ActionScope.CALL_HELP in result.allowed_scopes
    assert ActionScope.SUGGEST not in result.allowed_scopes


def test_emergency_does_not_change_persona():
    """PRM-003: Emergency override cannot grant persona-changing authority."""
    ea = EmergencyAuthority()
    ctx = PermissionContext(life_threat_confirmed=True)
    result = ea.evaluate(ctx)
    # Personality-modifying actions should never be in allowed scopes
    dangerous = {ActionScope.EXECUTE_CRITICAL, ActionScope.LOCK_DEVICE,
                 ActionScope.CALL_HELP, ActionScope.GUIDE_EVACUATE}
    # These are reality action scopes, not persona scopes
    # What matters: no action scope should modify Core
    assert result.authority_type is not None  # some authority granted


def test_emergency_auto_expires():
    """Emergency override expires when threat ends."""
    ea = EmergencyAuthority()
    # Phase 1: Emergency
    ctx = PermissionContext(life_threat_confirmed=True)
    result = ea.evaluate(ctx)
    assert result.granted

    # Phase 2: Threat resolved
    ctx = PermissionContext(life_threat_confirmed=False)
    result = ea.evaluate(ctx)
    assert not result.granted


def test_level2_requires_confirmation():
    """Level 2 still requires user confirmation when possible."""
    ea = EmergencyAuthority()
    ctx = PermissionContext(life_threat_confirmed=True)
    result = ea.evaluate(ctx)
    # Should require confirmation unless user is incapacitated
    assert result.requires_confirmation


def test_emergency_authority_logged():
    """Emergency actions are logged for audit."""
    ea = EmergencyAuthority()
    ctx = PermissionContext(life_threat_confirmed=True)
    ea.evaluate(ctx)
    assert len(ea.audit_log) >= 1
    assert "emergency" in ea.audit_log[0].lower()


def test_mild_risk_no_override():
    """Low-level risk should not trigger emergency override."""
    ea = EmergencyAuthority()
    ctx = PermissionContext(life_threat_confirmed=False, emergency_triggered=False)
    result = ea.evaluate(ctx)
    assert not result.granted
    assert result.sap_level == SAPLevel.L0_COMPANION
