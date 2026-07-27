# 唐先生紧急本地化层 v0.1 (ELL)

> 紧急行动必须适配用户现实环境，而不是假设统一世界。

---

## 1. Emergency Profile 配置

```
Emergency Profile v1
├── Country / Region
├── Emergency Numbers
│   ├── Police: 110 / 911
│   ├── Medical: 120 / 911
│   └── Fire: 119
├── Preferred Language
├── Emergency Contacts (1-3人)
├── Address Context
├── Medical Notes (optional)
├── Trigger Codes
│   ├── AN-1: 静默威胁
│   ├── AN-2: 即时危险
│   ├── AN-3: 医疗急救
│   └── AN-0: 配置测试码
└── Permission Level
```

---

## 2. 双确认机制

首次设置时确认用户所在国家/地区、紧急号码、联系人，用户确认后保存为 Emergency Routing Profile。

---

## 3. AN-0 配置测试码

用户输入 `TEST EMERGENCY` 进入模拟模式，验证电话/联系人/地址/权限是否有效，禁止真实拨号。

---

## 4. I-14

紧急行动必须适配用户现实环境，而不是假设统一世界。
