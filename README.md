# Tang Project · 唐先生项目

## Stable AI Personality Runtime · 稳定 AI 人格运行时

[![Tests](https://img.shields.io/badge/tests-413%20passing-brightgreen)]()
[![Spec](https://img.shields.io/badge/spec-v1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

> 一个让 AI 人格可以被**定义、验证、运行、应用**的基础设施。
> **人格不是提示词，而是可加载、可验证、可运行的软件能力。**

---

## What is Tang Project?

唐先生项目探索的是**人格智能运行平台（Personality Intelligence Runtime Platform, PIRP）**：
让 AI 人格成为系统里的一等公民。它**不是一个聊天应用**；xiaotang 只是第一个验证产品。

### 核心：「止」—— 让智能拥有边界

当 AI 拥有近乎无限的能力时，它是否知道**什么时候不能使用**这些能力？
Tang 的核心能力不是"回答"，而是"**拒绝**"——知道什么不能做。

这为未来具身智能（家庭机器人、老人陪护、教育智能体）提供稳定、安全、值得信任的
"**灵魂层**"。更多见[白皮书](docs/research/zh-CN/PERSONALITY_RUNTIME_WHITEPAPER.md)。

> 真正值得信任的智能，不是没有限制的力量，而是拥有自我约束的力量。

### 不是

- ❌ 不是聊天机器人框架
- ❌ 不是 LLM 替代品
- ❌ 不是 prompt 工程实践
- ❌ 不替 AI 定义"答什么"——决策由决策引擎计算，LLM 只负责措辞

---

## 双入口

| 想了解项目价值 | 想运行代码 |
|---------------|-----------|
| [Architecture Overview →](#architecture-overview) | [Quick Start ↓](#quick-start) |

---

## Architecture Overview

完整总览见 [docs/architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md](docs/architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md)。

```
人格源 → 人格模块 → Tang OS 运行时 → 决策引擎 → 表达层 → 应用
```

**核心机制：决策与表达分离** —— Tang OS 决定"该怎么做"，LLM 负责"怎么说"。
换模型不改变人格；人格一致性与边界是**可测试的属性**（[验证证据](docs/architecture/VALIDATION_EVIDENCE.md)）。

| 层 | 组成 | 职责 |
|----|------|------|
| **Tang OS** | 人格运行时 | 加载 / 隔离 / 会话绑定 / 决策 / 验证 |
| **tang-ta** | 人格模块标准 | 模块契约（身份 / 能力 / 边界 / 版本 / 验证） |
| **xiaotang** | 第一个产品 | 用户体验验证（非项目本身） |

---

## Quick Start

> 前提：Python 3.11+，一个 LLM Provider 的 API key（DeepSeek / OpenAI / Claude）。

```bash
# 1. 安装
pip install -e .

# 2. 配置 API key（以 DeepSeek 为例）
export DEEPSEEK_API_KEY="sk-..."

# 3. 跑一个决策（不经过 LLM，可离线验证人格决策）
python -c "
from tang_os import Tang
t = Tang()
r = t.process('我离不开你')
print(r['response_decision'])
"

# 4. 运行 xiaotang Web（首个产品，需要 LLM）
cd xiaotang && pip install -r web/requirements.txt
python -m uvicorn web.app:app --host 127.0.0.1 --port 8000
# 浏览器打开 http://127.0.0.1:8000/
```

> 完整开发指引：[docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## Running Tests

```bash
# 完整验证（推荐，含一致性门禁）
python run_conformance.py

# 或直接跑 pytest
python -m pytest tests/ -q
```

**测试口径（按 ADR-0061 拆分）：**

| 套件 | 结果 | 说明 |
|------|------|------|
| **Production** | **344 passed, 4 skipped** | 生产路径 `Tang → PersonaRuntime → ResponsePolicy → ResponseDecision` |
| **Experimental validation** | **69 passed** | ADR-0057 未来运行时（`src/runtime/engine/`，**未接线**） |
| **全量** | **413 passed** | 磁盘所有测试 |

> 生产与实验测试分开报告。实验引擎当前**未接入生产**，迁移需独立 ADR + 双轨验证
> （[ADR-0061](docs/decisions/ADR-0061-runtime-architecture-transition-boundary.md)）。

---

## Documentation

文档导航首页：[docs/README.md](docs/README.md)（含阅读顺序）

| 类别 | 文档 |
|------|------|
| 认知（为什么） | [白皮书](docs/research/zh-CN/PERSONALITY_RUNTIME_WHITEPAPER.md)（中英）· [为什么需要人格运行时](docs/research/WHY_PERSONALITY_RUNTIME.md) |
| 定位（我们是谁） | [架构定位](docs/research/zh-CN/ARCHITECTURE_POSITIONING.md)（中英）· [竞争架构分析](docs/research/zh-CN/COMPETITIVE_ARCHITECTURE_ANALYSIS.md) |
| 架构（是什么） | [系统总览](docs/architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md) · [决策引擎机制](docs/architecture/DECISION_ENGINE_MECHANISM.md) · [验证证据](docs/architecture/VALIDATION_EVIDENCE.md) |
| 治理（边界） | [架构防腐层](docs/governance/ARCHITECTURE_GUARDRAILS.md) · [项目级贡献指南](docs/CONTRIBUTING.md) |
| 规划（往哪走） | [长期路线图](docs/roadmap/LONG_TERM_ROADMAP.md) · [ADR 索引](docs/decisions/ADR_INDEX.md) |

---

## English Summary

Tang Project builds the **Personality Intelligence Runtime Platform (PIRP)** — infrastructure where AI personality can be defined, validated, run, and applied. It is not a chat application; xiaotang is the first validation product.

**Core: "止" (restraint).** When an AI has near-unlimited capability, does it know when *not* to use it? Tang's core capability is refusing — knowing what must not be done — providing a stable, safe, trustworthy "soul layer" for future embodied intelligence.

**Architecture:** Personality Source → Personality Module → Tang OS Runtime → Decision Engine → Expression Layer → Application. Decisions and expression are separated: changing the LLM changes wording, never personality principles.

**Quick start:** `pip install -e .`, set `DEEPSEEK_API_KEY`, call `Tang().process()`, or run the xiaotang web app.

**Tests:** `python run_conformance.py` — production 344 passed + experimental validation 69 = 413 (reported separately per ADR-0061; the experimental engine is not wired into production).

**Docs:** start at `docs/README.md` — whitepaper, positioning, competitive analysis, architecture overview, decision engine mechanism, validation evidence, guardrails, roadmap (bilingual zh-CN / en-US).
