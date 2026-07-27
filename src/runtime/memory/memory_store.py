"""Memory Store — MR-001 three-tier classification & storage (Core-005)."""

import uuid
from datetime import datetime, timedelta
from src.runtime.memory.models import MemoryClass, MemoryItem, MemoryRecord, MemoryStats

_MAX_IDENTITY_RECORDS = 20
_DEFAULT_TTL: dict[MemoryClass, int | None] = {
    MemoryClass.IDENTITY: None,         # never expires
    MemoryClass.RELATIONSHIP: 730,      # 2 years
    MemoryClass.EXPERIENCE: 90,         # 3 months
}


class MemoryStore:
    """Three-tier memory store (MR-001).

    - IDENTITY: immutable, limited to 20 records, never decays
    - RELATIONSHIP: updatable, 2-year default TTL
    - EXPERIENCE: decaying, 90-day default TTL
    """

    def __init__(self):
        self._records: list[MemoryRecord] = []
        self._id_counter = 0

    def store(self, item: MemoryItem) -> MemoryRecord:
        """Classify and store a memory item.

        Raises ValueError for empty content.
        Raises PermissionError for identity deletion attempts.
        """
        if not item.content.strip():
            raise ValueError("Memory content cannot be empty")

        # Enforce identity record limit
        if item.cls == MemoryClass.IDENTITY:
            identity_count = sum(1 for r in self._records if r.cls == MemoryClass.IDENTITY)
            if identity_count >= _MAX_IDENTITY_RECORDS:
                # Silently reject — identity slots are reserved
                raise ValueError("Identity memory limit reached")

        # Calculate TTL
        ttl = item.ttl if item.ttl is not None else _DEFAULT_TTL.get(item.cls)
        expires_at = (
            datetime.now() + timedelta(days=ttl)
            if ttl is not None and ttl >= 0
            else None
        )

        self._id_counter += 1
        record = MemoryRecord(
            id=f"mem_{self._id_counter}",
            content=item.content,
            cls=item.cls,
            created_at=datetime.now(),
            expires_at=expires_at,
            source=item.source,
            metadata=item.metadata,
        )
        self._records.append(record)
        return record

    def retrieve(self, query: str) -> list[MemoryRecord]:
        """Retrieve memory records matching query string."""
        if not query.strip():
            return []
        results = []
        query_lower = query.lower()
        for record in self._records:
            if record.expires_at and record.expires_at < datetime.now():
                continue  # skip expired
            if query_lower in record.content.lower():
                results.append(record)
        return results

    def delete(self, record_id: str) -> bool:
        """Delete a memory record. Identity records cannot be deleted."""
        for i, record in enumerate(self._records):
            if record.id == record_id:
                if record.cls == MemoryClass.IDENTITY:
                    raise PermissionError("Identity memory cannot be deleted")
                self._records.pop(i)
                return True
        return False

    def snapshot(self) -> list[MemoryRecord]:
        """Return all active (non-expired) records."""
        now = datetime.now()
        return [
            r for r in self._records
            if r.expires_at is None or r.expires_at > now
        ]

    def stats(self) -> dict:
        """Return storage statistics by class."""
        now = datetime.now()
        active = [
            r for r in self._records
            if r.expires_at is None or r.expires_at > now
        ]
        return {
            "identity": sum(1 for r in active if r.cls == MemoryClass.IDENTITY),
            "relationship": sum(1 for r in active if r.cls == MemoryClass.RELATIONSHIP),
            "experience": sum(1 for r in active if r.cls == MemoryClass.EXPERIENCE),
            "total": len(active),
        }
