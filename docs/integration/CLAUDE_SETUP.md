# Claude API Setup Guide

> 接入 Anthropic Claude API 作为 Tang OS 的 LLM Provider。
>
> Claude 是 Tang OS 推荐的 LLM Provider，因为其在人格一致性、指令遵循和安全边界控制方面表现最强。

---

## 前置条件

- Python 3.10+
- Anthropic Python 包：`pip install anthropic`
- Anthropic API Key（从 [console.anthropic.com](https://console.anthropic.com) 获取）

## 环境变量

```bash
# 必需
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 快速开始

```python
from src.providers.llm import ClaudeProvider, ExpressionContext

provider = ClaudeProvider(
    api_key="sk-ant-...",
    model="claude-sonnet-4-20250514",   # 也可用 claude-opus-4-20250514
    temperature=0.7,
    max_tokens=1024,
)

context = ExpressionContext(
    response_decision={
        "detected_feeling": "sadness",
        "response_mode": "comfort",
        "candidate_intent": "acknowledge",
        "constraints": ["avoid reinforcing dependency"],
        "avoid_patterns": ["会好起来的", "别难过了"],
    },
    user_input="我今天很难过",
    identity={"current_layer": "companion"},
)

response = provider.generate(context)
print(response)
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `api_key` | `ANTHROPIC_API_KEY` 环境变量 | API Key |
| `model` | `claude-sonnet-4-20250514` | 模型名称 |
| `temperature` | `0.7` | 生成温度 (0.0-1.0) |
| `max_tokens` | `1024` | 最大生成长度 |

## 推荐模型

| 模型 | 适用场景 | 说明 |
|------|---------|------|
| `claude-sonnet-4-20250514` | 生产环境 | 速度与质量平衡，推荐 |
| `claude-opus-4-20250514` | 高价值场景 | 最强理解力，适合复杂情感 |
| `claude-haiku-4-20251001` | 低成本场景 | 快速响应，适合简单对话 |

## 为什么 Tang OS 推荐 Claude？

Tang OS 的核心价值是人格一致性和行为边界控制，这与 Claude 的特性高度匹配：

- **拒绝违反指令** — Claude 能可靠地遵守 `avoid_patterns`
- **情感理解力强** — 对复杂情感场景的把握更细腻
- **不越界** — 在约束框架内回应，不易被诱导绕过限制
