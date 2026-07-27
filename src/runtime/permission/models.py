"""Permission Runtime — shared data models.

Defines the "law of permitted action" for Tang OS.
"""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Any


class SAPLevel(Enum):
    """Safety Assisted Autonomy Principle — three levels (SAP-001)."""
    L0_COMPANION = 0        # 建议/解释/支持
    L1_ASSISTED = 1         # 提醒/确认/准备
    L2_PROTECTIVE = 2       # 生命风险下的最小必要行动
    L3_DELEGATED = 3        # 用户预先授权的长期代理


class AuthorityType(Enum):
    """Types of authority grants."""
    USER_CONSENT = "user_consent"           # Standard user permission
    EMERGENCY_OVERRIDE = "emergency"        # Temporary life-safety override
    PRE_DELEGATED = "pre_delegated"         # Pre-authorized long-term proxy


class ActionScope(Enum):
    """Categories of actions subject to permission."""
    SUGGEST = "suggest"                     # Verbal suggestion only
    REMIND = "remind"                       # Notification/alert
    PREPARE = "prepare"                     # Prepare resource/info
    EXECUTE_NON_CRITICAL = "execute_non"    # Non-critical automated action
    EXECUTE_CRITICAL = "execute_critical"   # Life-safety automated action
    CALL_HELP = "call_help"                 # Contact emergency services
    LOCK_DEVICE = "lock_device"             # Disable hazardous equipment
    GUIDE_EVACUATE = "guide_evacuate"       # Guide to safety


@dataclass
class AuthorityGrant:
    """A single authority grant with scope, duration, and conditions."""
    authority_type: AuthorityType
    scope: list[ActionScope]
    sap_level: SAPLevel
    granted_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime | None = None
    reason: str = ""
    granted_by: str = "user"

    @property
    def is_active(self) -> bool:
        if self.expires_at is None:
            return True
        return datetime.now() < self.expires_at


@dataclass
class PermissionContext:
    """Full context for a permission evaluation."""
    current_sap_level: SAPLevel = SAPLevel.L0_COMPANION
    user_consent: bool = False
    life_threat_confirmed: bool = False
    emergency_triggered: bool = False
    pre_delegated: bool = False
    pending_grants: list[AuthorityGrant] = field(default_factory=list)


@dataclass
class PermissionVerdict:
    """Result of a permission evaluation."""
    granted: bool
    sap_level: SAPLevel
    authority_type: AuthorityType | None = None
    allowed_scopes: list[ActionScope] = field(default_factory=list)
    reason: str = ""
    requires_confirmation: bool = True
