# Phase 9-Q2: Frozen Asset Classification

> 生成时间：2026-07-27
> 方向决策：C — Personality Intelligence Infrastructure（人格智能基础设施）
> 垂直验证：老年/家庭陪护机器人（优先）
> 原则：Core 不可商业化破坏，Extension 允许行业扩展，Experiment 可淘汰

---

## 分类标准

| 等级 | 定义 | 修改规则 | 生命周期 |
|------|------|---------|---------|
| **Core** | 人格宪法级。修改即改变 Tang OS 本质 | 仅新 ADR 明确 Supersede，需 Found  er 批准 | 永久 |
| **Extension** | 领域扩展接口。允许行业定制 | 新增需 ADR，不修改 Core 约束 | 随领域迭代 |
| **Experiment** | 探索性资产。验证有效则升级，无效则废弃 | 无需 ADR，可自由创建/删除 | 6 个月复审 |

---

## Core（不可商业化破坏）

### 人格宪法 — 永远不变

| 资产 | 来源 | 冻结原因 |
|------|------|---------|
| I-1 ~ I-19 | Persona Foundation | 人格底线的不可协商原则 |
| I-20 ~ I-30 | Phase 7-8 | 架构宪法的不可违背约束 |
| E-1 | Engineering Invariant | 历史资产不用于运行 |
| ADR-0001 ~ ADR-0013 | 人格底座 | 十三项人格基本原则 |
| `docs/00_governance/` (4 files) | 项目法律 | 协作/术语/命名/仓库规则 |

### 运行时层 — 架构核心

| 资产 | 来源 | 冻结原因 |
|------|------|---------|
| Persona State Machine | Persona Runtime | 人格状态转换的核心模型 |
| Feel → Need Chain | Emotion Runtime | 情绪处理的不可逆链路 |
| Memory Ontology（6 类） | Memory Runtime | 记忆分类架构，不可合并 |
| Runtime Priority (P0-P6) | Architecture Constitution | 事件优先级仲裁规则 |
| Event Bus Model | Architecture Constitution | 事件路由架构 |

### 安全与主权 — 信任基础设施

| 资产 | 来源 | 冻结原因 |
|------|------|---------|
| P0-P3 权限模型 | HSL / Permission Model | 权限分级体系 |
| HSL Release Gates (7 gates) | Human Sovereignty Layer | 人类主权的七道门 |
| AN 触发系统 | UDETS | 用户预设优于 AI 推理 |
| Emergency Context ≠ Memory | I-19 | 紧急数据不渗入人格记忆 |
| Memory ≠ Context | I-17 | 记忆与上下文的严格分离 |
| Capability Belongs to Interface | I-23 + UCI | 能力属于接口，不属于载体 |
| Embodiment is Replaceable | I-22 | 人格不绑定硬件 |

### Core 完整性保护规则

```
任何新增 Extension 不得：
  ❌ 绕过 Permission Gate 访问设备
  ❌ 修改 Persona State Machine 的状态转换
  ❌ 合并 Emergency Context 进入普通 Memory
  ❌ 降低 HSL 权限确认门槛
  ❌ 使 Embodiment 具有人格修改能力

违反上述任何一条的 Extension = 架构违规，不予准入。
```

---

## Extension（允许行业扩展）

### 领域扩展接口

| 扩展点 | 当前资产 | 扩展方式 | 示例（老年陪护） |
|--------|---------|---------|----------------|
| Host Adapter | `HOST_ADAPTER_ARCHITECTURE.md` | 实现特定 Host Interface | 机器人传感器适配 |
| Device Capability | `DEVICE_CAPABILITY_BOUNDARY.md` | 声明 Capability 集合 | 跌倒检测 / 环境监测 |
| Voice Runtime | `VOICE_RUNTIME_ARCHITECTURE.md` | 接入 ASR/TTS | 方言语音识别 |
| Emergency Triggers | `USER_DEFINED_EMERGENCY_TRIGGER_SYSTEM.md` | 定义领域 AN 码 | "我摔倒了" / "药吃完了" |
| Response Corpus | `response_corpus/` | 领域定制语料 | 老年人沟通风格 |
| Wisdom Patterns | `wisdom_patterns/` | 按需引用 | 赡养/病痛/孤独相关 |

### Domain Extension Kit（DEK）结构

```
domain/{domain-name}/
├── HOST_ADAPTER.md         ← 设备层适配
├── EMERGENCY_TRIGGERS.md   ← 领域 AN 码定义
├── RESPONSE_CORPUS/        ← 领域语料
├── PERMISSION_PROFILE.md   ← 领域权限预设
└── TEST_MATRIX.md          ← 领域验证（Pass/Fail）
```

老年陪护机器人将作为第一个 DEK 验证。

### Extension 准入条件

```
□ 不违反 Core 任何 Invariant
□ 通过 Invariant Impact Check
□ 通过 Scenario 验证（至少 5 个场景）
□ 通过 Regression Suite
```

---

## Experiment（可淘汰）

### 探索期资产

| 资产 | 当前状态 | 复审时间 | 判定条件 |
|------|---------|---------|---------|
| 跨领域 Scenario（SV-048~112） | 理论验证完成 | 2027-01 | 是否纳入垂直领域验证 |
| WP-063~174（跨领域 WP） | 探索期 | 2027-01 | 是否存在实际使用数据 |
| 多语言/多文化人格扩展 | 未启动 | — | 确定垂直市场后决定 |
| `docs/05_reviews/` | 历史评审 | 归档 | 无需复审 |
| `docs/02_decisions/` (ADR-0020~0030) | 已 Accepted | 2027-06 | 与垂直验证是否一致 |

### Experiment → Core 升级路径

实验验证通过 → 写入 ADR → Invariant Impact Check → 加入 runtime spec → 进入 Core。

### Experiment 废弃条件

```
□ 6 个月无使用记录
□ 无实际场景引用
□ 与 Core 原则产生冲突
```

---

## 垂直领域映射（方向 C — 老年陪护机器人）

### Core 直接可用（无需修改）

```
Persona Runtime        ✅ 人格约束体系完整
Emotion Runtime        ✅ 情绪理解 + 安全边界
Memory Runtime         ✅ 保护模式 + 关系记忆
Permission P0-P3       ✅ 四级权限
HSL 七道门              ✅ 人类主权保障
Emergency Layer        ✅ AN 触发系统
Safety Priority P0     ✅ 紧急优先
```

### Extension 需开发

```
Host Adapter (Robot)   📋 机器人传感器接入
AN Triggers (Elder)    📋 跌倒/失联/用药 AN 码
Voice Runtime (方言)    📋 方言 ASR 接入
Response Corpus        📋 老年人陪伴语料
Permission Profile     📋 家属权限预设
```

### Experiment 暂不涉及

```
多 Host 并行运行        ⏸ 后续阶段
商业化 SDK             ⏸ 验证后
开发者平台              ⏸ 验证后
```

---

## 总结

| 等级 | 数量 | 说明 |
|------|------|------|
| Core | ~40 项 | 人格宪法 + 运行时架构 + 安全主权 |
| Extension | 7 个扩展点 | 行业定制接口 |
| Experiment | 4 项 | 探索期，6 个月复审 |

保护规则一句话：**Core 是 Tang OS 的 DNA，任何 Extension 不得修改 DNA。**
