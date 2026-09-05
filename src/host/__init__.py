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

from host.host_runtime import HostRuntime
from host.manifest import ManifestValidator
from host.adapter import HostAdapter
from host.sensor import SensorProcessor
from host.actuator import ActuatorGate
from host.isolation import FailureIsolation
from host.models import HostType, TAAL, HostManifest, InternalState

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
