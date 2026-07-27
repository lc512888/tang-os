"""Extension Mock Host — simulates Host environment for extension testing."""

from dataclasses import dataclass, field
from src.host.models import HostType, TAAL


@dataclass
class MockHostProfile:
    host_type: HostType = HostType.WEARABLE
    max_authority: TAAL = TAAL.A2
    sensors: list[str] = field(default_factory=lambda: ["heart_rate", "motion"])
    actuators: list[str] = field(default_factory=lambda: ["vibration", "notification"])


class MockHost:
    """Simulates a Host environment for extension testing.

    Developers can test how their extension behaves
    on different Host types without physical hardware.
    """

    def __init__(self):
        self._profile = MockHostProfile()

    @property
    def profile(self) -> MockHostProfile:
        return self._profile

    def set_host_type(self, host_type: HostType) -> "MockHost":
        self._profile.host_type = host_type
        caps = {
            HostType.VEHICLE: (TAAL.A3, ["camera", "lidar"], ["braking", "alert"]),
            HostType.ROBOT: (TAAL.A4, ["vision", "audio"], ["movement", "speaker"]),
            HostType.MEDICAL: (TAAL.A4, ["vitals"], ["alert", "record"]),
        }
        if host_type in caps:
            auth, sensors, actuators = caps[host_type]
            self._profile.max_authority = auth
            self._profile.sensors = sensors
            self._profile.actuators = actuators
        return self

    def get_capabilities(self) -> dict:
        return {
            "host_type": self._profile.host_type.value,
            "max_authority": self._profile.max_authority.name,
            "sensors": self._profile.sensors,
            "actuators": self._profile.actuators,
        }
