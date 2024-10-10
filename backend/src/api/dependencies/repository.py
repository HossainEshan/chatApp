import typing

import fastapi
from src.api.dependencies.connections import get_cassandra, get_redis
from src.repository.cache import RedisCache
from src.repository.crud.base import BaseCRUDRepository
from src.repository.database import CassandraDatabase

_repo_instances = {}  # Store repo instances to reduce overhead


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

        if not repo_type in _repo_instances:
            _repo_instances[repo_type] = repo_type(cassandra_db=cassandra_db, redis_cache=redis_cache)

        return _repo_instances[repo_type]

    return _get_repo
