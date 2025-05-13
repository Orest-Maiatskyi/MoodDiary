from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import MySQLDsn, RedisDsn


class Config(BaseSettings):
    debug: bool
    mysql_dsn: MySQLDsn
    redis_dsn: RedisDsn

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


config = Config()
