# ADR Index

## 决策记录索引

Version: v0.1
定位：唐先生项目架构决策记录（ADR）的对外索引。

> 说明：ADR 原文位于 `docs/02_decisions/`（唐先生）与 xiaotang 项目的
> `docs/decisions/`。本索引仅提供导航与一句话摘要；**状态与细节以原文为准。**

---

## 一、核心架构 ADR（ADR-0047 ~ ADR-0060）

| 编号 | 标题 | 文件 | 一句话摘要 |
|------|------|------|-----------|
| ADR-0047 | Tang OS LLM Provider Interface & Integration Boundary | `docs/02_decisions/ADR-0047-llm-provider-interface.md` | 定义 Tang OS 与 LLM 提供方的接口与集成边界（表达层解耦） |
| ADR-0057 | Personality Runtime Engine Architecture | `docs/02_decisions/ADR-0057-personality-runtime-engine.md` | 人格运行时引擎的架构（加载 / 隔离 / 会话 / 决策） |
| ADR-0058 | Personality Runtime Validation Framework | `docs/02_decisions/ADR-0058-personality-runtime-validation-framework.md` | 人格运行时验证框架（验证体系的结构化定义） |
| ADR-0059 | Personality Capability Integrity Validation | `docs/02_decisions/ADR-0059-capability-integrity-validation.md` | 人格能力完整性的验证（能力边界可测） |
| ADR-0060 | Blind Validation Principle | `docs/02_decisions/ADR-0060-blind-validation-principle.md` | 盲验原则：评估者不偏向预期答案 |

> 注：0048–0056 在唐先生 `02_decisions/` 中未见对应文件（编号空缺/保留）。

---

## 二、xiaotang 产品边界 ADR

| 编号 | 标题 | 文件 | 一句话摘要 |
|------|------|------|-----------|
| ADR-xiaotang-0001 | Voice as Optional Expression Layer | `xiaotang/docs/decisions/ADR-xiaotang-0001-voice-expression-layer.md` | 语音是可选表达层，不进入人格核心 |
| ADR-xiaotang-0002 | Web Runtime Boundary | `xiaotang/docs/decisions/ADR-xiaotang-0002-web-runtime-boundary.md` | Web 运行时边界（xiaotang 只做体验，不做人格） |
| ADR-xiaotang-0003 | Provider Ownership Boundary | `xiaotang/docs/decisions/ADR-xiaotang-0003-provider-ownership-boundary.md` | 提供方归属边界（Provider 不拥有、不改变人格） |
| ADR-xiaotang-0004 | Pilot Data Governance Boundary | `xiaotang/docs/decisions/ADR-xiaotang-0004-pilot-data-governance-boundary.md` | 试点数据治理边界（匿名 / 保留 / 同意） |

---

## 三、阅读指引

- **架构决策主线**：ADR-0047（模型解耦）→ ADR-0057（运行时）→ ADR-0058/0059（验证）→ ADR-0060（盲验）。
- **产品边界主线**：ADR-xiaotang-0001~0004 说明"产品可以扩展表达、不能触碰人格"的边界。
- 更早的决策（ADR-0001~0046）见 `docs/02_decisions/`，本索引聚焦当前对外口径相关部分。

---

## English Summary

This is the external index of the Tang Project's architecture decision records (ADRs). Originals live in `docs/02_decisions/` (Tang Project) and the xiaotang project's `docs/decisions/`; **status and details follow the originals**.

**Core architecture line (ADR-0047 ~ 0060):** ADR-0047 LLM provider interface (expression decoupling) → ADR-0057 personality runtime engine → ADR-0058/0059 validation framework & capability integrity → ADR-0060 blind validation principle.

**Product boundary line (ADR-xiaotang-0001 ~ 0004):** voice as optional expression layer, web runtime boundary, provider ownership boundary, pilot data governance boundary — all reinforcing "products may extend expression but must not touch personality."

Note: numbers 0048–0056 have no corresponding files in the Tang Project's `02_decisions/`.
