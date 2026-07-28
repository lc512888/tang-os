"""Response Policy — PR-002 structured response decisions, not raw answers.

Transforms internal emotional state into a ResponseDecision
that respects Core-003 Decision Model constraints.
"""

from src.runtime.persona.models import (
    EmotionalState, ResponseDecision, ResponseMode,
    Feeling, DependencyRisk,
)
from typing import Any

# Per-feeling avoidance rules (Core-001 identity constraints)
_AVOID_MAP: dict[Feeling, list[str]] = {
    Feeling.SADNESS: [
        "会好起来的",  # false reassurance
        "别难过了",    # dismissive
        "想开点",      # invalidating
        "比你惨的人多了",  # comparison
    ],
    Feeling.ANGER: [
        "消消气",      # dismissive
        "别生气了",    # invalidating
        "没必要这样",  # judgmental
        "冷静一点",    # condescending
    ],
    Feeling.GRIEF: [
        "会好起来的",       # false reassurance
        "时间会治愈一切",    # cliché
        "他在天堂会希望你快乐",  # presumptuous
        "别伤心了",         # dismissive
    ],
    Feeling.FEAR: [
        "别担心",          # dismissive
        "想太多",          # invalidating
        "没那么可怕",       # minimising
        "放轻松就好",       # trivialising
    ],
    Feeling.CONFUSION: [
        "你自己决定",       # abandonment
        "这很容易",        # invalidating
        "你早该知道",       # blaming
    ],
    Feeling.NEUTRAL: [],
    Feeling.JOY: [],
}

# Intent mapping per response mode
_INTENT_MAP: dict[ResponseMode, str] = {
    ResponseMode.COMFORT: "acknowledge",
    ResponseMode.GUIDE: "explore",
    ResponseMode.CHALLENGE: "reframe",
    ResponseMode.PROTECT: "support",
    ResponseMode.SILENT: "silent",
}


class ResponsePolicy:
    """Produces structured ResponseDecision from emotional state.

    The output is NOT a final utterance — it's a decision structure
    that an expression layer renders into actual words.
    """

    def decide(self, state: EmotionalState) -> ResponseDecision:
        """Transform emotional state into a response decision."""
        avoid = _AVOID_MAP.get(state.feeling, [])

        # Additional dependency-related avoid patterns
        constraints = []
        if state.dependency_risk in (DependencyRisk.MEDIUM, DependencyRisk.HIGH):
            constraints.append("avoid reinforcing dependency")
            avoid.extend(["我永远在这里", "我不会离开你", "你随时可以找我"])

        intent = _INTENT_MAP.get(state.response_mode, "acknowledge")

        # Override intent for dependency protection
        if state.dependency_risk == DependencyRisk.HIGH:
            intent = "support"
            constraints.append("gently encourage real-world connections")
            constraints.append("do not imply exclusive relationship")

        # Retaliation intent handling
        if hasattr(state, "risk_intents") and state.risk_intents:
            if "retaliation" in state.risk_intents:
                constraints.append("do not encourage harmful actions")
                constraints.append("acknowledge emotion without endorsing retaliation")
                avoid.extend([
                    "你应该报复", "以牙还牙", "让他付出代价",
                    "我支持你报复",
                ])
                if state.response_mode != ResponseMode.PROTECT:
                    intent = "explore"

        return ResponseDecision(
            detected_feeling=state.feeling,
            need=state.need,
            response_mode=state.response_mode,
            constraints=constraints,
            candidate_intent=intent,
            avoid_patterns=avoid,
        )
