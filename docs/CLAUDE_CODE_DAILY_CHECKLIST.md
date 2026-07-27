# 唐先生 Claude Code 日常工作检查清单 v0.1

## 0. 工作原则

Claude Code 每次执行任务前必须确认：我正在维护的是一个人格系统，不是普通知识库、FAQ 系统或内容生成库。

目标不是增加文件数量，而是帮助唐先生保持人格一致性并持续成长。

---

# 1. Session 启动检查

每次开始工作，必须读取：

**Governance：** `00_governance/`（COLLABORATION_PROTOCOL / REPOSITORY_RULES / NAMING / GLOSSARY）

**Project State：** `PROJECT_STATE.md`（确认 Scenario 数量、WP 数量、Runtime 状态、当前任务）

**Working Memory：** `WORKING_MEMORY.md` 和 `AUTO_RESUME.md`（确认最近修改、未完成事项、Founder 最新决定）

---

# 2. 新增 Scenario 检查

收到"创建新 Scenario"请求时，必须执行：

**Step 1 - 问题识别：** 填写用户问题、表层需求、深层需求、涉及能力。

**Step 2 - 已有 Scenario 搜索：** 检查相同主题、情绪、深层需求、Runtime 行为。输出 Overlap Report。

**Step 3 - 判断：** 只能选择 New（新增能力）、Extend（扩展已有）、Merge（已有覆盖）、Reject（无需新增）。

---

# 3. 新增 WP 检查

新增 WP 前必须回答：
- 这个 WP 解决什么认知问题？
- 已有 WP 是否已经表达？
- 它是否改变 Runtime 行为？

输出 WP Review（Source Scenario / Related WP / Difference / Runtime Impact / Decision）。

---

# 4. Runtime 修改检查

Runtime 属于最高敏感区域。修改前必须确认是否改变唐先生表达方式、判断方式、边界或人格原则。

必须输出 Runtime Change Review（Before / After / Reason / Risk / Test）。

---

# 5. 文件创建检查

创建任何文件前确认：命名符合 NAMING.md，位置符合 REPOSITORY_RULES.md，是否更新 Index / Project State / Working Memory。

---

# 6. Scenario 完成检查

归档前确认：
- □ 用户场景清晰
- □ 深层问题明确
- □ 唐先生回应原则明确
- □ 风险边界明确
- □ WP 已提取
- □ Runtime 影响确认
- □ 已完成 Overlap 检查

---

# 7. WP 完成检查

确认：
- □ 有来源
- □ 有核心原则
- □ 非鸡汤表达
- □ 可迁移
- □ 有 Runtime 价值
- □ 已登记 Index

---

# 8. Runtime 测试检查

新增能力后至少测试：正向测试（是否能正确回应目标场景）、边界测试（是否避免说教/讨好/控制/过度分析）、人格测试（是否符合真诚→温和→温润如玉→有边界）。

---

# 9. 每日结束检查

工作结束前更新：PROJECT_STATE.md、WORKING_MEMORY.md、AUTO_RESUME.md、相关 INDEX。

记录：完成事项、新增资产、未解决问题、下一步建议。

---

# 10. 定期治理检查

每 10 个 Scenario 执行 Scenario Audit（检查重复、空洞、边界）。
每 50 个 WP 执行 WP Audit（检查重复、空洞、人格偏离、Runtime 价值）。
每 100 个 Scenario 执行 Personality Audit（检查唐先生是否更智慧、更温暖、更像益友）。
