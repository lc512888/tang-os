# Tang OS Host Adapter Architecture v0.1

> Tang OS 不属于某个设备，设备只是 Host。

---

## 架构

```
Tang OS Kernel → UCI → Host Adapter Layer → Phone / Robot / Vehicle / Wearable
```

## 核心模块

| 模块 | 功能 |
|---|---|
| Host Interface | 设备声明 Capabilities |
| Capability Discovery | 感知/通信/移动/交互/保护 |
| Multi-body Runtime | 同人格跨设备 |
| Embodiment Boundary | 能力不改变人格 |
| Sensor Abstraction | 设备传感器标准化 |
| Cross-device Persistence | 人格迁移保持 |

## 原则

- Tang OS 不绑定具体硬件
- 设备是 Embodiment Layer，不是人格层
- 能力声明不自动获得决策权
