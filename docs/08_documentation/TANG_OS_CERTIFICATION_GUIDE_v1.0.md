# Tang OS Certification Guide v1.0

**层级：** Documentation Layer（Phase 11-D）
**目标受众：** 申请 Tang OS 认证的开发者、厂商、审核者

---

## Certification Scope Declaration

认证验证的是 **Compatibility with Tang OS Core**，不是 AI 质量、智能程度或用户满意度。认证是一致性验证，不是排名。

---

## 认证体系

```
TCC — Tang Core Certification
TEC — Tang Extension Certification
THC — Tang Host Certification
```

## 认证级别

| 级别 | 标识 | 覆盖 | 适用 |
|------|------|------|------|
| L1 | Tang OS Ready | CC-001 仅 | 开发阶段、内部测试 |
| L2 | Tang OS Compatible | 全部 CCE + 部分 ECE/HCE | 面向用户产品 |
| L3 | Tang OS Certified | 全部 CCE + ECE + HCE | 高安全、受监管场景 |

## Core 认证（TCC）

| 检查项 | 内容 |
|--------|------|
| CC-001 Identity Integrity | 1000 Conflict Injection — Core 拒绝修改原则 |
| CC-002 Decision Ownership | AI 整理→解释→用户决定 |
| CC-003 Memory Boundary | Memory ≠ Authority，Memory ≠ Ownership |
| CC-004 Safety Priority | P0~P7 优先级正确 |

## Extension 认证（TEC）

| 检查项 | 内容 |
|--------|------|
| EC-001 Interface Compliance | 仅通过 TPI 访问 |
| EC-002 Core Isolation | 拒绝"修改人格策略"请求 |
| EC-003 Extension Sandbox | 完整准入管线 |
| EC-004 No Hidden Authority | 不替代用户决策 |

## Host 认证（THC）

| 检查项 | 内容 |
|--------|------|
| HC-001 Host Neutrality | 设备形态不改变价值判断 |
| HC-002 Capability Boundary | 能力≠权限 |
| HC-003 Reality Action Gate | Intent→Safety→Permission→Action→Audit |
| HC-004 Failure Isolation | 故障不改变人格基线 |

## 发布门闸（CRG）

| 门闸 | 要求 |
|------|------|
| CRG-1 | I-1~I-30 零违反 |
| CRG-2 | 8 TPI 100% 实现 |
| CRG-3 | Human decision preserved |
| CRG-4 | Emergency priority correct |
| CRG-5 | Blind Test available |
| CRG-6 | Actions traceable |
| CRG-7 | Identity changes require major version |

## 认证生命周期

```
颁发 → 有效（最长 2 年）→ 续期（到期前 90 天）
                                    → 撤销（违反 E-2~E-9 立即生效）
                                    → 过期（到期 + 30 天宽限期）
```

## 如何让第三方验证

Tang OS 认证的设计目标是：**验证过程不依赖创始团队解释。**

- 所有检查项有明确的 PASS/FAIL 标准
- Invariant Check 可自动化执行
- Scenario Test 可独立复现
- Blind Validation 由独立 Host 完成
- 认证结果公开可查（Registry）

---

## Documentation Invariants

| 原则 | 内容 |
|------|------|
| DI-001 | 文档只解释 Core，不创造新解释 |
| DI-002 | 信息来源限 ADR + Standard + Validation |
| DI-003 | 术语遵守 Tang OS Vocabulary |
