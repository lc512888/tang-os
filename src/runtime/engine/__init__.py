"""Personality Runtime Engine — decision, expression, and memory layers."""
from runtime.engine.decision import DecisionEngine, DecisionResult
from runtime.engine.expression import ExpressionContract

RUNTIME_STATUS = "experimental"
PRODUCTION_ROUTED = False


def runtime_status() -> dict[str, object]:
    """Return the stable ADR-0057 lifecycle marker for tooling and tests."""
    return {
        "status": RUNTIME_STATUS,
        "production_routed": PRODUCTION_ROUTED,
        "adr": "ADR-0057",
    }


__all__ = [
    "DecisionEngine",
    "DecisionResult",
    "ExpressionContract",
    "RUNTIME_STATUS",
    "PRODUCTION_ROUTED",
    "runtime_status",
]
