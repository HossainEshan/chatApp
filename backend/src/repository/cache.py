from typing import Optional

import redis.asyncio as Redis
from redis.exceptions import RedisError
from src.config.manager import settings


class RedisCache:
    def __init__(self):
        """Initialize Redis connection attributes."""
        self.redis: Redis.Redis = None
        self.redis_uri: str = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"

    async def initialize(self) -> None:
        """Initialize Redis connection asynchronously."""
        try:
            self.redis = Redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
            )
            # Test connection by pinging the server
            await self.redis.ping()
        except RedisError as e:
            print(f"Failed to initialize Redis: {e}")
            raise

    async def close(self) -> None:
        """Close Redis connection."""
        if self.redis:
            try:
                await self.redis.close()
            except RedisError as e:
                print(f"Error closing Redis connection: {e}")


# Singleton instance of RedisCache
cache: RedisCache = RedisCache()
