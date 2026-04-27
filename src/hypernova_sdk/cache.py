"""TTL cache utilities."""

import functools
import time
from collections import OrderedDict
from threading import Lock
from typing import Any, Callable, TypeVar

T = TypeVar("T")

__all__ = ["ttl_cache", "memoize", "TTLCache"]


def ttl_cache(seconds: float = 60, maxsize: int = 256):
    """Decorator that caches function results with a TTL and LRU eviction.

    Args:
        seconds: Time-to-live in seconds. Default is 60.
        maxsize: Maximum number of cached entries. Default is 256.
                 Evicts the oldest entry when the limit is reached.

    Example:
        >>> @ttl_cache(seconds=30)
        ... def fetch_data(url):
        ...     return requests.get(url).json()
        >>> fetch_data("https://api.example.com/data")  # fetches
        >>> fetch_data("https://api.example.com/data")  # returns cached
    """
    def decorator(fn: Callable[..., T]) -> Callable[..., T]:
        cache: OrderedDict[str, tuple[float, Any]] = OrderedDict()
        lock = Lock()
        def wrapper(*args: Any, **kwargs: Any) -> T:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            with lock:
                if key in cache:
                    written_at, result = cache[key]
                    if now - written_at < seconds:
                        cache.move_to_end(key)
                        return result  # type: ignore[return-value]
                    del cache[key]  # expired — remove before recomputing
            result = fn(*args, **kwargs)
            with lock:
                cache[key] = (now, result)
                while len(cache) > maxsize:
                    cache.popitem(last=False)
            return result
        return wrapper
    return decorator


def memoize(fn: Callable[..., T]) -> Callable[..., T]:
    """Simple unbounded memoization (no expiry, lifetime of process).

    Example:
        >>> @memoize
        ... def expensive(x):
        ...     return x * 2
        >>> expensive(5)
        10
        >>> expensive(5)  # cached
        10
    """
    return functools.lru_cache(maxsize=None)(fn)


class TTLCache:
    """Thread-safe LRU cache with TTL eviction.

    Args:
        maxsize: Maximum number of entries. Default is 128.
        ttl: Time-to-live per entry in seconds. Default is 60.

    Example:
        >>> cache = TTLCache(ttl=30, maxsize=256)
        >>> cache.set("key", {"data": "value"})
        >>> cache.get("key")
        {'data': 'value'}
        >>> "key" in cache
        True
        >>> len(cache)
        1
        >>> cache.clear()
    """

    def __init__(self, maxsize: int = 128, ttl: float = 60) -> None:
        if maxsize < 0:
            raise ValueError("maxsize must be non-negative")
        self._cache: OrderedDict[str, tuple[float, Any]] = OrderedDict()
        self._maxsize = maxsize
        self._ttl = ttl
        self._lock = Lock()

    def get(self, key: str) -> Any | None:
        """Get a value, returning None if missing or expired."""
        with self._lock:
            if key not in self._cache:
                return None
            written_at, value = self._cache[key]
            if time.monotonic() - written_at > self._ttl:
                del self._cache[key]
                return None
            self._cache.move_to_end(key)
            return value

    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair, evicting oldest if at capacity."""
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (time.monotonic(), value)
            while self._cache and len(self._cache) > self._maxsize:
                self._cache.popitem(last=False)

    def clear(self) -> None:
        """Remove all entries."""
        with self._lock:
            self._cache.clear()

    def __len__(self) -> int:
        """Number of entries (includes potentially expired entries not yet evicted)."""
        return len(self._cache)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists and is not expired."""
        return self.get(key) is not None

    def __repr__(self) -> str:
        return f"TTLCache(maxsize={self._maxsize}, ttl={self._ttl})"