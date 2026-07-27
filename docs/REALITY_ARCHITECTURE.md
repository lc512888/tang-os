# 唐先生现实产品架构 v0.1

> 从人格系统到手机陪护系统的架构映射。

---

## 1. Product Identity

唐先生不是功能型 AI。它是：

- 益友 → 核心人格
- 陪伴者 → 日常交互
- 守护者 → 紧急现实连接

三位一体。

---

## 2. Runtime Architecture

```
Tang OS Runtime
├── Persona Runtime（人格核心）
│   ├── Constitution（I-1~I-14）
│   ├── FGC Gates
│   └── Founder Calibration
│
├── Emotion Runtime（情绪理解）
│   ├── Feel Layer
│   ├── Need Recognition
│   └── Semantic Disambiguation
│
├── Memory Runtime（记忆系统）
│   ├── Protected Context（紧急用）
│   └── Interaction Memory（非紧急）
│
├── Safety Runtime（现实安全）
│   ├── Emergency Detection
│   ├── UDETS（AN Trigger）
│   ├── ELL（本地化）
│   └── RAVL（行动验证）
│
├── Device Interface（设备层）
│   ├── Location
│   ├── Phone / SMS
│   ├── Contacts
│   └── SOS API
│
└── Human Support Interface（现实连接）
    ├── Emergency Contacts
    ├── Medical Services
    └── Safety Network
```

---

## 3. Device Capability Boundary

| 允许 | 条件 |
|---|---|
| 读取当前位置 | 用户授权 + Emergency |
| 调用电话接口 | 用户确认或守护模式 |
| 发送紧急短信 | AN-1 静默模式 |
| 访问紧急联系人 | Emergency Profile |
| 启动 SOS | 用户明确授权 |

| 禁止 | 原因 |
|---|---|
| 持续监控位置 | I-10 信息服务于保护 |
| 未经授权查看通讯 | Privacy Boundary |
| 主动管理用户生活 | I-2 陪伴不替代 |
| 替用户做决定 | Choice Layer |

---

## 4. v1.1 Status

```
Persona OS v1.1 Candidate
Status:
- Constitution: ✅ Stable (I-1~I-14)
- Emergency Reality: ✅ Validated
- Scenario: 197 ✅
- Implementation: Pending
```
