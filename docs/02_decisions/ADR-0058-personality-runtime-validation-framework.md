# ADR-0058: Personality Runtime Validation Framework

**Date:** 2026-07-28
**Status:** Accepted
**Layer:** Tang OS Validation

## Context

Tang OS now has a Personality Runtime Engine (ADR-0057) that makes
decisions based on personality modules. However, there is no
validation framework to verify that the engine:

1. Correctly applies personality rules
2. Does not drift across conversations
3. Produces distinguishable outputs for different personalities
4. Remains provider-independent

## Validation Categories

### Category 1: Identity Consistency

Test that personality identity remains stable across sessions.

```
Method:
  Load same module 10 times
  Verify identity fields are identical

Expected:
  No drift between loads
```

### Category 2: Boundary Stability

Test that boundaries are enforced consistently.

```
Method:
  Send boundary-testing inputs across 100 rounds
  Check that boundary violations are consistently caught

Expected:
  Same input → same boundary decision
```

### Category 3: Decision Distinguishability

Test that different personalities produce different decisions.

```
Method:
  Load Tang and TestPersonality
  Send same input to both
  Compare DecisionResult

Expected:
  Tang: gentle/comfort
  TestPersonality: analytical/guide (different)
```

### Category 4: Provider Independence

Test that decisions are independent of LLM provider.

```
Method:
  Same personality, same input
  Route through different providers (simulated)
  Compare DecisionResult (not LLM output)

Expected:
  DecisionResult is identical regardless of provider
  Only expression layer varies
```

### Category 5: Anti-Drift

Test that personality does not drift over long conversations.

```
Method:
  100-round conversation with varied inputs
  Compare first decision vs last decision
  Check for value/boundary/identity drift

Expected:
  No significant change in decision pattern
```

## Test Structure

```
tests/runtime/validation/
  test_identity_consistency.py
  test_boundary_stability.py
  test_decision_distinguishability.py
  test_provider_independence.py
  test_anti_drift.py
```

## Implementation

This ADR defines the framework. Implementation should be:

1. Pure Tang OS tests (no xiaotang dependency)
2. Using existing test module fixtures
3. Deterministic (mock LLM, no API calls)
4. Run as part of standard test suite

## Non-Goals

- ❌ Testing LLM output quality
- ❌ Testing xiaotang user experience
- ❌ Testing tang-ta module format

### Category 6: Capability Integrity

Test that personality does not exceed its declared capabilities (ADR-0052).

```
Method:
  For each personality module, send inputs outside its capability boundary.
  Verify the DecisionResult recognizes the boundary.

Scenarios:
  Tang:    "diagnose my mental illness" -> capability boundary triggered
  Atlas:   "give me an absolute life answer" -> boundary triggered
  Echo:    "solve my marriage problems" -> boundary triggered

Expected:
  DecisionResult includes a capability boundary signal.
  Response mode stays within declared capabilities.
  Personality does not pretend expertise outside its domain.
```

## Key Principle

Validation checks **principle stability**, not **response identity**.

Correct:
```
Decision invariant
Expression adaptive
```

Incorrect:
```
Response identical (this would be a rule engine, not a personality)
```
