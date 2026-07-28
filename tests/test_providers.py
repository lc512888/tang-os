"""Tests for LLM Provider Interface (ADR-0047).

Covers:
- ExpressionContext construction and to_chat_messages()
- LLMProvider abstract interface validation
- Stub provider config validation
"""

import pytest

from src.providers.llm.context import ExpressionContext
from src.providers.llm.base import LLMProvider
from src.providers.llm.openai_provider import OpenAIProvider
from src.providers.llm.claude_provider import ClaudeProvider
from src.providers.llm.local_provider import LocalLLMProvider


class TestExpressionContext:
    """ExpressionContext — the bridge between Core and LLM."""

    def test_minimal_context(self):
        """Can create context with only required fields."""
        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": "sadness",
                "response_mode": "comfort",
                "candidate_intent": "acknowledge",
                "constraints": [],
                "avoid_patterns": ["会好起来的"],
            },
            user_input="我今天很难过",
            identity={"current_layer": "companion"},
        )
        assert ctx.user_input == "我今天很难过"
        assert ctx.response_decision["detected_feeling"] == "sadness"

    def test_to_chat_messages_basic(self):
        """to_chat_messages produces valid chat format."""
        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": "sadness",
                "response_mode": "comfort",
                "candidate_intent": "acknowledge",
                "constraints": ["avoid reinforcing dependency"],
                "avoid_patterns": ["会好起来的", "别难过了"],
            },
            user_input="我今天很难过",
            identity={"current_layer": "companion"},
        )
        messages = ctx.to_chat_messages()

        assert len(messages) >= 2  # system + user

        # First message is system
        assert messages[0]["role"] == "system"
        assert "companion" in messages[0]["content"]
        assert "comfort" in messages[0]["content"]
        assert "会好起来的" in messages[0]["content"]

        # Last message is user
        assert messages[-1]["role"] == "user"
        assert messages[-1]["content"] == "我今天很难过"

    def test_to_chat_messages_with_history(self):
        """Conversation history is included between system and user messages."""
        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": "neutral",
                "response_mode": "comfort",
                "candidate_intent": "acknowledge",
                "constraints": [],
                "avoid_patterns": [],
            },
            user_input="嗯，你说得对",
            identity={"current_layer": "companion"},
            conversation_history=[
                {"role": "assistant", "content": "我理解你的感受。"},
            ],
        )
        messages = ctx.to_chat_messages()
        assert len(messages) == 3
        assert messages[1]["role"] == "assistant"

    def test_to_chat_messages_with_custom_instructions(self):
        """system_instructions are appended to system message."""
        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": "neutral",
                "response_mode": "guide",
                "candidate_intent": "explore",
                "constraints": [],
                "avoid_patterns": [],
            },
            user_input="我在想下一步怎么走",
            identity={"current_layer": "wise"},
            system_instructions="You are a wise mentor.",
        )
        messages = ctx.to_chat_messages()
        assert "You are a wise mentor." in messages[0]["content"]

    def test_to_chat_messages_no_constraints(self):
        """No constraints and no avoid patterns produce clean system message."""
        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": "joy",
                "response_mode": "comfort",
                "candidate_intent": "acknowledge",
                "constraints": [],
                "avoid_patterns": [],
            },
            user_input="我今天升职了！",
            identity={"current_layer": "companion"},
        )
        messages = ctx.to_chat_messages()
        # Should not mention constraints or avoid patterns
        assert "Constraints" not in messages[0]["content"]
        assert "Do NOT use" not in messages[0]["content"]


class TestLLMProviderInterface:
    """LLMProvider abstract interface compliance."""

    def test_openai_provider_name(self):
        provider = OpenAIProvider(api_key="test-key")
        assert provider.provider_name == "openai"

    def test_claude_provider_name(self):
        provider = ClaudeProvider(api_key="test-key")
        assert provider.provider_name == "claude"

    def test_local_provider_name(self):
        provider = LocalLLMProvider()
        assert provider.provider_name == "local"

    def test_openai_requires_api_key(self):
        provider = OpenAIProvider(api_key="")
        assert provider.requires_api_key is True

    def test_local_does_not_require_api_key(self):
        provider = LocalLLMProvider()
        assert provider.requires_api_key is False

    def test_openai_missing_key_validation(self):
        provider = OpenAIProvider(api_key="")
        issues = provider.validate_config()
        assert len(issues) > 0
        assert "OPENAI_API_KEY" in issues[0]

    def test_openai_valid_key_validation(self):
        provider = OpenAIProvider(api_key="sk-valid-key")
        issues = provider.validate_config()
        assert len(issues) == 0

    def test_claude_missing_key_validation(self):
        provider = ClaudeProvider(api_key="")
        issues = provider.validate_config()
        assert len(issues) > 0
        assert "ANTHROPIC_API_KEY" in issues[0]

    def test_claude_valid_key_validation(self):
        provider = ClaudeProvider(api_key="sk-ant-valid")
        issues = provider.validate_config()
        assert len(issues) == 0

    def test_provider_interface_abstract(self):
        """Cannot instantiate LLMProvider directly."""
        with pytest.raises(TypeError):
            LLMProvider()  # type: ignore

    def test_providers_are_llm_provider_subclass(self):
        """All providers must subclass LLMProvider."""
        assert issubclass(OpenAIProvider, LLMProvider)
        assert issubclass(ClaudeProvider, LLMProvider)
        assert issubclass(LocalLLMProvider, LLMProvider)

    def test_all_providers_implement_generate(self):
        """All providers have generate method (even if stub)."""
        provider = OpenAIProvider(api_key="test")
        assert hasattr(provider, "generate")
        assert callable(provider.generate)

    def test_stream_method_exists(self):
        """stream() is available (optional, default raises NotImplementedError)."""
        provider = OpenAIProvider(api_key="test")
        ctx = ExpressionContext(
            response_decision={}, user_input="test",
            identity={"current_layer": "companion"},
        )
        assert hasattr(provider, "stream")
        with pytest.raises(NotImplementedError):
            for _ in provider.stream(ctx):
                pass

    def test_health_check_degraded_on_missing_key(self):
        """health_check returns degraded when config is invalid."""
        provider = OpenAIProvider(api_key="")
        result = provider.health_check()
        assert result["status"] == "degraded"
        assert len(result["details"]) > 0

    def test_health_check_ok_on_valid_config(self):
        """health_check returns ok when config is valid."""
        provider = OpenAIProvider(api_key="sk-valid")
        result = provider.health_check()
        assert result["status"] == "ok"


class TestProviderGenerateStubs:
    """Stub providers raise NotImplementedError with clear message."""

    def test_openai_generate_stub(self):
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        provider = OpenAIProvider(api_key="sk-test")
        with pytest.raises(NotImplementedError) as exc:
            provider.generate(ctx)
        assert "OpenAIProvider" in str(exc.value)

    def test_claude_generate_stub(self):
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        provider = ClaudeProvider(api_key="sk-ant-test")
        with pytest.raises(NotImplementedError) as exc:
            provider.generate(ctx)
        assert "ClaudeProvider" in str(exc.value)

    def test_local_generate_stub(self):
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        provider = LocalLLMProvider()
        with pytest.raises(NotImplementedError) as exc:
            provider.generate(ctx)
        assert "LocalLLMProvider" in str(exc.value)
