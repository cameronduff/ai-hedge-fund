from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Models
    REASONING_MODEL: str = Field(
        alias="REASONING_MODEL", default="gemini-3.8-flash"
    )
    FORMATTING_MODEL: str = Field(
        alias="FORMATTING_MODEL", default="gemini-3.8-flash"
    )
    LOW_THINKING_BUDGET: int = Field(default=1024, alias="LOW_THINKING_BUDGET")
    MEDIUM_THINKING_BUDGET: int = Field(default=2048, alias="MEDIUM_THINKING_BUDGET")
    HIGH_THINKING_BUDGET: int = Field(default=4096, alias="HIGH_THINKING_BUDGET")

    # Trading 212
    TRADING_212_API_KEY: str = Field(alias="TRADING_212_API_KEY")
    TRADING_212_API_SECRET: str = Field(alias="TRADING_212_API_SECRET")
    TRADING_212_ENVIRONMENT: str = Field(default="demo", alias="TRADING_212_ENVIRONMENT")
    LIVE_TRADING_ENABLED: bool = Field(default=False, alias="LIVE_TRADING_ENABLED")

    # Pipeline Rate Limiting & Sizing
    MAX_CANDIDATES: int = Field(default=5, alias="MAX_CANDIDATES")
    RATE_LIMIT_DELAY_SECONDS: float = Field(default=4.5, alias="RATE_LIMIT_DELAY_SECONDS")
    MAX_POSITION_SIZE_PCT: float = Field(default=15.0, alias="MAX_POSITION_SIZE_PCT")
    MIN_CASH_RESERVE_PCT: float = Field(default=10.0, alias="MIN_CASH_RESERVE_PCT")

    @property
    def trading_212_base_url(self) -> str:
        if self.TRADING_212_ENVIRONMENT.strip().lower() == "live":
            return "https://live.trading212.com"
        return "https://demo.trading212.com"

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
