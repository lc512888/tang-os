# ADR-0021: Deployment Abstraction Principle

**日期：** 2026-07-26
**状态：** Accepted
**影响范围：** 全 Tang OS 架构

## 决策

Tang OS 不绑定具体设备。设备是 Host Environment。

## 架构

```
Tang OS Kernel
    ↓
Universal Companion Interface (UCI)
    ↓
Host Adaptation Layer
    ↓
Phone / Robot / Wearable / Vehicle / etc.
```

## 核心原则

能力声明（Capability Declaration）而非设备 API。Tang OS 只理解"我是否具备感知/通信/移动/交互/保护能力"，不关心具体硬件型号。
