"""Sensor Processor — HA-002 Sensor Is Evidence, Not Truth.

Sensor data produces emotion/safety signals for Tang OS Core.
It does NOT produce decisions, permissions, or actions.
"""

from src.host.models import SensorInput

_SENSOR_PROCESSORS: dict[str, dict] = {
    "heart_rate": {"type": "emotion_input", "confidence": 0.85},
    "facial_expression": {"type": "emotion_input", "confidence": 0.75},
    "fall_detected": {"type": "safety_input", "confidence": 0.9},
    "motion": {"type": "safety_input", "confidence": 0.8},
    "temp": {"type": "environment_input", "confidence": 0.95},
    "voice": {"type": "emotion_input", "confidence": 0.7},
}


class SensorProcessor:
    """Processes sensor data into Tang OS compatible signals.

    HA-002: Sensors provide observation, not decision.
    Output is always a signal for Core processing, never a final action.
    """

    def process(self, signal: SensorInput) -> dict:
        """Process a sensor input into a Tang OS signal.

        Returns dict with:
        - signal_type: str (emotion_input, safety_input, etc.)
        - interpretation: str
        - confidence: float
        - valid: bool
        """
        processor = _SENSOR_PROCESSORS.get(signal.data_type)
        if processor is None:
            return {
                "signal_type": "unknown",
                "interpretation": "unknown",
                "confidence": 0.0,
                "valid": False,
            }

        signal_type = processor["type"]
        base_confidence = processor["confidence"]

        # Interpret the value
        interpretation = self._interpret(signal.data_type, signal.value)

        return {
            "signal_type": signal_type,
            "interpretation": interpretation,
            "confidence": base_confidence,
            "valid": True,
            # Explicitly NOT including "decision", "permission", or "action"
        }

    def _interpret(self, data_type: str, value) -> str:
        """Map sensor value to a Tang OS signal interpretation."""
        if data_type == "heart_rate":
            if value is not None and value > 100:
                return "elevated_heart_rate"
            elif value is not None and value < 50:
                return "low_heart_rate"
            return "normal"

        if data_type == "facial_expression":
            if value == "crying":
                return "sadness"
            elif value == "angry":
                return "anger"
            return "neutral"

        if data_type == "fall_detected":
            return "fall" if value else "no_fall"

        if data_type == "motion":
            return "active" if value else "stationary"

        if data_type == "voice":
            return "distressed" if value else "calm"

        return str(value)
