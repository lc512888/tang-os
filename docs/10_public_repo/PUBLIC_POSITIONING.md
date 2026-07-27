# Tang OS Public Positioning v1.0

**层级：** Public Repository Layer
**来源：** ADR-0041 PS-001~005, ADR-0040 PRB-001~006

---

## 是什么

Tang OS 是一个**规范驱动的人格运行时框架**，用于在不同 AI 载体和扩展环境中保持身份一致性、伦理边界和能力治理。

## 不是什么

- ❌ AI 聊天机器人框架
- ❌ 数字人 SDK
- ❌ 情感陪伴引擎
- ❌ 人格模型训练工具
- ❌ Agent 框架

## 为什么存在

当前 AI 系统面临的核心问题不是"不够智能"，而是：
- 人格无边界：同一个 AI 在不同场景下行为不一致
- 能力无治理：Extension/Plugin 可以随意修改系统行为
- 身份无保护：用户无法确认 AI 是否"还是同一个"

Tang OS 解决的是：**AI 系统的身份连续性和行为可治理性。**

## 技术定位

```
Category: Personality Runtime Infrastructure
Stack: Specification → Reference Implementation → SDK → Validation
License: MIT
```

## 关键词（SEO）

- Personality Runtime
- AI Identity Governance
- Capability Admission Control
- Invariant Enforcement
- Cross-Host Personality Consistency
