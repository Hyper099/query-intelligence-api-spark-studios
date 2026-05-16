from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #! Default Values
    app_name: str                       = "Query Intelligence API"
    database_url: str                   = "sqlite:///./query_intelligence.db"
    
    prompt_template_path: str           = "app/prompts/extract_query.j2"
    prompt_version: str                 = "v1"
    
    anthropic_api_key: str | None       = Field(default=None, alias="ANTHROPIC_API_KEY")
    anthropic_model: str                = Field(default="claude-haiku-4-5-20251001", alias="ANTHROPIC_MODEL")
    anthropic_timeout_seconds: float    = Field(default=10.0, alias="ANTHROPIC_TIMEOUT_SECONDS")
    anthropic_max_retries: int          = Field(default=2, alias="ANTHROPIC_MAX_RETRIES")

    rate_limit_requests: int            = 100
    rate_limit_window_seconds: int      = 60

    #! Override with .env config
    model_config                        = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
