# ADR-0042: Reference Implementation Standard v1.0

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer（Implementation Boundary）
**影响范围：** Tang OS Reference Implementation 的发布、版本、验证、开源边界
**前序资产：** ADR-0041（Public Specification），PS-010（Reference Implementation Is Evidence）

---

## 背景

PS-010 已冻结核心原则：Reference Implementation Is Evidence, Not Definition。

但原则需要落地为可执行约束。当前缺少：
- Reference Implementation 与 Specification 的版本绑定规则
- Reference Implementation Gate（RIG）验收标准
- Open Source Boundary 决策框架

---

## 决策

### 一、Reference Implementation 定位

Reference Implementation（RI）是 Tang OS Specification 的可运行证明。

- RI 证明规范可以被实现
- RI 不定义规范
- RI 不替代规范
- RI 不拥有任何 Core 修改权

### 二、Reference Implementation Gate（RIG）

RI 版本发布前必须通过以下门闸：

| 编号 | 门闸 | 要求 |
|------|------|------|
| **RIG-001** | Spec Binding | RI 必须声明所绑定的 Specification 版本 |
| **RIG-002** | Identity Protection | RI 不修改 Core Identity Constitution |
| **RIG-003** | Negative Test Priority | RI 必须包含拒绝非法操作的 Negative Tests |
| **RIG-004** | Definition not Implementation | RI 不得声称自己为"官方 Tang OS 实现" |
| **RIG-005** | Test Reproducibility | RI 所有测试必须可独立复现 |
| **RIG-006** | Implementation Independence | RI 不得阻止或限制其他实现的兼容性 |
| **RIG-007** | Version Binding | RI 版本与 Specification 版本绑定 |

### 三、Version Binding（RI-005）

Reference Implementation 必须绑定 Specification Version。

```
Tang OS Specification v1.0
    ↓  requires
Reference Implementation v0.1
```

**禁止：**
- 旧 RI + 新 Spec = 自动兼容
- RI 版本号与 Specification 版本号分离导致混乱
- RI 不声明兼容的 Specification 版本

**规则：**
- RI Major 版本变更必须对应 Specification 的兼容版本声明
- RI 可独立发布 Patch（Bug 修复），但 Major/Minor 变更需重新验证 Spec 兼容性

### 四、RI-006: Testing Requirements

Reference Implementation 必须包含两类测试：

**Positive Tests（证明合法输入→正确行为）：**
- 规范的正常路径在 RI 上可运行
- 输出符合 SPEC 要求

**Negative Tests（证明非法能力→拒绝，更重要）：**
- 修改 Identity Constitution → Reject
- 绕过 Invariant → Reject
- 越权 Capability → Reject
- Memory 污染（I-17）→ Reject
- Host Authority 扩权 → Reject

### 五、RI-007: Version Rules

Reference Implementation 版本规则：

```
v0.x — 实验/参考实现阶段
```

**禁止声称：**
- "Tang OS v1.0 Implementation"

**必须声明：**
```
Tang OS Reference Implementation v0.x
compatible with Tang OS Specification v1.0
```

### 六、RIG-004: Fail Behavior

默认 Fail Closed。

| 环境 | 模式 | 行为 |
|------|------|------|
| 开发 | Fail Open | 发现问题 → 暴露 → 调试 |
| 生产 | Fail Closed | 未知状态 → 拒绝 |

生产环境中，涉及 Capability、Permission、Emergency Action、Physical Host 的操作：
- Unknown State → Reject
- 未通过 Permission Runtime → Reject
- 超出 Authority Ceiling → Reject

### 七、Open Source Neutrality（RI-008）

> Reference Implementation Standard does not mandate a specific licensing model. Open source policy is an ecosystem decision independent from compatibility requirements.

含义：
- 开源 ≠ 更标准
- 闭源 ≠ 不兼容
- Certification 不依据许可证判断
- 具体开源范围由生态战略阶段决定，不由规范约束

### 六、Reference Implementation Registry（待决）

是否需要官方 Registry 记录通过的 Reference Implementation？

可选：
- 单官方 RI（当前 Python 实现）
- 多 RI 注册（允许 Rust/Embedded 等实现注册）

建议多 RI 注册，但需与 ADR-0036 Extension Governance 协调。

---

## AR-GATE

### Constraint-001 必要性

是否需要 ADR-0042？

当前：Specification ✅ Certification ✅ Implementation ❌
风险：Implementation 可能反向成为标准。

**PASS ✅**

### Constraint-002 充分性

ADR-0042 只解决 Reference Implementation Boundary，未进入 Runtime 设计、Core 修改、产品策略。

**PASS ✅**

### Layer Discipline

Specification → Reference Implementation → Certification

**PASS ✅**

---

## 后续依赖

- RIG-004 Fail Behavior 模式决策
- Open Source Boundary Founder 决策
- Reference Implementation Registry 设计

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — RIG table restructured, RI-006/007 added

### Review 结果

| # | 检查维度 | 状态 | 补充 |
|---|---------|------|------|
| 1 | RI 定位 | ✅ Evidence not Authority | RIG-004 |
| 2 | 测试要求 | ✅ 已补充 | RI-006 Positive + Negative Tests |
| 3 | 版本规则 | ✅ 已补充 | RI-007 v0.x 前缀 + 兼容声明 |
| 4 | Multi-Impl Compat | 🟡 RIG-006 | 不阻止其他实现 |
| 5 | Open Source | 🟡 待决 | Found - Boundary 决策 |

### 补充项（已纳入）

| 编号 | 新增 | 理由 |
|------|------|------|
| RIG-003 | Negative Test Priority | 拒绝测试更重要 |
| RIG-005 | Test Reproducibility | 不可复现的测试无价值 |
| RIG-006 | Implementation Independence | 不阻止第三方实现 |
| RI-006 | Testing Requirements | Positive + Negative 双轨 |
| RI-007 | Version Rules | v0.x + 兼容声明 |

### AR-GATE 复核

```
Constraint-001:
  Necessary: ✅ PASS（RI 反向定义规范是真实风险）

Constraint-002:
  Sufficient: ✅ PASS（RIG-001~007 + RI-006~007 形成闭环）

Layer Discipline: ✅ PASS
No Duplication: ✅ PASS
Complexity Justified: ✅ PASS

Final: ✅ PASS — 等待 Accept
```
