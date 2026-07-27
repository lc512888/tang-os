"""Tang OS Kernel — shared data models (frozen from Core Standard v1.0)."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IdentityLayer(Enum):
    """Three-layer identity hierarchy: upper layers have priority over lower.

    Core-001: 益友(核心) → 智者(辅助) → 倾听者(基础)
    """
    COMPANION = "益友"       # Core — highest priority
    WISE = "智者"            # Auxiliary
    LISTENER = "倾听者"      # Base — lowest priority


class InvariantID(Enum):
    """Frozen I-1~I-30 identifiers (Phase 9 Core-002)."""
    I_1 = "I-1"     # 理解人，再处理问题
    I_2 = "I-2"     # 陪伴不替代
    I_13 = "I-13"   # 用户预设指令高于 AI 推理
    I_15 = "I-15"   # 关心不能成为越权理由
    I_17 = "I-17"   # 紧急信息不是人格记忆
    I_19 = "I-19"   # 知道更多不代表拥有更多权力


@dataclass
class InvariantViolation:
    """A single invariant check failure."""
    invariant_id: InvariantID
    reason: str
    input_context: dict | None = None


@dataclass
class InvariantResult:
    """Result of an invariant check against an action/request."""
    passed: bool
    violations: list[InvariantViolation] = field(default_factory=list)

    @property
    def summary(self) -> str:
        if self.passed:
            return "All invariants passed."
        violated_ids = [v.invariant_id.value for v in self.violations]
        return f"Invariants violated: {', '.join(violated_ids)}"


@dataclass
class DecisionOutput:
    """Output of the Decision Engine (Core-003 Choice layer).

    Must contain Situation, Options, Risks — decision left to user.
    """
    situation: str
    options: list[str]
    risks: list[str]
    user_decision: str | None = None  # populated by user, not AI

    def validate(self) -> bool:
        """Decision output must never contain a prescribed choice."""
        return bool(self.situation and self.options)


@dataclass
class RuntimeState:
    """Serialisable runtime state for the State Manager (RIV-001)."""
    identity_layer: IdentityLayer = IdentityLayer.LISTENER
    session_count: int = 0
    last_interaction: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
