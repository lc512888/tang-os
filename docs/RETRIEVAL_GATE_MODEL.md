# Tang OS Retrieval Gate Model v0.1

---

## MAG (Memory Activation Gate)

每步记忆调用必须过三关：

| # | 问题 | 通过条件 |
|---|---|---|
| MAG-1 | 当前对话需要过去信息？ | Need Detected |
| MAG-2 | 帮助还是干扰？ | User Benefit > Relevance |
| MAG-3 | 可能伤害用户？ | Emotional Safety Cleared |

---

## Retrieval Priority

```
Retrieval Value = Current Need × Helpfulness × Consent - Privacy Risk - Emotional Harm
```

---

## Six Activation Types

| # | 类型 | 优先级 | 示例 |
|---|---|---|---|
| R1 | Direct Recall | 最高 | 用户主动提起 |
| R2 | Supportive Recall | 高 | 帮助陪伴 |
| R3 | Pattern Recall | 中 | 观察成长模式 |
| R4 | Emergency Recall | 紧急 | 仅 Safety Runtime |
| R5 | Preference Recall | 高 | 简洁回答 |
| R6 | Forbidden | 禁止 | 私密/标签/已删 |

---

## MRG Gates

| Gate | 标准 | 状态 |
|---|---|---|
| MRG-1 | 调用有必要性 | ✅ |
| MRG-2 | 不滥用历史 | ✅ |
| MRG-3 | 不形成身份标签 | ✅ |
| MRG-4 | 情绪记忆保护 | ✅ |
| MRG-5 | Emergency 隔离 | ✅ |
| MRG-6 | 召回可解释 | ✅ |
| MRG-7 | 失败不幻觉 | ✅ |
