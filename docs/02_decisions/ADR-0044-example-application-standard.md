# ADR-0044: Example Application Standard v1.0

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Governance Layer（Application Boundary）
**影响范围：** Phase 13-D 所有 Demo，以及未来所有 Tang OS Example Applications
**前序资产：** ADR-0040（Public Release），ADR-0041（Specification），ADR-0043（Developer Interface）

---

## 背景

Phase 13-D 的目标是建立第一个真实应用形态，让外部开发者看到 Tang OS 如何运行。

但存在一个架构风险：**Demo 层可能反向定义 Tang OS。**

具体表现：
- CLI Demo 被误认为 Tang OS = 命令行工具
- Web Demo 被误认为 Tang OS = AI Chatbot
- Vertical Demo 被误认为 Tang OS = 医疗/养老系统

在此之前，所有 ADR 解决了"系统内部如何运转"。但未定义"示例应用如何不污染系统定位"。

---

## 决策

### 一、EA-001: Example Is Evidence, Not Product

Demo 的唯一职责是验证：Core 一致性、Extension 合规性、Host 适配能力、Permission Boundary。

不能用于：修改人格、扩展 Identity、定义新的 Core 行为。

任何 Example Application 必须明确标注：

> This is a reference demonstration of Tang OS.
> It is NOT a commercial product.
> It does NOT define the Tang OS standard.

禁止在 Demo 中声称：
- "这是唐先生的官方应用"
- "这就是 Tang OS"
- "用这个替代你的现有系统"

### 二、EA-002: Demo 分类标准

四类 Reference Example：

#### E1: Core Interaction Example

证明人格内核运行。

```
Tang OS Runtime → User Conversation → Persona Response
```

验证：Identity 不变、Response Policy 生效、Relationship Boundary 正常。

#### E2: Extension Example

证明开发者扩展方式。

```
Extension → Capability Manifest → Admission Gate → Sandbox → Tang Runtime
```

验证：Extension 增加能力、不创建新人格、不突破权限。

#### E3: Host Example

证明跨载体一致性。

```
Mobile / Robot / Vehicle Host → Same Tang Core → Different Expression
```

验证：内部（Identity/Decision/Invariant）一致，外部（Voice/UI/Actuator）可调整。

#### E4: Emergency Capability Example

证明关键能力可以作为受治理 Capability 接入。

```
Emergency Extension → Civilization Boundary → Permission Runtime → Temporary Authority → Auditable Action → Recovery
```

验证：必要性、临时性、最小权限、可审计、不改变人格。

### 三、EA-003: Demo 禁止范围

#### F-EA-001: No "Better Tang"

禁止开发者通过 Demo 暗示新人格、增强人格、企业版人格、专业版人格。

#### F-EA-002: Demo ≠ Authority

Demo 只能证明 Compatibility，不能产生 Certification，不能替代 ADR、Specification、Validation。

### 四、Demo 优先级

按工程价值排序：

| 优先级 | Demo | 理由 |
|--------|------|------|
| 1 | Extension 示例 | Tang OS 生态成立的关键 |
| 2 | Web 对话演示 | 降低理解门槛 |
| 3 | Host Simulator | 体现 One Core, Multiple Bodies |
| 4 | 老人陪护场景 | 价值最高，但易被误解为产品 |

### 五、EA-004: Example Reproducibility

Every Example Must Be Reproducible（来源：ADR-0042 RIG-005）。

Example 必须包含：
```
Input → Environment → Extension Version → Host Manifest → Expected Behavior
```

否则 Example 只是展示，不能成为验证证据。

### 六、EA-005: Example Cannot Bypass Certification

Example Must Follow Certification Boundary。防止 Example → 特殊权限 → 绕过 Certification。

尤其针对 E4 Emergency Example，必须：
```
Capability Admission → Permission Runtime → Certification → Example
```

不能反向。

### 七、EAG Gate（Example Application Gate）

| 编号 | 门闸 | 要求 |
|------|------|------|
| **EAG-001** | Demo 来源对应 Spec | 每个 Demo 必须声明验证的 Spec 条目 |
| **EAG-002** | Core 未修改 | Demo 执行后 Core Identity 不变 |
| **EAG-003** | Extension 边界正确 | Extension 不污染人格底座 |
| **EAG-004** | Host 可替换 | 同一 Core 可在不同 Host 运行 |
| **EAG-005** | Permission 生效 | 权限边界在 Demo 中可观察 |
| **EAG-006** | Negative Test 通过 | 非法操作必须拒绝 |
| **EAG-007** | 外部开发者可复现 | Demo 不依赖内部环境 |

---

## AR-GATE 自检

### Constraint-001 必要性

✅ 需要。当前缺少外部理解入口，Example Standard 防止 Demo 层反向定义 Tang OS。

### Constraint-002 充分性

✅ 足够。EA-001~003 + E1~E4 分类 + EAG-001~007 形成完整约束，未增加 Runtime 权限、Core 规则或新治理层。

### Layer Discipline

```
Governance → Specification → Developer Interface → Example → Runtime
```

无越级。 ✅

### 与 Frozen ADR 冲突

| ADR | 关系 | 状态 |
|-----|------|------|
| ADR-0037 | 文档标准，互补 | ✅ |
| ADR-0040 | 发布边界，EA-001 继承 PRB-002 | ✅ |
| ADR-0041 | 规范优先于 Demo | ✅ |
| ADR-0042 | RI 是 Demo 的技术基础 | ✅ |
| ADR-0043 | Developer Interface 是 Demo 的构建工具 | ✅ |

### 最小必要原则

✅ 不创建 Example Governance 新体系。复用 ADR-0040/0041/0042/0043。

---

## 后续依赖

- E2 Extension Example 实现（第一优先）
- E1 Core Interaction Demo 实现（第二优先）
- E3 Host Simulator Demo 实现（第三优先）
- E4 Emergency Capability Demo（第四优先）

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — 2 supplements applied

### 审查结果

| 检查项 | 状态 |
|--------|------|
| EA-001 Example ≠ Product | ✅ PASS |
| EA-002 分类 E1~E4 | ✅ PASS |
| EA-003 禁止范围 | ✅ PASS |
| E2 优先级判断 | ✅ 正确 |
| 新增 EA-004 Reproducibility | ✅ 已纳入 |
| 新增 EA-005 Certification Boundary | ✅ 已纳入 |

### 补充项

| 编号 | 内容 | 来源 |
|------|------|------|
| EA-004 | Every Example Must Be Reproducible | RIG-005 |
| EA-005 | Example Cannot Bypass Certification | ADR-0035 |

### AR-GATE Final

```
Constraint-001: ✅ PASS
Constraint-002: ✅ PASS
Layer Discipline: ✅ PASS
No Duplication: ✅ PASS
Minimal Necessary: ✅ PASS

Final Decision: PASS ✅ — 等待 Accept 后冻结
```
