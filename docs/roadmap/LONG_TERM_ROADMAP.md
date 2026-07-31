# Long-Term Roadmap

## 唐先生项目 · 长期路线图

Version: v0.1
定位：从"人格运行基础设施 + 首个验证产品"出发，分阶段走向"人格模块生态"。

---

## 愿景回顾

唐先生项目要建立的是：**一个让 AI 人格可以被定义、验证、运行和应用的基础设施。**
未来不是制造更多聊天机器人，而是让不同领域的人格智能，像软件模块一样被可靠创建。

本路线图的硬约束：**每个阶段都不得修改人格核心。** 产品层、表达层可以扩展，
人格层保持稳定。

---

## Phase 1 — Personality Runtime Ecosystem Foundation / 人格运行生态基础（当前 → 近期）

**目标：** 证明 **一个 Runtime 可以承载多个稳定人格**，为"人格模块生态"打好地基。

> 本阶段的重点不是"优化 Tang OS"，而是**生态的基础证明**：
> 同一套运行时，能否稳定承载多个不同的人格，且互不污染、可验证、可替换。

**关键交付：**
- 多人格并行验证：让多个独立人格模块在同一运行时上稳定运行、隔离成立
- 人格模块开发工具雏形：模块创作、校验、打包的工作流
- 验证体系深化：更多对抗式边界测试、跨提供方回归
- 多产品验证：在 xiaotang 之外再验证一个应用形态，证明"应用不拥有人格"
- 文档与治理落地：本套技术资料体系成为对外口径

**护栏：** 运行时冻结期间只做 bug fix；新能力走 ADR。

---

## Phase 2 — 多模态表达

**目标：** 扩展"怎么说"，不改变"做什么"。

**关键交付：**
- Expression Layer Expansion：
  - **Voice** —— 语音表达
  - **Avatar** —— 虚拟形象表达
  - **Real-time interaction** —— 实时交互

**核心注意：**
- 全部属于表达层扩展
- **不修改人格核心**
- 同一人格模块在文本 / 语音 / 形象间保持身份一致

---

## Phase 3 — 人格市场

**目标：** 让"人格模块"成为可流通的资产。

**关键交付：**
- **Personality Marketplace**（人格市场）
- 类似 App Store，但交易的是**人格模块**
- 配套：模块打包格式、版本管理、验证标准、发布与许可机制
- 开发者生态：允许第三方创作、发布、替换人格

**前提：** 模块标准（tang-ta）与验证体系必须先成熟 —— 市场信任建立在
"模块是可验证的"之上。

---

## Phase 4 — 企业应用

**目标：** 人格运行时进入企业场景。

**关键交付：**
- **Enterprise Personality Runtime**（企业人格运行时）
- 典型场景：
  - 企业助手
  - 教育 AI
  - 客户服务

**注意：** 每个企业应用仍是应用层消费人格，不改变人格层架构。

---

## 阶段推进原则

1. **每一阶段结束都可独立交付**，不存在"为了未来牺牲现在"。
2. **人格核心稳定优先于功能丰富** —— 宁可少加功能，不碰人格层。
3. **验证先于发布** —— 任何阶段的人格相关改动都过验证套件。

---

## English Summary

The Tang Project's long-term goal is infrastructure where AI personality can be defined, validated, run, and applied like software. The hard constraint across all phases: **never modify the personality core**; expand expression and applications, keep the personality layer stable.

- **Phase 1 — Personality Runtime Ecosystem Foundation.** Prove that **one runtime can reliably host multiple stable personalities** — isolated, verifiable, replaceable — and build the groundwork for the personality module ecosystem. Not "optimizing Tang OS"; it is the ecosystem's foundational proof.
- **Phase 2 — Multimodal expression.** Expand the Expression Layer: voice, avatar, real-time interaction. No personality-core changes; identity stays consistent across modalities.
- **Phase 3 — Personality Marketplace.** An App-Store-like marketplace where personality *modules* are the traded asset. Prerequisite: mature tang-ta standard and validation so modules are trustworthy.
- **Phase 4 — Enterprise Personality Runtime.** Enterprise assistants, education AI, customer service — each consuming personalities at the application layer without changing the personality architecture.

Advancement principles: each phase is independently deliverable; personality-core stability outranks feature richness; validation precedes release.
