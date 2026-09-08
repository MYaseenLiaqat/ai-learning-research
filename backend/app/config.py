from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./research.db"
    study_protocol_version: str = "v0.4"
    learning_module_version: str = "v0.4.0"
    system_prompt_version: str = "0.3.0"
    llm_provider: str = "groq"
    llm_base_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = "llama-3.1-8b-instant"
    llm_timeout_seconds: int = 30
    ai_interaction_cap: int = 8
    # Pilot parameter: maximum Supported-session duration in minutes.
    supported_phase_minutes: int = 20

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()