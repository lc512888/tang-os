"""Unsupported Claude / Anthropic provider skeleton.

The class preserves the provider interface and configuration shape, but
``generate()`` does not call an API and always raises
``ProviderUnsupportedError``. It is not a working Anthropic adapter.
"""

import os
from providers.llm.base import LLMProvider
from providers.llm.context import ExpressionContext
from providers.llm.exceptions import ProviderUnsupportedError


class ClaudeProvider(LLMProvider):
    """Reference skeleton for a future Anthropic Claude provider."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 1024,
        temperature: float = 0.7,
    ):
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self._model = model
        self._max_tokens = max_tokens
        self._temperature = temperature

    @property
    def provider_name(self) -> str:
        return "claude"

    @property
    def requires_api_key(self) -> bool:
        return True

    @property
    def is_configured(self) -> bool:
        return False

    def health_check(self) -> dict:
        return {"status": "unavailable", "details": ["Reference adapter skeleton; generation is unsupported."]}

    def validate_config(self) -> list[str]:
        issues = []
        if not self._api_key:
            issues.append(
                "ANTHROPIC_API_KEY not set. "
                "Pass api_key or set ANTHROPIC_API_KEY env var."
            )
        return issues

    def generate(self, context: ExpressionContext) -> str:
        """Raise ``ProviderUnsupportedError``; generation is not implemented."""
        _ = context  # placeholder — full implementation pending anthropic client setup
        # TODO: Implement Claude API call
        # messages = context.to_chat_messages()
        # client = Anthropic(api_key=self._api_key)
        # response = client.messages.create(
        #     model=self._model,
        #     max_tokens=self._max_tokens,
        #     temperature=self._temperature,
        #     system=messages[0]["content"] if messages[0]["role"] == "system" else "",
        #     messages=[m for m in messages if m["role"] != "system"],
        # )
        # return response.content[0].text
        raise ProviderUnsupportedError(
            "ClaudeProvider.generate() is a Reference Adapter Skeleton.\n"
            "It demonstrates the interface contract but does not include API client setup.\n"
            "To use: install 'anthropic' (pip install anthropic), set ANTHROPIC_API_KEY,\n"
            "then implement and test a concrete adapter against the provider API."
        )
