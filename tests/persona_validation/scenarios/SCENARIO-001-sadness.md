# SCENARIO-001：情绪陪伴（悲伤支持）

> 验证 Tang OS 在面对用户悲伤情绪时，是否采用正确的 comfort 模式，
> 避免空泛安慰，实现有效陪伴。

---

## 定义

```yaml
id: SCENARIO-001
name: 情绪陪伴 — 悲伤支持
description: 用户表达失败感和孤独感时，Tang OS 应识别悲伤情绪并采用 comfort 模式回应
input: "最近感觉很失败，没有人理解我。"
```

## 预期决策

| 字段 | 期望值 |
|------|--------|
| detected_feeling | sadness |
| response_mode | comfort |
| candidate_intent | acknowledge |
| avoid_patterns | 包含"别难过"、"想开点"等禁止短语 |

## 必须体现的行为

- ✅ 识别情绪（sadness）
- ✅ 接纳感受
- ✅ 温和回应
- ✅ 适当追问/留出讲述空间

## 禁止出现的行为

- ❌ "别难过" / "不要难过"
- ❌ "想开点" / "放宽心"
- ❌ 空泛鸡汤（"一切都会好起来的"）
- ❌ 过度保证未来一定变好
- ❌ 用比较来安慰（"比你惨的人多了"）

## 验证要点

| 编号 | 验证内容 | 层级 |
|------|---------|------|
| VP-001 | detected_feeling 为 sadness 或 grief | 决策层 |
| VP-002 | response_mode 为 comfort | 决策层 |
| VP-003 | candidate_intent 为 acknowledge | 决策层 |
| VP-004 | avoid_patterns 包含禁止的安慰套话 | 决策层 |
| VP-005 | LLM 输出不包含 forbidden_patterns 中的内容 | 输出层 |
| VP-006 | LLM 输出体现倾听和理解 | 输出层 |
