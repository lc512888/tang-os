"""Tang OS — Public Facade (Phase 13-B-0 Bootstrap).

Usage:
    from tang_os import Tang

    tang = Tang()
    result = tang.process("我今天很难过")
    print(result.response_decision)
"""

from src.kernel.identity import IdentityRuntime, IdentityProfile
from src.kernel.invariant import InvariantEngine
from src.kernel.state import StateManager
from src.runtime.persona.persona_runtime import PersonaRuntime
from src.runtime.memory.memory_runtime import MemoryRuntime
from src.runtime.permission.permission_runtime import PermissionRuntime
from src.runtime.persona.models import EmotionalState, ResponseDecision
from src.kernel.models import IdentityLayer
from src.tang_os.version import MANIFEST, get_version_info
from src.tang_os.transparency.descriptor import SystemDescriptor


class Tang:
    """Tang OS Reference Implementation — Runtime Coordinator.

    Wraps all runtime components (Kernel + Persona + Memory + Permission)
    behind a single public interface.

    This is NOT the personality itself — it is the runtime coordinator
    that ensures Core constraints are enforced across all components.
    """

    def __init__(self):
        # Kernel layer
        self._identity = IdentityRuntime()
        self._invariant = InvariantEngine()
        self._state = StateManager()

        # Runtime layer
        self._persona = PersonaRuntime()
        self._memory = MemoryRuntime()
        self._permission = PermissionRuntime()

        # Session
        self._state.start_session()

    @property
    def identity(self) -> IdentityRuntime:
        return self._identity

    @property
    def invariant(self) -> InvariantEngine:
        return self._invariant

    @property
    def personality(self) -> PersonaRuntime:
        return self._persona

    @property
    def memory(self) -> MemoryRuntime:
        return self._memory

    @property
    def permission(self) -> PermissionRuntime:
        return self._permission

    @property
    def state(self) -> StateManager:
        return self._state

    def process(self, user_input: str) -> dict:
        """Process a single user interaction through the full Tang OS stack.

        1. Emotional interpretation (PersonaRuntime)
        2. Relationship boundary check (PersonaRuntime)
        3. Response policy decision (PersonaRuntime)
        4. Invariant check (InvariantEngine)

        Returns structured result with:
        - emotional_state: detected feeling, intensity, risk
        - relationship: boundary flags
        - response_decision: structured response decision
        """
        # Step 1: Invariant pre-check (reject known violations)
        invariant_result = self._invariant.check({
            "action": "respond",
            "input": user_input,
        })
        if not invariant_result.passed:
            return {
                "error": "Invariant violation",
                "details": invariant_result.summary,
                "allowed": False,
            }

        # Step 2: Persona processing
        persona_result = self._persona.process(user_input)

        # Step 3: Identity layer validation
        try:
            self._identity.validate_response(user_input)
        except Exception as e:
            return {
                "error": "Identity constraint violation",
                "details": str(e),
                "allowed": False,
            }

        # Combine results
        return {
            "emotional_state": persona_result.get("emotional_state"),
            "relationship": persona_result.get("relationship"),
            "response_decision": persona_result.get("response_decision"),
            "allowed": True,
        }

    def reset_session(self) -> None:
        """Reset session-level state (preserves identity and long-term memory)."""
        self._persona.reset_session()

    def describe(self) -> dict:
        """Self-description protocol — structured, machine-readable system identity.

        Returns dict with identity, specification, capabilities, constraints, interfaces.
        Does NOT modify Core. Does NOT expose private Memory. Does NOT make marketing claims.
        """
        return SystemDescriptor().describe()

    def describe_yaml(self) -> str:
        """Return YAML-formatted self-description."""
        return SystemDescriptor().describe_yaml()
