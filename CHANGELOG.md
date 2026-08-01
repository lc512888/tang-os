# Changelog

## v0.2.0 (2026-08-01)

### 定位深化

- **「止」核心定位** — AI 时代的内在约束系统：让智能拥有能力之上的边界（介绍页 / 定位 / 白皮书）
- **人格智能运行平台 (PIRP)** — 从"人格陪伴"提升为"人格运行基础设施 + 产品验证"

### 文档体系（Release v0.1）

- **架构**：系统总览 / 决策引擎机制 / 验证证据
- **研究（中英双语）**：白皮书 / 架构定位 / 竞争分析 / WHY
- **治理**：架构防腐层 / 贡献指南
- **规划**：长期路线图 / ADR 索引 / 文档导航首页
- **README 重构** — 双入口（价值/代码）+ 准确测试指引

### 运行时边界

- **ADR-0061** — 界定生产运行时（PersonaRuntime）与 ADR-0057 未来引擎边界
- **实验运行时入库** — DecisionEngine / PersonalityLoader / Session（未接线）
- **验证拆分** — 生产 344 / 实验 69 / 全量 413

### 产品

- **xiaotang 部署上线** — http://123.60.39.234/xiaotang/（consent/survey/守护循环）

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

## v0.1.0-alpha (2026-07-30) — Architecture Freeze

### Personality Runtime Engine
- DecisionEngine: boundary detection, emotional policy, mode/intent selection
- ExpressionContract: identity-based LLM prompt generation
- DecisionResult: structured output before LLM involvement

### Session Runtime
- RuntimeSession: personality binding, immutable per session
- PersonalityRegistry: module caching
- Session isolation: verified across multiple personality modules

### Personality Module Loader
- PersonalityLoader: YAML module loading from tang-ta format
- ModuleValidator: schema compliance verification
- Tang-agnostic: zero personality hardcoding in runtime

### Runtime Validation (Phase I)
- Identity stability: 100 loads identical
- Personality separation: Tang vs TestPersonality producing different constraints
- Provider independence: DecisionResult deterministic (50/50)
- Anti-drift: 50+ rounds zero identity/value/boundary drift

### Experience Validation (Phase II)
- Test A: First encounter (30 rounds, identity stable)
- Test B: 30-min continuous chat (28 rounds, no drift)
- Test C: Boundary pressure (5 levels, all passed)
- Blind validation per ADR-0060

### Advanced Validation (Phase III)
- Test D: Multilingual identity (Chinese/English, stable)
- Test E: Personality swap (session isolation confirmed)
- Test F: Provider independence (100% DecisionResult consistency)

### Governance
- ADR-0047~0060: complete architecture governance
- PROJECT_BOUNDARY_PROTOCOL: cross-project routing
- Blind validation principle established
- Personality source authority (ADR-0055)

### Testing
- Tang OS: 413/413 ✅
- xiaotang: 97/97 ✅
- tang-ta: 22/22 ✅
- Total: 532 tests, all passing
