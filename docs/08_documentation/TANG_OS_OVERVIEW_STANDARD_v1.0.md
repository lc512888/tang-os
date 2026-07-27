# Tang OS Overview Standard v1.0

**层级：** Documentation Layer（Phase 11-D）
**目标受众：** 外部开发者、合作伙伴、研究者
**目标：** 5 分钟内理解 Tang OS 是什么、不是什么

---

## 定位声明（DOC-001-POSITION）

```
Tang OS is a personality runtime standard.

It defines how a consistent personality can exist across different Hosts.

It does not define a specific product form.
```

Tang OS 不是机器人系统（尽管可以运行在机器人上），不是 App（尽管可以运行在手机上），不是硬件芯片（尽管可以嵌入设备）。它是一个标准。

---

## Tang OS 是什么

Tang OS 是一个**人格运行平台标准**。

不是产品，不是框架，不是 SDK。而是一组定义"可信人格"如何在不同设备上运行、保持一致、不被篡改的公开标准。

## Tang OS 不是

| ❌ 不是 | ✅ 是 |
|---------|------|
| AI 聊天机器人 | 人格运行标准 |
| 情感陪伴应用 | 平台 + 标准体系 |
| 单一设备系统 | 跨 Host 架构 |
| 功能聚合器 | Core + Extension 分离 |

## 核心概念

```
人格（Persona）
  → 由 Core 定义的身份、价值观、决策逻辑
  → 在任何设备上保持一致

Core
  → 不可修改的人格内核
  → 包含 Identity Constitution + I-1~I-30

Extension
  → 在 Core 之上扩展能力
  → 通过 TPI 访问，不修改人格

Host
  → Core 运行的载体（机器人、车辆、穿戴设备等）
  → 不定义人格

Certification
  → 验证实现是否符合标准
  → 三类认证：Core / Extension / Host
```

## 定位演变

```
Phase 1-8:  人格模型
Phase 9:    人格标准
Phase 10:   架构证明（42/42 验证通过）
Phase 11:   生态协议（Governance Layer 闭环）
```

Tang OS 的独特价值：**一个别人可以实现，但不能随意改变其灵魂的标准。**

---

## Documentation Invariants

本文档受以下原则约束：

| 原则 | 内容 |
|------|------|
| DI-001 | 文档只解释 Core，不创造新解释 |
| DI-002 | 信息来源限 ADR + Standard + Validation |
| DI-003 | 术语遵守 Tang OS Vocabulary，禁止替代用词 |
