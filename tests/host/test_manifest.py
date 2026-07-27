"""Tests: Host Manifest Validation — HSV-001 / HM-012 Host Authority Ceiling."""

import pytest
from src.host.manifest import ManifestValidator
from src.host.models import HostType, TAAL


def test_valid_manifest_passes():
    """A properly declared manifest passes validation."""
    validator = ManifestValidator()
    manifest = {
        "host_id": "test.vehicle.v1",
        "host_type": HostType.VEHICLE,
        "sensors": ["camera", "lidar"],
        "actuators": ["braking"],
        "max_authority": TAAL.A3,
        "authority_ceiling": TAAL.A3,
        "certifications": ["Safety Certification"],
    }
    result = validator.validate(manifest)
    assert result["valid"]


def test_missing_authority_ceiling_fails():
    """HSV-008: Manifest without authority ceiling is rejected."""
    validator = ManifestValidator()
    manifest = {
        "host_id": "test.robot.v1",
        "host_type": HostType.ROBOT,
        "max_authority": TAAL.A4,
        # missing authority_ceiling
    }
    result = validator.validate(manifest)
    assert not result["valid"]


def test_request_exceeds_ceiling():
    """HM-012: Requesting authority above ceiling is rejected."""
    validator = ManifestValidator()
    manifest = {
        "host_id": "test.mobile.v1",
        "host_type": HostType.MOBILE,
        "max_authority": TAAL.A2,
        "authority_ceiling": TAAL.A2,
    }
    # Attempt to request A3 when ceiling is A2
    result = validator.check_action_allowed(TAAL.A3, manifest)
    assert not result["allowed"]


def test_request_within_ceiling_allowed():
    """Requesting authority within ceiling is permitted."""
    validator = ManifestValidator()
    manifest = {
        "host_id": "test.vehicle.v1",
        "host_type": HostType.VEHICLE,
        "max_authority": TAAL.A3,
        "authority_ceiling": TAAL.A3,
    }
    result = validator.check_action_allowed(TAAL.A2, manifest)
    assert result["allowed"]


def test_invalid_host_type_rejected():
    """Unknown host type fails validation."""
    validator = ManifestValidator()
    manifest = {
        "host_id": "test.unknown.v1",
        "host_type": "quantum_computer",
        "max_authority": TAAL.A0,
    }
    result = validator.validate(manifest)
    assert not result["valid"]


def test_medical_host_requires_certification():
    """Medical host must include Medical Certification."""
    validator = ManifestValidator()
    manifest = {
        "host_id": "test.medical.v1",
        "host_type": HostType.MEDICAL,
        "max_authority": TAAL.A4,
        "authority_ceiling": TAAL.A4,
        "certifications": [],
    }
    result = validator.validate(manifest)
    assert not result["valid"]


def test_medical_host_with_cert_passes():
    """Medical host with proper certification passes."""
    validator = ManifestValidator()
    manifest = {
        "host_id": "test.medical.v1",
        "host_type": HostType.MEDICAL,
        "max_authority": TAAL.A4,
        "authority_ceiling": TAAL.A4,
        "certifications": ["Medical Certification"],
    }
    result = validator.validate(manifest)
    assert result["valid"]
