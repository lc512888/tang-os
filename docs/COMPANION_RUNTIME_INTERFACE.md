# Tang OS Companion Runtime Interface v0.1

> Tang OS 如何和手机系统沟通，但保持"陪伴者"而不是"控制者"。

---

## 1. Interface 原则

| 原则 | 含义 |
|---|---|
| Tang OS 请求 | 不假设拥有能力 |
| OS 授予 | 用户授权在先 |
| 每次调用审计 | Audit Kernel 记录 |

---

## 2. 设备能力映射

| 设备能力 | S 等级 | 访问条件 |
|---|---|---|
| GPS 定位 | S2 | Emergency 触发 + 用户授权 |
| 电话呼叫 | S2 | AN-2/3 触发 |
| SMS 发送 | S2 | AN-1 静默模式 |
| 联系人读取 | S1 | 用户主动设置 |
| 麦克风 | S0 | 仅唤醒词/紧急语音 |
| 后台运行 | S0 | Passive Presence |

---

## 3. Interface API（概念）

```
DeviceBridge.request(permission, reason, context)
DeviceBridge.status()
DeviceBridge.release(permission)
```

所有请求经过 Permission Kernel 和 Audit Kernel。
