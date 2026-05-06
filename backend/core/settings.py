from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    db_host: str = Field(..., min_length=1)
    db_user: str = Field(..., min_length=1)
    db_pass: SecretStr = Field(...)
    db_name: str = Field(..., min_length=1)
    db_port: int = Field(default=3306, ge=1, le=65535)

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("db_host", "db_user", "db_name")
    @classmethod
    def not_empty(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty or whitespace")

        return value

    @field_validator("db_pass")
    @classmethod
    def password_not_empty(cls, value: SecretStr) -> SecretStr:
        if not value.get_secret_value().strip():
            raise ValueError("Field cannot be empty or whitespace")
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
