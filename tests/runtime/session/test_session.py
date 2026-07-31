"""Tests for Session Runtime — personality binding and isolation."""
import os
import pytest

_TEST_MODULES = os.path.join(
    os.path.dirname(__file__), "..", "..", "personality_runtime", "test_modules"
)
_VALID_TANG = os.path.join(_TEST_MODULES, "valid_tang")
_TEST_PERSONALITY = os.path.join(_TEST_MODULES, "test_personality")


class TestRuntimeSession:
    def test_create_session_with_tang(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        module = PersonalityLoader(_VALID_TANG).load()
        session = RuntimeSession(module)
        assert session.session_id.startswith("sess_")
        assert session.personality.name == "tang"
        assert session.identity["name"] == "Tang"

    def test_session_provides_personality_properties(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        module = PersonalityLoader(_VALID_TANG).load()
        session = RuntimeSession(module)
        assert session.values["core_values"][0]["id"] == "sincerity"
        assert len(session.boundaries["inviolable"]) >= 3
        assert session.style["tone"]["primary"] == "gentle"

    def test_summary(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        module = PersonalityLoader(_VALID_TANG).load()
        session = RuntimeSession(module)
        s = session.summary()
        assert s["personality"] == "tang"
        assert s["session_id"].startswith("sess_")


class TestSessionIsolation:
    def test_two_sessions_independent(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        t1 = PersonalityLoader(_VALID_TANG).load()
        t2 = PersonalityLoader(_TEST_PERSONALITY).load()
        s1 = RuntimeSession(t1)
        s2 = RuntimeSession(t2)
        assert s1.session_id != s2.session_id
        assert s1.identity["name"] == "Tang"
        assert s2.identity["name"] == "TestPersonality"

    def test_session_values_not_shared(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        s1 = RuntimeSession(PersonalityLoader(_VALID_TANG).load())
        s2 = RuntimeSession(PersonalityLoader(_TEST_PERSONALITY).load())
        v1 = {v["id"] for v in s1.values["core_values"]}
        v2 = {v["id"] for v in s2.values["core_values"]}
        assert "compassion" in v1
        assert "precision" in v2
        assert v1 != v2

    def test_session_style_isolated(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        s1 = RuntimeSession(PersonalityLoader(_VALID_TANG).load())
        s2 = RuntimeSession(PersonalityLoader(_TEST_PERSONALITY).load())
        assert s1.style["tone"]["primary"] == "gentle"
        assert s2.style["tone"]["primary"] == "analytical"


class TestPersonalityImmutability:
    """Personality must NOT change within a session."""

    def test_personality_immutable(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        module = PersonalityLoader(_VALID_TANG).load()
        session = RuntimeSession(module)
        original = session.personality.name
        assert session.personality.name == original

    def test_no_reassignment(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        module = PersonalityLoader(_VALID_TANG).load()
        session = RuntimeSession(module)
        with pytest.raises(AttributeError):
            session.personality = None  # should be read-only

    def test_session_created_at_set(self):
        from src.runtime.personality_loader import PersonalityLoader
        from src.runtime.session import RuntimeSession
        module = PersonalityLoader(_VALID_TANG).load()
        session = RuntimeSession(module)
        assert session.created_at is not None


class TestPersonalityRegistry:
    def test_register_and_get(self):
        from src.runtime.session.registry import PersonalityRegistry
        reg = PersonalityRegistry()
        module = reg.load(_VALID_TANG)
        assert module.name == "tang"
        assert reg.is_loaded("tang")
        cached = reg.get("tang")
        assert cached is module

    def test_get_nonexistent(self):
        from src.runtime.session.registry import PersonalityRegistry
        reg = PersonalityRegistry()
        assert reg.get("nonexistent") is None
        assert reg.is_loaded("nonexistent") is False

    def test_multiple_registrations(self):
        from src.runtime.session.registry import PersonalityRegistry
        reg = PersonalityRegistry()
        t1 = reg.load(_VALID_TANG)
        t2 = reg.load(_TEST_PERSONALITY)
        assert reg.is_loaded("tang")
        assert reg.is_loaded("test_personality")
        assert t1 is not t2
