# ADR-0034: Tang OS Ecosystem Boundary

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer
**优先级：** Higher than Extension Protocol
**影响范围：** Tang OS 全域 — Core 定义、Extension 准入、Host 关系、商业策略、Phase 11+ 所有阶段
**前序资产：** ADR-0001~0033, I-1~I-30, Phase 9 Standard v1.0, Phase 10 Vertical Validation

## 背景

Tang OS 已完成标准定义（Phase 9）和架构证明（Phase 10），当前处于 Phase 11 起点。

此时面临的历史常见风险是：

> 一个成功的人格系统，被不断加入功能，最后变成普通 AI 助手。

Project Snapshot 中提出的"结构审计"建议已被驳回。原因：

1. Context Overflow 刚修复，不应重新进入全量审查循环
2. 已冻结资产默认可信（ADR-0033），无需二次验证
3. 现在需要的是**前方边界**，不是**后方清理**

### 现有定位判断

Three possible paths evaluated:

| 路线 | 特征 | 当前资产匹配度 |
|------|------|--------------|
| A — 产品路线 | Tang Companion App，快商业化 | ❌ Core 设计为 Host 无关，产品化反而限制 |
| B — 平台路线 | Core + Interface + Host，第三方实现 | ✅ 架构天然支持 |
| C — 标准路线 | "可信人格运行标准"，类似 USB/Bluetooth | ✅ TPI、Extension Protocol、Blind Validation 全部指向此方向 |

**结论：** Tang OS 不适合 A。天然定位为 **B + C** — 人格运行平台 + 标准体系。

---

## 决策

### 一、Tang OS 最终定位

> Tang OS 是一个**人格运行平台标准**。不是产品，不是框架，不是 SDK。

- Core 定义人格操作系统的基础接口和不变性
- Extension 在 Core 之上扩展领域能力，但不修改 Core
- Host 是 Core 的运行载体，但不定义人格
- Certification 保证实现与标准的一致

### 二、资产三级分类（正式冻结）

```
TANG OS ASSETS

CORE（不可修改）
├── Identity Constitution
├── I-1 ~ I-30
├── Decision Model
├── Safety Model
├── Memory Boundary
└── TPI（Personality Interface）

性质：修改需新 ADR 明确 Supersede 旧决策，且需 Blind Validation 证明不破坏兼容性


EXTENSION（必须走准入）
├── Elder Care
├── Vehicle
├── Wearable
├── Education
├── Medical
└── 未来新增

性质：每次新增必须走完整准入流程。不得绕过。


EXPERIMENT（独立沙盒）
├── 未验证能力
├── 新交互范式
├── 新模型适配
└── 研究方向

性质：不进入 Core，不进入 Extension 注册表。实验完成后经准入评估再升级。
```

### 三、八条生态边界（不可侵犯）

以下八条构成 Tang OS 生态系统的宪法级约束，任何 Phase、任何商业需求、任何技术决策不得违反：

**E-2: Core 不追求功能最大化**

Core 的价值在于稳定和最小完备，不在于功能多少。新增功能的首选路径是 Extension，不是 Core。

**E-3: Extension 不污染人格底座**

Extension 运行在 TPI 之上，可以读取人格状态，但不得修改 Identity Constitution、Decision Model、Safety Model。人格底座是只读的。

**E-4: Host 不定义人格**

同一人格运行在不同 Host 上应保持一致。Host 可以限制表达能力（如无屏幕设备没有视觉输出），但不得改变人格的判断、价值观、决策逻辑。

**E-5: 商业需求不能修改 Invariant**

I-1~I-30 是 Tang OS 的公理层。任何商业需求——收入目标、合作伙伴要求、市场份额——都不能作为修改 Invariant 的理由。需要修改 Invariant 的，等同于创建新系统，不得命名为 Tang OS。

**E-6: 验证标准优先于开发速度**

未经验证的功能视为不存在。通过验证但未通过 Blind Validation 的功能不得进入 Extension 注册表。

**E-7: Core Authority Independence**

任何 Extension、Host、商业合作方、用户组织，均不得获得修改 Core Invariant 的权力。Core 的权威独立于任何外部利益相关者。商业压力不得成为修改人格原则的理由。

**E-8: Identity Version Integrity**

任何修改 Identity Constitution、Invariant、Decision Model 的行为，必须产生新的 Major Version。

```
Tang OS v1.x
    修改 I-12
    = Tang OS v2.0
```

禁止以 Minor Version 或 Patch 名义改变人格核心。v1.1 与 v1.0 必须共享同一人格基线；若人格基线改变，即为 v2.0。

**E-9: Compatible Fork Rule**

允许：
- Extension 开发
- Host Adaptation
- Implementation Variation（不同实现方式）

不允许：
- 修改 Core 后继续使用 "Tang OS" 名称

原则：可以有自己的发行版，但不能改内核哲学后仍声称官方 Tang OS。分叉版本必须在命名中明确区分。

### 四、新能力准入流程（Phase 11 起强制执行）

任何新能力进入 Tang OS 生态的路径：

```
Proposal
   ↓
ADR（决策记录）
   ↓
Invariant Check（必须通过全部 I-1~I-30）
   ↓
Interface Impact Check（是否影响 TPI？）
   ↓
Scenario Test（覆盖最少 3 个场景）
   ↓
Blind Validation（至少一个 Blind Host 验证）
   ↓
Approval（Founder 最终决策）
   ↓
Implementation
```

禁止行为：
- 跳过任一环节直接进入 Implementation
- 以"实验"为名绕过准入在 Core 中加功能
- 将未完成准入的功能作为"特性"宣传

---

## 原因

1. **防止人格漂移：** 大多数 AI 人格系统失败的原因不是技术不够，而是功能膨胀稀释了人格一致性
2. **保护已验证资产：** Phase 10 已验证 Core 在 4 种完全不同的 Host 上保持人格一致——这一优势不应被无边界扩展破坏
3. **商业可持续性：** B + C 路线短期不见效，但长期护城河远深于 A。平台+标准一旦建立，迁移成本使竞争无法追赶
4. **符合已有设计：** TPI、Extension Protocol、Blind Validation 这些已冻结资产天然指向生态思维，本 ADR 只是将其正式化

---

## 影响

### 正面
- Tang OS Core 获得免疫——不会被商业压力或功能需求侵蚀
- 所有利益相关者（开发者、Host 厂商、认证机构）有明确的游戏规则
- 避免"功能膨胀——人格漂移——重新设计"的死亡循环
- Phase 11 的后续阶段有清晰方向

### 负面
- 拒绝商业需求需要纪律——短期内可能失去某些合作机会
- Extension 准入流程增加开发周期
- 需要维护 Certification 体系和测试套件

---

## Phase 11 路线图

```
Phase 11-A  Ecosystem Boundary Standard  ← 本 ADR（Direction Lock）
      ↓
Phase 11-B  Certification Standard（定义认证级别、测试套件、合规标记）
      ↓
Phase 11-C  Extension Governance（正式化现有 Extension 分类、注册表、生命周期管理）
      ↓
Phase 11-D  Ecosystem Documentation（面向第三方的开发者文档、集成指南、参考实现）
```

不写代码。不扩能力。先把"未来十年不会跑偏"的边界钉死。

---

## 后续决策依赖

- ADR-0035: Certification Standard — 定义认证级别、测试套件、合规标记
- ADR-0036: Extension Governance — Extension 生命周期管理、版本策略、废弃流程
- Phase 11-D 文档计划的详细 scope 决策

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — Recommend Accept with Minor Reinforcement

### 评价

| 条款 | 评价 |
|------|------|
| E-2 Core 不追求功能最大化 | ✅ 必须 |
| E-3 Extension 不污染人格 | ✅ 核心 |
| E-4 Host 不定义人格 | ✅ 非常重要 |
| E-5 商业不能修改 Invariant | ✅ 必须 |
| E-6 验证优先开发 | ✅ 差异化核心 |
| E-7 Core Authority Independence | ✅ 审查后补充 |
| E-8 Identity Version Integrity | ✅ 审查后补充 |
| E-9 Compatible Fork Rule | ✅ 审查后补充 |

### 冲突数
0 — 与现有 ADR/Invariant 无冲突

### 补充边界（已纳入）
- **E-7:** 防止 Core 变成可购买规则
- **E-8:** 防止以版本号掩盖人格改变
- **E-9:** 标准路线的 Fork 治理

### 归档建议
此 ADR 属于 **Governance Layer / 最高优先级**，不应视为普通设计决策。
在 PROJECT_STATE_SNAPSHOT.md 中应标记为：

> Ecosystem Governance Foundation Established
