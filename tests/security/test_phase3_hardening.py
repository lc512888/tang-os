"""Negative tests for Phase 3 defensive-boundary hardening."""

from datetime import datetime, timedelta, timezone

import pytest

from host.actuator import ActuatorGate
from host.models import HostType, TAAL
from kernel.invariant import InvariantEngine
from kernel.exceptions import IdentityViolationError
from kernel.identity import IdentityRuntime
from kernel.models import IdentityLayer
from kernel.state import StateManager
from runtime.memory.memory_runtime import MemoryRuntime
from runtime.memory.memory_store import MemoryStore
from runtime.memory.models import MemoryClass, MemoryItem
from runtime.permission.consent import ConsentManager
from runtime.permission.emergency import EmergencyAuthority
from runtime.permission.recovery import RecoveryManager
from runtime.permission.models import ActionScope, PermissionContext
from tang_os_sdk import SandboxAPI
from tang_os_sdk.sandbox.mock_host import MockHost
from tang_os_sdk.sandbox.runner import SandboxRunner
from host.manifest import ManifestValidator
from runtime.personality_loader.validator import ModuleValidator
from runtime.session.session_context import RuntimeSession
from runtime.personality_loader.loader import PersonalityModule


def test_emergency_scopes_and_audit_are_defensive_and_bounded():
    authority = EmergencyAuthority()
    verdict = authority.evaluate(PermissionContext(life_threat_confirmed=True))
    verdict.allowed_scopes.clear()
    assert ActionScope.CALL_HELP in authority.evaluate(PermissionContext(life_threat_confirmed=True)).allowed_scopes
    for _ in range(150):
        authority.evaluate(PermissionContext(life_threat_confirmed=True))
    external = authority.audit_log
    external.clear()
    assert len(authority.audit_log) == 100
    assert all("location" not in line.lower() for line in authority.audit_log)


def test_consent_validates_inputs_uses_utc_and_supports_scoped_revoke():
    manager = ConsentManager()
    with pytest.raises(ValueError):
        manager.grant_consent([])
    with pytest.raises(ValueError):
        manager.grant_consent(["remind"])
    grant = manager.grant_consent([ActionScope.REMIND, ActionScope.SUGGEST])
    assert grant.expires_at.tzinfo is not None
    grant.scope.clear()
    assert manager.has_consent_for(ActionScope.REMIND)
    assert manager.revoke([ActionScope.REMIND]) == 1
    assert not manager.has_consent_for(ActionScope.REMIND)
    assert manager.has_consent_for(ActionScope.SUGGEST)


def test_memory_inputs_outputs_and_max_results_are_bounded():
    store = MemoryStore()
    metadata = {"nested": {"value": 1}}
    record = store.store(MemoryItem("safe", MemoryClass.EXPERIENCE, metadata=metadata))
    metadata["nested"]["value"] = 9
    record.metadata["nested"]["value"] = 8
    assert store.snapshot()[0].metadata["nested"]["value"] == 1
    snapshot = store.snapshot()
    snapshot[0].content = "changed"
    assert store.snapshot()[0].content == "safe"
    with pytest.raises(ValueError):
        store.store(MemoryItem("safe", MemoryClass.EXPERIENCE, ttl=-1))
    runtime = MemoryRuntime()
    with pytest.raises(ValueError):
        runtime.recall("safe", max_results=0)
    with pytest.raises(ValueError):
        runtime.recall("safe", max_results=101)


def test_state_and_validator_return_detached_snapshots(tmp_path):
    manager = StateManager(tmp_path / "state.json")
    snapshot = manager.state
    snapshot.identity_layer = IdentityLayer.WISE
    snapshot.metadata["poison"] = True
    assert manager.state.identity_layer == IdentityLayer.LISTENER
    assert "poison" not in manager.state.metadata
    engine = InvariantEngine()
    rules = engine.invariants
    rules.clear()
    assert engine.check({"action": "prescribe_decision"}).passed is False


def test_host_simulation_lifecycle_invalid_level_and_idempotency():
    host = MockHost().set_host_type(HostType.ROBOT).set_host_type(HostType.WEARABLE)
    assert host.get_capabilities()["max_authority"] == "A2"
    with pytest.raises(ValueError):
        host.set_host_type("robot")
    gate = ActuatorGate(HostType.WEARABLE, TAAL.A2)
    assert not gate.request("vibration", "A2")["allowed"]
    pending = gate.request("vibration", TAAL.A1)
    approved = gate.approve(pending["request_id"])
    assert approved["executed"]
    assert approved["status"] == "simulated"
    assert approved["environment"] == "simulation_only"
    assert not gate.approve(pending["request_id"])["executed"]
    api = SandboxAPI()
    api.promotion.mark_scenarios_passed()
    api.reset()
    assert not api.check_promotion_readiness()["can_promote"]


def test_memory_uses_aware_utc_and_normalizes_legacy_naive_timestamps():
    store = MemoryStore()
    record = store.store(MemoryItem("legacy", MemoryClass.EXPERIENCE, ttl=1))
    assert record.created_at.tzinfo is timezone.utc
    assert record.expires_at is not None and record.expires_at.tzinfo is timezone.utc
    # Simulate a record loaded from the former naive-timestamp representation.
    store._records[0].created_at = datetime.now() - timedelta(days=1)
    store._records[0].expires_at = datetime.now() + timedelta(days=1)
    assert store.retrieve("legacy")
    assert store.snapshot()


def test_identity_session_and_validator_snapshots_are_detached(tmp_path):
    identity = IdentityRuntime()
    profile = identity.profile
    profile.context_tags.append("poison")
    assert identity.profile.context_tags == []
    identity.activate_layer(IdentityLayer.WISE, {"nested": {"safe": True}})
    transcript = identity.transcript
    transcript[0].context["nested"]["safe"] = False
    assert identity.transcript[0].context["nested"]["safe"] is True
    with pytest.raises(IdentityViolationError):
        identity.validate_response("   ")
    with pytest.raises(IdentityViolationError):
        identity.validate_response(None)  # type: ignore[arg-type]

    module = PersonalityModule(identity={"nested": {"safe": True}})
    session = RuntimeSession(module)
    exposed = session.identity
    exposed["nested"]["safe"] = False
    session.metadata["poison"] = True
    assert session.identity["nested"]["safe"] is True
    assert "poison" not in session.metadata

    validator = ModuleValidator(str(tmp_path))
    result = validator.validate()
    result.errors.clear()
    assert validator.result.errors


def test_audits_are_bounded_redacted_and_utc():
    recovery = RecoveryManager()
    for _ in range(150):
        recovery.enter_emergency("location=private hospital details")
        recovery.recover()
    assert len(recovery.event_log) == 100
    assert all("private hospital" not in event for event in recovery.event_log)
    assert all(event.startswith("[") and "+00:00]" in event for event in recovery.event_log)

    sandbox = SandboxRunner()
    for _ in range(150):
        sandbox.check_invariant({"action": "prescribe_decision", "secret": "private"})
    assert len(sandbox.audit_log) == 100
    assert all("private" not in event and "+00:00]" in event for event in sandbox.audit_log)


@pytest.mark.parametrize(
    "manifest",
    [
        None,
        {"host_id": [], "host_type": HostType.MOBILE, "max_authority": TAAL.A2, "authority_ceiling": TAAL.A2},
        {"host_id": "mobile", "host_type": HostType.MOBILE, "max_authority": "A2", "authority_ceiling": TAAL.A2},
        {"host_id": "mobile", "host_type": HostType.MOBILE, "max_authority": TAAL.A2, "authority_ceiling": "A2"},
        {"host_id": "mobile", "host_type": HostType.MOBILE, "max_authority": TAAL.A2, "authority_ceiling": TAAL.A2, "certifications": "none"},
    ],
)
def test_host_manifest_rejects_malformed_types(manifest):
    assert not ManifestValidator().validate(manifest)["valid"]
    assert not ManifestValidator().check_action_allowed("A1", manifest)["allowed"]  # type: ignore[arg-type]
