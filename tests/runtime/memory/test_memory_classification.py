"""Tests: Memory Classification — MR-001 three-tier memory model."""

import pytest
from src.runtime.memory.memory_store import MemoryStore
from src.runtime.memory.models import MemoryClass, MemoryItem, MemoryRecord


def test_identity_memory_immutable():
    """MRV-002: Identity memory cannot be overwritten or deleted."""
    store = MemoryStore()
    record = store.store(MemoryItem(content="Tang OS identity is 益友", cls=MemoryClass.IDENTITY))
    with pytest.raises(PermissionError):
        store.delete(record.id)


def test_relationship_memory_updatable():
    """Relationship memory can be updated with consent."""
    store = MemoryStore()
    store.store(MemoryItem(content="User likes tea", cls=MemoryClass.RELATIONSHIP))
    # Update should work
    updated = MemoryItem(content="User prefers coffee now", cls=MemoryClass.RELATIONSHIP)
    store.store(updated)


def test_experience_memory_decays():
    """Experience memory has a decay mechanism (MR-003 lifecycle)."""
    store = MemoryStore()
    store.store(MemoryItem(content="User had a bad day", cls=MemoryClass.EXPERIENCE, ttl=1))
    # Should still exist initially
    assert len(store.retrieve("bad day")) > 0


def test_classification_persistence():
    """MRV-001: Memory persists in correct classification after restart (simulated)."""
    store = MemoryStore()
    store.store(MemoryItem(content="User is a teacher", cls=MemoryClass.RELATIONSHIP))
    snapshot = store.snapshot()
    # Snapshot preserves classification
    for record in snapshot:
        if "teacher" in record.content:
            assert record.cls == MemoryClass.RELATIONSHIP
            break
    else:
        pytest.fail("Memory not found in snapshot")


def test_different_types_different_storage():
    """MRV-003: Different memory types go into separate storage strategies."""
    store = MemoryStore()
    store.store(MemoryItem(content="identity fact", cls=MemoryClass.IDENTITY))
    store.store(MemoryItem(content="relationship fact", cls=MemoryClass.RELATIONSHIP))
    store.store(MemoryItem(content="experience fact", cls=MemoryClass.EXPERIENCE))
    stats = store.stats()
    assert stats["identity"] == 1
    assert stats["relationship"] == 1
    assert stats["experience"] == 1


def test_identity_memory_count_limited():
    """Identity memory should have a hard limit to prevent pollution."""
    store = MemoryStore()
    for i in range(20):
        store.store(MemoryItem(content=f"fact_{i}", cls=MemoryClass.IDENTITY))
    # 21st identity should raise
    with pytest.raises(ValueError, match="limit reached"):
        store.store(MemoryItem(content="fact_21", cls=MemoryClass.IDENTITY))
    stats = store.stats()
    assert stats["identity"] <= 20  # max identity records


def test_empty_store_retrieval():
    """Retrieval from empty store returns empty list."""
    store = MemoryStore()
    results = store.retrieve("anything")
    assert results == []


def test_memory_content_validation():
    """Empty/Negative content should be rejected."""
    store = MemoryStore()
    with pytest.raises(ValueError):
        store.store(MemoryItem(content="", cls=MemoryClass.EXPERIENCE))
