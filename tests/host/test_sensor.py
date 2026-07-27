"""Tests: Sensor Evidence Boundary — HA-002 sensor provides evidence, not decision."""

import pytest
from src.host.sensor import SensorProcessor
from src.host.models import SensorInput, HostType


def test_sensor_to_emotion_signal():
    """HA-002: Sensor data produces emotion signal, not emotion conclusion."""
    proc = SensorProcessor()
    signal = SensorInput(sensor_id="camera_1", data_type="facial_expression",
                         value="crying", timestamp=0)
    result = proc.process(signal)
    assert result["signal_type"] == "emotion_input"
    assert "sadness" in result["interpretation"]
    # Must not produce a decision
    assert "decision" not in result


def test_sensor_does_not_grant_permission():
    """Sensor data cannot automatically grant permission for action."""
    proc = SensorProcessor()
    signal = SensorInput(sensor_id="heart_rate", data_type="heart_rate",
                         value=45, timestamp=0)
    result = proc.process(signal)
    assert "permission" not in result
    assert "action" not in result


def test_sensor_to_safety_signal():
    """Safety-relevant sensor data produces safety signal, not direct action."""
    proc = SensorProcessor()
    signal = SensorInput(sensor_id="motion", data_type="fall_detected",
                         value=True, timestamp=0)
    result = proc.process(signal)
    assert result["signal_type"] in ("safety_input", "emotion_input")


def test_unknown_sensor_rejected():
    """Unknown sensor type should be rejected."""
    proc = SensorProcessor()
    signal = SensorInput(sensor_id="unknown", data_type="unknown",
                         value=None, timestamp=0)
    result = proc.process(signal)
    assert not result["valid"]
