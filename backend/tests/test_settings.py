from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

from core.settings import BASE_DIR, Settings


def test_valid_config():
    settings = Settings(
        database_url=SecretStr("postgres://user:pass@host/dbname?sslmode=require"),
    )

    assert settings.database_url.get_secret_value() == "postgres://user:pass@host/dbname?sslmode=require"


def test_env_file_is_resolved_from_backend_directory():
    env_file = Settings.model_config.get("env_file")

    assert isinstance(env_file, Path)
    assert env_file == BASE_DIR / ".env"
    assert env_file.is_absolute()


def test_database_url_cannot_be_empty():
    with pytest.raises(ValidationError):
        Settings(
            database_url=SecretStr("   "),
        )
