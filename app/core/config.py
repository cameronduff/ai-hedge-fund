from typing import Any
from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=False, populate_by_name=True
    )

    REASONING_MODEL: str = Field(alias="REASONING_MODEL")
    API_KEY: str = Field(alias="API_KEY")


settings = Settings()
