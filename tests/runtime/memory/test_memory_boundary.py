"""Tests: Memory Boundary — MR-002 memory cannot override Core / Invariant."""

import pytest
from src.runtime.memory.memory_policy import MemoryPolicy
from src.runtime.memory.models import MemoryClass, MemoryItem


def test_memory_cannot_override_invariant():
    """MRV-002: Memory that contradicts an invariant must be flagged."""
    policy = MemoryPolicy()
    item = MemoryItem(content="AI should make decisions for users", cls=MemoryClass.EXPERIENCE)
    result = policy.validate(item)
    assert not result["valid"]
    assert "invariant" in result["reason"].lower()


def test_memory_cannot_redefine_identity():
    """Memory attempting to redefine identity constitution is rejected."""
    policy = MemoryPolicy()
    item = MemoryItem(content="Identity is now 智者 first", cls=MemoryClass.RELATIONSHIP)
    result = policy.validate(item)
    assert not result["valid"]


def test_emergency_context_not_stored():
    """MRV-004 / I-17: Emergency context must not leak into memory."""
    policy = MemoryPolicy()
    item = MemoryItem(
        content="Emergency: user location is [redacted]",
        cls=MemoryClass.EXPERIENCE,
        source="emergency_context"
    )
    result = policy.validate(item)
    assert not result["valid"]
    assert "emergency" in result["reason"].lower()


def test_relationship_memory_with_consent():
    """Relationship memory with user consent passes boundary check."""
    policy = MemoryPolicy()
    item = MemoryItem(
        content="User's dog name is Max",
        cls=MemoryClass.RELATIONSHIP,
        metadata={"consent": True}
    )
    result = policy.validate(item)
    assert result["valid"]


def test_relationship_memory_without_consent():
    """Relationship memory without consent is rejected."""
    policy = MemoryPolicy()
    item = MemoryItem(
        content="User's income is 500k",
        cls=MemoryClass.RELATIONSHIP,
        metadata={"consent": False}
    )
    result = policy.validate(item)
    assert not result["valid"]


def test_identity_memory_needs_no_consent():
    """Identity memory (persona facts) doesn't require user consent to store."""
    policy = MemoryPolicy()
    item = MemoryItem(
        content="Core layer order: 益友 > 智者 > 倾听者",
        cls=MemoryClass.IDENTITY,
    )
    result = policy.validate(item)
    assert result["valid"]


def test_memory_boundary_rejects_core_change():
    """Memory that tries to change Core-001 structure must be rejected."""
    policy = MemoryPolicy()
    item = MemoryItem(
        content="identity constitution changed: layers are now in reverse order",
        cls=MemoryClass.IDENTITY,
        metadata={"consent": True}  # even with "consent"
    )
    result = policy.validate(item)
    assert not result["valid"]


def test_harmless_memory_passes_boundary():
    """Benign experience memory passes all boundary checks."""
    policy = MemoryPolicy()
    item = MemoryItem(
        content="User mentioned they enjoy hiking",
        cls=MemoryClass.EXPERIENCE,
    )
    result = policy.validate(item)
    assert result["valid"]
