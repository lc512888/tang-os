# 唐先生 · Context 加载策略

> 生成时间：2026-07-27
> 来源：I-17 (Memory ≠ Context) + I-19 (Emergency Context ≠ Memory) + E-1 (历史资产不用于运行)
> 目标：从"历史驱动"恢复为"状态驱动"
> 权威来源：ADR-0033 Frozen State Recovery Protocol（本文档为 ADR-0033 的工程细则，不替代 ADR-0033）

---

## ⚠️ 当前冲突

项目中有 **三套互相矛盾的启动序列**：

### 序列 A — `CLAUDE.md`
```
1. docs/AI_WORKFLOW_PROTOCOL.md  ← 首要读取
2. PROJECT_STATE.md               ← 当前项目状态
3. .claude/auto-resume.md         ← 会话恢复点
4. .doc/memory/WORKING_MEMORY.md  ← 工作记忆
```

### 序列 B — `PROJECT_STATE_SNAPSHOT.md`
```
"唯一入口。新会话首次读取此文件，不加载任何历史。"
```

### 序列 C — `.claude/auto-resume.md`
```
1. PROJECT_STATE_SNAPSHOT.md   ← 唯一入口
2. docs/00_governance/         ← 项目法律
3. 当前阶段文件（Phase 8 设计文档）
```

**结论：** 三部文件定义了三个不同的启动序列。这是上下文溢出的根因之一。

---

## 修复后统一加载策略

### 启动时必须加载（MANDATORY）

| # | 资产 | 原因 | 引用 |
|---|------|------|------|
| 1 | `PROJECT_STATE_SNAPSHOT.md` | 当前项目状态快照 | **唯一入口** |
| 2 | `docs/00_governance/` (4 files) | 项目法律/术语/命名/协作 | AI 工作前必须了解 |
| 3 | `docs/02_decisions/` (Current ADR) | 当前未完成的 ADR/已冻结 ADR 列表 | 决策指引 |
| 4 | `CLAUDE.md` | 项目规范 | 行为约束 |

### 按需加载（ON_DEMAND — 只在相关任务时加载）

| 资产 | 加载条件 |
|------|---------|
| `docs/01_vision/` | 当需要理解项目方向或做出决策时 |
| `docs/03_specs/architecture/` | 当需要修改或实现架构时 |
| `docs/03_specs/character/` | 当需要修改人格定义时 |
| `docs/04_characters/唐先生/` | 当需要修改角色时 |
| `docs/03_specs/memory/` | 当需要修改记忆系统时 |
| Phase 8 具体实现文档 | 当继续 Phase 8 开发时 |

### 禁止默认加载（FORBIDDEN）

| 资产 | 原因 |
|------|------|
| 全部 Scenario（197 条） | 仅在验证/设计讨论时需要，属于历史资产 |
| 全部测试日志 | 仅回归验证时加载 |
| 历史聊天记录 | I-17: Memory ≠ Context |
| 旧版本文档 | 仅 E-1 回溯验证时加载 |
| 执行日志 / Review 记录 | 仅审计时需要 |
| `docs/response_corpus/` | 仅风格学习时需要 |
| `docs/wisdom_patterns/` (174+ 条) | 仅设计/验证时需要 |
| `docs/anti_patterns/` | 仅审计时需要 |
| `PROJECT_STATE.md` | 已被 SNAPSHOT 取代 |
| `.doc/memory/WORKING_MEMORY.md` | 内容合并入 SNAPSHOT |

### 已冻结 / 只读资产（FROZEN — 不加载，仅记录存在）

| 资产 | 状态 |
|------|------|
| ADR-0001~0030 (全部 Accepted) | 已冻结，不可修改。启动 ADR-0031+ 需提交 Proposal |
| I-1~I-30 (全部 Core Invariants) | 已闭环，不可修改 |
| E-1 (Engineering Invariant) | 已确认，不可违背 |
| Scenario 197 条 | 设计完成，仅用于验证 |

---

## 恢复后新会话启动序列（STANDARDIZED）

```
Session Start
    │
    ▼
确认进入 Context Recovery Mode
    │
    ▼
[MANDATORY] 读取 PROJECT_STATE_SNAPSHOT.md（唯一入口）
    │
    ▼
[MANDATORY] 读取 docs/00_governance/（项目法律）
    │
    ▼
[ON_DEMAND] 根据任务选择加载：
    ├── 修改架构 → docs/03_specs/architecture/
    ├── 实现代码 → src/ + 相关 spec
    ├── 设计讨论 → docs/01_vision/ + 02_decisions/ + 相关 spec
    ├── 验证 → 相关 Scenario + WP
    ├── 审计 → 相关 docs + review records
    └── 其他 → 按需加载
```

## 违反惩罚

任何会话违反此协议导致上下文满载（接近 1M tokens）：
1. 回滚到上次 SNAPSHOT
2. 记录违规资产清单到 `PROJECT_STATE_SNAPSHOT.md` 的违规附录
3. 下个会话强制按本策略恢复
