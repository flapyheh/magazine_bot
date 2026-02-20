from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from typing import Type

class BotSettings(BaseSettings):
    BOT_TOKEN: str
    PAYMENTS_PROVIDER_TOKEN: str
    ADMIN_IDS: list[int] = Field(..., env='ADMIN_IDS')

    class Config:
        env_file = ".env"
        extra = "allow"

class PostgresSettings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str

    class Config:
        env_file = ".env"
        extra = "allow"

class LogSettings(BaseSettings):
    log_level: str
    log_format: str

    class Config:
        env_file = ".env"
        extra = "allow"

# В основном классе объявляйте поля с типами и значениями по умолчанию
class Settings(BaseSettings):
    bot: BotSettings = Field(default_factory=BotSettings)
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    log: LogSettings = Field(default_factory=LogSettings)

    @property
    def get_async_url(self) -> str:
        p = self.postgres
        return f"postgresql+asyncpg://{p.db_user}:{p.db_pass}@{p.db_host}:{p.db_port}/{p.db_name}"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()