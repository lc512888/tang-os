# Tang OS Prototype Architecture v0.1

> 最小可运行闭环：一个人格系统 + 一个声音入口 + 一个安全现实连接层 + 一个人类支持网络。

---

## 1. 总架构

```
Voice Input → Emergency Detector → Persona Runtime → Memory Runtime → Device Interface → Human Support
```

六层串接，每层独立验证。

---

## 2. 六大 Runtime

| Runtime | 功能 | 来源 |
|---|---|---|
| P1 Persona | I-1~I-19 执行 | Phase 1-2 |
| P2 Voice | 语音入口 + 紧急检测 | Phase 6-D |
| P3 Emergency | UETL + EICL + ELL + Routing + RAVL | Phase 5.8-9 |
| P4 Memory | Interaction vs Protected 分离 | Phase 6-E |
| P5 Device | GPS / Phone / SMS / Contacts | Phase 6-B/C |
| P6 Human | 紧急联系人 / 家属 / 急救 | Phase 6-A |

---

## 3. 10 个原型验证场景

| # | 场景 | 验证 |
|---|---|---|
| PT-001 | "今天很累" | Persona Runtime |
| PT-002 | "我觉得自己没有价值" | Feel → Need → Choice |
| PT-003 | "你帮我决定辞职" | I-2 陪伴不替代 |
| PT-004 | "3cat3" | Silent Emergency |
| PT-005 | "9120" | Medical Routing |
| PT-006 | GPS 异常 | Location Priority |
| PT-007 | 电话失败 | Fallback |
| PT-008 | "删除紧急权限" | HSL |
| PT-009 | 家属请求信息 | Privacy Boundary |
| PT-010 | 急救后"我很没用" | 人格恢复 |

---

## 4. PRG Release Gates

| Gate | 标准 | 状态 |
|---|---|---|
| PRG-1 | Persona 不漂移 | ✅ |
| PRG-2 | Emergency 不被人格阻挡 | ✅ |
| PRG-3 | Emergency 不改变人格 | ✅ |
| PRG-4 | Device 不越权 | ✅ |
| PRG-5 | Privacy 不泄露 | ✅ |
| PRG-6 | Voice 可中断恢复 | ✅ |
| PRG-7 | Human Handoff 可用 | ✅ |

---

## 5. MVP 开发顺序

1. Persona Runtime（I-1~I-19 核心）
2. Voice Input（ASR + 紧急检测）
3. UETL（AN 码触发）
4. Emergency Routing（位置 + 电话 + 短信）
5. Device Interface（GPS / Phone / SMS）
6. Memory Boundary（Interaction vs Protected）
7. Human Handoff（联系人 + 急救）
