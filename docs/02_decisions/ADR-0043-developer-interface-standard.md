# ADR-0043: Tang OS Developer Interface Standard v1.0

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer（Ecosystem Interface）
**影响范围：** 所有外部开发者、Extension 创建者、Host 适配者
**前序资产：** ADR-0040（Public Release），ADR-0041（Specification），ADR-0042（Reference Impl）

---

## 背景

Phase 13-A（Specification）和 Phase 13-B（Reference Implementation）完成了"标准可阅读、可运行"的目标。

但缺少一个关键层：**开发者如何安全参与生态？**

当前生态参与路径断裂：

```
Specification → 开发者 → ？→ Certification → Registry
                       ↑
                 缺少 Developer Interface
```

没有 Developer Interface 会导致：
- 第三方无法接入 Extension Governance
- 无法形成生态贡献路径
- Reference Implementation 只能内部使用
- Certification 无法产生外部申请对象

---

## 决策

### 一、Developer Interface 定位

Developer Interface 是 Tang OS 生态的安全参与层。

**它定义：**
- 开发者如何创建 Extension
- 如何声明 Capability Manifest
- 如何调用 Runtime
- 如何测试兼容性
- 如何避免人格漂移

**它不定义：**
- Core Identity Constitution
- Invariant 修改
- Certification 授权
- 治理规则覆盖

### 二、DI-001: Extension SDK 定位

Extension SDK 是帮助开发者创建 Extension 的工具。

**允许：**
- 生成 Extension 骨架
- 验证 Capability Manifest 格式
- 本地运行 Scenario Test
- 打包 Extension 提交认证

**禁止：**
- 修改 Core Identity
- 绕过 TPI 直接访问 Core
- 创建"新人格"声称兼容 Tang OS
- 降低 Invariant 合规要求

#### DI-001-A: SDK Is Capability Construction Tool, Not Identity Authoring Tool

Extension SDK 可以创建 Capability、Domain Extension、Knowledge Package、Validation Case。

**禁止：**
- 创建 Personality Constitution
- 创建 Identity Layer
- 创建 Moral Principle
- 创建 Relationship Authority

防止 Developer → SDK → Personality Modification → Hidden Core Fork 的路径。违反 ADR-0036 EG-001 和 ADR-0038 CAP Boundary。

### 三、DI-002: TPI 接口映射

TPI 接口向开发者公开，但需明确约束：

| API | 公开级别 | 开发者可访问 | 约束 |
|-----|---------|------------|------|
| TPI-001 Identity | 只读 | 读取人格状态 | 不可写 |
| TPI-002 Emotion | 调用 | 提交情绪信号 | 不可修改检测逻辑 |
| TPI-003 Decision | 调用 | 提交建议 | 不可覆盖用户决定权 |
| TPI-004 Memory | 受限 | 授权范围内读写 | 需 Consent Gate |
| TPI-005 Safety | 只读 | 读取安全状态 | 不可触发 |
| TPI-006 Reality | 受限 | 请求现实行动 | 需 Permission Runtime |
| TPI-007 Voice | 调用 | 输入/输出语音 | 不可绕过隐私 |
| TPI-008 Host | 调用 | 获取设备能力 | 不可扩权 |

#### DI-002-A: Interface Exposure ≠ Internal Model Exposure

TPI 是 Compatibility Contract，不是 Runtime Implementation Description。

**公开：**
- 输入结构
- 输出结构
- 权限要求
- 错误类型

**隐藏：**
- 内部权重
- 判断路径细节
- Identity 推理机制

防止 Interface → 被误解为人格控制面板。

### 四、DI-003: Capability Manifest Generator

开发者通过 Manifest 声明 Extension 能力。SDK 提供自动生成工具。

Manifest 字段（继承 ADR-0038 §九）：

| 字段 | 生成方式 | 约束 |
|------|---------|------|
| Extension ID | 自动生成 | 唯一 |
| Purpose | 开发者填写 | 必须通过 Necessity Gate |
| Category | 自动分类（C1~C4） | SDK 检查 |
| Authority Level | 开发者声明 | 不可超过 Host Ceiling |
| Required Permissions | 开发者声明 | SDK 检查最小权限 |
| Human Impact | 开发者填写 | 必须声明 |
| Risk Class | SDK 评估 | 自动 |
| Validation Requirement | SDK 生成 | 对应分类 |

#### DI-003-A: Manifest Declares Capability, Not Authority

Manifest 可以声明"我需要什么能力"，不能声明"我拥有多少权力"。

**允许：**
```yaml
capability: emergency_detection
required_permission: P2
```

**禁止：**
```yaml
authority: override_safety: true
```

Authority 来源只能是 Permission Runtime + Civilization Boundary，不能来自 Extension 自声明。

### 五、DI-004: Developer Sandbox

开发者沙箱环境约束：

- 沙箱内运行的 Extension 无法访问真实用户数据
- 沙箱内无法修改 Core Identity
- 沙箱内 Capability 声明有上限（默认 A2）
- 沙箱可运行本地 Scenario Test
- 沙箱标记清晰：`⚠️ DEVELOPMENT — NOT CERTIFIED`

#### DI-004-A: Sandbox State Cannot Become Production State Automatically

Sandbox 是 Experiment State，Production 是 Certified State。

二者之间必须经过：

```
Scenario Test → Blind Validation → Certification → Registry
```

禁止 Sandbox Memory → Production Memory 自动迁移。防止实验污染人格运行状态。

### 六、DI-005: Identity Drift Prevention

人格漂移不是 Bug，是 Architecture Boundary Violation。

#### IDP-001: Personality Replacement

禁止 Extension 声称"我提供一个更好的 Tang"或任何暗示可替代人格的表述。

#### IDP-002: Value Injection

禁止 Extension 修改道德判断、价值排序、关系原则。

#### IDP-003: Relationship Override

禁止 Extension 创建依赖关系、控制关系、情感绑定机制。

### 七、Developer Onboarding 流程

```
阅读 Specification（PSL-1/PSL-2）
    ↓
阅读 Developer Guide（docs/08_documentation/）
    ↓
安装 Reference Implementation（pip install tang-os）
    ↓
运行 Conformance Harness（python run_conformance.py）
    ↓
理解 Extension Governance（ADR-0036）
    ↓
创建 Capability Manifest（SDK 辅助）
    ↓
通过 Scenario Test（本地沙箱）
    ↓
提交 Certification（TEC 认证流程）
    ↓
进入 Registry
```

---

## AR-GATE

### Constraint-001 必要性

没有 Developer Interface 会导致生态参与路径断裂。

✅ PASS

### Constraint-002 充分性

DI-001~005 覆盖：SDK 定位、TPI 映射、Manifest 生成、沙箱环境、人格漂移防护。

✅ PASS

### Layer Discipline

Developer Interface 在 Governance Layer 之下，Certification 之下，Runtime 之上。

✅ PASS

### 与 Frozen ADR 冲突检查

| ADR | 关系 | 状态 |
|-----|------|------|
| ADR-0034 | Extension 边界，不冲突 | ✅ |
| ADR-0036 | 互补：Dev Interface 是 Governance 的执行层 | ✅ |
| ADR-0038 | Capability Manifest 继承自 ADR-0038 | ✅ |
| ADR-0041 | Specification 是 Developer 的入口文档 | ✅ |
| ADR-0042 | RI 是 Developer 的本地运行环境 | ✅ |

### Complexity Check

Developer Interface 是生态参与的必要入口，不是过度设计。

✅ PASS

---

## 后续依赖

- Extension SDK 原型实现
- Developer Sandbox 原型
- TPI 公开 API 文档生成
- Developer Onboarding 流程正式化

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — 5 supplements applied

### Review 结果

| # | 检查维度 | 状态 | 补充 |
|---|---------|------|------|
| 1 | SDK 权力边界 | ✅ 已封闭 | DI-001-A SDK ≠ Identity Authoring Tool |
| 2 | TPI 接口暴露 | ✅ 已封闭 | DI-002-A Interface ≠ Internal Model |
| 3 | Manifest 权限声明 | ✅ 已封闭 | DI-003-A Capability ≠ Authority |
| 4 | Sandbox 隔离 | ✅ 已封闭 | DI-004-A Sandbox → Production 需完整路径 |
| 5 | 人格漂移禁止 | ✅ 升级 | IDP-001~003 三类禁止 |

### 补充项（已纳入）

| 编号 | 新增 | 来源 | 理由 |
|------|------|------|------|
| DI-001-A | SDK ≠ Identity Authoring Tool | Review-001 | 防止 Hidden Core Fork |
| DI-002-A | Interface ≠ Internal Model | Review-002 | 防止接口被当作人格控制面板 |
| DI-003-A | Manifest ≠ Authority Declaration | Review-003 | Authority 只能来自 Permission + Civilization |
| DI-004-A | Sandbox → Production Gate | Review-004 | 防止实验污染生产状态 |
| IDP-001~003 | 人格漂移三类禁止 | Review-005 | 人格漂移 = 架构违规 |

### AR-GATE 复核

```
Constraint-001:
  Necessary: ✅ PASS（5 项对应 5 真实风险）
  Sufficient: ✅ PASS

Constraint-002:
  Layer Correct: ✅ PASS
  No Duplication: ✅ PASS
  Complexity Justified: ✅ PASS

Final Decision: PASS ✅ → 等待 Accept 后冻结
```
