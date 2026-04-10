from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    google_api_key: str
    supabase_url: str
    supabase_service_key: str
    database_url: str
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_host: str = "https://cloud.langfuse.com"
    serpapi_key: str
    app_env: str = "development"
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "case_sensitive": False}


@lru_cache
def get_settings() -> Settings:
    return Settings()
