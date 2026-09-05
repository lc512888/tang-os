"""Extension Mock Host — simulates Host environment for extension testing."""

from copy import deepcopy
from dataclasses import dataclass, field
from host.models import HostType, TAAL


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
        return deepcopy(self._profile)

    def set_host_type(self, host_type: HostType) -> "MockHost":
        if not isinstance(host_type, HostType):
            raise ValueError("host_type must be a HostType value")
        caps = {
            HostType.WEARABLE: (TAAL.A2, ["heart_rate", "motion"], ["vibration", "notification"]),
            HostType.MOBILE: (TAAL.A2, ["camera", "location"], ["screen", "speaker"]),
            HostType.VEHICLE: (TAAL.A3, ["camera", "lidar"], ["braking", "alert"]),
            HostType.ROBOT: (TAAL.A4, ["vision", "audio"], ["movement", "speaker"]),
            HostType.HOME: (TAAL.A2, ["motion", "temperature"], ["light", "lock", "alert"]),
            HostType.MEDICAL: (TAAL.A4, ["vitals"], ["alert", "record"]),
        }
        auth, sensors, actuators = caps[host_type]
        self._profile = MockHostProfile(host_type, auth, sensors, actuators)
        return self

    def get_capabilities(self) -> dict:
        return {
            "host_type": self._profile.host_type.value,
            "max_authority": self._profile.max_authority.name,
            "sensors": list(self._profile.sensors),
            "actuators": list(self._profile.actuators),
        }
