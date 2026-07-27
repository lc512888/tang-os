"""Sandbox API — clean public interface for third-party developers.

Usage:
    from tang_os_sdk import SandboxAPI

    sandbox = SandboxAPI()
    result = sandbox.run_scenario("fall_detection")
    sandbox.inject_failure("sensor_loss")
    gate = sandbox.check_promotion_readiness()
"""

from src.tang_os_sdk.sandbox.runner import SandboxRunner
from src.tang_os_sdk.sandbox.isolation import IsolationBoundary
from src.tang_os_sdk.sandbox.mock_host import MockHost
from src.tang_os_sdk.sandbox.scenario import ScenarioRunner
from src.tang_os_sdk.sandbox.failure import FailureInjector
from src.tang_os_sdk.sandbox.promotion import PromotionGate


class SandboxAPI:
    """Third-party safe experimental environment (Phase 13-C-4).

    Provides:
    - Runtime sandbox with mock Core
    - Extension Mock Host for testing
    - Built-in scenario runner
    - Failure injection for resilience testing
    - Production promotion gate (DI-004-A)
    """

    def __init__(self):
        self._runner = SandboxRunner()
        self._isolation = IsolationBoundary()
        self._host = MockHost()
        self._scenarios = ScenarioRunner()
        self._failure = FailureInjector()
        self._promotion = PromotionGate()

    @property
    def runner(self) -> SandboxRunner:
        return self._runner

    @property
    def mock_host(self) -> MockHost:
        return self._host

    @property
    def scenarios(self) -> ScenarioRunner:
        return self._scenarios

    @property
    def failure(self) -> FailureInjector:
        return self._failure

    @property
    def promotion(self) -> PromotionGate:
        return self._promotion

    def run_scenario(self, name: str) -> dict:
        """Run a predefined scenario in sandbox."""
        return self._scenarios.run(name, self._runner)

    def inject_failure(self, mode: str) -> dict:
        """Inject a failure mode into the sandbox."""
        return self._failure.inject(mode, self._runner)

    def check_promotion_readiness(self) -> dict:
        """Check if sandbox state can be promoted to production."""
        return self._promotion.evaluate(self._runner, self._isolation)

    def reset(self) -> None:
        """Reset sandbox to clean state."""
        self._runner = SandboxRunner()
        self._host = MockHost()
