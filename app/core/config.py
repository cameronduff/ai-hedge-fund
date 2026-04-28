from pydantic import Field

from pydantic.mypy import FIELD_FULLNAME
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODEL_CONFIG = SettingsConfigDict(
        env_file=".env", case_sensitive=False, populate_by_name=True
    )

    # Models
    REASONING_MODEL: str = Field(
        alias="REASONING_MODEL", default="gemini-3-pro-preview"
    )

    # API
    API_KEY: str = Field(alias="API_KEY")

    # Trading 212
    TRADING_212_API_KEY: str = Field(alias="TRADING_212_API_KEY")
    TRADING_212_API_SECRET: str = Field(alias="TRADING_212_API_SECRET")
    TRADING_212_PIE_ID: str = Field(alias="TRADING_212_PIE_ID")
    TRADING_212_USERNAME: str = Field(alias="TRADING_212_USERNAME")
    TRADING_212_PASSWORD: str = Field(alias="TRADING_212_PASSWORD")


settings = Settings()
