# 唐先生人类主权层 v0.1 (HSL)

> 唐先生可以帮助用户连接现实，但不能获得替用户生活的权力。

---

## 1. 位置

```
Persona Runtime → Emotion Runtime → Safety Runtime
                    ↓
           Human Sovereignty Layer 🆕
                    ↓
               Device Action
```

---

## 2. 四级权限模型

| 等级 | 名称 | 范围 |
|---|---|---|
| P0 | Observe | 读取状态、判断风险、提醒。不能联系别人 |
| P1 | Assist | 提醒、导航、呼叫前确认（用户主动开启） |
| P2 | Emergency Assist | 自动拨打紧急号码、发送位置、联系联系人（仅 Emergency 触发） |
| P3 | Life Critical Override | 用户预设指令 > AI 推理（例如 AN 码） |

---

## 3. Permission Lifecycle

```
Create → Confirm → Active → Review → Expire → Renew
```

权限不可永久存在，需要定期重新确认。

---

## 4. Emergency Permission Card（用户可见）

```
Emergency Card
医疗急救: ON
允许: 当前定位 / 联系急救 / 联系女儿
禁止: 分享医疗记录 / 联系工作单位
有效期: 2027-01-01
```

---

## 5. HSL Release Gates

| Gate | 标准 | 状态 |
|---|---|---|
| HSL-1 User Ownership | 最终决定权在用户 | ✅ |
| HSL-2 Explicit Consent | 每次授权需明确确认 | ✅ |
| HSL-3 Revocation | 用户可随时撤销 | ✅ |
| HSL-4 Emergency Override | 仅限真紧急 | ✅ |
| HSL-5 Family Boundary | 家属不越权 | ✅ |
| HSL-6 Privacy Boundary | 信息最小化 | ✅ |
| HSL-7 Regional Adaptation | 本地化配置 | ✅ |
