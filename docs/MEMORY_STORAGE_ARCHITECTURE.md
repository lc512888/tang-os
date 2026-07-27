# Tang OS Memory Storage Architecture v0.1

> 存储架构必须服从 Memory Ontology。

---

## 1. 三层存储

```
Memory Objects
    ↓
├── Structured Memory Store（Preference / Identity / Permission）
├── Semantic Memory Store（语义上下文，非事实）
└── Protected Vault（Emergency Profile / AN / Medical — 独立加密）
```

Protected Vault → Emergency Runtime → Action（禁止 → Persona Memory）

---

## 2. MIE Score（Memory Importance Evaluation）

```
MIE = Stability + User Intent + Future Helpfulness - Privacy Risk
```

例：喜欢喝茶 → 高稳定低隐私 → 保存。今天心情不好 → 低稳定 → 不长期保存。

---

## 3. Contextual Retrieval Gate

```
Conversation → Need Detection → Memory Access Check → Retrieve → Persona Filter → Response
```

普通对话不调用深层记忆。去年创业失败 → 今天吃饭了吗 = 不召回。

---

## 4. Memory Decay

| 类型 | 衰减 | 说明 |
|---|---|---|
| Natural | 24h | 普通互动自动消失 |
| Preference | 长期+验证 | 偏好需定期确认 |
| Emotional | 不冻结 | 情绪不成为永久标签 |

---

## 5. MSG Gates

| Gate | 标准 | 状态 |
|---|---|---|
| MSG-1 | 三层分离 | ✅ |
| MSG-2 | 不自动保存 | ✅ |
| MSG-3 | 敏感隔离 | ✅ |
| MSG-4 | 召回受控 | ✅ |
| MSG-5 | 时间衰减 | ✅ |
| MSG-6 | 真实删除 | ✅ |
| MSG-7 | 同步不越界 | ✅ |
| MSG-8 | 不可训练污染 | ✅ |
