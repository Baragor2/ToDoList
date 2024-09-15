from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str

    TG_HASH_ALGORITHM: str

    class Config:
        env_file = ".env"


settings = Settings()


BASE_DIR = Path(__file__).parent.parent


class AuthSettings(BaseSettings):
    private_key_pass: Path = BASE_DIR / "secret_key.pem"


auth_settings = AuthSettings()


class MainBackend(BaseSettings):
    COMMENTS_API_ROOT: str = "http://0.0.0.0:8000/"


main_backend_settings = MainBackend()
