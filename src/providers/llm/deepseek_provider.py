"""DeepSeek LLM Provider — First real LLM adapter for Tang OS.

DeepSeek API is OpenAI-compatible. This provider uses the `openai` Python
package with DeepSeek's base URL as the endpoint.

Architecture invariants (from ADR-0047 LP-003):
    - Provider MUST NOT modify Core Identity/State
    - Provider MUST respect avoid_patterns from ResponseDecision
    - Provider MUST NOT embed personality logic
    - Provider MUST NOT define Tang OS behavior rules

Tang OS decides HOW to respond (response mode, intent, constraints).
DeepSeek decides HOW TO EXPRESS the response in natural language.

Usage:
    provider = DeepSeekProvider()
    response = provider.generate(context)
"""

import os
from typing import Any

from src.providers.llm.base import LLMProvider
from src.providers.llm.context import ExpressionContext


# Default configuration
_DEFAULT_MODEL = "deepseek-chat"
_DEFAULT_BASE_URL = "https://api.deepseek.com/v1"
_DEFAULT_TIMEOUT = 60  # seconds
_DEFAULT_MAX_TOKENS = 2048
_DEFAULT_TEMPERATURE = 0.7


class DeepSeekProvider(LLMProvider):
    """LLM Provider for DeepSeek API (OpenAI-compatible).

    This is the first REAL provider implementation for Tang OS.
    It demonstrates the full Expression Layer contract in production.

    Configuration (in priority order: constructor arg > env var > default):
        api_key: DEEPSEEK_API_KEY
        model: DEEPSEEK_MODEL (default: deepseek-chat)
        base_url: DEEPSEEK_BASE_URL (default: https://api.deepseek.com/v1)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        temperature: float = _DEFAULT_TEMPERATURE,
        max_tokens: int = _DEFAULT_MAX_TOKENS,
        timeout: int = _DEFAULT_TIMEOUT,
    ):
        self._api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        self._model = model or os.environ.get(
            "DEEPSEEK_MODEL", _DEFAULT_MODEL
        )
        self._base_url = base_url or os.environ.get(
            "DEEPSEEK_BASE_URL", _DEFAULT_BASE_URL
        )
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._timeout = timeout
        self._client: Any = None  # lazy init

    @property
    def provider_name(self) -> str:
        return "deepseek"

    @property
    def requires_api_key(self) -> bool:
        return not self._api_key

    def validate_config(self) -> list[str]:
        """Validate configuration before making API calls."""
        issues = []
        if not self._api_key:
            issues.append(
                "DEEPSEEK_API_KEY not set. "
                "Pass api_key or set DEEPSEEK_API_KEY environment variable."
            )
        if not self._base_url:
            issues.append(
                "DEEPSEEK_BASE_URL not set. "
                "Pass base_url or set DEEPSEEK_BASE_URL environment variable."
            )
        # Verify OpenAI package is available
        try:
            import openai  # noqa: F401
        except ImportError:
            issues.append(
                "Missing required package: openai. "
                "Install with: pip install openai"
            )
        return issues

    def _get_client(self) -> Any:
        """Lazy-init the OpenAI client with DeepSeek configuration."""
        if self._client is None:
            from openai import OpenAI

            self._client = OpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
                timeout=self._timeout,
                max_retries=2,
            )
        return self._client

    def generate(self, context: ExpressionContext) -> str:
        """Generate a natural language response via DeepSeek API.

        Args:
            context: Complete expression context from Tang OS Core.

        Returns:
            Generated natural language response as a string.

        Raises:
            ProviderConfigError: If configuration is invalid.
            ProviderError: On API failure, rate limit, or network error.
        """
        # Step 1: Validate configuration
        issues = self.validate_config()
        if issues:
            raise ProviderConfigError(
                f"{self.provider_name} configuration errors:\n"
                + "\n".join(f"  - {i}" for i in issues)
            )

        # Step 2: Build messages from ExpressionContext
        messages = context.to_chat_messages()

        # Step 3: Call DeepSeek API
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )
        except ImportError as e:
            raise ProviderConfigError(
                f"Missing required package: openai. Install with: pip install openai"
            ) from e
        except Exception as e:
            raise ProviderError(
                f"{self.provider_name} API call failed: {e}"
            ) from e

        # Step 4: Extract response text
        try:
            text = response.choices[0].message.content
            if text is None:
                raise ProviderError(
                    f"{self.provider_name} returned empty response"
                )
            return text
        except (AttributeError, IndexError, TypeError) as e:
            raise ProviderError(
                f"{self.provider_name} unexpected response format: {e}"
            ) from e

    def stream(self, context: ExpressionContext):
        """Stream a response token by token from DeepSeek API.

        Args:
            context: Complete expression context from Tang OS Core.

        Yields:
            str: Text chunks as they are generated.

        Raises:
            ProviderConfigError: If configuration is invalid.
            ProviderError: On API failure, rate limit, or network error.
        """
        # Step 1: Validate configuration
        issues = self.validate_config()
        if issues:
            raise ProviderConfigError(
                f"{self.provider_name} configuration errors:\n"
                + "\n".join(f"  - {i}" for i in issues)
            )

        # Step 2: Build messages
        messages = context.to_chat_messages()

        # Step 3: Stream from DeepSeek API
        try:
            client = self._get_client()
            stream = client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature,
                max_tokens=self._max_tokens,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except ImportError as e:
            raise ProviderConfigError(
                "Missing required package: openai. Install with: pip install openai"
            ) from e
        except Exception as e:
            raise ProviderError(
                f"{self.provider_name} streaming failed: {e}"
            ) from e

    def health_check(self) -> dict:
        """Check if the provider is operational.

        Validates config and attempts a lightweight API connectivity check
        by listing available models (minimal cost).

        Returns:
            dict with keys:
                - status: str ('ok' | 'degraded' | 'unavailable')
                - details: list[str] — issue descriptions
        """
        # Base config validation
        issues = self.validate_config()
        if issues:
            return {"status": "degraded", "details": issues}

        # API connectivity check via model list (cheap call)
        try:
            client = self._get_client()
            client.models.list()
            return {"status": "ok", "details": []}
        except Exception as e:
            return {
                "status": "unavailable",
                "details": [f"API connectivity check failed: {e}"],
            }


class ProviderError(Exception):
    """Raised when an LLM Provider API call fails.

    This covers: network errors, rate limits, API errors, timeouts.
    """
    pass


class ProviderConfigError(Exception):
    """Raised when an LLM Provider has invalid or missing configuration.

    This covers: missing API keys, invalid endpoints, missing packages.
    """
    pass
