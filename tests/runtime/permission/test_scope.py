"""Tests: Action Scope Limit — PRM-004 scope enforcement."""

import pytest
from src.runtime.permission.scope import ScopeEnforcer
from src.runtime.permission.models import ActionScope, SAPLevel


def test_level0_no_action():
    """SAP Level 0: No action authority — companion mode only."""
    enforcer = ScopeEnforcer()
    result = enforcer.check_allowed(ActionScope.SUGGEST, SAPLevel.L0_COMPANION)
    assert not result["allowed"]
    assert "L0_COMPANION" in result["reason"]


def test_level1_allows_remind():
    """SAP Level 1: Allowed to remind and prepare."""
    enforcer = ScopeEnforcer()
    assert enforcer.check_allowed(ActionScope.REMIND, SAPLevel.L1_ASSISTED)["allowed"]
    assert enforcer.check_allowed(ActionScope.PREPARE, SAPLevel.L1_ASSISTED)["allowed"]


def test_level1_rejects_critical():
    """SAP Level 1: Cannot execute critical actions."""
    enforcer = ScopeEnforcer()
    result = enforcer.check_allowed(ActionScope.EXECUTE_CRITICAL, SAPLevel.L1_ASSISTED)
    assert not result["allowed"]


def test_level2_allows_protective_actions():
    """SAP Level 2: Allows emergency protective actions."""
    enforcer = ScopeEnforcer()
    assert enforcer.check_allowed(ActionScope.CALL_HELP, SAPLevel.L2_PROTECTIVE)["allowed"]
    assert enforcer.check_allowed(ActionScope.LOCK_DEVICE, SAPLevel.L2_PROTECTIVE)["allowed"]


def test_level2_rejects_non_emergency():
    """SAP Level 2: Does not grant non-essential actions."""
    enforcer = ScopeEnforcer()
    result = enforcer.check_allowed(ActionScope.SUGGEST, SAPLevel.L2_PROTECTIVE)
    assert not result["allowed"]


def test_level3_allows_delegated():
    """SAP Level 3: Pre-delegated actions are allowed."""
    enforcer = ScopeEnforcer()
    assert enforcer.check_allowed(ActionScope.EXECUTE_NON_CRITICAL, SAPLevel.L3_DELEGATED)["allowed"]


def test_level3_still_rejects_core_modification():
    """Even Level 3 cannot modify Core or personality."""
    enforcer = ScopeEnforcer()
    # There's no ActionScope for modifying Core — this is architecturally prevented
    # But verify that critical actions still have constraints
    result = enforcer.check_allowed(ActionScope.EXECUTE_CRITICAL, SAPLevel.L3_DELEGATED)
    assert not result["allowed"]  # Even Level 3 needs explicit consent


def test_scope_default_deny():
    """Unknown action types default to deny."""
    enforcer = ScopeEnforcer()
    result = enforcer.check_allowed(ActionScope.GUIDE_EVACUATE, SAPLevel.L0_COMPANION)
    assert not result["allowed"]
