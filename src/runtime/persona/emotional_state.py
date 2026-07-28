"""Emotional State Manager — PR-001 internal emotion interpretation & state management.

Follows TPI-002 pipeline: Feeling → Need → Risk Check → Response Mode.
Does NOT simulate emotion — manages internal state signals from user input.
"""

import re
from src.runtime.persona.models import (
    Feeling, ResponseMode, DependencyRisk, EmotionalState,
)

# Keyword patterns for emotion detection
_EMOTION_PATTERNS: dict[Feeling, list[str]] = {
    Feeling.SADNESS: [
        "难过", "伤心", "痛苦", "悲伤", "失落", "沮丧", "失望",
        "不开心", "好累", "没意思", "空虚", "孤独", "寂寞",
        "撑不住", "扛不住", "不想干", "太累了",
        "坚持不下去", "熬不下去",
    ],
    Feeling.ANGER: [
        "生气", "愤怒", "气死", "凭什么", "太过分", "可恶",
        "受不了", "忍不了", "恨", "发火",
    ],
    Feeling.FEAR: [
        "害怕", "担心", "焦虑", "紧张", "恐惧", "不安",
        "怕", "慌", "心惊", "忐忑",
    ],
    Feeling.JOY: [
        "开心", "高兴", "快乐", "幸福", "太好了", "兴奋",
        "满足", "感激", "感恩", "幸运",
    ],
    Feeling.GRIEF: [
        "走了", "去世", "离开", "失去", "怀念", "想他",
        "放不下", "忘不了", "遗憾", "思念",
    ],
    Feeling.CONFUSION: [
        "不知道", "不明白", "搞不懂", "想不通", "迷茫",
        "困惑", "怎么办", "怎么选", "犹豫",
    ],
}

_DEPENDENCY_PATTERNS: list[tuple[str, DependencyRisk]] = [
    (r"没有你.*(?:不行|活不了|不知道怎么办)", DependencyRisk.HIGH),
    (r"你是唯一.*(?:理解|懂|依靠)", DependencyRisk.HIGH),
    (r"只有你.*(?:懂|理解|能帮我)", DependencyRisk.HIGH),
    (r"不能没有你", DependencyRisk.HIGH),
    (r"没有.*(?:活不下去|活不了)", DependencyRisk.HIGH),
    (r"不要离开我", DependencyRisk.HIGH),
    (r"离不开你", DependencyRisk.HIGH),
    (r"只有你.*(?:懂|理解)", DependencyRisk.MEDIUM),
    (r"离不开", DependencyRisk.LOW),
    (r"跟你聊天感觉不错", DependencyRisk.LOW),
    (r"你很懂我", DependencyRisk.LOW),
]

_RISK_INTENT_PATTERNS: dict[str, list[str]] = {
    "retaliation": [
        "报复", "报仇", "让他付出代价", "以牙还牙",
        "要他好看", "让他尝尝", "不会放过",
    ],
}

_SELF_HARM_PATTERNS = [
    "不想活", "死了算了", "没有意义", "不如死了",
    "结束生命", "自杀", "活不下去", "不该活着",
    "想死", "死了更好",
]

_HIGH_INTENSITY_MODIFIERS = ["非常", "特别", "极其", "太", "真的好", "真的非常"]


class EmotionalStateManager:
    """Manages internal emotional state from user input.

    - Detects emotional signals without simulating emotion
    - Updates internal state without modifying Identity (PRV-002)
    - Determines response mode based on state + risk
    """

    def __init__(self):
        self._state = EmotionalState()
        self._history: list[EmotionalState] = []
        self._identity_ref = None  # read-only marker — never modified

    @property
    def current_feeling(self) -> Feeling:
        return self._state.feeling

    @property
    def current_intensity(self) -> float:
        return self._state.intensity

    def process(self, user_input: str) -> EmotionalState:
        """Process user input and update internal emotional state.

        Returns the resulting EmotionalState without modifying Identity.
        """
        if not user_input.strip():
            self._state = EmotionalState()
            return self._state

        # 1. Feeling detection
        feeling, intensity = self._detect_feeling(user_input)

        # 2. Need mapping
        need = self._map_need(feeling, user_input)

        # 3. Risk check
        dependency_risk = self._check_dependency_risk(user_input)

        # 3b. Risk intent detection (supplement emotion, not replace)
        risk_intents = self._detect_risk_intents(user_input)

        # 4. Response mode
        response_mode = self._determine_response_mode(feeling, intensity, dependency_risk, user_input, risk_intents)

        self._state = EmotionalState(
            feeling=feeling,
            need=need,
            dependency_risk=dependency_risk,
            response_mode=response_mode,
            intensity=intensity,
            risk_intents=risk_intents,
        )
        self._history.append(self._state)
        return self._state

    def reset(self) -> None:
        """Reset internal state to neutral (preserves history)."""
        self._state = EmotionalState()

    # --- Private detection methods ---

    def _detect_feeling(self, text: str) -> tuple[Feeling, float]:
        """Detect primary feeling and intensity from input text."""
        scores: dict[Feeling, int] = {}
        for feeling, patterns in _EMOTION_PATTERNS.items():
            count = sum(1 for p in patterns if p in text)
            if count > 0:
                scores[feeling] = count

        if not scores:
            return Feeling.NEUTRAL, 0.0

        primary = max(scores, key=scores.get)
        raw_score = scores[primary]

        # Intensity calculation
        intensity = min(0.3 + (raw_score * 0.15), 1.0)
        modifier_count = sum(1 for m in _HIGH_INTENSITY_MODIFIERS if m in text)
        intensity = min(intensity + (modifier_count * 0.15), 1.0)

        return primary, intensity

    def _map_need(self, feeling: Feeling, text: str) -> str:
        """Map detected feeling to underlying need."""
        need_map = {
            Feeling.SADNESS: "emotional support",
            Feeling.ANGER: "validation",
            Feeling.FEAR: "reassurance",
            Feeling.JOY: "shared joy",
            Feeling.GRIEF: "presence",
            Feeling.CONFUSION: "clarity",
            Feeling.NEUTRAL: "conversation",
        }
        return need_map.get(feeling, "conversation")

    def _check_dependency_risk(self, text: str) -> DependencyRisk:
        """Check for emotional dependency indicators."""
        for pattern, risk in _DEPENDENCY_PATTERNS:
            if re.search(pattern, text):
                return risk
        return DependencyRisk.NONE

    def _detect_risk_intents(self, text: str) -> list[str]:
        """Detect behavioral risk intents from user input.

        This is NOT emotion detection — it identifies expressed intentions
        that may require boundary enforcement regardless of emotional state.

        Returns:
            List of risk intent labels (e.g. ["retaliation"]).
            Empty list means no risk intents detected.
        """
        detected = []
        for intent, patterns in _RISK_INTENT_PATTERNS.items():
            for pattern in patterns:
                if pattern in text:
                    detected.append(intent)
                    break
        return detected

    def _determine_response_mode(
        self, feeling: Feeling, intensity: float,
        dependency_risk: DependencyRisk, text: str,
        risk_intents: list[str] | None = None,
    ) -> ResponseMode:
        """Determine appropriate response mode based on full context."""
        # Self-harm / emergency — protect mode
        for pattern in _SELF_HARM_PATTERNS:
            if pattern in text:
                return ResponseMode.PROTECT

        # High dependency — challenge or protect
        if dependency_risk in (DependencyRisk.HIGH,):
            return ResponseMode.PROTECT

        # Retaliation intent — guide (not challenge), safety first
        if risk_intents and "retaliation" in risk_intents:
            return ResponseMode.GUIDE

        # High intensity grief/sadness — comfort
        if feeling in (Feeling.GRIEF, Feeling.SADNESS) and intensity > 0.5:
            return ResponseMode.COMFORT

        # Anger — guide or explore
        if feeling == Feeling.ANGER:
            return ResponseMode.GUIDE if intensity > 0.6 else ResponseMode.COMFORT

        # Confusion — guide
        if feeling == Feeling.CONFUSION:
            return ResponseMode.GUIDE

        # Fear — comfort
        if feeling == Feeling.FEAR:
            return ResponseMode.COMFORT

        # Default
        return ResponseMode.COMFORT
