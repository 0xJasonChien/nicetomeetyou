from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class SystemConfiguration(BaseSettings):
    SECRET_KEY: str = 'default-key'  # noqa: S105
    DEBUG: bool = True
    ALLOWED_HOSTS: tuple[str] = ('*',)


class Configuration(BaseSettings, SystemConfiguration):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / '.env',
        extra='ignore',
    )


configuration = Configuration()
