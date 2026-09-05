"""Unsupported OpenAI-compatible provider skeleton.

The class preserves the provider interface and configuration shape, but
``generate()`` does not call an API and always raises
``ProviderUnsupportedError``. It is not a working OpenAI adapter.
"""

import os
from providers.llm.base import LLMProvider
from providers.llm.context import ExpressionContext
from providers.llm.exceptions import ProviderUnsupportedError


class OpenAIProvider(LLMProvider):
    """Reference skeleton for a future OpenAI-compatible provider."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4",
        base_url: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ):
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self._model = model
        self._base_url = base_url
        self._temperature = temperature
        self._max_tokens = max_tokens

    @property
    def provider_name(self) -> str:
        return "openai"

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
                "OPENAI_API_KEY not set. Pass api_key or set OPENAI_API_KEY env var."
            )
        return issues

    def generate(self, context: ExpressionContext) -> str:
        """Raise ``ProviderUnsupportedError``; generation is not implemented."""
        _ = context  # placeholder — full implementation pending openai client setup
        # TODO: Implement OpenAI API call
        # messages = context.to_chat_messages()
        # client = OpenAI(api_key=self._api_key, base_url=self._base_url)
        # response = client.chat.completions.create(
        #     model=self._model,
        #     messages=messages,
        #     temperature=self._temperature,
        #     max_tokens=self._max_tokens,
        # )
        # return response.choices[0].message.content
        raise ProviderUnsupportedError(
            "OpenAIProvider.generate() is a Reference Adapter Skeleton.\n"
            "It demonstrates the interface contract but does not include API client setup.\n"
            "To use: install 'openai' (pip install openai), set OPENAI_API_KEY,\n"
            "then implement and test a concrete adapter against the provider API."
        )
