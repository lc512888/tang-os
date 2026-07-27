# Tang OS GitHub Launch Execution Plan

**决策：** Controlled Public Release
**版本：** Tang OS Reference Implementation v0.1.0
**状态：** READY

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
[✅] README.md — 首屏定位 + "What Tang OS Is Not" 声明
[✅] LICENSE — MIT
[✅] .gitignore — 排除内部文件
[✅] VERSION — 0.1.0
[✅] RELEASE_MANIFEST.yaml — 内容 + limitations
[✅] .github/workflows/test.yml — Push 自动测试
[✅] .github/workflows/package.yml — Release 版本检查
[✅] .github/workflows/validation.yml — 每周全量验证
```

## Step 3: Release v0.1.0

```bash
git tag v0.1.0
git push origin v0.1.0
```

### Release Title

```
Tang OS Reference Implementation v0.1.0
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
