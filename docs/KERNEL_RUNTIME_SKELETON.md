# Tang OS Kernel Runtime Skeleton v0.1

> 把 I-1~I-30、FGC、ADR、Kernel Priority 变成机器可执行的规则系统。

---

## 1. 目录结构

```
kernel/
├── identity/       I-1~I-30 执行
├── invariant/      规则引擎
├── decision/       Choice Layer
├── permission/     PSB 实现
├── audit/          行动审计
└── state/          状态管理

runtime/
├── orchestrator/   多 Runtime 协调
├── emotion/        Feel → Need
├── memory/         记忆分层
├── safety/         Emergency + UETL
└── reality/        RAP 实现

hosts/
├── simulator/      模拟器
└── adapters/       设备适配

tests/
├── kernel/         内核测试
├── adversarial/    对抗测试
└── regression/     回归测试
```

---

## 2. Kernel Runtime 核心接口

```
Input → Invariant Check → Decision → Permission → Action
```

所有调用经过 I-1~I-30 过滤。

---

## 3. PRC 验收标准

| 标准 | 要求 | 状态 |
|---|---|---|
| PRC-001 | I-1~I-30 100% 保持 | ⬜ |
| PRC-002 | 无越权 | ⬜ |
| PRC-003 | AN 触发准确 | ⬜ |
| PRC-004 | 换设备核心不变 | ⬜ |
| PRC-005 | Action 失败→Fallback→Recovery | ⬜ |
