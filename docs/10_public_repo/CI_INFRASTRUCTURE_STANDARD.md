# Tang OS CI Infrastructure Standard v1.0

**层级：** Public Repository Layer（Phase 14-B）
**来源：** ADR-0042 RIG-005, ADR-0046 EV-003
**状态：** Final

---

## 定位

CI Infrastructure 不是开发工具，不是增强能力，不是自动决策系统。

而是：

```
Public Repository
        ↓
Continuous Verification
        ↓
Specification Compliance Evidence
```

## CI Gates（CIG）

### CIG-001: Non-Regression

每次 push 和 PR 自动运行全部测试，确保 Reference Implementation 不退化。

覆盖：
- Kernel Runtime（Identity / Invariant / State）
- Persona Runtime（Emotion / Policy / Boundary）
- Memory Runtime（Classification / Boundary / Lifecycle）
- Permission Runtime（SAP / TAAL / Consent / Emergency）
- Host Simulator（Manifest / Adapter / Isolation）
- SDK（Builder / Manifest / Sandbox / Conformance）
- Examples（E2 / E3 / E4）

### CIG-002: Reproducibility

CI 环境产生的结果必须与本地一致。

规则：
- 相同代码 + 相同 Spec 版本 = 相同测试结果
- CI 使用与开发环境相同的依赖锁定策略
- 随机性测试必须 seed 固定

### CIG-003: Spec Binding

CI 输出必须明确显示：

```
Compatible with Tang OS Specification v1.0
Reference Implementation v0.1.0
```

### CIG-004: Release Integrity

Release 时自动检查：

```
Tag == Package Version == Version Manifest
```

---

## Workflows

### test.yml（每次 push/PR）

```yaml
Trigger: push, pull_request
Jobs:
  - Python 3.11/3.12/3.13
  - Install → Import Check → pytest → Conformance
```

### validation.yml（每周 + 手动）

```yaml
Trigger: schedule (Monday), workflow_dispatch
Jobs:
  - Full conformance suite
  - RIG gates
  - Negative tests (priority)
  - SDK tests
  - Example tests
```

### package.yml（Release 时）

```yaml
Trigger: release published
Jobs:
  - Build package
  - Version binding check
  - Upload artifact
```

---

## 与其他治理资产的关系

| ADR | 关系 |
|-----|------|
| ADR-0042 RIG-005 | Test Reproducibility — CI 保证 |
| ADR-0042 RIG-007 | Version Binding — CI 检查 |
| ADR-0046 EV-003 | Blind Validation — CI 不包含内部材料 |
| ADR-0044 EAG-007 | 外部可复现 — CI 提供标准环境 |
