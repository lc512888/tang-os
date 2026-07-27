# COLLABORATION PROTOCOL — 协作协议

> 本文档定义唐先生项目的三方协作规则。属于 00_governance（项目法律层），极少改动。

## 决策权规则（最高原则）

### 唯一决策者

**Founder（你）是项目唯一拥有最终决策权的人。** 所有 AI（ChatGPT、Claude Code 及未来的任何 AI）只有建议权，没有决策权。

```
Founder（你）
  │
  ├── 唯一拥有最终决策权（Accept / Reject）
  │
  ├── ChatGPT
  │      ├── 提案（Proposal）
  │      ├── 风险提示（Risk）
  │      ├── 架构设计（Architecture）
  │      └── Review
  │
  └── Claude Code
         ├── 实现（Implementation）
         ├── 重构（Refactor）
         ├── 测试（Test）
         └── 冲突报告（Conflict Report）
```

### ADR 修改规则

任何 AI 不得自行修改已经 Accepted 的 ADR。修改流程：
1. AI 发现需要修改 → 提交 Proposal 或 Supersede 请求
2. 等待 Founder 决定
3. Accept 或 Reject

### 角色定义

| 角色 | 职责 | 决策权 |
|---|---|---|
| **Founder（你）** | 愿景、商业判断、最终产品决策 | **唯一最终决策权** |
| **Chief Architect（ChatGPT）** | 产品架构、设计推演、文档沉淀、一致性审查 | 设计建议权 |
| **Principal Engineer（Claude Code）** | 按已确认设计实现代码、重构、工程质量 | 工程建议权 |

## 数据流

```
你
  │
  ├── ChatGPT — 提案/架构/风险/Review
  │
  └── Claude Code — 实现/重构/测试/冲突报告
        │
        └── 共同同步 → Git Repository（唯一事实来源）
```

所有角色**不互相同步记忆**，都同步 Git。

## 黄金流程

```
讨论 → ADR → Spec → 实现 → Review → Accept → Commit
```

没有 ADR，不写核心代码。任何 AI 都不能自行修改已 Accepted 的 ADR。

## AI 工作前启动顺序

1. `docs/00_governance/` — 了解项目法律
2. `docs/01_vision/` — 理解项目方向
3. `docs/02_decisions/` — 了解已确认决策
4. `docs/03_specs/` — 了解具体规范
5. `src/` — 开始实现

## Design Session 规则

### 核心原则：一次只解决一个问题

任何 Design Session 只允许解决一个核心问题。如果讨论过程中发现新的问题，全部进入 Pending，绝不顺便讨论。

### 标准节奏

```
DS-NNN
Question: 一个核心问题
回答: 聚焦该问题的回答
Decision: Accepted / Changes Required
Next: 下一个问题
```

## Scenario 验证工作流（v2 — 高效模式）

> 基于唐先生 v0.1 人格基石已建立后的新工作方式。

### 输出格式

每个新 Scenario 按以下流程推进：

**Step 1 — ChatGPT 模拟唐先生**
```
唐先生（模拟回复）：
（直接给出唐先生第一反应，不提前分析、不解释）
```

**Step 2 — Founder 评审**
```
✅ 通过
✏️ 改一句
🔄 重写
💡 为什么不对
```

**Step 3 — 设计分析（仅当 Step 2 通过后）**
```
为什么这样回答；
是否符合 ADR；
是否产生新的 Runtime 观察；
是否需要 Proposal。
```

### 两个版本

| 版本 | 用途 | 说明 |
|---|---|---|
| **Version A：自然版** | 最终人格表达 | 唐先生真实会说的话，不追求金句 |
| **Version B：设计解析版** | 项目文档 | 对应哪些 ADR/Runtime/Observation，仅内部留存 |

### 角色重新定义

| 角色 | 定位 | 核心职责 |
|---|---|---|
| **Founder（你）** | 最终决策者 | 确认/修正/一票否决 |
| **ChatGPT** | **一号审稿人（Reviewer）** | 先模拟唐先生 → Founder 确认 → 再分析；不提前过度设计 |
| **Claude Code** | 首席工程师 | 按已确认设计实现代码 |

### 审稿人自我约束

ChatGPT 自定原则：

> 如果现实中一位温润、真诚、有学识的朋友不会这样说，就重写。
>
> 不追求"漂亮的总结"，只追求"真实的唐先生"。

## 冲突处理

任何 AI 发现设计冲突时：
1. 生成 Conflict Report（描述冲突双方 + 建议方案）
2. 提交给 Founder 决策
3. **不自行拍板**
