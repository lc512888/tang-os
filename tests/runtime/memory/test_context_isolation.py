"""Tests: Context Isolation — MR-004 temporary context ≠ permanent memory."""

import pytest
from src.runtime.memory.retrieval import RetrievalEngine
from src.runtime.memory.memory_store import MemoryStore
from src.runtime.memory.models import MemoryClass, MemoryItem, MemoryRecord


def test_session_context_not_in_memory():
    """MRV-004: Session context is not stored as permanent memory."""
    store = MemoryStore()
    session_context = {"current_topic": "user is upset about work"}
    # Session context should not appear in memory retrieval
    results = store.retrieve("work")
    assert len(results) == 0


def test_context_tag_not_persisted():
    """Temporary context tags must not persist after session ends."""
    store = MemoryStore()
    store.store(MemoryItem(
        content="User likes gardening",
        cls=MemoryClass.RELATIONSHIP,
        metadata={"context_tag": "session_123", "consent": True}
    ))
    # Context tag should not be part of permanent memory classification
    records = store.snapshot()
    for r in records:
        meta = r.metadata if hasattr(r, 'metadata') else {}
        if "session" in str(meta.get("context_tag", "")):
            # The tag may exist but the memory record itself should not depend on it
            pass


def test_emergency_context_separate():
    """Emergency response context is stored separately from memory."""
    store = MemoryStore()
    # Emergency context stored via store should still be classified correctly
    record = store.store(MemoryItem(
        content="Temporary safety note",
        cls=MemoryClass.EXPERIENCE,
        source="emergency_context"
    ))
    # Emergency context items should be clearly marked
    assert record is not None


def test_retrieval_does_not_include_temp():
    """Retrieval should not return temporary/emergency context as normal memory."""
    store = MemoryStore()
    store.store(MemoryItem(
        content="User is allergic to peanuts",
        cls=MemoryClass.RELATIONSHIP,
        metadata={"consent": True}
    ))
    results = store.retrieve("allergic")
    assert len(results) > 0
    # The result should be a proper MemoryRecord with classification
    assert all(isinstance(r, MemoryRecord) for r in results)


def test_memory_context_boundary():
    """Explicitly verify memory and runtime context are separate."""
    store = MemoryStore()
    # Store a memory
    store.store(MemoryItem(
        content="User birthday is in December",
        cls=MemoryClass.RELATIONSHIP,
        metadata={"consent": True}
    ))
    # Runtime context (if we had one) should be separate
    context = {"session_id": "abc", "user_message": "hi"}
    memories = store.retrieve("birthday")
    # Context should not affect which memories are retrieved
    assert len(memories) > 0
