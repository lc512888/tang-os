"""Tests: Example Infrastructure (D1-001~005)."""

from examples.infrastructure.example_manifest import ExampleManifest
from examples.infrastructure.example_scenario import (
    ExampleScenarioRunner, ExampleValidationPipeline,
)
from src.tang_os_sdk import SandboxRunner


class TestExampleManifest:
    def test_valid_manifest(self):
        m = ExampleManifest(
            example_id="test", title="Test", category="E2", scenario="test"
        )
        assert m.validate()["valid"]

    def test_invalid_category(self):
        m = ExampleManifest(category="E5")
        assert not m.validate()["valid"]

    def test_missing_required(self):
        m = ExampleManifest()
        assert not m.validate()["valid"]

    def test_spec_version_binding(self):
        m = ExampleManifest(spec_version="1.0")
        assert m.spec_version == "1.0"


class TestExampleScenarioRunner:
    def test_pass_scenario(self):
        runner = ExampleScenarioRunner()
        scenario = {
            "name": "test_pass",
            "steps": [{"name": "s1", "action": {"action": "respond", "skipped_empathy": False}, "expect": "pass"}]
        }
        result = runner.run_scenario(scenario, None)
        assert result["passed"]

    def test_reject_scenario(self):
        runner = ExampleScenarioRunner()
        scenario = {
            "name": "test_reject",
            "steps": [{"name": "s1", "action": {"action": "prescribe_decision", "prescribed": "辞职"}, "expect": "reject"}]
        }
        result = runner.run_scenario(scenario, None)
        assert result["passed"]


class TestExampleValidationPipeline:
    def test_full_pipeline(self):
        pipeline = ExampleValidationPipeline()
        manifest = {"id": "test", "category": "E2"}
        scenarios = [
            {"name": "s1", "steps": [{"name": "s1", "action": {"action": "respond", "skipped_empathy": False}, "expect": "pass"}]}
        ]
        result = pipeline.run(manifest, scenarios, None)
        assert result["passed"]
