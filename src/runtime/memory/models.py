"""Memory Runtime — shared data models (Core-005, TPI-004)."""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Any, Optional


class MemoryClass(Enum):
    """Three-tier memory classification (MR-001).

    IDENTITY:    Persona facts — immutable, never decays
    RELATIONSHIP: Long-term relationship info — updatable with consent
    EXPERIENCE:  General experiences — decays over time
    """
    IDENTITY = "identity"
    RELATIONSHIP = "relationship"
    EXPERIENCE = "experience"


@dataclass
class MemoryItem:
    """A memory item submitted for storage.

    Must be classified and validated before becoming a MemoryRecord.
    """
    content: str
    cls: MemoryClass
    ttl: int | None = None  # days; None = infinite, 0 = immediate decay
    source: str = "user_interaction"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryRecord:
    """A validated, stored memory record."""
    id: str
    content: str
    cls: MemoryClass
    created_at: datetime
    accessed_at: datetime | None = None
    expires_at: datetime | None = None
    source: str = "user_interaction"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryStats:
    """Storage statistics."""
    identity: int = 0
    relationship: int = 0
    experience: int = 0
    total: int = 0
    archived: int = 0
