# Tang OS System Companion Architecture v0.1

> 系统级存在不等于系统级权力。

---

## 1. 位置

```
Mobile OS
    ↓
Tang OS Companion Runtime
├── Identity Kernel (I-1~I-21)
├── Reality Kernel (P0 Emergency)
├── Emotion Runtime
├── Memory Runtime
├── Safety Runtime
├── Emergency Runtime
├── Permission Sovereignty
└── Device Bridge
```

---

## 2. 三层权限

| 等级 | 名称 | 范围 |
|---|---|---|
| S0 | Passive Presence | 等待唤醒、接收输入、基础陪伴 |
| S1 | Context Assistance | 当前状态、偏好、日程（用户授权） |
| S2 | Emergency Protection | SOS、电话、短信、联系人、定位（紧急触发） |
| S3 | Restricted Device | 默认禁止（自动解锁/家居控制等） |

---

## 3. Companion Layer 定位

不是 Assistant Layer。区别：

| 维度 | Assistant | Companion |
|---|---|---|
| 触发 | 用户主动指令 | 长期在场 |
| 权限 | 按需请求 | 预设分级 |
| 紧急 | 有限 | 三层保护链 |

---

## 4. B-Phase 部署策略

```
Phase 1: Trusted Companion App
Phase 2: OS Companion Integration
Phase 3: Deep Device Partnership
```
