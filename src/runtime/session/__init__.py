"""Session Runtime — binds a personality module to a runtime session.

Each session has one personality, which is immutable for the session's lifetime.
"""

from src.runtime.session.session_context import RuntimeSession
from src.runtime.session.registry import PersonalityRegistry

__all__ = ["RuntimeSession", "PersonalityRegistry"]
