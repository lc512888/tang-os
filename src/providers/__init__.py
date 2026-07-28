"""Tang OS Provider Layer — External service adapters.

Providers sit between Tang OS Core and external AI services (LLM, TTS, etc.).
They implement the Expression Layer contract, transforming structured
ResponseDecision into natural language through pluggable backends.

This package follows the architecture principle:
    Personality logic ≠ Model capability.
    LLM is expression, not identity.
"""

from src.providers.llm.base import LLMProvider
from src.providers.llm.context import ExpressionContext

__all__ = ["LLMProvider", "ExpressionContext"]
