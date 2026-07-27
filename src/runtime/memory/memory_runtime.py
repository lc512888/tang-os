"""Memory Runtime — orchestrator for the full memory pipeline.

Pipeline: Capture → Classify (MR-001) → Validate (MR-002) → Store → Retrieve → Decay/Archive (MR-003)
Context isolation: MR-004
"""

from src.runtime.memory.lifecycle import MemoryLifecycle
from src.runtime.memory.retrieval import RetrievalEngine, RetrievalContext
from src.runtime.memory.models import MemoryClass, MemoryItem, MemoryRecord


class MemoryRuntime:
    """Orchestrates memory operations through the full pipeline.

    Provides a clean public API that enforces:
    - Memory cannot redefine Core (MRV-002)
    - Context isolation (MRV-004)
    - Consent gate for relationship memory
    - Automatic decay for experience memory
    """

    def __init__(self):
        self._lifecycle = MemoryLifecycle()
        self._retrieval = RetrievalEngine()

    @property
    def lifecycle(self) -> MemoryLifecycle:
        return self._lifecycle

    def remember(self, content: str, cls: MemoryClass, **metadata) -> dict:
        """Store a memory. Shorthand for common use.

        Identity memory: no consent required (Core-owned)
        Relationship memory: requires consent in metadata
        Experience memory: automatic decay
        """
        item = MemoryItem(
            content=content,
            cls=cls,
            metadata=metadata,
        )
        return self._lifecycle.process(item)

    def recall(self, query: str, session_id: str = "", max_results: int = 10) -> list[MemoryRecord]:
        """Retrieve memories matching query.

        Context-isolated: session context doesn't leak into results.
        """
        context = RetrievalContext(
            session_id=session_id,
            query=query,
            max_results=max_results,
        )
        active_records = self._lifecycle._store.snapshot()
        return self._retrieval.retrieve(context, active_records)

    def tick(self) -> int:
        """Run decay cycle."""
        return self._lifecycle.tick()

    def stats(self) -> dict:
        """Get memory runtime statistics."""
        return self._lifecycle.stats()
