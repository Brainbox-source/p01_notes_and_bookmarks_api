from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    database_url: str

    # this tells pydantic to read the .env file
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")


# single instance of the settings to use throughout the app
settings = Settings()  # type: ignore[call-arg]
