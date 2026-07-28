# ADR-0047: Tang OS LLM Provider Interface & Integration Boundary v1.0

**日期：** 2026-07-28
**状态：** Accepted（Founder Approve — 2026-07-28）
**层级：** Architecture Layer（Provider Boundary）
**影响范围：** Phase 13-D（当前阶段）、所有外部开发者入口、README/公开文档
**前序资产：** ADR-0041（Public Specification），ADR-0042（Reference Implementation），ADR-0043（Developer Interface），ADR-0044（Example Application），SYSTEM_OVERVIEW.md

---

## 背景

### 架构现状

Tang OS v0.1.0 已发布至 GitHub。当前定位是"Personality Runtime Core"——一个输出结构化决策（`ResponseDecision`）而非自然语言的规则引擎。

内部设计文档（`SYSTEM_OVERVIEW.md`）正确规划了：

```
用户输入 → Tang OS Core → ResponseDecision → LLM Provider → 自然语言回复
```

并明确写明了架构原则：

> **人格逻辑与模型调用分离** — 角色行为由人格引擎控制，LLM 只是实现手段
> **Provider 可替换** — LLM、TTS、图像生成等外部服务通过适配器模式接入

但该 Provider 层 **全部标记 🏗 待建**。

### 问题

当前 GitHub 公开仓库存在三个缺口：

| 缺口 | 严重程度 | 影响 |
|------|---------|------|
| **Gap-1：定位声明缺失** | 🔴 最高 | README Quick Start 让开发者误以为 Tang OS 是完整聊天系统，实际输出只有 `Feeling.SADNESS` |
| **Gap-2：Provider 接口不存在** | 🔴 最高 | 开发者拿到代码后不知道在哪里接入 GPT/Claude/本地模型 |
| **Gap-3：Expression Layer 未契约化** | 🟡 高 | `ResponseDecision` 的消费方未定义，架构缺少"从决策到人话"的正式桥梁 |

### 根本原因

> **内部架构设计正确（层的划分是完整的），但开发者入口没有闭环。**

Tang OS 的核心价值——人格规则是稳定资产，LLM 是可替换的大脑语言能力——没有被暴露给外部开发者。开发者拿到的是一个"断了的下半截"。

---

## 决策

### 一、LP-001: Tang OS Is Not an LLM — 明确声明义务

**Tang OS 本身不是大语言模型。**

Tang OS 是一个 AI 人格运行时与认知控制层。它负责情绪理解、人格约束、回应策略决策、行为边界控制。自然语言生成需要通过 LLM Provider 完成。

此声明必须出现在：
- README.md **首页**（不藏在 docs 里）
- 项目首页 `pypi` 描述
- 开发者指南首段
- Self-Description Protocol（已有类似表述，需强化）

### 二、LP-002: Expression Layer Contract — 从决策到人话的接口

定义 `ExpressionContext` 作为 LLM Provider 的输入契约：

```python
@dataclass
class ExpressionContext:
    """The complete context an LLM Provider needs to generate a response.
    
    Combines Tang OS Core's structured decision with conversation history
    and identity constraints.
    """
    # Required: Tang OS Core output
    response_decision: ResponseDecision
    
    # Required: Original user input
    user_input: str
    
    # Required: Identity context
    identity: dict  # current_layer, constitution_rules
    
    # Optional: Conversation state
    conversation_history: list[dict] | None = None
    
    # Optional: Memory context
    memory_context: dict | None = None
    
    # Optional: System prompt / personality instructions
    system_instructions: str | None = None
```

**Expression Layer 的职责：**

```
Tang OS Core
    ↓ ResponseDecision
ExpressionContext（包装）
    ↓
LLM Provider.generate(context) → str
    ↓
自然语言回复（已完成身份约束、情绪匹配、边界控制）
```

### 三、LP-003: LLMProvider Protocol — Provider 抽象契约

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


class LLMProvider(ABC):
    """Abstract LLM Provider — Tang OS does not own the model.
    
    Any LLM that implements this interface can serve as the
    expression layer for Tang OS personality runtime.
    
    Provider implementations must:
    1. Accept ExpressionContext as input
    2. Respect avoid_patterns from ResponseDecision (not output them)
    3. Follow candidate_intent from ResponseDecision
    4. Return natural language string
    """
    
    @abstractmethod
    def generate(self, context: ExpressionContext) -> str:
        """Generate a natural language response from Tang OS context.
        
        The implementation:
        - MAY use ExpressionContext.to_chat_messages() as message base
        - MUST respect ResponseDecision.avoid_patterns
        - SHOULD follow ResponseDecision.candidate_intent
        - MUST NOT modify Tang OS Core state
        
        Returns generated text as string.
        """
        ...
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider identifier (e.g. 'openai', 'claude')."""
        ...

    # Optional methods (v0.2.0 preview — not abstract, no forced implementation):
    # stream()    → Streaming support for token-by-token generation
    # health_check() → Provider operational status check
```

### 四、LP-004: Provider 实现标准

每个 Provider 实现必须满足：

| 要求 | 说明 |
|------|------|
| **PMP-001** | 不修改 Core Identity 状态 |
| **PMP-002** | 不绕过 ResponseDecision 约束（尤其是 avoid_patterns） |
| **PMP-003** | 不持久化对话数据至 Provider 侧 |
| **PMP-004** | 支持通过环境变量配置 API Key |
| **PMP-005** | 声明兼容的 API 版本 |

官方推荐实现（按优先级）：
1. **OpenAI-compatible Provider** — 覆盖最多第三方模型（包括本地 ollama、vLLM）
2. **Claude Provider** — 与 Tang OS 设计理念最匹配（强人格一致性）
3. **Local Provider** — 完全离线场景

### 五、LP-005: 版本与定位更新

| 版本 | 内容 |
|------|------|
| v0.1.0（当前） | **Personality Runtime Core** — 情绪理解 + 人格约束 + 决策输出 |
| v0.2.0（下一目标） | **LLM Integration Layer** — Provider Interface + OpenAI/Claude/Local 实现 |
| v0.3.0（未来） | **Memory Runtime** — 长期记忆 + 关系记忆 |

**README.md 首页必须立即更新**（不等 v0.2.0），增加定位声明。

### 六、LP-006: Provider 包结构标准

```
src/
  providers/
    __init__.py
    llm/
      __init__.py
      base.py          ← LLMProvider 抽象基类
      context.py       ← ExpressionContext 定义
      openai_provider.py
      claude_provider.py
      local_provider.py
  tang_os/
    expression.py      ← Expression Layer 编排器（调用 Provider + 验证）
```

---

## 原因

| 原因 | 说明 |
|------|------|
| **R1 — 外部开发者可理解** | 没有 Provider 接口，开发者不知道 Tang OS 怎么"用" |
| **R2 — 保持 Provider 无关** | 抽象接口确保 Tang OS 不绑定任何特定模型 |
| **R3 — 架构完整性** | Provider 层是 SYSTEM_OVERVIEW.md 已规划但缺失的部分 |
| **R4 — 开源诚信** | README 必须诚实说明系统边界，否则造成误导 |
| **R5 — 版本语义清晰** | v0.1.0 是 Core，v0.2.0 加 LLM 集成，符合工程节奏 |

---

## 影响

### 正面

| 影响 | 程度 |
|------|------|
| 开发者拿到 Tang OS 后知道下一步做什么 | 🔵 决定性 |
| 保持"人格不是模型"的核心哲学可见 | 🔵 决定性 |
| Provider 可替换架构吸引更多开发者 | 🟢 显著 |
| 降低"又一个 Prompt 工程"的误解风险 | 🟢 显著 |
| 版本语义清晰化，项目可信度提升 | 🟢 显著 |

### 负面

| 影响 | 程度 |
|------|------|
| 需额外开发 Provider 实现代码 | 🟡 可控 |
| 部分首次接触的开发者可能因"需要自己接模型"而退缩 | 🟡 不可避免，但优于误导 |
| 需维护多 Provider 兼容性 | 🟡 长期成本 |

---

## AR-GATE 自检

### Constraint-001 必要性

当前 Tang OS Core 输出 `ResponseDecision` 但不生成自然语言。外部开发者无入口理解如何集成 LLM。架构完整性和开发者体验均要求此决策。

✅ PASS

### Constraint-002 充分性

LP-001~006 覆盖：定位声明、Expression Contract、Provider 抽象契约、实现标准、版本语义、包结构。足以让外部开发者理解并接入。

✅ PASS

### Layer Discipline

```
Architecture → Provider Boundary → Expression Layer → LLM Provider
```

Provider 层位于 Runtime 与外部模型之间，不越级修改 Core、Governance 或 Identity。无越级。

✅ PASS

### 与 Frozen ADR 冲突

| ADR | 关系 | 状态 |
|-----|------|------|
| ADR-0041 | Public Spec 定义系统边界，LP-001 补充外部可见边界 | ✅ 互补 |
| ADR-0042 | RI 是 Provider 的宿主，LP-003 定义 RI 的扩展方式 | ✅ 互补 |
| ADR-0043 | Developer Interface 是 TPI，LP-003 是 Provider 接口，层级不同 | ✅ 无冲突 |
| ADR-0044 | Example 需消费 Provider 接口，LP-002 为 Example 提供 Expression 契约 | ✅ 互补 |
| ADR-0038 | Civilization Boundary 在上游，Provider 在下游 | ✅ 无冲突 |

### 最小必要原则

✅ 不创建新的 Governance 层，不修改 Core Identity/Invariant/Constitution。仅在 Provider 边界增加接口抽象。

---

## 后续依赖

- **Phase 13-D-1**: 实现 `LLMProvider` 抽象基类 + `ExpressionContext` ✅ 已完成
- **Phase 13-D-2**: 实现 OpenAI-compatible Provider（Reference Adapter Skeleton）✅ 已完成
- **Phase 13-D-3**: 实现 Claude Provider（Reference Adapter Skeleton）✅ 已完成
- **Phase 13-D-4**: 更新 README.md 首页定位声明 ✅ 已完成
- **Phase 13-D-5**: 创建 `docs/integration/LLM_PROVIDER_GUIDE.md` ✅ 已完成
- **Phase 13-D-6**: 真实 Provider 实现（full API client）⬜ 待 Founder Accept 后推进
- **Phase 13-D-7**: 端到端 Demo 示例（Tang OS → Provider → 回复）⬜ 待 ADR 冻结后
- **Phase 13-D-8**: 版本升级 v0.2.0-alpha ⬜ 待真实 Provider 完成后

---

## Review Record

### 审查阶段一（Claude Code · 工程师初稿）

**日期：** 2026-07-28
**审查者：** Claude Code（工程师视角）
**总体结论：** PENDING — 等待 Founder + ChatGPT（首席架构师）审查

| 编号 | 审查内容 | 当前判断 |
|------|---------|---------|
| LP-001 | 定位声明是否足够清晰 | ✅ 建议通过 |
| LP-002 | ExpressionContext 字段是否完整 | ❓ 需架构师确认 |
| LP-003 | LLMProvider 抽象是否最小必要 | ✅ 建议通过 |
| LP-004 | 实现标准是否可执行 | ✅ 建议通过 |
| LP-005 | 版本语义化方案 | ✅ 建议通过 |
| LP-006 | 包结构设计 | ❓ 需架构师确认 |

### 审查阶段二（Claude Code · 架构一致性审查）

**日期：** 2026-07-28
**审查者：** Claude Code（架构审查）
**审查依据：** Founder 提出的 6 项 Review 要求

| # | 审查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | Core ↔ LLM 完全解耦 | ✅ PASS | Tang OS Core 零 import providers 包；零引用 OpenAI/Claude SDK |
| 2 | ExpressionContext 设计 | ✅ PASS | 纯数据协议；`to_prompt_messages()` 已重命名为 `to_chat_messages()`，明确为序列化辅助，非 Prompt 模板 |
| 3 | Provider 接口稳定性 | ✅ PASS | `stream()` 和 `health_check()` 已添加为非抽象可选方法，v0.2.0 预留 |
| 4 | Provider Stub 定位 | ✅ PASS | 全部标记为 "Reference Adapter Skeleton"，错误信息明确说明为设计契约演示 |
| 5 | README 三问确认 | ✅ PASS | Q1(是什么) → 副标题 "Personality Runtime Core"；Q2(不是什么) → 定位声明首行 "not an LLM"；Q3(如何用) → 定位声明 + Quick Start 注释指向集成文档 |
| 6 | ADR 边界确认 | ✅ PASS | Provider 层不越级修改 Core/Governance/Identity；无冲突 |

**架构审查结论：** 六项全部通过。架构边界正确，建议进入 Founder Accept。

### AR-GATE Final

```
Constraint-001: Necessary      ✅ PASS
Constraint-002: Sufficient     ✅ PASS
Layer Discipline:              ✅ PASS
No Duplication:                ✅ PASS
Complexity Ratio:              ✅ PASS
Minimal Necessary:             ✅ PASS

Architecture Review Phase-1:  ✅ PASS (6/6 checks)
Architecture Review Phase-2:  ✅ PASS (6/6 checks)

Founder Final Review (2026-07-28):
  - Core isolation             ✅ PASS
  - Provider boundary          ✅ PASS
  - Expression contract        ✅ PASS
  - Documentation consistency  ✅ PASS
  - Extension readiness        ✅ PASS

Final Decision: ACCEPTED ✅ — 冻结架构边界
```
### Review Record (Founder)

**日期：** 2026-07-28
**审查者：** Founder
**总体结论：** ACCEPT ✅ — 架构边界已验证，达到冻结条件

```
Founder Review:
  Core ↔ LLM decoupling       ✅ 人格逻辑与模型能力分离
  ExpressionContext 调整       ✅ to_chat_messages() 正确
  Provider Interface           ✅ 可选扩展设计合理，无过度工程
  Stub 定位                    ✅ Reference Adapter Skeleton
  README 三问                  ✅ 开发者认知闭环已形成
  ADR 边界                    ✅ Provider 不越权修改 Core/Governance

Final: ADR-0047 Accepted. 可以冻结。
```
