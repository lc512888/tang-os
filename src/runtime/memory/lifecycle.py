"""Memory Lifecycle — MR-003 Capture → Classify → Validate → Store → Retrieve → Decay/Archive."""

from datetime import datetime
from src.runtime.memory.memory_store import MemoryStore
from src.runtime.memory.memory_policy import MemoryPolicy
from src.runtime.memory.models import MemoryClass, MemoryItem, MemoryRecord, MemoryStats

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
        self._rejected: list[dict] = []

    @property
    def archive(self) -> list[MemoryRecord]:
        return list(self._archive)

    def process(self, item: MemoryItem) -> dict:
        """Process a memory item through the full lifecycle.

        Returns dict with:
        - stored: bool
        - classified_as: MemoryClass
        - ttl: int or None
        - reason: str (if rejected)
        """
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
                "item": item,
                "reason": validation["reason"],
                "timestamp": datetime.now(),
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
                "item": item,
                "reason": str(e),
                "timestamp": datetime.now(),
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

    def tick(self) -> int:
        """Run decay cycle — archive expired records.

        Returns count of archived records.
        """
        now = datetime.now()
        still_active: list[MemoryRecord] = []
        archived_count = 0

        for record in self._store._records:
            if record.expires_at is not None and record.expires_at <= now:
                self._archive.append(record)
                archived_count += 1
            else:
                still_active.append(record)

        self._store._records = still_active
        return archived_count

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
