"""Claude / Anthropic API LLM Provider.

Supports Anthropic's Claude API — the recommended provider for Tang OS
due to Claude's strong personality consistency and instruction following.

Requires:
    - anthropic Python package (pip install anthropic)
    - API key set via ANTHROPIC_API_KEY environment variable or constructor

Usage:
    provider = ClaudeProvider(api_key="sk-ant-...", model="claude-sonnet-4-20250514")
    response = provider.generate(context)
"""

import os
from src.providers.llm.base import LLMProvider
from src.providers.llm.context import ExpressionContext


class ClaudeProvider(LLMProvider):
    """LLM Provider for Anthropic's Claude API."""

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
        return not self._api_key

    def validate_config(self) -> list[str]:
        issues = []
        if not self._api_key:
            issues.append(
                "ANTHROPIC_API_KEY not set. "
                "Pass api_key or set ANTHROPIC_API_KEY env var."
            )
        return issues

    def generate(self, context: ExpressionContext) -> str:
        """Generate response via Anthropic Claude API.

        Note: This is a reference implementation stub.
        Production use requires the 'anthropic' package.
        """
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
        raise NotImplementedError(
            "ClaudeProvider.generate() is a Reference Adapter Skeleton.\n"
            "It demonstrates the interface contract but does not include API client setup.\n"
            "To use: install 'anthropic' (pip install anthropic), set ANTHROPIC_API_KEY,\n"
            "then uncomment the implementation in this method."
        )
