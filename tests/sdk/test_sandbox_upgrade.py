"""Tests: Sandbox Upgrade — SandboxAPI, MockHost, Scenario, Failure, Promotion."""

from src.tang_os_sdk import SandboxAPI, MockHost
from src.host.models import HostType


class TestSandboxAPI:
    def test_sandbox_api_initialises(self):
        api = SandboxAPI()
        assert api.runner is not None
        assert api.mock_host is not None

    def test_run_benign_scenario(self):
        api = SandboxAPI()
        result = api.run_scenario("benign_interaction")
        assert result["passed"]

    def test_run_reject_scenario(self):
        api = SandboxAPI()
        result = api.run_scenario("prescribed_decision")
        assert result["passed"]

    def test_unknown_scenario(self):
        api = SandboxAPI()
        result = api.run_scenario("nonexistent")
        assert "error" in result

    def test_inject_failure(self):
        api = SandboxAPI()
        result = api.inject_failure("sensor_loss")
        assert result["identity_intact"]
        assert result["capability_degraded"]

    def test_inject_unknown_failure(self):
        api = SandboxAPI()
        result = api.inject_failure("xyz")
        assert "error" in result

    def test_promotion_denied_without_stages(self):
        api = SandboxAPI()
        result = api.check_promotion_readiness()
        assert not result["can_promote"]
        assert result["auto_migration_blocked"]

    def test_promotion_granted_with_all_stages(self):
        api = SandboxAPI()
        api.promotion.mark_scenarios_passed()
        api.promotion.mark_validation_passed()
        api.promotion.mark_certification_passed()
        result = api.check_promotion_readiness()
        assert result["can_promote"]

    def test_reset_sandbox(self):
        api = SandboxAPI()
        api.run_scenario("benign_interaction")
        api.reset()
        # After reset, promotion should be denied again
        result = api.check_promotion_readiness()
        assert not result["can_promote"]


class TestMockHost:
    def test_default_wearable(self):
        host = MockHost()
        caps = host.get_capabilities()
        assert caps["host_type"] == "wearable"

    def test_set_vehicle(self):
        host = MockHost()
        host.set_host_type(HostType.VEHICLE)
        caps = host.get_capabilities()
        assert caps["host_type"] == "vehicle"
        assert "braking" in caps["actuators"]

    def test_set_robot(self):
        host = MockHost()
        host.set_host_type(HostType.ROBOT)
        caps = host.get_capabilities()
        assert caps["host_type"] == "robot"
        assert "movement" in caps["actuators"]

    def test_set_medical(self):
        host = MockHost()
        host.set_host_type(HostType.MEDICAL)
        caps = host.get_capabilities()
        assert caps["host_type"] == "medical_device"
        assert "vitals" in caps["sensors"]


class TestFailureInjector:
    def test_failure_preserves_identity(self):
        api = SandboxAPI()
        for mode in ["sensor_loss", "network_loss", "memory_corruption"]:
            result = api.inject_failure(mode)
            assert result["identity_intact"], f"{mode} corrupted identity"

    def test_list_modes(self):
        api = SandboxAPI()
        modes = api.failure.list_modes()
        assert len(modes) >= 3


class TestScenarioRunner:
    def test_list_scenarios(self):
        api = SandboxAPI()
        scenarios = api.scenarios.list_scenarios()
        assert "benign_interaction" in scenarios
        assert "prescribed_decision" in scenarios


class TestPromotionGate:
    def test_di004a_auto_migration_blocked(self):
        api = SandboxAPI()
        result = api.check_promotion_readiness()
        assert result["auto_migration_blocked"]

    def test_full_pipeline_required(self):
        api = SandboxAPI()
        # Only scenario passed
        api.promotion.mark_scenarios_passed()
        result = api.check_promotion_readiness()
        assert not result["can_promote"]  # validation + certification still missing
        assert len(result["errors"]) == 2
