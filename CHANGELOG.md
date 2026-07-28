# Changelog

## v0.1.0-alpha (2026-07-28)

### 新增架构

- **ADR-0047: LLM Provider Interface & Integration Boundary** — 人格逻辑与模型能力正式分离
- **LLMProvider 抽象接口** — `generate()` / `stream()` / `health_check()` 契约
- **ExpressionContext 协议层** — `to_chat_messages()` 标准化消息格式

### 新增 Provider

- **DeepSeek Provider** — 首个真实 LLM Adapter（OpenAI 兼容 API）
- **OpenAI / Claude / Local Provider Skeleton** — 参考适配器框架

### 新增验证

- **Persona Validation Framework** — 4 个行为场景验证人格一致性
- **Dependency Risk 分级** — LOW / MEDIUM / HIGH 三级依赖风险检测
- **Retaliation Intent Detection** — 独立于情绪识别的行为意图检测
- **External Validation Suite** — 首次用户操作流测试（11 项）

### 开发者体验

- **README 第一屏重构** — 定位声明 + 架构图 + Provider 表格
- **Try in 5 Minutes** — 三行命令从安装到运行
- **Quick Start** — 可复制运行的示例代码
- **Integration Guide** — 5 份 Provider 接入文档

### 测试

- **382 tests, 100% pass rate** (from 280)
- 4 skipped (需 DeepSeek API Key 的全管线测试)

---

## v0.1.0 (2026-07-27)

**兼容 Specification v1.0.**

### 新增

- Kernel Runtime: Identity / Invariant / State
- Persona Runtime: Emotional State / Response Policy / Relationship Boundary
- Memory Runtime: Three-tier Classification / Boundary / Lifecycle
- Permission Runtime: SAP Levels / TAAL / Consent / Emergency
- Host Simulator: Manifest / Adapter / Sensor / Actuator / Isolation
- Developer SDK: ExtensionBuilder / ManifestValidator / SandboxAPI / ConformanceRunner
- TPI Interface Package: 8 personality API contracts
- Capability Manifest Generator + Admission Evaluator
- Example Applications: E2 Extension / E3 Host / E4 Emergency
- Conformance Harness: RIG-001~007 + Negative Tests
- Validation Infrastructure: Blind Protocol + Report Template

### 治理

- 46 ADRs (ADR-0001~0046)
- Governance Layer: Civilization Boundary / Ecosystem / Certification / Extension / Documentation / Public Release / Specification / Developer Interface / Example / Contribution / External Validation

### 测试

- 280+ tests, 100% pass rate
