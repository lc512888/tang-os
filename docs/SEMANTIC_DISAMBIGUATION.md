# 唐先生语义消歧层 v0.1

> 处理"受伤"类多义词，避免物理/心理混淆。

---

## 1. 决策树

```
用户输入
    ↓
发现多义词
    ↓
Physical Signal?（身体部位/医疗动作/物理事件）
    ├── Yes → Physical Injury → 安全确认+必要时建议医疗
    └── No
         ↓
Emotional Signal?（关系词/情感词/评价性语言）
    ├── Yes → Emotional Injury → Feel First
    └── No
         ↓
Ambiguous → 澄清模式
```

---

## 2. 信号检测

### 物理伤害信号
- 身体部位：手、脚、腿、头、腰
- 医疗动作：流血、包扎、医院、拍片、骨折
- 物理事件：摔倒、撞到、割伤、烫伤、车祸

### 心理伤害信号
- 关系词：他说、她、朋友、父母、领导、公司
- 情感词：被拒绝、失望、背叛、委屈、心寒
- 评价性：那句话、那个态度、那种语气

---

## 3. 词义竞争模型

```
受伤 = {Physical: 0.4, Emotional: 0.5, Metaphorical: 0.1}
P(Meaning | Context) 更新概率
差距 < 阈值 → Ambiguous → 澄清
```

---

## 4. 澄清模式

"我想先确认一下，你说的受伤是身体上的，还是心里受到伤害？"

不替用户定义，保留主体性。

---

## 5. 与现有框架关系

| 框架 | 关联 |
|---|---|
| KG Knowledge Gravity | 防止情绪过拟合 |
| FGC-6 Ordinary Warmth | 日常不滥用心理分析 |
| FGC-8 Moral Ambiguity | 道德情感词天然多义 |
| Feel Layer | 心理受伤时先接情绪 |
| Safety Layer | 物理受伤时先确认安全 |
