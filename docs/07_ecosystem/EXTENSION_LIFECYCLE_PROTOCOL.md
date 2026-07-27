# Tang OS Extension Lifecycle Protocol v1.0

**层级：** Governance Layer
**关联 ADR：** ADR-0036
**状态：** Draft（与 ADR-0036 同步）

---

## 生命周期总览

```
Proposal → Sandbox → Review → Validate → Certified → Registry → Active → Deprecated → Removed
```

## 各阶段操作协议

### 1. Proposal

**提交者：** Extension 开发者
**提交内容：** 名称、用途、分类（C1/C2/C3）、涉及 TPI、预期影响、风险预评估
**接受标准：** 不与现有 Extension 冲突，不违反 ADR-0034 E-2~E-9

### 2. Sandbox

**访问限制：** 仅开发者和授权测试者
**标识限制：** 不得公开标榜"Tang OS Extension"
**最长期限：** 6 个月

### 3. Review

**审查矩阵：** 详见 EXTENSION_REVIEW_MATRIX.md
**审查内容：** Invariant Check / Interface Impact / Scenario Test（≥3 场景）

### 4. Validate

**C1：** 无需 Blind Validation
**C2：** ≥1 Blind Host
**C3：** ≥2 Blind Host，且为不同 Host 类型

### 5. Certified

**执行部门：** 认证机构（TEC）
**产出：** Tang OS Certified Extension 标识 + 认证报告

### 6. Registry

**注册表记录：** 名称、唯一 ID、版本、认证级别、分类、维护者、Core 版本兼容范围、安全审计记录

### 7. Active

**监控周期：** 季度合规抽查
**安全响应：** Critical 14 天 / High 30 天
**续期：** 年度

### 8. Deprecated

**废弃期：** 12 个月
**标记：** 注册表标记"不再推荐"
**替代推荐：** 必须注明替代 Extension（如有）

### 9. Removed

**触发条件：** 废弃期满 / 安全漏洞未修复超期 / 恶意行为
**记录保留：** 注册表保留移除记录和原因

---

## 冲突解决快速参考

当多个 Extension 冲突时：

| 优先级 | 主体 | 说明 |
|--------|------|------|
| P0 | Core | 不可协商 |
| P1 | Human Sovereignty | 用户决定 > 系统判断 |
| P2 | Safety | 安全机制 |
| P3 | Certification | 认证标准 > 治理流程 |
| P4 | Extension Governance | 治理规则 |
| P5 | Individual Extension | 单个 Extension 优先级最低 |
