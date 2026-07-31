"""PersonalityRegistry — caches loaded personality modules."""

from src.runtime.personality_loader import PersonalityLoader, PersonalityModule


class PersonalityRegistry:
    """Registry of loaded personality modules, keyed by module name.

    Modules are loaded once and cached for reuse across sessions.
    """

    def __init__(self):
        self._cache: dict[str, PersonalityModule] = {}

    def load(self, module_path: str) -> PersonalityModule:
        """Load a module by path. Caches by module name.

        If the module was already loaded, returns cached instance.
        """
        loader = PersonalityLoader(module_path)
        module = loader.load()
        self._cache[module.name] = module
        return module

    def get(self, name: str) -> PersonalityModule | None:
        """Get a cached module by name."""
        return self._cache.get(name)

    def is_loaded(self, name: str) -> bool:
        return name in self._cache

    def clear(self):
        self._cache.clear()
