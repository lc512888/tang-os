# ADR-0005: 最高决策权

**日期：** 2026-07-20
**状态：** Accepted
**替代者：** —
**影响范围：** 项目治理、所有 AI 的行为边界、ADR 修改流程

## 背景

Design Session 005 提出：随着项目推进，ChatGPT、Claude Code、以及未来的 Codex/Cursor 等 AI 都可能提出不同建议。如果没有明确的决策权规则，项目会"谁上下文最长谁说了算"，导致方向摇摆。

## 决策

### 1. 最高决策权归属

Founder（你）是项目唯一拥有最终决策权的人。

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

### 2. AI 只有建议权，没有决策权

所有 AI（ChatGPT、Claude Code、未来的 Codex/Cursor 等）只能：
- **提议**（Propose）
- **建议**（Recommend）
- **报告风险**（Report Risk）
- **提交冲突**（Submit Conflict Report）

不能：
- **自行决定产品方向**
- **推翻已定决策**

### 3. 已 Accepted 的 ADR 不可由 AI 自行修改

任何 AI 不得自行修改已经 Accepted 的 ADR。

修改流程：
```
AI 发现需要修改
  → 提交 Proposal / Supersede ADR-NNNN
  → 等待 Founder 决定
  → Accept 或 Reject
```

## 原因

- 长期项目中，AI 的上下文长度和记忆能力不统一，容易产生"谁上下文最长谁说了算"的局面
- 产品方向的一致性需要唯一的决策锚点
- AI 可以参与设计、实现、Review，但决策权应始终属于人

## 影响

- 所有 AI 的角色明确为"建议者"而非"决策者"
- 已 Accepted 的 ADR 受保护，修改需正式流程
- 项目治理结构完整：Governance → Vision → Decisions → Specs → Code
- COLLABORATION_PROTOCOL.md 需同步更新

## 后续决策依赖

无。
