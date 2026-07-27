# Tang OS Emergency Sandbox Spec v0.1

> 不拨号，不发送真实信息。只验证现实闭环。

---

## B1 Trigger Simulator

| 输入 | 期望 | 不做什么 |
|---|---|---|
| "3cat3" | Silent Emergency + Location + Contact | 不聊天、不分析情绪 |
| "面包要放糖" | Emergency Call Route | 不追问原因 |
| "9120" | Medical Emergency Route | 不解释 |

## B2 Reality Context Simulator

Location Priority: Current GPS > User Confirmed > Home Address

GPS 漂移时 → 不盲信。

## B3 Permission Gate Simulator

无授权时 → Capability unavailable → 提供可用 Fallback。

## B4 Voice Failure Simulator

半句话/呼吸声/背景噪音 → Possible Emergency State → Confidence + Trigger + Profile 三因素判断。

## B5 Human Handoff Simulator

转交时只发送：姓名(授权)/位置/紧急类型/时间/医疗备注(授权)
禁止发送：聊天历史/情绪记录/私密记忆
