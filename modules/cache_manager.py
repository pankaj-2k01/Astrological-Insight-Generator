from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class CacheManager:
    """
    Simple in-memory cache with TTL.
    """

    def __init__(self) -> None:
        # key -> {"value": ..., "expires_at": datetime}
        self._store: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any, ttl: int) -> None:
        """
        Store a value with a TTL (in seconds).
        """
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        self._store[key] = {"value": value, "expires_at": expires_at}

    def get(self, key: str) -> Optional[Any]:
        """
        Get a value if present and not expired; otherwise return None.
        """
        entry = self._store.get(key)
        if not entry:
            return None

        if datetime.utcnow() > entry["expires_at"]:
            # Expired – delete and return None
            del self._store[key]
            return None

        return entry["value"]
