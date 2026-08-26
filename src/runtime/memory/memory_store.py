"""Memory Store — MR-001 three-tier classification & storage (Core-005)."""

from copy import deepcopy
from datetime import datetime, timedelta, timezone
from runtime.memory.models import MemoryClass, MemoryItem, MemoryRecord, as_utc

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

    @staticmethod
    def _normalize_timestamps(record: MemoryRecord) -> None:
        """Migrate legacy naive record timestamps in place on access."""
        record.created_at = as_utc(record.created_at)
        if record.accessed_at is not None:
            record.accessed_at = as_utc(record.accessed_at)
        if record.expires_at is not None:
            record.expires_at = as_utc(record.expires_at)

    def store(self, item: MemoryItem) -> MemoryRecord:
        """Classify and store a memory item.

        Raises ValueError for empty content.
        Raises PermissionError for identity deletion attempts.
        """
        if not isinstance(item, MemoryItem):
            raise TypeError("item must be a MemoryItem")
        if not isinstance(item.content, str) or not item.content.strip():
            raise ValueError("Memory content cannot be empty")
        if len(item.content) > 10_000:
            raise ValueError("Memory content exceeds 10000 characters")
        if not isinstance(item.cls, MemoryClass):
            raise ValueError("Invalid memory class")
        if item.ttl is not None and (isinstance(item.ttl, bool) or not isinstance(item.ttl, int) or item.ttl < 0):
            raise ValueError("ttl must be a non-negative integer or None")
        if not isinstance(item.source, str) or not item.source.strip():
            raise ValueError("source must be a non-empty string")
        if not isinstance(item.metadata, dict):
            raise TypeError("metadata must be a mapping")

        # Enforce identity record limit
        if item.cls == MemoryClass.IDENTITY:
            identity_count = sum(1 for r in self._records if r.cls == MemoryClass.IDENTITY)
            if identity_count >= _MAX_IDENTITY_RECORDS:
                # Silently reject — identity slots are reserved
                raise ValueError("Identity memory limit reached")

        # Calculate TTL
        ttl = item.ttl if item.ttl is not None else _DEFAULT_TTL.get(item.cls)
        expires_at = (
            datetime.now(timezone.utc) + timedelta(days=ttl)
            if ttl is not None and ttl >= 0
            else None
        )

        self._id_counter += 1
        record = MemoryRecord(
            id=f"mem_{self._id_counter}",
            content=item.content,
            cls=item.cls,
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at,
            source=item.source,
            metadata=deepcopy(item.metadata),
        )
        self._records.append(record)
        return deepcopy(record)

    def retrieve(self, query: str) -> list[MemoryRecord]:
        """Retrieve memory records matching query string."""
        if not query.strip():
            return []
        results = []
        query_lower = query.lower()
        for record in self._records:
            self._normalize_timestamps(record)
            if record.expires_at and as_utc(record.expires_at) < datetime.now(timezone.utc):
                continue  # skip expired
            if query_lower in record.content.lower():
                results.append(record)
        return deepcopy(results)

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
        now = datetime.now(timezone.utc)
        active = []
        for record in self._records:
            self._normalize_timestamps(record)
            if record.expires_at is None or record.expires_at > now:
                active.append(record)
        return deepcopy(active)

    def archive_expired(self) -> list[MemoryRecord]:
        """Remove and return expired records without exposing internal storage."""
        now = datetime.now(timezone.utc)
        expired: list[MemoryRecord] = []
        active: list[MemoryRecord] = []
        for record in self._records:
            self._normalize_timestamps(record)
            if record.expires_at is not None and as_utc(record.expires_at) <= now:
                expired.append(record)
            else:
                active.append(record)
        self._records = active
        return deepcopy(expired)

    def stats(self) -> dict:
        """Return storage statistics by class."""
        now = datetime.now(timezone.utc)
        active = []
        for record in self._records:
            self._normalize_timestamps(record)
            if record.expires_at is None or record.expires_at > now:
                active.append(record)
        return {
            "identity": sum(1 for r in active if r.cls == MemoryClass.IDENTITY),
            "relationship": sum(1 for r in active if r.cls == MemoryClass.RELATIONSHIP),
            "experience": sum(1 for r in active if r.cls == MemoryClass.EXPERIENCE),
            "total": len(active),
        }
