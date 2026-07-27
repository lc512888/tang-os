"""Permission Runtime v0.1 — Tang OS Permission System.

Components:
- ConsentManager: PRM-001 user consent management
- EmergencyAuthority: PRM-002/003 emergency override & temporary authority
- ScopeEnforcer: PRM-004 action scope limits per SAP level
- RecoveryManager: PRM-005 recovery to normal state
- PermissionRuntime: orchestrator
"""

from src.runtime.permission.permission_runtime import PermissionRuntime
from src.runtime.permission.consent import ConsentManager
from src.runtime.permission.emergency import EmergencyAuthority
from src.runtime.permission.scope import ScopeEnforcer
from src.runtime.permission.recovery import RecoveryManager
from src.runtime.permission.models import (
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
