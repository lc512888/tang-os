# Architecture Review Gate v1.0

**生效日期：** 2026-07-27
**层级：** Governance Layer（高于 ADR）
**适用范围：** 所有新增 ADR、Invariant、Standard、Interface、Runtime Module、Test Gate、Governance Rule

---

## Constraint-001: 充分必要性约束（Sufficiency & Necessity Constraint）

任何新增设计必须同时满足必要性和充分性。

### 必要性（Necessity）

必须回答：**如果没有这个设计，会导致什么已知工程风险？**

必须明确对应以下至少一项风险：
- 架构风险
- 安全风险
- 边界风险
- 一致性风险
- 可维护性风险

无对应风险 → **Reject**。

### 充分性（Sufficiency）

必须回答：**这个设计是否足以解决目标问题？**

禁止：
- 表面描述
- 重复已有规则
- 增加文档复杂度
- 增加管理成本但未增加实际约束能力

无实际约束提升 → **Reject**。

### 检查格式

```
Need:
为什么必须存在？

Solve:
解决什么风险？

Gap:
已有体系哪里不足？

Result:
新增后是否形成闭环？
```

---

## Constraint-002: 工程一致性约束（Engineering Consistency Constraint）

任何设计必须符合 Tang OS 工程模型：

```
Principle
    ↓
Standard
    ↓
Interface
    ↓
Runtime
    ↓
Validation
```

### 禁止模式

**1. Principle → Runtime 越级**
- 错误：直接写代码实现尚未定义的能力
- 必须：原则定义 → 标准冻结 → 接口设计 → 实现

**2. Runtime 反向定义 Core**
- 错误：根据实现方便修改人格原则
- 禁止：Implementation → Modify Core
- 只能：Core → Runtime

**3. 新模块重复已有能力**
- 审查是否已有 Core Identity / Personality Runtime / Memory Runtime / Permission Runtime / Capability Admission / Host Boundary 覆盖
- 如已有覆盖：必须走 Extension，不能创建平行系统

**4. 增加复杂度但不增加约束能力**
- 判断标准：复杂度增长与约束收益之比
- 复杂度 +10、约束收益 +2 → **Reject**
- Tang OS 追求：**最小必要约束集（Minimal Necessary Constraint Set）**

---

## Architecture Review Gate 输出格式

每次架构输出末尾增加：

```
AR-GATE

Constraint-001 Sufficiency/Necessity

Necessary:
PASS / FAIL

Sufficient:
PASS / FAIL


Constraint-002 Engineering Consistency

Layer Correct:
PASS / FAIL

No Duplication:
PASS / FAIL

Complexity Justified:
PASS / FAIL


Final Decision: PASS → Continue / FAIL → Re-review
```
