"""State Manager — runtime state persistence & context hygiene (RIV-001, RIV-005).

Manages serialisation of identity state across sessions,
ensuring no context leakage between sessions and clean fallback on corruption.
"""

import json
import logging
import os
from copy import deepcopy
from pathlib import Path
import tempfile
from datetime import datetime
from dataclasses import asdict
from kernel.models import RuntimeState, IdentityLayer
from kernel.exceptions import StatePersistenceError

logger = logging.getLogger(__name__)

STATE_VERSION = "1.0"


class StateManager:
    """Manages runtime state with persistence.

    - Preserves identity layer across sessions (RIV-001)
    - Isolates session context from persistent state (RIV-005)
    - Handles corruption gracefully with default fallback

    Writes are crash-safe and atomic on one host filesystem. Coordination of
    concurrent writers in separate processes is intentionally out of scope;
    callers sharing a state path must provide an external lock.
    """

    def __init__(self, state_path: str | Path | None = None):
        self._path = Path(state_path) if state_path is not None else Path.cwd() / ".tang_state.json"
        self._state = RuntimeState()
        self._state.metadata["version"] = STATE_VERSION
        self._load()

    @property
    def state(self) -> RuntimeState:
        """Return a detached snapshot of runtime state."""
        return deepcopy(self._state)

    def update_state(
        self,
        *,
        identity_layer: IdentityLayer | None = None,
        last_interaction: str | None = None,
        metadata: dict | None = None,
    ) -> None:
        """Apply validated state changes without exposing internal mutable state."""
        if identity_layer is not None:
            if not isinstance(identity_layer, IdentityLayer):
                raise TypeError("identity_layer must be an IdentityLayer")
            self._state.identity_layer = identity_layer
        if last_interaction is not None:
            if not isinstance(last_interaction, str):
                raise TypeError("last_interaction must be a string")
            self._state.last_interaction = last_interaction
        if metadata is not None:
            if not isinstance(metadata, dict):
                raise TypeError("metadata must be a mapping")
            self._state.metadata.update(deepcopy(metadata))

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
        temporary_path: Path | None = None
        try:
            data = {
                "identity_layer": self._state.identity_layer.value,
                "session_count": self._state.session_count,
                "last_interaction": self._state.last_interaction,
                "metadata": self._state.metadata,
            }
            payload = json.dumps(data, ensure_ascii=False, indent=2)
            self._path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, raw_path = tempfile.mkstemp(
                prefix=f".{self._path.name}.", suffix=".tmp", dir=self._path.parent
            )
            temporary_path = Path(raw_path)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
                stream.write(payload)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_path, self._path)
            temporary_path = None
        except (OSError, UnicodeError, TypeError, ValueError) as e:
            raise StatePersistenceError("Failed to save runtime state") from e
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError:
                    logger.warning(
                        "Could not clean up state temporary file at %s", temporary_path
                    )

    def _load(self) -> RuntimeState:
        """Load state from disk, falling back to defaults on error."""
        if not self._path.exists():
            logger.debug("No state file found at %s — using defaults", self._path)
            return self._state

        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise TypeError("state root must be an object")

            layer_str = data.get("identity_layer", IdentityLayer.LISTENER.value)
            if not isinstance(layer_str, str):
                raise TypeError("identity_layer must be a string")
            layer = IdentityLayer(layer_str)

            session_count = data.get("session_count", 0)
            if isinstance(session_count, bool) or not isinstance(session_count, int):
                raise TypeError("session_count must be an integer")
            if session_count < 0:
                raise ValueError("session_count must not be negative")

            last_interaction = data.get("last_interaction")
            if last_interaction is not None and not isinstance(last_interaction, str):
                raise TypeError("last_interaction must be a string or null")

            metadata = data.get("metadata", {})
            if not isinstance(metadata, dict):
                raise TypeError("metadata must be an object")

            self._state = RuntimeState(
                identity_layer=layer,
                session_count=session_count,
                last_interaction=last_interaction,
                metadata=metadata,
            )
            if "version" not in self._state.metadata:
                self._state.metadata["version"] = STATE_VERSION
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError) as e:
            logger.warning(
                "Invalid state file at %s (%s) — using defaults",
                self._path,
                type(e).__name__,
            )
            self._state = RuntimeState()
            self._state.metadata["version"] = STATE_VERSION

        return self._state
