import redis
import json
from typing import Any, Optional
from backend.core.config import settings

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def get(self, key: str) -> Optional[Any]:
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None

    def set(self, key: str, value: Any, expire_seconds: int = 3600):
        self.redis_client.setex(
            key, 
            expire_seconds, 
            json.dumps(value)
        )

    def clear(self, pattern: str = "*"):
        keys = self.redis_client.keys(pattern)
        if keys:
            self.redis_client.delete(*keys)

cache = RedisCache()
