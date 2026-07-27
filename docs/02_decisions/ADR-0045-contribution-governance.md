# ADR-0045: Tang OS Contribution Governance Standard v1.0

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer（Ecosystem Contribution）
**影响范围：** 所有外部贡献者、Maintainer、社区治理
**前序资产：** ADR-0036（Extension Governance），ADR-0040（Public Release），ADR-0044（Example Application）

---

## 背景

Phase 13-A~D 完成了 Tang OS 从标准定义到生态证明的完整链路。但缺少开放生态前的最后一个关键环节：

> 第三方如何贡献代码、Extension、Host，而不会逐渐分叉出"另一个 Tang OS"？

现有的 ADR-0036（Extension Governance）定义了 Extension 的生命周期管理，ADR-0040（Public Release Boundary）定义了发布边界。但未定义：

- 贡献者的权限边界
- Maintainer 的角色和责任
- Proposal → Review → Merge 流程
- Fork 治理策略
- Specification 漂移防护

---

## 决策

### 一、贡献者分层

| 层级 | 角色 | 权限 | 获得方式 |
|------|------|------|---------|
| **Contributor** | 提交 PR / Extension | 提交代码、创建 Extension | 签署 CLA |
| **Reviewer** | 审核贡献 | 审核代码、批准 Extension | Maintainer 任命 |
| **Maintainer** | 维护模块 | Merge、版本发布 | Founder 任命 |
| **Core Maintainer** | 维护 Core | Core Identity 变更 | 仅 Founder |

### 二、CG-001: Contribution ≠ Core Modification

任何贡献不得修改：
- Core Identity Constitution
- I-1~I-30
- Tang OS Four Laws
- Civilization Boundary（ADR-0038）

违反上述任一条的贡献 → 直接关闭，不进入 Review。

### 三、CG-002: Fork Policy

允许：
- 功能分支（feature / extension）
- 个人 Fork
- 兼容实现

禁止：
- 修改 Core 后仍声称"Tang OS"
- Fork 后删除 Governance 文件
- Fork 后重命名为"Tang OS XXX Edition"

### 四、CG-003: Proposal → Review → Merge

```
Proposal（Issue / PR）
    ↓
Reviewer Check（24h 内响应）
    ↓
Invariant Check（自动 CI）
    ↓
AR-GATE（架构级变更）
    ↓
Maintainer Merge
    ↓
Core Maintainer（仅 Core 变更）
```

### 五、CG-004: Specification Drift Protection

| 防护 | 措施 |
|------|------|
| 文档漂移 | 文档 PR 必须关联对应 ADR |
| 代码漂移 | CI 自动运行 Conformance Harness |
| Extension 漂移 | 通过 ADR-0038 准入检查 |
| 命名漂移 | 通过 ADR-0037 DI-003 Vocabulary 检查 |

### 六、CG-005: Maintainer Boundary

Maintainer 可以：
- Review 和 Merge 非 Core 变更
- 管理 Extension Registry
- 管理 Issue 和 Discussion

Maintainer 不可以：
- 修改 Core Identity
- 修改 Governance ADR（ADR-0034/0038/0040/0045）
- 单方面变更 Specification

---

## AR-GATE

### Constraint-001 必要性

Contribution Governance 尚未被现有 ADR 覆盖。无此标准则开放贡献后必然出现分叉和漂移。

✅ PASS

### Constraint-002 充分性

CG-001~005 覆盖贡献者分层、Fork 策略、Review 流程、Spec 漂移防护、Maintainer 边界。

✅ PASS

### Layer Discipline

Governance Layer → Ecosystem Contribution → Implementation

✅ PASS

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — No supplements required

### Review 结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 必要性 | ✅ PASS | 贡献者治理未被现有 ADR 覆盖 |
| CG-001 | ✅ PASS | Contribution ≠ Core Modification，与 SDK 层互补 |
| CG-002 | ✅ PASS | Fork Policy 区分合法实现 Fork 与禁止的 Spec Fork |
| CG-003 | ✅ PASS | 与 ADR-0036 Extension Lifecycle 层级不同 |
| CG-004 | ✅ PASS | Specification Drift Protection，与 PS-006 闭环 |
| CG-005 | ✅ PASS | Maintainer 不拥有 Core/Identity/Spec 修改权 |

### 补充审查

| 编号 | 审查项 | 结论 |
|------|--------|------|
| Review-001 | Human Founder Boundary | ❌ 不新增 — ADR-0005 已覆盖 |
| Review-002 | Community Voting | ❌ 不加入 — 防 Popularity > Specification |
| Review-003 | Maintainer Certification | ❌ 不增加 — ADR-0035 认证对象是 Capability |
| Review-004 | CLA | ❌ 不加入 — 实现层问题，非架构 ADR |

### AR-GATE Final

```
Constraint-001: Necessary      ✅ PASS
Constraint-002: Sufficient     ✅ PASS
Layer Discipline:              ✅ PASS
No Duplication:                ✅ PASS
Complexity Ratio:              ✅ PASS
Minimal Necessary:             ✅ PASS

Final Decision: PASS ✅ — 等待 Founder Accept
```
