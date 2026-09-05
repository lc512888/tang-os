# OpenAI Setup Guide

> **状态：接口骨架，不可运行。** 当前 `OpenAIProvider.generate()` 明确返回
> `ProviderUnsupportedError`；即使 API Key 有效，`is_configured` 也为 `False`。

---

## 前置条件

- Python 3.10+
- OpenAI Python 包：`pip install openai`
- OpenAI API Key（或兼容服务的 API Key）

## 环境变量

```bash
# 必需
export OPENAI_API_KEY="sk-..."

# 可选：自定义 endpoint（用于 vLLM、Ollama 等兼容服务）
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

## 快速开始

```python
from providers.llm import OpenAIProvider, ExpressionContext

provider = OpenAIProvider(
    api_key="sk-...",
    model="gpt-4",           # 可选: gpt-4, gpt-3.5-turbo, gpt-4o
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

# 当前版本会抛出 ProviderUnsupportedError；请实现自定义 LLMProvider，
# 或使用已经可运行的 DeepSeekProvider。
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `api_key` | `OPENAI_API_KEY` 环境变量 | API Key |
| `model` | `gpt-4` | 模型名称 |
| `base_url` | `https://api.openai.com/v1` | API endpoint |
| `temperature` | `0.7` | 生成温度 (0.0-2.0) |
| `max_tokens` | `1024` | 最大生成长度 |

## 兼容服务

| 服务 | base_url | 说明 |
|------|---------|------|
| OpenAI | `https://api.openai.com/v1` | 官方 API |
| vLLM | `http://localhost:8000/v1` | 本地部署 |
| Ollama | `http://localhost:11434/v1` | 本地运行 |
| Azure OpenAI | `https://{你的资源}.openai.azure.com` | 企业版 |
