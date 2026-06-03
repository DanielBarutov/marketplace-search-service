import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    still_url: str | None = os.getenv("POSTGRES_CONNECTION_STRING")
    if still_url:
        database_url: str = still_url.replace("postgres:", "postgresql+asyncpg:", 1)
    else:
        database_url: str = (
            "postgresql+asyncpg://postgres:postgres@localhost:5435/search_db"
        )
    kafka_bootstrap_servers: str = (
        os.getenv("KAFKA_BROKERS") if os.getenv("KAFKA_BROKERS") else "localhost:9092"
    )
    kafka_topic_ads: str = (
        os.getenv("KAFKA_TOPIC_MARKETPLACE_ADS")
        if os.getenv("KAFKA_TOPIC_MARKETPLACE_ADS")
        else "ads"
    )
    kafka_consumer_group: str = "search-service"
    ad_service_url: str = (
        os.getenv("AD_SERVICE_URL")
        if os.getenv("AD_SERVICE_URL")
        else "http://localhost:8002"
    )
