# Tang OS Vocabulary v1.0

**层级：** PSL-2 Normative Spec（ADR-0041 PS-004）
**来源：** ADR-0037 DI-003

---

## 核心术语

| 标准术语 | 禁止替代 | 定义 |
|---------|---------|------|
| **Tang OS** | AI Agent, Digital Human, Companion Bot, Persona Model | 人格运行平台标准 |
| **Core** | Base Model, Engine, Kernel | 不可修改的人格内核（Identity + Invariant + Decision + Safety + Memory） |
| **Personality Interface (TPI)** | Prompt, Template, API 接口 | 8 个标准人格接口 |
| **Extension** | Plugin, Module, Add-on, Skill | 在 TPI 之上的受治理扩展 |
| **Host** | Device, Platform, Hardware, 载体 | Core 的运行载体（不定义人格） |
| **Certification** | Verification, Approval, 认证 | 实现兼容性验证 |
| **Validation** | Testing, QA, 验证 | 一致性验证过程 |
| **Invariant** | Rule, Constraint, 规则 | 不可修改的不变性（I-1~I-30） |
| **Identity Constitution** | 人格定义、角色设定 | 三层身份宪法（不可修改） |
| **Civilization Boundary** | 伦理准则、道德规则 | 能力文明边界（最高约束层） |
| **Capability Manifest** | 功能描述、能力声明 | Extension 的标准化声明文件 |
| **Host Manifest** | 设备信息、配置 | Host 的标准化声明文件 |
| **Permission Runtime** | 权限系统、授权模块 | 行动权限运行时 |
| **SAP Level** | 安全等级、操作模式 | Safety Assisted Autonomy 四级 |
| **TAAL** | 权限等级、行动级别 | Tang Action Authority Level 五级 |

---

## 行动等级术语

| 标准术语 | 含义 |
|---------|------|
| **A0 Information** | 信息提供 |
| **A1 Suggestion** | 建议 |
| **A2 Assistance** | 辅助执行 |
| **A3 Protective Action** | 保护行动 |
| **A4 Emergency Autonomous** | 紧急自主行动 |

---

## 扩展分类术语

| 标准术语 | 含义 |
|---------|------|
| **C1 Knowledge Extension** | 知识增强 |
| **C2 Capability Extension** | 能力增强 |
| **C3 Action Extension** | 行动能力 |
| **C4 Critical Action Extension** | 高风险行动能力（非更高级） |
