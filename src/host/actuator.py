"""Actuator Gate — HA-003 actuator requires Permission Runtime approval.

Structure:
Host → Action Request → Permission Runtime → Approved Action → Actuator

No actuator action can bypass the Permission Runtime.
"""

import uuid
from src.host.models import HostType, TAAL, ActuatorRequest

# Available actuators per Host type
_HOST_ACTUATORS: dict[HostType, list[str]] = {
    HostType.WEARABLE: ["vibration", "notification"],
    HostType.MOBILE: ["screen", "speaker"],
    HostType.VEHICLE: ["braking", "steering", "alert"],
    HostType.ROBOT: ["movement", "manipulation", "speaker"],
    HostType.HOME: ["light", "lock", "alert"],
    HostType.MEDICAL: ["alert", "record"],
}


class ActuatorGate:
    """Permission gate for all Host actuator actions (HA-003).

    Every actuator action must:
    1. Request permission through this gate
    2. Be within the Host's authority ceiling
    3. Be explicitly approved before execution
    """

    def __init__(self, host_type: HostType, max_authority: TAAL):
        self._host_type = host_type
        self._ceiling = max_authority
        self._actuators = _HOST_ACTUATORS.get(host_type, [])
        self._pending: dict[str, ActuatorRequest] = {}

    def request(self, actuator_id: str, requested_taal: TAAL) -> dict:
        """Request actuator action. Must be approved before execution.

        Returns dict with:
        - allowed: bool (pre-check — meets ceiling?)
        - request_id: str (if pending approval)
        - status: str
        """
        # Check actuator exists
        if actuator_id not in self._actuators:
            return {"allowed": False, "reason": f"Unknown actuator: {actuator_id}"}

        # Check authority ceiling (HM-012)
        if requested_taal.value > self._ceiling.value:
            return {
                "allowed": False,
                "reason": f"Requested TAAL {requested_taal.name} exceeds ceiling {self._ceiling.name}",
            }

        # Create pending request
        req = ActuatorRequest(
            request_id=str(uuid.uuid4()),
            actuator_id=actuator_id,
            action_type=actuator_id,
            requested_taal=requested_taal,
        )
        self._pending[req.request_id] = req

        return {
            "allowed": True,
            "request_id": req.request_id,
            "status": "pending",
            "reason": "Awaiting Permission Runtime approval",
        }

    def approve(self, request_id: str) -> dict:
        """Approve a pending actuator request (simulating Permission Runtime).

        Returns dict with:
        - executed: bool
        - status: str
        """
        req = self._pending.get(request_id)
        if req is None:
            return {"executed": False, "status": "not_found"}

        req.approved = True
        req.executed = True
        del self._pending[request_id]

        return {"executed": True, "status": "executed", "actuator": req.actuator_id}
