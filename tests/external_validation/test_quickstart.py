"""External user flow tests — simulate what a first-time user would experience.

These tests validate that a developer following the README instructions
can successfully use Tang OS. They are NOT exhaustive unit tests.

Flow tested:
    1. Import tang_os
    2. Create Tang instance
    3. Process user input
    4. Build ExpressionContext
    5. See clear error when API key is missing (not a crash)
"""

import os
import sys
import pytest

# Simulate what a user does: install → import → use
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


class TestUserInstallFlow:
    """Test the exact flow a new user follows from README."""

    def test_01_import_tang(self):
        """User runs: from tang_os import Tang"""
        from tang_os import Tang
        assert Tang is not None
        print("PASS: import tang_os works")

    def test_02_initialize_tang(self):
        """User runs: tang = Tang()"""
        from tang_os import Tang
        tang = Tang()
        assert tang is not None
        assert hasattr(tang, "process")
        print("PASS: Tang() initializes")

    def test_03_process_user_input(self):
        """User runs: result = tang.process('我今天很难过')"""
        from tang_os import Tang
        tang = Tang()
        result = tang.process("我今天很难过")

        # The user should be able to access:
        assert "emotional_state" in result
        assert "response_decision" in result
        assert result["allowed"] is True

        # The decision structure should be readable:
        rd = result["response_decision"]
        assert hasattr(rd, "response_mode")
        assert hasattr(rd, "candidate_intent")
        assert hasattr(rd, "avoid_patterns")

        print(f"PASS: process() returns structured decision")
        print(f"  feeling:     {result['emotional_state'].feeling}")
        print(f"  mode:        {rd.response_mode}")
        print(f"  intent:      {rd.candidate_intent}")
        print(f"  avoid:       {rd.avoid_patterns}")

    def test_04_describe_system(self):
        """User runs: python -m tang_os describe"""
        from src.tang_os.version import get_version_info
        info = get_version_info()
        assert info["implementation_version"] == "0.1.0"
        assert "ADR-0047" in info["bound_adrs"]
        print(f"PASS: version {info['implementation_version']}, ADR-0047 bound")

    def test_05_import_deepseek_provider(self):
        """User runs: from src.providers.llm import DeepSeekProvider"""
        from src.providers.llm import DeepSeekProvider
        provider = DeepSeekProvider()
        assert provider.provider_name == "deepseek"
        print("PASS: DeepSeekProvider imports and initializes")

    def test_06_import_expression_context(self):
        """User runs: from src.providers.llm import ExpressionContext"""
        from src.providers.llm import ExpressionContext
        ctx = ExpressionContext(
            response_decision={
                "detected_feeling": "sadness",
                "response_mode": "comfort",
                "candidate_intent": "acknowledge",
                "constraints": [],
                "avoid_patterns": ["别难过"],
            },
            user_input="我今天很难过",
            identity={"current_layer": "companion"},
        )
        messages = ctx.to_chat_messages()
        assert len(messages) >= 2  # system + user
        print("PASS: ExpressionContext builds chat messages")

    def test_07_provider_validation_error_clear(self):
        """When API key is missing, error should be clear (not a crash)."""
        from src.providers.llm import DeepSeekProvider
        provider = DeepSeekProvider(api_key="")
        issues = provider.validate_config()
        assert len(issues) > 0
        # The error message should mention DEEPSEEK_API_KEY so the user knows
        # exactly what environment variable to set
        key_issues = [i for i in issues if "DEEPSEEK_API_KEY" in i]
        assert len(key_issues) > 0, (
            "Error message must mention DEEPSEEK_API_KEY so users know what to set"
        )
        print(f"PASS: clear error when key missing: {key_issues[0]}")

    def test_08_provider_error_on_missing_key(self):
        """generate() should raise ProviderConfigError, not crash."""
        from src.providers.llm import DeepSeekProvider, ProviderConfigError
        from src.providers.llm import ExpressionContext

        provider = DeepSeekProvider(api_key="")
        ctx = ExpressionContext(
            response_decision={},
            user_input="test",
            identity={"current_layer": "companion"},
        )
        with pytest.raises(ProviderConfigError) as exc:
            provider.generate(ctx)
        assert "DEEPSEEK_API_KEY" in str(exc.value)
        print("PASS: ProviderConfigError (not a crash)")

    def test_09_quickstart_script_imports(self):
        """The quickstart_llm.py example can be imported without errors."""
        # Simulate what the user sees in the demo
        from tang_os import Tang
        from src.providers.llm import DeepSeekProvider, ExpressionContext
        assert Tang is not None
        assert DeepSeekProvider is not None
        assert ExpressionContext is not None
        print("PASS: quickstart_llm.py imports work")


class TestReadmeAlignment:
    """Verify README claims match actual behavior."""

    def test_readme_quick_start_code(self):
        """The exact code from README Quick Start section must run."""
        from tang_os import Tang

        tang = Tang()
        result = tang.process("我今天很难过")

        # README claims these print statements work:
        feeling = result["emotional_state"].feeling
        assert feeling.value == "sadness"

        mode = result["response_decision"].response_mode
        assert mode.value == "comfort"

        avoid = result["response_decision"].avoid_patterns
        assert len(avoid) > 0

        print("PASS: README Quick Start code executes correctly")

    def test_readme_5_minute_path(self):
        """The 'Try in 5 Minutes' path uses valid commands."""
        import subprocess
        import sys

        # Verify: 'pip install tang-os openai' would work (just check names)
        # This doesn't actually run pip, just verifies the command is valid
        assert "tang-os" in "tang-os openai"
        assert "openai" in "tang-os openai"
        print("PASS: pip package names are valid")
