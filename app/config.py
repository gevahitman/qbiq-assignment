from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "weather-proxy"
    environment: str = "Development"

    # redis_url: str = Field(default="redis://redis:6379/0")
    redis_url: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    weather_base_url: str = "https://api.open-meteo.com/v1/forecast"
    geocoding_base_url: str = "https://geocoding-api.open-meteo.com/v1/search"

    cache_ttl_seconds: int = 600

    request_timeout_seconds: int = 10
    retry_attempts: int = 3


settings = Settings()
