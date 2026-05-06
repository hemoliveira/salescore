from pathlib import Path

import pytest
from pydantic import SecretStr, ValidationError

from core.settings import BASE_DIR, Settings


def test_valid_config():
    settings = Settings(
        db_host="localhost",
        db_user="root",
        db_pass=SecretStr("123456"),
        db_name="company_sales_db",
        db_port=3306,
    )

    assert settings.db_host == "localhost"
    assert settings.db_user == "root"
    assert settings.db_pass.get_secret_value() == "123456"
    assert settings.db_name == "company_sales_db"
    assert settings.db_port == 3306


def test_default_db_port():
    config = Settings(
        db_host="localhost",
        db_user="root",
        db_pass=SecretStr("123456"),
        db_name="company_sales_db",
    )

    assert config.db_port == 3306


def test_env_file_is_resolved_from_backend_directory():
    env_file = Settings.model_config.get("env_file")

    assert isinstance(env_file, Path)
    assert env_file == BASE_DIR / ".env"
    assert env_file.is_absolute()


def test_text_fields_are_stripped():
    settings = Settings(
        db_host=" localhost ",
        db_user=" root ",
        db_pass=SecretStr("123456"),
        db_name=" company_sales_db ",
    )

    assert settings.db_host == "localhost"
    assert settings.db_user == "root"
    assert settings.db_name == "company_sales_db"


def test_db_host_cannot_be_empty():
    with pytest.raises(ValidationError):
        Settings(
            db_host="   ",
            db_user="root",
            db_pass=SecretStr("123456"),
            db_name="company_sales_db",
        )


def test_db_user_cannot_be_empty():
    with pytest.raises(ValidationError):
        Settings(
            db_host="localhost",
            db_user="   ",
            db_pass=SecretStr("123456"),
            db_name="company_sales_db",
        )


def test_db_name_cannot_be_empty():
    with pytest.raises(ValidationError):
        Settings(
            db_host="localhost",
            db_user="root",
            db_pass=SecretStr("123456"),
            db_name="   ",
        )


def test_db_pass_cannot_be_empty():
    with pytest.raises(ValidationError):
        Settings(
            db_host="localhost",
            db_user="root",
            db_pass=SecretStr("   "),
            db_name="company_sales_db",
        )


def test_db_port_must_be_greater_than_zero():
    with pytest.raises(ValidationError):
        Settings(
            db_host="localhost",
            db_user="root",
            db_pass=SecretStr("123456"),
            db_name="company_sales_db",
            db_port=0,
        )


def test_db_port_must_be_less_than_or_equal_to_65535():
    with pytest.raises(ValidationError):
        Settings(
            db_host="localhost",
            db_user="root",
            db_pass=SecretStr("123456"),
            db_name="company_sales_db",
            db_port=70000,
        )
