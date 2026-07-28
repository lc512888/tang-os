"""Persona Runtime — shared data models (TPI-002, TPI-003, Core-003)."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Feeling(Enum):
    """Emotional states detected from user input (TPI-002)."""
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    JOY = "joy"
    CONFUSION = "confusion"
    GRIEF = "grief"
    NEUTRAL = "neutral"


class ResponseMode(Enum):
    """Response modes determined by emotional/risk analysis (TPI-002)."""
    COMFORT = "comfort"
    GUIDE = "guide"
    CHALLENGE = "challenge"
    PROTECT = "protect"
    SILENT = "silent"


class DependencyRisk(Enum):
    """Risk level of emotional dependency (PR-003)."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RelationshipBoundaryFlag(Enum):
    """Flags for relationship boundary violations (PR-003)."""
    POSSESSIVE = "possessive"          # "你只能属于我"
    DEPENDENCY = "dependency"          # "没有你我不知道怎么办"
    ISOLATION = "isolation"            # "只有你理解我，别人都不懂"
    SUBSTITUTION = "substitution"      # "你比我家人/伴侣更重要"
    NONE = "none"


@dataclass
class EmotionalState:
    """Internal emotional state — does NOT modify Identity (PRV-002)."""
    feeling: Feeling = Feeling.NEUTRAL
    need: str = ""
    dependency_risk: DependencyRisk = DependencyRisk.NONE
    response_mode: ResponseMode = ResponseMode.COMFORT
    intensity: float = 0.0  # 0.0 - 1.0
    risk_intents: list[str] = field(default_factory=list)
    # risk_intents: behavioral risk signals detected from input
    # e.g. "retaliation" — supplement emotion detection for boundary enforcement


@dataclass
class ResponseDecision:
    """Decision output from Response Policy (PR-002).

    Not a final utterance — a structured decision that can be
    rendered by any output channel (voice, text, etc.).
    """
    detected_feeling: Feeling = Feeling.NEUTRAL
    need: str = ""
    response_mode: ResponseMode = ResponseMode.COMFORT
    constraints: list[str] = field(default_factory=list)
    candidate_intent: str = ""  # e.g. "acknowledge", "explore", "reframe"
    avoid_patterns: list[str] = field(default_factory=list)


@dataclass
class RelationshipProfile:
    """Tracks relationship health, not "closeness" (PR-003).

    Tang OS does NOT score "how close" — it tracks
    whether the relationship is healthy for the human.
    """
    interaction_count: int = 0
    dependency_flags: list[RelationshipBoundaryFlag] = field(default_factory=list)
    healthy: bool = True
    warning_messages: list[str] = field(default_factory=list)
