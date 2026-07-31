# ADR-0057: Personality Runtime Engine Architecture

**Date:** 2026-07-28
**Status:** Accepted
**Layer:** Tang OS Runtime Engine

## Context

Tang OS currently loads personality modules, binds them to sessions,
and passes context to LLM. However, the personality does not actively
participate in decision-making. The LLM receives identity/style
information but no structured decision guidance.

Without a runtime engine, personality is passive data rather than
an active governance layer.

## Decision: Three-Layer Engine

```
Personality Module (data)
    ↓
Runtime Engine (active)
    ├── Decision Layer    (boundaries, emotional policy)
    ├── Context Layer     (session state, memory boundary)
    └── Expression Layer  (LLM constraints, output guard)
    ↓
LLM (expression only)
```

### Layer 1: Decision Layer

Evaluates input against personality rules BEFORE LLM involvement:

```
Input
  → Boundary check (dependency risk, retaliation, inviolable rules)
  → Emotional policy (response mode mapping)
  → Value relevance (is this a value-laden input?)
  → DecisionResult (mode + intent + constraints)
```

### Layer 2: Context Layer

Manages what the personality knows vs what the user has shared:

```
Personality Memory (stable):
  - identity
  - values
  - boundaries
  - style (not session-specific)

User Context (session-scoped):
  - conversation history
  - user preferences
  - emotional state

Separation: NEVER mix personality memory with user context.
```

### Layer 3: Expression Layer

Constrains LLM output to stay within personality boundaries:

```
ExpressionContract:
  - Injects identity/role/style into system prompt
  - Applies decision constraints (mode, intent, avoid patterns)
  - Guards against boundary violations in output

The LLM may express freely WITHIN these constraints.
The LLM must NOT violate personality boundaries.
```

## Architecture Invariants

| Invariant | Enforcement |
|-----------|-------------|
| Engine must NOT hardcode Tang | All personality data comes from module |
| Engine must NOT modify module | Modules are read-only at runtime |
| Decision precedes expression | DecisionEngine runs before ExpressionContract |
| Personality is session-scoped | RuntimeSession binds one personality |
| Expression is LLM-agnostic | ExpressionContract works with any provider |

## File Structure

```
src/runtime/engine/
  decision.py     ← DecisionEngine + DecisionResult
  context.py      ← ContextManager (personality vs user memory)
  expression.py   ← ExpressionContract
```

## Boundaries

| Layer | Can Modify | Cannot Modify |
|-------|-----------|---------------|
| Decision Layer | session state | personality module |
| Context Layer | user context | personality identity |
| Expression Layer | LLM prompt | personality values |

## Non-Goals

- ❌ Replacing Tang OS core (kernel/runtime)
- ❌ Implementing LLM provider logic
- ❌ Adding product features
- ❌ Modifying xiaotang or tang-ta
