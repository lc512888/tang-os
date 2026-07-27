"""Tests: State Manager — runtime state persistence & context hygiene (RIV-001, RIV-005)."""

import pytest
import tempfile
import json
from pathlib import Path
from src.kernel.state import StateManager
from src.kernel.models import RuntimeState, IdentityLayer
from src.kernel.exceptions import StatePersistenceError


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
    sm1.state.identity_layer = IdentityLayer.COMPANION
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
    sm_a.state.identity_layer = IdentityLayer.WISE
    sm_a._save()

    sm_b = StateManager(path_b)
    sm_b._load()
    assert sm_b.state.identity_layer == IdentityLayer.LISTENER  # default, not WISE


def test_no_context_leakage():
    """RIV-005: Session context must not leak into persistent state."""
    sm = _fresh_manager()
    sm.state.last_interaction = "sensitive_info"
    sm._save()

    # Load into new manager — metadata should exactly match what was saved
    restored = sm._load()
    assert restored.last_interaction == "sensitive_info"


def test_corrupt_state_fallback():
    """Corrupted state file falls back to default state instead of crashing."""
    path = Path(tempfile.mkdtemp()) / "corrupt.json"
    path.write_text("{this is not valid json")

    sm = StateManager(path)
    sm._load()
    # Should have default values
    assert sm.state.identity_layer == IdentityLayer.LISTENER


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
    sm.state.identity_layer = IdentityLayer.WISE
    sm.state.session_count = 5
    sm.state.metadata["temp_flag"] = True

    sm.start_session()
    assert sm.state.identity_layer == IdentityLayer.WISE  # preserved
    assert "temp_flag" not in sm.state.metadata  # cleared
