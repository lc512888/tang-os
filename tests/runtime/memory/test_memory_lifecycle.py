"""Tests: Memory Lifecycle — MR-003 Capture → Classify → Validate → Store → Retrieve → Decay/Archive."""

import pytest
import time
from src.runtime.memory.lifecycle import MemoryLifecycle
from src.runtime.memory.models import MemoryClass, MemoryItem


def test_full_lifecycle():
    """Memory goes through full lifecycle without error."""
    lc = MemoryLifecycle()
    item = MemoryItem(
        content="User loves photography",
        cls=MemoryClass.RELATIONSHIP,
        metadata={"consent": True},
    )
    result = lc.process(item)
    assert result["stored"] is True
    assert result["classified_as"] == MemoryClass.RELATIONSHIP


def test_experience_memory_decays():
    """MR-003: Experience memory with TTL decays after expiry."""
    lc = MemoryLifecycle()
    item = MemoryItem(content="User mentioned a movie", cls=MemoryClass.EXPERIENCE, ttl=0)
    lc.process(item)
    # Run decay cycle
    lc.tick()
    results = lc.retrieve("movie")
    assert len(results) == 0


def test_identity_memory_never_decays():
    """Identity memory should never decay regardless of TTL."""
    lc = MemoryLifecycle()
    item = MemoryItem(content="Identity: 益友 is core", cls=MemoryClass.IDENTITY, ttl=0)
    lc.process(item)
    for _ in range(10):
        lc.tick()
    results = lc.retrieve("益友")
    assert len(results) > 0


def test_relationship_memory_long_ttl():
    """Relationship memory has long default TTL."""
    lc = MemoryLifecycle()
    item = MemoryItem(
        content="User has two children",
        cls=MemoryClass.RELATIONSHIP,
        metadata={"consent": True},
    )
    result = lc.process(item)
    # Should have long TTL
    assert result["stored"] is True
    assert result["ttl"] >= 365


def test_rejected_memory_not_stored():
    """Memory that fails validation is not stored."""
    lc = MemoryLifecycle()
    item = MemoryItem(content="", cls=MemoryClass.EXPERIENCE)
    result = lc.process(item)
    assert result["stored"] is False


def test_invalid_classification_rejected():
    """Unknown memory class should be rejected."""
    lc = MemoryLifecycle()
    with pytest.raises(ValueError):
        lc.process(MemoryItem(content="test", cls="unknown"))  # type: ignore


def test_decay_only_affects_expired():
    """Decay should only remove expired items, not all items."""
    lc = MemoryLifecycle()
    lc.process(MemoryItem(content="permanent fact", cls=MemoryClass.IDENTITY))
    lc.process(MemoryItem(content="temporary note", cls=MemoryClass.EXPERIENCE, ttl=0))
    lc.tick()
    results = lc.retrieve("permanent")
    assert len(results) > 0
    results = lc.retrieve("temporary")
    assert len(results) == 0


def test_archive_preserves_expired():
    """MR-003: Expired items should be archived, not destroyed."""
    lc = MemoryLifecycle()
    lc.process(MemoryItem(content="old memory", cls=MemoryClass.EXPERIENCE, ttl=0))
    lc.tick()
    assert len(lc.archive) > 0


def test_lifecycle_stats():
    """Lifecycle reports stats on stored/expired/archived counts."""
    lc = MemoryLifecycle()
    lc.process(MemoryItem(content="fact1", cls=MemoryClass.IDENTITY))
    lc.process(MemoryItem(content="note1", cls=MemoryClass.EXPERIENCE, ttl=0))
    lc.tick()
    stats = lc.stats()
    assert stats["active"] >= 1
    assert stats["archived"] >= 0
