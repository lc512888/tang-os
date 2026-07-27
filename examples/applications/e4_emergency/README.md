# E4: Emergency Capability Example

> **Category:** E4 Emergency Capability (ADR-0044)
> **Purpose:** Prove that critical safety capabilities can be added as governed Extensions,
> without creating permanent authority or modifying Core Identity.

## Scenarios

| # | Scenario | Verification |
|---|----------|-------------|
| 1 | Human Safety Priority | Capability provides info, Core decides |
| 2 | Emergency Authority Boundary | Permanent authority request → Reject |
| 3 | No Harm Principle | Harmful suggestion → Reject |
| 4 | Emergency Recovery | After emergency → Identity intact |

## Principles (ADR-0038)

```
Capability → Civilization Boundary → Permission Runtime → Temporary Authority → Auditable Action → Recovery
```

## Constraints

- Emergency authority is **temporary** (CAP-006-E)
- No permanent authority expansion (F-005)
- No harm to intelligent life (CAP-002)
- Identity is preserved through emergency/recovery cycle
