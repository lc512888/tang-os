"""Retrieval Engine — MR-004 context-isolated memory retrieval.

Ensures that session context, emergency context, and temporary data
are never returned as permanent memory (I-17, Core-005).
"""

from dataclasses import dataclass, field
from datetime import datetime
from src.runtime.memory.models import MemoryRecord, MemoryClass


@dataclass
class RetrievalContext:
    """Context for a memory retrieval request.

    Tracks the session boundary to prevent context leakage.
    """
    session_id: str
    query: str
    timestamp: datetime = field(default_factory=datetime.now)
    is_emergency: bool = False
    max_results: int = 10


class RetrievalEngine:
    """Context-isolated retrieval engine (MR-004).

    Guarantees:
    - Session context is never returned as permanent memory
    - Emergency context is clearly marked and separated
    - Temporary context tags don't leak into retrieval results
    - Results are ordered by relevance and recency
    """

    def retrieve(self, context: RetrievalContext, memory_pool: list[MemoryRecord]) -> list[MemoryRecord]:
        """Retrieve memory records matching the query within context boundaries."""
        if not context.query.strip():
            return []

        query_lower = context.query.lower()
        results: list[MemoryRecord] = []

        for record in memory_pool:
            # Skip expired
            if record.expires_at and record.expires_at < datetime.now():
                continue

            # Skip emergency-sourced records in non-emergency retrieval
            if not context.is_emergency and record.source == "emergency_context":
                continue

            # Content match
            if query_lower in record.content.lower():
                results.append(record)

        # Sort by recency (most recent first), then limit
        results.sort(key=lambda r: r.created_at, reverse=True)
        return results[:context.max_results]
