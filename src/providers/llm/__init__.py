"""LLM Provider sub-package — Natural language generation providers.

All providers implement the LLMProvider abstract interface defined in base.py.
Tang OS Core does NOT directly depend on any concrete provider.

Available providers:
- OpenAI-compatible (openai_provider.py)
- Claude / Anthropic API (claude_provider.py)
- Local model (local_provider.py)

Usage:
    from src.providers.llm import OpenAIProvider

    provider = OpenAIProvider(api_key="...", model="gpt-4")
    response = provider.generate(context)
"""

from src.providers.llm.base import LLMProvider
from src.providers.llm.context import ExpressionContext
from src.providers.llm.openai_provider import OpenAIProvider
from src.providers.llm.claude_provider import ClaudeProvider
from src.providers.llm.local_provider import LocalLLMProvider
from src.providers.llm.deepseek_provider import DeepSeekProvider, ProviderError, ProviderConfigError

__all__ = [
    "LLMProvider",
    "ExpressionContext",
    "DeepSeekProvider",
    "ProviderError",
    "ProviderConfigError",
    "OpenAIProvider",
    "ClaudeProvider",
    "LocalLLMProvider",
]
