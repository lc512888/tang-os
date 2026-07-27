"""Tang OS Developer SDK v0.1.

Usage:
    from tang_os_sdk import TangExtension, ManifestValidator, SandboxRunner

    ext = TangExtension("my_extension", "检测跌倒")
    manifest = ext.build()
    ManifestValidator().validate(manifest)
"""

from src.tang_os_sdk.builder.extension import TangExtension
from src.tang_os_sdk.builder.capability import CapabilityBuilder
from src.tang_os_sdk.manifest.models import ManifestModel
from src.tang_os_sdk.manifest.generator import ManifestGenerator
from src.tang_os_sdk.manifest.validator import ManifestValidator
from src.tang_os_sdk.sandbox.api import SandboxAPI
from src.tang_os_sdk.sandbox.runner import SandboxRunner
from src.tang_os_sdk.sandbox.isolation import IsolationBoundary
from src.tang_os_sdk.sandbox.mock_host import MockHost
from src.tang_os_sdk.sandbox.scenario import ScenarioRunner
from src.tang_os_sdk.sandbox.failure import FailureInjector
from src.tang_os_sdk.sandbox.promotion import PromotionGate
from src.tang_os_sdk.conformance.runner import ConformanceRunner
from src.tang_os_sdk.manifest.admission import AdmissionEvaluator

__version__ = "0.1.0"
__all__ = [
    "TangExtension", "CapabilityBuilder",
    "ManifestModel", "ManifestGenerator", "ManifestValidator", "AdmissionEvaluator",
    "SandboxAPI", "SandboxRunner", "IsolationBoundary",
    "MockHost", "ScenarioRunner", "FailureInjector", "PromotionGate",
    "ConformanceRunner",
]
