# ADR-0040: Tang OS Public Release Boundary

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer（Public Ecosystem Boundary）
**影响范围：** 所有对外发布行为、开源仓库、文档、社区、品牌使用
**前序资产：** ADR-0034~0039, AR-GATE

---

## 背景

Tang OS 已完成从人格设计（Phase 1-8）到运行时实现（Phase 12）的完整链路。当前具备：
- 37 条 ADR 构成的治理体系
- 154 测试覆盖的 Runtime v0.1
- Civilization Boundary → Host Adaptation 的 10 层架构

但是：**内部完整 ≠ 外部安全。**

对外公开后，系统将面临三类此前不存在的外部风险：

| 风险类别 | 具体表现 | 严重程度 |
|---------|---------|---------|
| **认知风险** | 被理解为 AI Agent / 聊天机器人 / Prompt 工程 | 高 |
| **治理风险** | 社区要求修改 Core / 商业方要求开放边界 | 高 |
| **品牌风险** | Fork 滥用 Tang OS 名称 / 二次开发破坏原则 | 中 |

已有的 ADR-0034（Ecosystem Boundary）和 ADR-0038（Civilization Boundary）定义了系统内部的能力边界，但未定义系统与外部世界接触时的保护规则。

---

## 决策

### 一、Public Release 核心原则

**PRB-001: Release Is Communication, Not Modification.**

公开不是修改。Tang OS 对外发布时不改变任何已冻结的 Core、Invariant、Governance 资产。发布只是让外部知道这些资产的存在。

**PRB-002: Understanding Precedes Participation.**

外部必须先正确理解 Tang OS 是什么，然后才被允许参与。禁止以"先拉人再解释"的方式扩张社区。

**PRB-003: Core Is Not Negotiable.**

任何外部压力（社区投票、商业合作、投资者要求）不能用于修改 Core Identity、Invariant、Four Laws。需要修改的等同于创建新系统，不得使用 Tang OS 名称。

**PRB-004: Ecosystem Is Observed, Not Controlled.**

Tang OS 不控制外部开发者生态。但通过 Certification Standard 和 Extension Governance 定义"什么可以标记为 Tang OS Compatible"。未经认证的实现不得使用官方标识。

**PRB-005: Public Interpretation Cannot Override Specification.**

公开讨论、社区实践、第三方文章可以解释 Tang OS、建议 Extension、创建兼容实现，但不能重新定义 Core、更改 Vocabulary 或覆盖 ADR。社区共识不是修改 Core 的合法依据。符合 ADR-0037 DI-001 并扩展到公开场景。

**PRB-006: Specification Is Implementation Independent.**

Tang OS Specification 不绑定任何特定实现。Python Runtime 是参考实现之一，未来可存在 Rust Runtime、Embedded Runtime 等多实现。不可将参考实现等同于标准本身。

### 二、对外发布前必须完成的 7 个前置条件

#### PC-001: Public Specification

完成 `docs/public/` 规范层，确保外部 5 分钟理解 Tang OS。

#### PC-002: Reference Implementation

完成完整的 Reference Implementation v0.1，可通过 `from tang_os import Tang` 运行。

#### PC-003: Developer Interface

提供 TPI 的实际 API 接口，开发者可基于此构建 Extension。

#### PC-004: Example Applications

至少 3 个官方 Demo：对话版 / 老人陪护版 / 开发者 Extension 创建指南。

#### PC-005: Contributor Governance

明确的 CONTRIBUTING.md，定义允许（Extension）和禁止（修改 Core、创建增强版）的边界。

#### PC-006: Vocabulary Standard

公开 Tang OS Vocabulary v1.0，防止概念漂移。

#### PC-007: Public Release Review

发布前必须经过一次 Public Release Review，确认所有前置条件满足且 Risk Assessment 通过。

### 三、Public Release 准入流程

```
内部完成
    ↓
PC-001~007 全部完成
    ↓
Public Release Review
    ↓
Risk Assessment（认知风险 / 治理风险 / 品牌风险）
    ↓
Founder 最终批准
    ↓
Release
```

### 四、禁止行为（Public Release Context）

**禁止将 Tang OS 称为：**
- "AI 聊天机器人框架"
- "数字人 SDK"
- "情感陪伴引擎"
- "人格模型"

**禁止场景：**
- 以 Tang OS 名义募集资金未经过 Founder 批准
- 对外声称"Tang OS 官方"未经认证
- 发布修改 Core 的 Fork 仍使用 Tang OS 名称

### 五、Phase 13 路线图

```
Phase 13-A  Public Specification
            └── docs/public/ 规范层

Phase 13-B  Reference Implementation v0.1
            └── from tang_os import Tang

Phase 13-C  Developer Interface
            └── TPI API Reference

Phase 13-D  Example Applications
            └── 3+ Demo 应用

Phase 13-E  Open Contribution Governance
            └── CONTRIBUTING.md + 贡献者协议

Phase 13-F  First External Validation
            └── 外部开发者/组织首次接入
```

---

## AR-GATE 检查

### Constraint-001: 充分必要性

**必要性：**
- 如果没有 Public Release Boundary，公开后面临认知漂移、Core 被商业压力侵蚀、Fork 滥用三大真实风险
- 已有 ADR-0034/0038 覆盖系统内部边界，但未覆盖系统与外部接触时的保护规则
- ✅ PASS

**充分性：**
- 新增 PC-001~007 前置条件 + 准入流程 + 禁止行为清单，形成闭环约束
- 不是描述性文档，每个 PC 都有明确完成标准
- ✅ PASS

### Constraint-002: 工程一致性

**层级正确：**
- Principle（PRB-001~004）→ Standard（PC-001~007）→ Interface → Runtime → Validation
- ✅ PASS

**无重复：**
- 不覆盖 ADR-0034（生态边界）、ADR-0038（文明边界）
- 增加的是"系统与外部接触"这一新维度
- ✅ PASS

**复杂度合理：**
- 7 个前置条件是发布的必要条件，不是额外功能
- 复杂度收益比正向
- ✅ PASS

**最终决定：** ✅ PASS → Continue

---

## 后续依赖

- Phase 13-A ~ 13-F 执行计划
- Public Specification 初稿
- Reference Implementation 发布版
- Contributor Governance 法律条款

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — 2 supplements applied

### Review 结果

| # | 检查维度 | 状态 | 补充 |
|---|---------|------|------|
| 1 | 必要性 | ✅ PASS | Public Exposure 场景是新增风险 |
| 2 | 重复性 | ✅ PASS | 与 ADR-0034~0037 不重复 |
| 3 | Public Authority | ✅ 已新增 | PRB-005 公共解释不得覆盖规范 |
| 4 | Spec vs Impl | ✅ 已新增 | PRB-006 规范与实现分离 |

### 补充项（已纳入）

| 编号 | 新增 | 来源 | 理由 |
|------|------|------|------|
| PRB-005 | Public Interpretation Cannot Override Spec | Review-003 | 防止社区共识修改 Core |
| PRB-006 | Specification Is Implementation Independent | Review-004 | 防止参考实现绑定为唯一标准 |

### AR-GATE 复核

```
Constraint-001:
  Necessary: ✅ PASS（Public Exposure 场景是真实新增风险）
  Sufficient: ✅ PASS（PRB-005 + PRB-006 形成闭环）

Constraint-002:
  Layer Correct: ✅ PASS
  No Duplication: ✅ PASS
  Complexity Justified: ✅ PASS（6 条 PRB = 最小必要集）

Final Decision: PASS ✅ → 等待 Accept 后冻结
```
