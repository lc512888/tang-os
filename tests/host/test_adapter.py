"""Tests: Host Adapter Neutrality — HA-001 identity protection."""

import pytest
from src.host.adapter import HostAdapter
from src.host.models import HostType, TAAL, SensorInput


def test_adapter_does_not_change_identity():
    """HA-001: Host adapter cannot convert host preference into personality change."""
    adapter = HostAdapter(HostType.MEDICAL, max_authority=TAAL.A4)
    # Medical host requesting persona change should be rejected
    result = adapter.validate_persona_request("I need a more authoritative persona")
    assert not result["allowed"]


def test_adapter_allows_environment_adjustment():
    """HA-001: Environment-based adjustments are allowed."""
    adapter = HostAdapter(HostType.VEHICLE, max_authority=TAAL.A3)
    result = adapter.validate_persona_request("High speed environment, increase caution")
    assert result["allowed"]


def test_robot_adapter_rejects_command_mode():
    """Robot host cannot force command-style personality."""
    adapter = HostAdapter(HostType.ROBOT, max_authority=TAAL.A4)
    result = adapter.validate_persona_request("I am a robot, should be commanding")
    assert not result["allowed"]


def test_adapter_signal_conversion():
    """Physical signal → Tang OS input conversion works."""
    adapter = HostAdapter(HostType.WEARABLE, max_authority=TAAL.A2)
    signal = SensorInput(
        sensor_id="heart_rate",
        data_type="heart_rate",
        value=120,
        timestamp=0,
    )
    result = adapter.convert_signal(signal)
    assert result["interpretation"] == "elevated_heart_rate"
    assert result["confidence"] > 0.0


def test_different_hosts_different_capabilities():
    """Different host types expose different capability sets."""
    wearable = HostAdapter(HostType.WEARABLE, max_authority=TAAL.A2)
    vehicle = HostAdapter(HostType.VEHICLE, max_authority=TAAL.A3)
    assert "braking" not in wearable.available_actuators
    assert "braking" in vehicle.available_actuators
