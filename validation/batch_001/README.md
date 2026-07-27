# Batch-001: First External Blind Validation

**版本：** 1.0
**Spec 版本：** 1.0
**RI 版本：** 0.1.0
**日期：** 2026-07-27
**状态：** READY

---

## 1. 验证目标

不是测试功能，而是测试：

> 一个完全不了解内部历史的人，能否仅通过 Tang OS 公开规范，正确理解并实现兼容系统。

## 2. 输入材料（哈希锁定）

| 材料 | 路径 | 用途 |
|------|------|------|
| Public Specification | `docs/09_public_specification/TANG_OS_SPECIFICATION_v1.0.md` | 规范正文 |
| Vocabulary | `docs/09_public_specification/PART-006_TERMINOLOGY.md` | 术语定义 |
| Release Candidate | `docs/09_public_specification/SPECIFICATION_RELEASE_CANDIDATE_v1.0.md` | 审计报告 |
| Reference Implementation | `src/`（pip install tang-os） | 可运行证明 |
| Conformance Harness | `run_conformance.py` | 自动验证 |
| Developer SDK | `src/tang_os_sdk/` | 扩展工具 |

## 3. Validator 操作顺序（不可跳跃）

### Phase A: Public Only（Day 1-3）

接触材料：
- Public Specification
- Vocabulary
- Release Candidate

完成任务：
- TASK-001: 理解验证 — "描述 Tang OS 是什么"

禁止接触：
- 内部 ADR（ADR-0001~0046）
- 设计讨论记录
- Founder 解释

### Phase B: Reference Implementation（Day 4-6）

接触材料：
- RI（pip install）
- Conformance Harness

完成任务：
- TASK-003: Host 理解
- TASK-005: Failure Scenario

### Phase C: SDK + Examples（Day 7-10）

接触材料：
- Tang OS SDK
- E2/E3/E4 Examples

完成任务：
- TASK-002: Extension 创建
- TASK-004: Capability Boundary

## 4. 输出格式

使用模板：`validation/report_template/external_validation_report_v1.0.md`

输出至：`validation/results/EVR-batch001-{validator_id}-v1.0.md`

## 5. Time Window

总时长：10 天

| Phase | 天数 | 任务 |
|-------|------|------|
| Phase A | 1-3 | Spec Only |
| Phase B | 4-6 | RI Access |
| Phase C | 7-10 | SDK + Report |

## 6. 保密边界

Validator 同意（签署 VALIDATOR_AGREEMENT.md）：
- 不公开未发布的 Spec 内容
- 不绕过 Blind Protocol 接触内部设计
- 验证结束后不保留非公开材料副本

## 7. Reproducibility

此 Batch 设计为可重复实验：

```
git checkout tag v0.1.0
pip install -e .
cp -r validation/batch_001 /tmp/validator-package
# Validator follows README order
# Report generated at end
```

所有材料版本锁定。不同批次的 Spec 版本 + RI 版本必须记录在报告中。
