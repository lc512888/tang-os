# NAMING — 命名规范

> 所有代码、文件、目录的命名规则。所有 AI 和人必须遵守。

## 目录命名

- 顶级 docs 目录：`NN_name`（数字排序前缀 + 下划线 + 英文小写）
- 其余目录：`kebab-case`（短横线连接，全小写）

## 文件命名

- 设计文档：`UPPER_SNAKE_CASE.md`（如 `COLLABORATION_PROTOCOL.md`）
- ADR 文件：`ADR-NNNN-name-with-dashes.md`
- Spec 文件：`UPPER_SNAKE_CASE.md`
- 代码文件：遵循各语言的社区规范（Python: snake_case, TypeScript: camelCase）

## ADR 编号

- 格式：`ADR-NNNN`（4 位数字，从 0001 开始）
- 状态：Draft → Accepted / Deprecated / Superseded

## 代码中的命名

- 类名：`PascalCase`
- 函数/方法：`snake_case`（Python）/ `camelCase`（TypeScript）
- 常量：`UPPER_SNAKE_CASE`
- 模块/包：`snake_case`

## 术语一致性

代码中的命名必须与 `GLOSSARY.md` 保持一致。例如：
- 角色相关类用 `Character`，不用 `Agent`、`Persona`、`Identity`
- 人格相关用 `Persona`，不用 `Profile`、`CharacterTrait`
- 记忆相关用 `Memory`，不用 `History`、`Context`
