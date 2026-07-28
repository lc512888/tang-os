# ADR-0001: xiaotang Project Scope

**日期：** 2026-07-28
**状态：** Accepted
**层级：** Application Layer（xiaotang Project Boundary）
**影响范围：** xiaotang 所有开发阶段

---

## 背景

Tang OS 已完成人格内核、LLM Provider 接口、验证框架的架构冻结。需要第一个应用层产品来验证"人格内核 → 用户陪伴体验"的完整闭环。

## 决策

### 一、项目定位

xiaotang 是 Tang OS 的**应用层验证产品**，不是 Tang OS 的修改层。

```
Tang OS  = 人格、认知、规则、边界、决策层
xiaotang = 应用层、交互层、用户体验层
```

### 二、架构边界

| 属于 xiaotang | 属于 Tang OS |
|--------------|-------------|
| UI / CLI / Web 界面 | 人格 Constitution |
| 会话历史管理 | Cognitive Framework |
| 用户输入预处理 | Emotion Detection |
| 显示逻辑 | Response Policy |
| 配置管理 | Invariant Engine |
| Provider 配置 | LLMProvider Interface |

### 三、禁止行为

- ❌ 修改 Tang OS Core
- ❌ 在 xiaotang 中复制人格逻辑
- ❌ 用 Prompt 模板替代 Tang OS 决策
- ❌ 绕过 Tang OS Decision Layer
- ❌ 在 UI 层做情绪判断

### 四、技术选型

| 层次 | 技术 | 原因 |
|------|------|------|
| 后端 | Python FastAPI | 与 Tang OS 同语言，快速验证 |
| LLM | DeepSeek（OpenAI 兼容） | 第一个真实 Provider |
| 界面 | CLI / 简单 Web | MVP 最小成本 |

### 五、MVP 范围

v0.1 仅实现：

1. 用户输入文字
2. 调用 Tang OS Core
3. 调用 LLM Provider
4. 返回唐先生回复
5. 无 API Key 降级模式（仅展示 Tang OS 决策）

不实现：用户账号、社交、记忆持久化、多角色、商业化功能。

---

## 原因

1. **边界清晰** — 避免 Tang OS Core 被应用层污染
2. **验证优先** — 核心问题是"用户能否感受到人格一致性"，不是"功能多丰富"
3. **低成本** — MVP 最小投入，验证后再扩展

## 后续依赖

- xiaotang v0.1 MVP 实现
- Tang OS Memory Runtime 接入（v0.3）
- Voice Provider 接入（v0.2）
