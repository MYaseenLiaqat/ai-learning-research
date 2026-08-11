from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./research.db"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None
    llm_timeout_seconds: int = 30
    ai_interaction_cap: int = 3

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
