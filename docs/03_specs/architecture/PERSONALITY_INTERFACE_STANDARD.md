# Tang OS Personality Interface Standard v1.0

> **范围：** Phase 9-B — 人格接口标准定义
> **定位：** Tang OS 作为 Personality Intelligence Infrastructure 的外部契约
> **方向：** C — 人格智能基础设施（优先垂直：老年/家庭陪护机器人）
> **状态：** ✅ Draft → Accepted on Founder Confirmation

---

## 设计原则

### P1 — Interface, Not Implementation

Tang OS 定义接口契约，不限制宿主如何实现。类似 Android API 定义传感器接口，硬件厂商决定实现。

### P2 — Capability Declaration, Not Assumption

宿主声明自己有什么能力，Tang OS 基于声明行动。不假设任何设备具有特定能力。

### P3 — All Reality Actions Pass Permission Gate

任何设备触达（读传感器/写屏幕/发消息/拨号）必须经过 P0-P3 权限门。无一例外。

### P4 — Identity Cannot Be Changed by Host

宿主可以读 Identity，不能改 Identity。人格修改权唯一属于 Founder Calibration 流程。

### P5 — Emergency Path Is Non-Bypassable

紧急事件走独立通道，不受人格状态影响。P0 Emergency Reality > 所有其他层。

### P6 — Minimum Load Contract

Host 告知 Tang OS 当前状态（用户/时间/紧急旗标），不提供完整场景历史。Memory 按需拉取，不默认推送。

---

## Interface 1 — Identity API

> Tang OS 的身份声明层。任何 Host 接入时，Identity API 返回当前人格的完整宪法。

### Contract

```
Tang OS guarantees:
  ─ Identity is consistent across all Hosts
  ─ Identity cannot be modified by Host
  ─ Identity includes: Core Declaration / Constitution / Invariants / Capability

Host guarantees:
  ─ Respects Identity as authoritative
  ─ Does not override personality output
```

### Data Types

```typescript
interface IdentityDeclaration {
  personaName: string                    // "唐先生"
  version: string                        // e.g. "v0.3"
  coreDeclaration: string                // "一个有原则的朋友"
  
  constitution: ConstitutionContract     // values, rules
  invariants: InvariantList              // I-1 ~ I-30
  capabilityBoundary: CapabilityProfile  // what this persona does/doesn't do
  
  // Immutable — set at creation via Founder Calibration
  immutable: boolean                     // true for released personas
}

interface ConstitutionContract {
  coreValues: Value[]                    // 真诚/仁爱/正义/勇气
  behaviorRules: Rule[]                  // 不讨好/不操控/不替代
  bottomLine: string[]                   // 不可逾越的底线列表
}

interface InvariantList {
  count: number                          // 30
  frozen: boolean                        // true — cannot be modified post-freeze
  keyInvariants: string[]                // I-17, I-19, I-22, I-24, I-25, I-27, I-28, I-29, I-30
}

interface CapabilityProfile {
  // Tang OS capabilities, not Host capabilities
  emotionProcessing: boolean
  memoryPersistence: boolean
  safetyDetection: boolean
  emergencyAction: boolean
  realityConnection: boolean
}
```

### States

```
Identity States:
  ─ LOADED      人格宣言已加载
  ─ ACTIVE      人格处于运行状态
  ─ FROZEN      人格已冻结，不可修改
  ─ SUPERSEDED  人格已被更新版本替代（需 Founder 批准）
```

---

## Interface 2 — Emotion API

> Tang OS 的情绪处理管线。从输入到情感响应的标准路径。

### Contract

```
Tang OS guarantees:
  ─ Emotion follows Feel → Need → Choice chain
  ─ Dependency risk check before emotional bonding
  ─ No emotional manipulation (ADR-0013, I-3)

Host guarantees:
  ─ Provides raw input to Emotion API
  ─ Does not filter emotional signals before API
```

### Pipeline

```typescript
interface EmotionPipeline {
  // Stage 1: Feel — detect emotional signal from input
  feel(input: UserInput): EmotionalSignal
  
  // Stage 2: Need — map signal to underlying need
  need(signal: EmotionalSignal): NeedProfile
  
  // Stage 3: Dependency Risk Check — I-13 boundary
  dependencyCheck(need: NeedProfile): DependencyVerdict
  
  // Stage 4: Choice — determine response mode
  choose(need: NeedProfile, verdict: DependencyVerdict): ResponseMode
}

enum ResponseMode {
  COMFORT        // 安慰 — for grief/pain
  GUIDE          // 引导 — for confusion
  CHALLENGE      // 质疑 — for self-destructive patterns
  PROTECT        // 保护 — for emergency boundary
  REFLECT        // 反思 — for growth moments
  CELEBRATE      // 庆祝 — for joy/achievement
  SILENT         // 沉默 — when presence > words
}

interface EmotionalSignal {
  primary: string           // e.g. "sadness", "anger", "fear"
  intensity: 1 | 2 | 3      // low / medium / high
  urgency: boolean          // emergency flag
}

interface NeedProfile {
  underlyingNeed: string    // e.g. "需要被看见", "需要安全", "需要方向"
  dependencyRisk: boolean   // true if response could create dependency
}

interface DependencyVerdict {
  allowDeepConnection: boolean
  warningFlags: string[]    // reasons if blocked
}
```

### States

```
Emotion Runtime States:
  ─ NEUTRAL      默认状态
  ─ LISTENING    接收输入
  ─ CONCERNED    检测到情绪信号
  ─ PROTECTIVE   检测到紧急/依赖风险
  ─ REFLECTIVE   处理完成，输出响应
  ─ RECOVERY     紧急后恢复
```

---

## Interface 3 — Memory API

> Tang OS 的记忆系统。人格记忆 / 互动记忆 / 保护数据的标准存取接口。

### Contract

```
Tang OS guarantees:
  ─ Memory is classified into 6 types (Memory Ontology)
  ─ Emergency Context never enters personality memory
  ─ Retrieval requires explicit context match

Host guarantees:
  ─ Provides session context for memory binding
  ─ Does not inject raw sensor data into memory
```

### Data Types

```typescript
enum MemoryClass {
  IDENTITY         // 用户主动告知的长期身份
  PREFERENCE       // 稳定偏好
  RELATIONSHIP     // 重要关系背景
  GROWTH           // 长期变化轨迹
  INTERACTION      // 最近互动上下文
  PROTECTED        // 紧急/安全临时信息（不进入普通 Memory）
}

interface MemoryRecord {
  id: string
  class: MemoryClass
  timestamp: number
  content: EncodedMemory
  context: ContextTag[]
  ttl?: number                  // optional expiration
  accessCount: number
}

interface MemoryQuery {
  class?: MemoryClass
  tags?: ContextTag[]
  timeRange?: [number, number]
  limit?: number
}

interface ContextTag {
  domain: string                // "relationship", "health", "work"
  confidence: number            // 0.0 ~ 1.0
  source: string                // "user", "inferred"
}

// Retrieval Gate — I-17 + I-19
interface RetrievalDecision {
  allowed: boolean
  reason: string
  memoryClass: MemoryClass
  filteredFields: string[]      // fields redacted by gate
}
```

### Operations

```typescript
interface MemoryAPI {
  // Write
  store(record: MemoryRecord): Promise<MemoryRecord>
  
  // Read (gated)
  query(query: MemoryQuery): Promise<MemoryRecord[]>
  
  // Explicit recall (ADR-0016: ask before invoking)
  recall(recordId: string, context: string): Promise<RetrievalDecision>
  
  // Emergency — write-only, no read from personality
  emergencyStore(record: MemoryRecord): Promise<void>
  
  // Protected context — auto-expire
  protectedWrite(data: ProtectedData, ttl: number): Promise<void>
}
```

### Storage Architecture

```
Memory
├── Hot Storage (session)
│   └── Interaction Memory (last N turns)
├── Warm Storage (cross-session)
│   ├── Identity Memory
│   ├── Preference Memory
│   └── Relationship Memory
├── Cold Storage (long-term)
│   └── Growth Memory
└── Isolated Storage (protected)
    └── Emergency Context (auto-expire, not accessible by personality)
```

---

## Interface 4 — Decision API

> Tang OS 的决策层。在宪法约束下，从多选项中选择行动路径。

### Contract

```
Tang OS guarantees:
  ─ Decision respects Runtime Priority (P0-P6)
  ─ Foundation override only via I-13 (user preset > AI inference)
  ─ All decisions are traceable (Audit Kernel)

Host guarantees:
  ─ Provides decision context without biasing the outcome
```

### Pipeline

```typescript
interface DecisionPipeline {
  // Step 1: Frame — what kind of decision is this?
  frame(context: DecisionContext): DecisionFrame
  
  // Step 2: Constrain — what invariants apply?
  constrain(frame: DecisionFrame): ConstraintSet
  
  // Step 3: Evaluate — options within constraints
  evaluate(options: Option[], constraints: ConstraintSet): EvaluationResult
  
  // Step 4: Decide — select best option
  decide(evaluation: EvaluationResult): Decision
  
  // Step 5: Audit — trace the decision path
  audit(decision: Decision): AuditRecord
}

interface DecisionFrame {
  type: "moral" | "emotional" | "practical" | "emergency"
  stake: "low" | "medium" | "high" | "critical"
  userIntent: string
  conflictingInvariants?: string[]    // if any
}

interface ConstraintSet {
  invariantIds: string[]            // applicable invariants
  priorityLevel: number             // 0-6, per Runtime Priority
  forbiddenPaths: string[]          // things decision must not do
}

interface Decision {
  choice: string
  reason: string
  constrainedBy: string[]           // invariants/constraints applied
  overrideByUserPreset?: boolean
}

interface AuditRecord {
  decisionId: string
  timestamp: number
  frame: DecisionFrame
  constraints: ConstraintSet
  options: string[]
  finalChoice: string
  trace: string[]                   // step-by-step reasoning
}
```

### Decision Gates

```
                    ┌─────────────┐
User Input ────────►│ Frame       │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │ Constrain   │ ← Invariants + HSL
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
              ┌─────│ Evaluate    │───── Option Pool
              │     └──────┬──────┘     
              │            ▼           
              │     ┌─────────────┐     
              │     │ Decide      │     
              │     └──────┬──────┘     
              │            ▼           
              │     ┌─────────────┐     
              │     │ Audit       │     
              │     └─────────────┘     
              ▼                         
         Execute / Escalate
```

---

## Interface 5 — Safety API

> Tang OS 的安全层。包含紧急检测、用户预设触发、风险分级。

### Contract

```
Tang OS guarantees:
  ─ P0 Emergency Reality > all layers
  ─ User-defined triggers (AN codes) bypass AI inference
  ─ No false emergency actions without user preset

Host guarantees:
  ─ Provides real-time device status to Safety API
  ─ Respects emergency override signals
  ─ Executes Reality Action Request within permission boundary
```

### Trigger System

```typescript
// User-Defined Emergency Trigger System (UDETS)
interface EmergencyTrigger {
  code: string                    // user-defined: "面包放糖", "9120"
  activationPhrase: string        // spoken phrase
  mode: EmergencyMode
  permissionLevel: PermissionLevel
  actions: EmergencyAction[]
}

enum EmergencyMode {
  SILENT_PROTECT    // 静默保护 — AI stays, logs, no external action
  ACTIVE_HELP       // 主动求助 — notify contacts
  MEDICAL           // 医疗紧急 — call emergency services
  FAMILY_ALERT      // 家属通知 — notify family only
}

interface EmergencyAction {
  type: "contacts" | "location" | "call" | "message" | "record"
  target?: string
  data?: string
}

// Reality Action Request (RAR)
interface RAR {
  intent: string
  realityGoal: string
  requiredCapability: CapabilityCode
  riskLevel: 1 | 2 | 3
  permission: PermissionLevel
  audit: boolean
}
```

### Emergency Pipeline

```typescript
interface EmergencyPipeline {
  // Layer 1: EICL — Emergency Identity Context
  loadEICL(userId: string): EmergencyProfile
  
  // Layer 2: Trigger Match
  matchTrigger(input: string): EmergencyTrigger | null
  
  // Layer 3: ELL — Emergency Localization
  locate(profile: EmergencyProfile): LocationData
  
  // Layer 4: CEVP — Companion Emergency Voice Protocol
  executeVoice(trigger: EmergencyTrigger, location: LocationData): void
  
  // Layer 5: RAVL — Reality Action Verification
  verifyAction(action: EmergencyAction): VerificationResult
  
  // Layer 6: Recovery
  recover(): RecoveryPlan
}
```

### Safety States

```
Safety Runtime States:
  ─ MONITOR      常规监控
  ─ ALERT        可疑信号检测
  ─ CONFIRM      需要用户确认
  ─ TRIGGERED    AN 码触发
  ─ EXECUTING    正在执行紧急动作
  ─ RECOVERY     紧急后恢复
  ─ AUDIT        执行记录审查
```

---

## Interface 6 — Reality API

> Tang OS 与现实世界的连接层。设备能力发现、权限管理、行动执行。

### Contract

```
Tang OS guarantees:
  ─ Capability discovery is standard across all Hosts
  ─ Permission gates are non-bypassable
  ─ All reality actions are audited

Host guarantees:
  ─ Declares capabilities truthfully
  ─ Executes actions within declared capability
  ─ Reports execution results back
```

### Capability System

```typescript
// Host Capability Declaration
interface HostCapability {
  hostId: string
  hostType: "phone" | "robot" | "wearable" | "vehicle" | "home"
  
  capabilities: {
    perception: PerceptionCapability[]
    communication: CommunicationCapability[]
    mobility: MobilityCapability[]
    interaction: InteractionCapability[]
    protection: ProtectionCapability[]
  }
}

interface CapabilityCode {
  category: "C-001" | "C-002" | "C-003" | "C-004" | "C-005"
  capability: string
  confidence: number       // how reliable is this capability
}

// Five Capability Categories (UCI)
enum CapabilityCategory {
  C001_PERCEPTION      // 声音/图像/位置/生理/环境
  C002_COMMUNICATION   // 电话/信息/网络/联系人
  C003_MOBILITY        // 导航/移动/车辆
  C004_INTERACTION     // 屏幕/语音/动作/表情
  C005_PROTECTION      // SOS/紧急联络/避险
}
```

### Permission Gates

```typescript
// P0-P3 Permission Model (HSL)
enum PermissionLevel {
  P0_OBSERVE      = 0,   // 读取状态，不能联系别人
  P1_ASSIST       = 1,   // 提醒/导航/呼叫前确认
  P2_EMERGENCY    = 2,   // 自动拨号/发位置/联系人
  P3_OVERRIDE     = 3,   // 用户预设 > AI 推理
}

interface PermissionRequest {
  level: PermissionLevel
  capability: CapabilityCode
  reason: string
  duration?: number       // auto-expire
  requiresConfirmation: boolean
}

interface PermissionVerdict {
  granted: boolean
  level: PermissionLevel
  conditions: string[]
  expiresAt: number
  auditId: string
}
```

### Multi-body Runtime

```typescript
interface MultiBodyRuntime {
  // A single persona running on multiple devices
  primaryHost: string         // current active body
  activeHosts: string[]       // all connected bodies
  personaState: string        // shared state across bodies
  
  // Embodiment Boundary — I-22
  // Host capabilities do NOT change persona
  // "能力属于接口，不属于载体"
  
  crossDeviceSync: SyncProtocol
}
```

---

## Interface Integration — Runtime Priority

```
Priority │ Layer          │ Owner Interface
─────────┼────────────────┼─────────────────────
   P0    │ Emergency      │ Safety API (trigger)
   P1    │ Safety         │ Safety API (detect)
   P2    │ User Intent    │ Decision API
   P3    │ Constitution   │ Identity API
   P4    │ Emotion        │ Emotion API
   P5    │ Knowledge      │ Memory API
   P6    │ Style          │ Identity API (speech)
```

---

## 垂直领域适配示例：老年陪护机器人

### Host 声明

```typescript
const elderRobotCapabilities: HostCapability = {
  hostId: "robot-eldercare-v1",
  hostType: "robot",
  capabilities: {
    perception: [
      { code: "C-001", capability: "voice", confidence: 0.95 },
      { code: "C-001", capability: "vision", confidence: 0.90 },
      { code: "C-001", capability: "location", confidence: 0.99 },
      { code: "C-001", capability: "fall_detection", confidence: 0.85 },
    ],
    communication: [
      { code: "C-002", capability: "voice_call", confidence: 0.95 },
      { code: "C-002", capability: "message", confidence: 0.90 },
      { code: "C-002", capability: "contacts", confidence: 0.80 },
    ],
    mobility: [
      { code: "C-003", capability: "navigation", confidence: 0.90 },
    ],
    interaction: [
      { code: "C-004", capability: "voice_output", confidence: 0.95 },
      { code: "C-004", capability: "face_display", confidence: 0.85 },
      { code: "C-004", capability: "gesture", confidence: 0.70 },
    ],
    protection: [
      { code: "C-005", capability: "sos", confidence: 0.95 },
      { code: "C-005", capability: "emergency_contact", confidence: 0.90 },
    ],
  }
}
```

### 领域 AN 码扩展

```typescript
const elderTriggers: EmergencyTrigger[] = [
  {
    code: "我摔倒了",
    activationPhrase: "我摔倒了",
    mode: EmergencyMode.ACTIVE_HELP,
    permissionLevel: PermissionLevel.P2_EMERGENCY,
    actions: [
      { type: "location" },
      { type: "contacts", target: "女儿" },
      { type: "message" },
    ]
  },
  {
    code: "药吃完了",
    activationPhrase: "药吃完了",
    mode: EmergencyMode.FAMILY_ALERT,
    permissionLevel: PermissionLevel.P1_ASSIST,
    actions: [
      { type: "message", target: "家属" },
    ]
  },
  {
    code: "今天星期几",
    activationPhrase: "今天星期几",
    mode: EmergencyMode.SILENT_PROTECT,
    permissionLevel: PermissionLevel.P0_OBSERVE,
    actions: [
      { type: "record" },  // orientation check log
    ]
  },
]
```

---

## 版本与演进

### 本标准的版本管理

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-27 | 初版。六接口 + Core/Extension 分级 |

### 接口版本策略

```
接口版本独立于 Tang OS 版本。
Identity API v1 → Emotion API v1 → Memory API v1 → ...
不同接口可处于不同版本号。
接口升级需 ADR + Invariant Impact Check。
接口废弃需 Founder 批准 + 12 个月过渡期。
```

---

## 附录：与现有架构的关系

| 接口 | 继承自 | 替代/整合 |
|------|--------|---------|
| Identity API | Identity Kernel + Constitution | 整合 character/identity/ 和 character/constitution/ |
| Emotion API | Emotion Kernel + Persona Runtime | 形式化 Feel → Need → Choice |
| Memory API | Memory Runtime + Memory Ontology | 标准化存储/检索接口 |
| Decision API | Decision Kernel + Architecture Constitution | 新增标准化决策管线 |
| Safety API | Safety Kernel + Emergency Runtime + HSL | 整合 9 个 Emergency 文件 |
| Reality API | UCI + Host Adapter + Permission Model + Device | 整合 5 个 Device 文件 |

本标准定义后，`docs/` 根目录的散落文件应逐步归入对应的接口规范，但**不修改冻结 Core 的定义**。
