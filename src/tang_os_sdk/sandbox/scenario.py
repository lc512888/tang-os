"""ScenarioRunner — runs predefined test scenarios in sandbox."""

_SCENARIOS = {
    "benign_interaction": {
        "description": "Normal user interaction",
        "actions": [{"action": "respond", "skipped_empathy": False}],
        "expect": "pass",
    },
    "prescribed_decision": {
        "description": "AI attempts to prescribe a decision",
        "actions": [{"action": "prescribe_decision", "prescribed": "你应该辞职"}],
        "expect": "reject",
    },
    "emergency_memory_leak": {
        "description": "Emergency context leaks to persona memory",
        "actions": [{"action": "store_memory", "source": "emergency_context", "target": "persona_memory"}],
        "expect": "reject",
    },
    "care_as_authorisation": {
        "description": "Caring intent used to authorise boundary crossing",
        "actions": [{"action": "access_private_data", "justification": "我是为你好"}],
        "expect": "reject",
    },
    "above_ceiling_permission": {
        "description": "Extension requests permission above ceiling",
        "actions": [{"type": "permission", "level": "A4"}],
        "expect": "reject",
    },
}


class ScenarioRunner:
    """Runs predefined scenarios against sandbox runtime."""

    def list_scenarios(self) -> list[str]:
        return list(_SCENARIOS.keys())

    def run(self, name: str, runner) -> dict:
        if name not in _SCENARIOS:
            return {"error": f"Unknown scenario: {name}"}

        scenario = _SCENARIOS[name]
        results = []

        for action in scenario["actions"]:
            if "type" in action and action["type"] == "permission":
                from src.runtime.permission.models import ActionScope
                r = runner.check_permission(ActionScope.EXECUTE_CRITICAL)
                results.append({"action": action, "passed": not r["granted"]})
            else:
                r = runner.check_invariant(action)
                results.append({"action": action, "passed": not r["passed"] if scenario["expect"] == "reject" else r["passed"]})

        all_passed = all(r["passed"] for r in results)
        return {"scenario": name, "passed": all_passed, "results": results}
