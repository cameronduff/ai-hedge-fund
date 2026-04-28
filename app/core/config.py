from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Models
    REASONING_MODEL: str = Field(
        alias="REASONING_MODEL", default="gemini-3-pro-preview"
    )

    # Trading 212
    TRADING_212_API_KEY: str = Field(alias="TRADING_212_API_KEY")
    TRADING_212_API_SECRET: str = Field(alias="TRADING_212_API_SECRET")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
