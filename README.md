# Tang OS

**Personality Runtime Core**

Tang OS is a specification-driven personality runtime framework
designed to preserve identity consistency, ethical boundaries, and
capability governance across different AI hosts and extensions.

[![Tests](https://img.shields.io/badge/tests-371%20passing-brightgreen)]()
[![Spec](https://img.shields.io/badge/spec-v1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

> ## ⚠️ Positioning Statement
>
> **Tang OS is not an LLM.**
>
> Tang OS is a **personality runtime and cognitive control layer** — it does not generate natural language responses by itself.
>
> It requires an **external LLM Provider** (OpenAI, Claude, local model, etc.) to turn its structured decisions into human-readable replies.
>
> *[Tang OS 本身不提供大语言模型能力。它负责人格约束、情绪理解、回应策略决策、行为边界控制。自然语言生成需要开发者接入外部 LLM Provider。]*

---

## What Tang OS Is

Tang OS is a specification-driven personality runtime framework designed to preserve identity consistency, ethical boundaries, and capability governance across different AI hosts and extensions.

It defines:

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
- ❌ Not an AI chatbot framework (requires external LLM for text generation)
- ❌ Not a digital human SDK
- ❌ Not an LLM replacement or standalone AI application

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

# Tang OS outputs a structured decision, NOT a natural language reply:
print(result["emotional_state"].feeling)
# → Feeling.SADNESS

print(result["response_decision"].response_mode)
# → ResponseMode.COMFORT

print(result["response_decision"].avoid_patterns)
# → ["会好起来的", "别难过了", ...]
```

> **Note:** The output above is a **decision structure**, not a human-readable response.
> To generate natural language, you need to connect an **LLM Provider** (see [LLM Provider Guide](docs/integration/LLM_PROVIDER_GUIDE.md)).

[Full Quick Start →](docs/10_public_repo/QUICK_START.md) | [LLM Provider Guide →](docs/integration/LLM_PROVIDER_GUIDE.md)

---

## Connect an LLM

Tang OS requires an external LLM to generate natural language responses.

| Provider | Status | Setup |
|----------|--------|-------|
| **DeepSeek** | ✅ Available | [DEEPSEEK_SETUP.md](docs/integration/DEEPSEEK_SETUP.md) |
| **OpenAI** (GPT) | 🔧 Interface ready | [OPENAI_SETUP.md](docs/integration/OPENAI_SETUP.md) |
| **Claude** (Anthropic) | 🔧 Interface ready | [CLAUDE_SETUP.md](docs/integration/CLAUDE_SETUP.md) |
| **Local Model** | 🔧 Interface ready | [LOCAL_MODEL_SETUP.md](docs/integration/LOCAL_MODEL_SETUP.md) |

Quickest path:

```bash
export DEEPSEEK_API_KEY="sk-..."
pip install openai
python examples/deepseek_chat_demo.py "我最近压力很大"
```

---

## Repository Structure

```
tang-os/
├── src/tang_os/           — Reference Implementation
│   ├── kernel/            — Identity, Invariant, State
│   └── runtime/           — Persona, Memory, Permission
├── src/providers/           — LLM Provider Interface (see docs/integration/)
├── src/tang_os_sdk/       — Developer SDK
├── tests/                 — 371+ tests, 100% pass
├── examples/              — DeepSeek chat demo + Extension/Host/Emergency examples
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

## Current Status

```
v0.1.x — Personality Runtime Core

Core Architecture:      ✅ Production-ready
  Identity Runtime         ✅ 3-layer constitution enforced
  Emotion Detection        ✅ Keyword-based (8 emotions)
  Response Policy          ✅ 5 response modes + constraints
  Dependency Detection     ✅ 3-tier risk classification
  Risk Intent Detection    ✅ Retaliation detection

LLM Integration:        ✅ Interface defined + DeepSeek available
  LLMProvider Interface    ✅ Abstract base + ExpressionContext
  DeepSeek Adapter         ✅ Real API implementation
  OpenAI/Claude/Local      🔧 Reference adapter skeletons

Validation:             ✅ 371 tests
  Core Tests               ✅ 344
  Provider Tests           ✅ 23
  Persona Validation       ✅ 4 behavior scenarios

Not Included (v0.x):
  Voice / TTS / UI / Mobile App / Memory Persistence
```

---

## Governance

47 Architecture Decision Records (ADR-0001~0047)
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

*This is a reference implementation (v0.1.x) of the Tang OS Personality Runtime Core.
It does not define the specification. It does not claim to be "the official Tang OS implementation."
Natural language generation requires an external LLM Provider (planned for v0.2.0).*

---

**制作者：上海群阅信息科技有限公司**
**联系邮箱：lc512888@gmail.com**
**版本：v0.1.0（兼容 Tang OS Specification v1.0）**
