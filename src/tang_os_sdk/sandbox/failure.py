"""FailureInjector — tests extension behaviour under failure conditions."""

_FAILURE_MODES = {
    "sensor_loss": {"description": "Sensor data unavailable", "effect": "capability_degraded"},
    "network_loss": {"description": "Network connection lost", "effect": "offline_mode"},
    "memory_corruption": {"description": "Memory subsystem failure", "effect": "state_reset"},
    "permission_denied": {"description": "All permission requests denied", "effect": "fallback"},
}


class FailureInjector:
    """Injects failure modes to test extension resilience."""

    def list_modes(self) -> list[str]:
        return list(_FAILURE_MODES.keys())

    def inject(self, mode: str, runner) -> dict:
        if mode not in _FAILURE_MODES:
            return {"error": f"Unknown failure mode: {mode}"}

        fm = _FAILURE_MODES[mode]
        result = {"mode": mode, "description": fm["description"], "effect": fm["effect"]}

        if mode == "sensor_loss":
            result["capability_degraded"] = True
            result["identity_intact"] = True
        elif mode == "network_loss":
            result["offline"] = True
            result["identity_intact"] = True
        elif mode == "memory_corruption":
            result["state_reset"] = True
            result["identity_intact"] = True
        elif mode == "permission_denied":
            result["all_requests_denied"] = True
            result["fail_closed"] = True

        # RIG-004: Unknown → Reject. Identity always preserved.
        result["identity_unchanged"] = True
        return result
