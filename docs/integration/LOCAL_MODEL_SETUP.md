# Local Model Setup Guide

> 接入本地模型作为 Tang OS 的 LLM Provider。
>
> 适合离线场景、隐私敏感场景或不想依赖外部 API 的开发环境。

---

## 前置条件

- Python 3.10+
- OpenAI Python 包：`pip install openai`
- 本地运行的 LLM 服务（Ollama / vLLM / llama.cpp 等）

## 方式一：Ollama（推荐起步）

### 1. 安装 Ollama

从 [ollama.com](https://ollama.com) 下载安装。

### 2. 拉取模型

```bash
ollama pull qwen2.5      # 中文能力强，推荐
# 或
ollama pull llama3.2     # 英文为主
```

### 3. 启动服务

```bash
ollama serve
```

服务默认运行在 `http://localhost:11434`

### 4. 使用

```python
from src.providers.llm import LocalLLMProvider, ExpressionContext

provider = LocalLLMProvider(
    base_url="http://localhost:11434/v1",
    model="qwen2.5",
    temperature=0.7,
    max_tokens=1024,
)
```

## 方式二：vLLM（生产级）

### 1. 部署模型

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
    --model mistral-7b-instruct \
    --api-key not-needed
```

### 2. 使用

```python
provider = LocalLLMProvider(
    base_url="http://localhost:8000/v1",
    model="mistral-7b-instruct",
)
```

## 方式三：llama.cpp

### 1. 启动服务

```bash
./llama-server \
    -m path/to/model.gguf \
    --host 0.0.0.0 \
    --port 8080
```

### 2. 使用

```python
provider = LocalLLMProvider(
    base_url="http://localhost:8080/v1",
    model="default",
    api_key="not-needed",
)
```

## 推荐模型（中文场景）

| 模型 | 量化 | 显存要求 | 中文能力 |
|------|------|---------|---------|
| Qwen2.5-7B | Q4_K_M | ~6GB | ⭐⭐⭐⭐⭐ |
| Qwen2.5-3B | Q4_K_M | ~3GB | ⭐⭐⭐⭐ |
| glm4-9b-chat | Q4_K_M | ~7GB | ⭐⭐⭐⭐⭐ |
| Yi-1.5-9B | Q4_K_M | ~7GB | ⭐⭐⭐⭐ |

## 注意事项

- 本地模型质量受模型大小和量化程度影响
- 小型模型可能不完全遵守 `avoid_patterns`
- 如需情感理解质量，建议使用 7B 以上参数量的模型
- 对于中文场景，Qwen2.5 系列是目前最佳选择
