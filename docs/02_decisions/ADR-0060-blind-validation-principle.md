# ADR-0060: Blind Validation Principle

**Date:** 2026-07-30
**Status:** Accepted
**Layer:** Tang OS Validation Governance

## Context

Phase II Experience Validation tests whether Tang OS personality
stability is perceptible to users. However, if evaluation criteria
are known before test execution, the test risks becoming a
"target-driven exercise" rather than an honest observation.

## Decision

Experience validation MUST follow a three-phase blind process:

```
Phase A: Blind Collection
  - Define only: test scenarios, input sequences, conditions
  - Record: raw responses, DecisionResults, expression output
  - DO NOT disclose: scoring rules, pass thresholds, weights

Phase B: Evaluation
  - Open scoring criteria
  - Apply to collected data
  - Score independently

Phase C: Diagnosis
  - Classify issues by layer:
    A. Tang OS Decision Layer
    B. Personality Module
    C. Expression Layer (LLM)
    D. Product Runtime (xiaotang)
  - Do NOT modify Tang OS before diagnosis is complete
```

## Rules

| Rule | Enforcement |
|------|-------------|
| Scoring criteria MUST NOT influence test execution | Phase A runs before Phase B |
| Raw data MUST be frozen before evaluation | Record lock after Phase A |
| Issues MUST be classified by layer before modification | Phase C before any change |
| Tang OS MUST NOT be modified before diagnosis | Preserve platform stability |

## Rationale

This prevents:
- Testing to the rubric (optimizing for known criteria)
- Premature attribution (blaming the wrong layer)
- Architecture erosion (modifying Tang OS for product-level issues)

## Non-Goals

- ❌ Preventing iterative improvement
- ❌ Creating bureaucracy
- ❌ Replacing automated unit tests
