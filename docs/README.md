# Tang Project Documentation

## 唐先生项目 · 文档导航首页

Version: v0.1

---

## What is Tang Project?

唐先生项目探索的是**人格运行基础设施（Personality Runtime Infrastructure）**——
让 AI 人格可以被定义、验证、运行和应用。它不是一个聊天应用；xiaotang 只是
第一个基于它的验证产品。

**核心论点：** 人格不是提示词，而是可加载、可验证、可运行的软件能力。

---

## 三个入口

```
访问者
 ├── 想了解项目价值  → Architecture Overview（架构总览）
 ├── 想研究技术      → Whitepaper（白皮书）
 └── 想运行代码      → Developer Guide（开发者指南）
```

| 入口 | 文档 | 谁看 |
|------|------|------|
| **项目价值** | [architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md](architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md) | 用户 / 合作方 / 任何人（10 分钟理解） |
| **技术研究** | [research/](research/)（白皮书 / 竞争分析 / 定位） | 技术研究者 / 开发者社区 / 投资 |
| **运行代码** | [CONTRIBUTING.md](CONTRIBUTING.md) + 项目根 README | 开发者 |

---

## 文档地图（对外）

### 认知层（为什么）

| 文档 | 位置 | 回答 |
|------|------|------|
| 人格运行时白皮书 | `research/en-US/` `research/zh-CN/` | 为什么未来 AI 需要人格运行时 |
| 竞争架构分析 | `research/en-US/` `research/zh-CN/` | 别人怎么建人格，我们站在哪 |
| 架构定位 | `research/en-US/` `research/zh-CN/` | 我们是谁、为什么这么建、往哪走 |

### 架构层（是什么）

| 文档 | 位置 |
|------|------|
| 系统架构总览 | `architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md` |

### 治理层（边界）

| 文档 | 位置 |
|------|------|
| 架构防腐层 | `governance/ARCHITECTURE_GUARDRAILS.md` |
| 项目级开发者指南 | `CONTRIBUTING.md` |
| Tang OS 核心贡献标准 | 项目根 `CONTRIBUTING.md` |
| 决策记录索引 | `decisions/ADR_INDEX.md` |

### 规划层（往哪走）

| 文档 | 位置 |
|------|------|
| 长期路线图 | `roadmap/LONG_TERM_ROADMAP.md` |

---

## 阅读建议

- **第一次接触：** 架构总览 → 白皮书
- **参与开发：** 架构总览 → 开发者指南 → 架构防腐层
- **研究定位：** 架构定位 → 竞争分析 → 白皮书

---

## 内部文档结构（项目治理）

> 以下为项目**内部**设计文档索引与协作规则。AI 开始工作前，**必须**先读
> `PROJECT_STATE_SNAPSHOT.md`（唯一入口，ADR-0033）。

### 00_governance/ — 项目法律（极少改动，AI 不得擅自修改）

| 文件 | 说明 |
|---|---|
| `COLLABORATION_PROTOCOL.md` | 三方协作规则（你/ChatGPT/Claude Code） |
| `GLOSSARY.md` | 术语表 —— 统一词汇，禁用词列表 |
| `NAMING.md` | 文件/目录/代码命名规范 |
| `REPOSITORY_RULES.md` | Git、文档、代码、ADR 行为规则 |

### 01_vision/ — 愿景层（极少改动）

| 文件 | 说明 |
|---|---|
| `VISION.md` | 项目愿景 |
| `FIRST_PRINCIPLES.md` | 第一性原理 |
| `PRODUCT_PHILOSOPHY.md` | 产品哲学 |
| `ROADMAP.md` | 路线图 + MVP 定义 |

### 02_decisions/ — 决策层（持续积累）

ADR 格式。状态：Draft → Accepted / Deprecated / Superseded。
对外索引见 `decisions/ADR_INDEX.md`。

### 03_specs/ — 规范层

`architecture/`、`character/`、`memory/` 子目录。

### 04_characters/ — 角色圣经 / 05_reviews/ — 设计评审

---

## 协作规则

1. **任何 AI 不得擅自修改 00_governance/**，必须经 Founder 批准
2. **没有对应的 ADR，不得编写核心业务代码**
3. **发现设计冲突 → Conflict Report，不自行决定**
4. **每次 Design Session 结束必须产生一个 Commit**

---

## English Summary

Tang Project is exploring **Personality Runtime Infrastructure** — making AI personality definable, verifiable, runnable, and applicable. It is not a chat application; xiaotang is the first validation product. Core claim: personality is not a prompt; it is a loadable, verifiable, runnable software capability.

**Three entry points:** (1) Understand the value → Architecture Overview; (2) Research the technology → Whitepaper / Competitive Analysis / Positioning (bilingual in `research/en-US` and `research/zh-CN`); (3) Run the code → Developer Guide and root README.

**Document map:** cognition layer (why), architecture layer (what), governance layer (boundaries), planning layer (where next).

The internal design-doc index and collaboration rules (00_governance structure, ADR workflow) are preserved in the "内部文档结构" section above for governance purposes.
