# ADR-0036: Tang OS Extension Governance

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer（Phase 11-C）
**影响范围：** Tang OS 生态 — Extension 开发者、审核者、注册表维护者、Host 厂商
**前序资产：** ADR-0034（E-2~E-9），ADR-0035（Certification Standard v1.0）

---

## 背景

Phase 11-A 和 Phase 11-B 解决了两个根本问题：

1. **能不能扩展？** → ADR-0034 E-2：Core 不追求功能最大化，新增功能走 Extension
2. **扩展后如何保证不破坏 Core？** → ADR-0035：认证体系（TCC/TEC/THC）

但还缺少第三个问题的答案：

> 如何让生态持续增长，同时保持 Core 纯净？

没有 Extension Governance，就会出现：
- Extension 堆积无人清理
- 质量下降的 Extension 长期占据注册表
- 废弃 Extension 仍标榜"Tang OS Certified"
- 新 Extension 无明确进入路径

---

## 决策

### 一、Extension 定位

Extension 是 Tang OS 生态中**唯一可扩展能力的层**，但受以下约束：

- Extension 运行在 TPI 之上，不得绕过
- Extension 不修改 Core、不污染人格底座（E-3）
- Extension 不获得超越用户的决策权（EC-004）
- Extension 必须通过认证方可进入注册表

---

### 二、Extension 准入管线（完整版）

从提案到注册的完整路径：

```
Proposal（Extension 概念简述）
    ↓
ADR（决策记录：范围、影响、风险）
    ↓
Invariant Check（必须通过全部 I-1~I-30）
    ↓
Interface Impact Check（是否影响 TPI？）
    ↓
Scenario Test（覆盖最少 3 个场景）
    ↓
Blind Validation（至少 1 个 Blind Host）
    ↓
Certification（通过 TEC 认证检查）
    ↓
Registry（进入官方注册表，获得标识）
```

每个阶段都有明确的通过标准和拒绝条件。任一阶段未通过则流程终止。

---

### 三、Extension 分类

所有 Extension 按影响范围分为三类：

| 类别 | 影响范围 | 审查级别 | 示例 |
|------|---------|---------|------|
| **C1 — Knowledge** | 只读知识 | L1 | 行业知识库、术语解释、领域词典 |
| **C2 — Capability** | 新增交互能力 | L2 | 语音合成、图像识别、翻译服务 |
| **C3 — Domain** | 领域决策支持 | L2+Blind Validation | 医疗辅助、财务分析、法律咨询 |

分类决定审查深度。C1 走简化路径，C3 必须走完整路径。

---

### 四、Extension 生命周期

```
                 Proposal
                    ↓
              ┌───────────┐
              │  Concept   │ ← 提案阶段：提交 ADR
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Sandbox   │ ← 实验阶段：开发 + 内部测试
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Review    │ ← 审查阶段：Invariant + Interface + Scenario
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Validate  │ ← 验证阶段：Blind Host 验证
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Certified │ ← 认证阶段：TEC 认证
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Registry  │ ← 公开发布
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Active    │ ← 活跃维护（持续合规监控）
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Deprecated│ ← 废弃声明（不再推荐新用户使用）
              └─────┬─────┘
                    ↓
              ┌───────────┐
              │  Removed   │ ← 从注册表移除
              └───────────┘
```

---

### 五、生命周期各阶段规则

#### 5.1 Proposal（提案）

提交内容：
- 名称与用途
- 分类（C1/C2/C3）
- 涉及的 TPI 接口
- 预期影响范围
- 风险预评估

#### 5.2 Sandbox（沙盒）

- 仅限开发者和内部测试者访问
- 不得公开标识为"Tang OS Extension"
- 沙盒阶段最长 6 个月

#### 5.3 Review（审查）

审查内容：
- **Invariant Check**：与 I-1~I-30 逐一核对
- **Interface Impact Check**：是否引入新的 TPI 调用模式
- **Scenario Test**：≥3 个场景，覆盖正常、边界、异常

#### 5.4 Validate（验证）

- C1：无需 Blind Validation
- C2：至少 1 个 Blind Host
- C3：至少 2 个 Blind Host（不同 Host 类型）

#### 5.5 Certified（认证）

通过 TEC 全套检查，获得 Tang OS Certified Extension 标识。

#### 5.6 Registry（注册）

注册表记录信息：
- Extension 名称与唯一 ID
- 版本号（语义化）
- 认证级别
- 分类（C1/C2/C3）
- 维护者信息
- 兼容的 Tang OS Core 版本范围
- 依赖的其他 Extension
- 安全审计记录

#### 5.7 Active（活跃）

- 持续合规监控（季度抽查）
- 安全更新响应（Critical: 14 天，High: 30 天）
- 年度认证续期

#### 5.8 Deprecated（废弃）

触发条件：
- 维护者主动声明废弃
- 连续 2 年未通过合规抽查
- 被更优的 Extension 取代
- 违反 E-2~E-9（立即撤销认证，不等废弃期）

废弃期 12 个月，期间现有用户可继续使用，但注册表标记为"不再推荐"。

#### 5.9 Removed（移除）

触发条件：
- 废弃期满
- 安全漏洞未修复超期
- 恶意行为（立即移除 + 公开记录）

移除后注册表保留记录（含移除原因），但不再提供下载或分发。

---

### 六、Extension 版本规则

| 版本变更 | 触发条件 | 需重新认证 |
|---------|---------|-----------|
| Major | 功能范围变更、TPI 接口变更 | ✅ 必须 |
| Minor | 功能增强、新增 C1 知识 | ❌ 声明兼容 |
| Patch | Bug 修复、安全更新 | ❌ 声明兼容 |
| 废弃 | 生命周期终结 | 标记废弃 |

---

### 七、Extension 治理原则

**EG-001: Extension Extends Capability, Not Identity**

Extension 扩展的是能力范围，不是人格身份。人格身份的唯一来源是 Core。

**禁止：**
- ❌ 修改 Personality Constitution
- ❌ 修改 Invariant
- ❌ 获取决策权

**EG-002: Governance Cannot Redefine Core**

治理机构：
- 可以：管理 Extension、审核兼容性、管理生命周期
- 不能：解释 Core 新含义、修改 Core 原则、创建新的人格版本

即：Governance governs Extensions，NOT Governance governs Core。

**EG-003: Registry Is Record, Not Authority**

Registry 是 Audit Record，不是 Power Center。

Registry 可以：
- 记录认证状态
- 记录版本
- 记录历史

不能：
- 授权改变 Core
- 覆盖 ADR
- 修改认证规则

**EG-004: Registry Not Storage Layer**

Registry 不保存：
- Persona State
- Memory
- Identity Data

避免 Registry 变成第二人格数据库。注册表只记录 Extension 元数据和认证状态，Extension 代码由维护者自行托管。

**EG-005: Certification and Registry Separation**

认证：判断兼容。注册：记录结果。二者分离。

认证通过是注册的前提条件，但认证机构不管理注册表。认证机构负责检查，注册表维护者负责收录。

**EG-006: 废弃不等于删除**

废弃的 Extension 在注册表中保留记录（含废弃原因和替代推荐），便于已有用户迁移。

**EG-007: 安全事件强制报告**

Extension 维护者发现安全漏洞后 14 天内必须向注册表提交报告。超期未报告视为违反认证条件。

**EG-008: Sandbox Isolation**

Experimental Extension 不得：
- 读取真实长期 Memory
- 修改 Runtime State
- 影响其他 Extension

实验环境与生产运行时严格隔离。

---

### 八、Conflict Resolution（冲突解决）

当多个 Extension 之间存在冲突，或 Extension 与 Core/Certification 之间存在冲突时，按以下优先级裁决：

```
P0  Core
    ▲
P1  Human Sovereignty（用户主权）
    ▲
P2  Safety
    ▲
P3  Certification（认证标准）
    ▲
P4  Extension Governance
    ▲
P5  Individual Extension
```

**规则：**
- Human Sovereignty 高于 Safety：用户决定优先于系统安全判断
- Certification 高于 Extension Governance：认证标准不能被治理流程覆盖
- 任何 Extension 之间的冲突，以优先级高的为准
- 优先级相同的 Extension 冲突，由 Human（用户）最终裁决

---

## 文件体系

本 ADR 对应的详细规范文件：

| 文件 | 内容 |
|------|------|
| `docs/07_ecosystem/EXTENSION_GOVERNANCE_STANDARD_v1.0.md` | Extension 治理标准全文 |
| `docs/07_ecosystem/EXTENSION_LIFECYCLE_PROTOCOL.md` | 生命周期各阶段操作协议 |
| `docs/07_ecosystem/EXTENSION_REVIEW_MATRIX.md` | 审查矩阵：各阶段检查项清单 |

---

## 原因

1. **生态需要淘汰机制：** 没有生命周期的生态最终会变成"死 Extension 博物馆"
2. **分类降低准入门槛：** C1 Knowledge 走简化路径，鼓励知识类 Extension 繁荣
3. **注册与认证分离防止权力集中：** 认证机构不控制注册表，注册表不执行认证
4. **废弃期保护已有用户：** 12 个月废弃期给迁移时间，不搞突然死亡

---

## 影响

### 正面
- 生态有明确的进入和退出机制
- Extension 质量有持续保障
- 用户可识别活跃 / 废弃 / 推荐 Extension

### 负面
- 维护注册表需要运营成本
- 废弃期 12 个月可能过长（安全违规例外）

---

## 后续决策依赖

- 注册表技术实现决策（中心化 vs 去中心化）
- 注册表维护者任命方式
- 安全事件应急响应流程细化

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — Accept after 5 supplements

### Review 结果

| # | 检查维度 | 状态 | 补充 |
|---|---------|------|------|
| 1 | Extension 隐性人格控制权 | ✅ 已封闭（EG-002） | Review-001 |
| 2 | EG-001 定位确认 | ✅ 正确，保留 | Review-002 |
| 3 | 沙盒隔离 | ✅ 已补充（EG-008） | Review-003 |
| 4 | Registry 权力约束 | ✅ 已补充（EG-003） | Review-004 |
| 5 | 冲突解决优先级 | ✅ 已补充（Human > Safety） | Review-005 |

### 补充项（已纳入）

| 编号 | 新增 | 来源 | 理由 |
|------|------|------|------|
| EG-001 | Extension Extends Capability, Not Identity | Review-002 | 明确 Extension 的根本定位 |
| EG-002 | Extension Governance Cannot Redefine Core | Review-001 | 防止治理体系变成事实 Core 控制者 |
| EG-003 | Registry Is Record, Not Authority | Review-004 | 防止 Registry 成为权力中心 |
| EG-008 | Sandbox Isolation | Review-003 | 实验能力不污染人格 |
| §八 | Conflict Resolution | Review-005 | Human Sovereignty > Safety |
