# xiaotang 架构设计

---

## 系统关系

```text
xiaotang 是 Tang OS 的应用层，不是 Tang OS 的修改层。
```

```text
用户
  │
  ▼
┌─────────────────────┐
│   xiaotang UI       │  ← 交互层（CLI / Web / 语音）
│                     │
│   Conversation      │  ← 会话管理（历史 + 上下文）
│   Service           │
│                     │
│   Tang OS Bridge    │  ← 调用 Tang OS Core
└─────────┬───────────┘
          │ 调用
          ▼
┌─────────────────────┐
│   Tang OS Core      │  ← 人格/认知/边界（外部不可修改）
│                     │
│   LLMProvider       │  ← 语言生成接口
│   (DeepSeek)        │
└─────────────────────┘
```

## 分层职责

| 层 | 职责 | 禁止 |
|----|------|------|
| **UI** | 用户交互、信息展示 | 不包含人格逻辑 |
| **Conversation** | 多轮对话管理、上下文裁剪 | 不修改 Tang OS 决策 |
| **Tang OS Bridge** | 调用 Tang.process() → ExpressionContext | 不绕过 Decision Layer |
| **Tang OS** | 情绪识别、人格约束、策略决策（外部系统） | 不包含 UI 逻辑 |

## 数据流（一次对话）

```
用户输入 "今天心情不好"
  ↓
Conversation Service 记录用户消息
  ↓
Tang.process("今天心情不好")
  ↓ 返回
ResponseDecision
  ├── feeling: sadness
  ├── mode: comfort
  ├── intent: acknowledge
  └── avoid: ["别难过", "想开点"]
  ↓
ExpressionContext 包装（含历史）
  ↓
DeepSeekProvider.generate(context)
  ↓ 返回
"我听到了，今天似乎有些事情让你感到低落..."
  ↓
Conversation Service 记录回复
  ↓
UI 展示给用户
```

## 架构原则

### P1: Tang OS 不拥有 UI

人格内核不包含任何交互层代码。

### P2: xiaotang 不拥有人格

应用层不复制、不修改、不绕过 Tang OS 人格逻辑。

### P3: LLM 是插件

Provider 可随时替换（DeepSeek / Claude / GPT / Local），人格不漂移。

### P4: 历史非记忆

对话历史只用于上下文传递，不替代 Tang OS Memory Runtime。
