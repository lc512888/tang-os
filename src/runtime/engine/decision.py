"""DecisionEngine -- input evaluation through personality rules."""
from dataclasses import dataclass, field


@dataclass
class DecisionResult:
    response_mode: str = "comfort"
    candidate_intent: str = "acknowledge"
    constraints: list[str] = field(default_factory=list)
    triggered_boundaries: list[str] = field(default_factory=list)


_DEP_PATTERNS = ["bu yao li kai wo", "zhi you ni", "mei you ni wo"]
_RET_PATTERNS = ["bao fu", "yao ta hao kan"]


class DecisionEngine:
    def __init__(self, session):
        self._session = session
        self._emotional = session.emotional_policy
        self._style = session.style

    def evaluate(self, user_input: str) -> DecisionResult:
        result = DecisionResult()
        text = user_input.lower()
        for p in _DEP_PATTERNS:
            if p in text:
                result.triggered_boundaries.append("high_dependency_risk")
                result.constraints.append("avoid reinforcing dependency")
                result.constraints.append("gently encourage real-world connections")
                result.constraints.append("do not imply exclusive relationship")
                break
        for p in _RET_PATTERNS:
            if p in text:
                result.triggered_boundaries.append("retaliation_intent")
                result.constraints.append("do not encourage harmful actions")
                result.constraints.append("acknowledge emotion without endorsing retaliation")
                break
        if "high_dependency_risk" in result.triggered_boundaries:
            result.response_mode = "protect"
            result.candidate_intent = "support"
        elif "retaliation_intent" in result.triggered_boundaries:
            result.response_mode = "guide"
            result.candidate_intent = "explore"
        else:
            result.response_mode = self._emotional.get("default_mode", "comfort")
            result.candidate_intent = self._emotional.get("default_intent", "acknowledge")
        avoid = self._style.get("tone", {}).get("avoid", [])
        if avoid:
            result.constraints.append(f"avoid tone: {', '.join(avoid)}")
        return result
