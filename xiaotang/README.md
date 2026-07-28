# 小唐 — 极轻陪聊

> 以唐先生（Tang OS）为内核的轻量陪伴聊天应用。

---

## 它是什么

小唐是一个**极轻的 CLI 陪聊应用**。

它的内核是 Tang OS 人格运行时，语言表达由 DeepSeek 驱动。

```
用户输入
  ↓
Tang OS（人格/认知/边界）
  ↓
DeepSeek（语言表达）
  ↓
小唐回复
```

**它不是 ChatGPT 替代品。** 它是唐先生人格在命令行中的最小实现。

## 快速开始

```bash
# 1. 安装依赖
pip install openai

# 2. 配置 API Key
export DEEPSEEK_API_KEY="sk-..."

# 3. 启动聊天
python xiaotang/app.py
```

## 用法

```bash
# 启动交互模式
python xiaotang/app.py

# 或单条消息
python xiaotang/app.py "最近压力很大"
```

## 特点

| 特性 | 说明 |
|------|------|
| **人格稳定** | Tang OS Core 确保每句回复符合唐先生人格 |
| **边界保护** | 依赖检测、报复意图识别自动生效 |
| **对话记忆** | 多轮对话上下文自然传递 |
| **极轻** | 无 UI、无数据库、无后端，一个文件搞定 |

## 原理

```
app.py (CLI)
  → Tang OS Core (人格决策)
    → ExpressionContext (协议层)
      → DeepSeek API (语言生成)
        → 回复显示
```

Tang OS 输出 `ResponseDecision`（情绪/模式/约束/禁止模式）。
DeepSeek 将其转化为自然语言，不修改人格逻辑。

## 配置

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API Key | — |
| `DEEPSEEK_MODEL` | 模型名 | `deepseek-chat` |
| `DEEPSEEK_BASE_URL` | API 地址 | `https://api.deepseek.com/v1` |
