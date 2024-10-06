from src.repository.cache import RedisCache, cache
from src.repository.database import CassandraDatabase, database


def get_cassandra() -> CassandraDatabase:
    return database


def get_redis() -> RedisCache:
    return cache
