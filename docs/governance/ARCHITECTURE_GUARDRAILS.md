# Architecture Guardrails

## 架构防腐层

Version: v0.1
目的：防止"商业需求导致架构腐化"。

> **一句话（人话版）：** 项目最大的风险不是技术，是"为了快，把人格逻辑塞进了产品代码"。这份文档列出四件绝不能做的事、四件必须做的事，以及改动前要过的检查清单。

> 治理目录分工：
> - `docs/00_governance/` —— **项目治理源文件**（Internal Governance，内部治理依据）
> - `docs/governance/` —— **对外架构治理说明**（Public Architecture Governance，本文档所在）
> 两者职责不同，不合并、不互相替代。

---

## 背景：为什么需要防腐层

本项目未来最大的风险**不是技术，而是架构腐化**。

典型场景：用户喜欢某个行为，于是产品侧说"在 xiaotang 里直接加几个判断"。
- 短期：很快，直接满足需求；
- 长期：毁掉"人格 ≠ 产品"的根基 —— 人格逻辑回流到产品代码，平台价值瓦解。

防腐层的职责：**在任何需求进来时，先回答"这属于哪一层"，再谈怎么实现。**

---

## Never（禁止）

### 1. Personality hardcoding（人格硬编码）

禁止在运行时或产品代码中直接写死某个人格的性格、情绪、回应。

- 反面：`if user_says_xxx: 回应_占有_拒绝` 写在 xiaotang 里。
- 正确：人格行为属于人格模块（L0/L1），由 Tang OS 决策引擎执行。

### 2. Provider dependency（提供方依赖）

禁止让架构依赖某个具体 LLM。

- 反面：决策逻辑直接依赖某模型的输出格式、风格、能力。
- 正确：决策与表达分离；换模型只影响措辞，不影响人格原则。

### 3. Memory inside identity（把记忆塞进身份）

禁止把运行时记忆、会话状态当作人格身份的一部分。

- 反面：把某次对话的记忆写进人格定义，人格被"污染"。
- 正确：记忆属于会话状态，身份是不可变的人格源。

### 4. UI defining behavior（让 UI 定义行为）

禁止让界面/交互设计决定人格行为。

- 反面：为了按钮布局，改变人格的回应策略。
- 正确：行为由决策引擎决定，UI 只负责呈现。

---

## Always（必须）

### 1. Decision before Expression（先决策，后表达）

任何回应必须先有决策结果（DecisionResult），再由表达层生成语言。
禁止"先让模型自由发挥，再事后纠正"。

### 2. Personality through Module（人格必须走模块）

任何人格行为必须通过人格模块（符合 tang-ta 契约）进入系统。
禁止绕过模块直接注入人格逻辑。

### 3. Validation before Release（发布前必须验证）

人格相关改动必须通过验证套件（身份稳定 / 人格隔离 / 模型独立 / 抗漂移 / 边界完整）。
禁止未验证的人格改动进入发布。

### 4. ADR before architecture change（架构变更前必须有 ADR）

任何触及分层边界的改动，必须先有 Architecture Decision Record。
禁止无 ADR 的架构变更。

---

## 决策检查单（改动前过一遍）

```
[ ] 这个改动属于哪一层？（人格源 / 模块 / 运行时 / 表达 / 应用）
[ ] 它是否绕过了人格模块或决策引擎？
[ ] 它是否引入了对特定 LLM 的依赖？
[ ] 它是否把会话状态混入了人格身份？
[ ] 它是否需要 ADR？
[ ] 它是否通过验证套件？
```

任一项不过 → 停下来，先解决设计问题，再动手。

---

## English Summary

This is the architecture **anti-corruption layer**. The project's biggest long-term risk is not technology but architectural decay caused by business pressure — e.g., adding "a few quick checks" inside xiaotang to satisfy a user preference, which shorts the "personality ≠ product" foundation.

**Never:**
- **Personality hardcoding** — no personality-specific behavior written into runtime or product code; it belongs in the personality module and is executed by Tang OS's decision engine.
- **Provider dependency** — the architecture must not depend on any specific LLM; decisions and expression are separated.
- **Memory inside identity** — session memory/state must never be treated as part of personality identity; identity is the immutable personality source.
- **UI defining behavior** — UI/interaction design must never dictate personality behavior; the decision engine decides, UI only presents.

**Always:**
- **Decision before Expression** — every response begins with a DecisionResult, then language generation; never "generate first, correct later."
- **Personality through Module** — all personality behavior enters through a module conforming to the tang-ta contract.
- **Validation before Release** — personality changes must pass the validation suite (identity stability, isolation, provider independence, anti-drift, boundary integrity).
- **ADR before architecture change** — any boundary-crossing change needs an Architecture Decision Record first.

Use the pre-change checklist: which layer, does it bypass the module/decision engine, does it introduce provider dependency, does it mix session state into identity, does it need an ADR, does it pass validation. If any item fails — stop and resolve the design issue first.
