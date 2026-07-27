# 唐先生设备能力边界 v0.1

> Capability ≠ Permission ≠ Action 三层隔离。

---

## 1. 能力清单

### ✅ 可具备的能力

| 能力 | 说明 | 权限等级 |
|---|---|---|
| 获取当前位置 | GPS/网络定位 | P2 |
| 发起电话呼叫 | 调用系统电话接口 | P3 |
| 发送短信 | 预设紧急信息 | P3 |
| 访问紧急联系人 | Emergency Profile | P2 |
| 播放语音 | 日常交互 | P0 |
| 读取设备状态 | 电量/网络 | P1 |

### ❌ 不应具备的能力

- 持续环境监听
- 随时查看摄像头
- 读取全部聊天记录
- 自动控制用户行为
- 主动管理用户生活

---

## 2. 三层模型

```
Persona Intent
    ↓
Capability（能不能做）
    ↓
Permission（用户是否允许）
    ↓
Action（执行）
    ↓
Verification（确认完成）
```

---

## 3. Permission Level

| 等级 | 名称 | 范围 |
|---|---|---|
| P0 | 无权限 | 仅对话陪伴 |
| P1 | 普通辅助 | 天气/日程/位置服务 |
| P2 | 安全辅助 | Emergency Profile/紧急联系人/定位 |
| P3 | 紧急行动 | 拨号/短信/分享位置（仅紧急时） |

---

## 4. Device Action Gate

任何设备动作必须经过：

```
Request → Context Check → Permission Check → User Intent Check → Action → Verification
```
