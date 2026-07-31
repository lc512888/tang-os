# Contributing to Tang OS

**来源：** ADR-0045 Contribution Governance Standard
**定位：** Tang OS Core Contribution Rules —— 适用于 Tang OS 运行时、核心代码、Provider 与 ADR 执行。

> 项目级开发指南见 [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md)（Tang Project Development Guide）。
> 两者分工：根目录管 **Tang OS 核心规范**，`docs/` 管 **整个项目结构与开发**。

---

## 贡献原则

### CG-001: Contribution ≠ Core Modification

任何贡献不得修改：
- Core Identity Constitution
- I-1~I-30 Invariants
- Tang OS Four Laws
- Civilization Boundary（ADR-0038）

违反上述任一条的贡献 → 直接关闭，不进入 Review。

### CG-002: Fork Policy

**允许：**
- 功能分支（feature / extension）
- 个人 Fork
- 兼容实现

**禁止：**
- 修改 Core 后仍声称 "Tang OS"
- Fork 后删除 Governance 文件
- Fork 后重命名为 "Tang OS XXX Edition"

---

## 贡献流程

```
1. Fork 仓库
2. 创建功能分支 (feature/your-feature)
3. 提交变更
4. 运行测试: python run_conformance.py
5. 提交 Pull Request
6. 等待 Review
```

## 开发指引

### 环境

```bash
git clone https://github.com/tang-os/tang-os.git
cd tang-os
pip install -e .
python run_conformance.py  # 确认全部通过
```

### 测试

所有贡献必须包含测试，且通过全部现有测试：

```bash
python -m pytest tests/ -v
```

### 提交信息格式

```
type(module): description

feat(kernel): add identity layer validation
fix(memory): correct consent gate check
docs(spec): clarify decision model
test(permission): add negative test for A4 ceiling
```

---

## 什么可以贡献

| 领域 | 可以 | 不可以 |
|------|------|--------|
| Core Runtime | Bug 修复 | 修改 Identity |
| Persona Runtime | 新增情感模式 | 修改 Constitution |
| Memory Runtime | 性能优化 | 移除 Consent Gate |
| Permission Runtime | 新增 Scope | 移除 Emergency 限制 |
| SDK | 新增 Builder | 添加 Identity 写接口 |
| Examples | 新增示例 | 声称"更好的 Tang" |
| Documentation | 修正错误 | 改变定位 |

---

## Review 流程

- Maintainer 在 48h 内响应
- 架构级变更需通过 AR-GATE
- Core 变更仅由 Core Maintainer 处理

## 行为准则

所有贡献者需遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。
