from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    A configuration class that defines settings for the application
    Attributes:
        env_name (str): The name of the environment
        base_url (str): The base URL of the application
        db_url (str): The database URL.
    Config:
        env_file (str): Specifies the path to an .env file to load environment variables.
    """
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"

class Config:
    env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    """
    Retrieves the application settings as a singleton,
    using an in-memory cache to optimize repeated access.
    Returns:
        Settings: An instance of the Settings class with the application configuration.
    """
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings