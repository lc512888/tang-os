"""Tang OS — Public Facade (Phase 13-B-0 Bootstrap).

Usage:
    from tang_os import Tang

    tang = Tang()
    result = tang.process("我今天很难过")
    print(result["response_decision"])
"""

import os
from dataclasses import asdict, dataclass, fields, is_dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, Iterator, Mapping

from kernel.identity import IdentityRuntime, IdentityProfile
from kernel.exceptions import IdentityViolationError
from kernel.invariant import InvariantEngine
from runtime.persona.persona_runtime import PersonaRuntime
from runtime.memory.memory_runtime import MemoryRuntime
from runtime.permission.permission_runtime import PermissionRuntime
from runtime.persona.models import EmotionalState, ResponseDecision
from kernel.models import IdentityLayer
from tang_os.version import MANIFEST, get_version_info
from tang_os.transparency.descriptor import SystemDescriptor
from providers.llm.base import LLMProvider
from providers.llm.context import ExpressionContext
from providers.llm.exceptions import (
    ProviderConfigError, ProviderError, ProviderTransportError, ProviderUnsupportedError,
)

if TYPE_CHECKING:
    from kernel.state import StateManager


@dataclass(frozen=True)
class RespondResult:
    """Result of the explicit, opt-in natural-language expression path."""

    allowed: bool
    text: str | None
    decision: Mapping[str, Any]
    error: str | None = None
    details: str | None = None
    error_code: str | None = None
    error_type: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "decision", _immutable_snapshot(self.decision))


class FrozenRecord(Mapping[str, Any]):
    """Immutable record retaining both mapping and attribute-style reads."""

    __slots__ = ("_values",)

    def __init__(self, values: Mapping[str, Any]) -> None:
        object.__setattr__(self, "_values", MappingProxyType(dict(values)))

    def __getitem__(self, key: str) -> Any:
        return self._values[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._values)

    def __len__(self) -> int:
        return len(self._values)

    def __getattr__(self, name: str) -> Any:
        try:
            return self._values[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("FrozenRecord is immutable")


def _immutable_snapshot(value: Any) -> Any:
    """Create a deeply immutable, detached public-result snapshot."""
    if is_dataclass(value) and not isinstance(value, type):
        return FrozenRecord({
            item.name: _immutable_snapshot(getattr(value, item.name))
            for item in fields(value)
        })
    if isinstance(value, Mapping):
        return MappingProxyType({key: _immutable_snapshot(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_immutable_snapshot(item) for item in value)
    return value


class Tang:
    """Tang OS Reference Implementation — Runtime Coordinator.

    Exposes Kernel, Persona, Memory, Permission, and optional expression-provider
    components behind one public interface. ``process()`` itself runs only the
    invariant and persona decision path; it does not automatically read memory,
    request permission, call tools, or invoke a provider.

    This is NOT the personality itself — it is the runtime coordinator
    that ensures Core constraints are enforced across all components.
    """

    def __init__(
        self,
        state_path: str | os.PathLike[str] | None = None,
        *,
        memory: MemoryRuntime | None = None,
        permission: PermissionRuntime | None = None,
        provider: LLMProvider | None = None,
    ):
        from kernel.state import StateManager

        # Kernel layer
        self._identity = IdentityRuntime()
        self._invariant = InvariantEngine()
        # The environment override is primarily useful for isolated hosts and
        # test runners. With neither argument nor override, the historical
        # ``<cwd>/.tang_state.json`` default remains unchanged.
        resolved_state_path = (
            state_path if state_path is not None else os.getenv("TANG_OS_STATE_PATH")
        )
        self._state = StateManager(resolved_state_path)

        # Runtime layer
        self._persona = PersonaRuntime()
        self._memory = memory if memory is not None else MemoryRuntime()
        self._permission = permission if permission is not None else PermissionRuntime()
        self._provider = provider

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
    def state(self) -> "StateManager":
        return self._state

    @property
    def provider(self) -> LLMProvider | None:
        """Configured expression provider, or ``None`` for offline decision-only use."""
        return self._provider

    def process(self, user_input: str) -> dict:
        """Process one interaction through the deterministic decision path.

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

        # Combine results
        return {
            "emotional_state": persona_result.get("emotional_state"),
            "relationship": persona_result.get("relationship"),
            "response_decision": persona_result.get("response_decision"),
            "allowed": True,
        }

    def respond(
        self,
        user_input: str,
        *,
        memory_context: dict | None = None,
        conversation_history: list[dict] | None = None,
        system_instructions: str | None = None,
    ) -> RespondResult:
        """Generate an optional utterance through the configured provider.

        This method is deliberately opt-in. ``process()`` remains deterministic,
        offline, and provider-independent. Memory is never read automatically;
        callers must explicitly pass already-authorized ``memory_context``.
        Persona interaction state may advance during ``process()`` before a
        provider failure. Such failures do not write memory, permission, tool,
        or external device state.
        """
        decision = self.process(user_input)
        if not decision.get("allowed", False):
            return RespondResult(
                allowed=False,
                text=None,
                decision=decision,
                error=decision.get("error"),
                details=decision.get("details"),
                error_code="decision_rejected",
                error_type="policy",
            )
        if self._provider is None:
            return RespondResult(
                allowed=False,
                text=None,
                decision=decision,
                error="Provider not configured",
                details="Pass provider=... to Tang() to opt in to text generation.",
                error_code="provider_not_configured",
                error_type="configuration",
            )

        response_decision = decision["response_decision"]
        serialized_decision = asdict(response_decision)
        for key, value in list(serialized_decision.items()):
            if hasattr(value, "value"):
                serialized_decision[key] = value.value
        try:
            context = ExpressionContext(
                response_decision=serialized_decision,
                user_input=user_input,
                identity={"current_layer": self._identity.current_layer.value},
                conversation_history=conversation_history,
                memory_context=memory_context,
                system_instructions=system_instructions,
            )
        except (TypeError, ValueError):
            return RespondResult(
                allowed=False, text=None, decision=decision,
                error="Invalid expression context", details="Caller-supplied context was rejected.",
                error_code="invalid_context", error_type="validation",
            )
        try:
            text = self._provider.generate(context)
            if not isinstance(text, str) or not text.strip():
                return RespondResult(
                    allowed=False, text=None, decision=decision,
                    error="Expression provider returned an invalid response",
                    details="The provider response must be a non-empty string.",
                    error_code="provider_invalid_response", error_type="provider",
                )
            self._identity.validate_response(text)
        except IdentityViolationError:
            return RespondResult(
                allowed=False,
                text=None,
                decision=decision,
                error="Identity constraint violation",
                details="Generated text did not satisfy identity constraints.",
                error_code="identity_violation",
                error_type="policy",
            )
        except ProviderConfigError:
            return RespondResult(
                allowed=False,
                text=None,
                decision=decision,
                error="Expression provider is not configured",
                details="Check the selected provider configuration.",
                error_code="provider_configuration_error",
                error_type="configuration",
            )
        except ProviderUnsupportedError:
            return RespondResult(
                allowed=False, text=None, decision=decision,
                error="Expression provider operation is unsupported",
                details="Choose an adapter that implements text generation.",
                error_code="provider_unsupported", error_type="provider",
            )
        except (ProviderTransportError, ProviderError):
            return RespondResult(
                allowed=False, text=None, decision=decision,
                error="Expression provider failure",
                details="The provider could not complete the request.",
                error_code="provider_failure", error_type="provider",
            )
        return RespondResult(allowed=True, text=text, decision=decision)

    def reset_session(self) -> None:
        """Reset process-local persona interaction state.

        This does not read, write, or clear ``MemoryRuntime``. Separately managed
        non-content identity/session metadata may remain in ``StateManager``.
        """
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
