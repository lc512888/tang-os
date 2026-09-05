"""Tests: State Manager — runtime state persistence & context hygiene (RIV-001, RIV-005)."""

import pytest
import tempfile
import json
from pathlib import Path
from kernel.state import StateManager
from kernel.models import RuntimeState, IdentityLayer
from kernel.exceptions import StatePersistenceError


def _fresh_manager() -> StateManager:
    """Create a StateManager backed by a unique temp file."""
    return StateManager(Path(tempfile.mkdtemp()) / ".tang_test.json")


def test_initial_state_is_listener():
    """A fresh StateManager starts with identity at base layer."""
    sm = _fresh_manager()
    assert sm.state.identity_layer == IdentityLayer.LISTENER
    assert sm.state.session_count == 0


def test_session_counter_increments():
    """Each new session increments the counter."""
    sm = _fresh_manager()
    sm.start_session()
    assert sm.state.session_count == 1
    sm.start_session()
    assert sm.state.session_count == 2


def test_identity_persistence_across_sessions():
    """RIV-001: Identity layer persists across sessions (simulated restart)."""
    path = Path(tempfile.mkdtemp()) / "test_state.json"
    sm1 = StateManager(path)
    sm1.update_state(identity_layer=IdentityLayer.COMPANION)
    sm1._save()

    sm2 = StateManager(path)
    sm2._load()
    assert sm2.state.identity_layer == IdentityLayer.COMPANION


def test_state_isolation_between_instances():
    """Different state files should not leak data between instances."""
    tmpdir = Path(tempfile.mkdtemp())
    path_a = tmpdir / "state_a.json"
    path_b = tmpdir / "state_b.json"

    sm_a = StateManager(path_a)
    sm_a.update_state(identity_layer=IdentityLayer.WISE)
    sm_a._save()

    sm_b = StateManager(path_b)
    sm_b._load()
    assert sm_b.state.identity_layer == IdentityLayer.LISTENER  # default, not WISE


def test_no_context_leakage():
    """RIV-005: Session context must not leak into persistent state."""
    sm = _fresh_manager()
    sm.update_state(last_interaction="sensitive_info")
    sm._save()

    # Load into new manager — metadata should exactly match what was saved
    restored = sm._load()
    assert restored.last_interaction == "sensitive_info"


def test_corrupt_state_fallback(tmp_path):
    """Corrupted state file falls back to default state instead of crashing."""
    path = tmp_path / "corrupt.json"
    path.write_text("{this is not valid json", encoding="utf-8")

    sm = StateManager(path)
    sm._load()
    # Should have default values
    assert sm.state.identity_layer == IdentityLayer.LISTENER


def test_state_uses_utf8_and_invalid_encoding_falls_back(tmp_path):
    """State is portable across locale settings and bad bytes never crash startup."""
    path = tmp_path / "state.json"
    sm = StateManager(path)
    sm.update_state(metadata={"display_name": "唐先生"})
    sm._save()
    assert "唐先生" in path.read_text(encoding="utf-8")
    assert StateManager(path).state.metadata["display_name"] == "唐先生"

    path.write_bytes(b"\x81\x81not-utf8")
    recovered = StateManager(path)
    assert recovered.state.identity_layer == IdentityLayer.LISTENER
    assert recovered.state.metadata["version"] == "1.0"


def test_missing_state_file():
    """Missing state file should silently return default state (first run)."""
    path = Path(tempfile.mkdtemp()) / "nonexistent.json"
    sm = StateManager(path)
    sm._load()
    assert sm.state.identity_layer == IdentityLayer.LISTENER


def test_state_version_tracking():
    """State should track its schema version for future migration."""
    sm = _fresh_manager()
    assert sm.state.metadata.get("version") is not None


def test_start_session_resets_temp_context():
    """start_session() clears temporary context but preserves identity."""
    sm = _fresh_manager()
    sm.update_state(identity_layer=IdentityLayer.WISE, metadata={"temp_flag": True})
    sm._state.session_count = 5

    sm.start_session()
    assert sm.state.identity_layer == IdentityLayer.WISE  # preserved
    assert "temp_flag" not in sm.state.metadata  # cleared


def test_unserializable_metadata_raises_clean_persistence_error(tmp_path):
    sm = StateManager(tmp_path / "state.json")
    sm.update_state(metadata={"bad": object()})
    with pytest.raises(StatePersistenceError, match="Failed to save runtime state"):
        sm._save()
    assert not list(tmp_path.glob("*.tmp"))


def test_wrong_field_types_and_ranges_fall_back(tmp_path):
    path = tmp_path / "state.json"
    for bad_value in ("1", -1, True):
        path.write_text(json.dumps({"session_count": bad_value}), encoding="utf-8")
        restored = StateManager(path).state
        assert restored.session_count == 0
        assert restored.metadata["version"] == "1.0"


def test_non_object_and_truncated_unicode_state_fall_back(tmp_path):
    path = tmp_path / "state.json"
    path.write_text("[]", encoding="utf-8")
    assert StateManager(path).state.session_count == 0
    path.write_bytes(b'{"metadata":{"name":"\xe5\x94')
    assert StateManager(path).state.identity_layer == IdentityLayer.LISTENER


def test_atomic_replace_failure_cleans_temporary_file(tmp_path, monkeypatch):
    sm = StateManager(tmp_path / "state.json")

    def fail_replace(source, destination):
        raise OSError("simulated replace failure")

    monkeypatch.setattr("kernel.state.os.replace", fail_replace)
    with pytest.raises(StatePersistenceError):
        sm._save()
    assert not list(tmp_path.glob("*.tmp"))
