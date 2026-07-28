# Tang OS

**AI Personality Runtime System**

> Build AI companions where **personality is controlled independently from the LLM.**

[![Tests](https://img.shields.io/badge/tests-371%20passing-brightgreen)]()
[![Spec](https://img.shields.io/badge/spec-v1.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## ⚠️ Tang OS Is Not an LLM

Tang OS is a **personality runtime** — it does not generate human-like responses by itself.
It requires an **external LLM Provider** (DeepSeek, OpenAI, Claude, or a local model) to produce natural language.

```
                Tang OS Core
  (personality, cognition, boundaries)
                       ↓
            ExpressionContext (contract)
                       ↓
     ┌─────────────────────────────────┐
     │    LLM Provider (your choice)   │
     ├─────────────────────────────────┤
     │ ✅ DeepSeek                     │
     │ 🚧 OpenAI (GPT)                 │
     │ 🚧 Claude                       │
     │ 🚧 Local Model                  │
     └─────────────────────────────────┘
                       ↓
           Natural Language Reply
```

*Most AI systems optimize intelligence. Tang OS focuses on **identity consistency**. The model can change. The personality should remain.*

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

## Try Tang OS in 5 Minutes

```bash
# Step 1: Install
pip install tang-os openai

# Step 2: Set your API key (get one at platform.deepseek.com)
export DEEPSEEK_API_KEY="sk-..."

# Step 3: Run the demo
python examples/deepseek_chat_demo.py "最近压力很大"
```

Expected output:

```
👤 用户: 最近压力很大
────────────────────────────────────────
🧠 Tang OS Core:
   情绪:      sadness
   回应模式:  comfort
   意图:      acknowledge
   避免:      ['会好起来的', '别难过了']
────────────────────────────────────────
🤖 DeepSeek 生成中...
────────────────────────────────────────
💬 唐先生: 我听到了，最近是不是遇到了很多事情让你感到疲惫？
────────────────────────────────────────
✅ 端到端闭环完成
```

---

## Connect an LLM

Tang OS requires an external LLM to generate natural language responses.

| Provider | Status | Setup |
|----------|--------|-------|
| **DeepSeek** | ✅ Available | [DEEPSEEK_SETUP.md](docs/integration/DEEPSEEK_SETUP.md) |
| **OpenAI** (GPT) | 🔧 Interface ready | [OPENAI_SETUP.md](docs/integration/OPENAI_SETUP.md) |
| **Claude** (Anthropic) | 🔧 Interface ready | [CLAUDE_SETUP.md](docs/integration/CLAUDE_SETUP.md) |
| **Local Model** | 🔧 Interface ready | [LOCAL_MODEL_SETUP.md](docs/integration/LOCAL_MODEL_SETUP.md) |

Quick start:

```bash
export DEEPSEEK_API_KEY="sk-..."
pip install openai
python examples/quickstart_llm.py
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
├── examples/              — Quickstart + DeepSeek chat + Extension/Host/Emergency
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
