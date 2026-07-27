# Tang OS Release Engineering Standard v1.0

**层级：** Public Repository Layer（Phase 14-C）
**来源：** ADR-0042 RI-007, ADR-0040 PRB-006
**状态：** Final

---

## 1. 版本体系

```
Specification:  v1.x     — 规范版本（Semantic Versioning）
Reference Impl: v0.x     — 实现版本（实验阶段前缀 v0）
Experimental:   v0.x-alpha — 实验版本
```

### 版本对应规则

| 组件 | 版本 | 说明 |
|------|------|------|
| Specification | v1.0 | 规范冻结版本 |
| Reference Implementation | v0.1.0 | 对应 Spec v1.0 |
| SDK | v0.1.0 | 随 RI 发布 |
| TPI Interface | v1.0.0 | 独立版本，独立于 Runtime |

## 2. Git Tag 规范

```
v{semver}
```

示例：
- `v0.1.0` — 首次公开发行
- `v0.1.1` — Bug 修复
- `v0.2.0` — 新增非 Core 功能
- `v1.0.0` — Specification + Implementation 同步 Major

**禁止：**
- `latest`, `stable`, `release` 等非版本 Tag
- Tag 与 setup.py 版本不一致

## 3. Release Artifact Integrity（RE-003）

每个 Release 必须包含以下工件，且版本一致：

```
Git Tag:    v0.1.0
setup.py:   version="0.1.0"
MANIFEST:   implementation.version == "0.1.0"
CI Check:   Tag == Package == Version Matrix
Spec:       "Compatible with Tang OS Specification v1.0"
```

不允许出现：
- Tag v0.1.0 但 package 为 v0.1.1
- Release 未包含 Conformance 结果
- Release 未包含 Version Binding 声明

## 4. Release Package 结构

```
tang-os-{version}.tar.gz
├── src/tang_os/           — Runtime Core（Layer 1）
├── src/tang_os_sdk/       — Developer SDK（Layer 2）
├── tests/                 — 完整测试套件
├── validation/            — Blind Validation Protocol
├── examples/              — E2/E3/E4
├── docs/09_public_specification/ — Specification v1.0
├── run_conformance.py     — 验证入口
├── pyproject.toml
├── setup.py
├── README.md
├── LICENSE
├── CHANGELOG.md
└── VERSION                 — 纯文本版本号文件
```

**不包含：**
- `.claude/` — 内部配置
- `.doc/` — 设计记忆
- `archive/` — 历史审计
- 内部 ADR Draft

## 5. GitHub Release 模板

### Release Title

```
Tang OS Reference Implementation v0.1.0
```

### Release Body

```markdown
## Tang OS Reference Implementation v0.1.0

**Compatible with Tang OS Specification v1.0.**

This release is a reference implementation.
It does not define the specification.
It does not claim to be "the official Tang OS implementation."

### What's Included

- Kernel Runtime: Identity, Invariant, State
- Persona Runtime: Emotional State, Response Policy, Relationship Boundary
- Memory Runtime: Three-tier Classification, Boundary, Lifecycle
- Permission Runtime: SAP L0~L3, TAAL A0~A4, Emergency Protocol
- Host Simulator: Manifest, Adapter, Sensor, Actuator, Isolation
- Developer SDK: ExtensionBuilder, ManifestValidator, SandboxAPI
- TPI Interface Package: 8 personality API contracts
- Conformance Harness: RIG-001~007, Negative Tests
- Example Applications: E2 Extension, E3 Host, E4 Emergency

### Installation

```bash
pip install tang-os==0.1.0
```

### Verification

```bash
python run_conformance.py
# Expected: ✅ CONFORMANT
```

### Tests

324 tests, 100% pass rate.

### Governance

46 Architecture Decision Records (ADR-0001~0046)

### Constraints

- This is a reference implementation (v0.x).
- It does NOT define the Tang OS specification.
- Core Identity is immutable.
- Extension cannot modify personality.
- Emergency authority is temporary and auditable.
```

## 6. Release Checklist（RE-001）

| Step | Check | Status |
|------|-------|--------|
| 1 | Version consistency（Tag == setup.py == MANIFEST） | ⬜ |
| 2 | Changelog updated | ⬜ |
| 3 | All tests pass | ⬜ |
| 4 | Conformance harness passes | ⬜ |
| 5 | Release notes written | ⬜ |
| 6 | Package built (`python -m build`) | ⬜ |
| 7 | Version binding declared | ⬜ |
| 8 | Disclaimer included | ⬜ |

## 7. Hotfix / Rollback 流程（RE-005）

### Hotfix
```
v0.1.0 → bug found → v0.1.1 (仅修复，不新增功能)
```

### Rollback
```
v0.1.1 → 问题严重 → 回退到 v0.1.0
```

**规则：**
- 不覆盖已发布的 Release
- v0.1.0 始终可访问
- Rollback 后发布 v0.1.2 包含回退原因

## 8. PyPI 发布策略

由 Founder 决定：

| 选项 | 策略 | 适合阶段 |
|------|------|---------|
| TestPyPI | `pip install -i https://test.pypi.org/simple/ tang-os` | 验证发布流程 |
| PyPI | `pip install tang-os` | 正式公开 |
| GitHub Releases | `pip install https://github.com/tang-os/tang-os/releases/...` | 当前阶段推荐 |

**当前建议：** GitHub Releases 先行，PyPI 在 External Validation 通过后。
