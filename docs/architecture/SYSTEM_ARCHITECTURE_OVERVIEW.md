# System Architecture Overview

## 唐先生项目 · 系统架构总览

Version: v0.1
目的：让一个不了解项目的人，在 10 分钟内理解整个系统。

> **一句话（人话版）：** 唐先生项目 = 人格运行平台（Tang OS）+ 人格模块标准（tang-ta）+ 一个验证产品（xiaotang）。这篇文档用一张图和五层分工讲清楚它们是怎么运作的。

---

## 1. 系统定位（System Purpose）

唐先生项目由三个核心部分组成：

| 组成 | 定位 |
|------|------|
| **Tang OS** | 人格运行平台（Personality Runtime Engine） |
| **tang-ta** | 人格模块标准（Personality Module Standard） |
| **xiaotang** | 用户体验产品（首个验证产品） |

一句话概括：**Tang OS 运行人格，tang-ta 定义人格的格式，xiaotang 让人格被真实用户体验到。**

唐先生项目不是"一个 AI 陪聊 App"，而是"一个人格运行基础设施项目，以 xiaotang 作为第一个消费级验证产品"。

---

## 2. 高层架构（High Level Architecture）

```
                User
                 │
                 │
             xiaotang          ← 应用层：用户体验
                 │
                 │
          Tang Bridge          ← 桥接层：输入归一化、调用 Tang OS
                 │
                 │
             Tang OS           ← 人格运行平台：加载 / 隔离 / 决策
                 │
                 │
      Personality Runtime      ← 运行时：模块执行、Session、边界
                 │
                 │
      Personality Module       ← 人格模块：身份 / 能力 / 边界 / 版本 / 验证
                 │
                 │
                LLM            ← 表达层：把决策变成自然语言
```

数据流自下而上：人格由模块定义，运行时执行，决策引擎决定"怎么应对"，LLM 只负责"怎么说"。

---

## 3. 分层职责（Layer Responsibility）

### Layer 0 — Personality Source（人格源）

**负责：**
- Identity（身份）
- Values（价值观）
- Boundaries（边界）

**不负责：**
- UI
- 对话管理
- 模型调用

> 回答"这个人格是什么"，而不是"这句话怎么回"。

### Layer 1 — Personality Module（人格模块）

**负责：**
- 标准化人格描述
- 版本管理
- 发布生命周期

> 符合 tang-ta 契约：Identity / Capability / Boundary / Version / Validation。

### Layer 2 — Tang OS（人格运行平台）

**负责：**
- 加载人格
- Session 绑定
- 决策执行
- 验证

**不负责：**
- 语言生成

> 核心原则：决策是计算出来的，不是采样出来的。

### Layer 3 — Expression Layer（表达层）

**负责：**
- 文本
- 语音
- 多语言

> 只负责措辞，不负责行为。换模型不改变人格原则。

### Layer 4 — Application（应用层）

**负责：**
- 用户体验
- 产品功能

> 应用只是人格运行的环境，不拥有人格。

---

## 4. 快速判断（10 秒）

| 问题 | 属于哪层 |
|------|----------|
| "唐先生该不该拒绝这种要求？" | 人格源 + 决策引擎（L0/L2） |
| "这句话用中文还是英文说？" | 表达层（L3） |
| "按钮怎么排版？" | 应用层（L4） |
| "怎么让人格可替换？" | 模块标准（L1） |

---

## English Summary

The Tang Project consists of three core parts: **Tang OS** (personality runtime engine), **tang-ta** (personality module standard), and **xiaotang** (the first consumer-facing validation product).

The high-level flow is: User → xiaotang (application) → Tang Bridge → Tang OS (runtime) → Personality Runtime → Personality Module → LLM (expression).

Five layers with strict responsibility boundaries:
- **L0 Personality Source** — defines identity, values, boundaries. Not UI/conversation/model.
- **L1 Personality Module** — standardized personality description, versioning, release lifecycle (tang-ta contract).
- **L2 Tang OS** — loads personalities, binds sessions, executes decisions, validates. Does NOT generate language.
- **L3 Expression Layer** — text, voice, multilingual expression only.
- **L4 Application** — user experience and product features; applications do not own personalities.

Key principle: *decisions are computed, not sampled.* LLM handles wording, never behavior. This is why the project is infrastructure for reliable AI personalities, not a chatbot.
