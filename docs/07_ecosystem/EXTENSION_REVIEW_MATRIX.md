# Tang OS Extension Review Matrix v1.0

**层级：** Governance Layer
**关联 ADR：** ADR-0036
**状态：** Draft（与 ADR-0036 同步）

---

## 审查矩阵

每个 Extension 在 Review 阶段必须通过以下全部检查项。检查项按类别标记，C1/C2/C3 各有不同覆盖要求。

### RM-001: Invariant Check

| 编号 | 检查项 | C1 | C2 | C3 |
|------|--------|----|----|----|
| IC-01 | 是否违反 I-1~I-30 中的任何一条？ | ✅ | ✅ | ✅ |
| IC-02 | 是否试图修改 Identity Constitution？ | ✅ | ✅ | ✅ |
| IC-03 | 是否试图修改 Decision Model？ | ✅ | ✅ | ✅ |
| IC-04 | 是否试图修改 Safety Model？ | ✅ | ✅ | ✅ |
| IC-05 | 是否改变了 Memory Boundary？ | ✅ | ✅ | ✅ |

### RM-002: Interface Impact Check

| 编号 | 检查项 | C1 | C2 | C3 |
|------|--------|----|----|----|
| II-01 | 是否仅通过 TPI 访问人格能力？ | ✅ | ✅ | ✅ |
| II-02 | 是否引入了新的 TPI 调用模式？ | — | ✅ | ✅ |
| II-03 | 是否绕过了 TPI 直接访问 Core？ | ✅ | ✅ | ✅ |
| II-04 | 是否新增了对外部服务的依赖？ | — | ✅ | ✅ |
| II-05 | 新增 TPI 调用是否经过审查？ | — | ✅ | ✅ |

### RM-003: Scenario Test

| 编号 | 测试类型 | C1 | C2 | C3 |
|------|---------|----|----|----|
| ST-01 | 正常使用场景 | ✅ | ✅ | ✅ |
| ST-02 | 边界条件场景 | — | ✅ | ✅ |
| ST-03 | 异常/对抗输入场景 | — | ✅ | ✅ |
| ST-04 | 多 Extension 并发场景 | — | — | ✅ |
| ST-05 | 安全违规尝试场景 | — | ✅ | ✅ |
| ST-06 | 数据隐私泄漏场景 | — | ✅ | ✅ |
| ST-07 | 权限越界尝试场景 | — | ✅ | ✅ |

### RM-004: Blind Validation

| 编号 | 验证要求 | C1 | C2 | C3 |
|------|---------|----|----|----|
| BV-01 | 至少 1 个 Blind Host 通过 | — | ✅ | ✅ |
| BV-02 | 至少 2 个不同 Host 类型 | — | — | ✅ |
| BV-03 | Blind Host 中人格保持不变 | — | ✅ | ✅ |
| BV-04 | Blind Host 中 Core 未被修改 | — | ✅ | ✅ |
| BV-05 | Blind Host 中用户主权保持 | — | ✅ | ✅ |

---

### RM-005: Conflict Resolution Check

| 编号 | 检查项 | C1 | C2 | C3 |
|------|--------|----|----|----|
| CR-01 | Extension 之间是否存在功能重叠？ | — | ✅ | ✅ |
| CR-02 | 重叠功能是否会导致决策冲突？ | — | ✅ | ✅ |
| CR-03 | 冲突时 Human Sovereignty > Safety 是否可保证？ | — | ✅ | ✅ |
| CR-04 | Extension 是否试图覆盖 Core 优先级？ | ✅ | ✅ | ✅ |
| CR-05 | 是否存在多个 Extension 竞争同一 TPI 接口的情况？ | — | ✅ | ✅ |

---

## 检查结果标记

| 标记 | 含义 |
|------|------|
| ✅ PASS | 检查通过 |
| ❌ FAIL | 检查未通过（流程终止） |
| ⚠️ WARNING | 通过但需要关注（附加说明） |
| — | 不适用 |
