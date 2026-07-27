# ADR-0020: Tang OS Deployment Model

**日期：** 2026-07-26
**状态：** Accepted
**决策：** B — System-Level Companion Runtime
**影响范围：** 工程架构、Permission 模型、设备能力

---

## 背景

Phase 7-E 开始涉及真实设备能力（GPS/电话/SMS/麦克风/后台运行）。部署架构选择会影响：

- 权限模型
- 紧急响应能力
- 隐私边界
- 工程复杂度

---

## 候选方案

| 方案 | 说明 | 优势 | 风险 |
|---|---|---|---|
| A 独立 App | 标准手机应用 | 开发快、分发简单 | 权限受限、后台困难 |
| B 系统级 Companion | 深度集成 OS | 权限完整、响应快 | 工程量大、平台依赖 |
| C Hybrid | App + Trusted Runtime | 平衡 | 架构复杂 |

---

## 建议

Phase 7-E 基于 Hybrid 模型设计，优先实现核心 Runtime 能力。
