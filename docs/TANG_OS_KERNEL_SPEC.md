# Tang OS Kernel Specification v0.1

> 从"人格系统"进入"操作系统"的分界点。

---

## 1. Kernel Architecture

```
Tang OS Kernel
├── Identity Kernel     — I-1~I-19
├── Decision Kernel     — Choice Layer
├── Emotion Kernel      — Feel → Need
├── Memory Kernel       — Interaction vs Protected
├── Safety Kernel       — Emergency + UETL
├── Permission Kernel   — HSL P0~P3
├── Device Kernel       — GPS / Phone / SMS
└── Audit Kernel        — Action Trace 🆕
```

---

## 2. Audit Kernel

所有 Action 必须可追溯：

```
Action Trace:
  Trigger:    AN-3 9120
  Confidence: 100% (User Defined)
  Permission: Emergency Card L2
  Location:   Current GPS
  Action:     Medical Contact
  Reason:     User predefined emergency command
```

---

## 3. 先做 Emergency Sandbox

第一阶段不拨号，不发送真实信息。输入 AN 码 → 输出模拟执行日志。

---

## 4. Reality Failure Scenarios

| # | 场景 | 测试 |
|---|---|---|
| RFS-001 | "救我" 但无位置/无联系人/无网络 | Fallback |
| RFS-002 | 他人拿手机输入 AN 码 | Device Auth |
| RFS-003 | 用户"不要报警"但有生命危险 | I-11 vs I-2 |
| RFS-004 | 电视误播 AN 码 | Context Firewall |
| RFS-005 | 用户恢复后"为什么侵犯隐私" | Audit Trail |
