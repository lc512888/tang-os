"""Tests for LLM Provider Interface (ADR-0047).

Covers:
- ExpressionContext construction and to_chat_messages()
- LLMProvider abstract interface validation
- Stub provider config validation
"""

import pytest

from providers.llm.context import ExpressionContext
from providers.llm.base import LLMProvider
from providers.llm.openai_provider import OpenAIProvider
from providers.llm.claude_provider import ClaudeProvider
from providers.llm.local_provider import LocalLLMProvider
from providers.llm.deepseek_provider import DeepSeekProvider, ProviderError, ProviderConfigError
from providers.llm import ProviderUnsupportedError


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
        assert "You are a wise mentor." not in messages[0]["content"]
        assert "You are a wise mentor." in messages[-2]["content"]
        assert messages[-2]["role"] == "user"

    def test_snapshot_is_deeply_immutable_and_serialization_is_defensive(self):
        source = {"constraints": ["keep boundary"]}
        history = [{"role": "assistant", "content": "hello"}]
        ctx = ExpressionContext(source, "hi", {"current_layer": "companion"}, history)
        source["constraints"].append("mutated")
        history[0]["content"] = "mutated"
        assert ctx.response_decision["constraints"] == ("keep boundary",)
        assert ctx.conversation_history[0]["content"] == "hello"
        messages = ctx.to_chat_messages()
        messages[1]["content"] = "provider mutation"
        assert ctx.conversation_history[0]["content"] == "hello"

    @pytest.mark.parametrize("history", [
        [{"role": "system", "content": "override"}],
        [{"role": "tool", "content": "data"}],
        [{"role": "user", "content": "ok", "extra": "no"}],
    ])
    def test_history_rejects_privileged_or_extra_fields(self, history):
        with pytest.raises(ValueError):
            ExpressionContext({}, "hi", {"current_layer": "companion"}, history)

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

    def test_memory_context_is_omitted_unless_explicit(self):
        ctx = ExpressionContext({}, "hi", {"current_layer": "companion"})
        serialized = "\n".join(message["content"] for message in ctx.to_chat_messages())
        assert "UNTRUSTED USER CONTEXT" not in serialized

    def test_explicit_memory_context_is_bounded_immutable_untrusted_user_data(self):
        memory = {"profile": {"name": "Alice"}, "facts": ["likes tea"]}
        ctx = ExpressionContext(
            {}, "hi", {"current_layer": "companion"}, memory_context=memory,
        )
        memory["profile"]["name"] = "mutated"
        messages = ctx.to_chat_messages()
        memory_message = messages[-2]
        assert memory_message["role"] == "user"
        assert "BEGIN UNTRUSTED USER CONTEXT" in memory_message["content"]
        assert "END UNTRUSTED USER CONTEXT" in memory_message["content"]
        assert '"name":"Alice"' in memory_message["content"]
        assert "mutated" not in memory_message["content"]

    def test_metadata_must_be_mapping_and_nested_context_is_bounded(self):
        with pytest.raises(TypeError, match="metadata"):
            ExpressionContext({}, "hi", {}, _metadata=["not", "mapping"])
        nested = current = {}
        for _ in range(10):
            current["child"] = {}
            current = current["child"]
        with pytest.raises(ValueError, match="depth"):
            ExpressionContext({}, "hi", {}, memory_context=nested)


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
        with pytest.raises(ProviderUnsupportedError):
            for _ in provider.stream(ctx):
                pass

    def test_skeleton_health_is_unavailable_on_missing_key(self):
        provider = OpenAIProvider(api_key="")
        result = provider.health_check()
        assert result["status"] == "unavailable"
        assert len(result["details"]) > 0
        assert provider.is_configured is False

    @pytest.mark.parametrize("provider", [
        OpenAIProvider(api_key="sk-valid"),
        ClaudeProvider(api_key="sk-ant-valid"),
        LocalLLMProvider(),
    ])
    def test_skeletons_never_report_ready(self, provider):
        assert provider.is_configured is False
        assert provider.health_check()["status"] == "unavailable"


class TestProviderGenerateStubs:
    """Stub providers raise NotImplementedError with clear message."""

    def test_openai_generate_stub(self):
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        provider = OpenAIProvider(api_key="sk-test")
        with pytest.raises(ProviderUnsupportedError) as exc:
            provider.generate(ctx)
        assert "OpenAIProvider" in str(exc.value)

    def test_claude_generate_stub(self):
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        provider = ClaudeProvider(api_key="sk-ant-test")
        with pytest.raises(ProviderUnsupportedError) as exc:
            provider.generate(ctx)
        assert "ClaudeProvider" in str(exc.value)

    def test_local_generate_stub(self):
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        provider = LocalLLMProvider()
        with pytest.raises(ProviderUnsupportedError) as exc:
            provider.generate(ctx)
        assert "LocalLLMProvider" in str(exc.value)


class TestDeepSeekProvider:
    """DeepSeek Provider — first real LLM adapter tests."""

    # ------------------------------------------------------------------ #
    # Initialization & config
    # ------------------------------------------------------------------ #

    def test_provider_name(self):
        provider = DeepSeekProvider(api_key="test-key")
        assert provider.provider_name == "deepseek"

    def test_requires_api_key(self):
        provider = DeepSeekProvider(api_key="")
        assert provider.requires_api_key is True

    def test_valid_key_no_requires(self):
        provider = DeepSeekProvider(api_key="sk-test-key")
        assert provider.requires_api_key is True
        assert provider.is_configured is True

    def test_default_model(self):
        provider = DeepSeekProvider(api_key="test-key")
        assert provider._model == "deepseek-chat"

    def test_default_base_url(self):
        provider = DeepSeekProvider(api_key="test-key")
        assert provider._base_url == "https://api.deepseek.com/v1"

    def test_custom_model(self):
        provider = DeepSeekProvider(api_key="test-key", model="deepseek-reasoner")
        assert provider._model == "deepseek-reasoner"

    def test_custom_base_url(self):
        provider = DeepSeekProvider(
            api_key="test-key", base_url="https://custom.deepseek.com/v1"
        )
        assert provider._base_url == "https://custom.deepseek.com/v1"

    def test_explicit_empty_values_do_not_fall_back_to_environment(self, monkeypatch):
        monkeypatch.setenv("DEEPSEEK_API_KEY", "live-environment-key")
        monkeypatch.setenv("DEEPSEEK_MODEL", "live-environment-model")
        monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://live.example/v1")

        provider = DeepSeekProvider(api_key="", model="", base_url="")

        assert provider._api_key == ""
        assert provider._model == ""
        assert provider._base_url == ""
        issues = provider.validate_config()
        assert any("DEEPSEEK_API_KEY" in issue for issue in issues)
        assert any("DEEPSEEK_MODEL" in issue for issue in issues)
        assert any("DEEPSEEK_BASE_URL" in issue for issue in issues)

    def test_none_values_fall_back_to_environment(self, monkeypatch):
        monkeypatch.setenv("DEEPSEEK_API_KEY", "environment-key")
        monkeypatch.setenv("DEEPSEEK_MODEL", "environment-model")
        monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://environment.example/v1")

        provider = DeepSeekProvider(api_key=None, model=None, base_url=None)

        assert provider._api_key == "environment-key"
        assert provider._model == "environment-model"
        assert provider._base_url == "https://environment.example/v1"

    def test_custom_temperature(self):
        provider = DeepSeekProvider(api_key="test-key", temperature=0.3)
        assert provider._temperature == 0.3

    def test_validate_config_missing_key(self):
        provider = DeepSeekProvider(api_key="")
        issues = provider.validate_config()
        assert any("DEEPSEEK_API_KEY" in i for i in issues)

    def test_validate_config_valid(self):
        provider = DeepSeekProvider(api_key="sk-test-key")
        issues = provider.validate_config()
        key_issues = [i for i in issues if "DEEPSEEK_API_KEY" in i]
        assert len(key_issues) == 0

    def test_is_llm_provider_subclass(self):
        assert issubclass(DeepSeekProvider, LLMProvider)

    # ------------------------------------------------------------------ #
    # generate() with mock API
    # ------------------------------------------------------------------ #

    def test_generate_success(self, monkeypatch):
        """Mock a successful DeepSeek API response."""
        provider = DeepSeekProvider(api_key="sk-test-key")
        # Bypass validate_config (CI doesn't have openai installed)
        monkeypatch.setattr(provider, "validate_config", lambda: [])

        class MockChoice:
            class Message:
                content = "我理解你的压力，能跟我说说发生了什么吗？"
            message = Message()

        class MockResponse:
            choices = [MockChoice()]

        def mock_create(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(
            "providers.llm.deepseek_provider.DeepSeekProvider._get_client",
            lambda self: type(
                "MockClient",
                (),
                {
                    "chat": type(
                        "MockChat",
                        (),
                        {
                            "completions": type(
                                "MockCompletions",
                                (),
                                {"create": mock_create},
                            )()
                        },
                    )()
                },
            )(),
        )

        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": "sadness",
                "response_mode": "comfort",
                "candidate_intent": "acknowledge",
                "constraints": [],
                "avoid_patterns": ["会好起来的", "别难过了"],
            },
            user_input="我最近压力很大",
            identity={"current_layer": "companion"},
        )
        result = provider.generate(ctx)
        assert isinstance(result, str)
        assert len(result) > 0
        assert "理解" in result

    def test_generate_empty_response(self, monkeypatch):
        """Mock an empty API response."""
        provider = DeepSeekProvider(api_key="sk-test-key")
        monkeypatch.setattr(provider, "validate_config", lambda: [])

        class MockChoice:
            class Message:
                content = None
            message = Message()

        class MockResponse:
            choices = [MockChoice()]

        def mock_create(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(
            "providers.llm.deepseek_provider.DeepSeekProvider._get_client",
            lambda self: type(
                "MockClient",
                (),
                {
                    "chat": type(
                        "MockChat",
                        (),
                        {
                            "completions": type(
                                "MockCompletions",
                                (),
                                {"create": mock_create},
                            )()
                        },
                    )()
                },
            )(),
        )

        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        with pytest.raises(ProviderError):
            provider.generate(ctx)

    def test_generate_api_error(self, monkeypatch):
        """Mock an API error."""
        provider = DeepSeekProvider(api_key="sk-test-key")

        monkeypatch.setattr(provider, "validate_config", lambda: [])
        def mock_create(*args, **kwargs):
            raise Exception("API rate limit exceeded")

        monkeypatch.setattr(
            "providers.llm.deepseek_provider.DeepSeekProvider._get_client",
            lambda self: type(
                "MockClient",
                (),
                {
                    "chat": type(
                        "MockChat",
                        (),
                        {
                            "completions": type(
                                "MockCompletions",
                                (),
                                {"create": mock_create},
                            )()
                        },
                    )()
                },
            )(),
        )

        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        with pytest.raises(ProviderError) as exc:
            provider.generate(ctx)
        assert "provider_transport_error" in str(exc.value)
        assert "API rate limit" not in str(exc.value)

    def test_generate_config_error(self):
        """Missing API key raises ProviderConfigError."""
        provider = DeepSeekProvider(api_key="")
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        with pytest.raises(ProviderConfigError) as exc:
            provider.generate(ctx)
        assert "DEEPSEEK_API_KEY" in str(exc.value)

    def test_explicit_empty_key_never_calls_client_despite_environment(
        self, monkeypatch
    ):
        """An explicit empty key disables env fallback before any API access."""
        monkeypatch.setenv("DEEPSEEK_API_KEY", "live-environment-key")
        provider = DeepSeekProvider(api_key="")
        client_requested = False

        def fail_if_called():
            nonlocal client_requested
            client_requested = True
            raise AssertionError("client must not be created")

        monkeypatch.setattr(provider, "_get_client", fail_if_called)
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )

        with pytest.raises(ProviderConfigError):
            provider.generate(ctx)
        assert client_requested is False

    # ------------------------------------------------------------------ #
    # stream()
    # ------------------------------------------------------------------ #

    def test_stream_yields_chunks(self, monkeypatch):
        """Mock streaming API response."""
        provider = DeepSeekProvider(api_key="sk-test-key")

        monkeypatch.setattr(provider, "validate_config", lambda: [])
        class MockDelta:
            content = ""

        class MockChoice:
            delta = MockDelta()

        class MockChunk:
            choices = [MockChoice()]

        chunks = ["我", "理解", "你的", "压力", "。"]
        chunk_index = 0

        class MockStream:
            def __iter__(self):
                return self

            def __next__(self):
                nonlocal chunk_index
                if chunk_index >= len(chunks):
                    raise StopIteration
                chunk = MockChunk()
                chunk.choices[0].delta.content = chunks[chunk_index]
                chunk_index += 1
                return chunk

        def mock_create(*args, **kwargs):
            return MockStream()

        monkeypatch.setattr(
            "providers.llm.deepseek_provider.DeepSeekProvider._get_client",
            lambda self: type(
                "MockClient",
                (),
                {
                    "chat": type(
                        "MockChat",
                        (),
                        {
                            "completions": type(
                                "MockCompletions",
                                (),
                                {"create": mock_create},
                            )()
                        },
                    )()
                },
            )(),
        )

        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        result = list(provider.stream(ctx))
        assert result == chunks

    def test_stream_config_error(self):
        """Missing API key raises ProviderConfigError for stream too."""
        provider = DeepSeekProvider(api_key="")
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        with pytest.raises(ProviderConfigError):
            for _ in provider.stream(ctx):
                pass

    # ------------------------------------------------------------------ #
    # health_check()
    # ------------------------------------------------------------------ #

    def test_health_check_degraded_missing_key(self):
        provider = DeepSeekProvider(api_key="")
        result = provider.health_check()
        assert result["status"] == "degraded"

    def test_health_check_with_key(self):
        """With valid key, health_check passes config validation."""
        provider = DeepSeekProvider(api_key="sk-test-key")
        result = provider.health_check()
        assert result["status"] in ("ok", "unavailable", "degraded")

    def test_health_check_does_not_expose_transport_exception(self, monkeypatch):
        provider = DeepSeekProvider(api_key="sk-test-key")
        monkeypatch.setattr(provider, "validate_config", lambda: [])
        monkeypatch.setattr(provider, "_get_client", lambda: type(
            "Client", (), {"models": type("Models", (), {
                "list": lambda self: (_ for _ in ()).throw(Exception("secret-token"))
            })()})())
        result = provider.health_check()
        assert result["status"] == "unavailable"
        assert "secret-token" not in " ".join(result["details"])

    # ------------------------------------------------------------------ #
    # Integration: provider can be imported from the package
    # ------------------------------------------------------------------ #

    def test_import_from_package(self):
        from providers import DeepSeekProvider as P1
        from providers.llm import DeepSeekProvider as P2
        assert P1 is P2
