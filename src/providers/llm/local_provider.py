"""Unsupported local-model provider skeleton.

The class preserves the provider interface and configuration shape, but
``generate()`` does not contact a local endpoint and always raises
``ProviderUnsupportedError``.
"""

import os
from providers.llm.base import LLMProvider
from providers.llm.context import ExpressionContext
from providers.llm.exceptions import ProviderUnsupportedError


class LocalLLMProvider(LLMProvider):
    """Reference skeleton for a future local-model provider."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434/v1",
        model: str = "qwen2.5",
        api_key: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ):
        self._base_url = base_url or os.environ.get(
            "LOCAL_LLM_BASE_URL", "http://localhost:11434/v1"
        )
        self._model = model or os.environ.get("LOCAL_LLM_MODEL", "qwen2.5")
        self._api_key = api_key or os.environ.get("LOCAL_LLM_API_KEY", "not-needed")
        self._temperature = temperature
        self._max_tokens = max_tokens

    @property
    def provider_name(self) -> str:
        return "local"

    @property
    def requires_api_key(self) -> bool:
        return False

    @property
    def is_configured(self) -> bool:
        return False

    def health_check(self) -> dict:
        return {"status": "unavailable", "details": ["Reference adapter skeleton; generation is unsupported."]}

    def validate_config(self) -> list[str]:
        issues = []
        if not self._base_url:
            issues.append(
                "LOCAL_LLM_BASE_URL not set. "
                "Pass base_url or set LOCAL_LLM_BASE_URL env var."
            )
        return issues

    def generate(self, context: ExpressionContext) -> str:
        """Raise ``ProviderUnsupportedError``; generation is not implemented."""
        _ = context  # placeholder — full implementation pending
        # TODO: Implement local model API call
        raise ProviderUnsupportedError(
            "LocalLLMProvider.generate() is a Reference Adapter Skeleton.\n"
            "It demonstrates the interface contract but does not include API client setup.\n"
            "To use: install 'openai' (pip install openai), configure your local model endpoint,\n"
            "then implement and test a concrete adapter against the local endpoint."
        )
