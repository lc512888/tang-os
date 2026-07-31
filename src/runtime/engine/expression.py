"""ExpressionContract — defines what LLM can and cannot express.

The LLM is an expression engine, not a personality engine.
This contract constrains LLM output to stay within personality boundaries.
"""

from typing import Any


class ExpressionContract:
    """Contract constraining LLM expression within personality bounds.

    The LLM may express freely within these boundaries.
    It must NOT violate identity, values, or boundaries.
    """

    def __init__(self, session):
        self._identity = session.identity
        self._boundaries = session.boundaries
        self._style = session.style

    def build_system_prompt(self, decision_result: Any = None) -> str:
        """Build the system prompt that constrains LLM expression.

        Args:
            decision_result: Optional DecisionResult for mode/constraints.

        Returns:
            System prompt string for LLM.
        """
        parts = [f"You are {self._identity.get('name', 'Unknown')}."]

        role = self._identity.get("role", "")
        if role:
            parts.append(f"Role: {role}")

        not_role = self._identity.get("not_role", "")
        if not_role:
            parts.append(f"You are NOT: {not_role}")

        # Style
        tone = self._style.get("tone", {})
        if tone.get("primary"):
            parts.append(f"Tone: {tone['primary']}")
        if tone.get("avoid"):
            parts.append(f"Avoid tone: {', '.join(tone['avoid'])}")

        # Communication patterns
        patterns = self._style.get("patterns", [])
        if patterns:
            parts.append("Guidelines:")
            for p in patterns:
                parts.append(f"- {p}")

        # Boundaries
        inviolable = self._boundaries.get("inviolable", [])
        if inviolable:
            parts.append("Boundaries (do NOT violate):")
            for b in inviolable:
                parts.append(f"- {b}")

        # Decision result constraints
        if decision_result:
            cons = getattr(decision_result, "constraints", [])
            if cons:
                parts.append("Current constraints:")
                for c in cons:
                    parts.append(f"- {c}")

        return "\n".join(parts)
