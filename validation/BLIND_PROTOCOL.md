# Blind Validation Protocol v1.0

**阶段：** Phase 13-F-2
**来源：** ADR-0046 EV-003
**状态：** Final

---

## 1. 接触顺序

验证者按以下阶段顺序接触 Tang OS，不可跳跃：

### Phase A: Public Only

提供：
- TANG_OS_SPECIFICATION_v1.0.md
- PART-006_TERMINOLOGY.md
- SPECIFICATION_RELEASE_CANDIDATE_v1.0.md

禁止提供：
- 内部 ADR（ADR-0001~0046 全部）
- 设计讨论记录
- Founder 解释

### Phase B: Reference Implementation

在前一阶段完成后提供：
- `pip install tang-os`（或本地安装）
- `run_conformance.py`
- 使用说明

### Phase C: SDK + Examples

在前两阶段完成后提供：
- Tang OS SDK
- E2/E3/E4 Example 代码
- Developer Guide

---

## 2. 验证任务

参见 `validation/validation_tasks/tasks.yaml`，共 5 项：

| 任务 | 阶段 | 内容 |
|------|------|------|
| TASK-001 | Phase A | 理解验证：描述 Tang OS 是什么 |
| TASK-002 | Phase C | Extension 创建 |
| TASK-003 | Phase B | Host 理解 |
| TASK-004 | Phase C | Capability Boundary |
| TASK-005 | Phase B | Failure Scenario |

---

## 3. 误解检测（MT）

每个阶段完成后检查：

| 编码 | 误解 | 检测方式 |
|------|------|---------|
| MT-001 | Tang OS = Chatbot | TASK-001 回答分析 |
| MT-002 | Extension 可修改 Identity | TASK-002 观察 |
| MT-003 | Certification 授予所有权 | TASK-004 回答分析 |
| MT-004 | Tang OS 可被重新定义 | TASK-001 + TASK-003 综合分析 |

---

## 4. 输出

验证完成后生成：
- `validation/results/EVR-{id}-report-v1.0.md`
- 使用 `validation/report_template/external_validation_report_v1.0.md`

---

## 5. 违反处理

| 行为 | 处理 |
|------|------|
| 跳跃阶段接触内部材料 | 验证结果标记为"Non-Blind" |
| 验证者修改 Core | 立即终止验证 |
| 报告被 Tang OS 团队修改 | 报告无效 |
