"""RuntimeSession — binds a personality module to a single runtime session.

A session has one personality, which is immutable for its lifetime.
The personality controls identity, values, boundaries, style, and
emotional policy for all interactions within this session.
"""

import uuid
from datetime import datetime, timezone
from typing import Any

from src.runtime.personality_loader import PersonalityModule


_SESSION_ID_PREFIX = "sess_"


class RuntimeSession:
    """A runtime session bound to a specific personality module.

    Usage:
        module = PersonalityLoader(path).load()
        session = RuntimeSession(module)
        print(session.personality.name)  # "tang"
        print(session.identity["role"])  # "companion"
    """

    def __init__(self, personality: PersonalityModule):
        self._session_id: str = f"{_SESSION_ID_PREFIX}{uuid.uuid4().hex[:12]}"
        self._personality: PersonalityModule = personality
        self._created_at: str = datetime.now(timezone.utc).isoformat()
        self._metadata: dict[str, Any] = {}

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def personality(self) -> PersonalityModule:
        """The bound personality module. Immutable for session lifetime."""
        return self._personality

    @property
    def identity(self) -> dict:
        return self._personality.identity

    @property
    def values(self) -> dict:
        return self._personality.values

    @property
    def boundaries(self) -> dict:
        return self._personality.boundaries

    @property
    def style(self) -> dict:
        return self._personality.style

    @property
    def emotional_policy(self) -> dict:
        return self._personality.emotional_policy

    @property
    def capabilities(self) -> dict:
        return self._personality.capabilities

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def metadata(self) -> dict:
        return self._metadata

    def summary(self) -> dict:
        return {
            "session_id": self._session_id,
            "personality": self._personality.name,
            "version": self._personality.version,
            "created_at": self._created_at,
        }
