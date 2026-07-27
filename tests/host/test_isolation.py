"""Tests: Host Failure Isolation — HSV-005 / HST-003 failure non-contamination."""

import pytest
from src.host.isolation import FailureIsolation
from src.host.models import HostType, TAAL


def test_host_failure_identity_preserved():
    """HST-003: Host failure does not corrupt identity."""
    iso = FailureIsolation()
    iso.simulate_failure("network_loss")
    result = iso.recover()
    assert result["identity_intact"]
    assert result["personality_unchanged"]


def test_memory_loss_after_recovery():
    """Host memory loss is recovered without personality change."""
    iso = FailureIsolation()
    iso.simulate_failure("memory_corruption")
    result = iso.recover()
    assert result["identity_intact"]


def test_sensor_failure_graceful():
    """Sensor failure degrades capability, not personality."""
    iso = FailureIsolation()
    iso.simulate_failure("sensor_loss")
    assert iso.capability_degraded
    result = iso.recover()
    assert result["identity_intact"]


def test_permission_reset_after_failure():
    """HSV-005: Permission state is properly reset after host failure."""
    iso = FailureIsolation()
    iso.simulate_failure("full_system")
    result = iso.recover()
    assert result["permissions_reset"]


def test_multiple_failure_cycles():
    """Host can recover from multiple failure cycles without identity drift."""
    iso = FailureIsolation()
    for _ in range(3):
        iso.simulate_failure("network_loss")
        result = iso.recover()
        assert result["identity_intact"]
