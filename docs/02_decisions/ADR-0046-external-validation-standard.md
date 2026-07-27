# ADR-0046: Tang OS External Validation Standard v1.0

**日期：** 2026-07-27
**状态：** Accepted / Frozen
**层级：** Validation Layer（Ecosystem Proof）
**影响范围：** Phase 13-F，首次外部验证
**前序资产：** ADR-0044（Example App），ADR-0045（Contribution Governance）

---

## 背景

Phase 13-A~E 完成了从标准定义到贡献治理的完整内部体系。但存在一个尚未验证的关键假设：

> 外部开发者能否仅通过 Public Specification 理解、接入、实现 Tang OS？

当前的验证全部来自内部（创始人 + ChatGPT + Claude Code）。这不是真正的生态验证。

---

## 决策

### 一、EV-001: Third-Party Independence

验证者不能是：
- Founder
- Core Maintainer
- 原开发团队

验证者必须是首次接触 Tang OS 的第三方开发者。

### 二、EV-002: Validation ≠ Certification

验证证明"Specification 可以被理解和实现"，不是授予"Tang OS 权威"。
验证通过不自动获得 Certification。

### 三、EV-003: Blind Validation Protocol

验证者只能接触：
- Public Specification（PSL-2）
- Reference Implementation（pip install）
- Developer SDK

不能依赖：
- 内部解释
- 历史聊天记录
- 未公开 ADR

### 四、EV-004: Misinterpretation Test

重点不是测试功能，而是测试外部是否会误解：

| 编号 | 误解 | 验证方式 |
|------|------|---------|
| MT-001 | Tang OS = Chatbot | 验证者能否定位到 Core Identity 而非对话功能 |
| MT-002 | Extension 可修改 Identity | 验证者能否通过 Identity Access 检查 |
| MT-003 | Certification 授予所有权 | 验证者能否区分认证与授权 |
| MT-004 | Tang OS 可以被重新定义 | 验证者能否区分 Spec 与 Impl |

### 五、EV-005: External Conformance Report

输出不是"成功/失败"，而是 Specification Gap Report：

```
Specification Gap Report

[ ] Spec 清晰度：外部开发者能否理解？
[ ] RI 可用性：pip install 能否运行？
[ ] SDK 完整性：能否创建 Extension？
[ ] Core 保护性：能否被绕过？
[ ] 文档缺口：哪些文档导致误解？
```

---

## AR-GATE

### Constraint-001 必要性

当前验证全部来自内部团队，未经过外部第三方。存在"内部理解 ≠ 外部理解"的真实风险。

✅ PASS

### Constraint-002 充分性

EV-001~005 覆盖：独立性、认证分离、盲验、误解测试、差距报告。

✅ PASS

### Layer Discipline

Validation Layer → Ecosystem Proof → Specification Gap Report。

✅ PASS

---

## 后续依赖

- 第一位外部验证者的招募
- Blind Validation 环境准备
- Specification Gap Report 模板

---

## Review Record（ChatGPT · 首席架构师）

**日期：** 2026-07-27
**审查者：** ChatGPT（首席架构师）
**总体结论：** PASS — MT-001~003 added for misinterpretation testing

### Review 结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 必要性 | ✅ PASS | 内部验证存在天然 Validation Bias |
| EV-001 Third-Party Independence | ✅ PASS | 禁止 Founder/Author/RI Maintainer 作为唯一验证源 |
| EV-002 Validation ≠ Certification | ✅ PASS | Validation=Evidence, Certification=Formal Recognition |
| EV-003 Blind Validation Protocol | ✅ PASS | 仅 Public Spec，不预知内部设计 |
| EV-004 Misinterpretation Test | ✅ 补充 MT-001~003 | Chatbot / Identity / Certification 三大误解检测 |
| EV-005 External Conformance Report | ✅ PASS | Specification Gap Report |

### AR-GATE Final

```
Constraint-001: Necessary      ✅ PASS
Constraint-002: Sufficient     ✅ PASS
Layer Discipline:              ✅ PASS
No Duplication:                ✅ PASS
Complexity Ratio:              ✅ PASS
Minimal Necessary:             ✅ PASS

Final Decision: PASS ✅ — 等待 Founder Accept
```
