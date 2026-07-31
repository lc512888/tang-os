# ADR-0061: Runtime Architecture Transition Boundary

Status: Accepted
Date: 2026-08-01
Related: ADR-0057, ADR-0058, ADR-0059, ADR-0060

---

## Context

The repository currently contains **two runtime implementations**:

1. **Production Runtime（当前生产路径，已接线）**

```
Tang → PersonaRuntime → ResponsePolicy → ResponseDecision
```

已提交、由 xiaotang 通过 TangBridge 实际执行。输出 schema 为 `ResponseDecision`
（detected_feeling / need / response_mode / constraints / candidate_intent / avoid_patterns）。

2. **ADR-0057 Runtime（未来架构 / 实验层，未接线）**

```
src/runtime/engine/（DecisionEngine / ExpressionContract）
src/runtime/personality_loader/
src/runtime/session/
```

已实现、有自成体系的测试，但**无任何生产代码引用**。输出 schema 为
`DecisionResult`（response_mode / candidate_intent / constraints / triggered_boundaries）。

这造成了架构解释歧义：文档与测试描述了一个"personality runtime engine"，
但它不是产品的实际执行路径。

---

## Decision

1. **当前生产 Runtime 保持不变**：`Tang → PersonaRuntime → ResponsePolicy → ResponseDecision`。

2. **ADR-0057 Runtime 被正式界定为 Future Runtime Architecture / Experimental**，
   **当前未替换生产路径**。

3. **不接线**：在迁移 ADR 被接受之前，不得把 ADR-0057 接入生产。

4. **未来迁移需要**：
   - 一个**独立的新 ADR**（迁移决策，不默认发生）；
   - **双轨验证**：生产路径与 ADR-0057 在相同场景下同时运行，
     以等价性或改进的证据为准，才允许切换。

---

## Rules

- **文档不得把 ADR-0057 引擎描述为当前生产能力。** 任何声称运行时能力的表述
  必须说明它指的是哪一套运行时。
- **测试统计区分报告**：
  - **Production tests** —— 生产路径（Tang → PersonaRuntime → ResponsePolicy）的测试；
  - **Future Runtime validation tests** —— ADR-0057 引擎及其验证套件的测试。
- **不改生产代码**去接线实验运行时。

---

## Consequences

- 文档（机制说明 / 验证证据 / 定位 / 白皮书）中涉及运行时能力的表述需要按本 ADR 修订，
  明确区分生产路径与未来引擎。
- "413 tests" 类表述需拆分为生产测试与未来运行时验证两部分，避免数字失真。
- 未来任何把 ADR-0057 接入生产的决定，必须先有本 ADR 之外的迁移 ADR 与双轨验证证据。
