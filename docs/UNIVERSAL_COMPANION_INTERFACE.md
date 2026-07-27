# Tang OS Universal Companion Interface v0.1 (UCI)

> 任何未来智能设备如何成为 Tang OS 的身体，而不会改变 Tang OS 的灵魂。

---

## 1. 五类能力

| 编码 | 能力 | 示例 |
|---|---|---|
| C-001 | Perception | 声音/图像/位置/生理/环境 |
| C-002 | Communication | 电话/信息/网络/联系人 |
| C-003 | Mobility | 导航/移动机器人/车辆 |
| C-004 | Interaction | 屏幕/语音/机器人动作/表情 |
| C-005 | Protection | SOS/紧急联络/避险动作 |

---

## 2. Reality Action Request (RAR)

```
RAR = { Intent, Reality Goal, Required Capability, Risk Level, Permission, Audit }
```

AN-3 不再是"拨打120"，而是：

```
Intent: Medical Emergency Assistance
Goal: Connect user to emergency medical support
Required: C-002 Communication + Location
```

宿主决定执行方式（Phone Call / Robot Hub / Vehicle System）。

---

## 3. I-23 能力属于接口，不属于载体

Tang OS 不思考"我是一部手机里的 AI"，而是"我是运行于某个现实载体上的 Companion"。
