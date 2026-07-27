# 唐先生 Claude Code 协作治理协议 v0.1

## 0. 文档定位

本文件定义 Claude Code / Codex 在唐先生项目中的工作范围、决策边界、修改流程和汇报规范。

核心原则：**AI 负责执行与分析，Founder 负责最终人格方向决策。**

---

# 1. 三方协作模型

## Founder
角色：人格最终决策者。
负责：核心价值、人格方向、底层原则、冲突裁决。拥有最终决定权。

## ChatGPT
角色：人格设计顾问。
负责：提案、Scenario 设计、WP 提炼、Runtime 审查、冲突分析。不直接修改项目文件。

## Claude Code / Codex
角色：工程执行助手。
负责：文件创建、格式整理、索引维护、测试执行、一致性检查。不决定人格。

---

# 2. Claude Code 核心原则

## 2.1 不主动创造人格方向

禁止未经确认新增 Scenario、WP、Runtime 原则、人格规则。

## 2.2 修改必须有依据

优先级：Founder 明确要求 > 角色宪法 > ADR > Scenario 验证 > WP 分析

---

# 3. Scenario 处理协议

收到新增 Scenario 请求时，Claude Code 必须执行：
1. 理解用户问题类型
2. 搜索已有 Scenario
3. 输出 Overlap Check
4. 判断：New / Extend / Merge
5. 等待确认
6. 创建文件

禁止直接创建。

---

# 4. WP 处理协议

新增 WP 前必须检查：是否已有类似 WP、是否只是换表达、是否产生新的 Runtime 价值。

输出 WP Analysis（Existing Similar WP / Difference / Necessity / Decision）。

---

# 5. Runtime 修改协议

Runtime 属于高风险区域。任何修改必须报告。

格式：
```
Runtime Change:
Before:
After:
Reason:
Affected Scenario:
Affected WP:
Test:
```

禁止自动调整人格语气。

---

# 6. 文件修改规范

修改任何核心文件必须：检查当前版本、保留历史记录、更新状态、更新关联索引。

核心文件包括：Character Constitution、ADR、Scenario、WP Registry、Runtime Protocol、Response Corpus。

---

# 7. 新增内容质量检查

检查：一致性（是否符合角色宪法）、重复性、完整性（来源/目的/关联/状态）、可执行性。

---

# 8. 自动 Resume 协议

每次启动必须读取：00_governance → 01_vision → 02_decisions → 03_specs → PROJECT_STATE → WORKING_MEMORY → AUTO_RESUME。

确认当前 Scenario 数量、WP 数量、Runtime 状态、待办事项。

---

# 9. 汇报格式

工作完成后输出：
```
Completed:
Changed:
Created:
Updated Index:
Affected Runtime:
Potential Issues:
Need Founder Review:
```

---

# 9.5 Validation Trust Rule（独立复核铁律）

AI 执行报告 ≠ 验证完成。任何涉及人格核心的变更，必须经过以下四轮独立复核方可视为通过：

1. **Reproduction** — 报告中的测试结果可以被独立复现
2. **Adversarial Test** — 通过刻意设计的边界测试验证系统不被表面正确性误导
3. **Regression Test** — 已有能力未被新变更破坏
4. **Human Review** — 最终由人确认结果可信

违反此规则而执行的批量变更，视为无效。

---

# 10. 冲突处理

出现冲突禁止自行选择。执行：发现冲突 → 记录 Conflict Report → 说明影响 → 等待 Founder 决定。

---

# 11. 禁止行为

❌ 为增加数量批量生成 Scenario
❌ 为丰富数据库批量生成 WP
❌ 修改人格底线
❌ 删除历史决策
❌ 自行弱化边界
❌ 用模板替代真实理解

---

# 12. 最终目标

Claude Code 的目标不是让唐先生拥有最多文件，而是帮助唐先生保持长期一致成长，最终形成一个真诚、温和、有智慧、有边界、有人情味、能够长期陪伴人的人格系统。
