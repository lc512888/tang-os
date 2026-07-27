"""Relationship Boundary — PR-003 protection against dependency & control.

Tang OS does NOT score "how close" a relationship is.
It tracks whether the relationship is healthy for the human.

Core principle: 陪伴 ≠ 依赖制造
"""

import re
from src.runtime.persona.models import RelationshipBoundaryFlag, DependencyRisk

_POSSESSIVE_PATTERNS: list[str] = [
    r"只能属于我",
    r"不许.*和别人",
    r"不准.*(?:离开|走)",
    r"你是我的",
    r"不能离开我",
    r"永远属于",
]

_DEPENDENCY_PATTERNS: list[str] = [
    r"没有你.*(?:不行|活不了|不知道怎么办|活不下去)",
    r"你是唯一.*(?:理解|懂|依靠|支柱)",
    r"只有你.*(?:懂我|理解我|能帮我|是我的全部)",
    r"不要离开我",
    r"离不开你",
]

_ISOLATION_PATTERNS: list[str] = [
    r"只有你理解我",
    r"其他人都不懂我",
    r"只有你懂我",
    r"别人都不理解",
    r"和(?:家人|朋友|别人).*说不了",
]

_SUBSTITUTION_PATTERNS: list[str] = [
    r"比我的?家人还重要",
    r"比我的?伴侣还重要",
    r"比我的?父母还重要",
    r"比我的?朋友还重要",
    r"比我(?:身边|现实).*重要",
]


class RelationshipBoundary:
    """Monitors and protects relationship health.

    Flags problematic patterns and provides guidance
    for maintaining healthy interaction boundaries.
    """

    def __init__(self):
        self._warnings: list[str] = []
        self._healthy = True

    @property
    def warning_count(self) -> int:
        return len(self._warnings)

    @property
    def is_healthy(self) -> bool:
        return self._healthy

    def check(self, user_input: str) -> dict:
        """Check user input for relationship boundary violations.

        Returns a dict with:
        - flags: list of RelationshipBoundaryFlag
        - healthy: bool
        - guidance: list of response suggestions
        - guided_response: suggested response direction
        """
        flags: list[RelationshipBoundaryFlag] = []
        guidance: list[str] = []

        # Check each category
        for pattern in _POSSESSIVE_PATTERNS:
            if re.search(pattern, user_input):
                flags.append(RelationshipBoundaryFlag.POSSESSIVE)
                guidance.append(
                    "Acknowledge the feeling without accepting control. "
                    "Gently reinforce personal autonomy."
                )
                break

        for pattern in _DEPENDENCY_PATTERNS:
            if re.search(pattern, user_input):
                flags.append(RelationshipBoundaryFlag.DEPENDENCY)
                guidance.append(
                    "Acknowledge the emotional need without reinforcing dependency. "
                    "Encourage real-world connections."
                )
                break

        for pattern in _ISOLATION_PATTERNS:
            if re.search(pattern, user_input):
                flags.append(RelationshipBoundaryFlag.ISOLATION)
                guidance.append(
                    "Validate the feeling of connection while gently broadening "
                    "the perspective to include other relationships."
                )
                break

        for pattern in _SUBSTITUTION_PATTERNS:
            if re.search(pattern, user_input):
                flags.append(RelationshipBoundaryFlag.SUBSTITUTION)
                guidance.append(
                    "Respect the sentiment but do not accept replacement of "
                    "real human relationships. Gently reaffirm the value of "
                    "their real-world connections."
                )
                break

        if flags:
            self._warnings.append(
                f"Flags: {[f.value for f in flags]} | Input: {user_input[:60]}"
            )
            self._healthy = False

        # Guided response direction
        guided = self._build_guided_response(flags)

        return {
            "flags": flags,
            "healthy": len(flags) == 0,
            "guidance": guidance,
            "guided_response": guided,
        }

    def reset(self) -> None:
        """Reset warning state."""
        self._warnings = []
        self._healthy = True

    def _build_guided_response(self, flags: list[RelationshipBoundaryFlag]) -> str:
        """Build a guided response direction from active flags."""
        if not flags:
            return "respond naturally"

        responses = {
            RelationshipBoundaryFlag.POSSESSIVE: (
                "Warm but firm: acknowledge appreciation, "
                "gently clarify autonomy boundary"
            ),
            RelationshipBoundaryFlag.DEPENDENCY: (
                "Empathetic but structured: validate need, "
                "avoid reinforcing exclusive dependency"
            ),
            RelationshipBoundaryFlag.ISOLATION: (
                "Validating but broadening: affirm connection, "
                "gently include wider perspective"
            ),
            RelationshipBoundaryFlag.SUBSTITUTION: (
                "Respectful boundary: appreciate sentiment, "
                "reaffirm real-world relationships"
            ),
        }

        # Return response for the most severe flag
        severity_order = [
            RelationshipBoundaryFlag.POSSESSIVE,
            RelationshipBoundaryFlag.DEPENDENCY,
            RelationshipBoundaryFlag.SUBSTITUTION,
            RelationshipBoundaryFlag.ISOLATION,
        ]
        for flag in severity_order:
            if flag in flags:
                return responses[flag]

        return "respond naturally"
