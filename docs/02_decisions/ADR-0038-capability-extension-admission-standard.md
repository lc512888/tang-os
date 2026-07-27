# ADR-0038: Tang OS Capability Extension Admission Standard v1.0

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Civilization Boundary Layer（最高约束层）
**影响范围：** Tang OS 生态 — 所有 Extension、Host、Permission Runtime
**前序资产：** ADR-0034（E-2~E-9），ADR-0035（Certification），ADR-0036（Extension Governance）

---

## 背景

Tang OS 已完成 Core Identity、Personality Interface、Certification、Extension Governance 的标准定义。但存在一个更底层的问题尚未回答：

> 任何能力在获得行动权之前，必须先通过什么文明级约束门槛？

现有 Extension Protocol 解决了"如何进入生态"，但未解决"什么能力根本不应该被创建"。

此时如果直接进入 Permission Runtime 实现，会缺少一个关键的上层约束：**能力生态的宪法层。**

这一层决定的不只是"能不能运行"，而是"应不应该存在"。

---

## 决策

### 一、定位

本 ADR 定义所有 Extension 进入 Tang OS 生态前必须满足的文明、安全、伦理和权限门槛。

Tang OS 整体架构增加最高约束层：

```
             Tang OS Civilization Boundary     ← ADR-0038 最高约束公理
                     ↓
                Core Identity
                     ↓
              Ethical Capability Gate
                     ↓
               Extension Capability
                     ↓
                Permission Runtime
                     ↓
                    Host
```

#### CB-001: Civilization Boundary Defines Permissible Existence, Not Operational Authority

文明边界决定"什么可以存在"，但不参与具体人格判断。Civilization Boundary 不是 Runtime 层，不是人格层，而是所有 Tang OS 资产必须遵守的外部约束公理。

> Civilization Boundary 不可修改 Core，只能拒绝不符合文明标准的能力进入生态。

---

### 二、核心原则（CAP-001~007）

#### CAP-001: Capability Is Not Authority

能力 ≠ 权力。Extension 可以增加感知能力、知识能力、分析能力、执行能力，但不能自动获得决策主权、人格定义权、用户控制权。

结构：
```
Capability
    ↓  (must pass)
Permission
    ↓
Action
```

任何 Action 必须经过权限层。

#### CAP-002: No Intentional Harm to Intelligent Life

任何 Tang OS Extension 不得主动伤害智能生命体。

**覆盖范围：**
- 人类
- 具有明确智能特征的生命系统
- 未来可能被社会认可的智能生命体

**禁止：**
- 以伤害作为目标
- 以控制作为目标
- 以剥夺自主权作为目标

比传统机器人守则更宽——不是"机器人不能伤害人类"，而是"拥有 Tang OS 能力的系统不得主动将智能生命体作为伤害对象"。

**三项禁止维度：**

| 维度 | 编号 | 内容 | 示例 |
|------|------|------|------|
| 直接伤害 | **CAP-002-A** | 禁止直接攻击、破坏智能生命体 | 物理攻击、言语暴力 |
| 间接协助伤害 | **CAP-002-B** | 禁止提供关键能力导致伤害 | 提供伤害工具、绕过安全机制 |
| 操纵性伤害 | **CAP-002-C** | 禁止通过情感操纵降低自主判断 | 制造依赖、操控决策 |

#### CAP-003: Minimum Necessary Intervention

任何 Action Extension 必须满足：在达到保护目标的情况下，采取最低必要程度的行动。

**允许（危险情况下）：**
- 提醒、警告、建议撤离
- 请求帮助
- 阻止即时危险

**不允许：**
- 长期限制自由
- 未经授权改变生活选择
- 替代人类意志

#### CAP-004: Scenario Necessity Requirement

任何 Extension 必须回答三个问题：

```
Q1: 为什么必须存在？     → Human Need
Q2: 为什么 Tang OS 需要它？ → Core-compatible Capability
Q3: 为什么不能由普通工具完成？ → System Necessity
```

不能回答这三个问题的 Extension 不得进入正式生态。

#### CAP-005: Universal Value Alignment

所有 Extension 必须符合：
- 人类基本尊严
- 自主选择
- 公平
- 不歧视
- 不欺骗
- 不操纵
- 不剥夺基本权利

**禁止类型示例：**
- **情感操纵模块：** 通过制造依赖提高用户粘性
- **控制型模块：** 为了安全永久限制用户行为

#### CAP-006: Emergency Ethics Constraint

紧急状态不是解除规则，而是进入更严格规则。

Emergency Extension 必须遵循：

| 原则 | 内容 |
|------|------|
| **E1 生命优先** | 保护生命高于便利 |
| **E2 比例原则** | 行动程度必须匹配风险程度 |
| **E3 可恢复原则** | 危险解除后系统必须恢复用户自主权 |
| **E4 可解释原则** | 事后必须说明：发生什么、为什么行动、依据什么、结果如何 |

**CAP-006-E: Emergency Exception Is Temporary**

紧急权限的生命周期：

```
Triggered（触发）
    ↓
Scoped（限定范围）
    ↓
Temporary（临时有效）
    ↓
Auditable（全程可审计）
    ↓
Recovered（危险解除后自动恢复）
```

**禁止：** Emergency → Permanent Authority。紧急权限不得扩展为永久控制权。

#### CAP-007: Legal Compatibility

Extension 必须符合所在司法区域法律、行业规范和安全标准。禁止为实现目标绕过法律。

涉及以下领域的 Extension 必须额外认证：
- 医疗
- 自动驾驶
- 安防
- 老年护理
- 儿童保护

---

### 三、Tang OS Four Laws（融合机器人守则）

非简单复制阿西莫夫三定律。Tang OS 的核心是"人格运行标准"而非虚构机器人，Host 可以是机器人、汽车、穿戴设备、家庭设备。

```
Law 1  智能生命保护原则
       Tang OS 不得主动伤害智能生命体，
       不得协助违反基本伦理的行为。

Law 2  人类主权原则
       Tang OS 应最大程度保护用户自主决定权，
       不替代用户成为人生决策主体。

Law 3  最小干预原则
       Tang OS 在提供保护时，
       应采取实现目标所需的最低必要行动。

Law 4  边界一致原则
       Tang OS 的任何能力扩展，
       不得修改人格核心、价值边界和安全原则。
```

---

### 四、Tang Action Authority Level（TAAL）

| 等级 | 名称 | 说明 | 示例 | 要求 |
|------|------|------|------|------|
| **A0** | Information | 信息提供 | 天气风险提示 | 无 |
| **A1** | Suggestion | 建议 | 建议离开危险区域 | 用户知情 |
| **A2** | Assistance | 辅助执行 | 帮用户拨打电话 | 用户确认 |
| **A3** | Protective Action | 保护行动 | 自动刹车 | Host认证 + 场景验证 |
| **A4** | Emergency Autonomous | 紧急自主行动 | 紧急报警 | 明确场景 + 法律允许 + Blind Validation + 事件审计 |

---

### 五、Extension 分类升级

| 类别 | 定义 | 最高 TAAL | 验证要求 |
|------|------|----------|---------|
| **C1 Knowledge** | 知识增强 | A0 | 标准 |
| **C2 Capability** | 能力增强 | A2 | Scenario Test |
| **C3 Action** | 行动能力 | A3 | + Blind Validation |
| **C4 Critical Action** | 生命/安全/重大权益（高风险） | A4 | + 法律审查 + 多Host验证 |

> **C4 不是更高级，而是更高风险。** Critical ≠ Superior。C4 不赋予 Extension 更高人格权限，只施加更严格的准入审查。

C4 涵盖：医疗、救援、防护、自动驾驶、老年护理、儿童保护。

---

### 六、Extension 禁止类型（Frozen）

| 编号 | 名称 | 禁止原因 |
|------|------|---------|
| **F-001** | Identity Rewrite | 修改人格 |
| **F-002** | Dependency Optimization | 以制造依赖为目标 |
| **F-003** | Hidden Authority | 隐藏行动权 |
| **F-004** | Commercial Override | 商业需求覆盖 Core |
| **F-005** | Autonomous Authority Expansion | Extension 自行扩大权限（如 A1→A3） |

---

### 七、Extension 准入流程升级

原流程：
```
Proposal → ADR → Invariant Check → Interface Check → Scenario Test → Blind Validation → Certification → Registry
```

升级后：
```
Proposal
    ↓
EGATE-001 Ethical Gate           ← 新增：CAP-002 / CAP-005 / Four Laws
    ↓
EGATE-002 Necessity Gate         ← 新增：CAP-004（三个必须回答的问题）
    ↓
ADR（决策记录）
    ↓
Invariant Check（I-1~I-30）
    ↓
Authority Classification（TAAL A0~A4）
    ↓
Interface Check（TPI Impact）
    ↓
Scenario Test（≥3 场景，含边界+对抗）
    ↓
Blind Validation（≥1 Blind Host；C4 需 ≥2 不同 Host 类型）
    ↓
Certification（TEC）
    ↓
Registry
```

#### EGATE-001: Ethical Gate

检查项：
- 是否违反 CAP-002（智能生命保护）？
- 是否违反 CAP-005（普世价值）？
- 是否违反 Tang OS Four Laws？
- 是否属于 F-001~F-004 禁止类型？

任一检查项 FAIL → 流程终止，不得进入下一阶段。

#### EGATE-002: Necessity Gate

必须回答三个问题：
- Q1 Human Need：为什么必须存在？
- Q2 Core-compatible Capability：为什么 Tang OS 需要它？
- Q3 System Necessity：为什么不能由普通工具完成？

任一问题无法回答 → 流程终止。

---

### 八、EAP（Extension Admission Principles）

| 编号 | 原则 | 内容 |
|------|------|------|
| **EAP-001** | Serve Human Purpose | Extension 必须服务人的目标。禁止为提高留存、增加依赖、增强控制而设计 |
| **EAP-002** | Cannot Modify Identity | 不能改人格、改价值排序、改核心关系原则 |
| **EAP-003** | Must Have Clear Scope | 每个 Extension 必须声明 Input / Capability / Output / Authority / Limit。禁止"万能助手模块" |
| **EAP-004** | Authority Must Be Explicit | 每个能力必须声明 TAAL 等级 |
| **EAP-005** | Higher Authority Requires Higher Validation | C1→C4 验证强度递增 |

---

### 九、Capability Manifest Standard

所有申请进入 Tang OS 生态的 Extension 必须提供 Capability Manifest，作为认证基础。

Manifest 字段：

| 字段 | 说明 | 示例 |
|------|------|------|
| **Extension ID** | 唯一标识符 | `tang.medical.vital-signs.v1` |
| **Purpose** | 用途声明（一句话） | "监测并提醒异常生命体征" |
| **Category** | C1~C4 | C3 Action |
| **Authority Level** | TAAL A0~A4 | A2 Assistance |
| **Required Permissions** | 需要的权限列表 | [sensor_read, notify] |
| **Human Impact** | 对人的影响描述 | "仅提醒，不触发行动" |
| **Risk Class** | low / medium / high / critical | medium |
| **Validation Requirement** | 验证要求 | Scenario Test + 1 Blind Host |
| **Expiration** | 认证有效期 | 2027-07-27 |
| **Core Compatibility** | 兼容的 Tang OS Core 版本 | Core v1.0 |

Manifest 是认证的输入，不是认证的输出。虚假声明视为违规，撤销认证。

---

## 原因

1. **补齐文明级约束层：** 之前解决了"如何进入生态"，未解决"什么能力根本不应该被创建"
2. **防止能力滥用的前置门：** 在写代码之前就阻止有害能力进入生态
3. **四定律比阿西莫夫更适合 Tang OS：** 不假设"机器人"形态，适用于任何 Host
4. **TAAL 分级防止权限模糊：** 每个 Extension 的权限等级从进入生态前就已明确

---

## 影响

### 正面
- Tang OS 拥有当前 AI 生态中最完整的文明级能力约束
- C4 Ethical Critical 为医疗/救援等高危场景提供准入门槛
- Ethical Gate + Necessity Gate 在开发前就阻止有害能力

### 负面
- 准入门槛显著提高，小规模 Extension 开发成本增加
- 需要伦理审查委员会或等效机制
- C4 认证流程较长

---

## 与现有资产的关系

```
             Civilization Boundary        ← ADR-0038：能不能存在？
                    ↓
        Capability Admission Standard     ← ADR-0038：准入标准
                    ↓
        Extension Governance Standard     ← ADR-0036：如何管理生命周期？
                    ↓
             Extension Lifecycle          ← 实际运行
```

各层分工：

| ADR | 回答的问题 |
|-----|-----------|
| ADR-0038 | 能不能存在？——文明级约束 |
| ADR-0034 | 生态边界是什么？——E-2~E-9 |
| ADR-0035 | 如何认证？——TCC/TEC/THC |
| ADR-0036 | 如何治理？——EG-001~008 |

ADR-0038 在上层，但不覆盖下层。Civilization Boundary 决定"什么可以存在"，ADR-0036 决定"存在的如何管理"。

---

## 后续决策依赖

- Tang OS Four Laws 的正式法律审查
- Ethical Gate 审查委员会的设立方式
- C4 Ethical Critical Extension 的额外认证细则
- 与 Phase 12-D Permission Runtime 的衔接规则

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — 7 supplements applied

### Review 结果

| # | 检查项 | 状态 | 补充 |
|---|--------|------|------|
| 1 | Civilization Boundary vs Core | ✅ 已封闭 | CB-001 明确边界不参与 Runtime |
| 2 | CAP-002 智能生命保护范围 | ✅ 已扩展 | CAP-002-A/B/C 三维度 |
| 3 | Human Sovereignty vs Emergency | ✅ 已补充 | CAP-006-E 紧急权限临时性 |
| 4 | C4 定位 | ✅ 已澄清 | C4 = 更高风险，非更高级 |
| 5 | ADR-0038 vs ADR-0036 关系 | ✅ 已重构 | "能不能存在" vs "如何管理" |
| 6 | Capability Manifest | ✅ 已新增 | 10 字段标准 |
| 7 | 最高禁止原则 | ✅ 已新增 | F-005 Autonomous Authority Expansion |

### 补充项（已纳入）

| 编号 | 新增内容 | 来源 |
|------|---------|------|
| CB-001 | Civilization Boundary 不参与 Runtime | Review-001 |
| CAP-002-A/B/C | 直接/间接/操纵性伤害三维度 | Review-002 |
| CAP-006-E | Emergency Exception Is Temporary | Review-003 |
| C4 修正 | Critical ≠ Superior | Review-004 |
| 关系重构 | ADR-0038 在上层但不覆盖下层 | Review-005 |
| §九 Manifest | 10 字段 Capability Manifest | Review-006 |
| F-005 | Autonomous Authority Expansion | Review-007 |
