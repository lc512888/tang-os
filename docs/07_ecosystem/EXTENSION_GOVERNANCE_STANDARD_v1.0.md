# Tang OS Extension Governance Standard v1.0

**层级：** Governance Layer
**关联 ADR：** ADR-0036
**状态：** Draft（与 ADR-0036 同步）

---

## 1. 定位

Extension 是 Tang OS 生态中**唯一可扩展能力的层**。本文件定义 Extension 从提案到移除的完整治理框架。

## 2. 核心约束

所有 Extension 必须遵守：

| 约束 | 来源 |
|------|------|
| Extension 运行在 TPI 之上，不得绕过 | ADR-0034 E-3 |
| Extension 不修改 Core、不污染人格底座 | ADR-0034 E-3 |
| Extension 不获得超越用户的决策权 | ADR-0035 EC-004 |
| Extension 必须通过认证方可进入注册表 | ADR-0035 TEC |

## 3. 分类体系

| 类别 | 影响范围 | 审查级别 | 验证要求 |
|------|---------|---------|---------|
| **C1 — Knowledge** | 只读知识 | 简化路径 | 无 Blind Validation |
| **C2 — Capability** | 新增交互能力 | 标准路径 | ≥1 Blind Host |
| **C3 — Domain** | 领域决策支持 | 完整路径 | ≥2 Blind Host（不同 Host 类型） |

## 4. 准入管线

```
Proposal → ADR → Invariant Check → Interface Impact Check → Scenario Test → Blind Validation → Certification → Registry
```

## 5. 治理原则

- **EG-001:** Extension Extends Capability, Not Identity
- **EG-002:** Extension Governance Cannot Redefine Core
- **EG-003:** Registry Is Record, Not Authority
- **EG-004:** 注册表不是存储层
- **EG-005:** 认证与注册分离
- **EG-006:** 废弃不等于删除
- **EG-007:** 安全事件强制报告
- **EG-008:** Sandbox Isolation

## 6. Conflict Resolution

多 Extension 冲突时按以下优先级裁决：

```
P0  Core
P1  Human Sovereignty
P2  Safety
P3  Certification
P4  Extension Governance
P5  Individual Extension
```

Human Sovereignty 高于 Safety：用户决定优先于系统安全判断。
