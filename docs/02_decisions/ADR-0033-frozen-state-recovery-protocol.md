# ADR-0033: Frozen State Recovery Protocol

**日期：** 2026-07-27
**状态：** Accepted
**影响范围：** 所有新会话启动流程、上下文加载策略、Claude Code 工作流程
**违反前例：** Phase 8 完成后因无此协议，新会话加载完整历史导致 1,019,079 tokens 满载

## 背景

Tang OS 已完成 Phase 1-8，累计 30 条 ADR、30 条 Invariant、197 条 Scenario、174+ Wisdom Patterns。每次新会话启动时，AI 面临两个极端：

- **极端 A：** 加载全部历史 → 上下文满载，无法工作
- **极端 B：** 零加载 → 像接陌生项目，重新理解和验证

根本原因：**架构状态已冻结，但恢复协议未冻结。**

## 决策

### 核心原则

> **已冻结阶段默认可信。恢复时只恢复状态，不重新设计。**
>
> **Frozen artifacts are authoritative unless a new ADR explicitly supersedes them.**

这条原则的含义：已冻结的 ADR、Invariant、Phase 产出在 Tang OS 生命周期中保持为公理，不作为每次启动的讨论对象。如需修改，必须提交新 ADR 明确 Supersede 旧决策。

### 冻结分级

| 等级 | 定义 | 资产 | 恢复动作 |
|------|------|------|---------|
| F0 — 已接受 | 不可修改，不可质疑 | ADR-0001~0030, I-1~I-30, E-1 | 仅记录存在，不加载内容 |
| F1 — 已闭环 | 设计完成，仅用于验证 | Scenario 197 条，WP/KB | 不默认加载，按需引用 |
| F2 — 当前阶段 | 可修改，当前工作区 | 当前 Phase 文档 | 加载至工作上下文 |

### Recovery 序列（替代所有旧启动序列）

```
Session Start
    │
    ▼
Context Recovery Mode
    │
    ├── [MANDATORY] PROJECT_STATE_SNAPSHOT.md（唯一入口）
    │       └── 记录：冻结资产列表、当前 Phase、架构图
    │
    ├── [MANDATORY] 当前 Phase 文档
    │       └── 仅加载未完成 Phase 的相关文件
    │
    └── [FORBIDDEN] 以下不默认加载
            ├── 已冻结 ADR 全文（仅标题引用）
            ├── Scenario / WP / AP
            ├── 历史聊天 / Review / 测试日志
            └── 旧版本文档

    完成上述步骤后，输出 Current Phase Pointer 并继续。
```

### 禁止行为清单

| 禁止 | 原因 |
|------|------|
| 重新验证已冻结阶段 | 违反 F0 可信原则 |
| 重新设计已完成的架构 | 违反 F0 冻结契约 |
| 从历史聊天重建上下文 | 违反 I-17 Memory ≠ Context |
| 重复生成已存在的文档 | 浪费上下文，制造混淆 |

### 允许行为清单

| 允许 | 条件 |
|------|------|
| 后台维护（去重/归类） | 不阻断主线，作为独立任务 |
| 发现冻结资产间的冲突 | 提交 Conflict Report，不自行修改 |
| 新 Phase 设计 | 基于冻结状态继续，不从零开始 |

## 原因

1. **避免重复劳动：** Phase 1-8 已累计大量设计资产，重新验证浪费 80%+ 上下文
2. **冻结可信：** 所有 ADR 已 Accept，Invariant 已闭环，无理由怀疑其有效性
3. **上下文容量约束：** Tang OS 知识库（197 SV + 174 WP + 30 ADR + 30 I）已远超单次上下文窗口，必须按需加载
4. **工程纪律 E-1 的强制要求：** 历史资产用于证明，不用于运行

## 影响

### 正面
- 新会话从 1M tokens → ~5K tokens 起步
- 消除"每次像接陌生项目"的认知偏差
- 冻结资产 100% 可信，无需反复确认

### 负面
- AI 首次接触某些冻结资产时可能缺乏深度上下文 → 通过按需加载补充
- 需要在 SNAPSHOT 中维护准确的冻结资产清单 → 每个 Phase 完成时更新

## 后续决策依赖

- 将此协议写入 CLAUDE.md 替代现有启动序列
- 更新 .claude/auto-resume.md 指向本协议
- 每个 Phase 闭环时更新 PROJECT_STATE_SNAPSHOT.md 的冻结状态
