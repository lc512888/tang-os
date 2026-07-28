"""Local LLM Provider — Fully offline, no API key required.

Supports locally hosted models via OpenAI-compatible endpoints
(Ollama, vLLM, llama.cpp, etc.).

Usage:
    # With Ollama (default): no API key needed
    provider = LocalLLMProvider(base_url="http://localhost:11434/v1", model="qwen2.5")

    # With vLLM or other OpenAI-compatible local server
    provider = LocalLLMProvider(
        base_url="http://localhost:8000/v1",
        model="mistral-7b",
        api_key="not-needed"
    )
"""

import os
from src.providers.llm.base import LLMProvider
from src.providers.llm.context import ExpressionContext


class LocalLLMProvider(LLMProvider):
    """LLM Provider for locally hosted models via OpenAI-compatible API."""

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

    def validate_config(self) -> list[str]:
        issues = []
        if not self._base_url:
            issues.append(
                "LOCAL_LLM_BASE_URL not set. "
                "Pass base_url or set LOCAL_LLM_BASE_URL env var."
            )
        return issues

    def generate(self, context: ExpressionContext) -> str:
        """Generate response via local model's OpenAI-compatible endpoint.

        Note: This is a reference implementation stub.
        Production use requires the 'openai' package.
        """
        _ = context  # placeholder — full implementation pending
        # TODO: Implement local model API call
        raise NotImplementedError(
            "LocalLLMProvider.generate() is a Reference Adapter Skeleton.\n"
            "It demonstrates the interface contract but does not include API client setup.\n"
            "To use: install 'openai' (pip install openai), configure your local model endpoint,\n"
            "then uncomment the implementation in this method."
        )
