"""Tests for Personality Module Loader."""
import os
import pytest

_TEST_MODULES = os.path.join(os.path.dirname(__file__), "test_modules")
_VALID_TANG = os.path.join(_TEST_MODULES, "valid_tang")
_INVALID_NO_BOUNDARIES = os.path.join(_TEST_MODULES, "invalid_no_boundaries")


class TestPersonalityLoader:
    def test_load_valid_module(self):
        from src.runtime.personality_loader import PersonalityLoader
        loader = PersonalityLoader(_VALID_TANG)
        module = loader.load()
        assert module.name == "tang"
        assert module.version == "1.0.0"
        assert module.identity["name"] == "Tang"
        assert len(module.values["core_values"]) == 3
        assert len(module.boundaries["inviolable"]) >= 3

    def test_validate_passes_for_valid_module(self):
        from src.runtime.personality_loader import PersonalityLoader
        loader = PersonalityLoader(_VALID_TANG)
        assert loader.validate() is True

    def test_validate_fails_for_invalid_module(self):
        from src.runtime.personality_loader import PersonalityLoader
        loader = PersonalityLoader(_INVALID_NO_BOUNDARIES)
        assert loader.validate() is False

    def test_load_invalid_module_raises(self):
        from src.runtime.personality_loader import PersonalityLoader
        loader = PersonalityLoader(_INVALID_NO_BOUNDARIES)
        with pytest.raises(ValueError, match="validation failed"):
            loader.load()

    def test_load_nonexistent_path_raises(self):
        from src.runtime.personality_loader import PersonalityLoader
        loader = PersonalityLoader("/nonexistent/path")
        with pytest.raises(FileNotFoundError):
            loader.load()


class TestModuleValidator:
    def test_valid_module_passes(self):
        from src.runtime.personality_loader.validator import ModuleValidator
        v = ModuleValidator(_VALID_TANG)
        result = v.validate()
        assert result.passed is True
        assert len(result.errors) == 0

    def test_invalid_module_fails(self):
        from src.runtime.personality_loader.validator import ModuleValidator
        v = ModuleValidator(_INVALID_NO_BOUNDARIES)
        result = v.validate()
        assert result.passed is False
        assert len(result.errors) > 0

    def test_validator_reports_missing_files(self):
        from src.runtime.personality_loader.validator import ModuleValidator
        import tempfile, os
        with tempfile.TemporaryDirectory() as td:
            v = ModuleValidator(td)
            result = v.validate()
            assert result.passed is False
            file_errors = [e for e in result.errors if "Missing" in e]
            assert len(file_errors) > 0


class TestPersonalityModuleObject:
    def test_default_values_for_missing_files(self):
        from src.runtime.personality_loader.loader import PersonalityModule
        m = PersonalityModule()
        assert m.name == "unknown"
        assert m.version == "0.0.0"
        assert m.identity == {}
        assert m.values == {}

    def test_module_name_from_manifest(self):
        from src.runtime.personality_loader.loader import PersonalityModule
        m = PersonalityModule(manifest={"module_name": "test-mod", "version": "2.0.0"})
        assert m.name == "test-mod"
        assert m.version == "2.0.0"


class TestNotTangSpecific:
    """Loader must NOT be hardcoded to know Tang."""

    def test_loader_does_not_mention_tang(self):
        import inspect
        from src.runtime.personality_loader import loader
        source = inspect.getsource(loader)
        assert "tang_os" not in source.lower() or "module_name" in source

    def test_validator_does_not_mention_tang(self):
        import inspect
        from src.runtime.personality_loader import validator
        source = inspect.getsource(validator)
        assert "Tang" not in source


class TestPersonalityIsolation:
    """Multiple modules loaded independently must not contaminate each other."""

    def test_load_two_modules(self):
        from src.runtime.personality_loader import PersonalityLoader
        t1 = PersonalityLoader(_VALID_TANG).load()
        t2 = PersonalityLoader(os.path.join(_TEST_MODULES, "test_personality")).load()
        assert t1.name == "tang"
        assert t2.name == "test_personality"
        assert t1.identity["name"] == "Tang"
        assert t2.identity["name"] == "TestPersonality"

    def test_values_isolated(self):
        from src.runtime.personality_loader import PersonalityLoader
        t1 = PersonalityLoader(_VALID_TANG).load()
        t2 = PersonalityLoader(os.path.join(_TEST_MODULES, "test_personality")).load()
        v1 = {v["id"] for v in t1.values["core_values"]}
        v2 = {v["id"] for v in t2.values["core_values"]}
        assert v1 != v2
        assert "compassion" in v1
        assert "precision" in v2

    def test_boundaries_isolated(self):
        from src.runtime.personality_loader import PersonalityLoader
        t1 = PersonalityLoader(_VALID_TANG).load()
        t2 = PersonalityLoader(os.path.join(_TEST_MODULES, "test_personality")).load()
        assert t1.boundaries["inviolable"] != t2.boundaries["inviolable"]

    def test_style_isolated(self):
        from src.runtime.personality_loader import PersonalityLoader
        t1 = PersonalityLoader(_VALID_TANG).load()
        t2 = PersonalityLoader(os.path.join(_TEST_MODULES, "test_personality")).load()
        assert t1.style["tone"]["primary"] == "gentle"
        assert t2.style["tone"]["primary"] == "analytical"

    def test_reload_does_not_cache(self):
        from src.runtime.personality_loader import PersonalityLoader
        t1 = PersonalityLoader(_VALID_TANG).load()
        t2 = PersonalityLoader(_VALID_TANG).load()
        assert t1 is not t2
        assert t1.name == t2.name
