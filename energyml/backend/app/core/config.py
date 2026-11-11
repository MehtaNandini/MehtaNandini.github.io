from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-backed application settings."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "EnergyML Research Platform"
    environment: str = "development"
    database_url: str = "sqlite:///./energyml.db"
    artifact_dir: Path = Path("../artifacts")
    dataset_dir: Path = Path("../datasets")
    default_random_seed: int = 42
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    max_request_bytes: int = 1_000_000

    @field_validator("artifact_dir", "dataset_dir", mode="before")
    @classmethod
    def expand_path(cls, value: str | Path) -> Path:
        return Path(value).expanduser()

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        allowed = {"development", "test", "production"}
        if value not in allowed:
            raise ValueError(f"environment must be one of {sorted(allowed)}")
        return value

    @field_validator("log_level")
    @classmethod
    def normalise_log_level(cls, value: str) -> str:
        return value.upper()

    api_prefix: str = Field(default="/api", pattern=r"^/")


@lru_cache
def get_settings() -> Settings:
    return Settings()
