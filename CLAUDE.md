# 唐先生 项目规范

> 本项目遵循顶层 CLAUDE.md 中的记忆恢复协议和任务执行 SOP，但有以下专门约定。

## 协作协议

本项目采用 **Git 作为唯一事实来源（Single Source of Truth）** 的协作模式。

```
你（Founder）— 愿景、商业、最终决策
  │
  ├── ChatGPT（首席架构师）— 设计、架构、文档沉淀、一致性审查
  │
  └── Claude Code（首席工程师）— 按已确认设计实现代码
        │
        └── 共同同步 → Git Repository
```

所有 AI 工作前启动顺序：
1. `docs/00_governance/` — 了解项目法律（AI 不得擅自修改 governance 文件）
2. `docs/01_vision/` — 理解项目方向
3. `docs/02_decisions/` — 了解已确认决策
4. `docs/03_specs/` — 了解具体规范
5. `src/` — 开始实现

## 工作启动协议（不可违背）

此协议已由 ADR-0033 Frozen State Recovery Protocol 取代。

每次启动后，按以下顺序恢复：

```
1. `PROJECT_STATE_SNAPSHOT.md`                  ← 唯一入口，Frozen State
2. `docs/02_decisions/ADR-0033-frozen-state-recovery-protocol.md`  ← 恢复协议
3. 当前 Phase 文档                              ← 仅未完成 Phase
```

**不加载：** 已冻结 ADR 全文、Scenario、Wisdom Patterns、历史聊天、Review、旧版文档。

完整治理体系位于 `docs/`：
- `AI_WORKFLOW_PROTOCOL.md` — 主协议（必须读取）
- `SCENARIO_CREATION_GUIDE.md` — Scenario 创建规则
- `WP_MASTER_INDEX_USAGE.md` — WP 治理规范
- `RUNTIME_UPDATE_PROTOCOL.md` — Runtime 更新规范
- `CLAUDE_CODE_GOVERNANCE_PROTOCOL.md` — AI 协作协议
- `CLAUDE_CODE_DAILY_CHECKLIST.md` — 日常执行清单
- `TANG_PERSONA_SYSTEM_AUDIT.md` — 人格审计协议
- `RESPONSE_STYLE_GUIDE.md` — 表达风格规范

## 核心流程（不可违背）

### 设计优先
- `docs/` 是本项目最重要的资产
- **没有对应的 Decision Record，不得编写核心业务代码**
- 代码必须与设计文档保持一致；发现冲突时提 Conflict Report，不自行决定

### 标准化工作流
| 步骤 | 谁做 | 产出 |
|---|---|---|
| Step 1 | 你提出需求 | 讨论议题 |
| Step 2 | ChatGPT 分析/设计 | ADR + Spec |
| Step 3 | **Claude Code 实现** | 代码 + Commit |
| Step 4 | ChatGPT Review | Review Report |
| Step 5 | 你 Accept | 最终决策 |

### 实现流程（Claude Code 职责）
1. 读取最新 Vision + ADR + 相关 Spec
2. 规划实现方案
3. 实现代码 + 对应测试
4. 自我验证
5. 提交 Commit（消息格式：`feat(module): description`）
6. 更新 auto-resume.md 和 WORKING_MEMORY.md

### 文档同步规则
| 变更类型 | 目标路径 |
|---|---|
| 项目法律/规范 | `docs/00_governance/`（AI 不得擅自修改） |
| 愿景/原则变更 | `docs/01_vision/` |
| 新增决策 | `docs/02_decisions/ADR-XXXX-name.md` |
| 架构变更 | `docs/03_specs/architecture/` |
| 角色设定变更 | `docs/04_characters/` |
| 记忆系统变更 | `docs/03_specs/memory/` |
| 角色模板变更 | `docs/03_specs/character/` |
| 设计评审 | `docs/05_reviews/REVIEW-NNNN-topic.md` |

### 铁律
- 不改无 Decision 的核心逻辑
- **不擅自做产品设计决策** — 发现设计冲突必须报告，等确认后再改
- 每阶段结束前问："如果今天停止，这个版本有独立价值吗？"
- 每次讨论结束必须产生一个 Commit
- 所有完成的功能必须可追溯到某份 ADR 和 Spec
