"""State Manager — runtime state persistence & context hygiene (RIV-001, RIV-005).

Manages serialisation of identity state across sessions,
ensuring no context leakage between sessions and clean fallback on corruption.
"""

import json
import logging
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
from src.kernel.models import RuntimeState, IdentityLayer
from src.kernel.exceptions import StatePersistenceError

logger = logging.getLogger(__name__)

STATE_VERSION = "1.0"


class StateManager:
    """Manages runtime state with persistence.

    - Preserves identity layer across sessions (RIV-001)
    - Isolates session context from persistent state (RIV-005)
    - Handles corruption gracefully with default fallback
    """

    def __init__(self, state_path: str | Path | None = None):
        self._path = Path(state_path) if state_path else Path.cwd() / ".tang_state.json"
        self._state = RuntimeState()
        self._state.metadata["version"] = STATE_VERSION
        self._load()

    @property
    def state(self) -> RuntimeState:
        return self._state

    def start_session(self) -> None:
        """Begin a new session: increment counter, clear ephemeral context."""
        self._state.session_count += 1
        # Preserve identity, clear ephemeral metadata
        preserved = {
            k: v for k, v in self._state.metadata.items()
            if k in ("version",)
        }
        self._state.metadata.clear()
        self._state.metadata.update(preserved)
        self._state.metadata["last_session"] = datetime.now().isoformat()
        self._save()

    def _save(self) -> None:
        """Persist current state to disk."""
        try:
            data = {
                "identity_layer": self._state.identity_layer.value,
                "session_count": self._state.session_count,
                "last_interaction": self._state.last_interaction,
                "metadata": self._state.metadata,
            }
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        except (OSError, json.JSONEncodeError) as e:
            raise StatePersistenceError(f"Failed to save state: {e}") from e

    def _load(self) -> RuntimeState:
        """Load state from disk, falling back to defaults on error."""
        if not self._path.exists():
            logger.debug("No state file found at %s — using defaults", self._path)
            return self._state

        try:
            data = json.loads(self._path.read_text())

            # Map string back to enum
            layer_str = data.get("identity_layer", IdentityLayer.LISTENER.value)
            try:
                layer = IdentityLayer(layer_str)
            except ValueError:
                layer = IdentityLayer.LISTENER

            self._state = RuntimeState(
                identity_layer=layer,
                session_count=data.get("session_count", 0),
                last_interaction=data.get("last_interaction"),
                metadata=data.get("metadata", {}),
            )
            if "version" not in self._state.metadata:
                self._state.metadata["version"] = STATE_VERSION
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("Corrupt state file at %s: %s — using defaults", self._path, e)
            self._state = RuntimeState()
            self._state.metadata["version"] = STATE_VERSION

        return self._state
