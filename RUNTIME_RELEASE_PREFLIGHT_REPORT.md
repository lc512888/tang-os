# Runtime Release Preflight Report

## 运行时 Release 预检报告

Version: v0.1
日期：2026-08-01
目的：在提交 ADR-0057~0060 与 `src/runtime` 前，确认运行时资产真实完整。
状态：**仅报告，未修改代码，未提交。**

---

## 1. Git HEAD 与工作区差异

| 项 | 值 |
|----|----|
| 分支 / HEAD | `main` / `4164519`（文档 Release v0.1） |
| 未提交条目 | 49（1 修改 `CHANGELOG.md` + 48 未跟踪） |
| 未跟踪核心源码 | `src/runtime/engine/`、`src/runtime/personality_loader/`、`src/runtime/session/`（9 个 .py） |
| 未跟踪测试 | `tests/runtime/*` + `tests/personality_runtime/`（22 项，含模块 yaml 数据） |
| 未跟踪文档 | ADR-0057~0060、IDENTITY_NAMING_POLICY |
| 未跟踪工具/生成 | `_ocr_*`、`_split_image.ps1`、`ocr_program.cs`、`GITHUB_LAUNCH_*` 等 |

---

## 2. 调用链验证（关键审计项）⚠️

### 生产执行路径（当前实际运行）

```
xiaotang
  → TangBridge（xiaotang/src/services/tang_bridge.py）
    → Tang()（src/tang_os/tang.py）
      → PersonaRuntime（src/runtime/persona/persona_runtime.py）  ← 已提交
        → EmotionalStateManager / RelationshipBoundary / ResponsePolicy
          → ResponseDecision（src/runtime/persona/models.py）
```

`Tang()` **只实例化** `PersonaRuntime / MemoryRuntime / PermissionRuntime`（均已在 git history）。

### 未入库的 ADR-0057 引擎（当前未接线）

```
src/runtime/engine/decision.py      → DecisionResult（另一套 schema，含 triggered_boundaries）
src/runtime/engine/expression.py    → ExpressionContract
src/runtime/personality_loader/     → PersonalityLoader / ModuleValidator
src/runtime/session/                → PersonalityRegistry / RuntimeSession
```

- **互相引用，但无任何生产代码（src/tang_os、src/kernel、xiaotang）引用它们**。
- 仅有 `tests/runtime/*` 与 `tests/personality_runtime/` 引用它们。

### 结论 ⚠️

> **未入库的 Runtime Engine 是"孤立代码"，不是生产执行路径。**

仓库当前存在**两套平行决策实现**，输出 schema 不同：
- 生产（已提交）：`ResponseDecision`（detected_feeling / need / mode / constraints / intent / avoid_patterns）
- ADR-0057（未入库）：`DecisionResult`（response_mode / intent / constraints / triggered_boundaries）

**提交它正确，但它是"存在"，不是"生产路径"。** 若仅提交而不接线，`xiaotang` 实际仍走 persona 路径。

---

## 3. 测试套件结果

| 范围 | 结果 | 说明 |
|------|------|------|
| **磁盘全量**（46 个 test 文件） | **413 passed / 4 skipped**（13.72s） | 含未入库引擎测试 |
| **仅已提交**（37 个 test 文件，HEAD 可复现） | **344 passed / 4 skipped**（7.35s） | HEAD 实际可复现数 |

**差异 = 69 个测试**，全部位于未入库的 `tests/runtime/*` 与 `tests/personality_runtime/`。

> ⚠️ 文档（VALIDATION_EVIDENCE / 定位 / 白皮书）声称"413+ tests"。**该数字在干净 checkout 下不可复现**（HEAD 只给 344）。需在提交后重测并校正口径。

---

## 4. ADR 与代码一致性

| ADR | 标题 | 对应代码 | 是否接线 |
|-----|------|----------|----------|
| ADR-0057 | Personality Runtime Engine Architecture | `src/runtime/engine/` + `personality_loader/` + `session/` | ❌ 未接线 |
| ADR-0058 | Personality Runtime Validation Framework | `tests/runtime/personality_validation/` + `tests/runtime/validation/` | ❌ 测的是未接线引擎 |
| ADR-0059 | Personality Capability Integrity Validation | `tests/runtime/personality_validation/` 相关用例 | ❌ 同上 |
| ADR-0060 | Blind Validation Principle | 测试中盲验用例 | ❌ 同上 |

**结论：ADR 设计与其实现代码互相一致，但都未进入生产路径。** 生产路径（persona/response_policy）没有对应的 ADR-0057~0060 映射——它是另一套已提交的决策实现。

---

## 5. 测试覆盖

- 未入库引擎的测试**自成一体**（engine 测试其 engine、loader 测试其 loader），覆盖了 ADR-0057~0060 描述的验证五维（身份稳定 / 人格隔离 / 模型独立 / 抗漂移 / 决策可区分）。
- 生产 persona 路径的测试来自已提交的 `tests/persona_validation/` 等（HEAD 可复现 344 个）。
- **两套引擎各测各的，没有交叉验证生产路径与 ADR-0057 引擎的一致性或互操作性。**

---

## 6. 预检结论与 Release 风险

| # | 风险 | 级别 |
|---|------|------|
| R1 | 文档声称 413 测试，HEAD 仅复现 344 —— 数字失真 | 🔴 高 |
| R2 | ADR-0057 引擎是孤立代码，非生产路径；提交后仍存在"两套引擎并存" | 🔴 高（需决策：接线 or 标记为实验层） |
| R3 | 工具/生成脚本（_ocr_*、ocr_program.cs）混入工作区，有误提交污染风险 | 🟡 中 |
| R4 | CHANGELOG 未同步 v0.1 | 🟢 低 |

## 7. 建议（供决策，未执行）

1. **提交前先决策"两套引擎"关系**：ADR-0057 引擎是(a) 替代生产 persona 路径的下一代，还是(b) 并行实验层？
   - (a) → 提交后进入接线工作（Tang() 切换到 engine），作为 v0.2 核心；
   - (b) → 提交时在 ADR/代码中明确标注"实验层 / 未接线"，避免被误读为生产。
2. **提交分组建议**：A(engine+loader+session+ADR-0057+tests) → B(ADR-0058~0060+validation tests) → E(CHANGELOG/状态) → C(IDENTITY_NAMING_POLICY)。D(工具/生成) 走 `.gitignore`。
3. **提交后重测**：更新"413 tests"口径为提交后真实计数，同步 CHANGELOG。
4. **接线前不加新功能**：引擎未进生产路径前，验证体系的价值无法在真实产品中体现。

---

*本报告仅审计，未修改任何代码，未提交任何变更。*
