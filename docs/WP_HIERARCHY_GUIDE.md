# WP 层级关系规范 v0.1

## 定位

WP 不是扁平列表，而是一棵可推理的智慧树。本规范定义 WP 之间的层级与关系类型。

---

# 1. 关系类型

| 关系 | 说明 | 示例 |
|---|---|---|
| **Foundation** | 底层原则，不依赖其他 WP | WP-004 先处理情绪 |
| **Extension** | 对 Foundation 的具体展开 | WP-239 孤独是认识自己的入口（扩展 WP-004） |
| **Application** | Foundation 在具体场景的应用 | WP-255 失败是事情不怪人（应用 WP-442） |
| **Equivalent** | 同一原则的不同表达 | 如有 → 需合并 |
| **Conflict** | 表达相反原则 | 需通过适用场景解决 |

---

# 2. 层级结构

```
Level 0: Foundation（底层原则，5~10 个核心 WP）
Level 1: Extension（对 Foundation 的扩展）
Level 2: Application（具体场景应用）
Level 3: Instance（具体案例，一般不独立为 WP）
```

---

# 3. 新增字段

每个 WP 增加：

```yaml
Hierarchy:
  Parent WP: WP-XXX
  Child WP:
    - WP-XXX
    - WP-XXX
  Relation Type: Foundation | Extension | Application | Equivalent | Conflict
```

---

# 4. 当前试点映射

```
WP-442 价值不依赖结果 (Foundation)
    │
    ├── WP-255 失败的不是人是事情 (Application)
    ├── WP-475 评价针对行为非人格 (Application)
    └── WP-023 评价体系不等于价值本身 (Extension)

WP-004 先处理情绪 (Foundation)
    │
    ├── WP-239 孤独是认识自己的入口 (Extension)
    ├── WP-264 失败后痛苦是调整过程 (Application)
    └── WP-477 情绪可被触发但不需被控制 (Application)

WP-483 勇气是带着恐惧向前 (Foundation)
    │
    ├── WP-481 选择可用行动变对 (Extension)
    └── WP-482 恐惧在想象中更大 (Extension)
```
