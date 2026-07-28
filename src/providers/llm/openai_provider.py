"""OpenAI-compatible LLM Provider.

Supports OpenAI API and any OpenAI-compatible service (vLLM, Ollama, etc.).

Requires:
    - openai Python package (pip install openai)
    - API key set via OPENAI_API_KEY environment variable or constructor

Usage:
    provider = OpenAIProvider(api_key="sk-...", model="gpt-4")
    response = provider.generate(context)
"""

import os
from src.providers.llm.base import LLMProvider
from src.providers.llm.context import ExpressionContext


class OpenAIProvider(LLMProvider):
    """LLM Provider for OpenAI-compatible APIs."""

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
        return not self._api_key

    def validate_config(self) -> list[str]:
        issues = []
        if not self._api_key:
            issues.append(
                "OPENAI_API_KEY not set. Pass api_key or set OPENAI_API_KEY env var."
            )
        return issues

    def generate(self, context: ExpressionContext) -> str:
        """Generate response via OpenAI API.

        Note: This is a reference implementation stub.
        Production use requires the 'openai' package.
        """
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
        raise NotImplementedError(
            "OpenAIProvider.generate() is a Reference Adapter Skeleton.\n"
            "It demonstrates the interface contract but does not include API client setup.\n"
            "To use: install 'openai' (pip install openai), set OPENAI_API_KEY,\n"
            "then uncomment the implementation in this method."
        )
