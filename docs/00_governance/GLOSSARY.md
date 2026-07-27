# GLOSSARY — 词汇表

> 统一项目术语，所有角色（AI 和人）使用同一套词汇。新增术语必须先更新本文档。

## 核心概念

| 术语 | 定义 | 英文 | 备注 |
|---|---|---|---|
| **角色** | 一个完整的数字人物，包含人格、记忆、形象 | Character | 项目交付的核心产品 |
| **人格** | 角色的性格、价值观、行为模式的总和 | Persona / Personality | 角色的"灵魂" |
| **角色宪法** | 角色行为的最高准则，不可轻易改变 | Character Constitution | 类比现实中的宪法 |
| **角色圣经** | 角色的完整定义文档，包含宪法+背景+成长 | Character Bible | 角色的"出生证明" |
| **记忆系统** | 管理角色记忆的基础设施 | Memory Runtime | 详见 `03_specs/memory/` |
| **关系** | 角色与用户之间的状态建模 | Relationship | 亲密度、信任度等 |
| **运行时** | 角色在交互中的执行环境 | Runtime | 人格的执行层 |
| **Provider** | 外部 AI 服务适配器（LLM/TTS/Image） | Provider | 可替换层 |
| **Design Session** | 一次正式的设计讨论，必须产出 Git 资产 | Design Session | 取代"聊天" |

## 禁用词

以下术语在项目中**禁止使用**，统一替换为规范术语：

| 禁用词 | 替换为 | 原因 |
|---|---|---|
| Agent | Character / Persona | Agent 太泛，不能体现角色感 |
| Bot | Character | Bot 暗示工具性 |
| 虚拟女友/男友 | 数字角色 / AI 角色 | 定位不是成人产品 |
| Prompt | Constitution / Persona Definition | Prompt 太技术化 |
| 聊天机器人 | 数字人物 / 角色 | 我们要塑造的是"人"不是"机" |
