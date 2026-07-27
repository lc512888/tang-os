"""Persona Runtime — orchestrator for emotional state, response policy, and relationship boundary.

Sits between Kernel (Identity / Invariant / State) and external interaction.
Implements the pipeline: Input → Feel → Need → Risk Check → Response Mode.
"""

from src.runtime.persona.emotional_state import EmotionalStateManager
from src.runtime.persona.response_policy import ResponsePolicy
from src.runtime.persona.relationship_state import RelationshipBoundary
from src.runtime.persona.models import (
    EmotionalState, ResponseDecision, RelationshipProfile,
    Feeling, ResponseMode, DependencyRisk,
)


class PersonaRuntime:
    """Orchestrates persona-level processing for a single interaction.

    Pipeline:
    User Input
      → EmotionalStateManager (detect feeling, need, risk)
      → RelationshipBoundary (check for dependency/control patterns)
      → ResponsePolicy (produce structured response decision)
      → Output
    """

    def __init__(self):
        self._emotion = EmotionalStateManager()
        self._policy = ResponsePolicy()
        self._relationship = RelationshipBoundary()

    @property
    def emotional_state(self) -> EmotionalState:
        """Current internal emotional state (read-only)."""
        return self._emotion.current_feeling  # returns Feeling actually

    @property
    def current_feeling(self) -> Feeling:
        return self._emotion.current_feeling

    @property
    def current_intensity(self) -> float:
        return self._emotion.current_intensity

    @property
    def relationship_healthy(self) -> bool:
        return self._relationship.is_healthy

    @property
    def warning_count(self) -> int:
        return self._relationship.warning_count

    def process(self, user_input: str) -> dict:
        """Process a single user input through the full persona pipeline.

        Returns:
        - emotional_state: detected internal state
        - relationship: boundary check result
        - response_decision: structured response decision
        """
        # Step 1: Emotional interpretation
        emotional = self._emotion.process(user_input)

        # Step 2: Relationship boundary check
        relationship = self._relationship.check(user_input)

        # Step 3: Response policy
        decision = self._policy.decide(emotional)

        return {
            "emotional_state": emotional,
            "relationship": relationship,
            "response_decision": decision,
        }

    def reset_session(self) -> None:
        """Reset session-level state (preserves long-term relationship profile)."""
        self._emotion.reset()
