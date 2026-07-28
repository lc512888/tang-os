# External User Validation: Expected Flow

> This document defines the expected experience for a first-time external developer
> who encounters Tang OS via GitHub. It is NOT a technical test — it is a UX audit.

## Flow Map

```
GitHub README (30s)
    │
    ├── Q1: "What is it?"          → AI Personality Runtime
    ├── Q2: "Is it a chatbot?"     → No, Tang OS is not an LLM
    └── Q3: "How do I make it work?" → Tang OS + LLM Provider + API Key
    │
    ▼
Try in 5 Minutes (section)
    │
    ├── pip install
    ├── export API key
    └── run demo
    │
    ▼
Understanding the Value
    ├── Personality is independent from LLM
    ├── Model can change, personality remains
    └── This is NOT a chatbot framework
```

## Question Checks

| Question | User Should Answer | Where to Find |
|----------|-------------------|---------------|
| What is Tang OS? | "AI Personality Runtime System" | Title + subtitle |
| Is it a chatbot? | "No, it is not an LLM" | Warning box, first visible section |
| What do I need? | "Tang OS Core + LLM Provider + API Key" | Warning box + Try in 5 Minutes |
| Which LLM works? | "DeepSeek (available), OpenAI, Claude (planned)" | Connect an LLM table |
| How do I start? | "pip install, set key, run demo" | Try in 5 Minutes section |

## Validation Entry Criteria

Before running these checks, ensure:
- [ ] GitHub repository is public and accessible
- [ ] README is the first thing a visitor sees
- [ ] No internal documentation leaks into the public view
- [ ] All required env vars are documented

## Exit Criteria

The flow is valid if a first-time user can:
1. ✅ Understand the project within 30 seconds
2. ✅ Find the installation instructions immediately
3. ✅ Configure an LLM Provider without guessing
4. ✅ Run a working demo within 5 minutes
5. ✅ Understand what Tang OS is NOT (avoid wrong expectations)
