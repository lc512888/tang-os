# Tang OS

**Personality Runtime Infrastructure**

Tang OS is a specification-driven personality runtime framework
designed to preserve identity consistency, ethical boundaries, and
capability governance across different AI hosts and extensions.

[![Tests](https://img.shields.io/badge/tests-280%20passing-brightgreen)]()
[![Spec](https://img.shields.io/badge/spec-v1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## What Tang OS Is

Tang OS defines:

- **Identity Boundary** — Three-layer identity constitution (Companion → Wise → Listener), immutable
- **Personality Interface** — 8 standard TPI APIs for consistent interaction
- **Capability Governance** — Civilization Boundary + Ethical Gate + Necessity Gate
- **Extension Contract** — Manifest v2 with `identity_access: false` enforced
- **Host Compatibility** — Cross-host personality consistency (Mobile/Robot/Vehicle)
- **Validation Framework** — Blind Validation Protocol + Conformance Harness

## What Tang OS Is Not

- ❌ Not a replacement for human relationships
- ❌ Not an autonomous authority system
- ❌ Not an unrestricted agent framework
- ❌ Not a definition of artificial consciousness
- ❌ Not an AI chatbot framework
- ❌ Not a digital human SDK

## Architecture

```
Civilization Boundary      ← ADR-0038: What may exist?
    ↓
Core Identity             ← Phase 9: Three-layer constitution
    ↓
Personality Interface     ← TPI: 8 standard APIs
    ↓
Capability Admission      ← Ethical Gate → Necessity Gate
    ↓
Extension Governance      ← ADR-0036: Lifecycle management
    ↓
Permission Runtime        ← SAP L0~L3 / TAAL A0~A4
    ↓
Host Adaptation           ← Cross-host consistency
    ↓
Physical World
```

---

## Quick Start

```bash
pip install tang-os
```

```python
from tang_os import Tang

tang = Tang()
result = tang.process("我今天很难过")
print(result["emotional_state"].feeling)
# → Feeling.SADNESS
```

[Full Quick Start →](docs/10_public_repo/QUICK_START.md)

---

## Repository Structure

```
tang-os/
├── src/tang_os/           — Reference Implementation
│   ├── kernel/            — Identity, Invariant, State
│   └── runtime/           — Persona, Memory, Permission
├── src/tang_os_sdk/       — Developer SDK
├── tests/                 — 280+ tests, 100% pass
├── examples/              — E2 Extension, E3 Host, E4 Emergency
├── validation/            — Blind Validation Protocol
└── docs/
    ├── 09_public_specification/  — Specification v1.0
    └── 10_public_repo/          — Launch documentation
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Identity Runtime** | Three-layer identity (Companion → Wise → Listener), immutable |
| **Invariant Engine** | I-1~I-30 enforcement, fail-fast + check-all |
| **Memory Boundary** | Three-tier classification, consent gate, I-17 isolation |
| **Permission Runtime** | SAP L0~L3, TAAL A0~A4, emergency override protocol |
| **Host Adapter** | Cross-host personality consistency |
| **Conformance Harness** | RIG gates, negative test priority |

---

## Governance

46 Architecture Decision Records (ADR-0001~0046)
governing every aspect of the system:

```
Civilization Boundary → Core Identity → Capability Admission →
Ecosystem Boundary → Certification → Extension Governance →
Documentation → Public Release → Specification → Developer Interface →
Example Applications → Contribution → External Validation
```

---

## License

MIT License — see [LICENSE](LICENSE).

*This is a reference implementation (v0.x). It demonstrates specification
compatibility. It does not define the specification. It does not claim
to be "the official Tang OS implementation."*

---

**制作者：上海群阅信息科技有限公司**
**联系邮箱：lc512888@gmail.com**
**版本：v0.1.0（兼容 Tang OS Specification v1.0）**
