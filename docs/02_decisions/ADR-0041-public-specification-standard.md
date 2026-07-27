# ADR-0041: Tang OS Public Specification Standard v1.0

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer（Public Specification）
**影响范围：** 所有对外公开的 Tang OS 规范文档、技术白皮书、开发者指引
**前序资产：** ADR-0037（Documentation Standard），ADR-0040（Public Release Boundary）

---

## 背景

ADR-0040 定义了"什么条件下 Tang OS 可以被外部接触"，但未定义"什么算 Tang OS 的官方规范"。

当前已有：
- ADR-0034 生态边界
- ADR-0035 认证标准
- ADR-0036 Extension 治理
- ADR-0037 文档标准
- ADR-0040 发布边界

但缺少一个统一定义：**什么叫 Tang OS Public Specification？**

否则容易出现：
- Overview 被误认为完整规范
- Developer Guide 被误认为开发许可
- Reference Implementation 被误认为唯一实现
- 社区文档被误认为官方标准

---

## 决策

### 一、Public Specification 定位

#### PS-001: Specification Defines Compatibility

Tang OS Public Specification 是：

> A normative description of Tang OS behavior that determines implementation compatibility.

不是：
- ❌ 产品说明
- ❌ 开发教程
- ❌ 商业白皮书
- ❌ 人格宣传材料

而是唯一可用于判定"某实现是否与 Tang OS 兼容"的权威依据。

#### PS-002: Specification Is Not Implementation

规范独立于实现。不同实现（Python、Rust、Embedded 等）必须产生相同行为。
Reference Implementation 是规范的证明，不是规范本身（PRB-006）。

#### PS-003: Specification Sources Only

规范文仅引用以下资产：
- Frozen ADR（已接受的决策记录）
- Frozen Standard（Phase 9 Core Standard v1.0 等）
- Validation Evidence（Phase 10 验证报告等）

禁止引用：
- 历史聊天记录
- 未冻结的设计讨论
- 外部文章或第三方解释

#### PS-004: Vocabulary Binding

规范必须使用 Tang OS Vocabulary（DI-003），禁止：
- 用"AI Agent"替代 Tang OS
- 用"Plugin"替代 Extension
- 用"Device"替代 Host
- 用"Prompt"替代 Personality Interface

#### PS-005: No Marketing Language

规范中禁止：
- 最高级用语（"最先进"、"唯一"）
- 产品对比（"优于XX"）
- 未来愿景（"将能"、"计划"）
- 情感诉求（"改变世界"）

#### PS-006: Specification Defines Compliance, Not Authority

Specification 可以定义如何判断兼容、如何验证实现，但不能定义新人格原则、新价值边界、新 Core 权限。防止未来生态误认为"规范拥有定义人格的权力"。

#### PS-007: Specification Level ≠ Certification Level

PSL 是文档成熟度分级，Certification 是实现兼容性分级。二者独立。PSL-3 不代表已认证，L3 Certified 不代表已发布规范。

#### PS-008: Specification Defines Interfaces, Not Internal APIs

Specification 定义 Interface Contract（TPI 等外部契约），不公开 Runtime Implementation Detail。Tang OS 是 Personality Operating Standard，不是 Software Library。

#### PS-009: Specification Interpretation Boundary

Specification 可以描述 Core 兼容性要求，但不能创造新的 Core 含义。禁止通过规范解释的方式重新定义 Identity、Invariant 或扩展 Authority。

```
Specification
    ├── defines: compatibility criteria, interface expectations, validation requirements
    └── cannot: redefine Identity, redefine Invariant, expand Authority
```

#### PS-010: Reference Implementation Is Evidence, Not Definition

Reference Implementation 证明规范的可实现性，但不定义规范本身。

```
Specification         → defines requirements
Reference Impl        → demonstrates one realization
External Impl         → allowed if compatible
```

防止官方实现垄断标准定义权。第三方实现只要通过认证即视为兼容。

#### PS-011: External Conformance Test Reference

Specification 定义"what must be true"，Conformance Test 定义"how to verify"。二者分离：

```
Specification → what must be true
    ↓
Conformance Test Suite → how to verify
    ↓
Certification → pass/fail
```

Specification 层不包含 Conformance Test 的具体实现，只引用测试的必要条件。

---

### 二、Public Specification Level（PSL）

| 级别 | 名称 | 内容 | 认证效力 |
|------|------|------|---------|
| **PSL-1** | Overview | Tang OS 是什么、核心概念、架构总览 | 无法律效力 |
| **PSL-2** | Normative Spec | Core / TPI / Extension / Permission / Host 的规范性描述 | 可作为认证依据 |
| **PSL-3** | Reference Guide | API 参考、实现示例、验证指南 | 辅助认证 |

PSL-2 为唯一认证依据。PSL-1 和 PSL-3 不得包含与 PSL-2 冲突的内容。

> **PSL ≠ Certification Level。** PSL 是文档成熟度，Certification 是实现兼容性。PSL-3 不代表已通过 TCC/TEC/THC 认证（PS-007）。

---

### 三、Public Specification Gate（PSG）

每个规范文档发布前必须通过以下门闸：

| 编号 | 门闸 | 要求 |
|------|------|------|
| **PSG-001** | 来源可追溯 | 每条声明必须可追溯到 Frozen ADR / Standard / Validation |
| **PSG-002** | 不与实现绑定 | 不要求必须使用 Python 参考实现 |
| **PSG-003** | 不与 Marketing 混淆 | 通过 PRB-002（理解先于参与）检查 |
| **PSG-004** | 实现分离 | 明确标注"本规范不绑定具体实现" |
| **PSG-005** | Certification 引用明确 | 涉及认证的内容必须链接到 ADR-0035 |
| **PSG-006** | 无营销语言 | 通过 PS-005 检查 |
| **PSG-007** | 第三方可验证 | 规范中的声明必须可由第三方独立验证 |

---

### 四、Compliance Matrix（CM-001）

Specification、Validation、Certification 之间的映射关系。每项 Spec 要求必须对应至少一项验证方法和一项认证检查：

| Spec ID | Requirement | Source | Validation | Certification |
|---------|------------|--------|------------|---------------|
| SPEC-001 | Specification Boundary | ADR-0041 | Audit | TCC |
| SPEC-100 | Tang OS Positioning | ADR-0034 | Doc Check | — |
| SPEC-200 | Identity Constitution | Core-001 | Identity Test | TCC |
| SPEC-300 | Invariant System | Core-002 | Invariant Check | TCC |
| SPEC-400 | Decision Model | Core-003 | Scenario Test | TCC |
| SPEC-500 | Safety Model | Core-004 | Safety Audit | TCC |
| SPEC-600 | Memory Boundary | Core-005 | Isolation Test | TCC |
| SPEC-700 | TPI | TPI v1.0 | Interface Test | TEC |
| SPEC-800 | Capability Classification | ADR-0038 | Capability Audit | TEC/THC |

Compliance Matrix 随 Specification 版本更新。新增 Spec 要求时必须同步更新对应 Validation 和 Certification 条目。

---

## AR-GATE

### Constraint-001: 必要性

**检查：** 是否解决已知风险？

公开标准缺少统一定义，会导致生态解释漂移。外部可能将 Overview 当作完整规范，将 Reference Implementation 当作唯一实现。

**结果：** ✅ PASS

### Constraint-002: 充分性

**检查：** 是否形成实际约束？

PS-001~005 明确规范 ≠ 实现 ≠ Marketing。PSL 三级区分认证效力。PSG 七门闸确保发布质量。

**结果：** ✅ PASS

### Layer Discipline

```
ADR Frozen Assets → Specification → Implementation
```

未越级。 ✅ PASS

### Minimal Necessary

新增：
- PS-001~011（11 条定位原则）
- PSL（三级分层）
- PSG（七门闸）
- CM-001（Compliance Matrix）

均对应公开阶段真实风险。PS-009/010/011 分别解决解释权边界、实现分离、验证路径三个审查发现的风险。

无过度设计。 ✅ PASS

---

## 后续依赖

- Public Specification PSL-2 初稿（Core / TPI / Permission / Host 规范正文）
- Vocabulary Standard 独立文档
- PSL-1 Overview 初稿

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — 3 supplements applied (Round 2)

### Review 结果

| # | 检查维度 | 状态 | 补充 |
|---|---------|------|------|
| 1 | Specification 权力化风险 | ✅ 已封闭 | PS-006 + PS-009 |
| 2 | PSL/Certification 重叠 | ✅ 已区分 | PS-007 |
| 3 | Vocabulary 独立文件 | 🟡 已完成 | PART-006_TERMINOLOGY.md |
| 4 | 规范是否包含 API | ✅ 已封闭 | PS-008 |
| 5 | Marketing Language 边界 | ✅ PASS | PS-005 保持 |
| 6 | Reference Impl 定义权 | ✅ 已封闭 | PS-010 |
| 7 | Compliance Matrix | ✅ 已新增 | CM-001 |
| 8 | Conformance Test 路径 | ✅ 已封闭 | PS-011 |

### 补充项（已纳入，Round 2）

| 编号 | 新增 | 来源 | 理由 |
|------|------|------|------|
| PS-009 | Specification Interpretation Boundary | Review-001 | 防止解释权成为 Core 控制权 |
| PS-010 | Reference Implementation Is Evidence | Review-002 | 防止官方实现垄断标准 |
| PS-011 | External Conformance Test Reference | Review-004 | 规范与验证路径分离 |
| CM-001 | Compliance Matrix | Review-003 | Spec→Validation→Cert 映射 |

### AR-GATE 复核

```
Constraint-001:
  Necessary: ✅ PASS（4 新增对应 4 真实风险）
  Sufficient: ✅ PASS

Constraint-002:
  Layer Correct: ✅ PASS
  No Duplication: ✅ PASS
  Complexity Justified: ✅ PASS（11 PS + CM-001 = 最小必要）

Final Decision: PASS ✅ → 冻结
```
