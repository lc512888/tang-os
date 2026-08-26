"""LLM Provider sub-package — Natural language generation providers.

All providers implement the LLMProvider abstract interface defined in base.py.
Tang OS Core does NOT directly depend on any concrete provider.

Available providers:
- OpenAI-compatible (openai_provider.py)
- Claude / Anthropic API (claude_provider.py)
- Local model (local_provider.py)

Usage:
    from providers.llm import OpenAIProvider

    provider = OpenAIProvider(api_key="...", model="gpt-4")
    response = provider.generate(context)
"""

from providers.llm.base import LLMProvider
from providers.llm.context import ExpressionContext
from providers.llm.openai_provider import OpenAIProvider
from providers.llm.claude_provider import ClaudeProvider
from providers.llm.local_provider import LocalLLMProvider
from providers.llm.deepseek_provider import DeepSeekProvider
from providers.llm.exceptions import (
    ProviderError, ProviderConfigError, ProviderUnsupportedError, ProviderTransportError,
)

__all__ = [
    "LLMProvider",
    "ExpressionContext",
    "DeepSeekProvider",
    "ProviderError",
    "ProviderConfigError",
    "ProviderUnsupportedError",
    "ProviderTransportError",
    "OpenAIProvider",
    "ClaudeProvider",
    "LocalLLMProvider",
]
