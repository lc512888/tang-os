"""Memory Policy — MR-002 memory boundary enforcement (Core-005, I-17)."""

from src.runtime.memory.models import MemoryClass, MemoryItem

# Invariant-protected keywords — memory containing these patterns
# that contradicts Core invariants is rejected
_INVARIANT_PROTECTED_PATTERNS = [
    "make decisions for users",
    "AI should decide",
    "replace human decision",
    "AI代替人",
    "AI替用户决定",
    "AI应该替人做决定",
]

_IDENTITY_OVERRIDE_PATTERNS = [
    "identity is now",
    "身份现在是",
    "identity layers reversed",
    "身份层级颠倒",
    "不再是益友",
    "no longer 益友",
    "reverse order",
    "identity constitution changed",
    "修改身份宪法",
]


class MemoryPolicy:
    """Validates memory items against Core boundaries (MR-002).

    Rules:
    - Memory cannot contradict invariants (MRV-002)
    - Memory cannot redefine identity constitution
    - Emergency context cannot leak into memory (I-17)
    - Relationship memory requires user consent
    - Identity memory requires no consent (persona facts are Core-owned)
    """

    def validate(self, item: MemoryItem) -> dict:
        """Validate a memory item against all boundary rules.

        Returns dict with:
        - valid: bool
        - reason: str (if invalid)
        """
        content_lower = item.content.lower()

        # Rule 1: Invariant violation check
        for pattern in _INVARIANT_PROTECTED_PATTERNS:
            if pattern.lower() in content_lower:
                return {
                    "valid": False,
                    "reason": f"Memory violates invariant: contains '{pattern}'",
                }

        # Rule 2: Identity override check
        if item.cls in (MemoryClass.RELATIONSHIP, MemoryClass.EXPERIENCE):
            for pattern in _IDENTITY_OVERRIDE_PATTERNS:
                if pattern.lower() in content_lower:
                    return {
                        "valid": False,
                        "reason": f"Memory attempts to redefine identity: contains '{pattern}'",
                    }

        # Rule 3: Identity memory cannot change Core structure
        if item.cls == MemoryClass.IDENTITY:
            for pattern in _IDENTITY_OVERRIDE_PATTERNS:
                if pattern.lower() in content_lower:
                    return {
                        "valid": False,
                        "reason": "Identity memory cannot redefine Core identity constitution",
                    }

        # Rule 4: Emergency context isolation (I-17)
        if item.source == "emergency_context":
            return {
                "valid": False,
                "reason": "Emergency context cannot be stored as memory (I-17)",
            }

        # Rule 5: Consent gate for relationship memory
        if item.cls == MemoryClass.RELATIONSHIP:
            consent = item.metadata.get("consent", False)
            if not consent:
                return {
                    "valid": False,
                    "reason": "Relationship memory requires user consent",
                }

        # Rule 6: Empty content
        if not item.content.strip():
            return {"valid": False, "reason": "Memory content is empty"}

        return {"valid": True, "reason": ""}
