import logging
import pathlib

import decouple
import pydantic
import pydantic_settings

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()


class BackendBaseSettings(pydantic_settings.BaseSettings):
    TITLE: str = "chatApp"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "UTC"
    DESCRIPTION: str | None = None
    DEBUG: bool = False

    BACKEND_SERVER_HOST: str = decouple.config("BACKEND_SERVER_HOST", cast=str)  # type: ignore
    BACKEND_SERVER_PORT: int = decouple.config("BACKEND_SERVER_PORT", cast=int)  # type: ignore
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""

    CASSANDRA_KEYSPACE: str = decouple.config("CASSANDRA_KEYSPACE", cast=str)  # type: ignore
    CASSANDRA_PASSWORD: str = decouple.config("CASSANDRA_PASSWORD", cast=str)  # type: ignore
    CASSANDRA_PORT: int = decouple.config("CASSANDRA_PORT", cast=int)  # type: ignore
    CASSANDRA_USERNAME: str = decouple.config("CASSANDRA_USERNAME", cast=str)  # type: ignore
    CASSANDRA_HOST: str = decouple.config("CASSANDRA_HOST", cast=str)  # type: ignore

    DB_TIMEOUT: int = decouple.config("DB_TIMEOUT", cast=int)  # type: ignore
    IS_DB_ECHO_LOG: bool = decouple.config("IS_DB_ECHO_LOG", cast=bool)  # type: ignore

    REDIS_HOST: str = decouple.config("REDIS_HOST", cast=str)  # type: ignore
    REDIS_PORT: int = decouple.config("REDIS_PORT", cast=int)  # type: ignore
    REDIS_PASSWORD: str = decouple.config("REDIS_PASSWORD", cast=str)  # type: ignore
    REDIS_DB: int = decouple.config("REDIS_DB", cast=int)  # type: ignore
    REDIS_MAX_CONNECTIONS: int = decouple.config("REDIS_MAX_CONNECTIONS", cast=int)  # type: ignore

    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)  # type: ignore
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str)  # type: ignore
    JWT_MIN: int = decouple.config("JWT_MIN", cast=int)  # type: ignore
    JWT_HOUR: int = decouple.config("JWT_HOUR", cast=int)  # type: ignore
    JWT_DAY: int = decouple.config("JWT_DAY", cast=int)  # type: ignore
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY

    ALLOWED_ORIGINS: list[str] = ["*"]
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]

    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    HASHING_ALGORITHM_LAYER_1: str = decouple.config("HASHING_ALGORITHM_LAYER_1", cast=str)  # type: ignore
    HASHING_ALGORITHM_LAYER_2: str = decouple.config("HASHING_ALGORITHM_LAYER_2", cast=str)  # type: ignore

    class Config(pydantic.ConfigDict):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True

    @property
    def set_backend_app_attributes(self) -> dict[str, str | bool | None]:
        """
        Set all `FastAPI` class' attributes with the custom values defined in `BackendBaseSettings`.
        """
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
