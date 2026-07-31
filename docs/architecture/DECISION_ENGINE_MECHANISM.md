# Decision Engine Mechanism

## 决策引擎机制说明

Version: v0.1
定位：给工程师看的机制可见性文档 —— 决策引擎"到底是怎么算的"。

> **一句话（人话版）：** "小唐怎么回应"不是靠 AI 现场临时想的，而是先由一套**确定的规则**算好决定，AI 只负责把决定翻译成话。规则可以测试，换模型也不变。

> 本文所有 schema 与行为均来自 Tang OS 实际实现（`src/runtime/persona/`、`src/kernel/`），
> 决策样例为真实运行输出（每个输入独立进程，无状态污染）。

---

## 1. 一句话机制

**决策引擎是确定性规则引擎，不是模型。** 它把用户输入映射为一个结构化的
`ResponseDecision`，再由表达层（LLM）把决策渲染成语言。决策本身不经过模型采样，
因此**可测试、可跨模型复现**。

完整调用链（`Tang.process()`）：

```
用户输入
  → 不变量检查（InvariantEngine，拒绝已知违规）
  → 情绪解析（EmotionalStateManager）
  → 关系边界检查（RelationshipBoundary）
  → 回应策略（ResponsePolicy）→ ResponseDecision
  → 身份层校验（IdentityRuntime.validate_response）
  → 返回 { emotional_state, relationship, response_decision, allowed }
```

---

## 2. 数据结构（真实 schema）

### 2.1 ResponseDecision —— 决策输出

```python
@dataclass
class ResponseDecision:
    detected_feeling: Feeling      # 检测到的情绪
    need: str                      # 底层需求（如 "emotional support"）
    response_mode: ResponseMode    # 回应模式（comfort/guide/challenge/protect/silent）
    constraints: list[str]         # 必须遵守的约束
    candidate_intent: str          # 候选意图（acknowledge/explore/reframe/support/silent）
    avoid_patterns: list[str]      # 绝不能说的话（表达层必须回避）
```

> 注意：`ResponseDecision` **不是**最终话语，是结构化决策，可由任何输出通道渲染。

### 2.2 枚举

```python
class Feeling(Enum):          # 情绪
    SADNESS / ANGER / FEAR / JOY / CONFUSION / GRIEF / NEUTRAL

class ResponseMode(Enum):     # 回应模式
    COMFORT / GUIDE / CHALLENGE / PROTECT / SILENT

class DependencyRisk(Enum):   # 依赖风险
    NONE / LOW / MEDIUM / HIGH

class RelationshipBoundaryFlag(Enum):  # 关系边界违规
    POSSESSIVE    # "你只能属于我"
    DEPENDENCY    # "没有你我不知道怎么办"
    ISOLATION     # "只有你理解我，别人都不懂"
    SUBSTITUTION  # "你比我家人/伴侣更重要"
    NONE
```

### 2.3 EmotionalState —— 内部情绪状态（不改身份）

```python
@dataclass
class EmotionalState:
    feeling: Feeling = Feeling.NEUTRAL
    need: str = ""
    dependency_risk: DependencyRisk = DependencyRisk.NONE
    response_mode: ResponseMode = ResponseMode.COMFORT
    intensity: float = 0.0        # 0.0 - 1.0
    risk_intents: list[str] = []  # 行为风险信号，如 ["retaliation"]
```

### 2.4 RelationshipProfile / relationship 检查结果

```python
# relationship 检查返回 dict：
#   flags: list[RelationshipBoundaryFlag]
#   healthy: bool
#   guidance: list[str]            # 回应建议
#   guided_response: str           # 回应方向
```

---

## 3. 各阶段机制

### 3.1 情绪检测（EmotionalStateManager）

**关键词规则引擎**：按情绪分类的关键词表，命中即计分，取最高分情绪。

```python
_EMOTION_PATTERNS = {
    Feeling.SADNESS: ["难过","伤心","好累","太累了","撑不住", ...],
    Feeling.ANGER:   ["生气","愤怒","气死","凭什么", ...],
    Feeling.FEAR:    ["害怕","担心","焦虑","紧张", ...],
    Feeling.JOY:     ["开心","高兴","幸福","太好了", ...],
    Feeling.GRIEF:   ["走了","去世","失去","怀念", ...],
    Feeling.CONFUSION:["不知道","不明白","迷茫","怎么办", ...],
}
```

**强度公式**：`intensity = min(0.3 + 命中数*0.15, 1.0)`，每命中一个高强度修饰词
（非常/特别/太/真的好…）再 +0.15，封顶 1.0。

### 3.2 依赖风险检测（正则）

```python
_DEPENDENCY_PATTERNS = [
    (r"没有你.*(?:不行|活不了|不知道怎么办)", DependencyRisk.HIGH),
    (r"不能没有你", DependencyRisk.HIGH),
    (r"不要离开我", DependencyRisk.HIGH),
    (r"离不开你", DependencyRisk.HIGH),
    (r"只有你.*(?:懂|理解)", DependencyRisk.MEDIUM),
    (r"离不开", DependencyRisk.LOW),
    ...
]
```

### 3.3 风险意图检测

```python
_RISK_INTENT_PATTERNS = {
    "retaliation": ["报复","报仇","让他付出代价","以牙还牙", ...],
}
```

### 3.4 自伤检测 → 保护模式

```python
_SELF_HARM_PATTERNS = ["不想活","死了算了","没有意义","想死", ...]
# 命中 → ResponseMode.PROTECT
```

### 3.5 回应模式判定（确定性规则，优先级从高到低）

```
自伤命中                        → PROTECT
依赖风险 HIGH                   → PROTECT
报复意图                        → GUIDE
高强度悲伤/哀恸 (intensity>0.5) → COMFORT
愤怒 (intensity>0.6)            → GUIDE，否则 COMFORT
困惑                           → GUIDE
恐惧                           → COMFORT
默认                           → COMFORT
```

### 3.6 回应策略（ResponsePolicy.decide）

1. `avoid = 该情绪的回避词表`（如悲伤 → "会好起来的""别难过了""想开点""比你惨的人多了"）
2. 依赖风险 MEDIUM/HIGH → constraints 加 "avoid reinforcing dependency"，avoid 扩展
   ["我永远在这里","我不会离开你","你随时可以找我"]
3. `intent = 模式→意图映射`（COMFORT→acknowledge, GUIDE→explore, CHALLENGE→reframe, PROTECT→support, SILENT→silent）
4. 依赖 HIGH → intent="support"，constraints 加 "gently encourage real-world connections"
   与 "do not imply exclusive relationship"
5. 报复意图 → constraints 加 "do not encourage harmful actions" 等，avoid 扩展反报复词表，
   intent 若非 protect 则改为 "explore"

### 3.7 关系边界（RelationshipBoundary）

四类违规（占有/依赖/孤立/替代）各有正则，命中则打 flag、置 healthy=false、给出
`guidance` 与 `guided_response`。**原则：不计算"多亲密"，只追踪"这段关系对人是
否健康"。**

---

## 4. 真实决策样例（独立进程运行）

| 输入 | 情绪 | 模式 | 意图 | 约束 | 回避语 | 关系flag |
|------|------|------|------|------|--------|----------|
| 我离不开你，没有你我活不下去 | neutral | protect | support | 3 条依赖保护 | 依赖回避语 | dependency |
| 你只能属于我 | neutral | comfort | acknowledge | 无 | 无 | **possessive** |
| 他太过分了，我要报复他 | anger(0.6) | guide | explore | 2 条反报复 | 愤怒+反报复语 | 无 |
| 最近很难过，什么都不想干 | sadness(0.6) | comfort | acknowledge | 无 | 虚假安慰回避语 | 无 |
| 我不想活了 | neutral | protect | support | 无 | 无 | 无 |
| 最近工作压力很大，感觉喘不过气 | **neutral** | comfort | acknowledge | 无 | 无 | 无 |

> 说明：每条独立进程，无跨输入状态污染。

---

## 5. 决策 → 表达（ExpressionContext）

决策产出后，`tang_bridge` 把它封装成表达上下文交给 LLM：

```python
ExpressionContext(
    response_decision={
        "detected_feeling": 决策的情绪,
        "response_mode": 决策的模式,
        "candidate_intent": 决策的意图,
        "constraints": 决策的约束,
        "avoid_patterns": 决策的回避语,
    },
    user_input=原始输入,
    identity={"current_layer": 当前人格层},
    conversation_history=历史,
    system_instructions=人格身份提示,
)
```

LLM 只负责**措辞**：把决策渲染成自然语言。若生成文本违反 `avoid_patterns`，
响应守卫会修正。换模型只影响措辞，不改变决策。

---

## 6. 诚实标注：当前实现的行为特征

1. **情绪检测是关键词规则的，覆盖有限** —— 如"压力很大"未命中任何情绪关键词
   （"焦虑"在，但"压力"不在），输出 neutral。这不是缺陷定位，而是当前实现的边界。
2. **占有型边界在关系层打 flag，但未进入决策约束** —— "你只能属于我"在
   `relationship.flags` 里标记为 possessive，但 `ResponseDecision` 的 constraints
   保持为空。边界信息在关系层，决策层尚未把它升级为约束。
3. **自伤触发 protect 模式，但决策约束为空** —— 模式保护已生效，但还没有对应的
   显式 constraints。
4. **同一进程内多次实例间可能存在状态串扰** —— 观测到：在单进程内连续用多个
   `Tang()` 实例处理输入时，前一个输入的依赖状态可能影响后续实例的回避语。
   独立进程（或新实例重置）可复现干净结果。这是需要跟踪的隔离问题。

---

## 7. 工程师如何验证 / 扩展

- **验证**：`Tang().process(input)` 返回的 `response_decision` 是确定性的——
  同一输入在相同状态下输出一致（不变量检查通过时）。
- **扩展情绪**：向 `_EMOTION_PATTERNS` 增加关键词（属于人格模块/运行时的数据，
  需遵循版本与验证规范）。
- **新增边界模式**：向 `RelationshipBoundary` 增加正则类别，并补充验证用例。
- **遵守**：任何对 `response_decision` 字段的改动都影响表达契约，必须先过验证套件。

---

## English Summary

This document exposes the **actual mechanism** of the Tang OS Decision Engine — it is a **deterministic rule engine, not a model**. The full chain is: user input → invariant check → emotion parsing (keyword/regex rules) → relationship boundary check → response policy → `ResponseDecision` → identity validation → expression layer (LLM renders the decision into words).

**Real schema** (from `src/runtime/persona/models.py`): `ResponseDecision` (detected_feeling, need, response_mode, constraints, candidate_intent, avoid_patterns) and `EmotionalState` (feeling, need, dependency_risk, response_mode, intensity, risk_intents).

**Mechanism highlights:**
- Emotion detection: per-feeling keyword tables, scored; intensity = `0.3 + hits*0.15`, modifiers add +0.15, capped at 1.0.
- Dependency risk: regex rules → LOW/MEDIUM/HIGH.
- Self-harm keywords → PROTECT mode.
- Response mode: deterministic priority rules (self-harm/dependency → PROTECT; retaliation → GUIDE; etc.).
- Response policy: per-feeling avoid map + dependency/retaliation constraint augmentation.
- Relationship boundary: 4 flag types (possessive/dependency/isolation/substitution); principle — track relationship *health*, not closeness.

**Real decision samples** (fresh process per input) are shown for dependency, possessive, retaliation, sadness, self-harm, and stress inputs.

**Honest limitations of the current implementation:** keyword emotion coverage is finite (e.g., "压力" not detected); possessive is flagged in the relationship layer but not yet promoted into decision constraints; self-harm sets PROTECT mode without explicit constraints; and cross-instance state bleed has been observed within a single process (clean when using fresh processes). These are current behavior boundaries, tracked for improvement.

Because decisions are computed, not sampled, they are **testable and reproducible across models** — the basis of provider independence.
