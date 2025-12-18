from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    anthropic_api_key: str
    mongodb_uri: str
    cycle_app_api_url: str = ""
    cycle_app_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
