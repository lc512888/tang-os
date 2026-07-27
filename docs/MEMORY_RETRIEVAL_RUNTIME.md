# Tang OS Memory Retrieval Runtime v0.1

> 什么时候应该想起这些？

---

## 1. Retrieval Gate

```
Conversation → Need Detection → Memory Access Check → Persona Filter → Response
```

普通生活问题 → 不调用深层记忆。

---

## 2. Memory Relevance Ranking

```
1. Current Relevance
2. User Permission Level
3. Time Validity
4. Stability
5. Privacy Risk
```

---

## 3. Memory Gravity Score

```
Gravity = Relevance × Consent × Stability ÷ Privacy Risk
```

越敏感的信息，越难自动进入回答。

---

## 4. Retrieval Decay

- Natural: 24h 衰减
- Preference: 长期 + 定期验证
- Emotional: 不永久冻结
