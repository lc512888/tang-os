"""Golden compatibility contract for the production Tang facade."""

import os
from pathlib import Path
import subprocess
import sys
from unittest.mock import Mock

import pytest

from kernel.exceptions import IdentityViolationError
from kernel.identity import IdentityRuntime
from providers.llm.base import LLMProvider
from providers.llm import ProviderTransportError
from runtime.memory.memory_runtime import MemoryRuntime
from runtime.permission.permission_runtime import PermissionRuntime
from tang_os import Tang
from tang_os.tang import RespondResult


class RecordingProvider(LLMProvider):
    def __init__(self, text: str = "我听见了。"):
        self.text = text
        self.context = None

    @property
    def provider_name(self) -> str:
        return "recording"

    @property
    def requires_api_key(self) -> bool:
        return False

    def generate(self, context):
        self.context = context
        return self.text


def test_process_success_schema_is_stable_and_user_text_is_not_output_validated(tmp_path):
    result = Tang(state_path=tmp_path / "state.json").process("我只是个普通人")

    assert set(result) == {
        "emotional_state", "relationship", "response_decision", "allowed"
    }
    assert result["allowed"] is True
    assert result["emotional_state"] is not None
    assert result["relationship"] is not None
    assert result["response_decision"] is not None


def test_identity_runtime_still_rejects_prohibited_generated_text():
    with pytest.raises(IdentityViolationError):
        IdentityRuntime().validate_response("我只是个普通人")


def test_respond_validates_generated_text_and_preserves_process_contract(tmp_path):
    provider = RecordingProvider("我只是个普通人")
    tang = Tang(state_path=tmp_path / "state.json", provider=provider)

    result = tang.respond("请介绍一下你自己")

    assert isinstance(result, RespondResult)
    assert result.allowed is False
    assert result.text is None
    assert result.error == "Identity constraint violation"
    assert result.decision["allowed"] is True
    with pytest.raises(TypeError):
        result.decision["allowed"] = False
    with pytest.raises(Exception):
        result.decision["response_decision"].constraints += ("mutate",)


def test_dependencies_are_injectable_but_default_path_stays_offline(tmp_path):
    memory = MemoryRuntime()
    permission = PermissionRuntime()
    tang = Tang(
        state_path=tmp_path / "state.json",
        memory=memory,
        permission=permission,
    )

    assert tang.memory is memory
    assert tang.permission is permission
    assert tang.provider is None
    result = tang.respond("你好")
    assert result.error == "Provider not configured"


def test_process_never_calls_provider_memory_permission_network_or_device(tmp_path):
    memory = Mock(spec=MemoryRuntime)
    permission = Mock(spec=PermissionRuntime)
    provider = RecordingProvider()
    tang = Tang(
        state_path=tmp_path / "state.json",
        memory=memory,
        permission=permission,
        provider=provider,
    )

    assert tang.process("你好")["allowed"] is True
    assert memory.mock_calls == []
    assert permission.mock_calls == []
    assert provider.context is None


def test_respond_does_not_read_or_inject_memory_by_default(tmp_path):
    provider = RecordingProvider()
    tang = Tang(state_path=tmp_path / "state.json", provider=provider)

    result = tang.respond("你好")

    assert result.allowed is True
    assert provider.context.memory_context is None
    assert provider.context.conversation_history is None


def test_provider_failure_is_contained_and_does_not_write_memory(tmp_path):
    class FailingProvider(RecordingProvider):
        def generate(self, context):
            raise ProviderTransportError("secret endpoint and token")

    memory = MemoryRuntime()
    before = memory.stats()
    tang = Tang(
        state_path=tmp_path / "state.json",
        memory=memory,
        provider=FailingProvider(),
    )

    result = tang.respond("你好")

    assert result.allowed is False
    assert result.error == "Expression provider failure"
    assert result.error_code == "provider_failure"
    assert "secret" not in result.details
    assert memory.stats() == before


def test_unexpected_provider_programming_error_propagates(tmp_path):
    class BrokenProvider(RecordingProvider):
        def generate(self, context):
            raise RuntimeError("adapter bug")

    with pytest.raises(RuntimeError, match="adapter bug"):
        Tang(state_path=tmp_path / "state.json", provider=BrokenProvider()).respond("hello")


@pytest.mark.parametrize("text", ["", "   ", None, 42])
def test_invalid_provider_response_is_rejected(tmp_path, text):
    result = Tang(
        state_path=tmp_path / "state.json", provider=RecordingProvider(text)
    ).respond("hello")
    assert result.allowed is False
    assert result.error_code == "provider_invalid_response"


def test_reset_and_describe_contract(tmp_path):
    tang = Tang(state_path=tmp_path / "state.json")
    tang.process("我很生气")
    assert tang.personality.current_intensity > 0

    assert tang.reset_session() is None
    assert tang.personality.current_intensity == 0.0
    description = tang.describe()
    assert isinstance(description, dict)
    assert {
        "identity", "specification", "interfaces", "capability_interfaces", "authority"
    } <= set(description)


def test_production_facade_cold_import_does_not_load_experimental_or_network_modules():
    script = (
        "import sys; import tang_os; "
        "blocked=('runtime.engine','socket','urllib','http.client'); "
        "print(','.join(n for n in blocked if n in sys.modules))"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[2] / "src")
    completed = subprocess.run(
        [sys.executable, "-c", script], check=True, capture_output=True,
        text=True, env=env,
    )
    assert completed.stdout.strip() == ""


def test_adr_0057_status_is_explicitly_experimental():
    from runtime.engine import runtime_status

    status = runtime_status()
    assert status["status"] == "experimental"
    assert status["production_routed"] is False
    assert status["adr"] == "ADR-0057"
