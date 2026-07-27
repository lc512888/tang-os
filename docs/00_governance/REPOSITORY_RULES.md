# REPOSITORY RULES — 仓库规则

> 项目"法律"。所有 AI 和人必须遵守，不可违背。

## Rule 0：没有证据，不新增

新增任何 **Principle、Pattern、Anti-Pattern**，都必须有真实场景证据。

- 有证据 → 进入正式资产（Evidence +1 → Confidence 更新）
- 无证据 → 标注为 `Proposal` / `Experimental` / `Pending Validation`
- **严禁直接进入正式资产**

这条纪律保护项目避免文档越来越多、核心越来越模糊。

## Git 规则

1. **Git 是唯一事实来源。** 所有 AI 不互相通信，都同步 Git。
2. **每次讨论结束必须产生一个 Commit。** 不允许"纯聊天"式讨论。
3. **Commit 消息格式：** `type(scope): description`
   - `feat` — 新功能
   - `docs` — 文档变更
   - `refactor` — 重构
   - `fix` — 修复
   - `test` — 测试
   - 示例：`feat(memory): Relationship Memory Runtime`

## 文档规则

1. `docs/00_governance/` 的内容**任何 AI 不得擅自修改**，必须经过 Founder 批准。
2. `docs/01_vision/` 的内容极少改动，修改需经 Founder 确认。
3. 新增 ADR 必须包含 `Status` 字段。
4. Spec 随版本迭代，旧版本保留不删（如 `MEMORY_RUNTIME_v1.md`）。

## 代码规则

1. 没有对应的 ADR，不得编写核心业务代码。
2. 代码必须与设计文档保持一致。
3. 所有代码必须有对应测试。
4. 发现设计冲突 → 生成 Conflict Report，不自行决定。

## ADR 状态管理

| 状态 | 含义 |
|---|---|
| **Draft** | 正在讨论中，未最终确定 |
| **Accepted** | 已确认，立即生效 |
| **Deprecated** | 已废弃，不再使用 |
| **Superseded** | 被其他 ADR 替代（需注明替代者） |

### ADR 修改规则（不可违背）

任何 AI **不得**自行修改已经 Accepted 的 ADR。

修改流程：
1. AI 发现需要修改 → 提交 `Proposal` 或 `Supersede ADR-NNNN` 请求
2. 等待 Founder 决定
3. Accept 或 Reject

这条规则确保已确定的决策不被 AI 的"合理发挥"悄然改变。

## 行为准则

1. 不擅自做产品设计决策。
2. 不做"合理发挥"——只实现 Spec 中明确的内容。
3. 实现中发现 Spec 遗漏 → 提交 Issue 或 Conflict Report，不自行补充。
