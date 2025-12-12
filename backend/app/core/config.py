from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = Field(default="dev", alias="APP_ENV")
    log_level: str = Field(default="info", alias="LOG_LEVEL")

    backend_host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")

    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")

    cloud_llm_endpoint: Optional[str] = Field(
        default=None, alias="CLOUD_LLM_ENDPOINT"
    )
    cloud_llm_token: Optional[str] = Field(default=None, alias="CLOUD_LLM_TOKEN")
    cloud_llm_model: Optional[str] = Field(default=None, alias="CLOUD_LLM_MODEL")

    gitlab_base_url: Optional[str] = Field(default=None, alias="GITLAB_BASE_URL")
    gitlab_token: Optional[str] = Field(default=None, alias="GITLAB_TOKEN")
    gitlab_project_id: Optional[int] = Field(default=None, alias="GITLAB_PROJECT_ID")


settings = Settings()
