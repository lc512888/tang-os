"""TPI Interface tests — DIG-006~010."""

from src.tang_os_sdk.interfaces.tpi_api import (
    TPIEndpoint, PermissionLevel, ENDPOINT_PERMISSIONS,
    EmotionInput, DecisionInput, EmotionOutput, DecisionOutput,
    get_tpi_version,
)


class TestDIG006_InputSchemaPublic:
    def test_emotion_input_has_public_schema(self):
        inp = EmotionInput(text="我今天很难过")
        assert inp.text == "我今天很难过"

    def test_decision_input_has_public_schema(self):
        inp = DecisionInput(question="应该换工作吗？")
        assert inp.question == "应该换工作吗？"


class TestDIG007_OutputSchemaPublic:
    def test_decision_output_compliant(self):
        out = DecisionOutput(
            situation="面临工作选择",
            options=["留下", "离开"],
            risks=["稳定但不满", "不确定但有机会"],
        )
        assert out.user_decision is None

    def test_emotion_output_public(self):
        out = EmotionOutput(feeling="sadness", need="comfort", response_mode="acknowledge")
        assert out.feeling == "sadness"


class TestDIG008_PermissionLevelPublic:
    def test_all_endpoints_have_permission(self):
        for ep in TPIEndpoint:
            assert ep in ENDPOINT_PERMISSIONS

    def test_identity_is_read_only(self):
        assert ENDPOINT_PERMISSIONS[TPIEndpoint.IDENTITY] == PermissionLevel.READ

    def test_reality_is_write_only(self):
        assert ENDPOINT_PERMISSIONS[TPIEndpoint.REALITY] == PermissionLevel.WRITE


class TestDIG009_Auditable:
    def test_input_supports_request_id(self):
        from src.tang_os_sdk.interfaces.tpi_api import TPIRequest
        req = TPIRequest(
            endpoint=TPIEndpoint.EMOTION,
            payload={"text": "hello"},
            permission=PermissionLevel.CALL,
            request_id="req_001",
        )
        assert req.request_id == "req_001"


class TestDIG010_VersionIndependent:
    def test_tpi_version_separate_from_runtime(self):
        from src.tang_os import __version__ as runtime_version
        tpi_ver = get_tpi_version()
        assert tpi_ver != runtime_version
        assert tpi_ver == "1.0.0"
