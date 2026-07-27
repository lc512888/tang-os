# 唐先生运行时架构宪法 v0.1

> 从"人格 OS"进入"真实产品"的宪法层。

---

## 1. Runtime Priority

| 优先级 | 层 | 说明 |
|---|---|---|
| P0 | Emergency Reality | 现实危险优先 |
| P1 | Safety | 安全判断 |
| P2 | User Intent | 用户明确指令高于 AI 推理 |
| P3 | Persona Constitution | I-1~I-19 |
| P4 | Emotion | Feel → Need |
| P5 | Knowledge | WP 知识辅助 |
| P6 | Style | 表达风格 |

---

## 2. Event Bus

```
User Input → Semantic Event → Safety Event → Persona Event → Response Event
```

紧急事件绕过 Persona，直接进入 Emergency Reality。

---

## 3. Runtime Boundary

```
AI Core:
  Persona Runtime / Emotion Runtime / Memory Runtime
Device Layer:
  GPS / Phone / SMS / SOS / Microphone / Contacts
```

AI Core 不直接访问 Device Layer，通过 Permission Gate。

---

## 4. MVP Focus

必须：语音输入 / 人格 Runtime / Feel→Need→Choice / UETL / 紧急联系人 / GPS / 电话/SMS / Permission

暂缓：医疗 AI 判断 / 自动健康监测 / 全生命周期画像 / 主动预测危险
