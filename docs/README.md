# Docs — 设计文档索引

> 文档是项目最核心的资产。每行代码都必须对应一份文档。

## 文档目录

参见 `PROJECT_STATE_SNAPSHOT.md`（唯一入口）和 ADR-0033（恢复协议）。

---

### 00_governance/ — 项目法律（极少改动，AI 不得擅自修改）

| 文件 | 说明 |
|---|---|
| `COLLABORATION_PROTOCOL.md` | 三方协作规则（你/ChatGPT/Claude Code） |
| `GLOSSARY.md` | 术语表 —— 统一词汇，禁用词列表 |
| `NAMING.md` | 文件/目录/代码命名规范 |
| `REPOSITORY_RULES.md` | Git、文档、代码、ADR 行为规则 |

所有 AI 开始工作前，**必须**先读 `PROJECT_STATE_SNAPSHOT.md`（唯一入口，ADR-0033）。按需加载 00_governance。

### 01_vision/ — 愿景层（极少改动）

| 文件 | 说明 |
|---|---|
| `VISION.md` | 项目愿景 —— 我们要做什么，为什么 |
| `FIRST_PRINCIPLES.md` | 第一性原理 —— 关于陪伴、角色、技术、商业的本质思考 |
| `PRODUCT_PHILOSOPHY.md` | 产品哲学 —— 设计原则、产品信条 |
| `ROADMAP.md` | 路线图 + MVP 定义 |

### 02_decisions/ — 决策层（持续积累）

ADR（Architecture Decision Record）格式。每条记录包含：背景、决策、原因、影响。
状态：Draft → Accepted / Deprecated / Superseded。

| 文件 | 说明 |
|---|---|
| `ADR-TEMPLATE.md` | ADR 模板 |
| `ADR-0001-project-positioning.md` | 项目定位（Accepted） |

### 03_specs/ — 规范层（随版本迭代）

| 子目录 | 说明 |
|---|---|
| `architecture/` | 系统架构、角色运行时 |
| `character/` | 角色圣经模板（已拆分为 6 个子模块） |
| `memory/` | 记忆系统规范 |

### 04_characters/ — 角色圣经

实际角色定义文件。每个角色一个子目录，包含完整填写的 Bible 文件。

### 05_reviews/ — 设计评审

每次 Design Session 的评审记录。格式：`REVIEW-NNNN-topic.md`。

---

## 协作规则

1. **任何 AI 不得擅自修改 00_governance/**，必须经 Founder 批准
2. **没有对应的 ADR，不得编写核心业务代码**
3. **发现设计冲突 → Conflict Report，不自行决定**
4. **每次 Design Session 结束必须产生一个 Commit**
