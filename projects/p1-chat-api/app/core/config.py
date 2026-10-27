"""App wide settings in one place"""
from pydantic_settings import BaseSettings, SettingsConfigDict 

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",env_file_encoding="utf-8")

    app_name: str = "LLM Chat Service"
    version: str = "0.2.0"
    model_name: str = "claude-haiku-5-5"
    anthropic_api_key: str
    system_prompt_path: str = "prompts/system_v1.txt"

settings = Settings()