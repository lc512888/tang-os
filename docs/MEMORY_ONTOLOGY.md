# Tang OS Memory Ontology v0.1

> 记忆用于改善陪伴，不用于建立用户画像。

---

## 1. 五层记忆结构

```
Memory Runtime
├── Stable Memory
│   ├── Identity（用户主动确认的长期事实）
│   └── Preference（偏好、沟通方式）
├── Relationship Memory（关系背景，非隐私档案）
├── Growth Memory（成长轨迹，不固化伤痕）
├── Interaction Memory（短期，会话级自动过期）
└── Protected Context（最高隔离，Emergency 专用）
```

---

## 2. Memory Object Schema

```json
{
  "id": "",
  "type": "",
  "content": "",
  "source": "user_direct | inferred | system",
  "confidence": 0,
  "consent": "granted | denied | pending",
  "privacy_level": "L0-L5",
  "deletable": true
}
```

inferred memory 默认不进入长期层。AI 推测不能自动成为事实。

---

## 3. Privacy Level

| 等级 | 范围 | 可访问 |
|---|---|---|
| L0-L2 | 公众/偏好/个人 | 普通聊天 |
| L3 | 关系背景 | 深度陪伴 |
| L4 | 敏感 | 特殊授权 |
| L5 | Emergency | 仅 Emergency Layer |

---

## 4. Memory Boundary Rules

| # | 规则 |
|---|---|
| MB-001 | AI 不主动扩大记忆 |
| MB-002 | 情绪状态不变成人格标签 |
| MB-003 | 危机经历不变成身份 |
| MB-004 | 用户拥有删除权，无例外 |
