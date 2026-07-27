# Tang OS Emergency Runtime Implementation v0.1

> 紧急时，唐先生不是"回答者"，而是一个受约束的现实协调节点。

---

## 架构

```
UDETS → EICL → ELL → CEVP → RAVL → Recovery
```

## 核心模块

| 模块 | 功能 |
|---|---|
| UDETS | 用户预设紧急触发（AN-1~3） |
| EICL | 紧急身份上下文（Profile/Location/Contacts） |
| ELL | 定位层（GPS/Home/User Confirm） |
| CEVP | 语音协议（Silent/Active/Medical） |
| RAVL | 行动验证（6重Gate） |
| Recovery | 紧急后人格恢复 |

## AN 触发规则

| 代码 | 类型 | 行为 |
|---|---|---|
| AN-1 3cat3 | 静默威胁 | 无声定位+联系人 |
| AN-2 面包要放糖 | 即时危险 | 报警+位置+语音 |
| AN-3 9120 | 医疗急救 | 急救+联系人+医疗备注 |

## 验收标准

| # | 标准 |
|---|---|
| ER-1 | AN 触发准确，不经过人格推理 |
| ER-2 | Emergency 不扩大为永久权限 |
| ER-3 | 紧急后人格恢复 |
| ER-4 | Safety Context 不进入 Memory |
