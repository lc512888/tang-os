"""Personality Module Loader — loads personality modules from tang-ta format.

A personality module is a directory of YAML manifest files that describe
a personality's identity, values, boundaries, style, and capabilities.

This loader validates the module against the Personality Module Contract
(ADR-0051) and makes it available to the Tang OS runtime.

Usage:
    loader = PersonalityLoader("/path/to/module")
    module = loader.load()
    print(module.identity["name"])
"""

from src.runtime.personality_loader.loader import PersonalityLoader, PersonalityModule
from src.runtime.personality_loader.validator import ModuleValidator, ValidationResult

__all__ = ["PersonalityLoader", "PersonalityModule", "ModuleValidator", "ValidationResult"]
