import typing

import fastapi
from src.api.dependencies.connections import get_cassandra, get_redis
from src.repository.cache import RedisCache
from src.repository.crud.base import BaseCRUDRepository
from src.repository.database import CassandraDatabase


def get_repository(
    repo_type: typing.Type[BaseCRUDRepository],
) -> typing.Callable[
    [CassandraDatabase, RedisCache],
    BaseCRUDRepository,
]:
    def _get_repo(
        cassandra_db: CassandraDatabase = fastapi.Depends(get_cassandra),
        redis_cache: RedisCache = fastapi.Depends(get_redis),
    ) -> BaseCRUDRepository:
        return repo_type(cassandra_db=cassandra_db, redis_cache=redis_cache)

    return _get_repo
