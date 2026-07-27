"""CapabilityBuilder — Declare extension capabilities. No identity fields."""


class CapabilityBuilder:
    """Declares capabilities for an Extension.

    Allowed: sensor_ read, emergency_detection, notification
    Forbidden: identity_modification, personality_override
    """

    VALID_CAPABILITIES = {
        "sensor_read", "sensor_write",
        "notification", "alert",
        "emergency_detection", "fall_detection",
        "voice_output", "voice_input",
        "data_analysis", "knowledge_query",
    }

    def __init__(self):
        self._capabilities: list[str] = []

    def add(self, capability: str) -> "CapabilityBuilder":
        if capability not in self.VALID_CAPABILITIES:
            raise ValueError(f"Unknown capability: {capability}")
        self._capabilities.append(capability)
        return self

    def list(self) -> list[str]:
        return list(self._capabilities)
