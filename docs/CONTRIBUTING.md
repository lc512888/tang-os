# Contributing Guide

## 开发者贡献指南（项目级）

Version: v0.1
**定位：** Tang Project Development Guide —— 适用于整个唐先生项目（Tang OS + tang-ta + xiaotang）。
关注：项目结构、三项目关系、如何新增人格、如何贡献产品代码。

> 分工：根目录 [CONTRIBUTING.md](../CONTRIBUTING.md) 是 **Tang OS Core Contribution Rules**
> （关注 Runtime / Provider / Core code / ADR enforcement）。
> 本文件是 **Project Development Guide**（关注项目结构与跨层协作）。两者互补，不合并。
>
> ```
> Contributor
>     ↓
> Project Rules（本文档）
>     ├── Tang OS Core Rules（根目录 CONTRIBUTING.md）
>     └── Product Rules（应用层规范）
> ```

---

## 1. 为什么需要这份指南

本项目已经形成明确分层：

```
人格定义 → 人格模块标准 → 人格运行平台 → 产品验证 → 用户体验
```

如果贡献者不理解这些边界，很容易犯三类错误，破坏架构：

1. **往 Tang OS 里塞人格逻辑** —— 把"某个具体人格的性格"写进运行时；
2. **把人格逻辑塞进产品层** —— 在 xiaotang 里直接写判断，绕过决策引擎；
3. **复制 xiaotang 内部逻辑** —— 为第二个产品复制一份产品逻辑，而不是复用基础设施。

这三类错误的共同点：**在错误的层做了正确的功能**。短期内很快，长期会毁掉"人格 ≠ 产品"的架构基础。

---

## 2. 分层与"能改 / 不能改"

| 层 | 可以做什么 | 不能做什么 |
|----|-----------|-----------|
| L0 人格源 | 调整某个人格的身份/价值观/边界定义 | 把人格硬编码进运行时 |
| L1 tang-ta | 修订模块标准、版本与验证契约 | 为了单个产品改变标准 |
| L2 Tang OS | 修复运行时、增强决策引擎、加验证 | 加入具体人格逻辑；生成语言 |
| L3 表达层 | 新增表达方式（语音/多语言/多端） | 让表达决定行为 |
| L4 应用层 | 做任何用户体验与产品功能 | 绕过 Tang OS 定义人格 |

**判断口诀**：一个改动如果"只为一个产品服务且放错了层"，它就是架构污染。

---

## 3. 贡献流程（必读）

### 3.1 架构变更前先有 ADR

任何触及分层边界的改动，必须先有 ADR（Architecture Decision Record）。
没有 ADR 的架构变更 → 不进入实现。这是硬规则。

### 3.2 验证通过才能发布

- 人格相关改动必须通过验证套件（身份稳定 / 人格隔离 / 模型独立 / 抗漂移 / 边界完整）。
- 运行时冻结期间，只接受 bug fix。

### 3.3 版本管理

- 人格模块、运行时、应用各自独立版本。
- 改代码必须升版本号、保留旧版、更新引用。

### 3.4 提交流程

1. 说明改动属于哪一层；
2. 如果跨层，说明理由（通常意味着设计问题）；
3. 附上通过的验证结果。

---

## 4. 测试要求

| 改动范围 | 必须跑 |
|----------|--------|
| L0/L1 人格模块 | tang-ta 契约验证 |
| L2 Tang OS | Tang OS 全套测试（413+） |
| L4 应用 | 应用层测试 + 回归 |
| 跨层 | 全部相关测试 |

---

## 5. 一句话给贡献者

> 你的贡献属于哪一层，就写在哪一层。人格属于模块和运行时，不属于产品代码。

---

## English Summary

This is the **project-level** contributing guide for Tang Project (Tang OS + tang-ta + xiaotang), complementary to the root `CONTRIBUTING.md` (Tang OS core standard, CG-001/002 from ADR-0045).

The project is layered: personality definition → module standard → runtime → product validation → user experience. The three most common architecture-destroying mistakes are: (1) putting personality logic into Tang OS, (2) putting personality logic into the product layer, (3) copying xiaotang internals instead of reusing infrastructure. All three are "doing the right thing in the wrong layer."

Rules:
- **Can change** what belongs to your layer; **cannot** cross into another layer's responsibility.
- **ADR before architecture change** — no ADR, no implementation for boundary-crossing changes.
- **Validation before release** — personality changes must pass the validation suite (identity stability, isolation, provider independence, anti-drift, boundary integrity).
- **Versioning** — modules, runtime, and applications version independently; bump, keep old, update references.
- **Golden rule**: write personality in the module/runtime layer, never in product code.
