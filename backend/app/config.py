import os
from dataclasses import dataclass


@dataclass
class Settings:
    anthropic_api_key: str
    mongodb_uri: str
    cycle_app_api_url: str = ""
    cycle_app_api_key: str = ""


_settings = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = Settings(
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
            mongodb_uri=os.environ.get("MONGODB_URI", ""),
            cycle_app_api_url=os.environ.get("CYCLE_APP_API_URL", ""),
            cycle_app_api_key=os.environ.get("CYCLE_APP_API_KEY", ""),
        )

        # Validate required fields
        if not _settings.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        if not _settings.mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is required")

    return _settings
