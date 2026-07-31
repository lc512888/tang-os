"""Module Validator — validates personality module structure and content.

Checks per ADR-0051 Personality Module Contract and PERSONALITY_MODULE_SPEC.md.
"""

from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of a module validation."""
    passed: bool = True
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


REQUIRED_FILES = [
    "manifest.yaml",
    "identity.yaml",
    "values.yaml",
    "boundaries.yaml",
]


class ModuleValidator:
    """Validates a personality module against the contract."""

    def __init__(self, module_path: str):
        self._path = module_path
        self._result = ValidationResult()

    @property
    def result(self) -> ValidationResult:
        return self._result

    def validate(self) -> ValidationResult:
        """Run all validation checks."""
        self._result = ValidationResult()
        self._check_structure()
        self._check_manifest()
        self._check_identity()
        self._check_boundaries()
        return self._result

    def _check_structure(self):
        import os
        for f in REQUIRED_FILES:
            fp = os.path.join(self._path, f)
            if not os.path.isfile(fp):
                self._result.passed = False
                self._result.errors.append(f"Missing required file: {f}")

    def _load_yaml(self, filename: str) -> dict | None:
        import os, yaml
        fp = os.path.join(self._path, filename)
        if not os.path.isfile(fp):
            return None
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self._result.errors.append(f"Failed to parse {filename}: {e}")
            self._result.passed = False
            return None

    def _check_manifest(self):
        m = self._load_yaml("manifest.yaml")
        if m is None:
            return
        if not m.get("module_name"):
            self._result.errors.append("manifest missing module_name")
            self._result.passed = False
        if not m.get("version"):
            self._result.errors.append("manifest missing version")
            self._result.passed = False
        lang = m.get("language", "")
        if lang != "neutral":
            self._result.warnings.append(
                f"manifest language should be 'neutral' (got '{lang}')"
            )
        source = m.get("source", {})
        if not source.get("origin"):
            self._result.warnings.append("manifest missing source.origin (ADR-0055)")

    def _check_identity(self):
        i = self._load_yaml("identity.yaml")
        if i is None:
            return
        if not i.get("name"):
            self._result.errors.append("identity missing name")
            self._result.passed = False
        if not i.get("role"):
            self._result.errors.append("identity missing role")
            self._result.passed = False
        if i.get("language", "") != "neutral":
            self._result.warnings.append("identity language should be 'neutral'")

    def _check_boundaries(self):
        b = self._load_yaml("boundaries.yaml")
        if b is None:
            return
        rules = b.get("inviolable", [])
        if len(rules) < 3:
            self._result.errors.append(
                f"boundaries must have >=3 inviolable rules (got {len(rules)})"
            )
            self._result.passed = False
