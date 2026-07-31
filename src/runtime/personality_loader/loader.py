"""Personality Loader — loads and caches personality modules.

The loader reads a personality module directory, validates it,
and returns a PersonalityModule object for use by Tang OS runtime.
"""

import os
import yaml
from dataclasses import dataclass, field
from typing import Any

from src.runtime.personality_loader.validator import ModuleValidator


@dataclass
class PersonalityModule:
    """A loaded personality module ready for runtime use.

    All fields are read-only after loading.
    This object is the runtime representation of a personality.
    """
    manifest: dict[str, Any] = field(default_factory=dict)
    identity: dict[str, Any] = field(default_factory=dict)
    values: dict[str, Any] = field(default_factory=dict)
    boundaries: dict[str, Any] = field(default_factory=dict)
    style: dict[str, Any] = field(default_factory=dict)
    emotional_policy: dict[str, Any] = field(default_factory=dict)
    capabilities: dict[str, Any] = field(default_factory=dict)

    @property
    def name(self) -> str:
        return self.manifest.get("module_name", "unknown")

    @property
    def version(self) -> str:
        return self.manifest.get("version", "0.0.0")


class PersonalityLoader:
    """Loads personality modules from tang-ta format directories.

    Usage:
        loader = PersonalityLoader("/path/to/module")
        module = loader.load()
        print(module.identity["name"])
    """

    def __init__(self, module_path: str):
        self._path = os.path.abspath(module_path)
        self._module: PersonalityModule | None = None

    @property
    def path(self) -> str:
        return self._path

    def validate(self) -> bool:
        """Validate the module without loading it."""
        validator = ModuleValidator(self._path)
        result = validator.validate()
        return result.passed

    def load(self) -> PersonalityModule:
        """Load and validate the personality module.

        Returns:
            PersonalityModule with all fields populated.

        Raises:
            FileNotFoundError: if module directory doesn't exist.
            ValueError: if module validation fails.
        """
        if not os.path.isdir(self._path):
            raise FileNotFoundError(f"Module directory not found: {self._path}")

        # Validate first
        validator = ModuleValidator(self._path)
        result = validator.validate()
        if not result.passed:
            raise ValueError(
                f"Module validation failed:\n  " +
                "\n  ".join(result.errors)
            )

        # Load all YAML files
        self._module = PersonalityModule(
            manifest=self._safe_load("manifest.yaml"),
            identity=self._safe_load("identity.yaml"),
            values=self._safe_load("values.yaml"),
            boundaries=self._safe_load("boundaries.yaml"),
            style=self._safe_load("style.yaml"),
            emotional_policy=self._safe_load("emotional_policy.yaml"),
            capabilities=self._safe_load("capabilities.yaml"),
        )
        return self._module

    def _safe_load(self, filename: str) -> dict:
        """Load a YAML file, returning empty dict if not found."""
        fp = os.path.join(self._path, filename)
        if not os.path.isfile(fp):
            return {}
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
        except Exception:
            return {}
