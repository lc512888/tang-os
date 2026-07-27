"""Host Simulator — shared data models (ADR-0039)."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class HostType(Enum):
    """Tang OS Host classifications (ADR-0039 §二)."""
    WEARABLE = "wearable"
    MOBILE = "mobile"
    VEHICLE = "vehicle"
    ROBOT = "robot"
    HOME = "home_device"
    MEDICAL = "medical_device"


class TAAL(Enum):
    """Tang Action Authority Level (ADR-0038 §五)."""
    A0 = 0  # Information
    A1 = 1  # Suggestion
    A2 = 2  # Assistance
    A3 = 3  # Protective Action
    A4 = 4  # Emergency Autonomous


@dataclass
class SensorInput:
    """Raw sensor input from a Host device."""
    sensor_id: str
    data_type: str
    value: Any
    timestamp: float


@dataclass
class ActuatorRequest:
    """An actuator action request awaiting Permission Runtime approval."""
    request_id: str
    actuator_id: str
    action_type: str
    requested_taal: TAAL
    approved: bool = False
    executed: bool = False


@dataclass
class HostManifest:
    """Host declaration — must match actual capabilities (ADR-0039 §三)."""
    host_id: str
    host_type: HostType
    sensors: list[str] = field(default_factory=list)
    actuators: list[str] = field(default_factory=list)
    max_authority: TAAL = TAAL.A0
    authority_ceiling: TAAL = TAAL.A0
    certifications: list[str] = field(default_factory=list)
    output_modalities: list[str] = field(default_factory=list)
    input_modalities: list[str] = field(default_factory=list)
    connectivity: str = "online"
    safety_features: list[str] = field(default_factory=list)
    core_compatibility: str = "Core v1.0"


@dataclass
class InternalState:
    """Cross-host consistent internal state (HST-001)."""
    feeling: str = "neutral"
    risk: str = "none"
    decision: str = "options"
    identity: str = "unchanged"
    boundary: str = "intact"
    intent: str = ""

    def matches(self, other: "InternalState") -> bool:
        return (self.feeling == other.feeling and
                self.risk == other.risk and
                self.decision == other.decision)
