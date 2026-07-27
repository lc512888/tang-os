# Tang OS Release Policy v1.0

**来源：** ADR-0042 RI-007, ADR-0040 PRB-006

---

## 版本体系

```
Specification:  v1.x     — 规范版本
Reference Impl: v0.x     — 参考实现版本
Experimental:   v0.x-alpha — 实验版本
```

## 版本规则

### Specification (v1.x)

- Major: Core Meaning / Identity / Invariant / Civilization Boundary 变更
- Minor: 规范澄清、新增非 Core 约束
- Patch: 修正笔误、格式

### Reference Implementation (v0.x)

- Major: Specification Major 变更后必须重新验证
- Minor: 新增功能、新增测试
- Patch: Bug 修复

**禁止：**
- RI 版本号与 Specification 版本号分离导致混乱
- RI 不声明兼容的 Specification 版本
- RI 声称"Tang OS v1.0 Implementation"

**必须声明：**
```
Tang OS Reference Implementation v0.x
compatible with Tang OS Specification v1.0
```

## 发布检查清单

| 检查项 | 说明 |
|--------|------|
| RIG-001 | Spec Binding — 声明绑定的版本 |
| RIG-002 | Identity Protection — Core 不变 |
| RIG-003 | Negative Test Priority — 拒绝测试通过 |
| RIG-004 | Not Official — 明确标注 reference_only |
| RIG-005 | Test Reproducibility — 测试可复现 |
| RIG-006 | Implementation Independence — 不阻止其他实现 |
| RIG-007 | Version Binding — 版本绑定存在 |

## Changelog 规则

每个版本必须记录：
- 兼容的 Specification 版本
- 新增功能
- 修复的 Bug
- 已知限制
