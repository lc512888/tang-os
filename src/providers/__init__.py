"""Tang OS Provider Layer — External service adapters.

Providers sit between Tang OS Core and external AI services (LLM, TTS, etc.).
They implement the Expression Layer contract, transforming structured
ResponseDecision into natural language through pluggable backends.

This package follows the architecture principle:
    Personality logic ≠ Model capability.
    LLM is expression, not identity.
"""

from providers.llm.base import LLMProvider
from providers.llm.context import ExpressionContext
from providers.llm.deepseek_provider import DeepSeekProvider
from providers.llm.exceptions import (
    ProviderError, ProviderConfigError, ProviderUnsupportedError, ProviderTransportError,
)

__all__ = [
    "LLMProvider", "ExpressionContext", "DeepSeekProvider",
    "ProviderError", "ProviderConfigError", "ProviderUnsupportedError", "ProviderTransportError",
]
