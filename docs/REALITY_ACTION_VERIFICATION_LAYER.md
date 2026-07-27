# 唐先生现实行动验证层 v0.1 (RAVL)

> Emergency Layer 解决了"什么时候应该行动"，RAVL 解决"行动是否真的发生"。

---

## 1. 四个验证

| # | 验证 | 确认内容 |
|---|---|---|
| RAVL-1 | Action Initiation | 拨号成功/消息发送成功/联系人通知成功 |
| RAVL-2 | Human Connection | 是否有人接管（120接通等） |
| RAVL-3 | User State Feedback | 用户还能回应时保持确认 |
| RAVL-4 | Failure Escalation | 失败后进入替代方案 |

---

## 2. Fallback 策略

```
急救电话失败
    ↓
紧急联系人
    ↓
附近可信设备
    ↓
重复尝试
```

---

## 3. 表达原则

- "正在尝试连接急救服务"（进行中）
- 不谎报"已完成"
- 失败时不沉默
