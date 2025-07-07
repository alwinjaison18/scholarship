"""
Cache utilities using Redis.
"""

import json
import pickle
from typing import Any, Optional, Union
from datetime import datetime, timedelta
import logging

try:
    import redis
    from redis import Redis
except ImportError:
    redis = None
    Redis = None

logger = logging.getLogger(__name__)


class CacheService:
    """Cache service using Redis."""

    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = None
        if redis:
            try:
                self.redis_client = redis.from_url(redis_url)
                # Test connection
                self.redis_client.ping()
                logger.info("Redis connected successfully")
            except Exception as e:
                logger.warning(f"Redis connection failed: {e}")
                self.redis_client = None
        else:
            logger.warning("Redis not available, cache will be disabled")

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        if not self.redis_client:
            return default

        try:
            value = self.redis_client.get(key)
            if value is None:
                return default

            # Try to deserialize as JSON first, then pickle
            try:
                return json.loads(value)
            except (json.JSONDecodeError, TypeError):
                return pickle.loads(value)
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return default

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL in seconds."""
        if not self.redis_client:
            return False

        try:
            # Try to serialize as JSON first, then pickle
            try:
                serialized_value = json.dumps(value)
            except (TypeError, ValueError):
                serialized_value = pickle.dumps(value)

            return self.redis_client.setex(key, ttl, serialized_value)
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.redis_client:
            return False

        try:
            return bool(self.redis_client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.redis_client:
            return False

        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False

    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern."""
        if not self.redis_client:
            return 0

        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Error clearing cache pattern {pattern}: {e}")
            return 0

    def get_stats(self) -> dict:
        """Get cache statistics."""
        if not self.redis_client:
            return {}

        try:
            info = self.redis_client.info()
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {}

# Cache decorators


def cache_result(ttl: int = 3600, key_prefix: str = ""):
    """Decorator to cache function results."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            cache = CacheService()

            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)

            return result
        return wrapper
    return decorator


# Global cache instance
cache = CacheService()
