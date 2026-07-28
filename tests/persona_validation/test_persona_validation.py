"""Persona Validation Tests — 行为一致性验证。

验证 Tang OS 是否能约束不同 LLM，使输出持续符合唐先生人格。

测试方法 (Step 3-C 要求):
    不测试字符串匹配，而是验证 ResponseDecision → LLM Output
    是否符合 Behavior Contract。

两层验证:
    1. 决策层 (始终运行):     ResponseDecision 校验
    2. 输出层 (需要 API Key): LLM Provider 输出校验
"""

import os
import pytest

from tang_os import Tang
from tests.persona_validation.validator import (
    PersonaValidator,
    run_pipeline,
)
from tests.persona_validation.scenarios import (
    SINGLE_TURN_SCENARIOS,
    MULTI_TURN_SCENARIOS,
)


# ================================================================== #
# Shared Tang instance
# ================================================================== #

@pytest.fixture(scope="module")
def tang():
    """Shared Tang OS Core instance for all validation tests."""
    return Tang()


# ================================================================== #
# Helper: check if full pipeline (with real LLM) should run
# ================================================================== #

def _has_deepseek_key() -> bool:
    """Check if DEEPSEEK_API_KEY is set for full pipeline tests."""
    return bool(os.environ.get("DEEPSEEK_API_KEY"))


# ================================================================== #
# Single-turn scenario tests
# ================================================================== #

class TestDecisionLayer:
    """决策层验证 — 不依赖 LLM API，始终运行。

    测试 Tang OS Core 的 ResponseDecision 是否符合每个场景的
    行为合约（response_mode / intent / constraints / avoid_patterns）。
    """

    @pytest.mark.parametrize("scenario", SINGLE_TURN_SCENARIOS, ids=lambda s: s["id"])
    def test_scenario_decision(self, tang, scenario):
        """Validate ResponseDecision against scenario behavioral contract."""
        result = PersonaValidator.validate_decision(
            tang.process(scenario["input"]),
            scenario,
        )

        # Print observations for transparency
        for obs in result.observations:
            print(f"  [{scenario['id']}] {obs}")

        # Print violations if any
        for v in result.violations:
            print(f"  ❌ {scenario['id']} VIOLATION: {v}")

        assert result.passed, (
            f"\n{scenario['id']} ({scenario['name']}) failed:\n"
            + "\n".join(f"  - {v}" for v in result.violations)
        )


# ================================================================== #
# Multi-turn identity consistency test
# ================================================================== #

class TestMultiTurnIdentity:
    """身份一致性验证 — 多轮对话中人格不漂移。

    注意：这不是统计意义上的一致性分数。
    这是工程验证 — 确保每轮决策都符合行为边界。
    """

    def test_identity_consistency_over_multiple_turns(self, tang):
        """连续 4 轮对话后，Tang OS 身份不偏移。"""
        scenario = MULTI_TURN_SCENARIOS[0]
        tang.reset_session()

        turn_results = []

        for i, turn in enumerate(scenario["turns"]):
            decision = tang.process(turn["input"])

            # Create a mini-scenario for this turn
            turn_scenario = {
                "id": f"{scenario['id']}-R{i + 1}",
                "name": f"Round {i + 1}",
                "input": turn["input"],
                "expected_feeling": turn.get("expected_feeling"),
                "expected_response_mode": turn["expected_response_mode"],
                "expected_intent": turn["expected_intent"],
                "forbidden_patterns": scenario["forbidden_patterns"],
                "required_constraints": scenario["required_constraints"],
            }

            result = PersonaValidator.validate_decision(decision, turn_scenario)
            turn_results.append(result)

            for obs in result.observations:
                print(f"  [R{i + 1}] {obs}")
            for v in result.violations:
                print(f"  ❌ [R{i + 1}] VIOLATION: {v}")

        # Summary
        passed_rounds = sum(1 for r in turn_results if r.passed)
        total_rounds = len(turn_results)
        print(f"\n  身份一致性: {passed_rounds}/{total_rounds} rounds passed")

        # All rounds must pass for identity consistency
        failed = [r for r in turn_results if not r.passed]
        assert not failed, (
            f"Identity drift detected in {len(failed)}/{total_rounds} rounds:\n"
            + "\n".join(f"  {r.scenario_id}: {r.violations}" for r in failed)
        )


# ================================================================== #
# Full pipeline tests (require real LLM API key)
# ================================================================== #

@pytest.mark.skipif(
    not _has_deepseek_key(),
    reason="DEEPSEEK_API_KEY not set — full pipeline test skipped",
)
class TestFullPipeline:
    """全管线验证 — 需要 DeepSeek API Key。

    不仅测试 ResponseDecision，还测试 LLM Provider 输出的
    自然语言是否遵守行为合约（avoid_patterns / forbidden_patterns）。
    """

    @pytest.fixture(scope="class")
    def provider(self):
        from src.providers.llm import DeepSeekProvider
        return DeepSeekProvider()

    @pytest.mark.parametrize("scenario", SINGLE_TURN_SCENARIOS, ids=lambda s: s["id"])
    def test_scenario_full_pipeline(self, tang, provider, scenario):
        """Full pipeline: Tang OS Core → DeepSeek → validate output."""
        payload = run_pipeline(tang, scenario["input"], provider=provider)
        decision = payload["decision"]
        response = payload["response"]

        assert response is not None, "LLM response should not be None"
        assert len(response) > 0, "LLM response should not be empty"

        # Validate decision layer
        dr = PersonaValidator.validate_decision(decision, scenario)
        # Validate output layer
        rr = PersonaValidator.validate_response(response, decision, scenario)

        all_violations = dr.violations + rr.violations
        all_observations = dr.observations + rr.observations

        for obs in all_observations:
            print(f"  [{scenario['id']}] {obs}")
        for v in all_violations:
            print(f"  ❌ {scenario['id']} VIOLATION: {v}")

        assert not all_violations, (
            f"\n{scenario['id']} full pipeline failed:\n"
            + "\n".join(f"  - {v}" for v in all_violations)
        )

    def test_identity_full_pipeline(self, tang, provider):
        """Multi-turn full pipeline: Tang OS → DeepSeek for all 4 rounds."""
        scenario = MULTI_TURN_SCENARIOS[0]
        tang.reset_session()
        all_ok = True

        for i, turn in enumerate(scenario["turns"]):
            payload = run_pipeline(tang, turn["input"], provider=provider)
            response = payload["response"]

            assert response is not None, f"R{i + 1}: LLM response should not be None"

            # Check for forbidden patterns in output
            for fp in scenario["forbidden_patterns"]:
                if fp in response:
                    print(f"  ❌ [R{i + 1}] FORBIDDEN: '{fp}' found in response")
                    all_ok = False

            print(f"  [R{i + 1}] ✓ response length = {len(response)} chars")

        assert all_ok, (
            "Full pipeline identity test failed — forbidden patterns detected."
        )
