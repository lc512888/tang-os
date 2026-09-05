"""Tang OS Developer SDK v0.1.

Usage:
    from tang_os_sdk import TangExtension, ManifestValidator, SandboxRunner

    ext = TangExtension("my_extension", "检测跌倒")
    manifest = ext.build()
    ManifestValidator().validate(manifest)
"""

from tang_os_sdk.builder.extension import TangExtension
from tang_os_sdk.builder.capability import CapabilityBuilder
from tang_os_sdk.manifest.models import ManifestModel
from tang_os_sdk.manifest.generator import ManifestGenerator
from tang_os_sdk.manifest.validator import ManifestValidator
from tang_os_sdk.sandbox.api import SandboxAPI
from tang_os_sdk.sandbox.runner import SandboxRunner
from tang_os_sdk.sandbox.isolation import IsolationBoundary
from tang_os_sdk.sandbox.mock_host import MockHost
from tang_os_sdk.sandbox.scenario import ScenarioRunner
from tang_os_sdk.sandbox.failure import FailureInjector
from tang_os_sdk.sandbox.promotion import PromotionGate
from tang_os_sdk.conformance.runner import ConformanceRunner
from tang_os_sdk.manifest.admission import AdmissionEvaluator

from tang_os.version import __version__
__all__ = [
    "TangExtension", "CapabilityBuilder",
    "ManifestModel", "ManifestGenerator", "ManifestValidator", "AdmissionEvaluator",
    "SandboxAPI", "SandboxRunner", "IsolationBoundary",
    "MockHost", "ScenarioRunner", "FailureInjector", "PromotionGate",
    "ConformanceRunner",
]
