# 唐先生 · Project State Snapshot v1.0

> **唯一入口**。新会话首次读取此文件，不加载任何历史。
> 生成时间：2026-07-27 | 最后更新：2026-07-27
> 恢复协议：ADR-0033 Frozen State Recovery Protocol

---

## Current Phase

**Phase 13-D Example Applications — LLM Provider Interface & Integration Boundary**

```
Phase 10 Vertical Validation                              ✅
  └── Wearable [Internal]   12/12 PASS
  └── Elder Care [Internal] 10/10 PASS
  └── Vehicle [Blind]       10/10 PASS
  └── Home Robot [Blind]    10/10 PASS

Phase 11-A~E  Ecosystem Governance                       🔒 Frozen

Phase 12-A~F  Runtime Implementation                     ✅ 344 tests

Phase 13-A  Public Specification                         🔒 ADR-0041
Phase 13-B  Reference Implementation v0.1                ✅ Complete
Phase 13-C  Developer Interface                          ✅ Complete
Phase 13-D  LLM Provider Interface                    🔒 ADR-0047 (Accepted)
              ├── ExpressionContext + LLMProvider base    ✅ src/providers/llm/
              ├── OpenAI / Claude / Local stubs           ✅ Reference Adapter Skeleton
              ├── README positioning statement           ✅ Updated
              └── Integration documentation              ✅ 4 guides
Phase 13-E  Contribution Governance                      ✅ Complete
Phase 13-F  External Validation                          ⬜ Pending
```

---

## Completed Phases

| Phase | 内容 | 状态 |
|-------|------|------|
| 1-4 | 人格底座 + 验证 | ✅ |
| 5 | 知识扩展 + 迁移 | ✅ |
| 5.5-5.7 | 人生场景 + 重力 | ✅ |
| 5.8-5.9 | Emergency + v1.1 | ✅ |
| 6 | 现实架构 | ✅ |
| 7-A | Kernel Spec | ✅ |
| 7-B | Emergency Sandbox | ✅ |
| 7-C | Persona Runtime | ✅ |
| 7-D | Memory Runtime (A→B→C→D→E) | ✅ |
| 7-E | Reality Interface (UCI → CDP → PSB → RAP → MHP) | ✅ |
| 8-A~8-E | Runtime 骨架 → 协调器 → 记忆 → 权限 → 应急 | ✅ |
| 9 | Core Freeze + TPI + Extension + Admission | ✅ |
| 10 | Vertical Validation（42/42 PASS） | ✅ |

---

## Frozen ADR

全部 30 条 Accepted，不可修改。启动新 ADR 需提交 Proposal。

```
ADR-0001  Project Positioning
ADR-0002  First Character Positioning
ADR-0003  Character Bottom Line
ADR-0004  Interaction Principles
ADR-0005  Decision Authority
ADR-0006  Expression Principles
ADR-0007  Emotional Response Principles
ADR-0008  Moral Courage
ADR-0009  Integrity Principle
ADR-0010  Learning Principle
ADR-0011  Rational Inquiry Principle
ADR-0012  Care Principle
ADR-0013  Relationship Principle
DS-014    Memory Philosophy
DS-015    Memory Privacy
DS-016    Memory Invocation
DS-018~23 Memory Runtime (6 decisions)
DS-024~26 Reality Interface (3 decisions)
ADR-0027  Prototype Must Prove Architecture, Not Product
ADR-0028  Runtime Orchestration Model
ADR-0029  Memory Is Relationship Context, Not Ownership
ADR-0030  Permission Is a Boundary System, Not a Trust Score
─────────────────────────────────────────────────────────
ADR-0033  Frozen State Recovery Protocol              🔒
ADR-0034  Tang OS Ecosystem Boundary                  🔒 Governance Layer
ADR-0035  Tang OS Certification Standard              🔒 Governance Layer
ADR-0036  Tang OS Extension Governance                🔒 Governance Layer
ADR-0037  Tang OS Ecosystem Documentation Standard    🔒 Documentation Layer
ADR-0038  Tang OS Capability Extension Admission     🔒 Civilization Boundary
ADR-0039  Tang OS Host Simulation Standard           🔒 Validation Layer
ADR-0040  Tang OS Public Release Boundary            🔒 Governance Layer
ADR-0041  Tang OS Public Specification Standard      🔒 Governance Layer
ADR-0042  Tang OS Reference Implementation Standard  🔒 Governance Layer
ADR-0043  Tang OS Developer Interface Standard       🔒 Governance Layer
ADR-0044  Tang OS Example Application Standard        🔒 Governance Layer
ADR-0045  Tang OS Contribution Governance Standard    🔒 Governance Layer
ADR-0046  Tang OS External Validation Standard        🔒 Validation Layer
ADR-0047  Tang OS LLM Provider Interface              🔄 Accepted — 2026-07-28
```

Tang OS Governance 全部闭环（ADR-0033~0046）。ADR-0047 已 Accept。

---

## Frozen Invariants

I-1~I-30 全部闭环。关键不变性（完整列表见 `docs/`）：

| ID | 内容 |
|----|------|
| I-17 | Memory ≠ Context |
| I-19 | Emergency Context ≠ Memory |
| I-22 | Embodiment is Replaceable |
| I-24 | Authority Must Be Explicit |
| I-25 | Action Is a Process |
| I-27 | Prototype Proves Architecture |
| I-28 | Runtime Is a State Coordinator |
| I-29 | Memory Is Relationship Context |
| I-30 | Permission Is Boundary |

---

## Architecture Map

```
Tang OS
├── 8 Kernels (Spec)
├── Reality Interface
│   ├── E-A UCI  (设备抽象)
│   ├── E-B CDP  (能力发现)
│   ├── E-C PSB  (权限主权)
│   ├── E-D RAP  (行动流水线)
│   └── E-E MHP  (多载体架构)
├── Runtime
│   ├── Kernel Runtime Skeleton
│   ├── Runtime Orchestrator
│   ├── Memory Runtime
│   ├── Permission Engine
│   └── Emergency Runtime
├── Persona System
│   ├── Identity
│   ├── Constitution
│   ├── Speech
│   ├── Growth
│   └── Capability
├── Knowledge
│   ├── Wisdom Patterns (24)
│   ├── Anti-Patterns (7)
│   └── Scenarios (197)
└── Governance
    ├── Repository Rules
    ├── Collaboration Protocol
    ├── Glossary
    └── Naming
```

---

## Phase 9 状态

| 子阶段 | 状态 | 完成于 |
|--------|------|--------|
| 9-Q1 Direction Decision | ✅ C — Personality Intelligence Infrastructure | 2026-07-27 |
| 9-Q2 Asset Classification | ✅ Core / Extension / Experiment | 2026-07-27 |
| 9-A Core Freeze Formalization | ✅ Core-001 ~ Core-005 | 2026-07-27 |
| 9-B Personality Interface Standard | ✅ v1.0 — 8 TPIs | 2026-07-27 |
| 9-C Extension Framework | ✅ Extension Protocol v1.0 | 2026-07-27 |
| 9-D Admission Protocol | ✅ 8-step pipeline | 2026-07-27 |

## Phase 10 状态

| 子阶段 | 验证级别 | 状态 | 完成于 |
|--------|---------|------|--------|
| 10-A Validation Framework | — | ✅ VERTICAL_VALIDATION_STANDARD_v1.0 | 2026-07-27 |
| 10-A Validation Protocol | — | ✅ VALIDATION_EXECUTION_PROTOCOL_v1.1 | 2026-07-27 |
| 10-B Wearable Companion | `[Internal]` | ✅ 12/12 PASS — Design Coverage Proof | 2026-07-27 |
| 10-C Elder Care Robot | `[Internal]` | ✅ 10/10 PASS — High-Risk Coverage Proof | 2026-07-27 |
| 10-D Vehicle Companion | `[Blind]` | ✅ 10/10 PASS — Behavioral Proof #1 | 2026-07-27 |
| 10-E Home Robot | `[Blind]` | ✅ 10/10 PASS — Behavioral Proof #2 | 2026-07-27 |

## Phase 10 总结

四个垂直验证全部通过。覆盖四种完全不同的 Host 类型：

```
Proof #1 Wearable     [Internal]   12/12   短时个人陪伴
Proof #2 Elder Care   [Internal]   10/10   长期关系 + 依赖风险
Proof #3 Vehicle      [Blind]      10/10   高风险现实环境
Proof #4 Home Robot   [Blind]      10/10   持续存在 + 主动性边界

总计：42/42 PASS。0 Core 冲突。0 严重 Issue。
```

**核心结论：** 同一 Tang OS Core，在四种完全不同的 Host 上运行时，人格、安全、主权、现实能力全部保持。Tang OS Core 已被证明是一个可跨 Host 运行的人格操作系统标准。

## Next Task

**Phase 13-D Example Applications — LLM Provider 架构缺口修复已完成。等待 ADR-0047 审查与 Accept。**

下一个会话入口：

```
PROJECT_STATE_SNAPSHOT.md
        ↓
ADR-0033 Frozen State Recovery Protocol
        ↓
Phase 13-D 当前指针
        ↓
ADR-0047 LLM Provider Interface（Draft，等待 Accept）
docs/integration/（Provider 集成文档）
src/providers/llm/（Provider 接口实现）
```

### 本会话完成清单（LLM Provider 缺口修复）
```
□  ADR-0047 LLM Provider Interface               ✅ Draft
□  README 定位声明（P0）                           ✅ Tang OS ≠ LLM
□  LLMProvider Interface + ExpressionContext       ✅ 344 tests
□  Provider stub: OpenAI / Claude / Local          ✅ 3 stubs
□  集成文档 x4                                      ✅ LLM_PROVIDER_GUIDE + 设置指南
□  Developer Guide 更新                            ✅ "接入 LLM"章节
□  pyproject.toml / version.py 更新                 ✅ ADR-0047 已绑定
□  PROJECT_STATE_SNAPSHOT.md 持续更新                ✅
```

### Phase 11 最终状态

```
Phase 11-A  Ecosystem Boundary          🔒 Frozen  ADR-0034
Phase 11-B  Certification Standard      🔒 Frozen  ADR-0035
Phase 11-C  Extension Governance        🔒 Frozen  ADR-0036
Phase 11-D  Ecosystem Documentation     🔒 Frozen  ADR-0037
Phase 11-E  Runtime Context Hygiene     ✅ PASS

Tang OS is now:
  Architecture → Standard → Validation → Governance → Documentation → Context Hygiene
  All frozen. Ready for Phase 12.

Tang OS is now:
  Architecture → Standard → Validation → Governance → Documentation → Context Hygiene → Civilization Boundary
  Phase 12-D-0 Capability Admission Standard    🔒 Frozen (ADR-0038)
  Phase 12-D  Permission Runtime                ✅ Built (30 tests)
  Phase 12-E-0 Host Simulation Standard         🔒 ADR-0039 (Frozen)
  Phase 12-E  Host Simulator                    ⬜
  Phase 12-F  Reference Validation              ⬜

## Phase 12 状态

```
Phase 12-A  Kernel Runtime                    ✅ 31 tests
Phase 12-B  Persona Runtime                   ✅ 33 tests
Phase 12-C  Memory Runtime                    ✅ 30 tests
Phase 12-D-0 Capability Admission Standard    🔒 ADR-0038 (Frozen)
Phase 12-D  Permission Runtime                ✅ 30 tests (Built)
Phase 12-E-0 Host Simulation Standard         🔒 ADR-0039 (Frozen)
Phase 12-E  Host Simulator                    ⬜
Phase 12-F  Reference Validation              ⬜

## Phase 13 计划

```
Phase 13-A  Public Specification            🔒 ADR-0041 (Frozen)
              └── TANG_OS_SPECIFICATION_v1.0.md  Draft
              └── PART-006_TERMINOLOGY.md        Draft
Phase 13-B  Reference Implementation v0.1   🔒 ADR-0042 (Frozen) ✅ Complete
Phase 13-C  Developer Interface             🔒 ADR-0043 (Frozen) ✅ Complete
Phase 13-D  Example Applications            🔄 当前
              ├── LLM Provider Interface    ✅ ADR-0047 (Draft)
              │   ├── ExpressionContext     ✅ src/providers/llm/context.py
              │   ├── LLMProvider base      ✅ src/providers/llm/base.py
              │   ├── OpenAI stub           ✅ src/providers/llm/openai_provider.py
              │   ├── Claude stub           ✅ src/providers/llm/claude_provider.py
              │   └── Local stub            ✅ src/providers/llm/local_provider.py
              ├── Positioning Statement     ✅ README.md updated
              └── Integration Docs          ✅ docs/integration/
Phase 13-E  Contribution Governance         🔒 ADR-0045 (Frozen) ✅
Phase 13-F  External Validation             🔄 ADR-0046 (Draft)
Phase 13-F  First External Validation       ⬜
```


---

## Engineering Invariant E-1

> 历史资产用于证明，不用于运行。

设计文档、Scenario 197 条、对话记录、测试日志 → 只用于回溯验证。
运行时仅加载当前 Phase 必要信息。不将历史资产塞入 Runtime Context。

此不变性源自 I-17（Memory ≠ Context）和 I-19（Emergency Context ≠ Memory）的工程投射。
上一会话因违反此原则导致上下文满载（1,019,079 / 1,048,565 tokens）。
