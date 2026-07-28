# DeepSeek Provider Setup Guide

> 接入 DeepSeek API 作为 Tang OS 的第一个真实 LLM Provider。

---

## 作用

DeepSeek Provider 是 Tang OS **第一个真实 LLM Adapter**。它证明了 Expression Layer 可以在不修改 Tang OS Core 的前提下，驱动真实 LLM 产生符合唐先生人格的自然语言回复。

**核心边界：**
- DeepSeek 负责 **语言生成**，不负责 **人格定义**
- Tang OS Core 决定"如何回应"（模式、意图、约束）
- DeepSeek 决定"如何表达"（措辞、语气、句式）

---

## 前置条件

- Python 3.10+
- OpenAI Python 包：`pip install openai`
- DeepSeek API Key（从 [platform.deepseek.com](https://platform.deepseek.com) 获取）

## 环境变量

```bash
# 必需
export DEEPSEEK_API_KEY="sk-..."

# 可选
export DEEPSEEK_MODEL="deepseek-chat"       # 默认: deepseek-chat
export DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"  # 默认: DeepSeek 官方
```

## 快速开始

### 方式一：Demo 脚本

```bash
export DEEPSEEK_API_KEY="sk-..."
python examples/deepseek_chat_demo.py "我最近压力很大"
```

预期输出：

```
👤 用户: 我最近压力很大
──────────────────────────────────────────────────
🧠 Tang OS Core:
   情绪:      sadness
   回应模式:  comfort
   意图:      acknowledge
   避免:      ['会好起来的', '别难过了']
──────────────────────────────────────────────────
🤖 DeepSeek 生成中...
──────────────────────────────────────────────────
💬 唐先生: 我听到了，最近是不是遇到了很多事情让你感到疲惫？
──────────────────────────────────────────────────
✅ 端到端闭环完成
   引擎: Tang OS Core → DeepSeek (deepseek-chat)
   ADR:  ADR-0047 (LLM Provider Interface)
```

### 方式二：代码中直接使用

```python
from tang_os import Tang
from src.providers.llm import DeepSeekProvider, ExpressionContext

# 1. Tang OS Core
tang = Tang()
decision = tang.process("我今天很难过")

# 2. Expression Layer
context = ExpressionContext(
    response_decision=decision,
    user_input="我今天很难过",
    identity={"current_layer": tang.identity.current_layer.value},
)

# 3. DeepSeek Provider
provider = DeepSeekProvider()
response = provider.generate(context)
print(response)
```

## 配置参数

| 参数 | 环境变量 | 默认值 | 说明 |
|------|---------|--------|------|
| `api_key` | `DEEPSEEK_API_KEY` | — | API Key（必需） |
| `model` | `DEEPSEEK_MODEL` | `deepseek-chat` | 模型名称 |
| `base_url` | `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | API endpoint |
| `temperature` | — | `0.7` | 生成温度 (0.0-2.0) |
| `max_tokens` | — | `2048` | 最大生成长度 |
| `timeout` | — | `60` | 请求超时（秒） |

## 推荐模型

| 模型 | 适用场景 | 说明 |
|------|---------|------|
| `deepseek-chat` | 通用对话 | 默认，性价比最高 |
| `deepseek-reasoner` | 复杂推理 | 深度思考，速度较慢 |

## 注意事项

> ⚠️ DeepSeek Provider 只负责语言生成，不包含任何唐先生人格逻辑。
>
> 人格定义、情绪判断、回应策略全部由 Tang OS Core 控制。
>
> 如果你发现 DeepSeek 的回复不符合唐先生风格，请在 Tang OS Core 层面调整，而不是修改 Provider。

## 架构示意

```
Tang OS Core
    │
    ▼
ResponseDecision
    │
    ├── detected_feeling: "sadness"
    ├── response_mode: "comfort"
    ├── candidate_intent: "acknowledge"
    └── avoid_patterns: ["会好起来的"]
    │
    ▼
ExpressionContext.to_chat_messages()
    │
    ▼
DeepSeek API
    │
    ▼
"我听到了，你今天似乎经历了一些让你难受的事情..."
```

## 相关文档

- [LLM Provider 总览](LLM_PROVIDER_GUIDE.md)
- [ADR-0047: LLM Provider Interface](../02_decisions/ADR-0047-llm-provider-interface.md)
