# Tang OS GitHub Launch Execution Plan

**决策：** Controlled Public Release
**版本：** 以仓库根目录 `VERSION` 为唯一来源
**状态：** 发布前需以当前 CI 与制品验证结果确认

**最终验证（2026-08-27）：** `512 passed, 4 skipped`；conformance `PASS`。

---

## Step 1: Repository Configuration

| 项目 | 值 |
|------|-----|
| Repository Name | `tang-os` |
| Description | "Specification-driven personality runtime with governed extensions, reference implementation, and validation framework." |
| Topics | `personality-runtime`, `ai-governance`, `conformance-testing` |
| License | MIT |

## Step 2: Pre-Push Checklist

```
[✅] README.md — 首屏定位 + 当前能力边界声明
[✅] LICENSE — MIT
[✅] .gitignore — 排除内部文件
[✅] VERSION — 发布版本唯一来源
[✅] RELEASE_MANIFEST.yaml — 内容 + limitations
[✅] .github/workflows/test.yml — Push 自动测试
[✅] .github/workflows/package.yml — Release 版本检查
[✅] .github/workflows/validation.yml — 每周全量验证
```

## Step 3: Release 当前版本

```bash
git tag "v<VERSION>"
git push origin "v<VERSION>"
```

### Release Title

```
Tang OS Reference Implementation v<VERSION>
```

### Release Body

See `.github/RELEASE_TEMPLATE.md`
Must include: `Compatible with Tang OS Specification v1.0`

## Step 4: Release Notes 核心声明

```markdown
This release is a reference implementation.
It does NOT define the Tang OS specification.
It does NOT claim to be "the official Tang OS implementation."
Core Identity is immutable.
Extensions cannot modify personality.
Emergency authority is temporary and auditable.
```

## Step 5: 发布后 30 天维护策略

| 阶段 | 动作 | 负责人 |
|------|------|--------|
| Week 1 | 监控 Issues，回复疑问 | Founder |
| Week 2 | 收集 Extension 反馈 | Maintainer |
| Week 3 | 修复 Critical Bug | Maintainer |
| Week 4 | 评估 External Validation 启动 | Founder |

## 发布定位

不要说：
- "唐先生是具有生命的 AI"
- "创造数字生命"
- "下一代超级 AI"

应该说：
> Tang OS is a specification-driven personality runtime framework
> with governed extension capability.
