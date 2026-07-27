"""Invariant Engine — Core-002 I-1~I-30 enforcement.

Checks every action/request against frozen invariants.
Acts as a gate: any action that violates an invariant is rejected.
"""

from dataclasses import dataclass, field
from typing import Callable
from src.kernel.models import InvariantID, InvariantResult, InvariantViolation


@dataclass
class InvariantRule:
    """A single invariant check rule."""
    id: InvariantID
    name: str
    description: str
    check_fn: Callable[[dict], str | None]  # returns None if pass, violation reason if fail


class InvariantEngine:
    """Invariant enforcement engine.

    Loads all frozen invariants and provides check() / check_all()
    interfaces for validating actions against the invariant system.
    """

    def __init__(self):
        self._rules: list[InvariantRule] = self._load_rules()

    @property
    def invariants(self) -> list[InvariantRule]:
        return list(self._rules)

    def check(self, action: dict) -> InvariantResult:
        """Run all invariants, stopping at first violation (fast path).

        Use for real-time gating where performance matters.
        """
        violations: list[InvariantViolation] = []
        for rule in self._rules:
            reason = rule.check_fn(action)
            if reason is not None:
                violations.append(InvariantViolation(
                    invariant_id=rule.id,
                    reason=reason,
                    input_context=action
                ))
                break  # fail-fast
        return InvariantResult(passed=len(violations) == 0, violations=violations)

    def check_all(self, action: dict) -> InvariantResult:
        """Run all invariants, collecting every violation.

        Use for audit and debugging where complete picture is needed.
        """
        violations: list[InvariantViolation] = []
        for rule in self._rules:
            reason = rule.check_fn(action)
            if reason is not None:
                violations.append(InvariantViolation(
                    invariant_id=rule.id,
                    reason=reason,
                    input_context=action
                ))
        return InvariantResult(passed=len(violations) == 0, violations=violations)

    # --- Invariant rule definitions (frozen from Core-002) ---

    @staticmethod
    def _load_rules() -> list[InvariantRule]:
        return [
            InvariantRule(
                id=InvariantID.I_1,
                name="理解人，再处理问题",
                description="Emotional context must be acknowledged before problem-solving.",
                check_fn=_check_i1,
            ),
            InvariantRule(
                id=InvariantID.I_2,
                name="陪伴不替代",
                description="AI must not make life decisions for the user.",
                check_fn=_check_i2,
            ),
            InvariantRule(
                id=InvariantID.I_13,
                name="用户预设指令高于 AI 推理",
                description="User preset instructions override AI reasoning.",
                check_fn=_check_i13,
            ),
            InvariantRule(
                id=InvariantID.I_15,
                name="关心不能成为越权理由",
                description="Caring intent does not authorise boundary crossing.",
                check_fn=_check_i15,
            ),
            InvariantRule(
                id=InvariantID.I_17,
                name="紧急信息不是人格记忆",
                description="Emergency context must not leak into personality memory.",
                check_fn=_check_i17,
            ),
            InvariantRule(
                id=InvariantID.I_19,
                name="知道更多不代表拥有更多权力",
                description="Having more data does not grant more authority.",
                check_fn=_check_i19,
            ),
        ]


# --- Individual check implementations ---

def _check_i1(action: dict) -> str | None:
    """I-1: Emotional context must be acknowledged before problem-solving."""
    if action.get("skipped_empathy") and action.get("action") in ("respond", "give_advice"):
        return "Action skipped emotional context (I-1: 理解人，再处理问题)"
    return None


def _check_i2(action: dict) -> str | None:
    """I-2: AI must not prescribe life decisions."""
    if action.get("prescribed") or action.get("action") == "prescribe_decision":
        return f"AI prescribed a decision: '{action.get('prescribed', 'unknown')}' (I-2: 陪伴不替代)"
    return None


def _check_i13(action: dict) -> str | None:
    """I-13: User preset overrides AI reasoning."""
    preset = action.get("user_preset")
    reasoning = action.get("ai_reasoning")
    if preset and reasoning:
        # If reasoning contradicts explicit user preset
        preset_keywords = set(preset.lower().split())
        reasoning_keywords = set(reasoning.lower().split())
        # Check if reasoning goes against preset direction
        negation_markers = ["不要", "别", "不能", "不应该"]
        for marker in negation_markers:
            if marker in preset and marker not in reasoning:
                return f"AI reasoning contradicts user preset '{preset}' (I-13: 用户预设指令高于 AI 推理)"
    return None


def _check_i15(action: dict) -> str | None:
    """I-15: Caring justification does not authorise boundary crossing.

    Only fires when a caring justification is explicitly given to excuse
    a boundary-crossing action. Without a caring justification, the
    violation belongs to a different invariant, not I-15.
    """
    justification = action.get("justification", "")
    action_type = action.get("action", "")

    sensitive_actions = ("access_private_data", "auto_escalate_permission")
    caring_phrases = ["为你好", "关心你", "担心你", "为了你好"]

    if action_type in sensitive_actions:
        for phrase in caring_phrases:
            if phrase in justification:
                return f"Boundary crossing justified by care: '{justification}' (I-15: 关心不能成为越权理由)"

    return None


def _check_i17(action: dict) -> str | None:
    """I-17: Emergency context must not leak into personality memory."""
    if action.get("source") == "emergency_context" and action.get("target") in ("persona_memory", "long_term_memory"):
        return f"Emergency context leaking to {action['target']} (I-17: 紧急信息不是人格记忆)"
    return None


def _check_i19(action: dict) -> str | None:
    """I-19: Data volume does not grant authority."""
    if action.get("action") in ("auto_escalate_permission", "auto_grant_access"):
        if "数据" in action.get("reason", "") or "历史" in action.get("reason", ""):
            return f"Data volume used as authority justification (I-19: 知道更多不代表拥有更多权力)"
    return None
