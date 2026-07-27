# ADR-0037: Ecosystem Documentation Standard

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Documentation Layer（Phase 11-D）
**影响范围：** Tang OS 所有对外文档、开发者入口、认证说明
**前序资产：** ADR-0034 / 0035 / 0036（Governance Layer 已闭环）

---

## 背景

Tang OS Governance Layer（ADR-0034/0035/0036）已完成闭环。但存在一个重要缺口：

> 外部世界如何准确理解 Tang OS？

文档层是 Tang OS 的对外认知入口。如果出现偏差，会产生两个风险：

1. **外部误解定位** — 被理解成 AI 产品、机器人系统、Agent Framework 或人格模型 SDK
2. **文档反向污染治理层** — 外部解释逐渐变成"事实标准"，Marketing 语言进入规范

**核心原则：** Documentation Must Reflect Frozen State, Not Define Frozen State.

---

## 决策

### 一、文档层定位

Tang OS 文档层是 Frozen State 的外部表达，不是新规范的来源。

- 文档解释 ADR、Standard、Validation 的产出
- 文档不创造新的架构决策
- 文档不引入 Marketing 语言
- 文档不替代 Governance Layer

### 二、Documentation Invariants（DI-001~003）

以下三条原则约束所有 Tang OS 对外文档，任何文档不得违反：

**DI-001: Documentation Cannot Modify Core Meaning.**

文档只能解释 Core，不能创造新的解释。任何文档中出现的定义，如果与 ADR 或 Standard 不一致，以 ADR/Standard 为准。

**DI-002: Documentation Source Authority.**

文档的信息来源只能来自：
- ADR（决策记录）
- Standard（标准规范）
- Validation（验证报告）

禁止来源：
- Marketing 材料
- 外部提案
- 临时讨论

**DI-003: Terminology Stability.**

建立 Tang OS Vocabulary，统一术语。禁止同一概念出现多个叫法。

统一术语表（必须使用）：
| 标准术语 | 禁止用词 |
|---------|---------|
| Personality Runtime | 人格引擎、AI人格系统 |
| Tang OS Core | 核心、内核（单独使用时混淆） |
| Extension | 插件、模块、功能包 |
| Host | 载体、设备端、运行环境 |
| Certification | 认证、资质验证 |
| Governance | 治理、管理规则 |

### 三、文档内容标准

各文档必须包含以下声明：

#### DOC-001-POSITION（Overview 定位声明）

```
Tang OS is a personality runtime standard.

It defines how a consistent personality can exist across different Hosts.

It does not define a specific product form.
```

防止：机器人 → Tang OS 是机器人系统；手机 → Tang OS 是 App；耳机 → Tang OS 是硬件人格芯片。

#### Architecture Principle（架构原则声明）

```
Host is replaceable.
Extension is replaceable.
Core is persistent.
```

可变（Extension / Host）与不变（Core）的明确区分，是 Tang OS 最大技术差异之一。

#### Developer Boundary Statement（开发者边界声明）

```
Developers create capabilities around Tang OS.
They do not create new identities under Tang OS.
```

防止生态出现 Tang OS Medical Edition / Enterprise Edition / Genius Edition 等人格分叉。

#### Certification Scope Declaration（认证范围声明）

认证验证的是 Compatibility with Tang OS Core，不是 AI 质量、智能程度或用户满意度。认证是一致性验证，不是排名。

#### Human Interaction Flow（Ecosystem Map 行为流）

```
Human
  ↓
Interaction
  ↓
Host
  ↓
Reality Interface
  ↓
Personality Interface
  ↓
Tang Core
```

强调 Tang OS 的最大特点：人在现实世界中的关系连续性。

---

## 原因

1. **防止定位漂移：** 无定位声明则外部自行定义，最终背离原始设计
2. **防止术语混乱：** 多名称 = 多理解 = 多边界模糊
3. **防止文档替代治理：** 文档只能解释已冻结状态，不创造新规范
4. **防止开发者越界：** 明确的 Developer Boundary 保护 Core 不被 Extension 无意侵蚀

---

## 影响

### 正面
- 所有对外文档有统一的定位、术语、边界
- 新开发者加入生态时不会误读 Tang OS
- 文档层成为治理层的放大器，而不是替代品
- Marketing 与 Engineering 使用同一套语言

### 负面
- 术语约束增加文档写作成本
- 需要维护 Term Glossary 和文档审计流程

---

## 文件变更

| 文件 | 变更 |
|------|------|
| `docs/08_documentation/TANG_OS_OVERVIEW_STANDARD_v1.0.md` | + DOC-001-POSITION |
| `docs/08_documentation/TANG_OS_ARCHITECTURE_GUIDE_v1.0.md` | + Architecture Principle |
| `docs/08_documentation/TANG_OS_DEVELOPER_GUIDE_v1.0.md` | + Developer Boundary Statement |
| `docs/08_documentation/TANG_OS_CERTIFICATION_GUIDE_v1.0.md` | + Certification Scope Declaration |
| `docs/08_documentation/TANG_OS_ECOSYSTEM_MAP_v1.0.md` | + Human Interaction Flow |
| `docs/08_documentation/` | + DI-001~003 全局约束 |

---

## 后续依赖

- Tang OS Term Glossary 的独立维护
- 文档审计流程的建立（谁审核、多久一次）
- 多语言文档的术语一致性管理

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS WITH MINOR AMENDMENTS

### Review 结果

| 项目 | 状态 | 补充 |
|------|------|------|
| Overview 定位 | ✅ | + DOC-001-POSITION |
| Architecture 边界 | ✅ | + Architecture Principle |
| Developer 边界 | ⚠️ | + Developer Boundary Statement |
| Certification 中立性 | ⚠️ | + Certification Scope |
| Ecosystem Map | ⚠️ | + Human Interaction Flow |
| Documentation Governance | ⚠️ | + DI-001~003 |
| Core 一致性 | ✅ | — |

### 补充项（已纳入）

| 编号 | 内容 | 来源 |
|------|------|------|
| DI-001 | Documentation Cannot Modify Core Meaning | Review-006 |
| DI-002 | Documentation Source Authority | Review-006 |
| DI-003 | Terminology Stability | Review-006 |
| DOC-001-POSITION | Tang OS 定位声明 | Review-001 |
| Architecture Principle | Host/Extension 可变，Core 持久 | Review-002 |
| Developer Boundary | 开发者创造能力，不创造身份 | Review-003 |
| Certification Scope | 认证验证一致性，不是排名 | Review-004 |
| Human Flow | 人在现实中的关系连续性 | Review-005 |
