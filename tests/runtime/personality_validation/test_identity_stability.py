"""Test Matrix 001: Identity Stability.

Load the same personality module 100 times.
All loads must produce identical identity, values, boundaries, style, capabilities.
"""
import os
import copy

_MODULES = os.path.join(os.path.dirname(__file__), "..", "..", "personality_runtime", "test_modules")
_VALID_TANG = os.path.join(_MODULES, "valid_tang")


def _load():
    from src.runtime.personality_loader import PersonalityLoader
    return PersonalityLoader(_VALID_TANG).load()


class TestIdentityStability:
    """100 identical loads must produce 100 identical results."""

    LOAD_COUNT = 100

    def test_100_loads_identical_identity(self):
        ref = _load()
        for i in range(self.LOAD_COUNT):
            m = _load()
            assert m.identity == ref.identity, f"Identity mismatch at load {i}"

    def test_100_loads_identical_values(self):
        ref = _load()
        for i in range(self.LOAD_COUNT):
            m = _load()
            assert m.values == ref.values, f"Values mismatch at load {i}"

    def test_100_loads_identical_boundaries(self):
        ref = _load()
        for i in range(self.LOAD_COUNT):
            m = _load()
            assert m.boundaries == ref.boundaries, f"Boundaries mismatch at load {i}"

    def test_100_loads_identical_style(self):
        ref = _load()
        for i in range(self.LOAD_COUNT):
            m = _load()
            assert m.style == ref.style, f"Style mismatch at load {i}"

    def test_100_loads_identical_manifest(self):
        ref = _load()
        for i in range(self.LOAD_COUNT):
            m = _load()
            assert m.manifest == ref.manifest, f"Manifest mismatch at load {i}"

    def test_module_name_unchanged(self):
        ref = _load()
        for i in range(self.LOAD_COUNT):
            m = _load()
            assert m.name == ref.name == "tang"

    def test_loads_different_objects(self):
        modules = [_load() for _ in range(10)]
        for i, m1 in enumerate(modules):
            for j, m2 in enumerate(modules):
                if i != j:
                    assert m1 is not m2, f"Same object at {i} and {j}"
