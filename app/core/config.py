from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Models
    REASONING_MODEL: str = Field(
        alias="REASONING_MODEL", default="gemini-3.1-pro-preview"
    )
    FORMATTING_MODEL: str = Field(
        alias="FORMATTING_MODEL", default="gemini-2.5-flash"
    )
    LOW_THINKING_BUDGET: int = Field(default=1024, alias="LOW_THINKING_BUDGET")
    MEDIUM_THINKING_BUDGET: int = Field(default=4096, alias="MEDIUM_THINKING_BUDGET")
    HIGH_THINKING_BUDGET: int = Field(default=16384, alias="HIGH_THINKING_BUDGET")

    # Trading 212
    TRADING_212_API_KEY: str = Field(alias="TRADING_212_API_KEY")
    TRADING_212_API_SECRET: str = Field(alias="TRADING_212_API_SECRET")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
