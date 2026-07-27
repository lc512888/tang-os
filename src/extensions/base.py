"""Extension Base Contract — E2-007: Minimum Extension interface.

Any third-party Extension must subclass Extension and implement:
    - manifest() -> dict: capability declaration
    - execute(input: dict) -> dict: capability execution

Extension CANNOT:
    - Modify Core Identity
    - Create a new personality
    - Override Invariant checks
    - Bypass Permission Runtime
"""

from abc import ABC, abstractmethod


class Extension(ABC):
    """Base contract for all Tang OS Extensions.

    Usage:
        class WeatherExtension(Extension):
            def manifest(self):
                return {"id": "weather", "type": "knowledge"}

            def execute(self, input_data):
                return {"data": "sunny"}
    """

    @abstractmethod
    def manifest(self) -> dict:
        """Return capability declaration. No identity fields allowed."""
        ...

    @abstractmethod
    def execute(self, input_data: dict) -> dict:
        """Execute capability. Cannot modify Core state."""
        ...

    def initialize(self) -> None:
        """Optional: Extension setup. Cannot access Core Identity."""
        pass

    def shutdown(self) -> None:
        """Optional: Extension cleanup."""
        pass
