# Tang OS Extension Protocol v1.0

> **文件定位：** `docs/05_standard/TANG_EXTENSION_PROTOCOL_v1.0.md`
> **范围：** Phase 9-C — 扩展框架 + Phase 9-D — 新能力准入规则
> **状态：** ✅ Accepted (2026-07-27)

---

## 第一部分：扩展框架

### 设计原则

Tang OS Core 是"人格硬件"，Extension 是"应用层"。

```
Tang Core（不可修改）
    │
    + Extension（行业定制）
    │
    + Host Adapter（载体适配）
    │
    = Tang OS Instance
```

**任何 Extension 不得修改 Core 的任何约束。**

---

### Extension 结构

```
{domain}-extension/
├── manifest.json            ← 扩展声明（名称/版本/依赖）
├── triggers.md              ← 领域 AN 码定义（可选）
├── corpus/                  ← 领域语料（可选）
├── permissions.md           ← 领域权限预设（必需）
├── adapter/                 ← 载体适配层（必需）
│   └── host_interface.ts    ← 实现 TPI-008
└── tests/                   ← 领域验证
    ├── scenarios.md         ← 场景测试
    └── regression.md        ← 回归验证
```

---

### 预定义 Extension 类型

| 类型 | Core 需求 | 主要扩展点 | 示例 |
|------|----------|-----------|------|
| Elder Care | 无 | AN 码 / 语料 / 家属权限 | 老年陪护机器人 |
| Medical | 无 | AN 码 / 设备接口 / 隐私 | 医院辅助机器人 |
| Education | 无 | 回应风格 / 知识 / 监护人权限 | 儿童教育设备 |
| Companion | 无 | 语料 / 长期记忆偏好 | 普通消费者 |

---

## 第二部分：新能力准入规则

### 准入管线（冻结）

```
Idea
  ↓
[Step 1] Proposal
  ↓
[Step 2] ADR
  ↓
[Step 3] Invariant Impact Check
  ↓
[Step 4] Scenario Test（≥5 场景）
  ↓
[Step 5] Security Review
  ↓
[Step 6] Founder Approval
  ↓
[Step 7] Implementation
  ↓
[Step 8] Regression Validation
```

**严禁跳过任何步骤。**

---

### Step 1 — Proposal

内容：

```
Proposal: [简短标题]
Author: [是谁提出的]
Problem: [解决什么问题]
Solution: [大致方案]
Core Impact: [是否触碰 Core]
Priority: [P0-P6, 见 Architecture Constitution]
```

### Step 2 — ADR

按 `docs/02_decisions/ADR-TEMPLATE.md` 格式编写。
必须包含 Invariant Impact Assessment 章节。

### Step 3 — Invariant Impact Check

检查矩阵：

```
Invariant     | 是否相关 | 是否违反 | 说明
I-1           | Y/N      | Y/N      | ...
I-2           | Y/N      | Y/N      | ...
...
I-30          | Y/N      | Y/N      | ...
```

**发现任何违反 → 终止。** 除非新 ADR 明确 Supersede 该 Invariant。

### Step 4 — Scenario Test

最少 5 个场景，覆盖：

```
□ 正常场景
□ 边界场景
□ 异常/错误场景
□ 冲突场景（与现有约束冲突时）
□ 拒绝场景（不应触发时）
```

### Step 5 — Security Review

检查：

```
□ 是否可能被滥用
□ 是否可能绕过 Permission Gate
□ 是否可能泄露用户数据
□ 是否有审计跟踪
□ Fallback 行为是否明确
```

### Step 6 — Founder Approval

**最终决策权唯一属于 Founder。** AI 只有建议权。

### Step 7 — Implementation

按人格接口标准实现，使用 TPI 接口，不直接修改 Core。

### Step 8 — Regression Validation

```
□ Core Invariant 全部通过
□ 已有 Scenario 未退化
□ 接口兼容性保持
□ 安全模型未降级
```

---

## 第三部分：禁止清单

### 永久禁止进入 Tang OS

```
❌ 广告推荐系统
❌ 用户行为画像商业化
❌ 情感操控优化留存
❌ AI 独立决策（无用户预设情况下）
❌ 绕过 Permission Gate 的能力
❌ 修改/删除 Core Invariant 的 Extension
❌ 冒充人类身份
❌ 未经用户同意的数据共享
```

### 需 Founder 批准的有争议能力

```
⚠️ 用户情绪数据的匿名化研究
⚠️ 多用户共享 Tang OS 实例
⚠️ 与第三方 AI 系统的互操作
⚠️ 自动健康监测
⚠️ AI 主动预测（非紧急场景）
```

---

## 第四部分：垂直验证 — 老年陪护机器人 DEK

作为方向 C 的第一个 Domain Extension Kit。

### Core 使用（零修改）

```
Persona Runtime        ✅ 人格约束体系直接可用
Emotion Runtime        ✅ 情绪理解直接可用
Safety API             ✅ AN 触发系统直接可用
Permission P0-P3       ✅ 四级权限直接可用
HSL 七道门              ✅ 人类主权直接可用
Memory API             ✅ Consent Gate 直接可用
```

### Extension 需开发

```
AN 码扩展:
  "我摔倒了"     → ACTIVE_HELP
  "药吃完了"     → FAMILY_ALERT
  "今天星期几"   → SILENT_PROTECT (定向检测)

语料适配:
  老年人沟通风格语料
  慢速语音 / 方言支持

权限预设:
  家属权限（监督/紧急联系人）
  设备权限（跌倒检测传感器）

Host Adapter:
  机器人传感器接入（TPI-008）
  语音输入输出（TPI-007）
```

---

## Extension 生命周期

```
Proposal → ADR → Invariant Check → Scenario Test → Security Review
    ↓
Founder Approval
    ↓
Implementation
    ↓
Validation
    ↓
Released
    ↓
Maintenance（定期复审）
    ↓
End of Life（Founder 决定）
```

---

## 协议总结

```
Tang OS Core  = 人格硬件（不可修改）
Extension     = 行业定制（不碰 Core）
Host          = 载体适配（不改变人格）
新能力准入     = 8 步管线（不可跳过）
```
