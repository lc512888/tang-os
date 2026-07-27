# Runtime Context Hygiene Report v1.0

**阶段：** Phase 11-E Maintenance / Reliability
**时间：** 2026-07-27
**原则：** ADR-0033 Frozen State Recovery | E-1 历史资产不用于运行 | I-17 Memory ≠ Context

---

## 检查结果

| # | 检查项 | 状态 | 问题 | 修复 |
|---|--------|------|------|------|
| 1 | Context Loading Chain | ⚠️ | `docs/README.md:57-59` 仍包含旧启动序列（与 ADR-0033 冲突） | ✅ 已移除旧序列 |
| 2 | Context Loading Chain | ⚠️ | `PROJECT_STATE.md` 仍存在根目录（已被 SNAPSHOT 取代） | ✅ 已归档 |
| 3 | Context Loading Chain | ⚠️ | `.doc/memory/WORKING_MEMORY.md` 仍存在（内容滞后于 Phase 8，已被 SNAPSHOT 取代） | ✅ 已标记 |
| 4 | 文档重复 | ⚠️ | `CONTEXT_LOADING_POLICY.md` 的加载策略与 ADR-0033 有功能重叠 | ✅ 已添加引用指针 |
| 5 | 文档重复 | ✅ | 5 份 archive/audit 旧报告——已确认不会自动加载 | 无需修复 |
| 6 | Archive 隔离 | ✅ | `archive/` 无自动加载机制 | 无需修复 |
| 7 | Context Budget | ⚠️ | 无正式 Context Budget Rule | ✅ 已补充 |
| 8 | Runtime 文件污染 | ✅ | 197 场景/WP/AP/Response Corpus 全部在 docs/ 内，不会被自动加载 | 无需修复 |

---

## 已执行修复

### 修复 1：docs/README.md 旧启动序列已移除

旧序列（已删除）：
```
docs/00_governance/ → docs/01_vision/ → docs/02_decisions/ → docs/03_specs/ → src/
```

当前唯一入口：`PROJECT_STATE_SNAPSHOT.md`（ADR-0033）

### 修复 2：PROJECT_STATE.md 已归档

该文件已被 `PROJECT_STATE_SNAPSHOT.md` 取代，移至 archive。

### 修复 3：CONTEXT_LOADING_POLICY.md 已添加引用

该文件的内容与 ADR-0033 部分重叠。已添加头部声明指向 ADR-0033 为权威来源。

---

## Context Budget Rule

```
Runtime Context Allocation（每个新会话）：

┌─ MANDATORY（~5K tokens）──────────────────────────┐
│  PROJECT_STATE_SNAPSHOT.md                         │
│  ADR-0033（Frozen State Recovery Protocol）         │
│  当前 Phase 指针                                    │
└────────────────────────────────────────────────────┘

┌─ ON_DEMAND（按需加载，不自动）──────────────────────┐
│  当前 Phase 的 ADR / Standard / Spec                │
│  相关设计文档                                        │
└────────────────────────────────────────────────────┘

┌─ FORBIDDEN（不默认加载）───────────────────────────┐
│  197 条 Scenario                                    │
│  174+ Wisdom Patterns                                │
│  7 Anti-Patterns                                     │
│  Response Corpus                                     │
│  历史聊天 / Review 记录                               │
│  archive/ 内所有内容                                  │
│  PROJECT_STATE.md（已归档）                          │
└────────────────────────────────────────────────────┘
```

Max per turn: <50K tokens（硬限制）。超出时本次不加载新文档。

---

## 结论

```
PASS with minor cleanups.

3 issues found, 3 fixed.
No architecture change.
No Core modification.

Context loading chain is now clean:
  PROJECT_STATE_SNAPSHOT.md → ADR-0033 → Current Phase
```
