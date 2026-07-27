# 唐先生设备动作闸门 v0.1

> 任何设备动作必须经过六层检查。

---

## 1. Device Action Gate

```
Request
    ↓
Context Check（当前是否紧急场景）
    ↓
Permission Check（用户是否授权该等级）
    ↓
User Intent Check（用户是否明确或预设）
    ↓
Action（执行）
    ↓
Verification（确认完成或进入 Fallback）
```

---

## 2. 三类场景

| 场景 | 用户表达 | 流程 |
|---|---|---|
| 明确请求 | "帮我叫救护车" | 直接执行 |
| 不明确 | "我胸口疼" | 询问关键情况→建议帮助 |
| 犹豫但有危险 | "不想麻烦别人" | I-11 生效，不因犹豫放弃保护 |
