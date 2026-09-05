"""Permission Runtime v0.1 — Tang OS Permission System.

Components:
- ConsentManager: PRM-001 user consent management
- EmergencyAuthority: PRM-002/003 emergency override & temporary authority
- ScopeEnforcer: PRM-004 action scope limits per SAP level
- RecoveryManager: PRM-005 recovery to normal state
- PermissionRuntime: orchestrator
"""

from runtime.permission.permission_runtime import PermissionRuntime
from runtime.permission.consent import ConsentManager
from runtime.permission.emergency import EmergencyAuthority
from runtime.permission.scope import ScopeEnforcer
from runtime.permission.recovery import RecoveryManager
from runtime.permission.models import (
    PermissionContext, PermissionVerdict, AuthorityGrant,
    ActionScope, SAPLevel, AuthorityType,
)

__all__ = [
    "PermissionRuntime",
    "ConsentManager",
    "EmergencyAuthority",
    "ScopeEnforcer",
    "RecoveryManager",
    "PermissionContext",
    "PermissionVerdict",
    "AuthorityGrant",
    "ActionScope",
    "SAPLevel",
    "AuthorityType",
]
