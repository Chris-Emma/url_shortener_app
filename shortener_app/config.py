from functools import lru_cache

from pydantic import BaseSettings
"""pydantic uses type annotation to validate data and manage settings"""

class Settings(BaseSettings):
    """Settings is a subclass of BaseSettings
    -It defines environment variables in the application"""
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

    class Config:
        """Enables pydantic to load environment variables from .env"""
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """Returns an instance of the Settings class
    - @lru_cache provides an option for caching"""
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings