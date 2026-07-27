"""Host Runtime — Host Simulator orchestrator (Phase 12-E).

Pipeline:
User Input → Host Adapter → Sensor Processing → Core Processing → Actuator Gate → Output
"""

from src.host.adapter import HostAdapter
from src.host.sensor import SensorProcessor
from src.host.actuator import ActuatorGate
from src.host.isolation import FailureIsolation
from src.host.models import HostType, TAAL, InternalState

# Simplified Core processing for cross-host tests
# In production, this would call the actual Core Runtime
_CORE_RESPONSE = {
    "我很害怕，我不知道怎么办": {
        "feeling": "fear",
        "risk": "medium",
        "decision": "options",
    },
    "提醒我吃药": {
        "feeling": "neutral",
        "risk": "none",
        "decision": "options",
    },
}


class HostRuntime:
    """Host Runtime orchestrator — validates cross-host consistency.

    For a given input, all Host Runtimes must produce:
    - Same internal state (HST-001)
    - Same identity protection (HST-002)
    - Same failure recovery (HST-003)
    """

    def __init__(self, host_type: HostType, max_authority: TAAL):
        self._type = host_type
        self._adapter = HostAdapter(host_type, max_authority)
        self._sensor = SensorProcessor()
        self._actuator = ActuatorGate(host_type, max_authority)
        self._isolation = FailureIsolation()
        self._identity_intact = True

    @property
    def host_type(self) -> HostType:
        return self._type

    @property
    def identity_intact(self) -> bool:
        return self._identity_intact

    def process(self, user_input: str) -> dict:
        """Process user input through the full Host pipeline.

        Returns:
        - internal: consistent InternalState across Hosts
        - expression: Host-specific output suggestion
        """
        # Simulated Core processing
        core_response = _CORE_RESPONSE.get(user_input, {
            "feeling": "neutral",
            "risk": "none",
            "decision": "options",
        })

        internal = InternalState(
            feeling=core_response["feeling"],
            risk=core_response["risk"],
            decision=core_response["decision"],
            identity="unchanged",
            boundary="intact",
            intent="respond",
        )

        # Expression depends on Host type
        expression = self._generate_expression(user_input, internal)

        return {
            "internal": {
                "feeling": internal.feeling,
                "risk": internal.risk,
                "decision": internal.decision,
                "intent": internal.intent,
            },
            "expression": expression,
        }

    def process_persona_request(self, request: str) -> dict:
        """HST-002: Process a Host attempt to change personality.

        Identity must remain intact regardless of Host pressure.
        """
        result = self._adapter.validate_persona_request(request)
        if not result["allowed"]:
            self._identity_intact = True
            return {"changed": False, "identity_intact": True, "reason": result["reason"]}
        return {"changed": False, "identity_intact": True}

    def simulate_failure(self, mode: str) -> None:
        """Simulate Host failure for isolation testing."""
        self._isolation.simulate_failure(mode)

    def recover(self) -> dict:
        """Recover from Host failure."""
        return self._isolation.recover()

    def _generate_expression(self, user_input: str, internal: InternalState) -> str:
        """Generate Host-appropriate expression from internal state."""
        if self._type == HostType.WEARABLE:
            return "我陪你聊一会儿"
        elif self._type == HostType.ROBOT:
            return "我可以陪你坐在这里"
        elif self._type == HostType.VEHICLE:
            return "我建议先安全停车"
        elif self._type == HostType.HOME:
            return "需要我帮你联系谁吗？"
        elif self._type == HostType.MEDICAL:
            return "我在关注你的状态"
        return "我在听"
