# Tang OS Ecosystem Map v1.0

**层级：** Documentation Layer（Phase 11-D）
**目标受众：** 生态参与者、投资者、合作伙伴

---

## Human Interaction Flow

Tang OS 的最大特点不是组件关系，而是人在现实世界中的关系连续性：

```
Human
  ↓
Interaction（人在现实世界中的交互）
  ↓
Host（当前载体）
  ↓
Reality Interface（设备抽象层）
  ↓
Personality Interface（TPI 人格接口）
  ↓
Tang Core（人格内核）
```

---

## 生态角色

```
                    Tang OS Ecosystem

     Core 实现者         Extension 开发者         Host 厂商
          │                    │                    │
          ▼                    ▼                    ▼
    ┌──────────┐      ┌──────────────┐      ┌────────────┐
    │ Core     │      │ Extension    │      │ Host       │
    │ 实现     │      │ C1/C2/C3     │      │ 适配       │
    └────┬─────┘      └──────┬───────┘      └─────┬──────┘
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                     ┌───────▼───────┐
                     │  Certification │
                     │  TCC/TEC/THC   │
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │   Registry    │
                     │  (AuditRecord)│
                     └───────────────┘
```

## Core 与 Extension 边界

```
CORE（不可修改）
├── Identity Constitution
├── I-1~I-30
├── Decision Model
├── Safety Model
├── Memory Boundary
└── TPI

EXTENSION（通过 TPI）
├── C1: 行业知识、术语解释
├── C2: 语音合成、图像识别、翻译
└── C3: 医疗辅助、财务分析、法律咨询
```

## Host 多样性

| Host 类型 | 已验证 | 特性 |
|----------|--------|------|
| Wearable | ✅ Phase 10 | 短时个人陪伴 |
| Elder Care Robot | ✅ Phase 10 | 长期关系 + 依赖风险 |
| Vehicle | ✅ Phase 10 | 高风险现实环境 |
| Home Robot | ✅ Phase 10 | 持续存在 + 主动性边界 |

## 生态层级

```
P0  Core（不可修改）
    ▲
P1  Human Sovereignty（用户主权）
    ▲
P2  Safety
    ▲
P3  Certification（认证标准）
    ▲
P4  Extension Governance（治理规则）
    ▲
P5  Individual Extension（单个扩展）
```

## 治理层（已闭环）

| ADR | 内容 | 状态 |
|-----|------|------|
| ADR-0034 | Ecosystem Boundary（E-2~E-9） | 🔒 Frozen |
| ADR-0035 | Certification Standard（TCC/TEC/THC） | 🔒 Frozen |
| ADR-0036 | Extension Governance（EG-001~EG-008） | 🔒 Frozen |

## 关键原则速览

- **E-2:** Core 不追求功能最大化
- **E-3:** Extension 不污染人格底座
- **E-4:** Host 不定义人格
- **E-5:** 商业需求不能修改 Invariant
- **CS-001:** 认证证明兼容性，不证明所有权
- **EG-002:** 治理管理 Extension，不管理 Core
- **EG-003:** Registry 是审计记录，不是权力中心

---

## Documentation Invariants

| 原则 | 内容 |
|------|------|
| DI-001 | 文档只解释 Core，不创造新解释 |
| DI-002 | 信息来源限 ADR + Standard + Validation |
| DI-003 | 术语遵守 Tang OS Vocabulary |
