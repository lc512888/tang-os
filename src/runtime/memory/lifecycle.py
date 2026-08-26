"""Memory Lifecycle — MR-003 Capture → Classify → Validate → Store → Retrieve → Decay/Archive."""

from collections import deque
from copy import deepcopy
from datetime import datetime, timezone
from runtime.memory.memory_store import MemoryStore
from runtime.memory.memory_policy import MemoryPolicy
from runtime.memory.models import MemoryClass, MemoryItem, MemoryRecord, MemoryStats

# Default TTLs per class
_DEFAULT_TTL: dict[MemoryClass, int | None] = {
    MemoryClass.IDENTITY: None,         # never decays
    MemoryClass.RELATIONSHIP: 730,      # 2 years
    MemoryClass.EXPERIENCE: 90,         # 3 months
}


class MemoryLifecycle:
    """Manages full memory lifecycle (MR-003).

    Pipeline:
    Capture → Classify → Validate → Store → Retrieve → Decay/Archive
    """

    def __init__(self):
        self._store = MemoryStore()
        self._policy = MemoryPolicy()
        self._archive: list[MemoryRecord] = []
        self._rejected: deque[dict] = deque(maxlen=100)

    @property
    def archive(self) -> list[MemoryRecord]:
        return deepcopy(self._archive)

    def process(self, item: MemoryItem) -> dict:
        """Process a memory item through the full lifecycle.

        Returns dict with:
        - stored: bool
        - classified_as: MemoryClass
        - ttl: int or None
        - reason: str (if rejected)
        """
        if not isinstance(item, MemoryItem):
            raise TypeError("item must be a MemoryItem")
        item = deepcopy(item)
        if not isinstance(item.cls, MemoryClass):
            raise ValueError(f"Invalid memory class: {item.cls}")

        # Identity memory never decays
        if item.cls == MemoryClass.IDENTITY:
            item.ttl = None
        # Set default TTL for other classes if not provided
        elif item.ttl is None:
            item.ttl = _DEFAULT_TTL.get(item.cls)

        # Validate
        validation = self._policy.validate(item)
        if not validation["valid"]:
            self._rejected.append({
                "class": item.cls.value,
                "reason": validation["reason"],
                "timestamp": datetime.now(timezone.utc),
            })
            return {
                "stored": False,
                "classified_as": item.cls,
                "ttl": item.ttl,
                "reason": validation["reason"],
            }

        # Store
        try:
            record = self._store.store(item)
        except (ValueError, PermissionError) as e:
            self._rejected.append({
                "class": item.cls.value,
                "reason": str(e),
                "timestamp": datetime.now(timezone.utc),
            })
            return {
                "stored": False,
                "classified_as": item.cls,
                "ttl": item.ttl,
                "reason": str(e),
            }

        return {
            "stored": True,
            "classified_as": item.cls,
            "ttl": item.ttl,
            "record_id": record.id,
        }

    def retrieve(self, query: str) -> list[MemoryRecord]:
        """Retrieve active (non-expired) memories."""
        return self._store.retrieve(query)

    def snapshot(self) -> list[MemoryRecord]:
        """Return a detached snapshot of active records."""
        return self._store.snapshot()

    def tick(self) -> int:
        """Run decay cycle — archive expired records.

        Returns count of archived records.
        """
        expired = self._store.archive_expired()
        self._archive.extend(expired)
        return len(expired)

    def stats(self) -> dict:
        """Return lifecycle statistics."""
        store_stats = self._store.stats()
        return {
            "active": store_stats["total"],
            "archived": len(self._archive),
            "rejected": len(self._rejected),
            "by_class": {
                "identity": store_stats["identity"],
                "relationship": store_stats["relationship"],
                "experience": store_stats["experience"],
            },
        }
