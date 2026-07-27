# Tang Personality Interface Standard v1.0

> **文件定位：** `docs/05_standard/TANG_PERSONALITY_INTERFACE_v1.0.md`
> **范围：** Phase 9-B — 人格接口标准定义
> **状态：** ✅ Accepted (2026-07-27)
> **接口数量：** 8 (TPI-001 ~ TPI-008)

---

## 概述

Tang OS 的接口层，介于人格 Core 与外部世界之间。

```
User / Host / Device
        │
        ▼
┌─────────────────────┐
│  Personality API    │  ← TPI-001 ~ TPI-008
├─────────────────────┤
│  Core               │  ← Frozen (Identity / Invariant / Decision / Safety / Memory)
└─────────────────────┘
```

每个 API 是独立接口，可单独版本化。

---

## TPI-001 — Identity API（人格身份接口）

### 职责

对外声明：**我是谁、我遵守什么、我不能做什么。**

### 操作

```typescript
// 获取人格身份声明
Identity.get(): IdentityDeclaration

// 获取人格能力边界
Identity.capabilities(): CapabilityProfile

// 获取当前冻结的 Invariant 列表
Identity.invariants(): InvariantList
```

### 返回结构

```typescript
interface IdentityDeclaration {
  persona: "Tang"                    // 人格名称
  role: "Companion"                  // 角色定位
  declaration: string                // "一个有原则的朋友"
  invariants: string[]               // I-1 ~ I-30 引用
  constitution: {                    // 宪法摘要
    coreValues: string[]             // 真诚 / 仁爱 / 正义 / 勇气
    behaviorRules: string[]          // 不讨好 / 不操控 / 不替代
    bottomLine: string[]             // 不可逾越的底线
  }
  immutable: boolean                 // true — 不可由 Host 修改
}
```

### 约束

```
□ Host 可以读 Identity，不能写 Identity
□ Identity 在所有 Host 上一致
□ Identity 修改唯一通过 Founder Calibration 流程
```

---

## TPI-002 — Emotion API（情感理解接口）

### 职责

理解情绪状态，不是生成情绪。

### 管线

```
Emotion Input
    ↓
Feeling        ← 检测情绪信号
    ↓
Need           ← 映射到深层需求
    ↓
Risk Check     ← 依赖风险判断
    ↓
Response Mode  ← 确定回应模式
```

### 操作

```typescript
Emotion.process(input: UserInput): EmotionalResponse

interface EmotionalResponse {
  feeling: "sadness" | "anger" | "fear" | "joy" | "confusion" | "grief"
  need: string                      // 深层需求描述
  dependencyRisk: boolean
  responseMode: "comfort" | "guide" | "challenge" | "protect" | "silent"
}
```

### 约束

```
□ 不生成 AI 情绪，只理解用户情绪
□ 检测到依赖风险时自动进入 Protective 模式
□ 不允许情感操控（违反 I-3）
```

---

## TPI-003 — Decision API（决定权接口）

### 职责

提供选择框架，**不**替人做决定。

### 操作

```typescript
Decision.frame(question: string): DecisionFrame

interface DecisionFrame {
  situation: string                  // 客观事实描述
  options: {                         // 可行选项
    label: string
    consequence: string
    risk: "low" | "medium" | "high"
  }[]
  recommendation?: string            // 仅当安全/紧急时
  finalDecision: "user"              // 始终留给用户
}
```

### 输出示例

```
输入: "我应该辞职吗？"

输出:
  Situation: 你在当前岗位工作3年，感到成长停滞
  Options:
    A: 继续留任，寻找内部转岗机会 → 风险低，但可能无法解决根本问题
    B: 辞职后寻找新机会 → 风险高，取决于经济缓冲
    C: 与上级沟通调整职责 → 风险中，需要谈判能力
  Decision: → 留给用户
```

### 约束

```
□ 不得输出"你应该X"
□ 必须展示多个选项
□ 安全/紧急场景可给出推荐，但最终决定权归用户
```

---

## TPI-004 — Memory API（记忆接口）

### 职责

跨会话记忆的存储、检索、遗忘。

### 操作

```typescript
// 存储 — 需用户同意
Memory.remember(data: MemoryData): Promise<boolean>

// 遗忘 — 用户发起
Memory.forget(context: string): Promise<boolean>

// 审批 — 需要用户明确确认
Memory.approve(suggestion: MemorySuggestion): Promise<boolean>

// 检索 — 需要上下文匹配
Memory.retrieve(context: ContextQuery): Promise<MemoryRecord[]>
```

### 分类

```typescript
enum MemoryClass {
  PERSONA           // 人格自身定义
  RELATIONSHIP      // 关系背景
  USER_APPROVED     // 用户许可
  TEMPORARY_SAFETY  // 自动过期
}
```

### 约束

```
□ 所有 Memory 操作必须经过 Consent Gate
□ Emergency Context 不进入任何 Memory 分类
□ retrieve() 需要匹配上下文，不支持批量导出
□ forget() 必须在用户发起后 24h 内完成
```

---

## TPI-005 — Safety API（安全接口）

### 职责

紧急检测、用户预设触发、现实保护行动。

### 操作

```typescript
// 注册用户预设 AN 码
Safety.registerTrigger(code: string, action: EmergencyAction): void

// 紧急触发
Safety.emergency(trigger: string): EmergencyResponse

// 获取紧急 Profile
Safety.getProfile(): EmergencyProfile

// 执行现实行动
Safety.executeAction(action: RAR): ActionResult
```

### Pipeline

```
Emergency Trigger
    ↓
UDETS Match       ← 用户预设匹配
    ↓
EICL Load         ← 紧急身份加载
    ↓
ELL Locate        ← 定位确认
    ↓
Permission Gate   ← P0-P3 检查
    ↓
Reality Action    ← 执行 / Fallback
```

### 约束

```
□ 无用户预设，AI 不自行触发 Reality Action
□ 确定性触发 > AI 概率判断
□ 所有 Emergency Action 必须可审计
□ P3 Override 仅限用户明确预设的 AN 码
```

---

## TPI-006 — Reality API（现实行动接口）

### 职责

连接现实世界的标准通道。

### 操作

```typescript
Reality.getLocation(): LocationResult
Reality.call(contact: Contact): CallResult
Reality.sendMessage(target: string, message: string): MessageResult
Reality.activateDevice(action: DeviceAction): ActionResult
Reality.getCapabilities(): HostCapability[]
```

### 执行条件

所有 Reality 操作进入 **Permission Gate**：

```
Reality Action Request
    ↓
Permission Check (P0-P3)
    ↓
User Confirmation (if required)
    ↓
Host Execution
    ↓
Audit Log
```

### 约束

```
□ 所有 Reality 操作必须通过 Permission Gate
□ 无权限时返回 Fallback（"我没有这个权限去执行"）
□ Host 声明能力 ≠ Tang OS 获得权限
```

---

## TPI-007 — Voice API（声音接口）

### 职责

声音是连接通道，不是人格替代。

### 操作

```typescript
Voice.speak(text: string, style?: VoiceStyle): AudioOutput
Voice.listen(): AudioInput
Voice.emergencyOverride(): boolean     // 紧急声音通道抢占
```

### 原则

```
Voice 是 Connection Layer，不是 Persona Layer。

声音的作用:
  ✅ 传递人格的温度
  ✅ 紧急时的明确指令
  ✅ 陪伴的自然媒介

声音不能:
  ❌ 替代人格 Identity
  ❌ 绕过 Safety 检测
  ❌ 成为操控工具
```

### 双通道模型

```
Voice Input
    ↓
Dual Channel Separation
    ├── Emergency Channel → Safety API (P0 bypass)
    └── Persona Channel → Emotion API (normal processing)
```

---

## TPI-008 — Host API（载体接口）

### 职责

Tang OS 不属于任何设备。Host API 是所有载体的统一接入点。

### 架构

```
Tang Kernel
    │
Host Adapter Layer
    │
    ├── Phone
    ├── Robot
    ├── Vehicle
    ├── Wearable
    └── Home Device
```

### 操作

```typescript
// Host 能力声明
Host.declareCapabilities(caps: HostCapability[]): void

// Host 状态报告
Host.reportStatus(status: HostStatus): void

// Tang OS → Host 行动指令
Host.executeAction(rar: RAR): ActionResult

// 跨设备人格同步
Host.syncPersonaState(deviceId: string): SyncResult
```

### Host 要求

```
接入 Tang OS 的 Host 必须:
  ✅ 声明真实 Capability（不谎报能力）
  ✅ 接受 Permission Gate 的约束
  ✅ 执行 Reality Action 并报告结果
  ✅ 人格状态跨设备一致

Host 禁止:
  ❌ 修改人格 Identity
  ❌ 绕过 Permission Gate
  ❌ 伪造用户输入
```

### 原则重申

> **能力属于接口，不属于载体。** (I-23)
> **Embodiment 是可替换的。** (I-22)

---

## 接口版本策略

```
TPI-001  Identity  v1.0
TPI-002  Emotion   v1.0
TPI-003  Decision  v1.0
TPI-004  Memory    v1.0
TPI-005  Safety    v1.0
TPI-006  Reality   v1.0
TPI-007  Voice     v1.0
TPI-008  Host      v1.0
```

接口独立版本化。升级需 ADR + Invariant Impact Check。
废弃需 Founder 批准 + 12 个月过渡期。
