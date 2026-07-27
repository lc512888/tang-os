"""TPI Personality Interface — Public API contracts (DIG-006~010).

DI-002-A: Interface Exposure ≠ Internal Model Exposure.
Only input/output schemas and permission requirements are public.
Internal personality mechanism is NOT exposed.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

TPI_INTERFACE_VERSION = "1.0.0"


class TPIEndpoint(Enum):
    IDENTITY = "identity"
    EMOTION = "emotion"
    DECISION = "decision"
    MEMORY = "memory"
    SAFETY = "safety"
    REALITY = "reality"
    VOICE = "voice"
    HOST = "host"


class PermissionLevel(Enum):
    READ = "read"
    WRITE = "write"
    CALL = "call"
    READ_WRITE = "read_write"


@dataclass
class TPIRequest:
    endpoint: TPIEndpoint
    payload: dict
    permission: PermissionLevel

    # DIG-009: All actions are auditable
    request_id: str = ""
    timestamp: str = ""
    source: str = ""


@dataclass
class TPIResponse:
    endpoint: TPIEndpoint
    data: dict
    permission_used: PermissionLevel
    error: str | None = None

    # DIG-009: All actions are auditable
    request_id: str = ""
    timestamp: str = ""


# ── DIG-006: Input Schema Public ────────────────────────────────────

@dataclass
class EmotionInput:
    """TPI-002 Emotion input schema."""
    text: str
    context: dict = field(default_factory=dict)


@dataclass
class DecisionInput:
    """TPI-003 Decision input schema."""
    question: str
    options: list[str] = field(default_factory=list)


@dataclass
class MemoryInput:
    """TPI-004 Memory input schema."""
    content: str
    memory_type: str = "experience"
    consent: bool = False


# ── DIG-007: Output Schema Public ──────────────────────────────────

@dataclass
class EmotionOutput:
    """TPI-002 Emotion output schema."""
    feeling: str
    need: str
    response_mode: str


@dataclass
class DecisionOutput:
    """TPI-003 Decision output schema (Core-003 compliance)."""
    situation: str
    options: list[str]
    risks: list[str]
    user_decision: None = None


# ── DIG-008: Permission Level Public ────────────────────────────────

ENDPOINT_PERMISSIONS: dict[TPIEndpoint, PermissionLevel] = {
    TPIEndpoint.IDENTITY: PermissionLevel.READ,
    TPIEndpoint.EMOTION: PermissionLevel.CALL,
    TPIEndpoint.DECISION: PermissionLevel.CALL,
    TPIEndpoint.MEMORY: PermissionLevel.READ_WRITE,
    TPIEndpoint.SAFETY: PermissionLevel.READ,
    TPIEndpoint.REALITY: PermissionLevel.WRITE,
    TPIEndpoint.VOICE: PermissionLevel.CALL,
    TPIEndpoint.HOST: PermissionLevel.READ,
}


# ── DIG-010: Version Independent ───────────────────────────────────

def get_tpi_version() -> str:
    """TPI version is independent of Runtime version."""
    return TPI_INTERFACE_VERSION
