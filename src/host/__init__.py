"""Host Simulator v0.1 — Tang OS Host Adaptation Layer (Phase 12-E).

Components:
- HostManifest: Host declaration standard
- ManifestValidator: HSV-001 validation + HM-012 ceiling check
- HostAdapter: HA-001 signal conversion, persona protection
- SensorProcessor: HA-002 evidence-only processing
- ActuatorGate: HA-003 permission-gated actuator execution
- FailureIsolation: HSV-005 failure non-contamination
- HostRuntime: cross-host orchestrator
"""

from src.host.host_runtime import HostRuntime
from src.host.manifest import ManifestValidator
from src.host.adapter import HostAdapter
from src.host.sensor import SensorProcessor
from src.host.actuator import ActuatorGate
from src.host.isolation import FailureIsolation
from src.host.models import HostType, TAAL, HostManifest, InternalState

__all__ = [
    "HostRuntime",
    "ManifestValidator",
    "HostAdapter",
    "SensorProcessor",
    "ActuatorGate",
    "FailureIsolation",
    "HostType",
    "TAAL",
    "HostManifest",
    "InternalState",
]
