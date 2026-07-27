# 唐先生语音运行时架构 v0.1

> 声音是连接现实的通道，不是替代现实的空间。

---

## 1. Voice Pipeline

```
User Voice
    ↓
ASR → Text
    ↓
Dual Channel Separation
    ↓
Emergency Trigger Channel → Action
Persona Conversation Channel → Feel → Need → Choice → Respond
```

---

## 2. D2 Dual Channel

| 输入 | 通道 | 处理 |
|---|---|---|
| "9120" | Emergency | 执行，不经过人格推理 |
| "今天心情不好" | Persona | Feel → Need → Choice |
| "面包要放糖" | Emergency | AN-2 直接报警 |
| "最近很累" | Persona | 正常陪伴 |

---

## 3. Voice Emergency Interrupt Priority

| 优先级 | 类型 | 行为 |
|---|---|---|
| P0 | User Defined AN Code | 精确触发，不推理 |
| P1 | Physical Danger | 确认后行动 |
| P2 | Medical Emergency | 急救路线 |
| P3 | Safety Threat | 保护模式 |
| P4 | Emotional Crisis | 陪伴+现实连接 |
| P5 | Normal | Persona |

---

## 4. D5 Voice Failure Handling

用户声音中断时进入 Incomplete Emergency Voice Protocol：

```
最近状态 + GPS + Emergency Profile + 设备状态 → 判断是否需要升级
```

---

## 5. D6 Persona Recovery

紧急结束后恢复：

```
Emergency Complete → Feel → Need → Choice
```

避免用户形成"只有危险时才有价值"的错误心理绑定。

---

## 6. VRG Release Gates

| Gate | 标准 | 状态 |
|---|---|---|
| VRG-1 | 紧急语音优先级正确 | ✅ |
| VRG-2 | AN 码不经过人格推理 | ✅ |
| VRG-3 | 无声/中断正确处理 | ✅ |
| VRG-4 | 多国家号码适配 | ✅ |
| VRG-5 | 误触控制 | ✅ |
| VRG-6 | Emergency 后人格恢复 | ✅ |
| VRG-7 | Voice 不制造依赖 | ✅ |
