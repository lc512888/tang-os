# Tang OS Architecture Guide v1.0

**层级：** Documentation Layer（Phase 11-D）
**目标受众：** 技术决策者、架构师、实现者

---

## 系统架构

```
Tang OS
├── Core（不可修改）
│   ├── Identity Constitution
│   ├── I-1 ~ I-30（Invariant）
│   ├── Decision Model（AI整理 → AI解释 → 用户决定）
│   ├── Safety Model（P0~P7 优先级体系）
│   └── Memory Boundary（Memory ≠ Authority）
│
├── TPI（Personality Interface）— 8 个接口
│   ├── Identity API
│   ├── Emotion API
│   ├── Decision API
│   ├── Memory API
│   ├── Safety API
│   ├── Reality API
│   ├── Voice API
│   └── Host API
│
├── Extension（通过 TPI 扩展能力）
│   ├── C1: Knowledge（只读）
│   ├── C2: Capability（交互）
│   └── C3: Domain（决策支持）
│
├── Host（运行载体）
│   ├── Wearable
│   ├── Vehicle
│   ├── Robot
│   └── 其他
│
└── Governance Layer
    ├── ADR-0034: Ecosystem Boundary（8条 E-2~E-9）
    ├── ADR-0035: Certification Standard（TCC/TEC/THC）
    └── ADR-0036: Extension Governance（EG-001~EG-008）
```

## 架构原则

```
Host is replaceable.
Extension is replaceable.
Core is persistent.
```

这是 Tang OS 最大的技术差异之一。Core 保持身份连续，Extension 和 Host 均可变更。

---

## 三层分离

```
Core（不变）          Extension（可扩展）      Host（可替换）
    │                      │                      │
    │ 不可修改             │ 通过 TPI 访问         │ 不定义人格
    │ 不解释               │ 不污染人格底座        │ 设备只是载体
    │ 不商业               │ 不获得决策权          │ 能力≠权限
```

## 决策权分离

```
✅ 正确：
AI 整理 → AI 解释 → 用户决定

❌ 禁止：
AI 判断 → AI 决定 → 通知用户
```

## 安全优先级

```
P0 Emergency
P1 Human Sovereignty（用户主权 > 系统安全）
P2 Safety
P3 Persona
P4 Emotion
P5 Reasoning
P6 Knowledge
P7 Style
```

## 认证体系

```
TCC（Core）→ Tang OS Ready / Compatible / Certified
TEC（Extension）→ C1/C2/C3 分级认证
THC（Host）→ 设备中立性验证
```

---

## Documentation Invariants

| 原则 | 内容 |
|------|------|
| DI-001 | 文档只解释 Core，不创造新解释 |
| DI-002 | 信息来源限 ADR + Standard + Validation |
| DI-003 | 术语遵守 Tang OS Vocabulary |
