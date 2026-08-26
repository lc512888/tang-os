"""LLMProvider — Abstract base class for all LLM providers.

Tang OS Core does NOT directly depend on any LLM model.
All natural language generation passes through this interface.

Each provider implementation:
    1. Receives ExpressionContext (containing ResponseDecision)
    2. Generates natural language via its model API
    3. Returns plain text response

Architecture invariants (from ADR-0047 LP-003):
    - Provider MUST NOT modify Core Identity/State
    - Provider MUST respect avoid_patterns from ResponseDecision
    - Provider SHOULD follow candidate_intent from ResponseDecision
    - Provider MUST NOT persist data to its own storage
"""

from abc import ABC, abstractmethod

from providers.llm.context import ExpressionContext
from providers.llm.exceptions import ProviderUnsupportedError


class LLMProvider(ABC):
    """Abstract LLM Provider — Tang OS does not own the model.

    Any LLM that implements this interface can serve as the
    expression layer for Tang OS personality runtime.

    Usage:
        class MyProvider(LLMProvider):
            def generate(self, context: ExpressionContext) -> str:
                ...
    """

    @abstractmethod
    def generate(self, context: ExpressionContext) -> str:
        """Generate a natural language response from Tang OS context.

        The implementation:
        - MAY use ExpressionContext.to_chat_messages() as message base
        - MUST respect context.response_decision["avoid_patterns"]
        - SHOULD follow context.response_decision["candidate_intent"]
        - MUST NOT modify Tang OS Core state

        Args:
            context: Complete expression context from Tang OS Core.

        Returns:
            Generated natural language response as a string.

        Raises:
            ProviderError: On API failure, rate limit, or auth error.
            ProviderConfigError: On missing/invalid configuration.
        """
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider identifier.

        Returns:
            e.g. 'openai', 'claude', 'local'
        """
        ...

    @property
    def requires_api_key(self) -> bool:
        """Whether this adapter's service requires an API key capability."""
        return True

    @property
    def is_configured(self) -> bool:
        """Whether the current adapter configuration passes validation."""
        return not self.validate_config()

    def stream(self, context: ExpressionContext):  # type: ignore[return]
        """Stream a response token by token when an adapter supports it.

        Default implementation raises NotImplementedError.
        Override in provider when streaming support is available.

        Args:
            context: Complete expression context from Tang OS Core.

        Yields:
            str: Text chunks as they are generated.

        Raises:
            NotImplementedError: If provider does not support streaming.
        """
        raise ProviderUnsupportedError(
            f"{self.provider_name} does not support streaming. "
            "Implement stream() in the concrete adapter to add this capability."
        )

    def health_check(self) -> dict:
        """Check whether the provider configuration appears operational.

        Default implementation pings validate_config.

        Returns:
            dict with keys:
                - status: str ('ok' | 'degraded' | 'unavailable')
                - details: list[str] — issue descriptions if degraded
        """
        issues = self.validate_config()
        if issues:
            return {"status": "degraded", "details": issues}
        return {"status": "ok", "details": []}

    def validate_config(self) -> list[str]:
        """Validate provider configuration.

        Returns:
            List of configuration issue descriptions.
            Empty list means configuration is valid.
        """
        return []
