# Tang Project · 唐先生项目

## Stable AI Personality Runtime · 稳定 AI 人格运行时

> 候选版 README（v0.1）。**不替换当前 README**，供评审后决定是否启用。

---

## What is Tang Project?

唐先生项目探索的是**人格运行基础设施**：让 AI 人格可以被**定义、验证、运行、应用**。

它不是一个聊天应用。它的核心论点是：

> **人格不是提示词，而是可加载、可验证、可运行的软件能力。**

第一个基于它构建的产品是 xiaotang —— 一个验证产品，不是项目的全部。

---

## Architecture Overview

架构总览见 [docs/architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md](docs/architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md)。

一句话架构：

```
人格源 → 人格模块 → Tang OS 运行时 → 决策引擎 → 表达层 → 应用
```

**核心机制：** 决策与表达分离 —— Tang OS 决定"该怎么做"，LLM 负责"怎么说"。
因此换模型不改变人格，人格一致性与边界是可测试的属性。

---

## Three Layers

| 层 | 组成 | 职责 |
|----|------|------|
| **Tang OS** | 人格运行时 | 加载 / 隔离 / 会话绑定 / 决策 / 验证 |
| **tang-ta** | 人格模块标准 | 人格模块的契约（身份/能力/边界/版本/验证） |
| **xiaotang** | 第一个产品 | 用户体验验证（非项目本身） |

---

## Developer Quick Start

> 前提：Python 3.11+，DeepSeek API key。

```bash
# 1. 安装依赖
pip install -r xiaotang/web/requirements.txt

# 2. 设置 API Key
export DEEPSEEK_API_KEY="sk-..."

# 3. 启动 Web 服务
cd xiaotang
python -m uvicorn web.app:app --host 127.0.0.1 --port 8000

# 4. 打开
# http://127.0.0.1:8000/
```

完整开发指引见 [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)（项目级开发者指南）。

---

## Documentation

| 入口 | 文档 |
|------|------|
| 文档导航首页 | [docs/README.md](docs/README.md) |
| 为什么需要人格运行时 | [docs/research/WHY_PERSONALITY_RUNTIME.md](docs/research/WHY_PERSONALITY_RUNTIME.md) |
| 人格运行时白皮书（中/英） | [docs/research/](docs/research/) |
| 系统架构总览 | [docs/architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md](docs/architecture/SYSTEM_ARCHITECTURE_OVERVIEW.md) |
| 长期路线图 | [docs/roadmap/LONG_TERM_ROADMAP.md](docs/roadmap/LONG_TERM_ROADMAP.md) |

---

## English Summary

Tang Project is building **personality runtime infrastructure**: making AI personality definable, verifiable, runnable, and applicable. It is not a chat application; xiaotang is the first validation product. Core claim: personality is not a prompt — it is a loadable, verifiable, runnable software capability.

**Architecture:** Personality Source → Personality Module → Tang OS Runtime → Decision Engine → Expression Layer → Application. Decision and expression are separated: Tang OS decides what to do, an LLM says how. This makes personality model-independent and testable.

**Three layers:** Tang OS (personality runtime), tang-ta (personality module standard), xiaotang (first product).

**Quick start:** Python 3.11+, set `DEEPSEEK_API_KEY`, run the xiaotang web service with uvicorn. Full guide in `docs/CONTRIBUTING.md`.

**Documentation:** start at `docs/README.md`; whitepaper, architecture overview, and roadmap are bilingual (zh-CN / en-US).
