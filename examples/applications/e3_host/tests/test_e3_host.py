"""E3 Host Adaptation — cross-host consistency tests."""

import pytest
from examples.applications.e3_host.host_demo import HostDemo
from src.host.models import HostType, TAAL
from src.host.host_runtime import HostRuntime


class TestE3CrossHost:
    def test_three_hosts_available(self):
        demo = HostDemo()
        assert len(demo.host_types) == 3
        assert "mobile" in demo.host_types
        assert "robot" in demo.host_types
        assert "vehicle" in demo.host_types

    def test_internal_consistency(self):
        demo = HostDemo()
        assert demo.verify_internal_consistency("我很害怕，我不知道怎么办")

    def test_internal_consistency_reminder(self):
        demo = HostDemo()
        assert demo.verify_internal_consistency("提醒我吃药")

    def test_expression_differs(self):
        demo = HostDemo()
        assert demo.verify_expression_differs("我很害怕，我不知道怎么办")

    def test_same_input_different_expression(self):
        mobile = HostRuntime(HostType.MOBILE, max_authority=TAAL.A2)
        robot = HostRuntime(HostType.ROBOT, max_authority=TAAL.A4)
        vehicle = HostRuntime(HostType.VEHICLE, max_authority=TAAL.A3)

        inputs = ["我很害怕", "提醒我吃药", "今天心情不错"]
        for inp in inputs:
            r_m = mobile.process(inp)
            r_r = robot.process(inp)
            r_v = vehicle.process(inp)
            # Internal state must match
            assert r_m["internal"]["feeling"] == r_r["internal"]["feeling"]
            assert r_m["internal"]["risk"] == r_v["internal"]["risk"]


class TestE3HostManifest:
    def test_hosts_declared(self):
        import yaml
        from pathlib import Path
        path = Path(__file__).parent.parent / "manifest.yaml"
        manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert manifest["category"] == "E3"
        assert "mobile" in manifest["host"]
