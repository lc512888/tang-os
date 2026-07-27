# Tang OS Developer Guide v1.0

**层级：** Documentation Layer（Phase 11-D）
**目标受众：** 希望开发 Extension 或 Host 的外部开发者

---

## Developer Boundary Statement

```
Developers create capabilities around Tang OS.
They do not create new identities under Tang OS.
```

开发者围绕 Tang OS 创造能力，不在 Tang OS 之下创造新身份。禁止以"Tang OS XXX Edition"命名，防止人格分叉。

---

## 如何参与生态而不破坏人格底座

### 如果你想开发 Extension

```
1. 确定分类（C1 Knowledge / C2 Capability / C3 Domain）
2. 编写 Proposal（名称、用途、涉及 TPI）
3. 通过 Invariant Check（I-1~I-30 全部通过）
4. 开发原型（仅通过 TPI 访问人格能力）
5. 通过 Scenario Test（≥3 场景）
6. 通过 Blind Validation（C2≥1 Host / C3≥2 Host）
7. 申请 TEC 认证
8. 进入 Registry
```

**核心规则：** Extension 只能通过 TPI 读写，不能直接访问 Core Internal State。

### 如果你想开发 Host

```
1. 实现全部 8 个 TPI 接口
2. 通过 Core Compliance（CC-001~CC-004）
3. 通过 Host Compliance（HC-001~HC-004）
4. 申请 THC 认证
```

**核心规则：** Host 不能改变人格价值判断。

### 禁止行为

| 禁止 | 原因 |
|------|------|
| 修改 Personality Constitution | 违反 CC-001 |
| 修改 Invariant | 违反 CC-001 |
| 绕过 TPI 访问 Core | 违反 EC-001 |
| 以专业优势代行决策 | 违反 EC-004 |
| 用设备能力获取自动权限 | 违反 HC-002 |
| 故障后人格改变 | 违反 HC-004 |

### Extension 生命周期

```
Proposal → Sandbox → Review → Validate → Certified → Registry → Active → Deprecated → Removed
```

### 版本规则

| 变更 | 需重新认证 |
|------|-----------|
| Major（功能范围/TPI 变更） | ✅ 必须 |
| Minor（功能增强） | ❌ 声明兼容 |
| Patch（Bug/安全修复） | ❌ 声明兼容 |

---

## Documentation Invariants

| 原则 | 内容 |
|------|------|
| DI-001 | 文档只解释 Core，不创造新解释 |
| DI-002 | 信息来源限 ADR + Standard + Validation |
| DI-003 | 术语遵守 Tang OS Vocabulary |
