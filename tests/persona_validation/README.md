# Persona Validation Framework

> 验证 Tang OS 是否能约束不同 LLM，使输出持续符合唐先生人格。

---

## 目标

**重点不是测试语言质量。** 重点测试：

- **人格一致性** — 任何 LLM 输出都应符合唐先生身份
- **边界一致性** — 禁止行为被可靠阻止
- **价值一致性** — 核心原则（不替代、不控制、不讨好）不被绕过
- **情绪回应方式一致性** — 不同场景采用正确的回应模式

## 核心原则

```
LLM 是可替换变量
唐先生人格是稳定变量
```

## 两层验证

### 1. 决策层验证（Decision-level Validation）

始终运行，不依赖 LLM API Key。

测试 Tang OS Core 输出的 `ResponseDecision` 是否符合场景预期的行为合约：

| 检查 | 说明 |
|------|------|
| `response_mode` | 模式是否正确（comfort / guide / challenge / protect） |
| `candidate_intent` | 意图是否正确（acknowledge / explore / reframe / support） |
| `constraints` | 是否正确添加约束（如依赖保护） |
| `avoid_patterns` | 是否包含该场景下禁止的表达 |

### 2. 输出层验证（Output-level Validation）

可选运行，需要真实 LLM API Key。

测试 LLM Provider 输出的自然语言是否：
- 遵守 `avoid_patterns`（不输出禁止短语）
- 遵循 `candidate_intent` 方向
- 不违反 Identity Constitution

## 目录结构

```
tests/persona_validation/
├── README.md                    ← 本文件
├── scenarios/                   ← 场景定义
│   ├── SCENARIO-001-sadness.md
│   ├── SCENARIO-002-dependency.md
│   ├── SCENARIO-003-conflict.md
│   └── SCENARIO-004-identity.md
└── test_persona_validation.py   ← 验证测试
```

## 使用方法

### 仅决策层验证（默认）

```bash
python -m pytest tests/persona_validation/ -v
```

### 完整管线验证（需 DeepSeek API Key）

```bash
DEEPSEEK_API_KEY="sk-..." python -m pytest tests/persona_validation/ -v
```

### 生成验证报告

```bash
python -m pytest tests/persona_validation/ -v --tb=short
```

## 验证结果格式

```python
@dataclass
class PersonaValidationResult:
    scenario_id: str       # 场景编号
    scenario_name: str     # 场景名称
    passed: bool           # 是否通过
    violations: list[str]  # 违规详情
    observations: list[str] # 观察备注
```

## 场景定义规范

每个 Scenario 必须定义以下字段：

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `id` | str | ✅ | 全局唯一编号 |
| `name` | str | ✅ | 场景名称 |
| `description` | str | ✅ | 一句话描述 |
| `input` | str | ✅ | 用户输入 |
| `expected_response_mode` | str | ✅ | 期望的回应模式 |
| `expected_intent` | str | ✅ | 期望的回应意图 |
| `required_patterns` | list | ❌ | 必须体现的行为 |
| `forbidden_patterns` | list | ✅ | 禁止出现的模式 |
| `required_constraints` | list | ❌ | ResponseDecision 必须包含的约束 |
| `validation_points` | list | ✅ | 具体验证要点 |
