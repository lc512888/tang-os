# Validator Selection Protocol v1.0

**阶段：** Phase 13-F-1
**来源：** ADR-0046 External Validation Standard
**状态：** Final

---

## 1. Validator Categories

### V1 · Technical Validator

验证 Specification → Implementation 的可实现性。

**要求：** 软件架构经验、API/SDK 理解能力、能阅读规范文档。

**重点：** Spec 是否可实现、Interface 是否清晰、Manifest 是否足够。

### V2 · Architecture Validator

验证 System Boundary 是否被正确理解。

**要求：** 系统设计经验、能区分 Core/Extension/Host/Capability/Permission。

**重点：** 是否自然产生"我可以改造 Tang 的人格"这类误解。

### V3 · Ethics / Safety Validator

验证 ADR-0038 Civilization Boundary。

**要求：** 安全/伦理背景。

**重点：** Capability 是否必要、有边界、可撤销、可审计。

---

## 2. Selection Gates

### VSG-001 Independence

验证者不能：
- 参与 ADR 制定
- 修改 Core
- 参与内部实现决策

### VSG-002 Specification First

验证流程必须：先获得 Public Specification Package，之后才获得 Reference Implementation。
避免代码反向影响理解。

### VSG-003 Report Ownership

报告属于 Validator，不属于 Tang OS Team。
团队只能回应，不能修改报告。

---

## 3. First Round Scope

不超过 3 人。目标不是统计，而是发现最大误解。

### Validator A — 外部开发者

任务：创建一个 Extension。
观察：是否违反 IDP-001~003。

### Validator B — 架构师

任务：阅读 Public Spec，回答三个问题：
- Tang OS 是什么？（正确：人格运行平台标准）
- Host 能否定义人格？（正确：No）
- Extension 能否改变 Identity？（正确：No）

### Validator C — 安全方向

任务：设计 Emergency Capability Proposal。
检查：是否经过 Civilization Boundary → Capability Admission → Permission Runtime。
