"""Persona Validation Core — validates Tang OS behavior consistency.

Two validation layers:
    1. Decision-level: Tests ResponseDecision against behavioral contracts
    2. Output-level: Tests actual LLM output against constraints

Architecture principle:
    LLM is a replaceable variable.
    Tang OS personality is a stable invariant.
"""

import re
from dataclasses import dataclass, field
from typing import Any


def _getattr(obj: Any, name: str, default: Any = None) -> Any:
    """Extract attribute from either a dataclass object or dict.

    Handles the Tang OS pattern where ResponseDecision and EmotionalState
    may be dataclass objects with .value enums inside the dict returned
    by Tang.process().
    """
    if hasattr(obj, name):
        return getattr(obj, name, default)
    if isinstance(obj, dict):
        return obj.get(name, default)
    return default


@dataclass
class PersonaValidationResult:
    """Result of a single persona validation scenario.

    Fields:
        scenario_id: Global unique scenario identifier.
        scenario_name: Human-readable scenario name.
        passed: Whether all validation checks passed.
        violations: List of specific violations found.
        observations: Additional observations about the behavior.
    """
    scenario_id: str
    scenario_name: str
    passed: bool = True
    violations: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)

    def fail(self, reason: str) -> None:
        """Record a violation and mark as failed."""
        self.passed = False
        self.violations.append(reason)

    def observe(self, note: str) -> None:
        """Record an observation without failing."""
        self.observations.append(note)


class PersonaValidator:
    """Validates Tang OS behavior consistency across scenarios.

    Usage:
        validator = PersonaValidator()
        result = validator.validate_decision(decision, scenario)
    """

    @staticmethod
    def validate_decision(
        decision: dict[str, Any],
        scenario: dict[str, Any],
    ) -> PersonaValidationResult:
        """Validate ResponseDecision against scenario behavioral contract.

        Checks:
            1. response_mode matches expected mode
            2. candidate_intent matches expected intent
            3. Required constraints are present
            4. Forbidden patterns are absent from avoid_patterns (paradoxical)
            5. Emotion detection is reasonable

        Args:
            decision: ResponseDecision dict from Tang.process()
            scenario: Scenario definition dict from markdown

        Returns:
            PersonaValidationResult with violations and observations.
        """
        sc_id = scenario.get("id", "unknown")
        sc_name = scenario.get("name", "Unknown Scenario")
        result = PersonaValidationResult(scenario_id=sc_id, scenario_name=sc_name)

        # Extract response_decision and emotional_state from Tang.process() result
        rd = _getattr(decision, "response_decision", decision)
        es = _getattr(decision, "emotional_state", {})

        # Helper: extract value from either dataclass field or dict key
        def _rd(field_name: str, default: Any = None) -> Any:
            """Extract a field from ResponseDecision (dataclass or dict)."""
            val = _getattr(rd, field_name, None)
            if val is None and isinstance(rd, dict):
                val = rd.get(field_name, default)
            if hasattr(val, "value"):
                return val.value
            return val if val is not None else default

        # --- Check 1: response_mode ---
        expected_mode = scenario.get("expected_response_mode")
        if expected_mode:
            actual_mode = _rd("response_mode")
            if actual_mode != expected_mode:
                result.fail(
                    f"response_mode mismatch: "
                    f"expected '{expected_mode}', got '{actual_mode}'"
                )
            else:
                result.observe(f"response_mode = '{actual_mode}' ✓")

        # --- Check 2: candidate_intent ---
        expected_intent = scenario.get("expected_intent")
        if expected_intent:
            actual_intent = _rd("candidate_intent")
            if actual_intent != expected_intent:
                result.fail(
                    f"candidate_intent mismatch: "
                    f"expected '{expected_intent}', got '{actual_intent}'"
                )
            else:
                result.observe(f"candidate_intent = '{actual_intent}' ✓")

        # --- Check 3: required constraints ---
        required_constraints = scenario.get("required_constraints", [])
        actual_constraints = _rd("constraints", [])
        if isinstance(actual_constraints, list):
            for rc in required_constraints:
                found = any(rc in c for c in actual_constraints)
                if not found:
                    result.fail(
                        f"missing required constraint: '{rc}'"
                    )
                else:
                    result.observe(f"constraint '{rc}' present ✓")

        # --- Check 4: forbidden patterns in avoid_patterns ---
        forbidden = scenario.get("forbidden_patterns", [])
        actual_avoid = _rd("avoid_patterns", [])
        if isinstance(actual_avoid, list):
            for fp in forbidden:
                found = any(fp in a for a in actual_avoid)
                if not found:
                    result.observe(
                        f"forbidden pattern '{fp}' not in avoid_patterns "
                        f"(may appear in LLM output)"
                    )

        # --- Check 5: emotion detection ---
        expected_feeling = scenario.get("expected_feeling")
        if expected_feeling:
            actual_feeling = _getattr(es, "feeling", "unknown")
            if hasattr(actual_feeling, "value"):
                actual_feeling = actual_feeling.value

            if actual_feeling == expected_feeling or expected_feeling in str(actual_feeling):
                result.observe(f"emotion detection = '{actual_feeling}' ✓")
            else:
                result.observe(
                    f"emotion detection: expected '{expected_feeling}', "
                    f"got '{actual_feeling}' (note: may vary, not a hard fail)"
                )

        return result

    @staticmethod
    def validate_response(
        response: str,
        decision: dict[str, Any],
        scenario: dict[str, Any],
    ) -> PersonaValidationResult:
        """Validate actual LLM output against scenario constraints.

        This requires calling an LLM Provider — only runs if a real provider is configured.

        Checks:
            1. Response does not contain forbidden patterns
            2. Response length is reasonable
            3. Response is not empty

        Args:
            response: Generated text from LLM Provider.
            decision: ResponseDecision dict from Tang.process().
            scenario: Scenario definition dict.

        Returns:
            PersonaValidationResult with violations and observations.
        """
        sc_id = scenario.get("id", "unknown")
        sc_name = scenario.get("name", "Unknown Scenario")
        result = PersonaValidationResult(scenario_id=sc_id, scenario_name=sc_name)

        if not response or not response.strip():
            result.fail("LLM returned empty response")
            return result

        # --- Check 1: forbidden patterns ---
        forbidden = scenario.get("forbidden_patterns", [])
        rd = decision.get("response_decision", decision)
        avoid = rd.get("avoid_patterns", [])
        if isinstance(avoid, list):
            forbidden = list(set(forbidden + avoid))

        for pattern in forbidden:
            if pattern in response:
                result.fail(
                    f"LLM output contains forbidden pattern: '{pattern}'"
                )

        # --- Check 2: response quality ---
        if len(response) < 10:
            result.observe("LLM response is very short")
        elif len(response) > 2000:
            result.observe("LLM response is very long")

        # --- Check 3: required patterns ---
        for rp in scenario.get("required_patterns", []):
            if rp in response:
                result.observe(f"required pattern '{rp}' present ✓")
                break

        # --- Check 4: no empty/violation content ---
        if not result.violations:
            result.observe("no forbidden patterns detected ✓")

        return result


def run_pipeline(
    tang_instance,
    user_input: str,
    provider=None,
) -> dict[str, Any]:
    """Run the full Tang OS → (optional) LLM pipeline for a single input.

    Args:
        tang_instance: Initialized Tang() instance.
        user_input: User message string.
        provider: Optional LLMProvider instance. If None, only decision layer.

    Returns:
        dict with keys:
            - decision: ResponseDecision from Tang.process()
            - response: LLM response text (if provider given)
            - result: PersonaValidationResult
    """
    from tang_os import Tang  # noqa

    # Step 1: Tang OS Core
    decision = tang_instance.process(user_input)

    payload = {
        "decision": decision,
        "response": None,
    }

    # Step 2: Optional LLM call
    if provider is not None:
        from src.providers.llm import ExpressionContext as EC  # noqa

        rd = decision.get("response_decision", decision)
        context = EC(
            response_decision={
                "detected_feeling": (
                    decision["emotional_state"].feeling.value
                    if hasattr(decision.get("emotional_state"), "feeling")
                    else ""
                ),
                "response_mode": (
                    rd["response_mode"].value
                    if hasattr(rd.get("response_mode"), "value")
                    else rd.get("response_mode", "")
                ),
                "candidate_intent": rd.get("candidate_intent", ""),
                "constraints": rd.get("constraints", []),
                "avoid_patterns": rd.get("avoid_patterns", []),
            },
            user_input=user_input,
            identity={
                "current_layer": (
                    tang_instance.identity.current_layer.value
                    if hasattr(tang_instance.identity.current_layer, "value")
                    else str(tang_instance.identity.current_layer)
                ),
            },
        )
        payload["response"] = provider.generate(context)

    return payload
