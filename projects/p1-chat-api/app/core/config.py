"""App wide settings in one place"""
from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

    app_name: str = "LLM Chat Service"
    version: str = "0.4.0"
    model_name: str = "claude-haiku-5-5"
    anthropic_api_key: str
    service_api_key: str
    system_prompt_path: str = "prompts/system_v1.txt"
    log_level: str = "INFO"
    request_timeout_seconds: float = 30.0
    max_retries: int = 2
    provider_base_url: str | None = None

settings = Settings()