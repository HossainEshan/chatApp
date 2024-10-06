from cassandra.cluster import Session as CassandraSession
from redis.asyncio import Redis as RedisClient
from src.repository.cache import RedisCache
from src.repository.database import CassandraDatabase


class BaseCRUDRepository:
    def __init__(self, cassandra_db: CassandraDatabase, redis_cache: RedisCache):
        self.db_session: CassandraSession = cassandra_db.session
        self.cache_session: RedisClient = redis_cache.redis
