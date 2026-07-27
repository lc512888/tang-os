"""Tests: Actuator Permission Gate — HA-003 actuator must pass Permission Runtime."""

import pytest
from src.host.actuator import ActuatorGate
from src.host.models import HostType, TAAL


def test_actuator_needs_permission():
    """HA-003: Actuator cannot execute without Permission Runtime approval."""
    gate = ActuatorGate(HostType.ROBOT, max_authority=TAAL.A3)
    result = gate.request("movement", TAAL.A3)
    assert result["allowed"]  # Pre-check passes
    assert result["status"] == "pending"  # Permission not yet granted


def test_actuator_executes_after_permission():
    """Actuator executes after Permission Runtime grants approval."""
    gate = ActuatorGate(HostType.VEHICLE, max_authority=TAAL.A3)
    req = gate.request("braking", TAAL.A3)
    result = gate.approve(req["request_id"])
    assert result["executed"]


def test_actuator_rejects_above_ceiling():
    """HA-003 / HM-012: Requesting action above authority ceiling is rejected."""
    gate = ActuatorGate(HostType.MOBILE, max_authority=TAAL.A2)
    req = gate.request("screen", TAAL.A4)  # A4 exceeds MOBILE ceiling of A2
    assert not req["allowed"]
    assert "ceiling" in req["reason"]


def test_actuator_rejects_unknown_action():
    """Unknown actuator action is rejected."""
    gate = ActuatorGate(HostType.WEARABLE, max_authority=TAAL.A2)
    req = gate.request("nuclear_launch", TAAL.A4)
    assert not req["allowed"]
