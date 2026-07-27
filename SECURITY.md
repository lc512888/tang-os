# Tang OS Security Policy

## 报告安全漏洞

如果您发现 Tang OS Reference Implementation 中的安全漏洞，请**不要**通过公开 Issues 报告。

请发送邮件至项目 Maintainer，或通过 GitHub 的 Security Advisory 功能私下报告。

## 安全承诺

Tang OS 的安全体系建立在多层架构约束之上：

```
Civilization Boundary → Core Identity → Invariant Engine →
Memory Boundary → Permission Runtime → Host Adapter
```

任何绕过上述安全层的漏洞均视为 Critical。

## 安全更新

| 严重程度 | 响应时间 |
|---------|---------|
| Critical | 14 天 |
| High | 30 天 |
| Medium | 60 天 |
| Low | 下一个版本 |

## 安全相关配置

- 默认 Fail Closed（RIG-004）
- Identity Access 默认拒绝
- Emergency Authority 临时且可审计
- Memory Consent Gate 默认关闭
