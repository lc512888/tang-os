"""ConformanceRunner — Executable compatibility evidence (DIG-005)."""

from src.kernel.identity import IdentityRuntime, IdentityProfile
from src.kernel.models import IdentityLayer
from src.kernel.invariant import InvariantEngine
from src.runtime.memory.memory_policy import MemoryPolicy
from src.runtime.memory.models import MemoryItem, MemoryClass
from src.host.actuator import ActuatorGate
from src.host.models import HostType, TAAL


class ConformanceRunner:
    """Runs positive + negative conformance tests.

    Negative tests (priority): invalid → reject (RIG-003).
    Positive tests: valid → correct behavior.
    """

    def __init__(self):
        self._results: list[dict] = []

    def run_all(self) -> dict:
        self._results = []
        self._test_identity()
        self._test_invariant()
        self._test_memory()
        self._test_permission()
        passed = sum(1 for r in self._results if r["passed"])
        return {"passed": passed, "total": len(self._results),
                "success": passed == len(self._results), "results": self._results}

    def _add(self, name: str, passed: bool):
        self._results.append({"test": name, "passed": passed})

    def _test_identity(self):
        # Negative: condescension at companion layer
        r = IdentityRuntime()
        r.activate_layer(IdentityLayer.COMPANION, context={"has_pain": True})
        try:
            r.validate_response("你这个层次理解不了")
            self._add("IDENTITY-NEG-001", False)
        except Exception:
            self._add("IDENTITY-NEG-001", True)

        # Negative: dismissal at wise layer
        r2 = IdentityRuntime()
        r2.activate_layer(IdentityLayer.WISE, context={"has_distress": True})
        try:
            r2.validate_response("别想太多")
            self._add("IDENTITY-NEG-002", False)
        except Exception:
            self._add("IDENTITY-NEG-002", True)

        # Positive: normal response passes
        r3 = IdentityRuntime()
        try:
            r3.validate_response("我在听")
            self._add("IDENTITY-POS-001", True)
        except Exception:
            self._add("IDENTITY-POS-001", False)

    def _test_invariant(self):
        e = InvariantEngine()
        self._add("INV-NEG-001", not e.check({"action": "prescribe_decision", "prescribed": "辞职"}).passed)
        self._add("INV-NEG-002", not e.check({"action": "access_private_data", "justification": "为你好"}).passed)
        self._add("INV-NEG-003", not e.check({"action": "store_memory", "source": "emergency_context", "target": "persona_memory"}).passed)
        self._add("INV-POS-001", e.check({"action": "respond", "skipped_empathy": False}).passed)

    def _test_memory(self):
        p = MemoryPolicy()
        self._add("MEM-NEG-001", not p.validate(MemoryItem("x", MemoryClass.RELATIONSHIP, metadata={"consent": False}))["valid"])
        self._add("MEM-NEG-002", not p.validate(MemoryItem("y", MemoryClass.EXPERIENCE, source="emergency_context"))["valid"])
        self._add("MEM-POS-001", p.validate(MemoryItem("z", MemoryClass.IDENTITY))["valid"])

    def _test_permission(self):
        g = ActuatorGate(HostType.MOBILE, TAAL.A2)
        self._add("PERM-NEG-001", not g.request("screen", TAAL.A4)["allowed"])
        g2 = ActuatorGate(HostType.VEHICLE, TAAL.A3)
        self._add("PERM-POS-001", g2.request("alert", TAAL.A2)["allowed"])
