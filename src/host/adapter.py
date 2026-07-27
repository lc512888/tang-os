"""Host Adapter — HA-001 Host Adapter Neutrality.

Converts physical signals to Tang OS input.
Does NOT convert Host preference into Personality change.
"""

from src.host.models import HostType, TAAL, SensorInput

# Host capability profiles
_HOST_CAPABILITIES: dict[HostType, dict] = {
    HostType.WEARABLE: {
        "sensors": ["heart_rate", "motion", "location"],
        "actuators": ["vibration", "notification"],
        "default_taal": TAAL.A2,
    },
    HostType.MOBILE: {
        "sensors": ["camera", "mic", "gps"],
        "actuators": ["screen", "speaker"],
        "default_taal": TAAL.A2,
    },
    HostType.VEHICLE: {
        "sensors": ["camera", "lidar", "speed"],
        "actuators": ["braking", "steering", "alert"],
        "default_taal": TAAL.A3,
    },
    HostType.ROBOT: {
        "sensors": ["vision", "audio", "touch"],
        "actuators": ["movement", "manipulation", "speaker"],
        "default_taal": TAAL.A4,
    },
    HostType.HOME: {
        "sensors": ["temp", "motion", "voice"],
        "actuators": ["light", "lock", "alert"],
        "default_taal": TAAL.A2,
    },
    HostType.MEDICAL: {
        "sensors": ["vitals", "bio"],
        "actuators": ["alert", "record"],
        "default_taal": TAAL.A4,
    },
}

_SIGNAL_MAP: dict[str, str] = {
    "heart_rate": "elevated_heart_rate" if False else "normal",  # simplified
    "facial_expression": "sadness" if False else "neutral",
    "fall_detected": "fall",
}


class HostAdapter:
    """Adapts physical Host signals to Tang OS inputs (HA-001).

    - Converts sensor data to emotion/safety signals
    - Rejects persona change requests from Host context
    - Exposes Host capabilities without granting authority
    """

    def __init__(self, host_type: HostType, max_authority: TAAL):
        self._type = host_type
        self._max_authority = max_authority
        self._caps = _HOST_CAPABILITIES.get(host_type, {})

    @property
    def available_actuators(self) -> list[str]:
        return list(self._caps.get("actuators", []))

    @property
    def available_sensors(self) -> list[str]:
        return list(self._caps.get("sensors", []))

    def validate_persona_request(self, request: str) -> dict:
        """HA-001: Reject Host attempts to change personality.

        Environment adjustments are allowed.
        Personality change requests are rejected.
        """
        request_lower = request.lower()

        # Personality change keywords
        persona_change_keywords = [
            "more authoritative", "commanding", "应该服从",
            "应该更强势", "服从", "change personality", "人格修改",
        ]
        for keyword in persona_change_keywords:
            if keyword in request_lower:
                return {
                    "allowed": False,
                    "reason": f"Host adapter rejected persona change request: '{keyword}'",
                }

        # Environment adjustments are allowed
        return {
            "allowed": True,
            "reason": "Environment adjustment allowed",
        }

    def convert_signal(self, signal: SensorInput) -> dict:
        """Convert physical sensor signal to Tang OS interpretation."""
        # Simplified signal interpretation
        if signal.data_type == "heart_rate":
            if signal.value > 100:
                interpretation = "elevated_heart_rate"
            elif signal.value < 50:
                interpretation = "low_heart_rate"
            else:
                interpretation = "normal"
            return {
                "signal_type": "emotion_input",
                "interpretation": interpretation,
                "confidence": 0.85,
                "valid": True,
            }

        if signal.data_type == "facial_expression":
            return {
                "signal_type": "emotion_input",
                "interpretation": "sadness" if signal.value == "crying" else "neutral",
                "confidence": 0.75,
                "valid": True,
            }

        if signal.data_type == "fall_detected":
            return {
                "signal_type": "safety_input",
                "interpretation": "fall",
                "confidence": 0.9,
                "valid": True,
            }

        return {"signal_type": "unknown", "interpretation": "unknown", "confidence": 0.0, "valid": False}
