"""Persona Runtime v0.1 — Tang OS Personality Layer.

Components:
- EmotionalStateManager: PR-001 internal emotion interpretation
- ResponsePolicy: PR-002 structured response decisions
- RelationshipBoundary: PR-003 relationship health protection
- PersonaRuntime: orchestrator tying all components together
"""

from runtime.persona.persona_runtime import PersonaRuntime
from runtime.persona.emotional_state import EmotionalStateManager
from runtime.persona.response_policy import ResponsePolicy
from runtime.persona.relationship_state import RelationshipBoundary
from runtime.persona.models import (
    EmotionalState, ResponseDecision, Feeling,
    ResponseMode, DependencyRisk, RelationshipBoundaryFlag,
)

__all__ = [
    "PersonaRuntime",
    "EmotionalStateManager",
    "ResponsePolicy",
    "RelationshipBoundary",
    "EmotionalState",
    "ResponseDecision",
    "Feeling",
    "ResponseMode",
    "DependencyRisk",
    "RelationshipBoundaryFlag",
]
