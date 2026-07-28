# Tang OS LLM Provider Guide v1.0

> **为什么需要这个文档？**
>
> Tang OS 是人格运行时内核（Personality Runtime Core），不是大语言模型。它输出结构化决策（`ResponseDecision`），不生成自然语言。要让 Tang OS "说话"，你需要接入一个 LLM Provider。

---

## 架构概览

```
用户输入 "我今天很难过"
       │
       ▼
┌─────────────────────────────────────┐
│         Tang OS Core                │
│                                     │
│  情绪理解 → 人格约束 → 策略决策     │
│                                     │
│  输出: ResponseDecision             │
│   ├── detected_feeling: "sadness"   │
│   ├── response_mode: "comfort"      │
│   ├── candidate_intent: "acknowledge"│
│   └── avoid_patterns: [...]         │
└──────────────────────┬──────────────┘
                       │
                       ▼
┌──────────────────────────────────────┐
│  Expression Layer (ExpressionContext) │
│  把决策包装成 LLM 可消费的 Prompt    │
└──────────────────────┬───────────────┘
                       │
                       ▼
┌──────────────────────────────────────┐
│        LLM Provider                  │
│                                      │
│  OpenAI / Claude / Local 等          │
│                                      │
│  输出: 自然语言回复                   │
└──────────────────────────────────────┘
```

**核心原则：** 人格逻辑 ≠ 模型能力。LLM 是表达能力，不是人格来源。

---

## 接口定义

所有 LLM Provider 实现 `LLMProvider` 抽象基类：

```python
from src.providers.llm import LLMProvider, ExpressionContext

class MyProvider(LLMProvider):
    @property
    def provider_name(self) -> str:
        return "my-provider"

    def generate(self, context: ExpressionContext) -> str:
        # context.response_decision — Tang OS 的结构化决策
        # context.user_input        — 原始用户输入
        # context.identity          — 当前人格层级
        # context.to_prompt_messages() — 可直接发给 LLM API 的 messages

        messages = context.to_prompt_messages()
        # 调用你的 LLM API ...
        return generated_text
```

### ExpressionContext 字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `response_decision` | dict | ✅ | Tang OS Core 的结构化决策输出 |
| `user_input` | str | ✅ | 用户原始输入 |
| `identity` | dict | ✅ | 当前身份层级 (companion/wise/listener) |
| `conversation_history` | list[dict] \| None | ❌ | 最近对话轮次 |
| `memory_context` | dict \| None | ❌ | 检索到的记忆上下文 |
| `system_instructions` | str \| None | ❌ | 自定义系统指令 |

### LLMProvider 合约

| 要求 | 强制 |
|------|------|
| 不修改 Core Identity 状态 | ✅ 必须 |
| 遵守 `avoid_patterns`（不输出禁止短语） | ✅ 必须 |
| 优先遵循 `candidate_intent` 方向 | ✅ 应当 |
| 不持久化对话数据到 Provider 侧 | ✅ 必须 |
| 支持通过环境变量配置 API Key | ✅ 应当 |

---

## 快速接入

### 方式一：OpenAI 兼容 API（推荐起步）

```python
from src.providers.llm import OpenAIProvider, ExpressionContext

provider = OpenAIProvider(
    api_key="sk-...",
    model="gpt-4",          # 或 "gpt-3.5-turbo"
)

context = ExpressionContext(
    response_decision={...},
    user_input="我今天很难过",
    identity={"current_layer": "companion"},
)

response = provider.generate(context)
```

支持：OpenAI、vLLM、Ollama、任何兼容 OpenAI API 的服务。

### 方式二：Claude API（推荐生产）

```python
from src.providers.llm import ClaudeProvider, ExpressionContext

provider = ClaudeProvider(
    api_key="sk-ant-...",
    model="claude-sonnet-4-20250514",
)

context = ExpressionContext(
    response_decision={...},
    user_input="我今天很难过",
    identity={"current_layer": "companion"},
)

response = provider.generate(context)
```

### 方式三：本地模型（完全离线）

```python
from src.providers.llm import LocalLLMProvider, ExpressionContext

# 默认指向 Ollama (http://localhost:11434/v1)
provider = LocalLLMProvider(
    model="qwen2.5",
    base_url="http://localhost:11434/v1",
)
```

---

## 端到端示例

```python
from tang_os import Tang
from src.providers.llm import OpenAIProvider, ExpressionContext

# 1. Tang OS Core — 人格决策
tang = Tang()
decision = tang.process("我今天很难过")

# 2. Expression Layer — 包装上下文
context = ExpressionContext(
    response_decision=decision,
    user_input="我今天很难过",
    identity={
        "current_layer": tang.identity.current_layer.value,
    },
)

# 3. LLM Provider — 生成回复
provider = OpenAIProvider(api_key="sk-...")
reply = provider.generate(context)

print(reply)
# → "我听到了，你今天似乎经历了一些让你难受的事情..."
```

---

## Provider 选择指南

| 场景 | 推荐 Provider | 说明 |
|------|--------------|------|
| 快速原型 | OpenAI (`gpt-3.5-turbo`) | 成本低、速度快 |
| 生产部署 | Claude (`claude-sonnet-4`) | 人格一致性最强 |
| 离线/隐私 | Local (Ollama + qwen2.5) | 数据不出本地 |
| 自定义模型 | OpenAI-compatible (vLLM) | 任意模型接入 |

---

## 相关文档

- [OpenAI 接入指南](OPENAI_SETUP.md)
- [Claude 接入指南](CLAUDE_SETUP.md)
- [本地模型接入指南](LOCAL_MODEL_SETUP.md)
- [ADR-0047: LLM Provider Interface & Integration Boundary](../02_decisions/ADR-0047-llm-provider-interface.md)
