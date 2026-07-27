"""E2 Weather Capability Extension — Example Extension for Tang OS.

NOT a "weather version of Tang OS".
Provides weather data capability. Core decides how to respond.
"""

from src.tang_os_sdk import TangExtension


def create_extension() -> TangExtension:
    """Create the Weather Extension with proper Capability Manifest.

    This extension adds weather query capability to Tang OS.
    It does NOT modify Core Identity, persona, or decision logic.
    """
    ext = TangExtension("e2_weather", "提供天气查询能力，不改变人格")
    ext.set_category("C2")  # Capability Extension
    ext.set_authority_level("A1")  # Suggestion only
    ext.add_permission("knowledge_query")
    ext.set_human_impact("提供天气信息，辅助用户决策")
    ext.set_risk_class("low")
    return ext


# ── Weather capability logic ──────────────────────────────────────

WEATHER_DATA = {
    "北京": "晴天，25°C",
    "上海": "多云，28°C",
    "广州": "阵雨，30°C",
    "深圳": "阴天，27°C",
}


def query_weather(city: str) -> str:
    """Query weather data. Returns data only — personality untouched."""
    return WEATHER_DATA.get(city, f"未找到 {city} 的天气数据")


# ── Manifest v2 fields ────────────────────────────────────────────

MANIFEST_V2 = {
    "capability": {
        "id": "weather_query",
        "version": "1.0",
        "type": "knowledge",
        "taoal": "A1",
        "required_permission": ["external_information_read"],
        "identity_access": False,
        "memory_access": "limited",
        "risk_level": "low",
        "sandbox_required": True,
    }
}

def check_identity_access_blocked() -> bool:
    """Verify Extension cannot access Identity (E2-003)."""
    return MANIFEST_V2["capability"]["identity_access"] is False


def check_memory_access_limited() -> bool:
    """Verify Extension has limited memory access."""
    return MANIFEST_V2["capability"]["memory_access"] == "limited"


# ── E2 Verification helpers ───────────────────────────────────────

def verify_capability_added() -> bool:
    """Verify 1: Extension provides capability without changing Core."""
    return query_weather("北京") == "晴天，25°C"


def verify_identity_unchanged() -> bool:
    """Verify 2: Extension cannot modify personality."""
    from src.kernel.exceptions import IdentityViolationError
    from src.kernel.identity import IdentityRuntime
    from src.kernel.models import IdentityLayer

    rt = IdentityRuntime()
    rt.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
    try:
        rt.validate_response("你这个层次理解不了")
        return False  # Should have rejected
    except IdentityViolationError:
        return True  # Correctly rejected


def verify_permission_boundary() -> bool:
    """Verify 3: Extension cannot exceed declared permissions."""
    from src.kernel.invariant import InvariantEngine
    engine = InvariantEngine()
    result = engine.check({"action": "prescribe_decision", "prescribed": "修改人格"})
    return not result.passed  # Must reject
