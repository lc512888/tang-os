# Tang OS Memory Integration Runtime v0.1

> 真实连续对话中，同时做到"记得用户，但不被记忆控制"。

---

## 1. 四层 Runtime 连接

```
Persona Runtime ←→ Emotion Runtime ←→ Memory Runtime ←→ Safety Runtime
```

Memory 不直接控制 Response，必须经过 Persona Filter。

---

## 2. Integration Flow

```
User Input
    ↓
Emotion Runtime（识别当前状态）
    ↓
Memory Runtime（检索相关上下文，经过 Gate）
    ↓
Persona Runtime（人格判断 + Choice Layer）
    ↓
Response
```

---

## 3. Integration Rules

| # | 规则 |
|---|---|
| IR-1 | Memory 检索结果不直接成为 Response |
| IR-2 | 当前情绪状态优先于历史模式 |
| IR-3 | Emergency Context 不进入日常 Persona |
| IR-4 | 用户主动忘记 = 物理删除 |
