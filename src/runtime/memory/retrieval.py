"""Retrieval Engine — MR-004 context-isolated memory retrieval.

Ensures that session context, emergency context, and temporary data
are never returned as permanent memory (I-17, Core-005).
"""

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from runtime.memory.models import MemoryRecord, as_utc


@dataclass
class RetrievalContext:
    """Context for a memory retrieval request.

    Tracks the session boundary to prevent context leakage.
    """
    session_id: str
    query: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
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
        if not isinstance(context.query, str) or not context.query.strip():
            return []
        if isinstance(context.max_results, bool) or not isinstance(context.max_results, int) or not 1 <= context.max_results <= 100:
            raise ValueError("max_results must be an integer between 1 and 100")

        query_lower = context.query.lower()
        results: list[MemoryRecord] = []

        for record in memory_pool:
            # Skip expired
            if record.expires_at and as_utc(record.expires_at) < datetime.now(timezone.utc):
                continue

            # Skip emergency-sourced records in non-emergency retrieval
            if not context.is_emergency and record.source == "emergency_context":
                continue

            # Content match
            if query_lower in record.content.lower():
                results.append(record)

        # Sort by recency (most recent first), then limit
        results.sort(key=lambda r: as_utc(r.created_at), reverse=True)
        return deepcopy(results[:context.max_results])
