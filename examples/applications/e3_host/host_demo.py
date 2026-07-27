"""E3 Host Adaptation Demo — Same Core, Multiple Hosts.

Shows that Tang OS Core maintains consistent identity,
feeling detection, and decision framework across different Host types,
while allowing expression to adapt to Host capabilities.
"""

from src.host.host_runtime import HostRuntime
from src.host.models import HostType, TAAL


class HostDemo:
    """Demonstrates identical internal state across different Hosts."""

    def __init__(self):
        self._hosts = {
            "mobile": HostRuntime(HostType.MOBILE, max_authority=TAAL.A2),
            "robot": HostRuntime(HostType.ROBOT, max_authority=TAAL.A4),
            "vehicle": HostRuntime(HostType.VEHICLE, max_authority=TAAL.A3),
        }

    @property
    def host_types(self) -> list[str]:
        return list(self._hosts.keys())

    def get_host(self, name: str) -> HostRuntime:
        return self._hosts[name]

    def process_all(self, user_input: str) -> dict:
        """Process same input on all Hosts and collect results."""
        results = {}
        for name, host in self._hosts.items():
            results[name] = host.process(user_input)
        return results

    def verify_internal_consistency(self, input_text: str) -> bool:
        """Verify all Hosts produce identical internal state."""
        results = self.process_all(input_text)
        states = [r["internal"] for r in results.values()]
        first = states[0]
        return all(
            s["feeling"] == first["feeling"]
            and s["risk"] == first["risk"]
            and s["decision"] == first["decision"]
            for s in states[1:]
        )

    def verify_expression_differs(self, input_text: str) -> bool:
        """Verify expression layer differs across Hosts (capability-adapted)."""
        results = self.process_all(input_text)
        expressions = [r["expression"] for r in results.values()]
        # At least one expression should differ (Host adaptation)
        return len(set(expressions)) > 1
